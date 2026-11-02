---
name: fix-flaky-test
description: Find and fix the cause of a test that fails only sometimes, such as on CI, on a slow machine or in a certain order. Use this for any intermittent failure, timeout in a test or "passes on rerun" situation. It replaces retries and longer sleeps with a proven fix.
---

# Fix a flaky test

A flaky test is a real defect, in the test or in the product. Retrying hides it
and teaches everyone to ignore red builds. The aim is to reproduce it on demand,
fix the cause, and show that the same conditions no longer break it.

## When to use

A test fails intermittently, or passes when rerun without changes.

## Steps

1. **Collect the failures.** Save the exact message, OS, job and commit. Note what
   the failing runs have in common.

2. **Reproduce it.** Try these until it fails:

   - Run the test many times in a loop.
   - Run it with other tests, in a different order, or in parallel.
   - Add CPU load, or limit the CPU.
   - Slow down the code it waits for with a temporary delay.

   Slowing the code is often the quickest way to prove a timing bug.

3. **Classify the cause.**

   | Type | Signs | Usual fix |
   | --- | --- | --- |
   | Fixed wait too short | Fails on slow hosts | Wait for the outcome |
   | Shared state | Depends on test order | Give each test its own state |
   | Real clock | Fails near midnight or a boundary | Inject the clock |
   | Unordered results | Order changes between runs | Sort or compare as a set |
   | Port, file or process conflict | Fails in parallel | Use unique resources |
   | Real race in the product | Wrong result under load | Fix the product |
   | External dependency | Fails with the network | Stub the boundary |

4. **Fix the cause.** Replace a fixed wait with a check on the actual outcome. A
   deadline only catches a hang, so set it longer than the time the product allows.
   Make sure a timeout prints enough output to explain itself.

5. **Check the assertions are unchanged.** The fix must not make the test accept
   behaviour it used to reject.

6. **Prove the fix.** Repeat the conditions from step 2. The old code must fail and
   the new code must pass under the same stress.

7. **Finish.** Follow `verify-and-report`.

## Stop and ask when

- You cannot reproduce it after trying everything in step 2. Report what you
  tried, and add diagnostics instead of guessing.
- The cause is a real product race that needs a design change.

## Common mistakes

| Tempting move | Why it fails | Do this instead |
| --- | --- | --- |
| Add a retry | Hides the defect | Find the cause |
| Increase a sleep | Slower, and still flaky | Wait for the outcome |
| Mark it as skipped | Removes the protection | Fix it, or file a linked issue with the owner's approval |
| Loosen the assertion | Accepts wrong behaviour | Keep the assertion |
| Declare it fixed after one pass | One pass proves nothing | Repeat under stress |

## Example

Failure: `replaced=false` after 5 seconds, on Windows runners only.

Weak fix: raise the wait from 5 to 15 seconds.

Strong fix:

```markdown
Reproduce: slowed the old process's shutdown to 6 seconds, and the test failed
with the same message as CI.
Cause: the test stopped after a fixed 5 seconds, while the handoff can take longer.
Fix: wait until the handoff finishes, with a 60-second bound for hangs.
Proof: with the same 6-second delay, the old test fails and the new one passes.
Assertions: unchanged.
```

## Report

```markdown
Failure: <message, where it occurred>
Reproduced by: <command or condition>
Cause: <type and explanation>
Fix: <what changed>
Proof: <old fails, new passes, under the same condition>
Assertions changed: <none, or why>
```
