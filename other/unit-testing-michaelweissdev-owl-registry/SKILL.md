---
name: unit-testing
description: >
  Design, write, and maintain robust, isolated, and deterministic unit tests.
  Use when writing unit test suites (pytest, jest, cargo test, junit), structuring
  test fixtures, applying AAA (Arrange-Act-Assert) patterns, testing boundary
  and error conditions, or configuring test mocks and parameterization.
compatibility: >
  Agent Skills-compatible coding agents implementing unit tests across
  modern programming languages.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "testing, unit-tests, fixtures, mocks, pytest, jest, tdd"
  topics: "testing, software-development"
---

# Professional Unit Testing

Unit tests verify the smallest testable parts of an application (functions, methods, classes) in complete isolation from external systems. High-quality unit tests are fast, deterministic, maintainable, and serve as executable specifications of expected behavior.

## Core Rules

1. **Test behavior, not implementation details**: Verify output and observable side effects for given inputs. Avoid asserting on private internal method calls or transient state.
2. **Follow the AAA Pattern (Arrange, Act, Assert)**: Separate setup, execution, and verification clearly in every test.
3. **Tests must be 100% deterministic**: Never depend on real system clocks, random number generators without fixed seeds, or external network services.
4. **Fast and isolated**: Unit tests should execute in milliseconds in memory. External databases, HTTP APIs, and filesystems should be mocked or injected.
5. **Test boundaries and failure branches**: Don't just test the happy path. Test empty collections, null inputs, maximum limits, negative numbers, and expected exception types.
6. **One logical assertion per test**: Each test should verify a single distinct behavior. If a test fails, the test name should explain exactly what broke.

---

## 1. The AAA Pattern (Arrange-Act-Assert)

```python
import pytest
from app.calculator import calculate_shipping_cost, CartItem

def test_calculates_express_shipping_for_standard_weight():
    # 1. Arrange: set up inputs and preconditions
    items = [
        CartItem(sku="WIDGET-01", weight_kg=1.5, price=25.0),
        CartItem(sku="WIDGET-02", weight_kg=0.5, price=10.0),
    ]
    express = True

    # 2. Act: invoke the behavior under test
    cost = calculate_shipping_cost(items, express=express)

    # 3. Assert: verify the exact expected outcome
    assert cost == 15.50
```

---

## 2. Testing Boundary and Negative Cases

Always test where code is most likely to break:

```python
def test_calculates_shipping_for_empty_cart_is_zero():
    assert calculate_shipping_cost([], express=False) == 0.0

def test_raises_value_error_for_negative_item_weight():
    invalid_item = CartItem(sku="BAD-01", weight_kg=-2.0, price=10.0)
    
    with pytest.raises(ValueError, match="Weight must be non-negative"):
        calculate_shipping_cost([invalid_item], express=False)
```

---

## 3. Parametrized Testing

Eliminate duplicate test functions by running a single test over a matrix of inputs:

```python
import pytest
from app.validators import is_valid_username

@pytest.mark.parametrize(
    ("username", "expected"),
    [
        ("alice", True),
        ("bob_123", True),
        ("dev-user", True),
        ("", False),           # Empty string
        ("ab", False),         # Too short (< 3 chars)
        ("a" * 31, False),     # Too long (> 30 chars)
        ("admin!", False),     # Invalid special char
        ("   ", False),        # Whitespace only
    ],
)
def test_username_validation(username: str, expected: bool):
    assert is_valid_username(username) is expected
```

---

## 4. Test Fixtures and Dependency Injection

Prefer dependency injection and clean fixtures over monkey-patching:

```python
import pytest
from app.services import OrderProcessor
from tests.fakes import InMemoryInventoryRepository

@pytest.fixture
def empty_inventory():
    return InMemoryInventoryRepository()

@pytest.fixture
def processor(empty_inventory):
    return OrderProcessor(inventory_repo=empty_inventory)

def test_order_fails_when_inventory_is_insufficient(processor):
    order = {"item_id": "SKU-99", "quantity": 5}
    result = processor.place_order(order)
    
    assert result.success is False
    assert "Insufficient stock" in result.error_message
```

---

## 5. Mocking Best Practices

Use mocks **only at the architectural boundaries** (e.g. HTTP clients, payment gateways, email senders):

- **Mock external dependencies, not internal logic**. Over-mocking leads to brittle tests that pass even when the code is broken.
- **Always verify mock call arguments**:
  ```python
  def test_sends_welcome_email_on_registration(mocker):
      mock_mailer = mocker.Mock()
      service = UserService(mailer=mock_mailer)

      service.register(email="user@example.com", name="Alice")

      mock_mailer.send.assert_called_once_with(
          to="user@example.com",
          subject="Welcome to Platform",
          template="welcome_email",
      )
  ```

---

## 6. Common Mistakes and Anti-Patterns

| Anti-Pattern | Risk | Correct Practice |
| :--- | :--- | :--- |
| Testing private methods directly | Brittle tests that break on internal refactor | Test public API behavior that exercises the private logic |
| Tests sharing mutable state | Tests pass or fail depending on execution order | Isolate each test with fresh fixtures |
| Sleep in tests (`time.sleep(2)`) | Slows down test suites; race condition flakiness | Use virtual clocks or synchronization events |
| Asserting on mock implementation | Test passes even if external library signature changed | Use verified fakes or type-checked mock specs |
| Broad assertions (`assert result is not None`) | Weak test that misses incorrect property values | Assert exact expected values and structures |

---

## 7. Verification Checklist

- [ ] Tests follow the AAA structure clearly.
- [ ] Happy path, edge cases (0, empty, max limits), and error branches are covered.
- [ ] Tests execute fast (< 100ms per unit test).
- [ ] No network, disk, or real timer dependencies in unit tests.
- [ ] Tests are deterministic and pass in random order (`pytest -n auto --randomly-seed=123`).
