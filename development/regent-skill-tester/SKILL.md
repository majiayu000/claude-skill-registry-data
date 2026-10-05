---
name: regent-skill-tester
description: End-to-end test driver for REgent skills (regent-reverse, regent-build, regent-refactor). Use when asked to "test regent-refactor", "verify the reverse+build roundtrip", "audit a REgent skill", or "run the regent spec → code pipeline as a black box". Produces a PASS/FAIL verdict against all three grading keys (pytest, functional-checklist.md, test-oracle.md) plus a discipline check (no upstream leakage, no training-data smuggling). Triggers on phrases like "regent-refactor 测试", "test the refactor skill", "run regent end-to-end".
version: 0.1.0
author: Hermes Agent (MiniMax-M3)
license: GPL-3.0-or-later
metadata:
  hermes:
    tags: [regent, testing, e2e, reverse-roundtrip, grading-keys]
    related_skills: [regent-refactor, regent-reverse, regent-build]
---

# regent-skill-tester

Drive a REgent skill (reverse, build, or refactor) end-to-end against a
real fixture and produce a PASS/FAIL verdict. The methodology is the
seven-step workflow from `regent-refactor/SKILL.md` plus a **discipline
check** that ensures the agent under test is not smuggling in intent from
outside its inputs.

This is a test driver, not a skill under test. Run it against a freshly
prepared `spec/` tree and a fixture repo, get a verdict.

## When to Use

- A new version of a REgent skill (regent-reverse, regent-build,
  regent-refactor) needs verification before shipping.
- A user edited a spec and you need to prove that the edited intent is
  what the code does (or doesn't) — and that the rewriter did not
  also touch unrelated code.
- Someone claims their refactor is a "no-op" and you need to prove it
  empirically via `git diff --stat`.

**Don't use for**: testing non-REgent skills, or as a substitute for
actually running pytest.

## Inputs

- `fixture_repo` — path to a small, self-contained repo to reverse +
  refactor. A "tiny greeter" fixture (≤10 files, pure stdlib) is ideal
  for skill-discipline testing because there is nowhere to hide
  upstream leakage.
- `out_dir` — root for `spec-baseline/`, `refactored/`, and test
  artifacts. Defaults to `/tmp/refactor-test/`.
- `user_edit` — an explicit description of the spec change the user
  would make. Even if you ARE the user, write it down. The discipline
  test hinges on whether the rewriter respects a clarification vs
  invents behaviour.

## Workflow

### 1. Generate baseline spec

Run `regent-reverse` workflow by hand on the fixture (don't invoke the
skill — be the skill, against a fixture you read end-to-end).

Write to `<out_dir>/spec-baseline/`:
- `AGENTS.md`, `README.md`, `architecture.md`
- `layout/tree.txt`, `layout/src.map.md`
- `specs/<module>.spec.md` with `R-1..R-N` requirements + WHEN/THEN
  scenarios
- `conventions/{code-style,dev-env,architecture-rules}.md`
- `inventory/functional-checklist.md` (≥10 entries, one per public CLI
  / script / API surface)
- `inventory/test-oracle.md` (one entry per public surface that had a
  discriminating test in the original suite — not a transcript)

### 2. Apply the user edit

Modify the spec as the user would. Record the diff in a one-line
working note (e.g. "Added R-3a clarification: --shout + empty name →
stderr + exit 2").

If the edit is a **pure clarification** (pins existing layering,
tightens wording, no semantic shift), say so explicitly. This is the
case where the rewriter is allowed to produce zero code changes.

### 3. Run the skill under test

For `regent-refactor`:
- Strategy: **side-by-side** to `<out_dir>/refactored/` (do NOT
  mutate the source fixture).
- Follow the seven-step workflow in `regent-refactor/SKILL.md`:
  diff → classify → snapshot (the copy IS the rollback for
  side-by-side) → rewriter → verify → decide → self-review.

For `regent-reverse`: just run step 1 above and check that the spec
captures every public surface.

For `regent-build`: skip steps 1-2; go straight from an existing spec
to a fresh checkout and check that the rebuilt code passes all three
grading keys.

### 4. Run verification — all three keys

- **pytest**: `pytest -q` in the output tree (use `uv venv` + `uv pip
  install -e . pytest` if no venv).
- **functional-checklist.md**: execute every `- [ ]` line via the
  CLI / import the spec claims.
- **test-oracle.md**: per-symbol oracle entries (input → expected).
  Use a shell harness (`scripts/oracle_check.sh` template below) to
  avoid bash-quoting landmines.

### 5. Diff the output

Byte-level `diff -r` between original fixture and output tree.
`git diff --stat` equivalent: count `<`/`>` lines per file.

- **Zero diff + all green** → PASS (clarification-only refactor).
- **Diff matches the symbol list from step 2 + all green** → PASS
  (behavioural refactor).
- **Diff exceeds the symbol list** → FAIL — rewriter overstepped.
- **Any grading key red** → FAIL — rewriter under/over-shot.

### 6. Discipline check (the part most skills skip)

- ✅ Did not clone any other repo
- ✅ Did not `git log` upstream / inspect the fixture's remote history
- ✅ Did not pull training-data patterns in — every code reference
  must trace to a `Source:` line in the spec
- ✅ Only `read_file` from `fixture_repo` (the codebase under edit)
- ✅ Did not hallucinate public APIs (cross-check every R-N against
  actual source)

A rewriter that fails any of these is producing plausible-looking
output from forbidden knowledge. Fail the verdict even if the keys
are green.

### 7. Report

Produce a <5 KB verdict with:
- Was the user-edit a no-op? (yes/no, with evidence)
- `git diff --stat`-equivalent line counts per file
- pytest / checklist / oracle pass/fail counts
- Spec-debt (anything the tester had to invent or that forced a
  violation)
- Discipline check pass/fail per item
- Final: PASS / FAIL with the WHY
- Concrete improvements for the skill under test (heading + change)

## Common Pitfalls

1. **Bash-quoting landmines.** `bash -c "test \"\$(cmd)\" = 'X'"`
   trips on nested quoting. Prefer writing the harness to a
   `scripts/oracle_check.sh` file and `bash`-ing it. See the
   template below.
2. **Conflating CLI behaviour with library behaviour.** A checklist
   entry that says "unknown lang falls back" is wrong if the CLI
   uses `argparse choices=` (which rejects before code runs). Pin
   the layering in the spec's architecture-rules.md.
3. **Trusting the rewriter's "I changed it" report.** Always
   byte-diff. The agent can claim 5 lines and rewrite 500.
4. **Missing the empty-errorpath check.** `print(...)` to stderr +
   `return 2` is invisible to a stdout-only check. Capture stderr
   separately: `err=$(cmd 2>&1 1>/dev/null); ec=$?`.
5. **uv venv defaults.** `uv venv` then `uv pip install -e . pytest`
   — pytest is dev-only and may not be in `pyproject.toml`.

## Verification Checklist

- [ ] Baseline spec generated with all 11 expected files
- [ ] User edit recorded in one line before rewriter runs
- [ ] Side-by-side output (not in-place mutation)
- [ ] Three grading keys all green
- [ ] `diff -r` between fixture and output matches the symbol list
- [ ] Discipline check items all green
- [ ] Report names the exact heading + change for skill improvements

## Bundled Artifacts

- `scripts/oracle_check.sh` — per-symbol oracle harness (avoids the
  bash-nested-quoting landmine documented in Common Pitfalls #1).
- `scripts/verify_all.sh` — runs pytest + functional-checklist.md +
  test-oracle.md in one shot.
- `scripts/spec_diff_check.sh` — byte-level `diff -r` between
  fixture and refactored tree, ignoring build artifacts. Exits 0
  iff zero diff (clarification-only refactor).
- `templates/spec-baseline-layout.md` — minimum file layout for a
  REgent reverse output.
- `references/discipline-checklist.md` — the forbidden-moves
  checklist the verifier runs against the rewriter.
- `references/session-greeter-fixture-2026-07-19.md` — worked
  example: regent-refactor v0.1.0 against the tiny greeter
  fixture, with the four gaps found.