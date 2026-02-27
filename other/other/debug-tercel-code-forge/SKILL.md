---
name: debug
description: >
  Use when encountering any bug, test failure, or unexpected behavior — enforces
  root cause investigation before fixes. Prevents symptom-fixing, masking bugs, and
  "just try this" approaches. For code-forge features, use code-forge:fixbug instead.
---

# Code Forge — Debug

Systematic root cause debugging for any technical issue.

## When to Use

- Any test failure, bug report, or unexpected behavior
- Performance degradation, build failures, integration issues
- ESPECIALLY when under time pressure or when "one quick fix" seems obvious

**For code-forge features:** Use `/code-forge:fixbug` instead — it adds upstream document tracing and state tracking on top of this methodology.

## Iron Law

**NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST.**

No "let me just try this." No "obvious fix." No guessing. Investigate first.

## Workflow

```
Root Cause Investigation → Pattern Analysis → Hypothesis Testing → Implementation (TDD fix)
```

## Four Phases

Complete each phase before moving to the next.

### Phase 1: Root Cause Investigation

1. **Read error messages carefully** — complete messages, not skimmed
2. **Reproduce consistently** — can you trigger it reliably?
3. **Check recent changes** — `git diff`, `git log` for what changed
4. **Gather evidence** — add diagnostic instrumentation at each boundary in multi-component systems
5. **Trace data flow backward** — from the error, walk back through the call chain

### Phase 2: Pattern Analysis

1. **Find working examples** — is there a similar feature that works?
2. **Compare against references** — read reference code COMPLETELY, not skimmed
3. **Identify differences** — list EVERY difference between working and broken
4. **Understand dependencies** — what does this code depend on? What depends on it?

### Phase 3: Hypothesis and Testing

1. **Form a single hypothesis** — state it clearly, write it down, be specific
2. **Test minimally** — smallest possible change that tests the hypothesis
3. **One variable at a time** — never change multiple things simultaneously
4. **Verify before continuing** — did the test confirm or refute the hypothesis?

If you don't know: **say so.** Don't pretend. "I don't understand why X happens" is valuable information.

### Phase 4: Implementation

1. **Create a failing test case first** — use TDD (see code-forge:tdd)
2. **Implement a single fix** — ONE change, not "while I'm here" improvements
3. **Verify the fix worked** — run the test, confirm it passes
4. **Run the full test suite** — ensure no regressions

### When Fixes Fail

Count your fix attempts:
- **< 3 attempts:** Return to Phase 1, gather more evidence
- **>= 3 attempts:** **STOP.** This is NOT a hypothesis failure — it's likely a **wrong architecture** or **wrong mental model.** Discuss with the user before proceeding.

## Anti-Rationalization Table

| Thought | Reality |
|---------|---------|
| "I know what's wrong" | Then Phase 1 will be fast. Do it anyway. |
| "Let me just try this quick fix" | Quick fixes mask root causes and create tech debt. |
| "It worked before, just revert" | Understanding WHY it broke prevents recurrence. |
| "The error message is clear" | Error messages often point to symptoms, not causes. |
| "It must be a library bug" | It's almost never a library bug. Check your code first. |
| "Let me add more logging" | Targeted logging at boundaries, not shotgun logging. |

## Red Flags

Stop immediately if you notice:
- You're trying the same approach a third time
- You're adding workarounds instead of fixing the actual issue
- You're suppressing error messages or catching/ignoring exceptions
- You're changing things "to see what happens" without a hypothesis
- The fix is larger than the feature it supports
