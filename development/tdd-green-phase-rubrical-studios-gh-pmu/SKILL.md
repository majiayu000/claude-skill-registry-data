---
name: tdd-green-phase
description: Guide experienced developers through GREEN phase of TDD cycle - writing minimal implementation to pass failing tests
license: Complete terms in LICENSE.txt
---

# TDD GREEN Phase
**Version:** 0.19.0
**Source:** Skills/tdd-green-phase/SKILL.md

Guide through GREEN phase: implementing minimum code to make failing test pass.

## When to Use
- RED phase test verified as failing
- Proceeding autonomously after RED phase
- Moving from RED to GREEN in TDD cycle

## Objective
**Write the minimum code to make the test pass.**

**Correct:** Implements exactly what test requires, simplest solution
**Incorrect:** Over-engineers, adds untested features, premature optimization

## Workflow

**Step 1: Understand Test Requirements**
- What behavior is expected?
- What inputs/outputs?
- What edge cases covered?

**Step 2: Plan Minimal Implementation**
Avoid: Features not in test, abstractions not needed, premature optimization

**Step 3: Implement (Single Code Block)**
```
TASK: [Description]
STEP 1: Open implementation file
STEP 2: Navigate to location
STEP 3: Add/modify implementation code
STEP 4: Context about choices
STEP 5: Save file
STEP 6: Run test command
STEP 7: Verify test PASSES
STEP 8: Report: Did test pass?
```

**Step 4: Verify Success**
- [ ] Test executed without errors
- [ ] Test passed (green)
- [ ] No other tests broke
- [ ] Implementation is minimal

**Step 5: Analyze**
- Passes → Proceed autonomously to REFACTOR phase
- Still fails → Revise implementation
- Other tests fail → Fix regressions first

## Principles
1. **YAGNI:** Implement only what test requires
2. **Simplest Thing:** Hard-coded values acceptable if test passes
3. **Let Tests Drive Design:** Test tells you the interface
4. **Hard-Code First:** Generalize when more tests require it

## Implementation Strategies
- **Fake It:** Return expected value (temporary)
- **Obvious Implementation:** Straightforward solution
- **Triangulation:** Multiple tests force generalization

## Anti-Patterns
- Feature creep (adding untested features)
- Optimization before profiling
- Copy-paste without understanding

## Checklist
- [ ] Target test now PASSES
- [ ] Implementation is minimal
- [ ] No regressions (full suite green)
- [ ] Ready to proceed to REFACTOR phase

---

**End of TDD GREEN Phase Skill**
