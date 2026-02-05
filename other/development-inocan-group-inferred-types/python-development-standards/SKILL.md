---
name: Python Development Standards
description: This skill should be used when the user asks about "Python code style", "type hints", "structlog logging", "how to log", "code organization", "testing patterns", "error handling", or needs guidance on Python development best practices, project conventions, or coding standards for this project.
---

# Python Development Standards

This skill provides Python development standards enforced by the python-dev-framework plugin. Use these patterns when writing Python code in this project.

## Quick Reference

| Topic | Standard |
|-------|----------|
| Type hints | Required on all functions |
| Future imports | `from __future__ import annotations` required |
| Generics | Use `list[str]` not `typing.List[str]` |
| Logging | Use structlog, no `print()` in src/ |
| Testing | 75% coverage minimum, pytest |
| Layout | `src/` layout with `types/`, `models/`, `_internal/` |

## Type Hints

Require type hints on all function parameters and return types:

```python
from __future__ import annotations


def process_items(items: list[str], limit: int | None = None) -> dict[str, int]:
    """Process items and return counts."""
    ...
```

**Key rules:**
- Add `from __future__ import annotations` at top of every module
- Use built-in generics (`list`, `dict`, `set`) not `typing` module equivalents
- Use `X | None` instead of `Optional[X]`
- Import protocols from `collections.abc` not `typing`

## Logging with structlog

Use structlog for all logging. The `print()` function is banned in `src/` (Ruff T201).

**Basic usage:**
```python
import structlog

log = structlog.get_logger()
log.info("user_created", user_id=123, email="user@example.com")
log.error("payment_failed", order_id=456, reason="insufficient_funds")
```

For configuration and advanced patterns, see `references/logging-patterns.md`.

## Code Organization

### Directory Layout

```
src/
├── package_name/
│   ├── __init__.py
│   ├── types/           # Type definitions
│   │   ├── __init__.py
│   │   └── _internal.py # Private types
│   ├── models/          # Data models
│   │   ├── __init__.py
│   │   └── api.py       # Pydantic models (API boundaries only)
│   └── _internal/       # Private utilities (never import externally)
│       └── utils.py
```

### API Boundaries

Use Pydantic models only at API boundaries for validation:

```python
from pydantic import BaseModel


class CreateUserRequest(BaseModel):
    email: str
    name: str
```

Use dataclasses for internal domain models.

## Error Handling

- Raise specific exceptions, not generic `Exception`
- Create custom exception classes for domain errors
- Log errors with context before re-raising

```python
class PaymentError(Exception):
    """Domain error for payment failures."""

    def __init__(self, order_id: int, reason: str) -> None:
        self.order_id = order_id
        self.reason = reason
        super().__init__(f"Payment failed for order {order_id}: {reason}")
```

## Testing

Follow these testing standards:

- **Structure**: Arrange-Act-Assert pattern
- **Fixtures**: Use pytest fixtures for shared setup
- **Parametrize**: Use `@pytest.mark.parametrize` for multiple test cases
- **Coverage**: Maintain 75% minimum coverage

```python
import pytest


@pytest.mark.parametrize("input,expected", [
    ("hello", 5),
    ("", 0),
])
def test_string_length(input: str, expected: int) -> None:
    # Arrange - done via parametrize
    # Act
    result = len(input)
    # Assert
    assert result == expected
```

## Immutability Patterns

Prefer immutable patterns to avoid subtle bugs:

| Prefer | Over | Why |
|--------|------|-----|
| `tuple(items)` | `list.append()` loop | Immutable result |
| `@dataclass(frozen=True)` | `@dataclass` | Immutable objects |
| `= None` with `or []` | `= []` default | Mutable default bug |
| `field(default_factory=list)` | `= []` in dataclass | Mutable default bug |

## Additional Resources

### Reference Files

For detailed patterns and configuration examples:
- **`references/logging-patterns.md`** - Complete structlog configuration and advanced logging patterns

### Project Documentation

- **`CLAUDE.md`** - Complete project standards and enforcement rules
- **`docs/adr/`** - Architecture Decision Records
- **`docs/tdd/`** - Technical Design Documents
