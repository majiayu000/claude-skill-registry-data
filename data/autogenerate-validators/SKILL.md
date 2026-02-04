---
name: autogenerate-validators
description: Autogenerate validation functions from business rules (BR-*) that specify formats, patterns, ranges, or constraints. Use when BR-* includes validation specifications like regex patterns, min/max values, or allowed values.
allowed-tools: [Read, Write, Edit]
---

# autogenerate-validators

**Skill Type**: Actuator (Code Generation)
**Purpose**: Generate validation functions from BR-* rules
**Prerequisites**:
- Business rules (BR-*) with validation specifications

---

## Agent Instructions

You are **autogenerating validators** from **business rule specifications**.

Your goal is to transform **structured validation rules** (BR-*) into **validation functions** with tests.

---

## Generation Patterns

### Pattern 1: Regex Validation

**Input**:
```yaml
BR-001: Email validation
  Format: regex ^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$
  Error: "Invalid email format"
```

**Generated**:
```python
# Generated from: BR-001
import re

EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

def validate_email(email: str) -> Optional[str]:
    """Validate email format (BR-001)"""
    if not re.match(EMAIL_REGEX, email):
        return "Invalid email format"
    return None

# Generated tests
def test_validate_email_valid():
    assert validate_email("user@example.com") is None

def test_validate_email_invalid():
    assert validate_email("invalid") == "Invalid email format"
```

---

### Pattern 2: Range Validation (Min/Max)

**Input**:
```yaml
BR-010: Payment amount
  Minimum: 0.01
  Maximum: 10000.00
  Error: "Amount must be between $0.01 and $10,000"
```

**Generated**:
```python
# Generated from: BR-010
PAYMENT_MIN_AMOUNT = 0.01
PAYMENT_MAX_AMOUNT = 10000.00

def validate_payment_amount(amount: float) -> Optional[str]:
    """Validate payment amount range (BR-010)"""
    if amount < PAYMENT_MIN_AMOUNT or amount > PAYMENT_MAX_AMOUNT:
        return "Amount must be between $0.01 and $10,000"
    return None

# Generated tests
def test_validate_amount_valid():
    assert validate_payment_amount(100.00) is None

def test_validate_amount_below_min():
    assert validate_payment_amount(0.005) == "Amount must be between $0.01 and $10,000"

def test_validate_amount_above_max():
    assert validate_payment_amount(10001.00) == "Amount must be between $0.01 and $10,000"

def test_validate_amount_boundary_min():
    assert validate_payment_amount(0.01) is None  # Exactly at minimum

def test_validate_amount_boundary_max():
    assert validate_payment_amount(10000.00) is None  # Exactly at maximum
```

---

### Pattern 3: Enum Validation (Allowed Values)

**Input**:
```yaml
BR-005: Card types
  Allowed: ["Visa", "Mastercard", "Amex"]
  Error: "Card type not supported"
```

**Generated**:
```python
# Generated from: BR-005
ALLOWED_CARD_TYPES = ["Visa", "Mastercard", "Amex"]

def validate_card_type(card_type: str) -> Optional[str]:
    """Validate card type is supported (BR-005)"""
    if card_type not in ALLOWED_CARD_TYPES:
        return "Card type not supported"
    return None

# Generated tests
def test_validate_card_visa():
    assert validate_card_type("Visa") is None

def test_validate_card_mastercard():
    assert validate_card_type("Mastercard") is None

def test_validate_card_invalid():
    assert validate_card_type("Discover") == "Card type not supported"
```

---

### Pattern 4: Length Validation

**Input**:
```yaml
BR-020: Username length
  Minimum: 3 characters
  Maximum: 20 characters
  Pattern: alphanumeric and underscore only
  Error: "Username must be 3-20 alphanumeric characters"
```

**Generated**:
```python
# Generated from: BR-020
USERNAME_MIN_LENGTH = 3
USERNAME_MAX_LENGTH = 20
USERNAME_PATTERN = r'^[a-zA-Z0-9_]+$'

def validate_username(username: str) -> Optional[str]:
    """Validate username format and length (BR-020)"""
    # Check length
    if len(username) < USERNAME_MIN_LENGTH or len(username) > USERNAME_MAX_LENGTH:
        return "Username must be 3-20 alphanumeric characters"

    # Check pattern
    if not re.match(USERNAME_PATTERN, username):
        return "Username must be 3-20 alphanumeric characters"

    return None

# Generated tests
def test_validate_username_valid():
    assert validate_username("user123") is None

def test_validate_username_too_short():
    assert validate_username("ab") == "Username must be 3-20 alphanumeric characters"

def test_validate_username_invalid_chars():
    assert validate_username("user@123") == "Username must be 3-20 alphanumeric characters"
```

---

### Pattern 5: Uniqueness Validation

**Input**:
```yaml
BR-004: Email uniqueness
  Check: User.exists(email) must be false
  Error: "Email already registered"
```

**Generated**:
```python
# Generated from: BR-004
def validate_email_unique(email: str) -> Optional[str]:
    """Validate email is not already registered (BR-004)"""
    from .models import User
    if User.exists(email):
        return "Email already registered"
    return None

# Generated tests
def test_validate_email_unique_new_email():
    assert validate_email_unique("new@example.com") is None

def test_validate_email_unique_existing_email(db_with_user):
    # Assumes fixture creates user@example.com
    assert validate_email_unique("user@example.com") == "Email already registered"
```

---

## Test Generation Rules

**For every validator, generate**:
1. **Happy path test**: Valid input → None
2. **Error case test**: Invalid input → error message
3. **Boundary tests**: Min/max edges
4. **Empty/null tests**: Empty string, None
5. **Format tests**: Specific invalid formats

---

## Output Format

```
[VALIDATOR GENERATION]

Input: 4 business rules with validation specs

Generated Validators:
  ✓ validate_email() from BR-001 (regex pattern)
  ✓ validate_password_length() from BR-002 (min length)
  ✓ validate_email_unique() from BR-004 (uniqueness check)
  ✓ validate_card_type() from BR-005 (enum values)

Generated Constants:
  ✓ EMAIL_REGEX
  ✓ PASSWORD_MIN_LENGTH
  ✓ ALLOWED_CARD_TYPES

Generated Tests:
  ✓ 16 tests (4 validators × 4 tests average)

Running tests...
  ✓ All 16 tests PASSING

Files:
  + src/validators.py (4 validators, 72 lines)
  + src/constants.py (7 constants, 14 lines)
  + tests/test_validators.py (16 tests, 98 lines)
```

---

## Notes

**Why autogenerate validators?**
- **Consistency**: All validators follow same pattern
- **Completeness**: Comprehensive test coverage auto-generated
- **Speed**: BR-* → code in seconds
- **Accuracy**: No manual coding errors

**Homeostasis Goal**:
```yaml
desired_state:
  all_br_validation_rules_have_validators: true
  all_validators_have_tests: true
  all_tests_passing: true
```

**"Excellence or nothing"** 🔥
