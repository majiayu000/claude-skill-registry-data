---
name: debugging
description: Find the cause before fixing. Use for a bug, failing test or unexpected behavior, before proposing a change.
---

# Debugging

Find the cause first. A fix without one is a guess that moves the symptom.

1. **Reproduce it.** Get the exact input, command and output. If it won't reproduce, say so and stop guessing.
2. **Read the evidence.** The full error, the stack, the log lines around it, and `git log` for what changed lately.
3. **Narrow it.** Compare a working case with the broken one. Bisect by commit, input or code path, and change one thing at a time.
4. **Say the cause in one sentence** and the check that shows it: "X fails because Y; Z proves it." Run the check.
5. **Fix that cause**, with the test that would have caught it (see `bud:code-style`).
6. **Show the same reproduction passing** (see `bud:verify`).

If three fixes in a row haven't worked, the cause is wrong. Go back to step 2 and tell Jason what you ruled out.
