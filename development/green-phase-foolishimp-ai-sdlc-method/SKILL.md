---
name: green-phase
description: Implement minimal code to make failing tests pass (GREEN phase of TDD). Write just enough code to pass tests, no more. Use after red-phase when tests are failing.
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob]
---

# green-phase

**Skill Type**: Actuator (TDD Workflow)
**Purpose**: Write minimal code to make failing tests pass (GREEN phase)
**Prerequisites**:
- Tests exist and are FAILING (from red-phase)
- Requirement key (REQ-*) with details

---

## Agent Instructions

You are in the **GREEN** phase of TDD (RED → GREEN → REFACTOR).

Your goal is to **write MINIMAL code** to make the failing tests pass.

**Key principle**: Write the **simplest code that works**. Do NOT over-engineer. Refactoring comes later.

---

## Workflow

### Step 1: Review Failing Tests

**Read the test file** to understand:
- What functionality is being tested?
- What are the expected inputs and outputs?
- What business rules must be enforced?

**Example**:
```python
# tests/auth/test_login.py shows we need:
- login(email: str, password: str) -> LoginResult
- LoginResult with fields: success, user, error
- Email validation (BR-001)
- Password length validation (BR-002)
- Account lockout logic (BR-003)
```

---

### Step 2: Determine Implementation File Location

**Follow project conventions**:

**Python**:
```
tests/auth/test_login.py  → src/auth/login.py
tests/services/test_payment.py → src/services/payment.py
```

**TypeScript**:
```
src/auth/login.test.ts    → src/auth/login.ts
src/services/payment.test.ts → src/services/payment.ts
```

**Java**:
```
src/test/java/auth/LoginTest.java → src/main/java/auth/Login.java
```

---

### Step 3: Implement Minimal Code

**Write the simplest code that makes tests pass**:

```python
# src/auth/login.py

# Implements: <REQ-ID>
# Business Rules: BR-001, BR-002, BR-003

import re
from dataclasses import dataclass
from typing import Optional
from datetime import datetime, timedelta

@dataclass
class LoginResult:
    success: bool
    user: Optional['User'] = None
    error: Optional[str] = None

class User:
    def __init__(self, email: str, password_hash: str):
        self.email = email
        self.password_hash = password_hash
        self.failed_attempts = 0
        self.locked_until: Optional[datetime] = None

    def check_password(self, password: str) -> bool:
        # Simplified: In real code, use bcrypt
        return self.password_hash == hash_password(password)

# Implements: <REQ-ID>
def login(email: str, password: str) -> LoginResult:
    # Implements: BR-001 (email validation)
    if not validate_email(email):
        return LoginResult(success=False, error="Invalid email format")

    # Implements: BR-002 (password minimum length)
    if len(password) < 12:
        return LoginResult(success=False, error="Password must be at least 12 characters")

    # Get user from database (simplified)
    user = get_user_by_email(email)
    if not user:
        return LoginResult(success=False, error="User not found")

    # Implements: BR-003 (account lockout)
    if user.locked_until and datetime.now() < user.locked_until:
        return LoginResult(success=False, error="Account locked. Try again in 15 minutes")

    # Check password
    if not user.check_password(password):
        user.failed_attempts += 1

        # Implements: BR-003 (lock after 3 attempts)
        if user.failed_attempts >= 3:
            user.locked_until = datetime.now() + timedelta(minutes=15)

        return LoginResult(success=False, error="Invalid password")

    # Success - reset failed attempts
    user.failed_attempts = 0
    user.locked_until = None

    return LoginResult(success=True, user=user)

# Implements: BR-001 (email validation)
def validate_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def hash_password(password: str) -> str:
    # Simplified: In real code, use bcrypt
    return str(hash(password))

def get_user_by_email(email: str) -> Optional[User]:
    # Simplified: In real code, query database
    # For now, return mock user for testing
    return User(email, hash_password("SecurePass123!"))
```

**Key implementation principles**:
- ✅ Tag code with REQ-* keys in comments
- ✅ Tag business rule implementations with BR-* keys
- ✅ Write just enough code to pass tests (no gold-plating)
- ✅ Use clear, descriptive names
- ✅ Keep functions focused (single responsibility)
- ✅ Don't worry about perfect code (refactoring comes next)

---

### Step 4: Run Tests (Expect SUCCESS)

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
tests/auth/test_login.py::test_login_with_valid_credentials PASSED ✓
tests/auth/test_login.py::test_login_fails_with_invalid_email PASSED ✓
tests/auth/test_login.py::test_login_fails_with_short_password PASSED ✓
tests/auth/test_login.py::test_account_locked_after_3_failed_attempts PASSED ✓

4 tests passed in 0.12s
```

**✅ All tests PASSING!** This is what we want in GREEN phase.

**⚠️ If tests still FAIL**: Fix implementation and retry until all tests pass.

---

### Step 5: Verify Test Coverage

**Check coverage**:

```bash
# Python
pytest --cov=src/auth tests/auth/test_login.py --cov-report=term-missing

# TypeScript
npm test -- --coverage

# Java
mvn test jacoco:report
```

**Expected**: Coverage should be high (aim for 80%+ overall, 100% for critical paths).

---

### Step 6: Commit Implementation (GREEN Commit)

**Create commit with implementation**:

```bash
git add src/auth/login.py
git commit -m "GREEN: Implement <REQ-ID>

Implement user login functionality with email/password.

Implements:
- <REQ-ID>: User login
- BR-001: Email validation (regex pattern)
- BR-002: Password minimum 12 characters
- BR-003: Account lockout after 3 failed attempts (15min)

Tests: 4 tests passing ✓
Coverage: 95%
"
```

**Commit message format**:
- Prefix: `GREEN:`
- Brief description
- List of REQ-* and BR-* implemented
- Test status (all passing)

---

## Output Format

When you complete the GREEN phase, show:

```
[GREEN Phase - <REQ-ID>]

Implementation: src/auth/login.py

Code Created:
  ✓ LoginResult dataclass
  ✓ User class
  ✓ login() function (<REQ-ID>)
  ✓ validate_email() function (BR-001)
  ✓ hash_password() helper
  ✓ get_user_by_email() helper

Business Rules Implemented:
  ✓ BR-001: Email validation (regex)
  ✓ BR-002: Password minimum 12 characters
  ✓ BR-003: Account lockout after 3 attempts

Running tests...
  tests/auth/test_login.py::test_login_with_valid_credentials PASSED ✓
  tests/auth/test_login.py::test_login_fails_with_invalid_email PASSED ✓
  tests/auth/test_login.py::test_login_fails_with_short_password PASSED ✓
  tests/auth/test_login.py::test_account_locked_after_3_failed_attempts PASSED ✓

Result: 4/4 tests PASSING ✓ (GREEN phase)

Coverage: 95% (38/40 lines covered)

Commit: GREEN: Implement <REQ-ID>

✅ GREEN Phase Complete!
   Next: Invoke refactor-phase skill to improve code quality
```

---

## Prerequisites Check

Before invoking this skill, ensure:
1. Tests exist and are FAILING (from red-phase)
2. Requirement details available (what to implement)

If prerequisites not met:
- No tests → Invoke `red-phase` skill first
- Tests already passing → Already implemented, skip to refactor-phase

---

## Next Steps

After GREEN phase completes:
1. **Do NOT refactor yet** (tests must pass first)
2. Invoke `refactor-phase` skill to improve code quality and eliminate tech debt
3. Tests should STILL PASS after refactoring

---

## Implementation Strategies

### Strategy 1: Simplest Thing That Works

```python
# First implementation (naive, but works)
def login(email: str, password: str) -> LoginResult:
    if email == "user@example.com" and password == "SecurePass123!":
        return LoginResult(success=True)
    return LoginResult(success=False)
```

**Then improve** to handle more cases until all tests pass.

### Strategy 2: Test-by-Test

Implement code to pass **one test at a time**:
1. Make `test_login_with_valid_credentials` pass
2. Make `test_login_fails_with_invalid_email` pass
3. Make `test_login_fails_with_short_password` pass
4. Make `test_account_locked_after_3_failed_attempts` pass

### Strategy 3: Fake It Till You Make It

Start with **hard-coded values**, then generalize:
```python
# Step 1: Hard-coded (passes one test)
def validate_email(email: str) -> bool:
    return email == "user@example.com"

# Step 2: Generalize (passes all tests)
def validate_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@...'
    return re.match(pattern, email) is not None
```

---

## Common Pitfalls to Avoid

❌ **Over-engineering**: Don't add features not tested
❌ **Premature optimization**: Don't optimize before refactor phase
❌ **Perfect code**: Don't worry about code quality yet (refactor phase handles this)
❌ **Skipping tests**: All tests must pass before moving to refactor
❌ **Adding untested code**: Every line should be tested

✅ **Do this instead**:
- Write minimal code
- Make tests pass
- Move to refactor phase
- Improve code quality there

---

## Notes

**Why minimal implementation?**
- Prevents over-engineering (YAGNI - You Aren't Gonna Need It)
- Forces focus on requirements (only implement what's tested)
- Faster to refactor simple code
- Easier to understand

**GREEN phase mantra**: "Make it work, then make it right"
- GREEN phase = make it work
- REFACTOR phase = make it right

**Homeostasis Goal**:
```yaml
desired_state:
  tests_passing: true
  all_requirements_implemented: true
  code_coverage: >= 80%
```

**"Excellence or nothing"** 🔥
