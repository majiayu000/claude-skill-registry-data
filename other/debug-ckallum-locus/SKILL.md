---
name: debug
version: 1.0.0
description: |
  debug this, fix this bug, why is this failing, investigate error, trace the issue,
  something is broken, test failure, systematic debugging, diagnose, root cause.
  Four-phase systematic debugging: investigate → analyze patterns → hypothesis test → fix.
  Parallel investigation for independent failures.
argument-hint: [error-description]
allowed-tools:
  - Bash
  - Read
  - Edit
  - Write
  - Grep
  - Glob
  - Agent
  - AskUserQuestion
---

# Systematic Debugging

Four mandatory phases. Do not skip ahead to fixing — understand first.

## Phase 1: Investigate

### Read the error carefully

Don't skim. Read the full error output, stack trace, and surrounding logs. Extract:
- **What** failed (exact error message)
- **Where** it failed (file, line, function)
- **When** it started failing (recent change? always broken?)

### Reproduce consistently

```bash
# Run the failing command/test
<reproduce command>
```

If it doesn't reproduce, it's likely a race condition, environment issue, or flaky test. Investigate those vectors specifically.

### Check recent changes

```bash
git log --oneline -10
git diff HEAD~3 --stat
```

Did a recent commit touch the failing area? If so, read that diff first.

### Gather evidence in multi-component systems

If the failure spans multiple components, trace the data flow:
1. Where does the input enter the system?
2. What transformations happen?
3. Where does the output diverge from expected?

Add temporary logging if needed to narrow down the boundary.

## Phase 2: Pattern Analysis

### Find a working example

Find code that does something similar and works:

```bash
# Search for similar patterns
```

Use Grep/Glob to find analogous code paths, test cases, or previous implementations.

### Compare against the reference

What's different between the working version and the broken one? Common differences:
- Missing null/undefined check
- Different argument order
- Missing await/async
- Wrong import path
- Stale cache or state
- Environment variable missing

### Understand the dependency chain

Trace what the broken code depends on:
- What does it import?
- What state does it expect?
- What runs before it?
- What external services does it call?

## Phase 3: Hypothesis and Test

### Form a single hypothesis

Based on evidence from Phases 1-2, state one clear hypothesis:
> "The failure occurs because X, which causes Y, resulting in Z."

### Test minimally

Make the smallest possible change to test your hypothesis. If the hypothesis is right, the minimal fix should resolve the issue. If wrong, revert and form a new hypothesis.

**Do NOT:**
- Change multiple things at once
- "Try random fixes and see what sticks"
- Add workarounds without understanding the root cause

### Verify before continuing

Run the reproduction again. If the fix works, proceed to Phase 4. If not, go back to Phase 2 with new information.

## Phase 4: Implement the Fix

### Create a failing test case

Before applying the fix permanently, write a test that captures the bug:

```
# Test that reproduces the exact failure
```

This ensures the bug doesn't regress.

### Implement a single fix

Apply the minimal fix. One change, one commit. Don't bundle unrelated cleanup.

### Verify comprehensively

1. The new test passes
2. The original failure no longer reproduces
3. Existing tests still pass
4. No regressions introduced

### If 3+ fix attempts have failed

Stop. Question the architecture:
- Is the mental model of the system wrong?
- Is there a deeper design issue?
- Present findings to the user via AskUserQuestion with options:
  A) Continue debugging with a different approach
  B) Escalate — describe the full investigation so far

## Parallel Investigation Mode

When you encounter **2+ independent failures** (different root causes, different components):

Dispatch one agent per independent failure domain:

```text
prompt: "Investigate this failure:
<error output>
<relevant file paths>

Follow systematic debugging phases 1-3. Report: root cause hypothesis, evidence, and proposed minimal fix. Do NOT apply the fix."
description: "Debug: <failure description>"
```

Rules for parallel dispatch:
- Only parallelize genuinely independent failures (different files, different subsystems)
- If failures might be related (same component, cascading), investigate sequentially
- Each agent investigates but does NOT fix — collect all root causes first, then apply fixes in the right order

## Red Flags — You're Going Wrong If:

- **Changing code without understanding why it's broken.** Stop. Go back to Phase 1.
- **"It works now but I don't know why."** That's not fixed. Find the actual cause.
- **Adding a try/catch to suppress the error.** That's hiding, not fixing.
- **The fix is longer than 20 lines.** Probably over-engineering. Simpler fix likely exists.
- **You're debugging for 15+ minutes without new evidence.** Step back, gather more data, or ask the user for context.

## Gotchas

- **Reproduce FIRST.** If you can't reproduce it, you can't verify the fix. Don't guess.
- **Check the test, not just the code.** Sometimes the test itself is wrong — asserting the wrong thing, using stale fixtures, or having a race condition.
- **Environment differences matter.** CI vs local, Node version, env vars, database state. Ask if the failure is environment-specific.
- **Flaky tests need special treatment.** If it fails intermittently, it's likely timing, ordering, or shared state. Run it 5x in a row to confirm.
- **Don't trust error messages literally.** "Cannot find module X" might mean X exists but has a syntax error. "Connection refused" might mean wrong port, not server down. Verify the actual state.
