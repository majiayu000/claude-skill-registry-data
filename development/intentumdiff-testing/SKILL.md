---
name: intentumdiff-testing
description: >-
  How to add and run tests across every layer of the IntentumDiff repo — Python (pytest), Rust
  (cargo), and the VS Code extension (node:test) — plus the conventions and gotchas that make
  tests actually run and actually mean something. Use this whenever you write a test, run the
  suites, add a fixture, reproduce engine behavior in a test, investigate a failing/xfailed
  test, or check the release-candidate gate. It gives the exact run commands per layer, how to
  add a test in each (including the extension's easy-to-miss "add the file to the test:unit
  list or it silently won't run" trap), the no-network / determinism rules, the
  stash-to-confirm-preexisting technique, and how to treat regressions vs documented gaps. Read
  intentumdiff-build to build before testing, and intentumdiff-dev-loop for where testing fits the
  workflow.
---

# IntentumDiff — Adding & running tests

Three test stacks. Test the layer you changed **and the ones downstream of it**; a Rust-core
change needs a `maturin develop --release` first (see `intentumdiff-build`), a pure-Python or TS
change does not.

## Run the suites

```bash
# Python (from repo root; venv python on Windows). Add PYTHONUTF8=1 PYTHONIOENCODING=utf-8 if
# a test prints non-ASCII (the console is cp1252 on Windows and will UnicodeEncodeError).
.venv/Scripts/python.exe -m pytest tests/unit -q
.venv/Scripts/python.exe -m pytest tests/unit/test_reindex_groups.py -q     # one file
.venv/Scripts/python.exe -m pytest "tests/unit/test_x.py::test_name" -q     # one test

# Rust
(cd crates/rust-core-host && cargo test --release)   # NOT a workspace member; -p from the root fails            # the engine crate
cargo test --workspace                  # everything

# VS Code extension (from plugins/vscode). `test` compiles then runs node:test on out/.
cd plugins/vscode && npm run lint && npm run test
cd plugins/vscode && npm run test:integration   # gated by INTENTUMDIFF_SKIP_LIVE_DIFF=1
```

Test tree: `tests/unit`, `tests/integration`, `tests/security` (adversarial Wasm sandbox),
`tests/benchmarks`, `tests/browser`, shared `tests/fixtures/` + `tests/conftest.py`;
`plugins/vscode/test/` (+ `test/fixtures`, `test/integration`); Rust tests live in-crate under
`#[cfg(test)]`.

## Adding a test — Python (pytest)

Drop a `test_*.py` in `tests/unit/` (pytest auto-discovers — no registration needed). For
**engine behavior, drive the real engine** instead of hand-building trees where possible:
```python
from intentumdiff.differ import SemanticDiffer
diff = SemanticDiffer().diff_strings(old, new, "file.py", language_hint="python")
assert [c.change_type for c in diff.changes] == [...]
```
For pure functions (e.g. presentation helpers), import and call them directly and build the
minimal frozen models (`SemanticNode`, `Change`, `ChangeGroup` from `intentumdiff.core.models`).
Prefer real fixtures in `tests/fixtures/` for cross-language snippet coverage.

## Adding a test — VS Code extension (node:test) — READ THIS GOTCHA

Tests use `node --test` with `node:assert/strict`:
```ts
import assert from "node:assert/strict";
import test from "node:test";
import { buildReleaseNotes } from "../src/releaseNotes";
test("descriptive name", () => { assert.equal(...); });
```
**Gotcha: `npm run test:unit` runs an EXPLICIT list of `out/test/*.test.js` files in
`plugins/vscode/package.json`.** A new `test/foo.test.ts` compiles but **will not run** until
you add `out/test/foo.test.js` to that `test:unit` script list. Always update the list when you
add a test file, or the new tests silently pass by never executing. The pure logic under test
must be vscode-free (no `import "vscode"`) so it runs under `node --test`; the thin vscode
provider wrapper is covered by integration tests. **Unit tests must do no network** (the LLM
prompt/parse logic is pure and tested; the fetch lives in the wrapper).

For webview HTML/interaction, use the **panel-render harness** (see `intentumdiff-vscode`):
import `out/src/reviewWebviewModel.js`, build a model, render HTML, assert on it (JSDOM for
script execution), or serve it for the Claude Preview MCP.

## Adding a test — Rust (`cargo test`)

Add a `#[cfg(test)] mod tests { ... }` block in the relevant crate module and assert on the
computed `SemanticNode`/`NodeFacts`/change output. Run `cargo test -p <crate>`. Keep new engine
behavior covered here — it's the authoritative layer.

## Conventions that make tests meaningful

- **Deterministic, offline.** Unit tests never hit the network and never depend on wall-clock
  or machine-specific state.
- **Assert intent, not incidental shape.** Pin the leading "what" of a message rather than an
  exact sentence that will drift; assert the derived category/risk, not a formatting detail.
- **Test the contract, not the implementation.** For change groups, assert the index-space
  invariant (every `raw_change_indices` in range, owned by node identity) rather than a
  hardcoded index that a re-sort could move.

## Engine-debugging gotchas (learned the hard way)

- **`DiffConfig(diagnostics=True)` silently disables the Rust core paths** (both the certified
  batch and per-stage `rust_matching` are gated on `not diagnostics.enabled`) — a diagnostics
  trace therefore always shows the PYTHON pipeline and can never observe a rust-fed defect. To
  inspect the rust path, monkeypatch `intentumdiff.differ.try_rust_core_tree_diff` (spy on its
  inputs/outputs) or use the batch `entity_fast_path` metadata with `profile_phases`.
- The rust-vs-python matching can be diffed directly: capture the rust `matching` via the spy,
  then call `differ._compute_matching(old_tree, new_tree, config)` on the captured trees.
- **Splitting a module breaks monkeypatches silently (the #78–#81 splits, learned 3×).**
  `patch("intentumdiff.cli.X")`/`setattr(cli, "X", ...)` patches the *façade's* binding; after a
  split, functions resolve `X` in their OWN module's globals, so the patch becomes inert — the
  test then exercises the real dependency and fails obscurely (or worse, passes while testing
  nothing; the live-server integration patches were inert for months). Rule: patch the module
  that LOOKS THE NAME UP, which is where the *calling* function lives, not where the target is
  defined — e.g. handlers constructing `SemanticDiffer` directly ⇒ `cli._commands.SemanticDiffer`,
  but paths through the `_differ()` helper ⇒ `cli._shared.SemanticDiffer`. When splitting:
  grep tests for `"<module>.<name>"` patch strings FIRST, and keep the patchable seams
  (e.g. `intentumdiff.differ.try_rust_core_*`) in the module tests already target.
- **Splitting a file also silently weakens source-content ratchets.** themeColors.test.ts
  pins regexes against `extension.ts`/`reviewWebviewModel.ts` SOURCE (the #27 hex-count
  ratchet, CSP pins, git-apply flags). Moving code out of a scanned file makes the ratchet
  under-count without failing. After any split, re-point the pins and make count-ratchets
  concatenate the split modules before counting.

## The corpus harness family (per-language ratchets under tests/fixtures/corpus/)

Each language dir holds `playground.<ext>` + two RATCHETED manifests (generated from what the
engine could see at generation time — they pin regressions without asserting unfixed gaps):

- `playground.expect.json` → `test_corpus_invariants.py`: **content visibility** (every listed
  token must appear in semantic-tree labels; gaps live in `invisible_tokens_at_generation`) and
  **mutation non-equivalence** (regex-derived literal bump / string edit / append must never be
  style-only or zero changes; known-bad cases carry `mutation_xfail` entries — when one starts
  passing the test FAILS until you delete the stale entry, by design).
- `edit_matrix.expect.json` → `test_construct_edit_matrix.py`: five derivation verbs
  (delete/rename/duplicate/modify-literal/swap) derived from the tree via
  `construct_edit_matrix.py`. Language vocab is scoped there: `_ENTITY_EXACT_BY_LANGUAGE`,
  `_LITERAL_EXACT_BY_LANGUAGE`, `_NEWLINE_INCLUSIVE_SPAN_TYPES` (span-end conventions differ
  per grammar — see issue #52's declared remainder). An honest `skip` (e.g. "no literals
  discoverable") beats a fabricated derivation.
- `test_position_convention.py`: asserts every corpus language's entity labels anchor at
  **0-based** lines (issue #52), with a non-vacuity check for the 14 crates that were flipped.

Adding a language = write the playground snippet, generate both manifests with the harness
helpers (`build_manifest`, the visibility walker), then run all three files. Regenerating a
manifest is a DELIBERATE act — byte-diff it and explain the change in the commit.

## Picking the guard set for a change (learned the hard way)

Before declaring a change verified, **grep tests/unit for files named after the module or
rule you touched** (e.g. touching the generic-text pipeline → `test_generic_text_diff.py`
exists and is the dedicated contract). The #35 port ran scenario suites but missed the
dedicated file; the full-suite gate caught 3 placement regressions post-commit. Scenario
suites assert counts/labels — dedicated files pin finer behavior (e.g. inline-highlight
placement), so both belong in the acceptance set.

## Investigating a failure (don't just report it — see intentumdiff-dev-loop)

1. Get the assertion: `pytest ... -q --tb=short`.
2. Read the test's *intent* — is the expectation still correct, or did a phase/name legitimately
   change (a stale assertion) vs a real behavior regression?
3. **Confirm pre-existing vs introduced:** `git stash push <your changed files>` → re-run the
   same tests → `git stash pop`. Same failures without your changes ⇒ pre-existing (say so, and
   document undocumented ones in `docs/BACKLOG.md` — the RC gate treats them as blockers).
4. `xfailed` = documented engine gaps (`pytest.mark.xfail` / `pytest.xfail(...)`), expected to
   fail until fixed; they are **not** failures. They flip to "unexpectedly passed" when the gap
   closes — that's the signal to remove the marker.

## Release-candidate gate

`docs/BACKLOG.md` → "0.0.1 RC Release Gate" lists what must be green before tag/publish:
Python proof gates, Rust parser/core tests, VS Code tests, competitor matrix + completion
audit, release-media validators, package dry-runs, and `git diff --check`. The strict engine
boundary gate runs with `INTENTUMDIFF_ENFORCE_RUST_ONLY_ENGINE=1`. Never mark work done with
failing tests, partial implementation, or unresolved errors.

## Oracle modules look dead but aren't — check what the test CALLS before deleting

A Python module with **no `src/` importer** is not automatically dead: it may be a **test
oracle** that pins Rust behavior. `analysis/invariances.py` is the canonical example — nothing
in `src/` imports it (production uses the Rust `apply_invariances` from `rust_core`, and the
boundary test enforces that), yet `tests/unit/test_invariances.py` *calls* its `apply_invariances`
directly to pin `invariance_groups.rs`, and its pydantic models validate the canonical
`rules.yaml` safety contract (the `_ALLOWED_EVALUATORS` allowlist). Deleting it would remove the
oracle. Rule: before deleting a "no importer" module, grep the tests for **calls** (not just
imports) to its symbols — an imported-and-called module is a live oracle, retired only at Phase B
with the pyo3 layer. (The engine-boundary ratchet allows this: oracle modules import only
`core.models`, never `analysis`, so they stay off the debt set.)
