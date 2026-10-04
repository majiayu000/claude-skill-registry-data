---
name: green
description: TDD Green Phase - Implement minimal code to make the failing test pass
---

# TDD Green Phase

You are now in the **Green Phase** of TDD. Follow these instructions to make the failing test pass with MINIMAL code.

## Why minimality matters

The Green Phase deliberately writes the smallest implementation that turns the active test green -- even hardcoded returns, even obviously-incomplete logic. This is not laziness or naivete:

- It **exposes refactoring opportunities** in the next phase. When the implementation does exactly one thing, structural smells are visible. Over-implemented green code looks "already clean" and hides design problems.
- It **prevents premature generalization**. The shape of the right abstraction emerges from the second and third test, not the first. Implementing for hypothetical future tests locks in a design before its constraints are known.
- It **keeps the red-green-refactor cycle short**. Each cycle pays a cost in tokens and context; over-implementing in green collapses several future cycles into one large one and loses the per-test feedback loop.

## Your Mission

1. Implement the **minimal code** necessary to make the failing test pass
2. Use the **simplest possible solution** (hardcoded values are acceptable)
3. Avoid adding features for future tests
4. Verify all tests pass
5. NO optimization, NO refactoring yet

## Context: $ARGUMENTS

## Green Phase Rules

- **Minimal code only**: Just enough to pass the current test
- **Baby steps**: Make the smallest possible change
- **No future features**: Don't implement what future tests might need
- **Simple is better**: Hardcoded returns are perfectly fine
- **Tests must pass**: Verify all tests are green
- **No refactoring yet**: Save improvements for Refactor phase

## Process

### Step 1: Analyze the Failing Test

Understand what the test expects:
- What input does the test provide?
- What output does it expect?
- What is the **simplest** way to produce that output?

### Step 2: Write Minimal Implementation

Implement **only what's needed** to make the current test pass:

```typescript
// For first test "should return 0 for empty input":
export const calculate = (input: string): number => {
  return 0; // Minimal - just make the test pass
};

// For second test "should return number for single input":
export const calculate = (input: string): number => {
  if (input === "") return 0;
  return parseInt(input); // Still simple
};

// For third test "should add two numbers":
export const calculate = (input: string): number => {
  if (input === "") return 0;
  const numbers = input.split(",");
  if (numbers.length === 1) return parseInt(numbers[0]);
  return parseInt(numbers[0]) + parseInt(numbers[1]); // Only now add logic
};
```

### Step 3: Run Tests

Run `pnpm test` and verify:
- Current test now passes
- All previous tests still pass

### Step 4: Verify No Over-Implementation

Check yourself:
- Did I implement features for future tests? -> Remove them
- Did I add logic not demanded by current test? -> Remove it
- Did I optimize prematurely? -> Simplify
- Did I refactor existing code? -> Revert, save for Refactor phase

### Step 5: Report Completion

```
Green Phase Complete:
**Implementation**: [brief description of what was added]
**Result**: All tests now pass ([X] passing)
**Approach**: [explain why this is minimal]

Proceeding to Refactor phase.
```

## Minimal Implementation Strategies

### Hardcoded Returns (Preferred for Early Tests)
```typescript
// Test: "should return 0 for empty input"
return 0; // Perfect - minimal
```

### Simple Conditionals (When Multiple Tests)
```typescript
// Test: "should return number for single input"
if (input === "") return 0;
return parseInt(input); // Still simple
```

### Generalization (Only When Forced)
```typescript
// Test: "should add multiple numbers" - NOW generalize
return input.split(",").reduce((sum, n) => sum + parseInt(n), 0);
```

## Important Guidelines

### DO
- Write minimal code to make test pass
- Use hardcoded values when appropriate
- Take baby steps
- Verify all tests pass

### DON'T
- Implement beyond what tests demand
- Add features for future tests
- Optimize prematurely
- Refactor during Green phase

## Psychological Resistance

You will feel resistance:
- **"This is too simple"** -> That's correct! Minimal is the way
- **"Hardcoded values feel wrong"** -> They're exactly right for early tests
- **"I should implement ahead"** -> Resist this strongly
- **"This is inefficient"** -> Actually accelerates development

Trust the process. Simple steps compound into elegant solutions.

## Completion

After completing Green phase, proceed to Refactor phase:

```
Green Phase Complete. Proceeding to Refactor phase.
```
