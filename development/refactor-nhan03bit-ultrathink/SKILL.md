---
name: refactor
description: Safe, incremental code refactoring with verification checkpoints and rollback safety
layer: hub
category: workflow
triggers:
  - "/refactor"
  - "refactor this"
  - "clean up this code"
  - "restructure this"
  - "extract this"
  - "simplify this"
inputs:
  - target: Code, file(s), or module to refactor
  - goal: What the refactoring should achieve (readability, modularity, testability, etc.)
  - constraints: What must NOT change (public API, behavior, performance characteristics)
outputs:
  - refactoringPlan: Step-by-step plan with verification at each step
  - changes: List of all modifications made
  - verificationResults: Test results and behavioral checks at each checkpoint
linksTo:
  - test
  - code-review
  - scout
  - debug
linkedFrom:
  - cook
  - team
  - ship
  - optimize
preferredNextSkills:
  - test
  - code-review
fallbackSkills:
  - debug
  - scout
riskLevel: medium
memoryReadPolicy: selective
memoryWritePolicy: selective
sideEffects:
  - Modifies source code files
  - May modify or create test files
  - Runs tests between refactoring steps
---

# Refactor Skill

## Purpose

Improve code structure, readability, and maintainability WITHOUT changing external behavior. Refactoring is the disciplined practice of restructuring existing code -- altering its internal structure without altering its external behavior.

The cardinal rule: **After refactoring, the system does exactly what it did before. Only the code is different.**

## Workflow

### Phase 1: Assessment

1. **Read the target code** thoroughly. Understand what it does, how it does it, and why it is structured the way it is.

2. **Identify the specific smells** -- What is wrong with the current structure?
   - **Long function/method**: Does too many things (> 30 lines is a signal)
   - **Deep nesting**: More than 3 levels of indentation
   - **Duplication**: Same or similar code in multiple places
   - **God object/module**: One file doing everything
   - **Primitive obsession**: Using raw types instead of domain objects
   - **Feature envy**: Code that uses another module's data more than its own
   - **Shotgun surgery**: A single change requires editing many files
   - **Unclear naming**: Variables/functions named `data`, `result`, `temp`, `handle`
   - **Dead code**: Unreachable or unused code
   - **Inappropriate coupling**: Modules that know too much about each other

3. **Define the refactoring goal** -- What does the code look like when we are done?
   - More readable? (clearer names, shorter functions)
   - More modular? (better separation of concerns)
   - More testable? (injectable dependencies, pure functions)
   - More extensible? (easier to add new features)

4. **Identify behavioral constraints** -- What must NOT change?
   - Public API signatures
   - External behavior (what callers observe)
   - Performance characteristics (within tolerance)
   - Side effects (file writes, API calls, database operations)

5. **Check test coverage** -- What tests exist for this code?
   - If tests exist: They are our safety net. Run them before and after each step.
   - If no tests exist: **Write characterization tests first** before refactoring. These tests capture the current behavior (even if it has bugs) so we can verify behavior is preserved.

### Phase 2: Refactoring Plan

6. **Break the refactoring into small, safe steps**. Each step should be:
   - **Atomic**: One type of change at a time (rename, extract, move, inline)
   - **Verifiable**: Tests can confirm behavior is preserved after this step
   - **Reversible**: If this step breaks something, it can be undone without affecting other steps

7. **Common refactoring moves** (use as building blocks):

   | Move | When to Use | Risk |
   |------|-------------|------|
   | **Rename** | Unclear names | Very Low |
   | **Extract function** | Long function, duplicated logic | Low |
   | **Extract module/file** | God object, mixed concerns | Medium |
   | **Inline** | Over-abstraction, wrapper adds no value | Low |
   | **Move** | Feature envy, wrong module | Medium |
   | **Replace conditional with polymorphism** | Complex switch/if chains | Medium |
   | **Introduce parameter object** | Function with 4+ parameters | Low |
   | **Replace magic values with constants** | Unexplained literals | Very Low |
   | **Simplify conditional** | Complex boolean expressions | Low |
   | **Pull up / Push down** | Inheritance hierarchy adjustment | Medium |

8. **Order the steps** from lowest risk to highest. Rename before extract. Extract before move.

### Phase 3: Execution (Step by Step)

9. **For each refactoring step**:

   a. **Announce the step**: "Step N: [move type] -- [description]"

   b. **Read the current state** of affected files

   c. **Apply the change** using Edit tool

   d. **Verify**: Run tests. If tests pass, proceed. If tests fail:
      - Is it a test that needs updating (testing implementation, not behavior)?
      - Or did we accidentally change behavior? If so, revert and reconsider.

   e. **Checkpoint**: The code should be in a working state after every step. If interrupted here, the refactoring is partially complete but the code works.

10. **Do NOT combine steps** -- Even if two changes seem related, apply them separately and verify between them. This is the discipline that keeps refactoring safe.

### Phase 4: Verification and Report

11. **Run the full test suite** after all steps are complete.

12. **Compare before/after** -- The external behavior should be identical. Internal structure should match the refactoring goal.

13. **Produce the refactoring report** using the template below.

## Refactoring Report Template

```markdown
# Refactoring Report

## Target
[What was refactored]

## Goal
[What the refactoring aimed to achieve]

## Before/After Summary
| Metric | Before | After |
|--------|--------|-------|
| Files | [count] | [count] |
| Functions | [count] | [count] |
| Max nesting depth | [N] | [N] |
| Longest function (lines) | [N] | [N] |
| Test coverage | [%] | [%] |

## Steps Performed
1. **[Move type]**: [description] — Tests: PASS
2. **[Move type]**: [description] — Tests: PASS
3. ...

## Files Changed
- [file 1]: [what changed]
- [file 2]: [what changed]
- [new file]: [why created]

## Verification
- [ ] All existing tests pass
- [ ] No behavioral changes (same inputs → same outputs)
- [ ] New characterization tests added (if needed)
- [ ] Code matches refactoring goal

## Remaining Opportunities
- [Further refactoring that could be done but was out of scope]
```

## Usage

### Basic refactoring
```
/refactor Clean up src/lib/utils.ts -- it is 400 lines and does too many things
```

### Specific move
```
/refactor Extract the validation logic from the form component into a separate module
```

### Naming cleanup
```
/refactor Improve naming in the payment processing module -- variables like 'x', 'tmp', and 'data' need descriptive names
```

### Module restructuring
```
/refactor Split the monolithic api/route.ts into separate route handlers per resource
```

## Examples

### Example: Extract function

**Before**:
```typescript
function processOrder(order: Order) {
  // 15 lines of validation logic
  // 10 lines of discount calculation
  // 20 lines of tax calculation
  // 10 lines of shipping calculation
  // 5 lines of total assembly
}
```

**After** (4 steps):
1. Extract `validateOrder(order)` -- Tests: PASS
2. Extract `calculateDiscount(order)` -- Tests: PASS
3. Extract `calculateTax(order, subtotal)` -- Tests: PASS
4. Extract `calculateShipping(order)` -- Tests: PASS

```typescript
function processOrder(order: Order) {
  validateOrder(order);
  const discount = calculateDiscount(order);
  const tax = calculateTax(order, order.subtotal - discount);
  const shipping = calculateShipping(order);
  return { ...order, discount, tax, shipping, total: order.subtotal - discount + tax + shipping };
}
```

### Example: Replace magic values

**Step 1**: Extract constants
```typescript
// Before
if (retries > 3) { setTimeout(fn, 5000); }

// After
const MAX_RETRIES = 3;
const RETRY_DELAY_MS = 5000;
if (retries > MAX_RETRIES) { setTimeout(fn, RETRY_DELAY_MS); }
```

## Guidelines

- **Never refactor and change behavior in the same step** -- These are fundamentally different activities. Do them separately.
- **Tests first** -- If there are no tests, write characterization tests before touching the code.
- **Small steps always** -- The smaller the step, the easier it is to verify and the harder it is to introduce bugs.
- **One refactoring type per step** -- Do not rename and extract in the same step.
- **Preserve the public API** -- Internal changes only. If the API needs to change, that is a different task.
- **Leave the code better than you found it** -- But do not boil the ocean. Fix what was asked, note what else could be improved.
- **Refactoring is not rewriting** -- If the code needs to be completely replaced, that is a different task with different risks.
- **Know when to stop** -- Refactoring has diminishing returns. Stop when the code is clear enough for the next developer to work with.
