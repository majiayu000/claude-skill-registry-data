---
name: fastapi-sqlalchemy-standards
description: >-
  FastAPI + SQLAlchemy standards for this project. Use when writing or reviewing
  FastAPI routers, dependencies, SQLAlchemy models, or database sessions. Triggers
  on tasks involving get_db, Depends, ORM models, sessions, authentication dependencies,
  or any mention of "duplicate", "bare except", "inline import", or HTTP status codes.
---

# FastAPI + SQLAlchemy Standards

Project-specific rules derived from production bugs and code review findings.

---

## 1. SQLAlchemy — Always Use Modern `Mapped[]` Style

Python 3.12+ / SQLAlchemy 2.x project. **All models must use the modern declarative style.**

```python
# ❌ BANNED — legacy Column() style
from sqlalchemy import Column, String, Boolean
id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
email = Column(String, unique=True)

# ✅ REQUIRED — modern Mapped[] style
from sqlalchemy.orm import Mapped, mapped_column
id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
email: Mapped[str] = mapped_column(String, unique=True)
```

**Rule**: If you see `Column(` in any model file, it is wrong. Rewrite it.

### Typed fields

```python
# ❌ Wrong — Mapped[object] hides the real type
created_at: Mapped[object] = mapped_column(DateTime(timezone=True), ...)

# ✅ Correct
from datetime import datetime
created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), ...)
```

### SQLite test compat — JSON vs JSONB

Always use `JSON().with_variant(JSONB, "postgresql")` — NOT bare `JSONB` — so SQLite-based tests still work:

```python
# ❌ Breaks SQLite tests
data: Mapped[dict] = mapped_column(JSONB, nullable=True)

# ✅ Works on both PostgreSQL (prod) and SQLite (tests)
from sqlalchemy import JSON
from sqlalchemy.dialects.postgresql import JSONB
data: Mapped[dict] = mapped_column(JSON().with_variant(JSONB, "postgresql"), nullable=True)
```

---

## 2. `get_db` — Single Source of Truth

**There must be exactly ONE `get_db` function in the entire codebase.**

```
db/session.py        ← SINGLE definition here
routers/dependencies.py  ← re-import only: `from db.session import get_db`
```

```python
# ❌ BANNED — duplicate definition in dependencies.py
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ CORRECT — re-export from the canonical location
from db.session import get_db  # noqa: F401  (re-export)
```

**Why**: FastAPI's dependency override system (`app.dependency_overrides[get_db]`) uses function object identity. Two `get_db` functions = two different keys = tests only override one and the app uses the other.

---

## 3. `routers/dependencies.py` Patterns

### Never use bare `except Exception` in auth code

```python
# ❌ WRONG — swallows real errors (DB crash → silently becomes 401)
try:
    payload = jwt.decode(...)
    ...
except Exception:
    raise credentials_exception

# ✅ CORRECT — only catch JWT-specific failures
from jose import JWTError
try:
    payload = jwt.decode(...)
except JWTError:
    raise _CREDENTIALS_401
```

### No inline imports inside functions

```python
# ❌ WRONG — slow, hides deps from IDE, re-evaluated each call
def get_current_user(...):
    from core.security import ALGORITHM  # ← inline
    ...

# ✅ CORRECT — top of file
from core.security import ALGORITHM
```

### Module-level exception constants

```python
# ❌ WRONG — allocates new HTTPException object on every request
def get_current_user(...):
    credentials_exception = HTTPException(status_code=401, ...)
    ...

# ✅ CORRECT — create once at module level
_CREDENTIALS_401 = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)
```

### Correct HTTP status for inactive users

```python
# ❌ WRONG — 400 Bad Request implies the client sent bad data
raise HTTPException(status_code=400, detail="Inactive user")

# ✅ CORRECT — 403 Forbidden: user exists but access denied
raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User account is deactivated")
```

---

## 4. Service Layer — Dependency Injection, Not Session Storage

```python
# ❌ SMELL — service holds db session, impossible to unit test without DB
class LLMAnalysisService:
    def __init__(self, db: Session):
        self.db = db
        self.result = self.db.query(...)  # ← tightly coupled

# ✅ BETTER — inject pre-fetched data, keep service pure
class LLMAnalysisService:
    def analyze(self, image_data: bytes, excel_data: bytes | None) -> dict:
        ...  # No DB access — just logic
```

The **router** fetches data from DB, passes it to the service, and writes results back.

---

## 5. Import Ordering (isort-compatible)

```python
# ✅ Correct order for every Python file in this project
from __future__ import annotations  # ← always first if used

# stdlib
import uuid
from collections.abc import Generator
from datetime import datetime

# third-party
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

# local — first-party
from core.config import settings
from db.session import get_db
from models.user import User
```

Run `ruff check --select I --fix .` to auto-fix import order.

---

## Checklist — Before Submitting Any ORM/API Code

- [ ] All model columns use `Mapped[T]` + `mapped_column()` — no `Column()`
- [ ] `Mapped[object]` does not exist anywhere — use the real type
- [ ] `get_db` defined exactly once (`db/session.py`), re-imported everywhere else
- [ ] JSONB columns use `JSON().with_variant(JSONB, "postgresql")` for SQLite compat
- [ ] No bare `except Exception` in authentication/authorization paths
- [ ] No inline imports inside function bodies
- [ ] HTTP 403 (not 400) for active/inactive user access denial
- [ ] `from __future__ import annotations` at top of every file using `X | Y` types
