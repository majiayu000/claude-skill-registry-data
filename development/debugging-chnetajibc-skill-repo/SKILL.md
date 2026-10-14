---
name: debugging
description: "Debug via reproduce, minimize, observe, hypothesis, instrument, fix, regression-test. Never change random code and hope."
---

# debugging

Prove the cause before the fix: reproduce → minimize → hypothesize → instrument → fix → regression-test.

## Activate when

- Failing tests, broken builds, wrong runtime behavior, production incidents under investigation.

## Do NOT activate for

- Code archaeology without a defect (see git/git-history-analysis).

## Procedure

1. Reproduce reliably with a script or exact steps; no repro, no fix — only investigation.
2. Minimize: cut inputs, scope, and concurrency until the smallest failing case remains.
3. Hypothesize one cause at a time; instrument (logs, traces, debugger, bisect) to confirm or kill each hypothesis. Stop-the-line on data-loss/corruption paths.
4. Fix the root cause, not the symptom; add the regression test that fails without the fix.
5. Guard: check adjacent code for the same defect class; record the RCA briefly.
6. Verify: repro passes, full related suite green, regression test committed.
