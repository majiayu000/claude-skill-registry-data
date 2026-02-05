---
name: tdd-failure-recovery
description: Guide experienced developers through TDD failure scenarios and recovery procedures when tests behave unexpectedly
license: Complete terms in LICENSE.txt
---

# TDD Failure Recovery
**Version:** {{VERSION}}

## When to Use

- RED phase test passes unexpectedly (should fail)
- GREEN phase test still fails (should pass)
- REFACTOR phase breaks tests (should stay green)
- Tests behave unpredictably or inconsistently

## Scenario 1: RED Phase Test Passes Unexpectedly

**Possible causes:**
1. Feature already exists
2. Test is too permissive
3. Test setup incorrect

**Recovery:**
1. Add intentional failure to verify test can fail
2. Check for existing implementation
3. Review test logic
4. Revise test and verify it fails
5. Resume TDD cycle

## Scenario 2: GREEN Phase Test Still Fails

**Possible causes:**
1. Implementation incomplete
2. Implementation has bugs
3. Test expectations misunderstood

**Recovery:**
1. Read failure message carefully
2. Verify implementation code
3. Check test requirements
4. Revise implementation
5. Run full test suite
6. Resume TDD cycle

## Scenario 3: REFACTOR Phase Breaks Tests

**Possible causes:**
1. Behavioral change introduced
2. Breaking change in API
3. Incomplete refactoring
4. Test dependency on implementation

**Recovery:**
1. **IMMEDIATE ROLLBACK**
2. Analyze what broke
3. Decide: Skip, smaller refactoring, or fix test

**Critical principle:**
```
TESTS MUST STAY GREEN
If refactoring breaks tests -> ROLLBACK
Do not proceed with broken tests
```

## Scenario 4: Rollback Procedure

1. Identify changes to undo
2. Restore previous code version
3. Verify file state matches pre-change
4. Run full test suite
5. Verify all tests GREEN

## Scenario 5: Inconsistent Test Results

**Possible causes:**
1. Test order dependency
2. Timing issues
3. External dependencies
4. Random data in tests

**Recovery:**
1. Run failing test alone
2. Check test isolation
3. Fix with proper setup/teardown
4. Verify consistency

## Diagnostic Flowchart

```
Test failed unexpectedly -> What phase?

RED: Should fail but passes -> Test invalid, revise test
GREEN: Should pass but fails -> Implementation incomplete, revise impl
REFACTOR: Should stay green but fails -> ROLLBACK immediately
```

## Prevention Strategies

1. **Verify Each Phase** - Never assume, always run tests
2. **Clear Communication** - Report exact results
3. **Maintain Green State** - Tests green except during RED phase

## Common Recovery Patterns

| Pattern | Situation | Action |
|---------|-----------|--------|
| Reset | Confused state | Rollback to last green |
| Minimal Fix | Small issue | Targeted correction |
| Skip | Risk > reward | Defer to later |
| Divide and Conquer | Large change broke | Break into smaller changes |

## Resources

- `resources/failure-diagnostic-flowchart.md`
- `resources/recovery-procedures.md`
- `resources/test-isolation-guide.md`

---

**End of TDD Failure Recovery Skill**
