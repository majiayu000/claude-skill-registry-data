---
name: python
description: Python development with ruff, mypy, pytest - TDD and type safety
when-to-use: When working on Python files
user-invocable: false
paths: ["**/*.py", "pyproject.toml", "setup.py", "requirements*.txt"]
effort: medium
---

# Python Skill

## Type Hints

- Use type hints on all function signatures
- Use `typing` module for complex types

```python
def process_user(user_id: int, options: dict[str, Any] | None = None) -> User:
    ...
```

---

## Patterns

### Dependency Injection

```python
# Don't import dependencies directly in business logic — pass them in.

# Bad
from .db import database
def get_user(user_id: int) -> User:
    return database.fetch(user_id)

# Good
def get_user(user_id: int, db: Database) -> User:
    return db.fetch(user_id)
```

### Result Pattern (No Exceptions in Core)

```python
from dataclasses import dataclass

@dataclass
class Result[T]:
    value: T | None
    error: str | None

    @property
    def is_ok(self) -> bool:
        return self.error is None
```

---

## Python Anti-Patterns

- ❌ `from module import *`
- ❌ Mutable default arguments
- ❌ Bare `except:` clauses
- ❌ Using `type: ignore` without explanation
- ❌ Global variables for state
- ❌ Classes when functions suffice

---

*TRIM 2026-07-18 (ADR-0008, FOCUS-004): this skill auto-fires on every `.py` edit here
(`paths: **/*.py`, ~123 files), so its defects did real harm. Cut the sections that prescribe a
toolchain and layout Tessera pointedly does not use: the "Tooling (Required)" block (ruff + `mypy
--strict` + `pyproject.toml` + `.pre-commit-config.yaml` — Tessera is uv-venv + stdlib-heavy `scripts/`
+ `run-tests.sh`), the `src/package_name/core|infra` + FastAPI project structure (Tessera uses
`scripts/`, `bin/`), the GitHub-Actions and pre-commit-hook scaffolding, the `package_name`-layout
pytest example, and the Pydantic pattern (a dependency Tessera doesn't carry). Kept the language core:
type hints, DI, the Result pattern, and the anti-patterns. **Nothing lost:** the cut scaffolding is
generic downstream Python-app content (not Tessera-specific) and survives in **git history** (pre this
commit). This trims the *project* copy only; the global `~/.claude/skills/python` copy is currently
un-trimmed, but — per the base lesson of 2026-07-18 — a global copy is NOT a guaranteed archive (base's
was silently trimmed to match). How downstream apps should actually receive the full body is the open
delivery question — see `docs/observatory.md` → "Skill-body delivery has no copy mechanism".*
