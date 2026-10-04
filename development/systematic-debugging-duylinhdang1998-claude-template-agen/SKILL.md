---
name: systematic-debugging
description: Use when encountering any bug, test failure, or unexpected behavior. 4-phase root cause investigation BEFORE proposing fixes. Use for production bugs, test failures, performance issues, build failures.
---

# Systematic Debugging

## The Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

Random fixes waste time and create new bugs. Quick patches mask underlying issues.

**If you haven't completed Phase 1, you cannot propose fixes.**

## When to Use

Use for ANY technical issue:
- Test failures
- Bugs in production
- Unexpected behavior
- Performance problems
- Build failures
- Integration issues

**ESPECIALLY when:**
- Under time pressure (rushing = thrashing)
- "Quick fix" seems obvious
- You've already tried multiple fixes
- Previous fix didn't work

## The Four Phases

```
┌────────────────────────────────────────────────────────────┐
│                                                            │
│  Phase 1         Phase 2         Phase 3         Phase 4   │
│  ┌───────┐      ┌─────────┐     ┌────────────┐  ┌───────┐ │
│  │ ROOT  │ ───► │ PATTERN │ ──► │ HYPOTHESIS │─►│  FIX  │ │
│  │ CAUSE │      │ ANALYSIS│     │   TEST     │  │       │ │
│  └───────┘      └─────────┘     └────────────┘  └───────┘ │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### Phase 1: Root Cause Investigation

**BEFORE attempting ANY fix:**

#### 1. Read Error Messages Carefully
```
Don't skip past errors or warnings
Read stack traces COMPLETELY
Note: line numbers, file paths, error codes
```

#### 2. Reproduce Consistently
- Can you trigger it reliably?
- What are the exact steps?
- If not reproducible → gather more data, don't guess

#### 3. Check Recent Changes
```bash
git diff HEAD~5
git log --oneline -10
```
What changed that could cause this?

#### 4. Trace Data Flow
Where does bad value originate?

```
Error at line 50
  ↑ Called from line 30 with bad value
    ↑ Value set at line 15
      ↑ ROOT CAUSE: Missing validation at line 10
```

**Fix at source, not at symptom.**

#### 5. Gather Evidence (Multi-Component Systems)

```bash
# Layer 1: Input
echo "=== Input data: ==="
echo "$INPUT"

# Layer 2: Processing
echo "=== After processing: ==="
echo "$PROCESSED"

# Layer 3: Output
echo "=== Final output: ==="
echo "$OUTPUT"
```

Run once → see WHERE it breaks → investigate that layer.

### Phase 2: Pattern Analysis

**Find the pattern before fixing:**

1. **Find Working Examples**
   - Similar working code in same codebase?
   - What works that's similar to what's broken?

2. **Compare Against References**
   - Read reference implementation COMPLETELY
   - Don't skim - read every line

3. **Identify Differences**
   - What's different between working and broken?
   - List EVERY difference, however small

### Phase 3: Hypothesis and Testing

**Scientific method:**

1. **Form Single Hypothesis**
   ```
   "I think X is the root cause because Y"
   ```
   Write it down. Be specific.

2. **Test Minimally**
   - SMALLEST possible change to test hypothesis
   - One variable at a time
   - Don't fix multiple things at once

3. **Verify Before Continuing**
   - Worked? → Phase 4
   - Didn't work? → NEW hypothesis
   - DON'T add more fixes on top

### Phase 4: Implementation

**Fix the root cause, not the symptom:**

1. **Create Failing Test**
   - Simplest possible reproduction
   - MUST have before fixing
   - Use `test-driven-development` skill

2. **Implement Single Fix**
   - Address root cause identified
   - ONE change at a time
   - No "while I'm here" improvements

3. **Verify Fix**
   - Test passes?
   - No other tests broken?
   - Issue actually resolved?

4. **If 3+ Fixes Failed: STOP**

   Pattern indicating architectural problem:
   - Each fix reveals new problem elsewhere
   - Fixes require "massive refactoring"
   - Each fix creates new symptoms

   **Question fundamentals:**
   - Is this pattern sound?
   - Should we refactor architecture vs. continue fixing?

   **Discuss with user before attempting more fixes**

## Red Flags - STOP and Return to Phase 1

- "Quick fix for now, investigate later"
- "Just try changing X and see"
- "Add multiple changes, run tests"
- "I don't fully understand but this might work"
- Proposing solutions before tracing data flow
- "One more fix attempt" (when already tried 2+)

## Quick Reference

| Phase | Key Activities | Success Criteria |
|-------|---------------|------------------|
| **1. Root Cause** | Read errors, reproduce, trace | Understand WHAT and WHY |
| **2. Pattern** | Find working examples, compare | Identify differences |
| **3. Hypothesis** | Form theory, test minimally | Confirmed or new hypothesis |
| **4. Fix** | Create test, fix, verify | Bug resolved, tests pass |

## Impact

- Systematic approach: 15-30 minutes to fix
- Random fixes approach: 2-3 hours of thrashing
- First-time fix rate: 95% vs 40%
- New bugs introduced: Near zero vs common
