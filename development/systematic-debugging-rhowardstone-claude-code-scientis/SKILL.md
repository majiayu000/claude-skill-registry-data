---
name: systematic-debugging
description: Use when encountering any bug, test failure, unexpected result, or failed replication - before proposing fixes or explanations
---

# Systematic Debugging

## Overview

Random fixes waste time and create new problems. Quick patches mask underlying issues.

**Core principle:** ALWAYS find root cause before attempting fixes. Symptom fixes are failure.

**Violating the letter of this process is violating the spirit of debugging.**

## The Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

If you haven't completed Phase 1, you cannot propose fixes.

## When to Use

Use for ANY unexpected outcome:

**In software:** Test failures, bugs, unexpected behavior, performance problems, build failures, integration issues

**In research:** Failed replications, unexpected results, null findings, contradictory data, equipment issues, protocol failures

**Use this ESPECIALLY when:**
- Under time pressure (emergencies make guessing tempting)
- "Just one quick fix" seems obvious
- You've already tried multiple fixes
- Previous fix didn't work
- You don't fully understand the issue

**Don't skip when:**
- Issue seems simple (simple issues have root causes too)
- You're in a hurry (systematic is faster than thrashing)
- Someone wants it fixed NOW (systematic is faster than thrashing)

## The Four Phases

You MUST complete each phase before proceeding to the next.

### Phase 1: Root Cause Investigation

**BEFORE attempting ANY fix:**

1. **Read Error Messages/Outputs Carefully**
   - Don't skip past errors, warnings, or anomalies
   - They often contain the exact solution
   - Read stack traces/logs completely
   - Note specifics: line numbers, values, timestamps

2. **Reproduce Consistently**
   - Can you trigger it reliably?
   - What are the exact steps/conditions?
   - Does it happen every time?
   - If not reproducible → gather more data, don't guess

3. **Check Recent Changes**
   - What changed that could cause this?
   - Code changes, protocol changes, equipment changes
   - New dependencies, config, reagents, parameters
   - Environmental differences

4. **Gather Evidence in Multi-Component Systems**

   **WHEN system has multiple components:**

   **For software:** CI → build → deploy, API → service → database
   **For research:** Sample prep → measurement → analysis, multiple experimental stages

   **BEFORE proposing fixes, add diagnostic instrumentation:**
   ```
   For EACH component boundary:
     - Log/record what data enters component
     - Log/record what data exits component
     - Verify environment/conditions at each layer
     - Check state at each stage

   Run once to gather evidence showing WHERE it breaks
   THEN analyze evidence to identify failing component
   THEN investigate that specific component
   ```

5. **Trace Data/Causation Flow**
   - Where does the bad value/result originate?
   - What upstream process produced this?
   - Keep tracing backward until you find the source
   - Fix at source, not at symptom

### Phase 2: Pattern Analysis

**Find the pattern before fixing:**

1. **Find Working Examples**
   - Locate similar working code/experiments in same project
   - What works that's similar to what's broken?

2. **Compare Against References**
   - If implementing pattern/protocol, read reference COMPLETELY
   - Don't skim - read every line/step
   - Understand the pattern fully before applying

3. **Identify Differences**
   - What's different between working and broken?
   - List every difference, however small
   - Don't assume "that can't matter"

4. **Understand Dependencies**
   - What other components/conditions does this need?
   - What settings, config, environment, reagents?
   - What assumptions does it make?

### Phase 3: Hypothesis and Testing

**Scientific method:**

1. **Form Single Hypothesis**
   - State clearly: "I think X is the root cause because Y"
   - Write it down
   - Be specific, not vague

2. **Test Minimally**
   - Make the SMALLEST possible change to test hypothesis
   - One variable at a time
   - Don't fix multiple things at once

3. **Verify Before Continuing**
   - Did it work? Yes → Phase 4
   - Didn't work? Form NEW hypothesis
   - DON'T add more fixes on top

4. **When You Don't Know**
   - Say "I don't understand X"
   - Don't pretend to know
   - Ask for help
   - Research more

### Phase 4: Implementation

**Fix the root cause, not the symptom:**

1. **Create Failing Test Case**
   - Simplest possible reproduction
   - Automated test if possible (software) or documented protocol (research)
   - MUST have before fixing

2. **Implement Single Fix**
   - Address the root cause identified
   - ONE change at a time
   - No "while I'm here" improvements
   - No bundled changes

3. **Verify Fix**
   - Test passes now? Experiment works?
   - No other tests/results broken?
   - Issue actually resolved?

4. **If Fix Doesn't Work**
   - STOP
   - Count: How many fixes have you tried?
   - If < 3: Return to Phase 1, re-analyze with new information
   - **If ≥ 3: STOP and question the architecture/approach (step 5 below)**
   - DON'T attempt Fix #4 without fundamental discussion

5. **If 3+ Fixes Failed: Question Fundamentals**

   **Pattern indicating fundamental problem:**
   - Each fix reveals new problem in different place
   - Fixes require "massive changes" to implement
   - Each fix creates new symptoms elsewhere

   **STOP and question fundamentals:**
   - Is this approach fundamentally sound?
   - Are we "sticking with it through sheer inertia"?
   - Should we redesign vs. continue fixing symptoms?

   **Discuss before attempting more fixes**

## Red Flags - STOP and Follow Process

If you catch yourself thinking:
- "Quick fix for now, investigate later"
- "Just try changing X and see if it works"
- "Add multiple changes, run tests"
- "Skip the test, I'll manually verify"
- "It's probably X, let me fix that"
- "I don't fully understand but this might work"
- "Reference says X but I'll adapt it differently"
- "Here are the main problems: [lists fixes without investigation]"
- Proposing solutions before tracing causation
- **"One more fix attempt" (when already tried 2+)**
- **Each fix reveals new problem in different place**

**ALL of these mean: STOP. Return to Phase 1.**

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Issue is simple, don't need process" | Simple issues have root causes too. Process is fast for simple problems. |
| "Emergency, no time for process" | Systematic debugging is FASTER than guess-and-check thrashing. |
| "Just try this first, then investigate" | First fix sets the pattern. Do it right from the start. |
| "I'll write test after confirming fix works" | Untested fixes don't stick. Test first proves it. |
| "Multiple fixes at once saves time" | Can't isolate what worked. Causes new problems. |
| "Reference too long, I'll adapt the pattern" | Partial understanding guarantees problems. Read it completely. |
| "I see the problem, let me fix it" | Seeing symptoms ≠ understanding root cause. |
| "One more fix attempt" (after 2+ failures) | 3+ failures = fundamental problem. Question approach, don't fix again. |

## Quick Reference

| Phase | Key Activities | Success Criteria |
|-------|---------------|------------------|
| **1. Root Cause** | Read outputs, reproduce, check changes, gather evidence | Understand WHAT and WHY |
| **2. Pattern** | Find working examples, compare | Identify differences |
| **3. Hypothesis** | Form theory, test minimally | Confirmed or new hypothesis |
| **4. Implementation** | Create test, fix, verify | Problem resolved, tests pass |

## Real-World Impact

From debugging sessions:
- Systematic approach: 15-30 minutes to fix
- Random fixes approach: 2-3 hours of thrashing
- First-time fix rate: 95% vs 40%
- New problems introduced: Near zero vs common
