---
name: prod-python
description: Use when writing, reviewing, or refactoring Python code - enforces PEP standards, modern 3.13+ typing, clean architecture, and eliminates AI slop patterns in favor of human-readable production code
---

# Production Python

Write Python like a senior developer — simple, readable, PEP-compliant. No AI slop. No over-engineering. No unnecessary abstractions.

**Core principle:** The best code is the simplest code that solves the problem correctly.

## When to Use

- Writing any Python code (scripts, APIs, libraries, CLIs)
- Refactoring existing Python code
- Code reviews — flag AI patterns
- Code feels bloated, over-abstracted, or "AI-generated"

## AI Slop — Eliminate on Sight

### Module-Level Docstrings on Every File

```python
# SLOP
"""User authentication module for handling login and registration."""

from flask import request

# CLEAN — filename says it all
from flask import request
```

Only add module docstrings for genuinely complex algorithms or non-obvious design decisions. Never add `# src/path/file.py` path comments.

### Over-Documented Obvious Code

```python
# SLOP — 20 lines to say "sum prices"
def calculate_total(items: List[Dict[str, Any]]) -> float:
    """
    Calculate the total price of items.

    Args:
        items: List of item dictionaries containing prices

    Returns:
        float: The total sum of all item prices

    Raises:
        ValueError: If items is empty
        KeyError: If price key missing
    """
    total = 0.0
    for item in items:
        total += item['price']
    return total

# CLEAN
def calculate_total(items: list[dict]) -> float:
    return sum(item['price'] for item in items)
```

Docstrings: one line max for obvious functions. Skip entirely if the signature tells the story.

### Narrating Code with Comments

```python
# SLOP
# Initialize the user list
users = []
# Loop through each record
for record in records:
    # Create user object
    user = User(record)
    # Append to list
    users.append(user)

# CLEAN
users = [User(r) for r in records]
```

Comments explain **WHY**, never **WHAT**. If you need to explain what code does, rewrite the code.

### Legacy `typing` Imports

```python
# SLOP — pre-3.9 style
from typing import List, Dict, Optional, Union, Tuple, Any

def process(data: List[Dict[str, Any]]) -> Optional[Dict[str, Union[str, int]]]:
    ...

# CLEAN — modern builtins + PEP 604
def process(data: list[dict]) -> dict | None:
    ...
```

**Never import from `typing` for:** `List`, `Dict`, `Tuple`, `Set`, `FrozenSet`, `Type`, `Optional`, `Union`. Use builtins and `|` syntax.

### Premature Abstraction

```python
# SLOP
class DataProcessor:
    def __init__(self, config):
        self.config = config

    def process(self, data):
        return self._transform(self._validate(data))

    def _validate(self, data):
        return data

    def _transform(self, data):
        return [x * 2 for x in data]

# CLEAN
def process_data(data: list[int]) -> list[int]:
    return [x * 2 for x in data]
```

Classes are for **state**. If your class has one method or no meaningful state, it's a function.

### Over-Engineered Return Types

```python
# SLOP
class ValidationResult:
    def __init__(self, is_valid: bool, error: str | None = None):
        self.is_valid = is_valid
        self.error = error

def validate(user: dict) -> ValidationResult:
    if not user.get('email'):
        return ValidationResult(False, "Email required")
    return ValidationResult(True)

# CLEAN
def validate(user: dict) -> str | None:
    """Return error message or None if valid."""
    if not user.get('email'):
        return "Email required"
    return None
```

### Wrapper Functions That Add Nothing

```python
# SLOP
def get_user_by_email(email: str) -> dict | None:
    """Retrieve a user record from the database by their email address."""
    query = "SELECT * FROM users WHERE email = :email"
    result = db.execute(query, {"email": email}).fetchone()
    return dict(result) if result else None

# CLEAN
def get_user(email: str) -> dict | None:
    return db.execute(
        "SELECT * FROM users WHERE email = :email", {"email": email}
    ).fetchone()
```

### Noise Logging

```python
# SLOP
logger.info("Starting user processing")
logger.info(f"Found {len(users)} users")
for user in users:
    logger.debug(f"Processing user {user.id}")
    process(user)
logger.info("Finished processing users")

# CLEAN
logger.info("Processing %d users", len(users))
for user in users:
    process(user)
if failures:
    logger.error("Failed %d users: %s", len(failures), failures[:5])
```

Log **events that matter**: errors, warnings, key metrics. Not every step.

### Defensive Programming Against Impossible States

```python
# SLOP — checking for things that can't happen
def process_order(order: Order) -> None:
    if order is None:
        raise ValueError("Order cannot be None")
    if not isinstance(order, Order):
        raise TypeError("Expected Order instance")
    if not hasattr(order, 'items'):
        raise AttributeError("Order must have items")
    # actual logic starts here...

# CLEAN — trust your own code, validate at boundaries
def process_order(order: Order) -> None:
    for item in order.items:
        item.fulfill()
```

Validate at system boundaries (user input, external APIs). Trust internal code.

## Modern Python (3.13+)

### Type Syntax

```python
# Builtins as generics (3.9+)
names: list[str] = []
config: dict[str, int] = {}
pair: tuple[str, int] = ("a", 1)
ids: set[int] = set()

# Union with | (3.10+)
def find(id: int) -> User | None: ...
def parse(value: str | bytes) -> dict: ...

# type statement for aliases (3.12+)
type JSON = dict[str, 'JSON'] | list['JSON'] | str | int | float | bool | None
type Handler = Callable[[Request], Response]

# TypeVar with defaults (3.13+)
from typing import TypeVar
type T = TypeVar('T', default=int)

# Generic classes — modern syntax (3.12+)
class Stack[T]:
    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        return self._items.pop()
```

### When to Type-Hint

```python
# SKIP type hints — signature is obvious
def double(x):
    return x * 2

def greet(name):
    return f"Hello, {name}"

# ADD type hints — return type isn't obvious
def fetch_user(user_id: int) -> User | None: ...
def parse_config(path: str) -> dict[str, str]: ...
def connect(url: str, *, timeout: float = 30) -> Connection: ...
```

Type-hint when the types **clarify**. Skip when they're noise.

### Structural Pattern Matching (3.10+)

```python
# Use match for complex dispatch — not if/elif chains
match command:
    case {"action": "create", "name": str(name)}:
        create_resource(name)
    case {"action": "delete", "id": int(id_)}:
        delete_resource(id_)
    case {"action": str(action)}:
        raise ValueError(f"Unknown action: {action}")

# For HTTP status handling
match response.status_code:
    case 200 | 201:
        return response.json()
    case 404:
        return None
    case 429:
        raise RateLimitError(response.headers.get("Retry-After"))
    case status if status >= 500:
        raise ServerError(f"Server error: {status}")
```

### Exception Groups (3.11+)

```python
# Collect multiple errors, raise together
async def validate_all(items: list[dict]) -> list[dict]:
    errors = []
    valid = []
    for i, item in enumerate(items):
        try:
            valid.append(validate(item))
        except ValueError as e:
            errors.append(e)

    if errors:
        raise ExceptionGroup("Validation failed", errors)
    return valid
```

### F-Strings — Always

```python
# Use f-strings, never % or .format()
name = f"{first} {last}"
path = f"/api/v{version}/users/{user_id}"
msg = f"Processed {count:,} items in {elapsed:.2f}s"
```

### Walrus Operator

```python
# Assign and test in one expression
if (match := pattern.search(text)) is not None:
    process(match.group(1))

if (user := get_user(email)) is not None:
    send_welcome(user)

# In while loops
while (chunk := f.read(8192)):
    process(chunk)

# In comprehensions
results = [
    cleaned
    for raw in data
    if (cleaned := clean(raw)) is not None
]
```

## Production Patterns

### Error Handling

```python
# Specific exceptions with context
def load_config(path: str) -> dict:
    try:
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError:
        raise ValueError(f"Config not found: {path}") from None
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in {path}: {e}") from e

# Custom exceptions — only when callers need to catch them
class PaymentError(Exception):
    def __init__(self, amount: float, reason: str):
        self.amount = amount
        self.reason = reason
        super().__init__(f"Payment of {amount} failed: {reason}")
```

Never catch bare `Exception` unless re-raising. Never silently swallow errors.

### Data Classes over Dicts

```python
# When you need structured data with known fields
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class User:
    name: str
    email: str
    active: bool = True

# For config / settings
@dataclass(frozen=True, slots=True)
class DBConfig:
    host: str
    port: int = 5432
    pool_size: int = 10
```

Use `slots=True` for memory efficiency. Use `frozen=True` when immutability makes sense.

### Async Done Right

```python
import asyncio
import httpx

async def fetch_users(urls: list[str]) -> list[dict]:
    async with httpx.AsyncClient() as client:
        tasks = [client.get(url) for url in urls]
        responses = await asyncio.gather(*tasks, return_exceptions=True)

    results = []
    for resp in responses:
        if isinstance(resp, Exception):
            logger.error("Fetch failed: %s", resp)
            continue
        results.append(resp.json())
    return results
```

### Context Managers for Resources

```python
from contextlib import contextmanager

@contextmanager
def db_transaction(conn):
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise

# Usage
with db_transaction(conn) as tx:
    tx.execute("INSERT INTO users ...")
```

### Comprehensions — Know When to Stop

```python
# YES — simple transforms and filters
active = [u for u in users if u.active]
by_id = {u.id: u for u in users}
emails = {u.email for u in users}

# NO — too complex, use a loop
# SLOP
results = [
    transform(item)
    for group in data
    for item in group.items
    if item.valid and item.category in allowed
    and not item.archived
]

# CLEAN
results = []
for group in data:
    for item in group.items:
        if item.valid and item.category in allowed and not item.archived:
            results.append(transform(item))
```

If a comprehension needs more than one `if` or is hard to read in 2 seconds, use a loop.

### Pathlib over os.path

```python
from pathlib import Path

config_dir = Path.home() / ".config" / "myapp"
config_dir.mkdir(parents=True, exist_ok=True)

for py_file in Path("src").rglob("*.py"):
    process(py_file)

content = Path("data.json").read_text()
Path("output.txt").write_text(result)
```

### Enums for Fixed Choices

```python
from enum import StrEnum

class Status(StrEnum):
    PENDING = "pending"
    ACTIVE = "active"
    SUSPENDED = "suspended"

# Use StrEnum so values serialize naturally
user.status = Status.ACTIVE
assert user.status == "active"  # works
```

## Import Organization (PEP 8)

```python
# 1. Standard library
import json
import logging
from pathlib import Path

# 2. Third-party
import httpx
from fastapi import FastAPI

# 3. Local
from .models import User
from .config import settings
```

No blank lines within groups. One blank line between groups. Alphabetical within each group. Absolute imports preferred. Use `isort` for automation.

## Project Layout

```
project/
    src/
        project_name/
            __init__.py
            main.py
            models.py
            config.py
    tests/
        test_main.py
        test_models.py
        conftest.py
    pyproject.toml
```

Use `pyproject.toml` for all config. No `setup.py`, no `setup.cfg`, no `requirements.txt` for libraries (use `pyproject.toml` dependencies). `requirements.txt` is acceptable for applications that pin exact versions.

## Quick Reference

| Situation | Do | Don't |
|---|---|---|
| Types | `list[str]`, `dict | None` | `List[str]`, `Optional[Dict]` |
| Module docstrings | Skip | `"""Module for X."""` everywhere |
| Function docstrings | One line or skip | Multi-paragraph for simple code |
| Comments | Explain WHY | Narrate WHAT |
| Functions | One clear purpose | `_helper`, `_util` suffixes |
| Classes | When state is needed | Single-method wrappers |
| Errors | Specific + context | Bare `except Exception` |
| Logging | Errors + key events | Every step |
| Strings | f-strings | `.format()` or `%` |
| Paths | `pathlib.Path` | `os.path.join` |
| Data | `@dataclass(slots=True)` | Plain dicts for structured data |
| Config | `pyproject.toml` | `setup.py` + `setup.cfg` |
| Constants | `StrEnum` / `IntEnum` | Magic strings/numbers |
| Validation | At boundaries only | Defensive checks everywhere |

## Red Flags — Simplify Immediately

- `from typing import List, Dict, Optional, Union` — use builtins + `|`
- `from __future__ import annotations` — unnecessary on 3.13+
- Module docstring on every file
- `# src/path/file.py` comment at top
- Function with `_helper`, `_util`, `_internal` suffix
- Class with one method → make it a function
- Docstring longer than the function body
- More comments than code
- 3+ levels of indentation → refactor
- `isinstance` checks in internal code
- `if x is not None: return x` / `else: return None` → just `return x`
- Wrapper functions that add nothing
- `**kwargs` when you know the exact parameters
- Empty `__init__.py` with docstrings
- `try: ... except Exception: pass`

## Real-World Impact

**Before (AI slop — 45 lines):**
```python
from typing import List, Dict, Any, Optional

class UserValidator:
    """Validator for user data."""

    def __init__(self) -> None:
        self.required_fields: List[str] = ['email', 'name']

    def validate(self, user: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate user data.

        Args:
            user: User dictionary to validate

        Returns:
            Validation result with is_valid and errors
        """
        errors: List[str] = []
        for field in self.required_fields:
            if not user.get(field):
                errors.append(f"{field} is required")

        return {
            'is_valid': len(errors) == 0,
            'errors': errors
        }

validator = UserValidator()
result = validator.validate(user_data)
if not result['is_valid']:
    handle_errors(result['errors'])
```

**After (clean — 8 lines):**
```python
def validate_user(user: dict) -> list[str]:
    errors = []
    if not user.get('email'):
        errors.append("Email required")
    if not user.get('name'):
        errors.append("Name required")
    return errors

if errors := validate_user(user_data):
    handle_errors(errors)
```

**Result:** 82% less code. More readable. Same functionality. No imports needed.
