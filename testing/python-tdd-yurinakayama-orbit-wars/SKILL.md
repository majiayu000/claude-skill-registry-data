---
description: Python TDD workflow - write pytest tests first, implement, verify 80%+ coverage
---

# Python TDD Workflow

Enforce test-driven development for Python. Write pytest tests first, then implement. Verify 80%+ coverage with `pytest --cov`.

## When to Use

- Implementing new Python functions/classes
- Adding test coverage to existing code
- Fixing bugs (write failing test first)
- Building critical business logic

## TDD Cycle

### 1. RED - Write Failing Test
```python
# tests/test_validator.py
import pytest
from mypackage.validator import validate_email

@pytest.mark.parametrize("email,expected", [
    ("user@example.com", True),
    ("invalid", False),
    ("", False),
    ("user@.com", False),
    ("@example.com", False),
    ("user@example", False),
])
def test_validate_email(email: str, expected: bool) -> None:
    assert validate_email(email) == expected
```

### 2. GREEN - Write Minimal Implementation
```python
# mypackage/validator.py
import re

def validate_email(email: str) -> bool:
    if not email:
        return False
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))
```

### 3. REFACTOR - Improve While Tests Pass
```bash
pytest tests/test_validator.py -v
```

## Test Patterns

### Parametrized Tests
```python
@pytest.mark.parametrize("input_val,expected", [
    (1, "one"),
    (2, "two"),
    (3, "three"),
])
def test_number_to_word(input_val, expected):
    assert number_to_word(input_val) == expected
```

### Fixtures
```python
@pytest.fixture
def db_session():
    session = create_test_session()
    yield session
    session.rollback()
    session.close()

def test_create_user(db_session):
    user = create_user(db_session, name="Test")
    assert user.name == "Test"
```

### Mocking
```python
from unittest.mock import AsyncMock, patch

@patch("mypackage.api.httpx.AsyncClient.get")
async def test_fetch_data(mock_get):
    mock_get.return_value = AsyncMock(
        status_code=200,
        json=AsyncMock(return_value={"key": "value"})
    )
    result = await fetch_data()
    assert result == {"key": "value"}
```

### Async Tests
```python
import pytest

@pytest.mark.asyncio
async def test_async_function():
    result = await async_operation()
    assert result is not None
```

## Coverage Commands

```bash
# Run with coverage
pytest --cov=src --cov-report=term-missing

# Coverage by file
pytest --cov=src --cov-report=html

# Minimum coverage threshold
pytest --cov=src --cov-fail-under=80

# With race detection (for threaded code)
pytest -n auto  # parallel execution with pytest-xdist
```

## Coverage Targets

| Code Type | Target |
|-----------|--------|
| Critical business logic | 100% |
| Public APIs | 90%+ |
| General code | 80%+ |
| Generated code | Exclude |

## Best Practices

### DO:
- Write test FIRST (before implementation)
- Use parametrized tests for multiple cases
- Test edge cases (empty, None, boundary values)
- Use fixtures for setup/teardown
- Test behavior, not implementation
- Use `pytest.raises` for expected exceptions

### DON'T:
- Write tests after implementation
- Test private methods directly
- Use `assert True` or `assert False`
- Share mutable state between tests
- Depend on test execution order

## Related

- `/python-lint` - Fix build and lint errors
- `/python-review` - Code review
- Skills: `python-testing`, `tdd-workflow`

## Language

- Internal reasoning and thinking should be in English
- **All user-facing output, reports, and summaries must be written in Japanese**
