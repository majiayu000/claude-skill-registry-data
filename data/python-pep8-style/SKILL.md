---
name: python-pep8-style
description: Use this skill when writing Python code following PEP 8 and modern Python best practices. Provides comprehensive guidance on code layout, naming conventions, EAFP philosophy, type hints, exception handling, and pytest-based TDD. Covers all critical PEP 8 rules including indentation, imports, whitespace, documentation, and idiomatic Python patterns. Appropriate for any task involving .py files, Python code reviews, refactoring, or ensuring Python code quality.
---

# Python PEP 8 Style Guide Skill

This skill embeds PEP 8 (Python Enhancement Proposal 8) - the official style guide for Python code authored by Guido van Rossum, Barry Warsaw, and Alyssa Coghlan. It also incorporates modern Python best practices from the Google Python Style Guide and community standards.

## When to Use This Skill

- Writing new Python code that should follow PEP 8 standards
- Reviewing Python code for style compliance
- Refactoring Python code to improve readability
- Learning idiomatic Python patterns
- Setting up Python project structure and tooling

## Core Python Philosophy

### The Zen of Python (PEP 20)

```python
import this
# Beautiful is better than ugly.
# Explicit is better than implicit.
# Simple is better than complex.
# Complex is better than complicated.
# Flat is better than nested.
# Sparse is better than dense.
# Readability counts.
# Special cases aren't special enough to break the rules.
# Although practicality beats purity.
# Errors should never pass silently.
# Unless explicitly silenced.
# In the face of ambiguity, refuse the temptation to guess.
# There should be one-- and preferably only one --obvious way to do it.
# Now is better than never.
# Although never is often better than *right* now.
# If the implementation is hard to explain, it's a bad idea.
# If the implementation is easy to explain, it may be a good idea.
# Namespaces are one honking great idea -- let's do more of those!
```

### EAFP vs LBYL

Python favors **EAFP (Easier to Ask for Forgiveness than Permission)** over LBYL (Look Before You Leap):

```python
# EAFP (Pythonic)
try:
    value = data["key"]["nested"]
except KeyError:
    value = default_value

# LBYL (Avoid)
if "key" in data and "nested" in data["key"]:
    value = data["key"]["nested"]
else:
    value = default_value
```

## Structural Limits

| Element | Limit | Rationale |
|---------|-------|-----------|
| Line length | 79-88 chars | PEP 8: 79, Black: 88 |
| Function length | ≤25 lines | Single responsibility |
| Function parameters | ≤5 | Use dataclasses/kwargs for more |
| Nesting depth | ≤4 levels | Extract to functions |
| Import groups | 3 | stdlib → third-party → local |

## Critical PEP 8 Rules

### Code Layout

```python
# 4 spaces per indentation level (NEVER tabs)
def long_function_name(
        var_one, var_two, var_three,
        var_four):
    print(var_one)

# Break BEFORE binary operators
income = (gross_wages
          + taxable_interest
          + (dividends - qualified_dividends)
          - ira_deduction)

# Two blank lines around top-level definitions
class MyClass:
    pass


def my_function():
    pass
```

### Imports

```python
# Standard library imports first
import os
import sys
from pathlib import Path

# Third-party imports second (blank line separator)
import requests
from pydantic import BaseModel

# Local imports third (blank line separator)
from myapp.models import User
from myapp.utils import helpers

# NEVER use wildcard imports
# from module import *  # BAD
```

### Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Modules | lowercase_underscore | `my_module.py` |
| Packages | lowercase | `mypackage` |
| Classes | PascalCase | `MyClass` |
| Functions | snake_case | `my_function()` |
| Variables | snake_case | `my_variable` |
| Constants | UPPER_SNAKE_CASE | `MAX_SIZE` |
| Private | _leading_underscore | `_internal_var` |
| "Private" class | __double_leading | `__mangled` |

### Whitespace

```python
# YES - spaces around operators
x = 1
y = x + 2
if x == 4:
    print(x, y)

# YES - no spaces inside brackets
spam(ham[1], {eggs: 2})
foo = (0,)

# YES - no space before colon in slices
ham[1:9], ham[1:9:3], ham[:9:3], ham[1::3]

# YES - no spaces around = in keyword arguments
def complex(real, imag=0.0):
    return magic(r=real, i=imag)

# YES - spaces around = with type annotations
def munge(sep: str = None): ...
```

## Modern Python Features

### Type Hints (PEP 484, 585)

```python
from typing import Optional
from collections.abc import Sequence, Mapping

# Modern type hints (Python 3.10+)
def process_items(
    items: list[str],
    config: dict[str, int] | None = None,
) -> dict[str, list[str]]:
    """Process items with optional configuration."""
    ...

# Protocol for duck typing
from typing import Protocol

class Serializable(Protocol):
    def to_dict(self) -> dict[str, Any]: ...
```

### Dataclasses

```python
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class User:
    username: str
    email: str
    created_at: datetime = field(default_factory=datetime.now)
    is_active: bool = True
    tags: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.email = self.email.lower()
```

### Context Managers

```python
from contextlib import contextmanager

# Always use context managers for resources
with open("file.txt") as f:
    data = f.read()

# Custom context manager
@contextmanager
def database_transaction(connection):
    transaction = connection.begin()
    try:
        yield transaction
        transaction.commit()
    except Exception:
        transaction.rollback()
        raise
```

## TDD Workflow

### 1. Red Phase - Write Failing Test

```python
import pytest

def test_user_creation_with_valid_email():
    user = User(email="test@example.com", name="Test")
    assert user.email == "test@example.com"

def test_user_creation_with_invalid_email_raises():
    with pytest.raises(ValueError, match="Invalid email"):
        User(email="invalid", name="Test")
```

### 2. Green Phase - Minimal Implementation

```python
@dataclass
class User:
    email: str
    name: str

    def __post_init__(self) -> None:
        if "@" not in self.email:
            raise ValueError("Invalid email format")
```

### 3. Refactor Phase - Improve While Green

```python
import re
from dataclasses import dataclass

EMAIL_PATTERN = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w+$")

@dataclass
class User:
    email: str
    name: str

    def __post_init__(self) -> None:
        self._validate_email()
        self.email = self.email.lower()

    def _validate_email(self) -> None:
        if not EMAIL_PATTERN.match(self.email):
            raise ValueError(f"Invalid email format: {self.email}")
```

## Exception Handling

```python
# Define specific exceptions
class UserNotFoundError(Exception):
    """Raised when a user cannot be found."""
    def __init__(self, user_id: int) -> None:
        self.user_id = user_id
        super().__init__(f"User {user_id} not found")

# Use exception chaining
def get_user(user_id: int) -> User:
    try:
        return database.fetch_user(user_id)
    except DatabaseError as e:
        raise UserNotFoundError(user_id) from e

# Catch specific exceptions
try:
    result = process_data(data)
except ValueError as e:
    logger.warning("Invalid data: %s", e)
    result = default_value
except (IOError, OSError) as e:
    logger.error("IO error: %s", e)
    raise ProcessingError("Failed to process") from e
```

## Quality Checklist

Before delivering Python code, verify:

### Code Style
- [ ] PEP 8 compliant (run `ruff check`)
- [ ] Line length ≤88 characters (Black standard)
- [ ] Imports organized (stdlib → third-party → local)
- [ ] No wildcard imports
- [ ] Consistent naming conventions

### Type Safety
- [ ] Type hints on all public functions
- [ ] `mypy` passes without errors
- [ ] `Optional` used for nullable types
- [ ] Return types specified

### Testing
- [ ] Tests written first (TDD)
- [ ] `pytest` tests pass
- [ ] Edge cases covered
- [ ] Error conditions tested

### Documentation
- [ ] Docstrings for public APIs (PEP 257)
- [ ] Module-level docstring
- [ ] Complex logic explained

### Modern Python
- [ ] Dataclasses for data containers
- [ ] Context managers for resources
- [ ] EAFP pattern used
- [ ] f-strings for formatting

## Essential Tooling

```bash
# Modern Python toolchain
uv pip install ruff mypy pytest pytest-cov bandit

# Run quality checks
ruff check .              # Linting (replaces flake8, isort)
ruff format .             # Formatting (replaces black)
mypy .                    # Type checking
pytest --cov=src          # Tests with coverage
bandit -r src/            # Security analysis
```

## Reference Files

For detailed patterns and examples, see:
- `references/python-patterns.md` - Comprehensive PEP 8 patterns
- `references/testing-patterns.md` - pytest and TDD patterns
- `references/modern-python.md` - Type hints, dataclasses, async

## Template Files

Quick-start templates available in `assets/templates/`:
- `class_template.py` - Standard class structure
- `service_class.py` - Service object pattern
- `pytest_test.py` - pytest test file template
- `cli_script.py` - Command-line script template