---
description: Investigate root causes systematically using scientific method
---

# Debug

Investigate and fix the issue described in "$ARGUMENTS" using systematic root cause analysis. No guessing — find the cause before attempting fixes.

## Prerequisites

None — this is a utility skill that can run anytime a bug is encountered.

## Process

### Phase 1: Investigation

1. **Read error messages carefully:**
   - Read the full error output, stack trace, and any warnings
   - Note file paths, line numbers, and error codes
   - Don't skip past errors — they often contain the solution

2. **Reproduce the issue:**
   - Identify the exact steps to trigger the bug
   - Can it be triggered reliably?
   - If not reproducible, gather more data before proceeding

3. **Check recent changes:**
   - What changed recently that could cause this? (git log, git diff)
   - New dependencies, config changes, environment differences?

### Phase 2: Analysis

4. **Trace the data flow:**
   - Where does the bad value originate?
   - Trace backward through the call stack to the source
   - Fix at the source, not at the symptom

5. **Find working examples:**
   - Is there similar code that works correctly?
   - What's different between working and broken?

### Phase 3: Hypothesis

6. **Form a single hypothesis:**
   - State clearly: "I think X is the root cause because Y"
   - Be specific, not vague

7. **Test minimally:**
   - Make the smallest possible change to test the hypothesis
   - One variable at a time
   - If it doesn't work, form a NEW hypothesis — don't pile fixes

### Phase 4: Fix

8. **Write a failing test** that reproduces the bug

9. **Implement the fix** — address the root cause, not the symptom

10. **Verify:**
    - The failing test now passes
    - No other tests broke
    - The original issue is resolved

11. **Commit** the fix with a clear message explaining what was wrong and why

## Output

Present findings to the user:
- What the root cause was
- What was changed to fix it
- The commit hash
- Any related issues discovered during investigation
