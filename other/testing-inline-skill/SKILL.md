---
name: testing-inline-skill
description: >-
  In-session testing delegate — runs the testing workflow inline (no subagent):
  language/framework test discovery, scoped test writing for current-diff files,
  execution and failure triage. Decision tree with skip rules, scope bounds,
  enforcement deltas, and output contract. Triggers: inline testing, write
  tests in-session, plan-execution-inline-skill testing step.
license: Apache-2.0
compatibility: opencode
metadata:
  mirrors: testing-subagent
category: Code Quality
---

# Testing (inline)

You are executing the testing delegate's workflow **in this session** — no
subagent, no fresh context. The trade you are accepting: you keep the session's
context and the caller's full tool access, so the discipline below is advisory,
not harness-enforced. Follow it anyway.

## Decision tree

1. **Skip check (run first):**
   - Changed files are all pure-data (JSON/YAML/MD configs, docs) with no
     testable logic → report "no testable changes", stop.
   - The project has no test runner discoverable from manifests (package.json
     scripts, pyproject, Makefile, CI files) → report "test-inviable stack",
     stop. Never install a test framework unprompted.
2. **Discover:** nearest existing test for each changed source file (TS: sibling
   `*.test.ts`; PY: `tests/<dir>/test_<name>.py`); mirror its framework and
   style. No existing tests → place per language convention.
3. **Write:** cover the behavior change, one assertion per contract point;
   table-driven when >3 similar cases. No snapshots of generated output.
4. **Execute:** run ONLY the new/affected tests (scoped, not the suite).
5. **Triage failures:** product bug → report, do not fix past the test's scope;
   test bug → fix and re-run (max 3 cycles).

## Scope bounds

- Write/modify **test files only**. Product-code fixes are findings, not edits.
- Test only files in the current diff (`git diff --name-only --diff-filter=AM`,
  minus configs/docs). Untouched modules are out of scope.

## Enforcement deltas (vs testing-subagent)

| Subagent enforcement | Inline discipline (you) |
|---|---|
| Fresh context window | You carry session context — restate the diff's intent in one line before writing tests so drift is visible |
| Session-isolated tool state | Same session — prefix every write with the target test file path in your narration |
| Tier-model routing | Same model as the caller — if the diff exceeds your context comfort, say so and stop rather than guessing |

## Output contract

**Status:** [success | partial | failed]
**Output:** tests written (paths) + run result (passed/failed counts) + skipped-reason if any
**Summary:** ≤3 sentences
**Issues:** blockers, product bugs found, or "None"
