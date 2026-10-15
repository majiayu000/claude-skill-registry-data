---
name: debug
description: |
  Systematic root cause analysis. Reproduce, isolate, fix, verify, prevent.
  Use when: "debug this", "why is this broken", "investigate", "root cause",
  "this doesn't work", or when something is failing.
---

# /debug — Root Cause Analyst

Don't guess. Reproduce. Isolate. Fix. Verify. Prevent.

## Process

1. **Reproduce** — Can you trigger the bug reliably?
2. **Isolate** — What's the smallest input that causes it?
3. **Hypothesize** — What could cause this behavior?
4. **Test** — Verify/falsify each hypothesis
5. **Fix** — Minimal change that resolves the root cause
6. **Verify** — Confirm the fix works AND doesn't break other things
7. **Prevent** — Write a test that catches this if it regresses

## Output

```
## Debug Report

### Symptom
{what the user observed}

### Root Cause
{what actually went wrong}

### Fix
{what was changed}

### Regression Test
{test that prevents recurrence}
```
