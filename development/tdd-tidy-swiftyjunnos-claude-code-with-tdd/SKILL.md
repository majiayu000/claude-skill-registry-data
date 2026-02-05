---
name: tdd-tidy
description: Execute Kent Beck's Tidy First approach by making structural changes to code without changing behavior. Prepares code for easier behavioral changes by improving structure first.
---

# Tidy First - Structural Changes Only

## Overview

This skill implements Kent Beck's "Tidy First" philosophy. It focuses exclusively on structural improvements that make code easier to work with, without changing any behavior. These changes are committed separately from behavioral changes to maintain clear change history.

## When to Use

Use this skill when:
- Code structure is hindering progress
- About to add new behavior but code is messy
- Want to improve code readability before changes
- Need to separate structural from behavioral commits
- Following Tidy First workflow

## Philosophy

**Tidy First Principle:**
> Make the change easy, then make the easy change

**Key Concepts:**
- Structural changes NEVER alter behavior
- Tests must pass before AND after tidying
- Tidy changes are committed separately
- Tidying makes future behavioral changes easier
- Small, incremental structural improvements

## Workflow

### Step 1: Verify Tests Pass

**Confirm Prerequisites:**
1. ALL tests must be passing
2. No compiler warnings or errors
3. Code is in a stable state

**Establish Baseline:**
- Note which tests are passing
- These same tests must pass after tidying
- If tests fail after change, you changed behavior - revert

### Step 2: Identify Structural Improvements

**Purely Structural Changes (Safe):**
- **Renaming:** Variables, functions, classes for clarity
- **Extract Method:** Pull out cohesive blocks of code
- **Move Code:** Relocate to more logical locations
- **Reorganize Imports:** Clean up import statements
- **Format Code:** Consistent indentation and spacing
- **Add Comments:** Improve documentation
- **Remove Dead Code:** Delete unused code
- **Introduce Constant:** Replace magic numbers
- **Inline Temporary:** Remove unnecessary variables

**NOT Structural (Behavioral - Don't Do):**
- Changing algorithms or logic
- Adding new features
- Fixing bugs
- Modifying return values
- Changing control flow
- Altering data structures

### Step 3: Make Changes Incrementally

**One Change at a Time:**
1. Make ONE structural change
2. Run ALL tests immediately
3. Confirm tests still pass (exact same results)
4. If ANY test fails, you changed behavior - REVERT immediately
5. Repeat for next tidying

**Stay Disciplined:**
- No mixing structural and behavioral changes
- Tests must stay green throughout
- Each change should be small and reversible
- Don't get carried away - know when to stop

### Step 4: Prepare for Separate Commit

**Commit Discipline:**
- These changes should be committed separately
- Commit message should indicate "structural changes only"
- Use "refactor:" or "tidy:" prefix in commit message
- Make it clear no behavior was changed

**Example Commit Message:**
```
refactor: extract user validation logic to separate method

Structural changes only - no behavior modified.
```

### Step 5: Validate No Behavior Change

**Final Verification:**
1. Run complete test suite
2. All tests that passed before still pass
3. No new tests needed (behavior unchanged)
4. No test modifications (unless fixing test structure)

**Report:**
- List structural changes made
- Confirm all tests still pass
- Explain how structure is now improved
- Indicate code is ready for behavioral changes

## When to Tidy

**Before Adding Behavior:**
- Code is messy or unclear
- Structure will make new feature difficult
- Duplication exists where you'll work
- Names are confusing in area of change

**During TDD Cycle:**
- After GREEN phase, before next RED
- When refactoring reveals structural issues
- To separate concerns before growing code

**Don't Tidy:**
- If tests are failing
- When under extreme time pressure
- If change is already easy without tidying
- When behavior change is trivial

## Important Reminders

- **NEVER** change behavior while tidying
- **ALWAYS** keep tests green
- **ONE** structural change at a time
- **RUN** tests after each change
- **REVERT** if tests fail
- **COMMIT** separately from behavioral changes
- **STOP** when code is "tidy enough"

## Difference from Refactoring

**Tidy First:**
- Done BEFORE behavioral changes
- Prepares code for easier modification
- Separate commit from behavior
- Makes future work easier

**Refactor (TDD REFACTOR):**
- Done AFTER behavioral changes (GREEN phase)
- Cleans up implementation just added
- Part of TDD cycle
- Improves code just written

Both are structural, but timing and purpose differ.

## Next Steps

After completing Tidy First:
1. All tests must still pass
2. Commit structural changes separately
3. Now make behavioral changes with cleaner code
4. Follow with regular TDD cycle if adding features
