---
name: python-modern-typing
description: >-
  Strict modern Python typing standards (Python 3.10+ / 3.12).
  Covers built-in generics, union operator, future annotations, and SQLAlchemy Mapped[] type safety.
---

# Modern Python Typing Standards

Rules for writing clean, robust, and PEP-compliant type hints in Python 3.10+.

## Rules

### 1. Future Annotations
- Always put `from __future__ import annotations` at the top of every Python file.
- This delays evaluation of type annotations, avoiding import circularity and enabling forward-references.

### 2. Built-in Generics (PEP 585)
- Never import capitalised generic types from `typing` (e.g., `List`, `Dict`, `Tuple`, `Set`).
- Use built-in lowercase collections instead: `list`, `dict`, `tuple`, `set`.

### 3. Union Operator (PEP 604)
- Never use `typing.Union` or `typing.Optional`.
- Use the `|` operator for unions (e.g., `str | int`).
- Use `T | None` instead of `Optional[T]`.

### 4. Strict Type Safety
- **No `Any`:** Never use `Any`. Be explicit. Use `object` or generic type variables if necessary.
- **Annotate Everything:** All function signatures must type-hint all arguments and return values.

### 5. SQLAlchemy ORM Type Safety
- Ensure `Mapped[]` wrapper matches the column SQL type precisely (e.g., `Mapped[datetime]` instead of `Mapped[object]` or `Mapped[str]`).
- Do not use bare `Mapped` without a type parameter.

---

## Examples

### Good Typing Style
```python
from __future__ import annotations

from collections.abc import Sequence
from uuid import UUID

def process_items(
    items: list[str],
    prefix: str | None = None
) -> dict[str, list[int]]:
    result: dict[str, list[int]] = {}
    # implementation...
    return result
```

### Bad Typing Style
```python
from typing import List, Dict, Optional

def process_items(
    items: List[str],
    prefix: Optional[str] = None
) -> Dict[str, List[int]]:
    # ...
```

---

## Anti-Patterns

| ❌ Don't | ✅ Do instead |
|---------|--------------|
| `from typing import List, Dict, Optional` | Use `list`, `dict`, `str | None` |
| `data: Any` | Use specific models, `dict[str, object]`, or `object` |
| `Mapped[object]` for datetime columns | `Mapped[datetime]` |
| `Optional[Sequence[int]]` | `Sequence[int] | None` |
