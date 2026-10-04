---
name: red
description: TDD Red Phase - Activate ONE test from the test list and make it fail with explicit predictions
---

# TDD Red Phase

You are now in the **Red Phase** of TDD. Follow these instructions to activate ONE test and make it fail.

## Your Mission

1. Activate exactly ONE test from the test list
2. Make explicit predictions about how it will fail
3. Verify the test fails for the right reason
4. Maintain strict discipline - NO implementation during Red phase

## Context: $ARGUMENTS

## Red Phase Rules

- **One test at a time**: Convert exactly ONE `it.todo()` to executable test
- **All other tests remain as `it.todo()`**: Never have more than one failing test
- **Two-stage failure**: First compilation error, then runtime/assertion error
- **Make predictions**: Explicitly state expected failures before running tests
- **No implementation**: Don't write code to make test pass yet

## Process

### Step 1: Activate One Test

Identify the next `it.todo()` and convert it to executable test code:

```typescript
// Convert from:
it.todo("should return 0 for empty input");

// To:
it("should return 0 for empty input", () => {
  expect(calculate("")).toBe(0);
});
```

Leave all other tests as `it.todo()`.

### Step 2: Predict Compilation Error

Before running the test, state your prediction:

```
Red Phase - Compilation Error Prediction:
- Test: "should return 0 for empty input"
- Expected: Compilation error
- Reason: Function `calculate` doesn't exist yet
- Error: "Cannot find name 'calculate'"
```

### Step 3: Run Test - Verify Compilation Error

Run `pnpm test` and verify:
- Compilation error as predicted, OR
- Prediction wrong -> STOP and explain discrepancy

### Step 4: Create Empty Function

Create minimal function stub (no logic):

```typescript
export const calculate = (input: string): number => {
  return undefined as unknown as number; // Intentionally wrong
};
```

### Step 5: Predict Runtime Error

Before running again, state your prediction:

```
Red Phase - Runtime Error Prediction:
- Test: "should return 0 for empty input"
- Expected: Runtime assertion error
- Expected value: 0
- Actual value: undefined
- Diff:
  Expected: 0
  Received: undefined
```

### Step 6: Run Test - Verify Runtime Error

Run `pnpm test` and verify:
- Assertion error as predicted, OR
- Prediction wrong -> STOP and explain discrepancy

### Step 7: Report Completion

You MUST output the full Step 7 block verbatim with `Correct` or `Incorrect`
chosen for each prediction. Do not abbreviate. Do not collapse the two
prediction lines into one.

**Why this format matters:** The block is mechanically parsed to compute
`predictions_correct_rate`. The parser expects two lines matching
`(- |Correct|Incorrect)` per cycle -- one for the compilation prediction,
one for the runtime prediction. Collapsing them into a single line, summarizing
them as "both correct", or skipping the block entirely drops the predictions
count for this cycle to zero. Format consistency here directly drives a metric
the experiment measures.

```
Red Phase Complete:
**Test Activated**: "should return 0 for empty input"
**Compilation Prediction**: Cannot find name 'calculate' Correct
**Runtime Prediction**: Expected 0, received undefined Correct
**Result**: Test fails as expected with assertion error

Proceeding to Green phase.
```

## Important Guidelines

### DO
- Activate exactly ONE test at a time
- Make explicit predictions before running tests
- Verify test fails for the right reason
- Keep all other tests as `it.todo()`

### DON'T
- Activate multiple tests
- Skip making predictions
- Write implementation to make test pass
- Continue if prediction fails without explanation

## Prediction Failure Protocol

If your prediction was wrong:

```
Prediction Failed:
- Predicted: [what you expected]
- Actual: [what happened]
- Discrepancy: [explanation]

Investigating the discrepancy before proceeding.
```

## Completion

After completing Red phase, proceed to Green phase:

```
Red Phase Complete. Proceeding to Green phase.
```
