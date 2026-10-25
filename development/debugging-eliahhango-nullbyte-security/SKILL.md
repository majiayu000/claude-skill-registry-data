---
name: debugging
description: Diagnose a defect or unexpected behaviour by reproducing it, reducing the case, tracing the data and proving the fix with a regression test.
---

# Debugging: reproduce, reduce and fix the root cause

- Reproduce before changing code. Record the exact command, input, environment and observed output; a bug you cannot reproduce is a hypothesis, not a fix target.
- Reduce the case: remove unrelated data, narrow the input and disable optional layers. A minimal reproduction is the fastest path to the cause.
- Follow the data. Inspect the value at the boundary before and after each transform; do not assume the failure is where the stack trace ends.
- Use version control as a tool: bisect commits, diff working trees, or temporarily instrument one path. Change one variable per experiment.
- Fix the cause, not the symptom. If the fault is shared, patch the shared control point and check every caller.
- Add a regression test that fails on the old code. Re-run the original reproduction and the affected test suite.
- If the bug is environmental, state what differs and how to verify it. Do not close it as 'works on my machine'.

---

_NullByte skill pack. Original guidance for this tool; no third-party skill text is bundled._
