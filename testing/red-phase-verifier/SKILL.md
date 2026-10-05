---
name: red-phase-verifier
description: This skill should be used when the user asks to "write tests first", "run TDD", "verify red phase", "check failing tests", or when practicing test-driven development. Ensures tests fail before implementation.
---

# Red Phase Verifier

Ensures tests are written BEFORE implementation and fail initially.

## Purpose

In TDD:
1. **RED**: Write failing tests
2. **GREEN**: Implement to pass
3. **REFACTOR**: Improve while green

This skill enforces Step 1.

## Activation Triggers

This skill activates when:
- Running /dev-loop command
- Creating test files before implementation
- Mentioning "write tests first"

## Verification Process

### Step 1: Check Implementation Exists

```python
# If implementing UserService.create_user:
# Check if method exists and has logic

import inspect
from app.services import UserService

method = getattr(UserService, 'create_user', None)
if method:
    source = inspect.getsource(method)
    if 'pass' not in source and 'raise NotImplementedError' not in source:
        # Implementation exists!
        WARN: "Implementation found before tests"
```

### Step 2: Run Tests

```bash
pytest tests/test_new_feature.py -v --tb=short
```

### Step 3: Verify Failures

Expected output:
```
FAILED tests/test_new_feature.py::test_create - AssertionError
FAILED tests/test_new_feature.py::test_validate - AttributeError
```

### Step 4: Report

```
RED PHASE VERIFICATION

Tests written: 5
Tests failing: 5

Red phase confirmed!
Implementation may now proceed.
```

## Warning Cases

### Case 1: Tests Pass Before Implementation

```
WARNING: Tests passed before implementation!

Failing tests: 0/5

This indicates:
1. Tests don't test new functionality
2. Tests have trivial assertions
3. Implementation already exists

Action: Regenerate stricter tests
```

### Case 2: Partial Failures

```
PARTIAL RED PHASE

Tests failing: 3/5
Tests passing: 2/5

Passing tests may be:
1. Testing existing functionality (OK)
2. Trivial assertions (NOT OK)

Review passing tests:
- test_helper_exists: assert helper <- TRIVIAL
- test_constant: assert X == X <- TRIVIAL

Action: Strengthen or remove trivial tests
```

### Case 3: Wrong Failure Type

```
UNEXPECTED FAILURE TYPE

test_create_user: SyntaxError in test file

Tests should fail due to:
- AssertionError (expected behavior not met)
- AttributeError (method doesn't exist yet)
- NotImplementedError (placeholder)

NOT due to:
- SyntaxError (test file broken)
- ImportError (missing dependency)
- TypeError (wrong arguments)

Action: Fix test file syntax
```

## Enforcement

When red phase not verified:

```
CANNOT PROCEED TO GREEN PHASE

Red phase requirements not met:
- 2 tests passed before implementation
- 1 test has syntax error

Fix issues, then run verification again.
```

## Expected Failure Types

### Good Failures (Proceed)

- `AssertionError` - Assertion failed (expected)
- `AttributeError` - Method/attribute doesn't exist yet
- `NotImplementedError` - Placeholder implementation
- `ModuleNotFoundError` - Module not created yet

### Bad Failures (Fix First)

- `SyntaxError` - Test code is broken
- `IndentationError` - Test code formatting issue
- `NameError` - Undefined variable in test
- `TypeError` - Wrong arguments in test setup

## Dev Loop Integration

When integrated with /dev-loop:

1. Tests written -> Run red phase verifier
2. If all fail correctly -> Proceed to implementation
3. If some pass -> Warn and suggest fixes
4. If wrong failures -> Block until fixed

```
TDD LOOP: RED PHASE

Running red phase verification...

test_create_user: FAILED (AttributeError)
test_validate_email: FAILED (AssertionError)
test_duplicate_email: FAILED (AssertionError)
test_get_user: FAILED (NotImplementedError)
test_list_users: FAILED (NotImplementedError)

Red phase: 5/5 tests failing correctly

Proceeding to GREEN phase...
```
