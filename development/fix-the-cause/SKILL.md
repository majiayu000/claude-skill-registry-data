---
name: fix-the-cause
description: "Use when debugging. Reproduce first, as a failing test when the bug has a testable shape, and capture the broken state. Ask why until you reach the real cause and fix it there. No null check to silence a crash. Two failed tries at the same approach means stop."
disable-model-invocation: true
kind: principle
---

# Fix the cause

Don't patch symptoms. Find what's wrong and fix that.

Symptom fixes pile up. Each one makes the system harder to reason about and leaves the real bug in place. Fixing the cause is slower the first time and faster every time after.

## Reproduce first, always

Before touching any code, see the bug and capture the broken state. A screenshot for UI. A query result or an error payload for backend. That capture is half your evidence, and the only way to know your fix did anything.

If you can't reproduce it, stop and say so. Don't fix what you can't see.

When the bug has a testable shape, the reproduction is a failing test. Write the smallest test that shows the bug, run it, and confirm it fails for the right reason, not a typo or a missing import. Then fix, rerun, and watch it go green. Commit the test first, then the fix, so a reviewer sees red then green. Skip the test only when it would need a heavy harness or brittle mocks, and say why.

## Then find the cause

- **Ask why until you get there.** The first answer is usually a symptom of the next one.
- **Don't add a guard to make it stop.** A null check that silences a crash is a symptom fix. The crash was telling you something. If you can't name which caller sends the null and why, you haven't found the bug.
- **A workaround that needs a paragraph to justify is the wrong fix.** Fix the code, not the comment.
- **Fix the pattern, not the instance.** Grep for the same shape elsewhere. If it's wrong here, it's probably wrong there.
- **When stuck, look. Don't guess.** Add logging, read the actual error text, print the actual value. Guessing feels faster and isn't.

## Two strikes, stop

If the second try at an approach fails the same way the first did, the approach is wrong, not the execution. Stop. Write down what you tried and why it failed. Bring the next idea. Ten variations of a broken idea feels like progress from the inside. It isn't.

## Bugs after a restart

Code doesn't change between runs. State does. When something fails after a restart, suspect leftover state before code: config files, caches, lock files, serialized state. If clearing a state file fixes it, the real fix is validating that state on the way in.

## Then prove it

Capture the same thing you captured at the start. Before and after, side by side. That pair is the evidence for the fix.
