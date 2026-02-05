---
name: type-safety
description: Type safety best practices for modern Python development. Activated when working with type hints, basedpyright, typing-extensions, Protocol, TypedDict, generics, or type narrowing.
---

# Type safety

## Purpose

Comprehensive guide for achieving strict type safety in Python projects using basedpyright and typing-extensions. Covers modern typing patterns, type narrowing, protocols, and TypedDict best practices.

## When to use

This skill activates when:

- Writing type hints for functions and classes
- Resolving basedpyright errors
- Using typing-extensions features
- Implementing protocols or generic types
- Performing type narrowing
- Working with TypedDict specifications

## Core principles

### Comprehensive type hints required

**MANDATORY: All code must have complete type hints**

```python
# All functions must have type hints
def process(data: list[str], config: Config) -> Result:
    """Process data according to configuration."""
    pass

# All class attributes must be typed
@dataclass(slots=True, frozen=True)
class Result:
    success: bool
    data: dict[str, list[str]]
    errors: list[str] | None = None
```

### Zero tolerance for type errors

**CRITICAL: There is NO SUCH THING as an "acceptable" type error**

- ALL basedpyright errors MUST be fixed
- NEVER use `# type: ignore` without explicit user confirmation
- NEVER use `# pyright: ignore` without explicit user confirmation
- Type errors indicate real bugs or design issues

## typing-extensions usage

Use `typing-extensions` to provide modern typing features:

```python
from typing_extensions import (
    ReadOnly,  # Immutable TypedDict fields
    TypeIs,    # Improved type narrowing
    Doc,       # Inline type documentation
)
```

### ReadOnly for immutable TypedDict

```python
from typing_extensions import ReadOnly, TypedDict

class Config(TypedDict):
    """Configuration with immutable fields."""
    name: ReadOnly[str]
    options: ReadOnly[list[str]]
    enabled: ReadOnly[bool]

# Usage enforces immutability
config: Config = {
    'name': 'example',
    'options': ['a', 'b'],
    'enabled': True
}

# Type error: cannot modify ReadOnly field
config['name'] = 'other'  # basedpyright error
```

### TypeIs for type narrowing

```python
from typing_extensions import TypeIs

def is_valid_config(value: object) -> TypeIs[Config]:
    """Type narrowing with TypeIs."""
    return (
        isinstance(value, dict)
        and 'name' in value
        and isinstance(value['name'], str)
    )

# Usage
def process_value(value: object) -> None:
    if is_valid_config(value):
        # value is narrowed to Config
        print(value['name'])  # No type error
```

## Type narrowing patterns

### Using isinstance

```python
def process_result(result: Result | None) -> str:
    """Process result with type narrowing."""
    if result is None:
        return "No result"

    # result is narrowed to Result
    return result.data

def handle_value(value: str | list[str]) -> list[str]:
    """Normalize value to list."""
    if isinstance(value, str):
        return [value]
    return value
```

### Pattern matching for type narrowing

```python
from typing import Literal

ResultType = Literal['success', 'error', 'warning']

def handle_result(result: dict[str, object]) -> str:
    """Handle result using pattern matching."""
    match result:
        case {'type': 'success', 'data': str(message)}:
            return f"Success: {message}"
        case {'type': 'error', 'error': str(error)}:
            return f"Error: {error}"
        case _:
            return "Unknown result"
```

## Protocol patterns

### Defining protocols

```python
from typing import Protocol

class Processable(Protocol):
    """Protocol for processable types."""

    def process(self, data: list[str]) -> Result:
        """Process data into result."""
        ...

    def validate(self, result: Result) -> bool:
        """Validate result."""
        ...

# Structural subtyping - no inheritance needed
class SimpleProcessor:
    """Implements Processable protocol without inheriting."""

    def process(self, data: list[str]) -> Result:
        return Result(success=True, data={}, errors=None)

    def validate(self, result: Result) -> bool:
        return result.success

def use_processor(processor: Processable) -> None:
    """Accept any type implementing Processable protocol."""
    result = processor.process(['data'])
    if processor.validate(result):
        print("Valid result")
```

## Generic type patterns

### Generic functions

```python
from typing import TypeVar, Sequence

T = TypeVar('T')

def first(items: Sequence[T]) -> T | None:
    """Get first item from sequence."""
    return items[0] if items else None

# Type inference
result1: str | None = first(['a', 'b', 'c'])
result2: int | None = first([1, 2, 3])
```

### Generic classes

```python
from typing import TypeVar, Generic

T = TypeVar('T')

@dataclass(slots=True, frozen=True)
class Result(Generic[T]):
    """Generic result type."""
    value: T | None
    error: str | None

    @property
    def is_ok(self) -> bool:
        return self.error is None
```

## basedpyright configuration

```toml
# pyproject.toml
[tool.basedpyright]
typeCheckingMode = "strict"
pythonVersion = "3.14"
pythonPlatform = "All"

reportMissingTypeStubs = "error"
reportUnknownArgumentType = "error"
reportUnknownVariableType = "error"
reportMissingParameterType = "error"
```

## Common type issues and solutions

### Issue: Untyped function parameter

```python
# Error
def process(data):  # basedpyright error
    pass

# Fix
def process(data: list[str]) -> Result:
    pass
```

### Issue: Type narrowing needed

```python
# Error
def process(result: Result | None) -> str:
    return result.data  # basedpyright error

# Fix
def process(result: Result | None) -> str:
    if result is None:
        return ""
    return result.data
```

## Running type checks

```bash
# Run basedpyright
uv run basedpyright

# Check specific file
uv run basedpyright src/yourpackage/module.py

# With verbose output
uv run basedpyright --verbose
```

---

**Additional resources:**

- [basedpyright documentation](https://docs.basedpyright.com/)
- [typing-extensions documentation](https://typing-extensions.readthedocs.io/)
