---
name: intentumdiff-repo-split
description: >-
  Rules and mechanics for splitting the IntentDiff monorepo into the 76 polyglot repos under
  buchochelliq-labs (intentdiff-core, -plugin-sdk, -registry, -python, -go, -java, -vscode, and
  intentdiff-<lang>-parser x69). Use this whenever you create, populate, or scaffold a split repo,
  decide which files/docs/skills go where, run scripts/create-split-repos.sh, or wire the
  SDK-masters-skills sync. It states the SETTLED decisions (files-only import — NO history;
  per-parser granularity; private; the existing `intentdiff` repo is UNTOUCHED), the per-repo file
  and skill/doc mapping, and the sequencing rule (extraction happens at the readiness cutover, not
  before). Read intentdiff-architecture for the target topology and intentdiff-plugin-repo for the
  parser-repo rules the SDK masters.
---

# IntentDiff — Repo split (monorepo → 76 polyglot repos)

The end state (issue #82, `docs/TARGET_ARCHITECTURE.md`): one shared Rust backend + thin C-ABI
bindings, across **77 repos** in `buchochelliq-labs` — 76 NEW + the existing `intentdiff`.

## Settled decisions (do NOT re-litigate)

1. **Files-only import — bring NO commit history.** Each repo starts from ONE clean initial commit
   of its file subtree. No `git filter-repo` / subtree-split. Rationale: avoids leaking
   cross-component history, old secrets, large blobs, and the never-commit artifacts.
2. **The existing `buchochelliq-labs/intentdiff` repo is the ARCHIVE of record — leave it
   UNTOUCHED.** `intentdiff-core` is a brand-NEW repo (maintainer overrode the earlier "rename the
   existing repo" plan, 2026-07-22). Files-only means the monorepo is the only place blame/provenance
   history survives — do not delete it.
3. **One repo per parser** (`intentdiff-<lang>-parser` x69, from `crates/parsers/<lang>`), created
   via a template + automation, not by hand. See [intentdiff-plugin-repo].
4. **All repos PRIVATE** (match the org). `intentdiff-core` flips to public at release.
5. **Sequencing: extraction is Phase C — it happens at the READINESS CUTOVER**, after the Python
   shell is genuinely thin (GitPython dropped #98, config/cache/registry ported, C ABI + pyo3
   retired). Populating source before then just creates a snapshot that goes stale as the monorepo
   keeps moving. The monorepo stays green and is the source of truth until cutover. Scaffolding
   (README + docs + skills + build manifests + the SDK skill-master/sync) MAY be set up earlier.

## The repos + what files each gets

| Repo | Status | File subtree it receives |
|---|---|---|
| `intentdiff-core` | new | `crates/rust-core-host`, `index-engine(-lib)`, `{html,llm,patch,terminal}-renderer`, `crates/patches` + a standalone workspace `Cargo.toml`, C-ABI header, the `intentdiff` CLI |
| `intentdiff-plugin-sdk` | new | `crates/sdk`, `crates/sql-parser-lib`, `plugins/wit/plugin.wit`, `templates/plugin-template/` — **root of the DAG; masters the plugin skills** |
| `intentdiff-<lang>-parser` x69 | new | `crates/parsers/<lang>/` + a standalone `Cargo.toml` depending on the SDK. See [intentdiff-plugin-repo] |
| `intentdiff-registry` | new | `registry.yaml` schema + generated catalog + the vetting CI (root of trust) |
| `intentdiff-python` | new | the thin `src/intentdiff` shell, `pyproject.toml`, Tier-A/C tests |
| `intentdiff-go` / `intentdiff-java` | new | thin C-ABI binding scaffolds |
| `intentdiff-vscode` | new | `plugins/vscode`, `apps/review-shell` — **VSIX BUNDLES the native Rust core + ALL OOB `.wasm` plugins, NO Python** (per-platform, self-contained; spawns the native live-server). Decided 2026-07-22. |
| `intentdiff` (existing) | KEEP | untouched archive of full history |

## Docs + skills travel with the code (each repo gets its relevant subset)

Skills are documentation — copy the relevant `.claude/skills/intentdiff-*` into each repo:

| Repo | Skills it carries |
|---|---|
| `intentdiff-core` | architecture, engine, guardrails, language-profiles, diff-expectations, perceptual-asset-diff, build, testing, dev-loop |
| `intentdiff-<lang>-parser` | **plugin-repo** (SDK-mastered) + parsers, build, testing |
| `intentdiff-plugin-sdk` | plugin-repo (MASTER), parsers, architecture, build |
| `intentdiff-vscode` | vscode, release-notes, perceptual-asset-diff |
| `intentdiff-python` | architecture (binding view) + usage |
| `intentdiff-registry` | plugin-repo (trust rules) + a registry-schema doc |

Cross-cutting skills (architecture, dev-loop, build, testing) land in most repos; area skills only
in their repo.

**Docs are AUTHORED FRESH — do NOT copy the monorepo `docs/`.** The existing docs are a
*reference*, not a source to duplicate: read them, then write a tight, repo-scoped set (README +
the few docs that repo actually needs). Tighten and trim as you go — the monorepo docs accreted
history the split repos don't need. **No competitor references** (no "vs <tool>", "unlike
<competitor>", competitor names, or benchmark-against framing) anywhere in the new docs or READMEs —
describe what IntentDiff does on its own terms. Skills (dev tooling) are copied as above; prose docs
are rewritten.

## The SDK masters the plugin skills — copy, don't fork

`intentdiff-plugin-sdk` holds the **canonical** copy of the plugin-facing skills
(`intentdiff-plugin-repo`, `intentdiff-parsers`). Parser repos get a STAMPED COPY at creation; the
repo TEMPLATE carries it. **Never edit a parser repo's copy** — edits go to the SDK master, then a
`sync-skills` job in the SDK fans the update out to every `intentdiff-*-parser` (a PR per repo, or a
push, keyed off the org's parser list). This is the same "template + automation, not 69 hand-edits"
rule as the repos themselves. Avoid git submodules (one is clean; 69 is friction).

## GitHub Actions — split per repo, don't copy wholesale (double-check first)

The monorepo's 5 workflows are monorepo-shaped (test/build EVERYTHING). Distribute the relevant
job to each repo — do NOT copy all 5 into every repo. Keep the **pinned action SHAs** (#88).

| Monorepo workflow / action | Goes to |
|---|---|
| `tests.yml` — cargo pins | `intentdiff-core` (Tier A) + each parser (Tier B) |
| `tests.yml` — pytest | `intentdiff-python` |
| `publish.yml` — platform wheels | `intentdiff-python` (native lib → `intentdiff-core`) |
| `build-wasm.yml` | each `intentdiff-<lang>-parser` |
| `release-media-manifest-gate.yml` | `intentdiff-vscode` |
| `security.yml` — semgrep(py) / cargo-audit(rust) | split by language into the relevant repos |
| `.github/actions/semantic-diff` (composite) | `intentdiff-core` (the product's CI action) |

**Parser repos share ONE reusable workflow owned by the SDK** — `intentdiff-plugin-sdk` publishes a
reusable `build-wasm + parity/fuzz + register` workflow; each parser repo's `.github/workflows/`
is a thin CALLER (`uses: buchochelliq-labs/intentdiff-plugin-sdk/.github/workflows/parser-ci.yml@…`).
A CI fix is then one edit in the SDK, not 69. Same rule as the skills. Before moving any workflow,
double-check it for monorepo path assumptions (e.g. the #94 dbt cross-tree WIT path) and strip them.

## Hygiene — never add files that shouldn't be there

The migration must not re-introduce the junk we just removed. Every populate step:
- Honors `.gitignore` + the never-commit list: `boo.py`, `image.png`, `*.orig`, `*.pyd`, `vendor/`,
  build outputs (`target/`, staged `.wasm` except a plugin's intentionally-shipped set), diagnostic
  dumps (`artifacts/*` except CI-gated release media), `__pycache__`, editor/OS cruft.
- Uses an **allowlist per repo** (copy only that repo's declared subtree) rather than a blanket copy.
- Ships each repo's `.gitignore` with the same guards so nothing junk can be re-added post-split.

## Automation

- **Creation:** `scripts/create-split-repos.sh` — idempotent (SKIPS existing, so it never touches
  `intentdiff`), `DRY_RUN=1` previews, private + empty. Already run (76 created 2026-07-22).
- **Population (files-only):** for each repo — copy its subtree honoring `.gitignore` + the
  never-commit list (`boo.py`, `image.png`, `*.pyd`, `vendor/`, staged `.wasm`), drop in the
  standalone build manifest, `git init` → one commit → push. Extend the creation script into a
  `populate-split-repos.sh` when the cutover comes.

## Hard rules

- **Never modify the existing `intentdiff` repo** as part of the split.
- **Never bring history** — files-only, one initial commit per repo.
- **Never copy the never-commit artifacts** or gitignored build outputs into a new repo.
- **Each extracted crate needs its OWN build manifest** (monorepo shares one workspace `Cargo.toml`;
  a parser repo depends on the published/vendored SDK, not the workspace).
- **Do not populate source before the readiness cutover** — scaffolding only until Python is thin.
