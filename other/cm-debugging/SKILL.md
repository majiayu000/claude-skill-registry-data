---
name: cm-debugging
description: Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes
token_budget: 1500
compressed: true
deprecated: false
---

# Systematic Debugging

## TL;DR
- **Use when** any bug, test failure, or unexpected behavior surfaces
- **Process**: reproduce → isolate → diagnose root cause → fix
- **Defense in depth**: also add a test that locks the bug
- **Next**: cm-tdd → cm-quality-gate

## Overview

Random fixes waste time and create new bugs. Quick patches mask underlying issues.

**Core principle:** ALWAYS find root cause before attempting fixes. Symptom fixes are failure.

**Violating the letter of this process is violating the spirit of debugging.**

## The Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

If you haven't completed Phase 1, you cannot propose fixes.

## When to Use

Use for ANY technical issue:
- Test failures
- Bugs in production
- Unexpected behavior
- Performance problems
- Build failures
- Integration issues

**Use this ESPECIALLY when:**
- Under time pressure (emergencies make guessing tempting)
- "Just one quick fix" seems obvious
- You've already tried multiple fixes
- Previous fix didn't work
- You don't fully understand the issue

**Don't skip when:**
- Issue seems simple (simple bugs have root causes too)
- You're in a hurry (rushing guarantees rework)
- Manager wants it fixed NOW (systematic is faster than thrashing)

## The Four Phases

You MUST complete each phase before proceeding to the next.

### Phase 0.5: Memory Integrity Check (BEFORE blaming code)

> **BEFORE blaming code, ASK: "Could memory be causing this bug?"**

1. **SUSPECT** — Identify relevant memories:
   - What module/file is the bug in?
   - Read `.cm/learnings.json` filtered by that scope
   - List all active learnings + decisions for this area

2. **INVESTIGATE** — Did AI follow a memory when writing buggy code?
   - Check: Does the buggy code match a `prevention` pattern from any learning?
   - Check: Does the buggy code follow a `decision` that may be outdated?
   - If YES → that memory is a **suspect**

3. **VERIFY** — Is the suspect memory still correct?
   - Compare learning with current codebase (not when it was recorded)
   - Has the dependency/pattern/architecture changed since learning was recorded?
   - If memory is WRONG → proceed to HEAL

4. **HEAL** (only if memory confirmed as cause):
   - **Invalidate:** Set `status = "invalidated"` — learning is proven wrong
   - **Correct:** Update `prevention` with correct info, set `status = "corrected"`
   - **Scope-reduce:** Learning is right for smaller scope → narrow the scope
   - **Record meta-learning** in `.cm/meta-learnings.json`

```
IF memory caused the bug:
  → HEAL memory FIRST
  → THEN proceed to Phase 1 to fix code
  → The code fix will be correct because memory is now correct

IF memory did NOT cause the bug:
  → Proceed to Phase 1 normally
```

> **WHY PHASE 0.5?** Fix memory first → code fix will be correct.
> Without fixing memory → bug will return next session (bug loop).

### Phase 1: Root Cause Investigation

**BEFORE attempting ANY fix:**

1. **Read Error Messages Carefully**
   - Don't skip past errors or warnings
   - They often contain the exact solution
   - Read stack traces completely
   - Note line numbers, file paths, error codes

2. **Reproduce Consistently**
   - Can you trigger it reliably?
   - What are the exact steps?
   - Does it happen every time?
   - If not reproducible → gather more data, don't guess

3. **Check Recent Changes**
   - What changed that could cause this?
   - Git diff, recent commits
   - New dependencies, config changes
   - Environmental differences

4. **Gather Evidence in Multi-Component Systems**

   **WHEN system has multiple components (CI → build → signing, API → service → database):**

   **BEFORE proposing fixes, add diagnostic instrumentation:**
   ```
   For EACH component boundary:
     - Log what data enters component
     - Log what data exits component
     - Verify environment/config propagation
     - Check state at each layer

   Run once to gather evidence showing WHERE it breaks
   THEN analyze evidence to identify failing component
   THEN investigate that specific component
   ```

5. **Trace Data Flow**

   **WHEN error is deep in call stack:**

   - Where does bad value originate?
   - What called this with bad value?
   - Keep tracing up until you find the source
   - Fix at source, not at symptom

### Phase 2: Pattern Analysis

**Find the pattern before fixing:**

1. **Find Working Examples**
   - Locate similar working code in same codebase
   - What works that's similar to what's broken?

2. **Compare Against References**
   - If implementing pattern, read reference implementation COMPLETELY
   - Don't skim - read every line
   - Understand the pattern fully before applying

3. **Identify Differences**
   - What's different between working and broken?
   - List every difference, however small
   - Don't assume "that can't matter"

4. **Understand Dependencies**
   - What other components does this need?
   - What settings, config, environment?
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
   - Automated test if possible
   - MUST have before fixing
   - Use the `cm-tdd` skill for writing proper failing tests

2. **Implement Single Fix**
   - Address the root cause identified
   - ONE change at a time
   - No "while I'm here" improvements
   - No bundled refactoring

3. **Verify Fix**
   - Test passes now?
   - No other tests broken?
   - Issue actually resolved?

4. **If Fix Doesn't Work**
   - STOP
   - Count: How many fixes have you tried?
   - If < 3: Return to Phase 1, re-analyze with new information
   - **If ≥ 3: STOP and question the architecture (step 5 below)**
   - DON'T attempt Fix #4 without architectural discussion

5. **If 3+ Fixes Failed: Question Architecture**

   **Pattern indicating architectural problem:**
   - Each fix reveals new shared state/coupling/problem in different place
   - Fixes require "massive refactoring" to implement
   - Each fix creates new symptoms elsewhere

   **Discuss with your human partner before attempting more fixes**

   This is NOT a failed hypothesis - this is a wrong architecture.

### Step 5: Record Learning (MANDATORY)

After fixing any bug, ALWAYS write to `.cm/CONTINUITY.md` → "Mistakes & Learnings":

```
- What Failed:      [exact error message or behavior]
- Why It Failed:    [root cause from Phase 1]
- How to Prevent:   [concrete pattern to avoid]
- Scope:            [global | module:{name} | file:{path}]
```

**Scope rules:** Choose the SMALLEST scope that applies.
- Bug in one file → `file:src/api/routes.ts`
- Bug in module pattern → `module:auth`
- Bug in project-wide practice → `global`

**Anti-duplicate:** If a similar learning already exists in `.cm/learnings.json`,
reinforce it (reinforceCount++) instead of creating a new entry.

> **Token savings:** Next time same error pattern appears, AI reads the learning
> (~50 tokens) instead of repeating full 4-phase debug cycle (~3,000 tokens).
> **This is the #1 token saver in the entire kit.**

---

## Red Flags - STOP and Follow Process

If you catch yourself thinking:
- "Quick fix for now, investigate later"
- "Just try changing X and see if it works"
- "Add multiple changes, run tests"
- "Skip the test, I'll manually verify"
- "It's probably X, let me fix that"
- "I don't fully understand but this might work"
- "Pattern says X but I'll adapt it differently"
- "Here are the main problems: [lists fixes without investigation]"
- Proposing solutions before tracing data flow
- **"One more fix attempt" (when already tried 2+)**
- **Each fix reveals new problem in different place**

**ALL of these mean: STOP. Return to Phase 1.**

**When you see these user signals:** STOP. Return to Phase 1.
- "Stop guessing"
- "Ultrathink this"

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Issue is simple, don't need process" | Simple issues have root causes too. Process is fast for simple bugs. |
| "Emergency, no time for process" | Systematic debugging is FASTER than guess-and-check thrashing. |
| "Just try this first, then investigate" | First fix sets the pattern. Do it right from the start. |
| "I'll write test after confirming fix works" | Untested fixes don't stick. Test first proves it. |
| "Multiple fixes at once saves time" | Can't isolate what worked. Causes new bugs. |

## Quick Reference

| Phase | Key Activities | Success Criteria |
|-------|---------------|------------------|
| **1. Root Cause** | Read errors, reproduce, check changes, gather evidence | Understand WHAT and WHY |
| **2. Pattern** | Find working examples, compare | Identify differences |
| **3. Hypothesis** | Form theory, test minimally | Confirmed or new hypothesis |
| **4. Implementation** | Create test, fix, verify | Bug resolved, tests pass |

## When Process Reveals "No Root Cause"

If systematic investigation reveals issue is truly environmental, timing-dependent, or external:

1. You've completed the process
2. Document what you investigated
3. Implement appropriate handling (retry, timeout, error message)
4. Add monitoring/logging for future investigation

**But:** 95% of "no root cause" cases are incomplete investigation.

## Integration

**Related skills:**
- **cm-tdd** - For creating failing test case (Phase 4, Step 1)
- **cm-quality-gate** - Verify fix worked before claiming success
