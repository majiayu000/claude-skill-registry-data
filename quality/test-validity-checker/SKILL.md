---
name: test-validity-checker
description: This skill should be used when the user asks to "check tests", "validate tests", "review test quality", "verify test coverage", or when writing test files or running pytest. Ensures tests are meaningful.
---

# Test Validity Checker

Auto-validates that tests are meaningful and catch real bugs.

## Activation Triggers

This skill activates when:
- Writing test files
- Before pytest execution
- When test coverage is checked
- When dev loop is running

## Validity Checks

### Check 1: Empty Test Detection

```python
# INVALID - Empty body
def test_user():
    pass

# INVALID - Only setup, no assertions
def test_create():
    user = create_user()
    # No assertions!

# VALID
def test_user_creation():
    user = create_user()
    assert user.id is not None
    assert user.is_active
```

**Action**: Flag empty tests, require assertions

### Check 2: Trivial Assertion Detection

```python
# INVALID - Always passes
def test_always_passes():
    assert True

def test_truthy():
    user = create_user()
    assert user  # Just checks existence

# INVALID - Testing constants
def test_constant():
    assert 1 + 1 == 2

# VALID - Tests actual behavior
def test_user_email_lowercase():
    user = create_user(email='TEST@Example.COM')
    assert user.email == 'test@example.com'
```

**Action**: Require value comparisons, not just truthiness

### Check 3: Assertion Count

```python
# WEAK - Only 1 assertion
def test_single_assertion():
    response = client.get('/api/users/')
    assert response.status_code == 200

# STRONG - Multiple assertions
def test_list_users():
    response = client.get('/api/users/')
    assert response.status_code == 200
    assert 'results' in response.data
    assert len(response.data['results']) > 0
    assert 'email' in response.data['results'][0]
```

**Minimum**: 2 meaningful assertions per test

### Check 4: Edge Case Coverage

For each function under test, require:

- Happy path (valid input -> expected output)
- Invalid input (validation error)
- Boundary conditions (min, max, empty)
- Error handling (exceptions caught)

```python
# Complete test suite example
class TestUserService:
    # Happy path
    def test_create_user_success(self):
        ...

    # Invalid input
    def test_create_user_invalid_email(self):
        with pytest.raises(ValidationError):
            ...

    # Boundary
    def test_create_user_max_length_name(self):
        user = create_user(name='x' * 255)  # Max length
        ...

    # Error handling
    def test_create_user_database_error(self, mocker):
        mocker.patch('app.models.User.save', side_effect=DatabaseError)
        with pytest.raises(ServiceError):
            ...
```

### Check 5: Test Independence

```python
# INVALID - Shared state
shared_user = None

def test_create():
    global shared_user
    shared_user = create_user()  # Modifies global

def test_read():
    assert shared_user.email  # Depends on previous test

# VALID - Independent tests
def test_create(user_factory):
    user = user_factory()
    assert user.id

def test_read(user_factory):
    user = user_factory()
    assert user.email
```

**Action**: Each test must be runnable in isolation

### Check 6: No Mocking Internals

```python
# INVALID - Testing implementation
def test_service_calls_model(self, mocker):
    mock_create = mocker.patch('User.objects.create')
    service.create_user(data)
    mock_create.assert_called_once()  # Tests HOW, not WHAT

# VALID - Testing behavior
def test_service_creates_user(self):
    user = service.create_user(data)
    assert User.objects.filter(id=user.id).exists()  # Tests WHAT
```

## Validation Report

When checking tests, output:

```
TEST VALIDITY REPORT

File: tests/test_user_service.py

 test_create_user_success
   - Assertions: 4
   - Tests behavior: Yes
   - Independent: Yes

 test_create_user_validation
   - Assertions: 1 (minimum 2)
   - Suggestion: Add assertion for error message

 test_trivial
   - Issue: assert True (trivial)
   - Action: Remove or rewrite

Summary:
- Valid: 8/10
- Warnings: 1
- Invalid: 1

Recommendation: Fix 2 issues before continuing
```

## Auto-Fix Actions

When issues detected:

1. **Empty test** -> Generate test body
2. **Trivial assertion** -> Suggest meaningful assertion
3. **Low assertion count** -> Add more assertions
4. **Missing edge cases** -> Generate edge case tests
5. **Shared state** -> Refactor to fixtures
