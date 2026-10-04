---
name: intentumdiff-architecture
description: >-
  Orientation and ground rules for the IntentumDiff / py-semantic-diff repository (a
  Rust+Python semantic-diff engine with a VS Code extension). Use this skill FIRST
  whenever you start any task in this repo — implementing a feature, fixing a bug,
  reviewing code, or answering "how does X work / where does X live". It maps the repo,
  states the Rust-vs-Python engine boundary, gives the exact build/test/run commands
  (including the maturin --release and .pyd-locking gotchas that silently waste hours),
  and lists the hard invariants you must not break. If a task touches the diff engine,
  the extension UX, release notes, or images, read this then hand off to the more specific
  intentumdiff-* skill. Trigger even when the user doesn't say "architecture" — any work in
  this repo benefits from it.
---

# IntentumDiff — Architecture & Ground Rules

IntentumDiff is a **semantic** diff engine: it compares two versions of a file at the
syntax-tree level (not line-by-line) to say *what changed and why it matters* —
refactors vs behavior changes, moves, style-only noise, guardrail violations — and
surfaces that as a CLI, a Python API/LiveServer, and a **VS Code extension**.

## The one rule that governs everything: the engine boundary

**The Rust core is the engine. Python is a thin product shell.** This is not
aspirational cleanup — it is the release contract.

- **Rust owns** (`crates/`): parsing (Wasm parser components), semantic-tree
  construction, matching, edit generation, refinement, moves, refactoring detection,
  invariances, presentation/grouping, guardrails, schema interpretation, cross-file
  analysis, and the final `SemanticDiff` output. The primary engine crate is
  `crates/rust-core-host` (built as the `intentumdiff_rust_core` PyO3 extension).
- **Python owns** (`src/intentumdiff/`): public API/CLI, VCS/source collection, config,
  LiveServer/LSP/HTTP protocol glue, DTO compatibility, packaging/docs/release tooling.
- **New processing logic goes into Rust, never Python.** Python engine modules
  (`intentumdiff.analysis.*`, `intentumdiff.core.engine`) remain only as a *temporary test
  oracle* until each slice is parity-certified in Rust. Do not extend them.

Sources of truth (read when the boundary matters):
`docs/RUST_PYTHON_ENGINE_ARCHITECTURE.md` and `docs/ENGINE_BOUNDARY_AUDIT.md`. The strict
gate runs with `INTENTUMDIFF_ENFORCE_RUST_ONLY_ENGINE=1`.

### North star: Rust is the *complete* backend; bindings are thin (roadmap — `docs/TARGET_ARCHITECTURE.md`, #82)

The boundary is *tightening*. The end goal is **one shared Rust core with thin polyglot
bindings** (Python / Go / Java / …). Today "Rust owns the engine" but Python still owns
real *backend* subsystems — git/VCS (`sources/git_source.py`), config (`core/config.py`),
the plugin registry client (`plugins/hub.py`), the live-server (`live_server.py`), the
cache (`cache/sqlite_store.py`). Under the north star those are all Rust too, because a Go
or Java binding cannot share a Python file. The litmus test for new code: **"would a Go
binding need this, and could it use the Python version?"** If yes/no → it is backend →
Rust, not a language binding. This is the readiness bar for the eventual repo split
(#90–#101); nothing is being executed yet, but *don't add new backend logic to the Python
layer*.

> Nuance worth knowing: the default single-file live diff uses the **certified native
> batch path** (parsing + diff in Rust via `convert_cst`, bypassing the Wasm parser).
> A Python fallback still exists for unsupported surfaces. `docs/ARCHITECTURE.md`
> documents the (legacy) Python pipeline internals — accurate for behavior, but treat
> Rust as where new work lands.

## Repo map (where things live)

```
src/intentumdiff/            Python shell: differ.py (orchestrator), core/models.py
                           (frozen pydantic v2), analysis/ (shrinking remnant:
                           guardrails, invariances, cross_file, diagnostics,
                           schema_resolver/user_schemas, keyed_profiles (guardrails
                           still uses its keyed identity helpers) + resource_profiles
                           (hcl/puppet enricher pending its Rust port, #90);
                           refinement/presentation/moves AND the query/statement/path
                           profile modules were deleted — the Rust core is the only
                           engine and is AUTHORITATIVE for profile-label enrichment,
                           no Python fallback #90), sources/, live_server.py,
                           lsp_server/, serve/
crates/                    Rust: rust-core-host (the engine), parsers/* (Wasm parser
                           components per language), index-engine, renderers, sdk
plugins/vscode/            The VS Code extension (TypeScript). src/ + test/ + media/ + docs/
plugins/intentumdiff_dbt/    Separately-packaged dbt plugin
docs/                      Architecture + subsystem docs + BACKLOG.md (roadmap/known issues)
tests/unit, tests/integration, tests/security   Python test suites + fixtures/
```

## Build, test, run (copy-paste, and the traps)

**Rust core** (needed after any change under `crates/rust-core-host/`):
```bash
# From the REPO ROOT (the crate is pyo3-free since #B.6 — maturin reads pyproject.toml's
# `bindings = "cffi"`; `cd crates/rust-core-host && maturin …` now errors, no pyproject there).
RUSTUP_TOOLCHAIN=1.95.0 maturin develop --release   # ALWAYS --release
rm -f src/intentumdiff/*.pyd                           # kill any retired pyo3 in-tree shadow
```
- **Always `--release`.** A plain `maturin develop` is a *debug* core: functionally
  identical but ~20–50× slower on compute paths (the perceptual image diff drops from
  ~6 s to ~0.3 s purely from `--release`). Details: `docs/BUILDING.md`.
- **Windows lock:** the extension keeps the core `.dll` loaded. Stop it before rebuilding
  or the install fails with `Access is denied (os error 5)`:
  `Get-Process -Name intentumdiff | Stop-Process -Force`. The in-tree
  `src/intentumdiff/intentumdiff_rust_core.pyd` SHADOWS every install (loader tries
  `intentumdiff.intentumdiff_rust_core` first) — after building, copy the fresh `.pyd` over it
  and verify via `_load_backend().__file__`, not a bare import (full recipe:
  intentumdiff-build's stale-shadow bullet).
- **Pure Python or TypeScript change → no maturin rebuild.** Only rebuild for Rust
  source changes.

**Python tests:** `.venv/Scripts/python.exe -m pytest tests/unit -q` (Windows; prefix
`PYTHONUTF8=1 PYTHONIOENCODING=utf-8` if printing non-ASCII).

**Rust tests:** `(cd crates/rust-core-host && cargo test --release)` — NOT a workspace member; `-p` from the root fails.

**Extension:** `cd plugins/vscode && npm run lint && npm run test` (`lint` is `tsc
--noEmit`; `test` is `node --test` on compiled `out/`). Integration tests gate on
`INTENTUMDIFF_SKIP_LIVE_DIFF=1`.

## Repo I/O (OneDrive) — search gotcha & how to work around it

This repo lives on a **OneDrive-synced path** (`C:\Users\…\OneDrive\Documents\GitHub\py-semantic-diff`),
so filesystem I/O is slow and tree-wide operations frequently **time out (~20s)** or get
backgrounded. Observed this session: `Glob "**/plugin.wit"`, unscoped ripgrep, and `find .` all
timed out; a broad `find` got auto-backgrounded. Work around it:

- **Prefer `Read` on a known direct path over discovery.** The repo map above + a file's imports
  usually tell you the exact path — read it directly instead of globbing to find it (e.g. the
  profile modules are named in `analysis/presentation.py`'s imports; the WIT is
  `src/intentumdiff/plugins/wit/plugin.wit`).
- **Scope every `Grep`/`Glob` to a subdirectory**, not the repo root — e.g. search
  `plugins/vscode/src`, `src/intentumdiff/analysis`, or `crates/rust-core-host/src`, never `**` from
  the top.
- **Avoid `find` / unscoped `**` globs.** If you must search broadly, target one subtree at a time.
- **Don't block on a long scan** — if a shell search gets backgrounded, abandon it and re-run a
  scoped tool instead of waiting.
- **Keep heavy/temporary output off the synced tree.** OneDrive can sync files mid-write (flagged
  as a secondary cause of slow perceptual-diff artifact writes) — write scratch files, generated
  panels, and eval workspaces to the session scratchpad/`$TEMP`, not into the repo.

## Hard invariants — do NOT break these (from CLAUDE.md)

- **Engine:** don't move processing/analysis logic into Python; it belongs in Rust.
- **VS Code diff is native-first:** open diffs with `vscode.diff` (left = read-only
  `intentumdiff-base:` from `git show <ref>:<path>`, right = the real editable working file).
  Do **not** reintroduce Monaco, `createDiffEditor` webview embeds, the `media/monaco/`
  bundle, or the retired gap machinery (`gapStates`, `expandGap`, floating chevrons).
- **Theme-native styling:** chrome uses `--vscode-*` vars; change categories use the
  contributed `intentumdiff.semanticChanges.*` color IDs. No hardcoded chrome hex literals,
  no bundled Google Fonts / JetBrains Mono. Codicons only (`codicon codicon-*`) — never
  ship custom chrome SVG icons. Must read in Dark+, Light+, and High-Contrast.
- **Privacy (BYOK):** never bundle an API key or run a paid proxy. The LLM explainer is
  opt-in; keys live in VS Code SecretStorage, never settings.json. A consent modal precedes
  any send. Default sends a locally-derived privacy-safe fact sheet (counts/enums/flags — no
  source, identifiers, or literals); verbatim source goes only to a **local** endpoint. Unit
  tests do **no** network.

## Where to go next (the other intentumdiff-* skills)

- **`intentumdiff-engine`** — diff internals: models, GumTree matching, change groups and the
  **index-space contract** (`raw_change_indices`), NodeFacts, invariances, presentation.
- **`intentumdiff-vscode`** — the extension: native diff, CodeLens/Peek/decorations, review
  panel, content classes, theme/privacy rules.
- **`intentumdiff-release-notes`** — intent "what/why", risk buckets, deterministic + BYOK-LLM
  narrative.
- **`intentumdiff-perceptual-asset-diff`** — image/asset diff (engine artifacts + viewer).
- **`intentumdiff-architecture-audit`** — reason over the codebase and produce a findings
  report (the flywheel's "find all the problems" step).
- **`intentumdiff-dev-loop`** — the flywheel: pick work → change the right layer → verify →
  document → commit.
- **`intentumdiff-build`** — build any layer from source (Rust core, Wasm parsers, extension,
  dbt plugin), the toolchain pins, and the rebuild-or-not decision.
- **`intentumdiff-testing`** — add and run tests across Python / Rust / the extension, the
  conventions, and the pre-existing-vs-introduced technique.
- **`intentumdiff-parsers`** — the Wasm parser plugins + WIT contract; add or fix a language at
  the grammar/tree level.
- **`intentumdiff-language-profiles`** — the per-language diff tuning (keyed/review/scaffold node
  types) above the parser; where most per-language quality bugs live.
- **`intentumdiff-guardrails`** — protected-config policy (`intentumdiff.yaml`), keyed/resource
  identity, important-vs-immutable severity.

## Doc index (read on demand)

| Need | Doc |
|---|---|
| **Target architecture (polyglot core, thin bindings, repo split)** | **`docs/TARGET_ARCHITECTURE.md`** (roadmap, #82) |
| Engine boundary / migration gate | `docs/RUST_PYTHON_ENGINE_ARCHITECTURE.md`, `docs/ENGINE_BOUNDARY_AUDIT.md` |
| Full pipeline + data models + security | `docs/ARCHITECTURE.md` |
| Build the Rust core, toolchain, gotchas | `docs/BUILDING.md` |
| Roadmap, RC gate, known issues | `docs/BACKLOG.md` |
| Extension diff/viewer design | `plugins/vscode/docs/architecture/diff-viewer.md` |
| Privacy / BYOK guarantees | `plugins/vscode/PRIVACY.md` |
| Guardrails, schema profiles, perceptual diff | `docs/GUARDRAILS.md`, `docs/SCHEMA_AWARE_DIFF_PROFILES.md`, `docs/PERCEPTUAL_ASSET_DIFF.md` |

The repo-root `CLAUDE.md` is the compressed version of these rules and is authoritative if
anything here conflicts with it.
