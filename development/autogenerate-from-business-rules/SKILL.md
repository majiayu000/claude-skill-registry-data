---
name: autogenerate-from-business-rules
description: Autogenerate production code from disambiguated business rules (BR-*). Converts BR-* specifications into validators, constants, and logic. Use when requirements have been disambiguated into BR-*, C-*, F-* format.
allowed-tools: [Read, Write, Edit, Bash]
---

# autogenerate-from-business-rules

**Skill Type**: Actuator (Code Generation)
**Purpose**: Autogenerate production code from business rules (BR-*)
**Prerequisites**:
- Requirements disambiguated into BR-*, C-*, F-* format
- Requirement key (REQ-*) available

---

## Agent Instructions

You are **autogenerating code** from **disambiguated business rules**.

Your goal is to transform **structured BR-* specifications** into **production code** with tests.

**This is NOT traditional coding** - you are translating formal specifications into executable code.

---

## Workflow

### Step 1: Parse Business Rules

**Read requirement and extract BR-* rules**:

**Example**:
```yaml
<REQ-ID>: User login with email and password

Business Rules:
- BR-001: Email validation
  - Format: regex ^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$
  - Error message: "Invalid email format"

- BR-002: Password minimum length
  - Minimum: 12 characters
  - Error message: "Password must be at least 12 characters"

- BR-003: Account lockout
  - Max attempts: 3
  - Lockout duration: 15 minutes
  - Error message: "Account locked. Try again in {remaining} minutes"

- BR-004: Email must be unique
  - Check: User.exists(email) must be false
  - Error message: "Email already registered"
```

---

### Step 2: Generate Constants from BR-*

**Extract constants** from business rules:

```python
# src/auth/constants.py
# Generated from: <REQ-ID>

# BR-001: Email validation
EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
EMAIL_VALIDATION_ERROR = "Invalid email format"

# BR-002: Password minimum length
PASSWORD_MIN_LENGTH = 12
PASSWORD_LENGTH_ERROR = "Password must be at least 12 characters"

# BR-003: Account lockout
MAX_LOGIN_ATTEMPTS = 3
LOCKOUT_DURATION_MINUTES = 15
LOCKOUT_ERROR_TEMPLATE = "Account locked. Try again in {remaining} minutes"

# BR-004: Email uniqueness
EMAIL_UNIQUE_ERROR = "Email already registered"
```

**Generated automatically from**:
- Numbers → constants (12 → PASSWORD_MIN_LENGTH)
- Strings → error messages (→ constants)
- Patterns → regex patterns

---

### Step 3: Generate Validators from BR-*

**Invoke**: `autogenerate-validators` skill (sub-skill)

**Generate validation functions**:

```python
# src/auth/validators.py
# Generated from: <REQ-ID>

import re
from typing import Optional
from .constants import (
    EMAIL_REGEX, EMAIL_VALIDATION_ERROR,
    PASSWORD_MIN_LENGTH, PASSWORD_LENGTH_ERROR
)


def validate_email(email: str) -> Optional[str]:
    """
    Validate email format.

    Generated from: BR-001 (Email validation)

    Args:
        email: Email address to validate

    Returns:
        None if valid, error message if invalid

    Examples:
        >>> validate_email("user@example.com")
        None
        >>> validate_email("invalid")
        'Invalid email format'
    """
    # Generated from: BR-001
    if not re.match(EMAIL_REGEX, email):
        return EMAIL_VALIDATION_ERROR
    return None


def validate_password_length(password: str) -> Optional[str]:
    """
    Validate password meets minimum length requirement.

    Generated from: BR-002 (Password minimum length)

    Args:
        password: Password to validate

    Returns:
        None if valid, error message if invalid

    Examples:
        >>> validate_password_length("SecurePassword123!")
        None
        >>> validate_password_length("short")
        'Password must be at least 12 characters'
    """
    # Generated from: BR-002
    if len(password) < PASSWORD_MIN_LENGTH:
        return PASSWORD_LENGTH_ERROR
    return None


def validate_email_unique(email: str) -> Optional[str]:
    """
    Validate email is not already registered.

    Generated from: BR-004 (Email uniqueness)

    Args:
        email: Email address to check

    Returns:
        None if unique, error message if already exists

    Examples:
        >>> validate_email_unique("new@example.com")
        None
        >>> validate_email_unique("existing@example.com")
        'Email already registered'
    """
    # Generated from: BR-004
    from .models import User
    if User.exists(email):
        return EMAIL_UNIQUE_ERROR
    return None
```

**Key features of generated validators**:
- ✅ Tagged with BR-* key in comments
- ✅ Comprehensive docstrings with examples
- ✅ Return `None` for valid, error message for invalid
- ✅ Type hints for clarity
- ✅ Use constants (no magic numbers/strings)

---

### Step 4: Generate Logic from BR-*

**Generate business logic functions**:

```python
# src/auth/lockout.py
# Generated from: <REQ-ID>

from datetime import datetime, timedelta
from typing import Optional
from .constants import MAX_LOGIN_ATTEMPTS, LOCKOUT_DURATION_MINUTES


class LoginAttemptTracker:
    """
    Track login attempts and manage account lockout.

    Generated from: BR-003 (Account lockout)
    """

    def __init__(self):
        self.failed_attempts = 0
        self.locked_until: Optional[datetime] = None

    def is_locked(self) -> bool:
        """
        Check if account is currently locked.

        Generated from: BR-003

        Returns:
            True if locked, False otherwise
        """
        # Generated from: BR-003
        if self.locked_until is None:
            return False
        return datetime.now() < self.locked_until

    def record_failed_attempt(self) -> bool:
        """
        Record a failed login attempt and lock if threshold reached.

        Generated from: BR-003

        Returns:
            True if account locked, False otherwise
        """
        # Generated from: BR-003
        self.failed_attempts += 1

        if self.failed_attempts >= MAX_LOGIN_ATTEMPTS:
            self.locked_until = datetime.now() + timedelta(minutes=LOCKOUT_DURATION_MINUTES)
            return True

        return False

    def reset_attempts(self) -> None:
        """Reset failed attempts after successful login"""
        # Generated from: BR-003
        self.failed_attempts = 0
        self.locked_until = None

    def get_remaining_lockout_time(self) -> Optional[int]:
        """
        Get remaining lockout time in minutes.

        Generated from: BR-003

        Returns:
            Minutes remaining if locked, None if not locked
        """
        # Generated from: BR-003
        if not self.is_locked():
            return None
        return (self.locked_until - datetime.now()).seconds // 60
```

---

### Step 5: Generate Tests for Generated Code

**Auto-generate tests** for all generated code:

```python
# tests/auth/test_validators.py
# Generated from: <REQ-ID>

import pytest
from src.auth.validators import (
    validate_email,
    validate_password_length,
    validate_email_unique
)


class TestEmailValidation:
    """Tests for BR-001: Email validation"""

    def test_valid_email(self):
        # Generated from: BR-001
        assert validate_email("user@example.com") is None

    def test_invalid_email_no_at_sign(self):
        # Generated from: BR-001
        assert validate_email("invalid") == "Invalid email format"

    def test_invalid_email_no_domain(self):
        # Generated from: BR-001
        assert validate_email("user@") == "Invalid email format"

    def test_invalid_email_no_tld(self):
        # Generated from: BR-001
        assert validate_email("user@example") == "Invalid email format"


class TestPasswordValidation:
    """Tests for BR-002: Password minimum length"""

    def test_valid_password(self):
        # Generated from: BR-002
        assert validate_password_length("SecurePassword123!") is None

    def test_password_exactly_12_chars(self):
        # Generated from: BR-002
        assert validate_password_length("12Characters") is None

    def test_password_too_short(self):
        # Generated from: BR-002
        assert validate_password_length("short") == "Password must be at least 12 characters"

    def test_password_11_chars(self):
        # Generated from: BR-002 (boundary test)
        assert validate_password_length("11Character") == "Password must be at least 12 characters"
```

---

### Step 6: Run Generated Tests

**Verify generated code works**:

```bash
pytest tests/auth/test_validators.py -v
```

**Expected**: All generated tests PASS ✓

---

### Step 7: Commit Generated Code

**Create commit**:

```bash
git add src/auth/constants.py src/auth/validators.py src/auth/lockout.py tests/auth/test_validators.py
git commit -m "GEN: Autogenerate code from BR-* for <REQ-ID>

Autogenerate production code and tests from business rules.

Generated from Business Rules:
- BR-001: Email validation → validate_email() + tests
- BR-002: Password minimum length → validate_password_length() + tests
- BR-003: Account lockout → LoginAttemptTracker class + tests
- BR-004: Email uniqueness → validate_email_unique() + tests

Files Generated:
- src/auth/constants.py (14 constants)
- src/auth/validators.py (3 validators, 87 lines)
- src/auth/lockout.py (LoginAttemptTracker, 76 lines)
- tests/auth/test_validators.py (24 tests, 142 lines)

Tests: 24 tests, all passing ✓
Coverage: 100%

Generated from: <REQ-ID> (BR-001, BR-002, BR-003, BR-004)
"
```

---

## Output Format

When you complete code generation, show:

```
[CODE GENERATION - <REQ-ID>]

Parsed Business Rules:
  ✓ BR-001: Email validation (regex pattern)
  ✓ BR-002: Password minimum length (12 chars)
  ✓ BR-003: Account lockout (3 attempts, 15min)
  ✓ BR-004: Email uniqueness check

Generated Constants:
  ✓ EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@...'
  ✓ EMAIL_VALIDATION_ERROR = "Invalid email format"
  ✓ PASSWORD_MIN_LENGTH = 12
  ✓ PASSWORD_LENGTH_ERROR = "Password must be at least 12 characters"
  ✓ MAX_LOGIN_ATTEMPTS = 3
  ✓ LOCKOUT_DURATION_MINUTES = 15
  ✓ 8 more constants...

Generated Validators:
  ✓ validate_email() from BR-001
  ✓ validate_password_length() from BR-002
  ✓ validate_email_unique() from BR-004

Generated Logic:
  ✓ LoginAttemptTracker class from BR-003
    - is_locked() method
    - record_failed_attempt() method
    - reset_attempts() method
    - get_remaining_lockout_time() method

Generated Tests:
  ✓ 24 tests for all validators and logic
  ✓ Happy path tests
  ✓ Error case tests
  ✓ Boundary tests

Files Generated:
  + src/auth/constants.py (14 constants, 28 lines)
  + src/auth/validators.py (3 validators, 87 lines)
  + src/auth/lockout.py (1 class, 76 lines)
  + tests/auth/test_validators.py (24 tests, 142 lines)

Running generated tests...
  ✓ All 24 tests PASSING

Coverage: 100%

Commit: GEN: Autogenerate code from BR-* for <REQ-ID>

✅ Code Generation Complete!
   Generated: 333 lines of production code + tests
   From: 4 business rules (BR-001, BR-002, BR-003, BR-004)
   Ratio: 1 BR → 83 lines of code (average)
```

---

## Prerequisites Check

Before invoking this skill, ensure:
1. Requirements have been disambiguated (BR-*, C-*, F-* exist)
2. Requirement key (REQ-*) available
3. Business rules are sufficiently detailed for code generation

If prerequisites not met:
- No BR-* → Invoke `disambiguate-requirements` skill (from requirements-skills plugin)
- Vague BR-* → Ask user for clarification

---

## Skills Used

This orchestrator skill invokes:
1. `autogenerate-validators` - Generate validation functions from BR-*
2. `autogenerate-constraints` - Generate constraint checks from C-*
3. `autogenerate-formulas` - Generate formula implementations from F-*

---

## Generation Patterns

### Pattern 1: Validation Rules → Validators

**Input**:
```yaml
BR-001: Email validation
  Format: regex ^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$
  Error: "Invalid email format"
```

**Generated**:
```python
EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

def validate_email(email: str) -> Optional[str]:
    if not re.match(EMAIL_REGEX, email):
        return "Invalid email format"
    return None
```

### Pattern 2: Min/Max Constraints → Validators

**Input**:
```yaml
BR-002: Password length
  Minimum: 12 characters
  Maximum: 128 characters
```

**Generated**:
```python
PASSWORD_MIN_LENGTH = 12
PASSWORD_MAX_LENGTH = 128

def validate_password_length(password: str) -> Optional[str]:
    if len(password) < PASSWORD_MIN_LENGTH:
        return f"Password must be at least {PASSWORD_MIN_LENGTH} characters"
    if len(password) > PASSWORD_MAX_LENGTH:
        return f"Password must be at most {PASSWORD_MAX_LENGTH} characters"
    return None
```

### Pattern 3: Enumerated Values → Validators

**Input**:
```yaml
BR-005: Card types
  Allowed: ["Visa", "Mastercard"]
  Error: "Card type not supported"
```

**Generated**:
```python
ALLOWED_CARD_TYPES = ["Visa", "Mastercard"]

def validate_card_type(card_type: str) -> Optional[str]:
    if card_type not in ALLOWED_CARD_TYPES:
        return "Card type not supported"
    return None
```

### Pattern 4: Rate Limits → Trackers

**Input**:
```yaml
BR-006: Rate limiting
  Max requests: 100 per hour per user
  Error: "Rate limit exceeded. Try again in {remaining} minutes"
```

**Generated**:
```python
MAX_REQUESTS_PER_HOUR = 100

class RateLimitTracker:
    def __init__(self):
        self.requests = []

    def check_rate_limit(self, user_id: str) -> Optional[str]:
        # Remove requests older than 1 hour
        cutoff = datetime.now() - timedelta(hours=1)
        self.requests = [r for r in self.requests if r.timestamp > cutoff]

        # Check if limit exceeded
        user_requests = [r for r in self.requests if r.user_id == user_id]
        if len(user_requests) >= MAX_REQUESTS_PER_HOUR:
            # Calculate remaining time
            oldest = min(r.timestamp for r in user_requests)
            remaining = 60 - (datetime.now() - oldest).seconds // 60
            return f"Rate limit exceeded. Try again in {remaining} minutes"

        return None

    def record_request(self, user_id: str) -> None:
        self.requests.append(Request(user_id, datetime.now()))
```

---

### Step 8: Generate Tests (Auto-Test Generation)

**For every generated function, generate tests**:

**Generation rule**:
- 1 happy path test (valid input)
- 1 error case test (invalid input)
- 1 boundary test (edge of valid range)
- 1 null/empty test (if applicable)

**Example**:
```python
# Auto-generated from BR-001
def test_validate_email_valid():
    assert validate_email("user@example.com") is None

def test_validate_email_invalid():
    assert validate_email("invalid") == "Invalid email format"

def test_validate_email_empty():
    assert validate_email("") == "Invalid email format"

def test_validate_email_null():
    with pytest.raises(TypeError):
        validate_email(None)
```

---

## Prerequisites Check

Before invoking this skill, ensure:
1. Requirements have BR-* specifications
2. BR-* are sufficiently detailed (include formats, error messages, thresholds)

If BR-* too vague:
- Ask user: "BR-001 says 'Email validation' - what regex pattern should I use?"
- Suggest: "Should I use standard email regex or custom pattern?"

---

## Next Steps

After code generation:
1. Run generated tests (verify all pass)
2. Commit generated code
3. Integrate generated code into feature implementation (TDD or BDD workflow)

---

## Configuration

This skill respects configuration in `.claude/plugins.yml`:

```yaml
plugins:
  - name: "@aisdlc/code-skills"
    config:
      code_generation:
        auto_generate_from_br: true           # Auto-invoke when BR-* detected
        auto_generate_validators: true
        auto_generate_tests: true             # Generate tests for generated code
        require_tests_for_generated_code: true
        language: "python"                    # Target language
```

---

## Language-Specific Generation

### Python
- Constants: UPPER_SNAKE_CASE
- Functions: snake_case
- Classes: PascalCase
- Type hints: Required
- Docstrings: Google style

### TypeScript
- Constants: UPPER_SNAKE_CASE
- Functions: camelCase
- Classes: PascalCase
- Type annotations: Required
- JSDoc: Required

### Java
- Constants: UPPER_SNAKE_CASE
- Methods: camelCase
- Classes: PascalCase
- Javadoc: Required
- Annotations: Required

---

## Notes

**Why autogenerate from BR-*?**
- **Eliminates manual coding** for common patterns
- **Reduces errors** (no typos in validation logic)
- **Ensures consistency** (all validators follow same pattern)
- **Speeds development** (BR-* → code in seconds)
- **Maintains traceability** (generated code tagged with BR-*)

**What can be autogenerated**:
- ✅ Validators (regex, min/max, enum)
- ✅ Constants (numbers, strings, patterns)
- ✅ Error messages
- ✅ State machines (lockout, rate limiting)
- ✅ Tests for all generated code

**What CANNOT be autogenerated**:
- ❌ Complex business logic (requires human judgment)
- ❌ UI/UX decisions
- ❌ Integration with external systems
- ❌ Optimization strategies

**Homeostasis Goal**:
```yaml
desired_state:
  all_br_rules_have_code: true
  generated_code_has_tests: true
  generated_tests_passing: true
```

**"Excellence or nothing"** 🔥
