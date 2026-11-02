---
name: debug-failure
description: Find the root cause of an error, crash, failing test, regression or wrong behaviour, then fix it with a regression test. Use this whenever something is broken or behaves unexpectedly and the cause is not already proven, even if a fix seems obvious. Do not guess at fixes.
---

# Debug a failure

Guessing is the slowest way to debug. A fix that makes the symptom disappear
without explaining it usually moves the bug somewhere else. Your job is to explain
the failure with evidence, then change as little as possible.

## When to use

Any failure whose cause you have not proven. For intermittent test failures, use
`fix-flaky-test`.

## Steps

1. **Capture the exact failure.** Copy the full error, stack trace, command and
   input. Read all of it, starting with the first error. Later errors are often
   side effects.

2. **Reproduce it.** Run the smallest command that shows the failure. If you
   cannot reproduce it, say so and collect more data. Do not "fix" it blind.

3. **Check for a recent cause.** Run `git log --oneline -10 -- <file>`. If it
   worked before, find the change that broke it. `git bisect` helps when the
   range is large.

4. **Read the code at the failure.** Open the exact file and line in the trace.
   Follow the bad value back to where it was created.

5. **Write down a hypothesis.** Use this form: "X fails because Y. If that is true,
   then Z will show it." Choose Z so that it could prove you wrong.

6. **Test one hypothesis at a time.** Add a log, assertion or debugger stop, and
   run it. Change one thing per run, and remove temporary logging afterwards.

7. **Explain the cause.** You are ready to fix it when you can say why it fails,
   why it did not fail before, and why your fix addresses that.

8. **Write the regression test.** It must fail on the current code for the same
   reason as the bug. Follow `write-tests`.

9. **Fix the cause.** Make the smallest change, and run the regression test.

10. **Look for the same bug elsewhere.** Search for the same pattern.

11. **Finish.** Follow `verify-and-report`.

## Three failed attempts

If three attempts have not worked, stop editing. Revert your experiments, write
down what you ruled out, and rethink. Your model of the system is wrong somewhere.
Check your assumptions: the right file, the right branch, a stale build, the right
environment, the version that is actually installed.

## Stop and ask when

- The failure only appears in an environment you cannot reach.
- The real fix is much larger than the task, or changes a public contract.
- The test may be right and the requested behaviour wrong.

## Common mistakes

| Tempting move | Why it fails | Do this instead |
| --- | --- | --- |
| Wrap it in `try`/`catch` | Hides the failure | Find why it throws |
| Add a null check | Bad data still reaches this point | Find where the null came from |
| Change the test to match | Removes the signal | Decide which side is wrong, with evidence |
| Add a retry or a longer timeout | Hides a race or slowdown | Find what is slow or racing |
| Change several things at once | You cannot tell what worked | Make one change per run |
| Call a failure unrelated | Often it is not | Check it against your baseline |

## Example

Failure: `TypeError: cannot read 'email' of undefined` in `sendReceipt`.

Weak fix: `user?.email`. The crash stops, and receipts silently stop sending.

Strong work:

```markdown
Hypothesis: `findUser` returns undefined for deleted users.
Check: logged the id, then queried it. The user was soft-deleted.
Cause: `findUser` filters deleted users, while orders keep their user id.
Fix: use `findUserIncludingDeleted` for receipts.
Regression test: an order from a deleted user still sends a receipt.
```

## Report

```markdown
Symptom: <exact error>
Reproduce: <command>
Cause: <what is wrong, and why it fails now>
Evidence: <what you ran or read that proves it>
Fix: <what changed>
Regression test: <name, and how it failed before the fix>
```
