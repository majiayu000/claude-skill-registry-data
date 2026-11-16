---
name: debugging
description: Systematically debug a failure by reproducing it, isolating the root cause, fixing it, and verifying the fix. Use when the user reports a bug, error, failing test, crash, regression, or unexpected behavior and wants it diagnosed or fixed, including intermittent or production-only problems they ask you to fix. Do not use for code review, new feature work, or performance tuning without a concrete failure.
---

# Debugging

Find the root cause before changing code. A fix without a reproduction is a guess.

## 1. Reproduce

- Collect the exact symptom: error message, stack trace, failing command, inputs, environment, and what changed recently.
- Reproduce it with the smallest reliable command, preferably an existing or new failing test.
- If you cannot reproduce it, report what you tried and ask for the missing information instead of guessing at a fix.

## 2. Isolate

- Read the code on the failing path. Form one hypothesis at a time and test it with evidence: logs, assertions, a debugger, a narrower test, or `git bisect` for regressions.
- Distinguish the root cause from the symptom. Ask why the bad state was possible, not only where it surfaced.
- Check whether the same cause affects other call sites.

## 3. Fix

- Make the smallest change that fixes the root cause, following project conventions.
- Add or keep a regression test that fails without the fix.
- Remove temporary logging and debugging code.
- Do not suppress the error, widen types, retry blindly, or weaken tests to make the symptom disappear.

## 4. Verify and report

- Run the reproduction, the regression test, and the relevant existing tests.
- Report the root cause, the fix, the evidence that it works, and any related risks or follow-ups. If verification could not run, say so.

## Examples

- Use: "The checkout test started failing after the last merge." "Users get a 500 when uploading a PNG."
- Skip: "Review this PR." (code review) "Make the dashboard load faster." (no concrete failure)
