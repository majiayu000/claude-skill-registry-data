---
name: tdd-refactor-phase
description: Guide experienced developers through REFACTOR phase of TDD cycle - improving code quality while maintaining green tests
license: Complete terms in LICENSE.txt
---

# TDD REFACTOR Phase
**Version:** {{VERSION}}

## When to Use

- GREEN phase complete with passing test
- Proceeding autonomously from GREEN phase
- Code works but could be improved

## REFACTOR Phase Objectives

1. **Improve code quality** - Make code cleaner, more maintainable
2. **Keep tests green** - Ensure all improvements maintain functionality

### Refactoring IS
- Improving code structure without changing behavior
- Making code more readable
- Eliminating duplication
- Simplifying complex logic

### Refactoring IS NOT
- Adding new features
- Changing tested behavior
- Breaking tests to "improve" code

## Workflow

### Step 1: Analyze Refactoring Opportunities

Identify:
- Code duplication
- Long or complex functions
- Unclear variable/function names
- Complex conditional logic
- Magic numbers/strings

### Step 2: Evaluate Suggestions

**Refactor Now:**
- Clear improvement
- Low risk, high value
- Won't over-engineer

**Skip Refactoring:**
- Premature abstraction
- Risk > reward
- Code already clear enough

### Step 3: Apply Refactoring (if approved)

```
TASK: [Brief description]

STEP 1: [Open implementation file]
STEP 2: [Navigate to code]
STEP 3: [Apply refactored code]
STEP 4: [Explanation of improvement]
STEP 5: [Save file]
STEP 6: [Run full test suite]
STEP 7: [Verify ALL tests still PASS]
STEP 8: [Report back: All tests green?]
```

### Step 4: Verify Tests Remain Green

**If any test fails:**
1. Rollback immediately
2. Keep tests green
3. Try smaller refactoring

## Best Practices

### Refactor in Small Steps
```
1. Extract one variable -> Run tests
2. Rename one function -> Run tests
3. Extract one function -> Run tests
```

### One Refactoring at a Time

Focus on one improvement, then run tests.

### Golden Rule
```
Tests must ALWAYS be green after refactoring.
If refactoring breaks tests -> ROLLBACK
```

## Common Refactorings

| Refactoring | Before | After |
|-------------|--------|-------|
| Extract Variable | Expression embedded | Well-named variable |
| Extract Function | Long function | Smaller focused functions |
| Rename | Unclear names | Names express intent |
| Eliminate Duplication | Same code multiple places | Single function |
| Simplify Conditional | Nested conditions | Guard clauses |

## When to Skip Refactoring

1. **Premature Abstraction** - Only one use of code
2. **Code Already Clear** - Current code is good enough
3. **High Risk, Low Value** - Not worth risk
4. **Over-Engineering** - Adds design patterns prematurely

## Rollback Procedures

1. Rollback changes (git checkout or undo)
2. Verify tests return to green
3. Options: Try smaller, skip, or investigate

## Checklist Before Next Feature

- [ ] Code analyzed for refactoring opportunities
- [ ] Suggestions evaluated
- [ ] If refactoring applied: All tests PASS
- [ ] If skipped: Valid reason documented

## Resources

- `resources/refactor-checklist.md`
- `resources/common-refactorings.md`
- `resources/when-to-skip-refactoring.md`

---

**End of TDD REFACTOR Phase Skill**
