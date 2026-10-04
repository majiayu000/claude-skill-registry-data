---
name: debugging-and-recovery
description: Use when something is broken, a test is failing, behavior is wrong, when investigating a production incident, when a user reports a bug, when a feature works locally but not in another environment, or when the system behaves differently than the contract specifies.
---

# Debugging and Recovery

## Overview

Reproduce → localize → fix → guard. Never guess at root cause. The fix is not done until a regression test guards it. For bugs with GitHub issues, see `triage-issue` for the full investigation + issue creation flow.

## When to Use

- Something broke or behaves unexpectedly
- A test is failing and the cause is not obvious
- A bug has been reported and needs diagnosis before a fix
- An error is ambiguous — multiple possible causes

## When NOT to Use

- The fix is obvious and well-understood — just implement with `tdd`
- The bug is a missing feature, not broken behavior — use `spec-driven-development`
- You want to preemptively prevent bugs — use `code-review-and-quality`

## Common Rationalizations

| Thought | Reality |
|---------|---------|
| "I know what the bug is" | You think you do. Reproduce it first. |
| "I'll just try this fix and see" | Untested fixes introduce new bugs |
| "The root cause is obvious from the stack trace" | Stack traces show symptoms, not causes |
| "A unit test would be too hard to write for this" | Write an integration test — the behavior is observable |
| "The fix is one line, no test needed" | One-line bugs are re-introduced in one line |

## Red Flags

- Fixing before reproducing — you might be fixing the wrong thing
- Fix that passes all tests but doesn't change observable behavior
- No regression test added — the bug will return
- Root cause described as "it just wasn't working" — not a cause
- Fix modifies more than what the bug report describes

## Core Process

### Step 1: Reproduce

Get the minimal reproduction: exact steps, inputs, environment. If you can't reproduce it, you don't understand it. Run the failing scenario manually or via test before writing any fix.

### Step 2: Write a failing test

Before fixing:

```
RED: Write a test that reproduces the bug
     → The test must fail
     → If it passes, your reproduction is wrong
```

The test proves you understand the bug.

### Step 3: Localize

With a failing test, trace the code path:
- Where does the expected behavior diverge from actual?
- What invariant is being violated?
- What recently changed in this code path? (`git log -p <files>`)
- Is it the logic, the data, or the interface contract?

### Step 4: Fix — minimum change

Implement the smallest change that makes the failing test pass. Do not refactor adjacent code. Do not fix other bugs you notice. Do not add features.

### Step 5: Guard

Run the full test suite. Confirm:
- The specific regression test passes
- No previously passing tests now fail
- The fix doesn't silently break adjacent behavior

### Step 6: Document

If the bug was non-obvious: add a comment explaining WHY the fix is correct, not what it does. Consider whether the bug points to a missing contract invariant in `.forge/contracts/`.

## Verification

- [ ] Bug reproduced before any fix was written
- [ ] Failing test written that specifically captures the bug
- [ ] Root cause identified (not just symptom)
- [ ] Fix is the minimum change to make the test pass
- [ ] Regression test passes after fix
- [ ] Full test suite still passes
- [ ] If contract was violated: `.forge/contracts/` updated with the missing invariant
