---
name: tdd-refactor
description: Execute the REFACTOR phase of TDD by improving code structure while keeping all tests green. Removes duplication, improves naming, and enhances code quality without changing behavior.
---

# TDD REFACTOR Phase

## Overview

This skill executes the REFACTOR phase of Test-Driven Development. It improves code quality, removes duplication, and enhances structure while ensuring all tests remain green. Changes are purely structural with no behavioral modifications.

## When to Use

Use this skill when:
- All tests are passing (GREEN phase completed)
- Code has duplication or code smells
- Naming could be clearer
- Structure could be improved
- Following the TDD RED → GREEN → REFACTOR cycle

## Workflow

### Step 1: Verify GREEN State

**Confirm Prerequisites:**
1. ALL tests must be passing
2. No compiler warnings or errors
3. Code is in a working state

**If Tests Fail:**
- Do NOT refactor
- Fix failing tests first
- Return to GREEN phase

### Step 2: Identify Refactoring Opportunities

**Look for Code Smells:**
- Duplication (same code in multiple places)
- Long methods that do too much
- Unclear variable or method names
- Complex conditional logic
- Hidden dependencies
- Poor separation of concerns

**Common Refactorings:**
- Extract Method
- Rename Variable/Method/Class
- Inline Method
- Move Method
- Replace Magic Number with Constant
- Simplify Conditional Expression
- Remove Dead Code

### Step 3: Refactor Incrementally

**One Change at a Time:**
1. Make ONE structural change
2. Run ALL tests immediately
3. Confirm tests still pass (behavior unchanged)
4. If tests fail, revert and try differently
5. Repeat for next refactoring

**Keep Tests Green:**
- Never let tests go red during refactoring
- If a test fails, you changed behavior - revert immediately
- Run tests after EVERY change, not just at the end

### Step 4: Distinguish Change Types

**Structural Changes (Safe to commit together):**
- Renaming for clarity
- Extracting methods
- Moving code to better locations
- Reorganizing imports
- Formatting improvements
- Comment additions/improvements

**Behavioral Changes (Commit separately):**
- Adding new features
- Changing how code works
- Modifying functionality
- Fixing bugs

**Keep Them Separate:**
- Never mix structural and behavioral changes in same commit
- Follow Tidy First principle
- Structural changes should not alter any test results

### Step 5: Report Results

**Document Changes:**
- List what was refactored
- Explain why the refactoring improves code
- Confirm all tests still pass
- Note any remaining code smells for future cycles

## Refactoring Principles

**Safety First:**
- Always have green tests before refactoring
- Make small, incremental changes
- Run tests constantly
- Revert if anything breaks

**Quality Goals:**
- Remove duplication ruthlessly
- Express intent clearly through naming
- Make dependencies explicit
- Keep methods small and focused
- Minimize state and side effects

**When to Stop:**
- Code is clear and expressive
- Duplication is removed
- Structure is sound
- Further changes would be premature
- Time to move to next test

## Important Reminders

- **ONLY** refactor when tests are green
- **NEVER** change behavior during refactoring
- Make **ONE** change at a time
- Run tests after **EACH** change
- Revert if tests fail
- Keep structural changes separate from behavioral changes

## Next Steps

After completing REFACTOR phase:
1. All tests must still be passing
2. Consider committing structural changes (Tidy First)
3. Move to next RED phase for next test
4. Or complete the current TDD cycle with commits
