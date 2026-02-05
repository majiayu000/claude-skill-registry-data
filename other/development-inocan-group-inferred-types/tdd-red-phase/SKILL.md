---
name: tdd-red-phase
description: Guide experienced developers through RED phase of TDD cycle - writing failing tests and verifying expected failures
license: Complete terms in LICENSE.txt
---

# TDD RED Phase
**Version:** 0.19.0
**Source:** Skills/tdd-red-phase/SKILL.md

Guide through RED phase: writing failing tests and verifying expected failures.

## When to Use
- Starting new feature implementation
- User issues "Start-Story [ID]" (IDPF-Agile)
- Beginning new TDD iteration

## Objective
**Write a test that fails for the right reason.**

**Correct failure:** Feature doesn't exist, behavior not implemented, failure message clear
**Incorrect failure:** Syntax error, missing imports, test passes unexpectedly

## Workflow

**Step 1: Identify Testable Behavior**
One test per behavior, one behavior per test.
```
Good: "GET /users returns 200 status"
Bad: "User management works" (too broad)
```

**Step 2: Write Failing Test (Single Code Block)**
```
TASK: [Description]
STEP 1: Create/open test file
STEP 2: Add imports
STEP 3: Write complete test (AAA: Arrange-Act-Assert)
STEP 4: Save file
STEP 5: Run test command
STEP 6: Verify test FAILS with expected message
STEP 7: Report: Did test fail as expected?
```

**Step 3: Execute and Verify**
- [ ] Test executed without syntax errors
- [ ] Test failed (not passed)
- [ ] Failure message indicates missing implementation

**Step 4: Analyze**
- Fails as expected → Proceed autonomously to GREEN phase
- Passes unexpectedly → Revise test
- Errors instead of fails → Fix test code

## Best Practices
- Write minimal tests (single assertion)
- Clear test names: `test_[feature]_[scenario]_[expected_result]`
- Descriptive assertions with helpful failure messages

## Anti-Patterns
- Writing implementation first
- Skipping failure verification
- Tolerating test errors

## Checklist
- [ ] Test complete and syntactically correct
- [ ] Test FAILS (not passes, not errors)
- [ ] Failure message clearly indicates missing implementation
- [ ] Ready to proceed to GREEN phase

---

**End of TDD RED Phase Skill**
