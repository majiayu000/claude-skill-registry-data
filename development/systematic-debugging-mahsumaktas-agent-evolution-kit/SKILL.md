---
name: systematic-debugging
description: "Systematic debugging process for any error, test failure, or unexpected behavior. Investigate root cause BEFORE proposing a fix."
---

# Systematic Debugging

## Overview

Random fixes waste time and create new bugs. Quick patches mask underlying problems.

**Core principle:** ALWAYS find the root cause before fixing. Symptom fixes are failures.

**Violating the letter of this process violates the spirit of debugging.**

## Iron Rule

```
NO FIX WITHOUT ROOT CAUSE INVESTIGATION
```

If you have not completed Phase 1, you may not propose a fix.

## When to Use

**For EVERY technical problem:**
- Test failures
- Production errors
- Unexpected behavior
- Performance issues
- Build failures
- Integration problems

**ESPECIALLY when:**
- Under time pressure (urgency makes guessing tempting)
- A "quick fix" seems obvious
- Multiple fixes have been tried
- A previous fix did not work
- You do not fully understand the problem

**Do not skip because:**
- The problem looks simple (simple problems have root causes too)
- You are in a hurry (rushing guarantees rework)
- A manager wants it fixed NOW (systematic is faster than thrashing)

## Four Phases

Do NOT proceed to the next phase without completing the current one.

### Phase 1: Root Cause Investigation

**BEFORE attempting ANY fix:**

1. **Read Error Messages Carefully**
   - Do not skip errors or warnings
   - They usually contain the exact solution
   - Read stack traces completely
   - Note line numbers, file paths, error codes

2. **Reproduce Consistently**
   - Can you trigger it reliably?
   - What are the exact steps?
   - Does it happen every time?
   - If not reproducible, gather more data -- do NOT guess

3. **Check Recent Changes**
   - What changed that could cause this?
   - Git diff, recent commits
   - New dependencies, config changes
   - Environment differences

4. **Gather Evidence Across Components**

   If the system has multiple components (API, service, database, etc.):

   ```
   FOR EACH component boundary:
     - Log the data entering the component
     - Log the data leaving the component
     - Verify environment/config propagation
     - Check state at each layer

   Run once to gather evidence --> show WHERE it breaks
   THEN analyze evidence to identify the failing component
   THEN investigate that specific component
   ```

5. **Trace the Data Flow**

   If the error is deep in the call stack:
   - Where was the bad value created?
   - Who passed this bad value?
   - Trace backward until you find the source
   - Fix at the source, not at the symptom

### Phase 2: Pattern Analysis

**Before fixing, find the pattern:**

1. **Find Working Examples**
   - Find similar working code in the same codebase
   - What works that is similar to what is broken?

2. **Compare with Reference**
   - If you are implementing a pattern, read the reference implementation COMPLETELY
   - Do not skim -- read every line
   - Understand the pattern fully before applying

3. **Identify Differences**
   - What is different between working and broken?
   - List every difference, no matter how small
   - Do not assume "that is not important"

4. **Understand Dependencies**
   - What other components does this need?
   - What settings, config, environment?
   - What assumptions are being made?

### Phase 3: Hypothesis and Test

**Scientific method:**

1. **Form a Single Hypothesis**
   - State clearly: "I believe the root cause is X because Y"
   - Write it down
   - Be specific, not vague

2. **Test with Minimum Change**
   - Make the SMALLEST POSSIBLE change to test the hypothesis
   - One variable at a time
   - Do not fix multiple things at once

3. **Verify Before Proceeding**
   - Did it work? Yes --> Phase 4
   - Did it not work? Form a NEW hypothesis
   - Do NOT pile more fixes on top

4. **If You Do Not Know**
   - Say "I do not understand X"
   - Do not pretend you do
   - Ask for help
   - Research further

### Phase 4: Implementation

**Fix the root cause, not the symptom:**

1. **Create a Failing Test**
   - Simplest possible reproduction
   - Automated test if possible
   - One-off test script if no framework exists
   - Must exist BEFORE the fix
   - **REQUIRED SKILL:** `tdd-workflow` (when writing the fix)

2. **Apply a Single Fix**
   - Address the identified root cause
   - ONE change at a time
   - No "while I am here" improvements
   - No bundled refactoring

3. **Verify the Fix**
   - Does the test pass now?
   - Did any other tests break?
   - Is the problem actually resolved?

4. **If the Fix Does Not Work**
   - STOP
   - Count: How many fixes have you attempted?
   - Fewer than 3: Return to Phase 1, re-analyze with new information
   - **3 or more: STOP and question the architecture (see step 5 below)**
   - Do NOT attempt a 4th fix without the architecture discussion

5. **3+ Fixes Failed: Question the Architecture**

   **Indicators of an architectural problem:**
   - Each fix exposes new shared state, coupling, or issues in a different place
   - Fixes require "massive refactoring" to apply
   - Each fix creates new symptoms elsewhere

   **STOP and question the fundamentals:**
   - Is this pattern fundamentally sound?
   - Are we continuing just because of inertia?
   - Should we refactor the architecture instead of patching symptoms?

   **Discuss with the user before attempting more fixes.**

   This is not a failed hypothesis -- it is a wrong architecture.

## Red Flags -- STOP and Follow the Process

If you catch yourself thinking:
- "Quick fix for now, I will investigate later"
- "Let me just change X and see if it works"
- "Make multiple changes, run the tests"
- "Skip the test, I will verify manually"
- "Probably X, let me fix that"
- "I do not fully understand but this might work"
- "The pattern says X but I will adapt it differently"
- "The main issues are: [list of fixes without investigation]"
- Proposing a solution without tracing the data flow
- **"One more fix attempt" (after 2+ failures)**
- **Each fix exposing new problems in different places**

**ALL OF THESE MEAN: STOP. Return to Phase 1.**

**If 3+ fixes have failed:** Question the architecture (see Phase 4.5).

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Problem is simple, no need for the process" | Simple problems have root causes too. The process is fast for simple bugs. |
| "Emergency, no time for process" | Systematic debugging is FASTER than guess-and-check thrashing. |
| "Let me try this first, then investigate" | The first fix sets the pattern. Get it right from the start. |
| "I will write the test after verifying the fix works" | Untested fixes do not hold. Test first to prove it. |
| "Fixing multiple things at once saves time" | You cannot isolate what worked. Creates new bugs. |
| "The reference is too long, I will adapt the pattern" | Partial understanding GUARANTEES errors. Read it all. |
| "I can see the problem, let me fix it" | Seeing the symptom is not understanding the root cause. |
| "One more fix attempt" (after 2+ failures) | 3+ failures = architectural problem. Question the pattern, do not keep patching. |

## Quick Reference

| Phase | Key Activities | Success Criteria |
|-------|---------------|-----------------|
| **1. Root Cause** | Read errors, reproduce, check changes, gather evidence | Understand WHAT and WHY |
| **2. Pattern** | Find working examples, compare | Identify differences |
| **3. Hypothesis** | Form theory, test with minimum change | Verified or new hypothesis |
| **4. Implementation** | Create test, fix, verify | Bug resolved, tests pass |

## Supporting Techniques

- **Binary search:** Narrow down the problem by bisecting the code
- **Git bisect:** Find the commit that introduced the bug (`git bisect start`)
- **Log analysis:** Examine system logs, search for patterns
- **Minimal reproduction:** Reproduce the problem with the smallest possible example

**Related skills:**
- **`tdd-workflow`** -- Creating a failing test (Phase 4, Step 1)
- **`verification-gate`** -- Do NOT claim success without verifying the fix works
