---
name: debug
description: "Discipline skill — systematic debugging process. Use when encountering any bug, debug issue, test failure, broken function, or unexpected behavior, before proposing fixes."
user-invocable: true
---

# Systematic Debugging

Random fixes waste time and create new bugs. Quick patches mask underlying issues.

**Core principle:** ALWAYS find root cause before attempting fixes.

## Usage

`/debug`

Invoke this skill when encountering any bug, test failure, or unexpected behavior. Follow the four phases in order.

## When to use

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

## The Iron Law

```text
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

If you haven't completed Phase 1, you cannot propose fixes.

## The Four Phases

Complete each phase before proceeding to the next.

### Phase 1: Root Cause Investigation

**BEFORE attempting ANY fix:**

1. **Read Error Messages Carefully**
   - Don't skip past errors or warnings
   - Read stack traces completely
   - Note line numbers, file paths, error codes

2. **Reproduce Consistently**
   - Can you trigger it reliably?
   - What are the exact steps?
   - If not reproducible, gather more data — don't guess

3. **Check Recent Changes**
   - What changed that could cause this?
   - Git diff, recent commits
   - New dependencies, config changes

4. **Gather Evidence in Multi-Component Systems**
   - Log what data enters each component boundary
   - Log what data exits each component boundary
   - Verify environment/config propagation
   - Run once to gather evidence showing WHERE it breaks
   - THEN investigate that specific component

5. **Trace Data Flow**
   - Where does the bad value originate?
   - What called this with the bad value?
   - Keep tracing up until you find the source
   - Fix at source, not at symptom

### Phase 2: Pattern Analysis

1. **Find Working Examples** — locate similar working code in the same codebase
2. **Compare Against References** — read reference implementations COMPLETELY, don't skim
3. **Identify Differences** — list every difference between working and broken, however small
4. **Understand Dependencies** — what components, settings, environment does it need?

### Phase 3: Hypothesis and Testing

1. **Form Single Hypothesis** — "I think X is the root cause because Y"
2. **Test Minimally** — smallest possible change, one variable at a time
3. **Verify** — did it work? Yes = Phase 4. No = new hypothesis. DON'T stack fixes.

### Phase 4: Implementation

1. **Create Failing Test Case** — simplest possible reproduction, automated if possible. Use `/tdd` for proper failing tests.
2. **Implement Single Fix** — address the root cause, ONE change at a time, no "while I'm here" improvements.
3. **Verify Fix** — test passes? No other tests broken? Issue actually resolved? Use `/verify` before claiming done.

**If fix doesn't work:**

- If < 3 attempts: return to Phase 1, re-analyze with new information
- **If >= 3 attempts: STOP and question the architecture**

**3+ failed fixes indicate an architectural problem:**

- Each fix reveals new coupling in different places
- Fixes require massive refactoring
- Each fix creates new symptoms elsewhere
- Discuss with the user before attempting more fixes

## Red Flags - STOP and Follow Process

- "Quick fix for now, investigate later"
- "Just try changing X and see if it works"
- "Add multiple changes, run tests"
- "It's probably X, let me fix that"
- "I don't fully understand but this might work"
- Proposing solutions before tracing data flow
- "One more fix attempt" (when already tried 2+)

**ALL of these mean: STOP. Return to Phase 1.**

## Common Rationalizations

| Excuse                                    | Reality                                                                  |
| ----------------------------------------- | ------------------------------------------------------------------------ |
| "Issue is simple, don't need process"     | Simple issues have root causes too. Process is fast for simple bugs.     |
| "Emergency, no time for process"          | Systematic debugging is FASTER than guess-and-check thrashing.           |
| "Just try this first, then investigate"   | First fix sets the pattern. Do it right from the start.                  |
| "I'll write test after confirming fix"    | Untested fixes don't stick. Test first proves it.                        |
| "Multiple fixes at once saves time"       | Can't isolate what worked. Causes new bugs.                              |
| "I see the problem, let me fix it"        | Seeing symptoms is not understanding root cause.                         |

## Quick Reference

| Phase                  | Key Activities                                         | Success Criteria            |
| ---------------------- | ------------------------------------------------------ | --------------------------- |
| **1. Root Cause**      | Read errors, reproduce, check changes, gather evidence | Understand WHAT and WHY     |
| **2. Pattern**         | Find working examples, compare                         | Identify differences        |
| **3. Hypothesis**      | Form theory, test minimally                            | Confirmed or new hypothesis |
| **4. Implementation**  | Create test, fix, verify                               | Bug resolved, tests pass    |

## Related Skills

- `/tdd` — TDD cycle for creating failing test cases in Phase 4
- `/verify` — verification before claiming the fix is complete
