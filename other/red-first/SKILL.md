---
name: red-first
description: >
  Regression-test-first bug fixing: reproduce, write a failing test that proves the bug, show it
  red, then fix to green with the minimal pattern-consistent change. Use whenever the user reports
  a bug, pastes failing behavior or a stack trace, or says "fix this bug", "found a bug",
  "write the failing regression test", "prove the bug first". A bug is not fixed until a test
  proves it was real. When a log file is the evidence, delegate diagnosis to the log-analyzer skill,
  then return here for the test-first fix.
---

# Red First — Test-Proven Bug Fixing

A fix without a proving test is a guess wearing a commit message. Order is fixed: reproduce → red → green → sweep. Never fix first.

## Phase 1 — Reproduce & Root-Cause

1. Read the evidence: pasted output, stack trace, screenshot description. If the evidence is a log file, run the **log-analyzer** skill for diagnosis and come back with its root cause.
2. Read the full delegation chain around the failure — entry point → service → model → schema. Never diagnose from the entry point alone.
3. State the root cause in one sentence: which line, which wrong assumption, which input triggers it. If you cannot state it, keep reading — do not proceed on a hunch.

## Phase 2 — Red

1. Write one regression test that fails **because of this bug** — named by behavior (`it_marks_cycle_complete_when_single_email_sent`), minimal setup, placed next to the feature's existing tests, matching their style.
2. Run it. **Show the red output.** A test that passes on broken code is testing the wrong thing — rewrite it until it fails for the stated root cause.
3. Test at the same level the bug lives: unit test for pure logic, feature test for flow/state bugs. Real database for anything touching persistence; fake only at the established seams (HTTP, job dispatch, event listeners, AI resolver).

## Phase 3 — Green

1. Minimal fix, consistent with the file's existing patterns — same naming, same error-handling style. No refactoring, no drive-by cleanups, no "while I'm here."
2. Run the regression test: green. Run the **full suite**: green. A fix that breaks a neighbor is not done.
3. Formatter/lint clean.

## Phase 4 — Sweep for Siblings

Same bug pattern elsewhere? Symmetric paths (the parallel driver, the cache path next to the API path), copy-pasted logic, the same wrong assumption in a neighboring class. Report sibling occurrences; fix them only on request — that's a scope decision, not yours.

## Output Contract

1. **Root cause** — one sentence, `file:line`.
2. **Red proof** — test name + the failing assertion output.
3. **Fix** — what changed, why minimal.
4. **Green proof** — regression test + full-suite results.
5. **Siblings** — same pattern found elsewhere, or "none".

## Hard Rules

- No fix before a red test exists — if the user explicitly waives the test, note the waiver in the report.
- If the bug can't be reproduced, say so with what was tried; never ship a speculative fix for an unreproduced bug.
- The regression test stays in the suite permanently; it is the bug's tombstone.
