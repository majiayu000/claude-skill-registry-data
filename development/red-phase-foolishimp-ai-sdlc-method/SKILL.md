---
name: red-phase
description: Write failing tests before implementation (RED phase of TDD). Creates test file with test functions that fail because code doesn't exist yet. Use when starting TDD workflow or adding tests for new functionality.
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob]
---

# red-phase

**Skill Type**: Actuator (TDD Workflow)
**Purpose**: Write tests that fail because the code doesn't exist yet (RED phase)
**Prerequisites**:
- Requirement key (REQ-*) with details
- No existing tests for this requirement

---

## Agent Instructions

You are in the **RED** phase of TDD (RED → GREEN → REFACTOR).

Your goal is to **write tests that FAIL** because the implementation doesn't exist yet.

---

## Workflow

### Step 1: Understand the Requirement

**Parse the requirement**:
- What functionality needs to be implemented?
- What are the business rules (BR-*)?
- What are the constraints (C-*)?
- What are the expected inputs and outputs?

**Example**:
```yaml
<REQ-ID>: User login with email and password

Business Rules:
- BR-001: Email must be valid format
- BR-002: Password minimum 12 characters
- BR-003: Max 3 login attempts, 15min lockout

Expected behavior:
- Input: email (string), password (string)
- Output: LoginResult(success: bool, user: User | None, error: str | None)
```

---

### Step 2: Design Test Cases

**Create test cases covering**:
1. **Happy path** - Valid inputs, expected success
2. **Business rules** - Each BR-* gets at least 1 test
3. **Edge cases** - Boundary conditions, null inputs, empty strings
4. **Error cases** - Invalid inputs, expected failures

**Example test cases for <REQ-ID>**:
```python
# Happy path
test_login_with_valid_credentials()

# Business rules
test_login_fails_with_invalid_email()       # BR-001
test_login_fails_with_short_password()      # BR-002
test_account_locked_after_3_failed_attempts() # BR-003

# Edge cases
test_login_with_empty_email()
test_login_with_empty_password()
test_login_with_nonexistent_user()

# Error cases
test_login_with_null_email()
test_login_with_null_password()
```

---

### Step 3: Determine Test File Location

**Follow project conventions**:

**Python**:
```
src/auth/login.py          → tests/auth/test_login.py
src/services/payment.py    → tests/services/test_payment.py
```

**TypeScript**:
```
src/auth/login.ts          → src/auth/login.test.ts
src/services/payment.ts    → src/services/payment.test.ts
```

**Java**:
```
src/main/java/auth/Login.java         → src/test/java/auth/LoginTest.java
src/main/java/services/Payment.java   → src/test/java/services/PaymentTest.java
```

**If unsure**: Check existing test files to follow project structure.

---

### Step 4: Write Test File

**Template structure**:

```python
# tests/auth/test_login.py

# Validates: <REQ-ID>
# Business Rules: BR-001, BR-002, BR-003

import pytest
from auth.login import login, LoginResult  # Will fail - doesn't exist yet

def test_login_with_valid_credentials():
    """Test successful login with valid email and password"""
    # Validates: <REQ-ID> (happy path)
    result = login("user@example.com", "SecurePass123!")
    assert result.success == True
    assert result.user is not None
    assert result.user.email == "user@example.com"

def test_login_fails_with_invalid_email():
    """Test login fails with invalid email format"""
    # Validates: BR-001 (email validation)
    result = login("invalid-email", "SecurePass123!")
    assert result.success == False
    assert result.error == "Invalid email format"

def test_login_fails_with_short_password():
    """Test login fails with password < 12 characters"""
    # Validates: BR-002 (password minimum length)
    result = login("user@example.com", "short")
    assert result.success == False
    assert result.error == "Password must be at least 12 characters"

def test_account_locked_after_3_failed_attempts():
    """Test account locks after 3 failed login attempts"""
    # Validates: BR-003 (lockout after 3 attempts)
    # Attempt 1
    login("user@example.com", "wrong_password")
    # Attempt 2
    login("user@example.com", "wrong_password")
    # Attempt 3
    login("user@example.com", "wrong_password")
    # Attempt 4 should be locked
    result = login("user@example.com", "correct_password")
    assert result.success == False
    assert result.error == "Account locked. Try again in 15 minutes"
```

**Key elements**:
- ✅ Comment at top: `# Validates: <REQ-ID>`
- ✅ List business rules: `# Business Rules: BR-001, BR-002, BR-003`
- ✅ Each test tagged with what it validates
- ✅ Clear test names (what is being tested)
- ✅ Docstrings explaining test purpose
- ✅ Assertions for expected behavior

---

### Step 5: Run Tests (Expect FAILURE)

**Run the test suite**:

```bash
# Python
pytest tests/auth/test_login.py -v

# TypeScript/JavaScript
npm test src/auth/login.test.ts

# Java
mvn test -Dtest=LoginTest
```

**Expected output**:
```
tests/auth/test_login.py::test_login_with_valid_credentials FAILED
tests/auth/test_login.py::test_login_fails_with_invalid_email FAILED
tests/auth/test_login.py::test_login_fails_with_short_password FAILED
tests/auth/test_login.py::test_account_locked_after_3_failed_attempts FAILED

ImportError: cannot import name 'login' from 'auth.login'
```

**✅ This is GOOD!** Tests fail because implementation doesn't exist yet.

**⚠️ If tests PASS**: Something is wrong - tests should fail in RED phase!

---

### Step 6: Commit Tests (RED Commit)

**Create commit with tests**:

```bash
git add tests/auth/test_login.py
git commit -m "RED: Add tests for <REQ-ID>

Write failing tests for user login functionality.

Tests cover:
- BR-001: Email validation
- BR-002: Password minimum length
- BR-003: Account lockout after 3 attempts

Tests: 4 tests (all failing as expected - RED phase)

Validates: <REQ-ID>
"
```

**Commit message format**:
- Prefix: `RED:`
- Brief description
- Details of what's tested
- REQ-* key for traceability

---

## Output Format

When you complete the RED phase, show:

```
[RED Phase - <REQ-ID>]

Requirement: User login with email and password

Test Cases Created:
  ✓ test_login_with_valid_credentials (happy path)
  ✓ test_login_fails_with_invalid_email (BR-001)
  ✓ test_login_fails_with_short_password (BR-002)
  ✓ test_account_locked_after_3_failed_attempts (BR-003)

Test File: tests/auth/test_login.py (4 tests, 87 lines)

Running tests...
  tests/auth/test_login.py::test_login_with_valid_credentials FAILED
  tests/auth/test_login.py::test_login_fails_with_invalid_email FAILED
  tests/auth/test_login.py::test_login_fails_with_short_password FAILED
  tests/auth/test_login.py::test_account_locked_after_3_failed_attempts FAILED

Result: 4 tests FAILED ✓ (expected - RED phase)

Commit: RED: Add tests for <REQ-ID>

✅ RED Phase Complete!
   Next: Invoke green-phase skill to implement functionality
```

---

## Prerequisites Check

Before invoking this skill, ensure:
1. Requirement key (REQ-*) exists
2. Requirement details available (what to implement)
3. No existing tests for this requirement (or you're adding to them)

If prerequisites not met:
- No REQ-* → Invoke `requirement-extraction` skill
- No requirement details → Ask user for clarification

---

## Next Steps

After RED phase completes:
1. **Do NOT implement code yet** (that's GREEN phase)
2. Invoke `green-phase` skill to implement functionality
3. Tests should PASS in GREEN phase

---

## Test Templates (by Language)

### Python (pytest)

```python
# tests/test_feature.py

# Validates: <REQ-ID>
# Business Rules: <BR-ID>, <BR-ID>

import pytest
from module import function

def test_happy_path():
    """Test successful case"""
    # Validates: <REQ-ID>
    result = function("valid_input")
    assert result == expected_output

def test_business_rule_validation():
    """Test business rule enforcement"""
    # Validates: BR-001
    with pytest.raises(ValidationError):
        function("invalid_input")
```

### TypeScript (Jest)

```typescript
// feature.test.ts

// Validates: <REQ-ID>
// Business Rules: <BR-ID>, <BR-ID>

import { function } from './module';

describe('Feature', () => {
  test('happy path - successful case', () => {
    // Validates: <REQ-ID>
    const result = function('valid_input');
    expect(result).toBe(expected_output);
  });

  test('business rule - validation error', () => {
    // Validates: BR-001
    expect(() => function('invalid_input')).toThrow(ValidationError);
  });
});
```

### Java (JUnit)

```java
// FeatureTest.java

// Validates: <REQ-ID>
// Business Rules: <BR-ID>, <BR-ID>

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class FeatureTest {
    @Test
    void testHappyPath() {
        // Validates: <REQ-ID>
        var result = Feature.function("valid_input");
        assertEquals(expected_output, result);
    }

    @Test
    void testBusinessRuleValidation() {
        // Validates: BR-001
        assertThrows(ValidationException.class, () -> {
            Feature.function("invalid_input");
        });
    }
}
```

---

## Notes

**Why write tests first?**
- Tests = executable specification of requirements
- Failing tests prove tests can detect bugs (no false positives)
- Forces thinking about API design before implementation
- Ensures testability (if you can't write the test, the design is wrong)

**Common mistakes to avoid**:
- ❌ Writing tests that pass immediately (not testing anything)
- ❌ Writing implementation before tests (not TDD)
- ❌ Skipping edge cases or error cases
- ❌ Not tagging tests with REQ-* keys (loses traceability)

**Homeostasis Goal**:
```yaml
desired_state:
  tests_written_first: true
  tests_failing: true  # In RED phase, failure is success!
  requirement_coverage: 100%
```

**"Excellence or nothing"** 🔥
