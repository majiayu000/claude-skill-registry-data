---
name: tdd-failure-recovery
description: Guide experienced developers through TDD failure scenarios and recovery procedures when tests behave unexpectedly
license: Complete terms in LICENSE.txt
---

# TDD Failure Recovery
**Version:** 0.19.0

Guide through diagnosing and recovering from unexpected test behaviors.

## When to Use
- RED phase test passes unexpectedly
- GREEN phase test still fails
- REFACTOR phase breaks tests
- Need to rollback to previous working state

## Failure Scenarios

### Scenario 1: RED Phase Test Passes
**Expected:** Fail | **Actual:** Passes

**Causes:** Feature exists, test too permissive, test setup incorrect

**Recovery:**
1. Verify test can fail (add intentional failure)
2. Check for existing implementation (delete if found)
3. Review test logic (correct assertion?)
4. Revise test → Re-run → Verify fails
5. Proceed autonomously to GREEN phase

### Scenario 2: GREEN Phase Test Fails
**Expected:** Pass | **Actual:** Fails

**Causes:** Implementation incomplete, bugs, misunderstood requirements

**Recovery:**
1. Read failure message carefully
2. Verify implementation matches requirements
3. Fix syntax/logic errors
4. Revise implementation → Re-run
5. Run full suite (no regressions)
6. Proceed autonomously to REFACTOR phase

### Scenario 3: REFACTOR Breaks Tests
**Expected:** Stay green | **Actual:** Fails

**Recovery:**
1. **IMMEDIATE ROLLBACK** - Return to last green
2. Verify tests green again
3. Options:
   - Skip refactoring
   - Try smaller refactoring
   - Fix brittle test (if over-coupled)
4. Continue with next behavior or Story-Complete

### Scenario 4: Rollback Required
When rollback to previous working state is needed.

**Procedure (Single Code Block):**
```
TASK: Rollback to previous working state
STEP 1: Identify changes to undo
STEP 2: Restore previous code
STEP 3: Verify file state matches pre-change
STEP 4: Run full test suite
STEP 5: Verify all tests GREEN
STEP 6: Report: Tests green?
```

### Scenario 5: Inconsistent Test Results
Tests pass sometimes, fail other times

**Causes:** Order dependency, timing issues, external dependencies, random data

**Recovery:**
1. Isolate test (run alone, different order)
2. Check test isolation (proper setup/teardown)
3. Fix isolation issues (fixtures, mocks)
4. Verify consistent pass/fail

## Diagnostic Flowchart
```
Test failed unexpectedly → What phase?
├─ RED (should fail, but passes) → Test invalid → Revise test
├─ GREEN (should pass, but fails) → Impl incomplete → Revise impl
└─ REFACTOR (should stay green) → ROLLBACK → Try smaller or skip
```

## Prevention Strategies
1. **Verify Each Phase:** Always run tests, don't assume
2. **Clear Communication:** Report exact results
3. **Maintain Green State:** Tests always green except during RED

## Golden Rule
```
Tests should ALWAYS be green except during RED phase
If not green when expected → STOP and recover
```

---

**End of TDD Failure Recovery Skill**
