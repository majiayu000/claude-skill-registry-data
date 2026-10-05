---
name: bug-fix
description: Use when investigating or fixing a bug, error, crash, regression, or unexpected behavior. Enforces reproduce-first, evidence-based root cause analysis, and a regression test before the fix.
---

# Bug Fix

Goal: fix the cause, prove it stays fixed, leave a record.

## Steps

1. **Observe.**
   Collect what is actually known: error message, logs, failing input,
   expected vs. actual behavior. Write down what is evidence and what is
   assumption.

2. **Reproduce.**
   Make the bug happen on demand — ideally as a failing automated test.
   If you cannot reproduce it, say so and propose what extra evidence you
   need (logs, inputs, environment). Do not "fix" what you cannot see fail.

3. **Find the root cause.**
   Follow the evidence chain: observed behavior → project source →
   dependency source → docs. If the docs and the behavior disagree, the
   behavior wins — read the library source if you must.
   The root cause is the answer to "why did this happen", not "where does
   it hurt".

4. **Write the regression test first.**
   A test that fails because of the bug. This is the proof your fix works
   and the guard against the bug returning.

5. **Fix.**
   The smallest change that removes the cause. If the real fix is large or
   risky (L2/L3), propose it with the Problem / Plan / Risk / Question
   message before implementing. If you must ship a workaround instead of the
   root-cause fix, say so explicitly — never disguise one as the other.

6. **Verify.**
   The regression test passes, the full relevant test suite passes, and
   nothing else changed behavior. Run the `verify-work` skill.

7. **Record.**
   Journal entry: `docs/agent-journal/YYYY-MM-DD-bug-<slug>.md`
   (format: Problem / How found / Root cause / Fix / Regression test).

## Do not

- Do not touch the failing test's assertions to make it pass.
- Do not fix the symptom and call it done.
- Do not batch unrelated "improvements" into the bug fix.
