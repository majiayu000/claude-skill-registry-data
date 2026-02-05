---
name: tdd-green-phase
description: Guide experienced developers through GREEN phase of TDD cycle - writing minimal implementation to pass failing tests
license: Complete terms in LICENSE.txt
---

# TDD GREEN Phase
**Version:** {{VERSION}}

## When to Use

- RED phase test has been verified as failing
- Proceeding autonomously from RED phase
- Implementing feature to pass test

## GREEN Phase Objective

**Write the minimum code to make the test pass.**

## Workflow

### Step 1: Understand Test Requirements

- What behavior is expected?
- What inputs does test provide?
- What output/result does test expect?

### Step 2: Plan Minimal Implementation

**Include:**
- Minimum logic needed
- Required data structures
- Expected return values

**Avoid:**
- Features not in test
- Abstractions not yet needed
- Premature optimization

### Step 3: Implement to Pass Test

Provide single code block:
```
TASK: [Brief description]

STEP 1: [Open implementation file]
STEP 2: [Navigate to location]
STEP 3: [Add implementation code]
STEP 4: [Explanation]
STEP 5: [Save file]
STEP 6: [Run test command]
STEP 7: [Verify test PASSES]
STEP 8: [Report back: Did test pass?]
```

### Step 4: Verify and Proceed

**If test passes:** Proceed to REFACTOR phase
**If test fails:** Revise implementation, repeat
**If other tests fail:** Fix regressions first

## Best Practices

### YAGNI (You Aren't Gonna Need It)

**Good:** Implements exactly what test requires
**Poor:** Implements untested features "just in case"

### Simplest Thing That Works

```
Test: Function should return sum of two numbers

WRONG: Generic calculation engine with plugins
RIGHT: Function returns a + b
```

### Hard-Code First, Generalize Later

```
Test expects result: 5
Implementation: return 5

Next test expects different result
-> Now implement real logic
```

## Common Mistakes

1. **Over-Implementation** - Adding features not required
2. **Premature Abstraction** - Creating abstractions before needed
3. **Ignoring Test Failure Details** - Not reading expectations
4. **Breaking Existing Tests** - Run full suite

## Implementation Strategies

| Strategy | When | Example |
|----------|------|---------|
| Fake It | Simple test | `return 5` |
| Obvious | Clear solution | `return a + b` |
| Triangulation | Unsure how to generalize | Multiple tests force generalization |

## Checklist Before REFACTOR Phase

- [ ] Target test PASSES
- [ ] Implementation is minimal
- [ ] No existing tests broke
- [ ] Code is understandable
- [ ] No untested features added

## Resources

- `resources/green-phase-checklist.md`
- `resources/minimal-implementation-guide.md`
- `resources/triangulation-examples.md`

---

**End of TDD GREEN Phase Skill**
