---
name: tdd-red-phase
description: Guide experienced developers through RED phase of TDD cycle - writing failing tests and verifying expected failures
license: Complete terms in LICENSE.txt
---

# TDD RED Phase
**Version:** {{VERSION}}

## When to Use

- Starting implementation of a new feature or behavior
- User issues "Start-Story [ID]" command in IDPF-Agile framework
- Beginning a new TDD iteration

## RED Phase Objective

**Write a test that fails for the right reason.**

### Right Reason
- Test fails because feature doesn't exist yet
- Test fails because behavior not implemented
- Failure message clearly indicates what's missing

### Wrong Reason
- Test fails due to syntax error
- Test fails due to missing imports
- Test passes unexpectedly

## Workflow

### Step 1: Identify Testable Behavior

**Good:**
- "Function returns sum of two numbers"
- "GET /users returns 200 status"
- "Invalid email shows validation error"

**Poor:**
- "User management works" (too broad)
- "Fix the bug" (not a behavior)

### Step 2: Write the Failing Test

**Test structure:**
```
1. ARRANGE: Set up test data and preconditions
2. ACT: Execute the behavior being tested
3. ASSERT: Verify the expected outcome
```

Provide single code block:
```
TASK: [Brief description]

STEP 1: [Create or open test file]
STEP 2: [Add necessary imports]
STEP 3: [Write complete test function]
STEP 4: [Save file]
STEP 5: [Run test command]
STEP 6: [Verify test FAILS with expected message]
STEP 7: [Report back: Did test fail as expected?]
```

### Step 3: Execute and Verify Failure

**Checklist:**
- [ ] Test executed without syntax errors
- [ ] Test failed (not passed)
- [ ] Failure message indicates missing implementation

### Step 4: Analyze and Proceed

**If fails as expected:** Proceed to GREEN phase
**If passes unexpectedly:** Revise test
**If errors instead of fails:** Fix test code

## Best Practices

### Write Minimal Tests
- Test verifies one specific behavior
- Uses simplest possible test data
- Single assertion (or closely related)

### Use Clear Test Names
```
test_[feature]_[scenario]_[expected_result]

Examples:
- test_add_function_with_positive_numbers_returns_sum
- test_get_users_when_authenticated_returns_200
```

## Common Mistakes

1. **Test Passes Immediately** - Feature already exists or test wrong
2. **Test Has Syntax Errors** - Fix before proceeding
3. **Test Too Broad** - Split into multiple tests
4. **Unclear Failure Message** - Add descriptive assertions

## Anti-Patterns

1. **Writing Implementation First** - Test first, then code
2. **Skipping Failure Verification** - Always run and verify
3. **Tolerating Test Errors** - Fix so test fails cleanly

## Checklist Before GREEN Phase

- [ ] Test code is complete and syntactically correct
- [ ] Test executes without errors
- [ ] Test FAILS (does not pass)
- [ ] Failure message indicates missing implementation
- [ ] Test is focused on single behavior

## Resources

- `resources/red-phase-checklist.md`
- `resources/test-structure-patterns.md`
- `resources/failure-verification-guide.md`

---

**End of TDD RED Phase Skill**
