---
name: python-style-guide-compact
description: Compact Python style guide. Key conventions for clean, typed, documented code.
---

# Python Style Essentials

## Imports
```python
# Standard library
import os
from pathlib import Path

# Third-party
import numpy as np

# Application
from myproject import utils
```
- Absolute imports only, alphabetized within groups
- **Application imports**: Prefer module imports (`from myproj import utils`) to avoid circular deps.
- **Third-party/Std**: Class imports ok (`from pathlib import Path`, `from pydantic import BaseModel`).

## Type Annotations
```python
def process(items: list[str], config: dict[str, Any] | None = None) -> int:
    """Process items with optional config."""
    if config is None:
        config = {}
    return len(items)
```
- Use built-in types: `list`, `dict`, `set`, `tuple` (not `typing.List`)
- Annotate all public functions
- Never use mutable defaults: `= None` then check inside

## Naming
| Type | Style | Example |
|------|-------|---------|
| module | `lower_under` | `my_module.py` |
| class | `CapWords` | `MyClass` |
| function/method | `lower_under` | `do_thing()` |
| constant | `UPPER_UNDER` | `MAX_SIZE` |
| private | `_leading` | `_internal` |

## Docstrings (Google style)
```python
def fetch_data(url: str, timeout: int = 30) -> dict[str, Any]:
    """Fetch data from URL.

    Args:
        url: The endpoint URL.
        timeout: Request timeout in seconds.

    Returns:
        Parsed JSON response as dict.

    Raises:
        ConnectionError: If request fails.
    """
```

## Key Rules
- **88 char lines** (Ruff/Black default), 4-space indent
- **f-strings** for string interpolation
- **Logging**: Use Loguru: `logger.info("Item {}", item)` (lazy `{}`)
- **File I/O**: Prefer `Path.read_text()`/`write_text()` over `open()` for simple operations
- **Implicit false**: `if not items:` not `if len(items) == 0:`
- **Comprehensions**: keep simple, use loop if complex
- **Exceptions**: catch specific, never bare `except:`
- **Empty `__init__.py`**: no code in `__init__.py` files

## Preferred Libraries

| Purpose | Library |
|---------|---------|
| Data validation | `pydantic` |
| Logging | `loguru` |
| CLI | `cyclopts`, `rich` |
| Testing | `pytest`, `pytest-mock` |

## Common Patterns
```python
# Property
@property
def area(self) -> float:
    return self._side ** 2

# Ternary
x = "yes" if condition else "no"

# Main guard
if __name__ == "__main__":
    main()
```
