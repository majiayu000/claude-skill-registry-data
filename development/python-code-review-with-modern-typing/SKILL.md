---
name: Python Code Review with Modern Typing
description: Review Python code ensuring strict type safety with Python 3.12+ conventions. Use when reviewing Python code, writing new Python code, or refactoring existing Python code.
---

# Python Code Review with Modern Typing

## Overview

This skill provides systematic Python code review with emphasis on Python 3.12+ type annotations. It enforces strict typing and built-in generic types (`list`, `dict`, `type`) instead of deprecated `typing` equivalents (`List`, `Dict`, `Type`).

**Scope**: This skill focuses exclusively on type annotations, not code logic, design patterns, performance, or general quality.

## When to Use

- Reviewing pull requests containing Python code
- Writing new Python functions, classes, or modules
- Refactoring existing Python code to modern standards
- Conducting code audits for type safety
- Before merging Python code to main branch

## Process

Focus only on type annotation issues.

### 1. Type Annotation Audit

Check every function, method, and variable for proper type annotations:

```python
# ✅ CORRECT - Modern Python 3.12 syntax
def process_items(items: list[str], count: int) -> dict[str, int]:
    result: dict[str, int] = {}
    for item in items[:count]:
        result[item] = len(item)
    return result

# ❌ INCORRECT - Missing types
def process_items(items, count):
    result = {}
    for item in items[:count]:
        result[item] = len(item)
    return result

# ❌ INCORRECT - Old typing module syntax
from typing import List, Dict

def process_items(items: List[str], count: int) -> Dict[str, int]:
    ...
```

**Required checks:**
- [ ] All function parameters have type annotations
- [ ] All function return types are annotated (use `-> None` if no return)
- [ ] All class attributes have type annotations
- [ ] Complex variables have inline type annotations
- [ ] No imports from `typing` for `List`, `Dict`, `Set`, `Tuple`, `Type`

### 2. Built-in Generic Types

Verify usage of built-in generics instead of `typing` module equivalents:

**Use these (Python 3.12+):**
- `list[T]` not `List[T]`
- `dict[K, V]` not `Dict[K, V]`
- `set[T]` not `Set[T]`
- `tuple[T, ...]` not `Tuple[T, ...]`
- `type[T]` not `Type[T]`

**Import from typing:**
- `Any`, `Optional`, `Union`, `Callable`, `Protocol`, `TypeVar`, `Generic`
- `Literal`, `TypedDict`, `NotRequired`, `Required`
- `overload`, `final`, `override`

```python
# ✅ CORRECT - Modern syntax
from typing import Protocol, TypeVar

T = TypeVar('T')

class Container(Protocol):
    def get_items(self) -> list[str]: ...

def merge_dicts(a: dict[str, int], b: dict[str, int]) -> dict[str, int]:
    return {**a, **b}

# ❌ INCORRECT - Old typing module imports
from typing import List, Dict, Protocol

def merge_dicts(a: Dict[str, int], b: Dict[str, int]) -> Dict[str, int]:
    return {**a, **b}
```

### 3. Optional and Union Types

Check for proper use of modern union syntax:

```python
# ✅ CORRECT - Python 3.10+ union syntax
def find_user(user_id: int) -> dict[str, str] | None:
    return users.get(user_id)

def process(value: int | str | float) -> str:
    return str(value)

# ❌ INCORRECT - Old Optional/Union syntax
from typing import Optional, Union

def find_user(user_id: int) -> Optional[dict[str, str]]:
    return users.get(user_id)

def process(value: Union[int, str, float]) -> str:
    return str(value)
```

### 4. Type Completeness Check

Ensure no untyped code exists:

**Check these locations:**
- Function signatures (parameters and returns)
- Lambda expressions (where possible)
- Class attributes and properties
- Module-level variables
- Generator and comprehension expressions (when complex)

```python
# ✅ CORRECT - Fully typed
class UserService:
    _cache: dict[int, str]

    def __init__(self, cache: dict[int, str] | None = None) -> None:
        self._cache = cache or {}

    def get_user(self, user_id: int) -> str | None:
        return self._cache.get(user_id)

# ❌ INCORRECT - Untyped attribute
class UserService:
    def __init__(self, cache=None):
        self._cache = cache or {}

    def get_user(self, user_id):
        return self._cache.get(user_id)
```

### 5. Type Checking Validation

Run static type checker:

```bash
mypy --strict your_module.py
```

Configure in `pyproject.toml`:
```toml
[tool.mypy]
strict = true
python_version = "3.12"
```

### 6. Review Checklist

- [ ] No imports of `List`, `Dict`, `Set`, `Tuple`, `Type` from `typing`
- [ ] All functions have parameter and return type annotations
- [ ] All class attributes are typed
- [ ] Union types use `|` syntax, not `Union[]`
- [ ] Optional types use `X | None`, not `Optional[X]`
- [ ] Complex nested types are properly annotated
- [ ] `mypy --strict` passes without errors
- [ ] No `# type: ignore` comments without justification

## Examples

### Example 1: API Handler Review

**Before (❌):**
```python
from typing import Dict, List, Optional

def get_users(limit=10, offset=0):
    users = fetch_from_db(limit, offset)
    return {"users": users, "count": len(users)}

def create_user(data):
    user_id = save_to_db(data)
    return {"id": user_id}
```

**After (✅):**
```python
from typing import TypedDict

class UserResponse(TypedDict):
    users: list[dict[str, str]]
    count: int

class CreateResponse(TypedDict):
    id: int

def get_users(limit: int = 10, offset: int = 0) -> UserResponse:
    users: list[dict[str, str]] = fetch_from_db(limit, offset)
    return {"users": users, "count": len(users)}

def create_user(data: dict[str, str]) -> CreateResponse:
    user_id: int = save_to_db(data)
    return {"id": user_id}
```

### Example 2: Data Processing Pipeline

**Before (❌):**
```python
from typing import List, Dict, Callable

def transform_data(data, transformers):
    result = []
    for item in data:
        for transformer in transformers:
            item = transformer(item)
        result.append(item)
    return result
```

**After (✅):**
```python
from typing import Callable, TypeVar

T = TypeVar('T')

def transform_data(
    data: list[T],
    transformers: list[Callable[[T], T]]
) -> list[T]:
    result: list[T] = []
    for item in data:
        for transformer in transformers:
            item = transformer(item)
        result.append(item)
    return result
```

### Example 3: Class with Type Parameters

**Before (❌):**
```python
from typing import Generic, TypeVar, List, Optional

T = TypeVar('T')

class Container(Generic[T]):
    def __init__(self):
        self._items = []

    def add(self, item):
        self._items.append(item)

    def get_all(self):
        return self._items
```

**After (✅):**
```python
from typing import Generic, TypeVar

T = TypeVar('T')

class Container(Generic[T]):
    _items: list[T]

    def __init__(self) -> None:
        self._items = []

    def add(self, item: T) -> None:
        self._items.append(item)

    def get_all(self) -> list[T]:
        return self._items
```

## Anti-patterns

- ❌ **Don't**: Import `List`, `Dict`, `Set`, `Tuple`, `Type` from `typing` module
  - ✅ **Do**: Use built-in `list`, `dict`, `set`, `tuple`, `type` with generic syntax

- ❌ **Don't**: Use `Optional[X]` or `Union[X, Y]` syntax
  - ✅ **Do**: Use `X | None` and `X | Y` union syntax

- ❌ **Don't**: Leave any function, method, or class attribute untyped
  - ✅ **Do**: Add complete type annotations everywhere

- ❌ **Don't**: Use `# type: ignore` without explanation
  - ✅ **Do**: Fix the type issue or document why it's necessary

- ❌ **Don't**: Use `Any` as a shortcut to avoid thinking about types
  - ✅ **Do**: Define proper types even if they're complex

- ❌ **Don't**: Skip type annotations on simple functions
  - ✅ **Do**: Type everything, even trivial functions

- ❌ **Don't**: Mix old and new typing syntax in the same codebase
  - ✅ **Do**: Consistently use Python 3.12+ syntax throughout

## Testing This Skill

Follow instructions in `examples/EXAMPLES.md`.

---

**Remember**: No untyped code. Use Python 3.12+ built-in generics. Type everything.
