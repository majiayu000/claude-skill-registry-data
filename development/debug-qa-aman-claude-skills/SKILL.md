---
name: debug
description: >
  Debug a bug or unexpected behavior systematically. Use when the user says "there's a bug",
  "this isn't working", "I'm getting an error", "help me debug", "why is this failing",
  "unexpected behavior", "test is failing", "something is broken", or describes behavior
  that doesn't match expectations - even if they don't say "debug".
---

## Overview

Based on **"The Pragmatic Programmer"** by Andrew Hunt & David Thomas. Hunt & Thomas's debugging philosophy: debugging is a puzzle to be solved with evidence, not a crisis to be panicked through. The key discipline is don't guess. Form a hypothesis, predict what you'll see if the hypothesis is correct, test it, and observe. Repeat.

Their rubber duck principle: before asking for help, explain the problem out loud (to a rubber duck or anyone). The act of articulating often reveals the answer.

## Workflow

### Step 1: Reproduce the bug reliably
You cannot debug what you cannot reproduce.
- What exact steps produce the bug? Document them.
- Is it 100% reproducible or intermittent?
- On which environments? (dev only, staging, prod?)
- Since when? (what changed recently?)

If you can't reproduce it reliably, make that the first problem to solve.

### Step 2: Understand the expected vs actual behavior
State explicitly:
- Expected: what should happen?
- Actual: what is happening?
- Evidence: logs, error messages, screenshots

Do not skip this. Vague bug descriptions lead to fixing the wrong thing.

### Step 3: Form a hypothesis
What is your best theory for why the actual differs from expected?
Write it down. Debugging without a hypothesis is random exploration.

### Step 4: Predict the evidence
If your hypothesis is correct, what will you see when you look at [specific thing]?
Make a prediction before you look. This keeps you honest.

### Step 5: Test the hypothesis
- Add targeted logging or use a debugger to observe the predicted evidence
- Change one thing at a time - not multiple
- If the evidence matches: hypothesis confirmed, move to Step 6
- If the evidence doesn't match: your hypothesis is wrong, go back to Step 3

### Step 6: Fix the root cause (not the symptom)
Hunt & Thomas: fix the problem, not the symptom.
- Symptom fix: catching an exception that shouldn't be thrown
- Root cause fix: understanding why the exception is thrown and preventing it

Ask "why" five times before writing the fix.

### Step 7: Verify the fix
- Does the original reproduction case pass?
- Do existing tests still pass?
- Write a test that would have caught this bug originally

### Step 8: Document the learning
What was the root cause? What made it hard to find? How could it be caught earlier next time?

## Anti-Patterns

**1. Guessing instead of hypothesizing**
Bad: Randomly changing things until it works.
Good: Form a hypothesis. Predict evidence. Test. Observe. Either confirm or refute.

**2. Fixing the symptom**
Bad: Adding a null check to stop the crash.
Good: Understanding why null is reaching that point and preventing it at the source.

**3. Changing multiple things at once**
Bad: "Let me try these 5 changes together."
Good: One change at a time. Otherwise you don't know which change fixed it.

**4. Not writing a regression test**
Bad: Fix the bug, move on.
Good: Write a test that reproduces the bug before fixing it. The test passes after the fix. It lives in the suite forever.

## Quality Checklist

- [ ] Bug is reproducible with documented steps
- [ ] Expected vs actual behavior stated explicitly
- [ ] Hypothesis written down before testing
- [ ] Evidence predicted before looking
- [ ] One change at a time during investigation
- [ ] Root cause identified (not just symptom)
- [ ] Fix verified against original reproduction case
- [ ] Regression test written
