---
name: verify-work
description: Use before claiming any task is done, complete, or fixed. A final verification pass that catches unverified claims, unintended changes, and leftover debris before reporting to the user.
---

# Verify Work

Goal: never tell the user something works without having watched it work.

Run this before every "Done" report. "It should work" is not a verification.

## Checklist

1. **Run the tests.**
   The relevant test suite actually executed, actually green — in this
   session, after the last change. A test run from before your final edit
   proves nothing.

2. **Run the thing.**
   Where possible, exercise the changed behavior for real: call the
   endpoint, run the command, hit the code path. One real execution beats
   ten confident explanations.

3. **Read the full diff.**
   - Every changed line is intentional and belongs to this task.
   - No accidental behavior changes, no unrelated "improvements".
   - No leftover debug output, commented-out code, or TODO placeholders.

4. **Check the tests themselves.**
   No test was weakened, skipped, or deleted to get to green. If one was —
   with approval — it is mentioned in the report.

5. **Check the claims.**
   Everything you are about to tell the user is something you observed, not
   something you infer. Anything unverified is reported as unverified:
   "not tested: X" is honest; silence is not.

6. **Second opinion (L2/L3).**
   If an advisor/reviewer model is available, have it review the result
   before you present it. If not, re-read the diff once more with fresh
   eyes on the riskiest part.

## Then report

```
Done:     <one sentence>
Verified: <what you ran and what you observed>
Recorded: <journal file path>
```

If any check failed, the task is not done — say what failed and what you
are doing about it instead.
