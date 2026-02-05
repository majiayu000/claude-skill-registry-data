---
name: autogenerate-constraints
description: Autogenerate constraint checking code from constraints (C-*) that specify system limits, timeouts, dependencies, or environmental requirements. Use when C-* includes technical constraints like timeouts, API limits, or compliance requirements.
allowed-tools: [Read, Write, Edit]
---

# autogenerate-constraints

**Skill Type**: Actuator (Code Generation)
**Purpose**: Generate constraint checking code from C-* specifications
**Prerequisites**:
- Constraints (C-*) with technical specifications

---

## Agent Instructions

You are **autogenerating constraint checks** from **constraint specifications**.

Your goal is to transform **structured C-* constraints** into **constraint checking functions** and **configuration**.

---

## Generation Patterns

### Pattern 1: Timeout Constraints

**Input**:
```yaml
C-001: Stripe API timeout
  Timeout: 10 seconds
  Behavior: Raise TimeoutError if exceeded
  Fallback: Return error to user
```

**Generated**:
```python
# Generated from: C-001
STRIPE_API_TIMEOUT = 10  # seconds

def call_stripe_api(operation, **kwargs):
    """
    Call Stripe API with timeout constraint.

    Generated from: C-001 (Stripe API timeout)

    Args:
        operation: Stripe API operation to call
        **kwargs: Operation parameters

    Returns:
        API response

    Raises:
        TimeoutError: If operation exceeds 10 seconds
    """
    # Implements: C-001
    try:
        return operation(timeout=STRIPE_API_TIMEOUT, **kwargs)
    except TimeoutError as e:
        # Fallback: Return error to user
        raise PaymentError("Payment service temporarily unavailable") from e

# Generated test
def test_stripe_timeout_respected(mock_stripe):
    # C-001: Verify timeout is set
    mock_stripe.Charge.create = Mock()
    call_stripe_api(mock_stripe.Charge.create, amount=100)
    mock_stripe.Charge.create.assert_called_with(timeout=10, amount=100)

def test_stripe_timeout_handles_error(mock_stripe_timeout):
    # C-001: Verify timeout error handling
    with pytest.raises(PaymentError):
        call_stripe_api(mock_stripe_timeout.Charge.create, amount=100)
```

---

### Pattern 2: Rate Limit Constraints

**Input**:
```yaml
C-010: API rate limit
  Limit: 100 requests per minute
  Behavior: Return 429 status if exceeded
  Retry: After 60 seconds
```

**Generated**:
```python
# Generated from: C-010
API_RATE_LIMIT = 100  # requests per minute
RATE_LIMIT_WINDOW = 60  # seconds

class RateLimiter:
    """
    Enforce API rate limits.

    Generated from: C-010 (API rate limit)
    """

    def __init__(self):
        self.requests = []

    def check_rate_limit(self) -> Optional[int]:
        """
        Check if rate limit would be exceeded.

        Generated from: C-010

        Returns:
            None if OK, seconds to wait if rate limited
        """
        # Implements: C-010
        now = datetime.now()
        cutoff = now - timedelta(seconds=RATE_LIMIT_WINDOW)

        # Remove old requests
        self.requests = [r for r in self.requests if r > cutoff]

        # Check limit
        if len(self.requests) >= API_RATE_LIMIT:
            # Calculate retry time
            oldest = min(self.requests)
            retry_after = RATE_LIMIT_WINDOW - (now - oldest).seconds
            return retry_after

        return None

    def record_request(self) -> None:
        """Record a request for rate limiting"""
        self.requests.append(datetime.now())

# Generated tests
def test_rate_limit_under_limit():
    limiter = RateLimiter()
    for _ in range(99):
        limiter.record_request()
    assert limiter.check_rate_limit() is None

def test_rate_limit_at_limit():
    limiter = RateLimiter()
    for _ in range(100):
        limiter.record_request()
    retry_after = limiter.check_rate_limit()
    assert retry_after is not None
    assert 0 < retry_after <= 60
```

---

### Pattern 3: Resource Limit Constraints

**Input**:
```yaml
C-020: File upload size
  Max size: 10 MB
  Behavior: Reject files larger than limit
  Error: "File too large. Maximum size is 10 MB"
```

**Generated**:
```python
# Generated from: C-020
MAX_UPLOAD_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB

def validate_file_size(file_size: int) -> Optional[str]:
    """
    Validate file size is within limit.

    Generated from: C-020 (File upload size limit)

    Args:
        file_size: File size in bytes

    Returns:
        None if valid, error message if too large
    """
    # Implements: C-020
    if file_size > MAX_UPLOAD_SIZE_BYTES:
        return "File too large. Maximum size is 10 MB"
    return None

# Generated tests
def test_file_size_valid():
    assert validate_file_size(5 * 1024 * 1024) is None  # 5 MB

def test_file_size_at_limit():
    assert validate_file_size(10 * 1024 * 1024) is None  # Exactly 10 MB

def test_file_size_too_large():
    assert validate_file_size(11 * 1024 * 1024) == "File too large. Maximum size is 10 MB"
```

---

### Pattern 4: Dependency Constraints

**Input**:
```yaml
C-030: Python version
  Minimum: 3.8
  Behavior: Raise error if version < 3.8
  Error: "Python 3.8 or higher required"
```

**Generated**:
```python
# Generated from: C-030
import sys

PYTHON_MIN_VERSION = (3, 8)

def check_python_version() -> None:
    """
    Check Python version meets minimum requirement.

    Generated from: C-030 (Python version constraint)

    Raises:
        RuntimeError: If Python version < 3.8
    """
    # Implements: C-030
    if sys.version_info < PYTHON_MIN_VERSION:
        current = f"{sys.version_info.major}.{sys.version_info.minor}"
        required = f"{PYTHON_MIN_VERSION[0]}.{PYTHON_MIN_VERSION[1]}"
        raise RuntimeError(
            f"Python {required} or higher required. Current version: {current}"
        )

# Generated test
def test_python_version_check():
    # This test always passes (we're running on valid Python)
    check_python_version()  # Should not raise
```

---

### Pattern 5: Compliance Constraints

**Input**:
```yaml
C-040: PCI-DSS compliance
  Constraint: Never store full credit card numbers
  Behavior: Tokenize cards via Stripe API
  Validation: No card numbers in logs or database
```

**Generated**:
```python
# Generated from: C-040
def validate_no_card_numbers(text: str) -> Optional[str]:
    """
    Validate text does not contain credit card numbers.

    Generated from: C-040 (PCI-DSS compliance)

    Args:
        text: Text to validate (log message, database field, etc.)

    Returns:
        None if valid, error message if card number detected
    """
    # Implements: C-040 (PCI-DSS: no storing card numbers)
    # Simple Luhn algorithm check for card-like patterns
    import re

    # Pattern: 13-19 digit sequences
    potential_cards = re.findall(r'\b\d{13,19}\b', text)

    for number in potential_cards:
        if _is_valid_luhn(number):
            return "PCI-DSS violation: Potential card number detected"

    return None

def _is_valid_luhn(card_number: str) -> bool:
    """Check if number passes Luhn algorithm (credit card check)"""
    # Luhn algorithm implementation
    digits = [int(d) for d in card_number]
    checksum = 0
    for i, d in enumerate(reversed(digits)):
        if i % 2 == 1:
            d = d * 2
            if d > 9:
                d = d - 9
        checksum += d
    return checksum % 10 == 0

# Generated tests
def test_validate_no_card_numbers_safe_text():
    assert validate_no_card_numbers("User logged in") is None

def test_validate_no_card_numbers_detects_visa():
    # Valid Visa test number
    assert validate_no_card_numbers("Card: 4532015112830366") == "PCI-DSS violation: Potential card number detected"
```

---

### Pattern 6: Idempotency Constraints

**Input**:
```yaml
C-050: Payment idempotency
  Constraint: Same idempotency key = same charge
  Key format: SHA256(user_id + timestamp + amount)
  Behavior: Return existing charge if key matches
```

**Generated**:
```python
# Generated from: C-050
import hashlib
from typing import Optional

def generate_idempotency_key(user_id: str, amount: float, timestamp: int) -> str:
    """
    Generate idempotency key for payment.

    Generated from: C-050 (Payment idempotency)

    Args:
        user_id: User identifier
        amount: Payment amount
        timestamp: Unix timestamp

    Returns:
        SHA256 hash as idempotency key
    """
    # Implements: C-050
    data = f"{user_id}{timestamp}{amount}"
    return hashlib.sha256(data.encode()).hexdigest()

def check_idempotency(idempotency_key: str) -> Optional[str]:
    """
    Check if idempotency key already used.

    Generated from: C-050

    Returns:
        Existing charge_id if key used, None if new
    """
    # Implements: C-050
    from .models import Payment
    existing = Payment.get_by_idempotency_key(idempotency_key)
    if existing:
        return existing.charge_id
    return None

# Generated tests
def test_generate_idempotency_key_deterministic():
    key1 = generate_idempotency_key("user123", 100.00, 1637000000)
    key2 = generate_idempotency_key("user123", 100.00, 1637000000)
    assert key1 == key2  # Same inputs → same key

def test_check_idempotency_new_key():
    key = generate_idempotency_key("user123", 100.00, 1637000000)
    assert check_idempotency(key) is None
```

---

## Prerequisites Check

Before invoking this skill, ensure:
1. Constraints (C-*) exist with detailed specifications
2. Specifications include: values, behaviors, error messages

If C-* too vague:
- Ask user: "C-001 says 'API timeout' - what timeout value should I use?"

---

## Next Steps

After constraint generation:
1. Run generated tests (verify all pass)
2. Commit generated code
3. Integrate into feature implementation

---

## Notes

**Why autogenerate constraints?**
- **Compliance**: Ensures constraints are enforced in code
- **Consistency**: All constraints follow same pattern
- **Documentation**: Generated code includes constraint rationale
- **Testability**: Constraints are verified via tests

**Homeostasis Goal**:
```yaml
desired_state:
  all_constraints_have_code: true
  all_constraint_code_has_tests: true
  all_tests_passing: true
```

**"Excellence or nothing"** 🔥
