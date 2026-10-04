---
name: debug
description: Use when encountering bugs, test failures, or unexpected behavior. Systematic root cause investigation and bug fixing before attempting any fixes.
---

# Systematic Debugging

## The Discipline

Random fixes waste time and introduce new bugs. Guessing is not debugging.

Find the root cause before attempting any fix. Treating symptoms is failure.

## When to Apply

Use for every technical issue:
- Test failures
- Bugs (development or production)
- Unexpected behavior
- Performance problems
- Build or integration failures

Use it especially when:
- Under time pressure (urgency makes guessing tempting)
- The fix seems obvious ("just one quick change")
- Previous attempts have not worked
- You do not fully understand the issue

## The Rule

```
No fixes without root cause investigation first.
```

If you have not completed Phase 1, you cannot propose fixes.

## Phase 1: Root Cause Investigation

Before attempting any fix:

1. **Read the Error**
   - Read the full error message and stack trace
   - Note line numbers, file paths, error codes
   - Errors often contain the exact answer

2. **Reproduce Reliably**
   - Can you trigger it consistently?
   - What are the exact steps?
   - If not reproducible, gather more data. Do not guess.

3. **Check What Changed**
   - `git log --oneline -10` and `git diff HEAD~3`
   - New dependencies, config changes, environment differences

4. **Instrument Multi-Component Systems**
   Before proposing fixes in systems with multiple layers:
   ```
   For each component boundary:
     Log what enters
     Log what exits
     Verify config propagation
   Run once to see WHERE it breaks
   Then investigate that specific component
   ```

5. **Trace Data Flow**
   - Where does the bad value originate?
   - What called this function with incorrect input?
   - Keep tracing backward until you find the source
   - Fix at the source, not at the symptom

## Phase 2: Pattern Analysis

1. Find working examples of similar code in the same codebase
2. Compare against references. Read them completely, do not skim.
3. List every difference between working and broken, no matter how small
4. Map dependencies: what does this component need from its environment?

## Phase 3: Hypothesis and Test

1. **Form a single hypothesis**
   - State it explicitly: "X is the root cause because Y"
   - Be specific

2. **Test with the smallest possible change**
   - One variable at a time
   - Do not fix multiple things simultaneously

3. **Evaluate**
   - Confirmed? Move to Phase 4
   - Rejected? Form a new hypothesis from the evidence
   - Do not stack fixes on top of each other

## Phase 4: Fix Implementation

1. **Write a failing test** that reproduces the bug
2. **Implement a single fix** addressing the root cause
3. **Run verification immediately** — execute the test, command, or operation that was failing

## Phase 5: Verification Loop (MANDATORY)

**The first fix is NEVER assumed correct.** Every fix must pass through this loop before being considered done.

1. **Run the exact failing scenario again**
   - Execute the same command, test, or operation that originally failed
   - Do not skip this. Do not assume. RUN IT.

2. **Evaluate the result:**
   - **PASS** — The original error is gone AND no new errors appeared → proceed to Phase 6
   - **PARTIAL** — Original error changed but something else broke → return to Phase 3 with new evidence. The fix exposed a deeper issue.
   - **FAIL** — Same error persists → the hypothesis was wrong. Return to Phase 1 with what you learned. Do NOT retry the same fix with minor variations.

3. **Run broader verification**
   - Run the full test suite (or at minimum, all tests in the affected module)
   - Check for regressions: did fixing this break something else?
   - If regressions appear, they are YOUR responsibility — fix them before proceeding

4. **Repeat until clean**
   - This loop continues until verification passes cleanly
   - There is no "good enough" — either it works or it doesn't
   - Every iteration must produce NEW evidence, not repeat the same attempt

5. **If three or more fix attempts have failed:**
   - Stop attempting patches entirely
   - Question whether the architecture is fundamentally wrong
   - Each fix revealing a new problem in a different location is a signal of structural issues
   - Present your findings and discuss with the human before continuing
   - Do NOT silently try a fourth approach

## Red Flags: Return to Phase 1

If you catch yourself thinking any of these, stop:
- "Quick fix for now, investigate later"
- "Just try changing X and see"
- "I do not fully understand but this might work"
- "Here are the problems:" (listing fixes without investigation)
- Proposing solutions before tracing data flow
- "One more fix attempt" after two failures
- **"It should work now"** — without running verification
- **"This fix is straightforward, no need to test"** — ALWAYS test
- **"The test passed so we're done"** — run broader verification too

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Too simple for the full process" | Simple bugs have root causes. The process is fast for simple issues. |
| "No time, it is an emergency" | Systematic debugging is faster than thrashing. |
| "I see the problem, let me fix it" | Seeing symptoms is not understanding root cause. |
| "Multiple fixes at once saves time" | Cannot isolate what worked. Introduces new bugs. |
| "One more attempt" (after 2+) | Three failures means architectural problem. Stop fixing, start questioning. |
| "It should work now" | Should is not evidence. Run the verification. Show the output. |
| "The fix is obvious" | Obvious fixes that aren't verified cause the worst regressions. |

## Phase 6: After Verified Fix

- Document what the root cause was and what evidence confirmed the fix
- Ensure the regression test is committed
- If the issue was environmental or timing-dependent, add monitoring or logging for future investigation
- Show the user the passing verification output — proof, not promises
