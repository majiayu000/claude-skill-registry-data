---
name: intentumdiff-dev-loop
description: >-
  The development flywheel for the IntentumDiff repo — how to take a unit of work from idea to
  a verified, documented, committed change without breaking the invariants. Use this whenever
  you implement a feature or fix, pick up work from the backlog, respond to an audit finding,
  or maintain the repo. It gives the loop (sense → plan → change the RIGHT layer → verify with
  the RIGHT commands → document → commit), a layer-decision guide (Rust engine vs Python shell
  vs extension), the exact build/test/rebuild rules per layer (including when a maturin
  rebuild is and isn't needed), how to investigate test failures to root cause, how to avoid
  stick-plaster fixes, and the commit conventions. Read intentumdiff-architecture first; pull in
  intentumdiff-engine / -vscode / -release-notes / -perceptual-asset-diff for the area you touch,
  and intentumdiff-architecture-audit for the "sense" step.
---

# IntentumDiff — Development flywheel

A repeatable loop so the repo can be continually developed without regressing its contracts.
Each turn of the wheel: **sense → plan → change → verify → document → commit.**

## 1. Sense — where the next unit of work comes from

- **Backlog:** `docs/BACKLOG.md` (roadmap, RC gate, "Known issues (pre-existing)"). The RC gate
  section says what must stay green.
- **Audit:** run `intentumdiff-architecture-audit` to surface invariant violations and debt, or
  focus it on the area you're about to touch.
- **Failing/xfail tests:** treat red tests as actionable signal — investigate, don't just
  report (see §4).

Pick one coherent unit. If it sprawls, split it and note the rest in the backlog rather than
ballooning one change.

## 2. Plan — decide the RIGHT layer before typing

| The change is about… | Layer / where it lives |
|---|---|
| Parsing, matching, diffing, grouping, refactoring/move detection, invariances, presentation, guardrails, cross-file, NodeFacts | **Rust core** `crates/rust-core-host` (the engine). New engine logic goes here — not Python. |
| API/CLI shape, VCS/source collection, config, LiveServer/LSP/HTTP protocol, DTO compatibility | **Python shell** `src/intentumdiff/` |
| Diff surfaces, CodeLens/Peek/decorations, review panel, intent "what/why", release notes, content classes, asset viewer, theme | **Extension** `plugins/vscode/` |

If you find yourself adding semantic processing to `src/intentumdiff/analysis/` or
`core/engine.py`, stop — that's the test-oracle, not the product engine (see
`intentumdiff-architecture` → engine boundary). Confirm the authoritative fix belongs in Rust.

## 3. Change — follow the area skill + the invariants

Read the relevant skill for the area (`intentumdiff-engine`, `-vscode`, `-release-notes`,
`-perceptual-asset-diff`) and honor the hard rules from `intentumdiff-architecture`: engine
boundary, native-first diff, theme-native styling, BYOK/privacy, no committing `boo.py`/
`image.png`, don't touch the MonacoEditorInterfaceDesign reference.

**Fix at the source, not downstream (no stick-plasters).** After a change, ask: "am I cleaning
up a mess, or preventing it?" If your fix compensates for something built wrong upstream, go
fix the upstream construction. The change-group index-space bug is the canonical example — the
right fix was making the producer emit `[]`, not tagging it so a later pass erases phantom
indices. Keep a late reconciliation pass only as a principled contract boundary, never as cover
for a broken producer.

## 4. Verify — the RIGHT commands per layer (and when to rebuild)

**Rebuild rule:** only Rust source changes need a core rebuild.
```bash
# Rust core changed → rebuild (ALWAYS --release; stop the extension host on Windows first).
# The crate is pyo3-FREE (#B.6): run maturin from the REPO ROOT so it reads pyproject.toml
# (`bindings = "cffi"`) — NOT `cd crates/rust-core-host` (that dir has no pyproject → maturin errors).
Get-Process -Name intentumdiff -ErrorAction SilentlyContinue | Stop-Process -Force   # Windows
RUSTUP_TOOLCHAIN=1.95.0 maturin develop --release   # from repo root; cffi cdylib, not a pyo3 .pyd
```
This builds a bare cdylib at `.venv/Lib/site-packages/intentumdiff/intentumdiff_rust_core/intentumdiff_rust_core.<ext>`
(`.dll`/`.so`/`.dylib`); `rust_core._load_backend()` ctypes-loads it over the C ABI (`intentumdiff_call`).
Pure-Python (`src/intentumdiff/`) or TypeScript (`plugins/vscode/`) changes need **no** maturin rebuild.

**A stale in-tree `.pyd` or standalone install SHADOWS the fresh cdylib — clear both or your
rebuild is a no-op.** `_load_backend()` auto-detects: it uses a pyo3 *extension* if `find_spec`
finds one whose origin ends in an extension suffix (a leftover `src/intentumdiff/intentumdiff_rust_core.pyd`
from the old pyo3 era, or a `pip install`ed standalone `intentumdiff_rust_core`), else the ctypes
path. A leftover pyo3 artifact silently exercises yesterday's engine. After any core rebuild:
```bash
rm -f src/intentumdiff/*.pyd                                   # kill the retired pyo3 in-tree shadow
.venv/Scripts/python.exe -m pip uninstall -y intentumdiff_rust_core 2>$null   # kill any standalone pyo3 install
```
Verify which backend is live before trusting any probe:
`python -c "import intentumdiff.rust_core as r; print(type(r._load_backend()).__name__)"` must print
`_CtypesBackend` (force it with `INTENTUMDIFF_RUST_CORE_CTYPES=1`; `INTENTUMDIFF_RUST_CORE_PYO3=1` selects pyo3 if one is present).

**Test the layer you touched (and the ones downstream of it):**
```bash
# Python
.venv/Scripts/python.exe -m pytest tests/unit -q          # add PYTHONUTF8=1 for non-ASCII prints
# Rust
(cd crates/rust-core-host && cargo test --release)   # NOT a workspace member; -p from the root fails
# Extension
cd plugins/vscode && npm run lint && npm run test          # lint = tsc --noEmit; test = node --test
```

**Reproduce engine behavior directly** instead of guessing:
`SemanticDiffer().diff_strings(old, new, filename, language_hint=...)` and inspect `changes` /
`change_groups`. For the extension, use the panel-render harness (see `intentumdiff-vscode`) +
the Claude Preview MCP for visual/interaction checks.

**Investigating a test failure — root cause, not report:**
1. Get the assertion: run it with `-q --tb=short`.
2. Read the test's *intent* — is the expectation still correct?
3. Classify: genuine regression (worth `git bisect`) vs documented gap (`xfail`) vs stale
   assertion/reference (fix the reference/expectation — honestly, not by masking).
4. Confirm pre-existing vs introduced: `git stash push <your changed files>` → re-run → pop.
   Same failure without your changes ⇒ pre-existing; say so, and document it in the backlog if
   it's undocumented (the RC gate treats undocumented red tests as blockers).

Never mark work done with failing tests, partial implementation, or unresolved errors.

**Skipped and xfailed tests are DEBT, not a resting state — investigate and drive them down.**
A green summary that hides `N skipped, M xfailed` is not "all passing". Every skip/xfail must be
*understood and justified*, and the counts must trend to zero — a rising count is a regression
signal. Capture the reasons with `pytest tests/unit -rsx --tb=no` and triage:

- **xfailed = a documented engine/oracle gap that fails loudly (XPASS) when fixed.** Sources:
  corpus `mutation_xfail` in `*.expect.json` (#46 "content mutation reported style-only" class),
  `edit_matrix.expect.json` `xfail` verbs, `scenario_suite.py` `xfail=` cases, and explicit
  `pytest.xfail(...)` sites (e.g. go import-reorder oracle gap, java annotation-reorder engine
  gap). These are the exact debt the #57 Rust migration retires — **fix the engine (in Rust), then
  delete the marker** (a language flip routinely turns several xfails XPASS, as scala/perl did).
  Never *add* an xfail to make a change "pass" — an xfail is a tracked promise to fix (backlog/issue),
  not a mute button.
- **skipped = mostly environmental gates; split reducible from irreducible.**
  *Reducible (recover the coverage):* a missing optional dep (`importorskip("duckdb")`,
  `importorskip("P4")` → `pip install` it) or an unbuilt Wasm parser (`"<lang>_parser.wasm not
  built"` → build it, see `intentumdiff-build`). *Irreducible (must carry an explicit reason and be
  justified/tracked):* platform-only (`skipif sys.platform == "win32"`, named-pipe), a
  non-applicable engine variant (`"no rust support"`/`"no rust finalizer"` parametrization), or
  optional browser/integration smokes (playwright/fastapi/uvicorn). Irreducible skips stay, but
  each needs a reason string and a home in the backlog — they must not silently accumulate.

When a change legitimately can't clear a skip/xfail this unit, file/annotate a backlog entry with
the plan, don't just leave the count higher.

## 5. Document

- Record durable, non-obvious decisions and known-issues in `docs/BACKLOG.md`; reconcile any
  doc that now contradicts the code (`CLAUDE.md`, `docs/architecture/*`).
- If a finding is bigger than the current unit, add a backlog entry instead of scope-creeping.
- **File a tracked GitHub issue for every out-of-scope gap you discover — don't let it evaporate.**
  When you hit a bug, parity divergence, or blocker while doing something else (e.g. a language
  that won't flip, a residual-noise follow-up, a shared-pass gap), open a GitHub issue with
  `gh issue create` right then: precise repro (default-vs-routed where relevant), the root-cause
  *direction*, an acceptance contract, and `Related` cross-refs. This is not optional bookkeeping —
  it's how the next unit gets picked up. The #57 flip triage did exactly this (#63 schema profiles,
  #64 html path-profile, #66 powershell move-recovery, #67 graphql compaction, #65 skip/xfail
  burn-down); each blocked flip left a ready-to-work issue instead of a mental note. Label it
  (`rust-core`/`language-profile`/`diff-quality`/`enhancement`), and when the fix later lands +
  is tested, mark the issue `ready-for-review` (never close it yourself). A buried backlog line or
  an in-flight observation is not tracking; a labelled issue is.
- **Feed the flywheel: capture what was unclear back into a skill.** Whenever something in this
  repo was surprising or cost you real digging, add a concise, source-grounded note to the
  closest `.claude/skills/` skill (a gotcha, a known hotspot, a corrected assumption) — or
  propose a new skill. Prefer stable symbol/function anchors over line numbers, explain the
  *why*, and don't just restate CLAUDE.md or one docstring. The skill set is meant to be
  self-improving; a fact learned the hard way and not written down gets re-learned every
  session. If it was a real defect/violation, log it in `docs/BACKLOG.md` too.

## 6. Commit

- Branch off `main` if you're on it; otherwise commit to the working branch. Do **not** push
  or open a PR unless asked.
- **Do not stage** the repo-root artifacts `boo.py` / `image.png` (or other pre-existing
  unrelated changes) — stage only the files for this unit.
- End every commit message with:
  ```
  Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>
  ```
- Write the message to explain the *why* and the root cause, not just the what. Note whether it
  needs a maturin rebuild.

## Then turn the wheel again

Re-run the audit (or the specific check) to confirm the finding is gone and nothing regressed,
pick the next unit, and repeat. The flywheel: each verified, documented change makes the next
one safer and the audit shorter.

## Large-scale code deletion (learned in the #57 stage-4b retirement, 2026-07-15)

When cutting whole regions/functions out of a big module (differ.py):

1. **Line-range block cuts take collateral**: module-level CONSTANTS defined between
   deleted functions vanish silently (`_GENERIC_STRING_LABELS` / `_NAMED_ENTITY_NODE_TYPES`
   were still used by surviving functions → 422 gate failures as `NameError`s at runtime,
   not import time). After any cut, run `python -m pyflakes` over every touched file and
   grep for "undefined" — it catches this class statically in seconds.
2. **Import success ≠ correctness**: `import intentumdiff.differ` passes with missing
   module-level names if they're only referenced inside function bodies. Collection
   passing means little; the pyflakes pass is the cheap gate.
3. **Behavior pinned to the deleted layer hides in flag-flips**: the commit differ
   deliberately re-ran batch-declined files with `experimental_rust_core=False` ("don't
   retry rust") — post-retirement that flag means the token-fallback kill switch, not
   "python pipeline". Grep for config mutations (`model_copy(update=`) of engine flags
   when retiring an engine tier; each one encodes an assumption about what the fallback IS.
4. **Ledgers and fixtures reference file paths**: `test_engine_boundary`'s debt-path list
   and `semanticdiff_competitor_gap_matrix.json`'s implementation_paths assert files EXIST.
   Deleting a module means sweeping `grep -rn "<path>" tests/ docs/` for path-existence pins.
