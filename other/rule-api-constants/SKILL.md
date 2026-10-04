---
name: rule-api-constants
description: MANDATORY when editing files matching ["api/src/constants/**/*.py", "api/src/db/lookups/**/*.py", "api/src/**/*_enum.py"]. Constants, StrEnum, and lookup table patterns in the API
---

# API Constants Rules

## StrEnum vs Constants vs Lookup Tables

ALWAYS use `StrEnum` for small, fixed, dev-time sets (< ~20 values) whose members never change at runtime — e.g., statuses, categories. ALWAYS use plain UPPER_SNAKE_CASE constants grouped in `api/src/constants/` for configuration thresholds and timeouts. ALWAYS use database-backed lookup tables under `api/src/db/lookups/` for values added or changed via migrations or admin UI.

Correct:
```python
# api/src/db/lookups/grant_status.py
from enum import StrEnum

class GrantStatus(StrEnum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    APPROVED = "approved"
    REJECTED = "rejected"
```

Incorrect:
```python
# Magic strings duplicated across the codebase
if status == "DRAFT": ...
if status == "draft": ...
```

## Naming

ALWAYS name enum members in UPPER_SNAKE_CASE with lower_snake_case string values that match the database representation. ALWAYS name constant modules by concern (`validation_constants.py`, `timeout_constants.py`). NEVER prefix enum class names with `Enum`.

## Lookup Table Pattern

ALWAYS follow the four-tier pattern for DB-backed lookups: (1) a `StrEnum` of known values, (2) a `LookupConfig` mapping members to ids/labels, (3) a `LookupTable` SQLAlchemy model, (4) FK columns on consuming models. NEVER define lookup rows ad hoc — always via Alembic migration.

## Single Source of Truth

NEVER hardcode the same magic string in more than one module. ALWAYS import from the enum. ALWAYS expose a `choices()` helper for Click/Marshmallow when needed.

Correct:
```python
from api.src.db.lookups.grant_status import GrantStatus
fields.String(validate=validate.OneOf([s.value for s in GrantStatus]))
```

## Immutability

NEVER mutate enum members or constants at runtime. NEVER import constants via `from module import *`.

---

## Related Rules

- **`api-database.mdc`** — lookup table model patterns and migrations
- **`api-form-schema.mdc`** — schema validation using enums
- **`api-validation.mdc`** — `ValidationErrorType` enum conventions
- **`cross-domain.mdc`** — boolean naming, SSM-driven config separation

## Specialist Validation

**Simple (add enum value):** No specialist needed.
**Moderate (new enum or constants module):** Invoke `codebase-conventions-reviewer`.
**Complex (new lookup table, migration, four-tier wiring):** Invoke `architecture-strategist` and `kieran-python-reviewer`.
