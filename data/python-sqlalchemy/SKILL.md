---
name: python-sqlalchemy
description: >
  SQLAlchemy ORM patterns for Python database access. Use when defining models,
  writing queries, implementing upserts, working with JSON columns, or managing
  database sessions.
auto_load:
  enabled: true
  triggers:
    keywords: [sqlalchemy, orm, mapped_column, sessionmaker, alembic, upsert, postgres]
    file_patterns: ["*.py"]
  priority: high
  load_with: [python-fundamentals]
---

## Quick Reference

| Task | SQLAlchemy 2.0 Pattern |
|------|-------------------------|
| Define model | `class User(Base): ...` with `Mapped[...]` + `mapped_column(...)` |
| Open session | `SessionLocal = sessionmaker(bind=engine)` |
| Query rows | `session.scalars(select(User).where(...)).all()` |
| Query one | `session.scalar(select(User).where(...))` |
| Get by PK | `session.get(User, user_id)` |
| Insert/update | `session.add(obj)` then `session.commit()` |
| Delete | `session.delete(obj)` then `session.commit()` |
| Eager loading | `select(User).options(selectinload(User.posts))` |
| Pagination | `.order_by(...).limit(limit).offset(offset)` |
| Upsert (Postgres) | `insert(...).on_conflict_do_update(...)` |

| Session Rule | Why |
|--------------|-----|
| One session per request/unit of work | Prevent state leaks |
| Always rollback on exceptions | Keep transaction clean |
| Commit explicitly | Avoid accidental writes |
| Refresh after commit when needed | Ensure DB-generated fields loaded |

## When to Use This Skill

Use for **SQLAlchemy ORM and query design**:
- Defining typed models with SQLAlchemy 2.0 APIs
- Building CRUD and filtering queries
- Managing sync or async sessions and transactions
- Solving N+1 issues with relationship loading strategies
- Implementing Postgres upserts and JSONB queries

**Related skills:**
- For Python fundamentals: see `python-fundamentals`
- For async patterns: see `python-asyncio`
- For backend architecture: see `python-backend`

---

# SQLAlchemy 2.0 Practical Guide

## Base Setup

### Sync Engine and Session

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


class Base(DeclarativeBase):
    pass


engine = create_engine(
    "postgresql+psycopg://user:pass@localhost:5432/app",
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
```

### Async Engine and Session

```python
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


engine = create_async_engine(
    "postgresql+asyncpg://user:pass@localhost:5432/app",
    pool_pre_ping=True,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autoflush=False,
    expire_on_commit=False,
)
```

## Model Patterns

### Typed Model Example

```python
from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(320), unique=True, index=True)
    profile: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    posts: Mapped[list["Post"]] = relationship(back_populates="author", cascade="all, delete-orphan")


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200), index=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)

    author: Mapped[User] = relationship(back_populates="posts")
```

### Modeling Guidelines

- Use `Mapped[T]` and `mapped_column(...)` for all mapped fields
- Add DB-level constraints (`unique`, `index`, foreign keys) instead of app-only checks
- Keep relationship names explicit (`author`/`posts`) and mirrored with `back_populates`
- Prefer server timestamps (`server_default=func.now()`) for write consistency

## Query Patterns

### Select and Filter

```python
from sqlalchemy import select


def list_active_users(session, limit: int = 50):
    stmt = (
        select(User)
        .where(User.profile["active"].as_boolean().is_(True))
        .order_by(User.created_at.desc())
        .limit(limit)
    )
    return session.scalars(stmt).all()
```

### Single Row and Existence

```python
from sqlalchemy import exists, select


def get_user_by_email(session, email: str) -> User | None:
    return session.scalar(select(User).where(User.email == email))


def user_exists(session, email: str) -> bool:
    return bool(session.scalar(select(exists().where(User.email == email))))
```

### Relationship Loading

```python
from sqlalchemy import select
from sqlalchemy.orm import selectinload


def list_users_with_posts(session):
    stmt = select(User).options(selectinload(User.posts))
    return session.scalars(stmt).all()
```

- Use `selectinload` for one-to-many collections in list pages
- Use `joinedload` for many-to-one or when row explosion is acceptable
- Avoid lazy loading in response serialization paths

## Transactions and Session Lifecycle

### Sync Unit of Work

```python
def create_user(session, email: str) -> User:
    user = User(email=email)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
```

### Safe Session Scope

```python
from collections.abc import Generator


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
```

### Async Session Scope

```python
from collections.abc import AsyncGenerator


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as db:
        try:
            yield db
            await db.commit()
        except Exception:
            await db.rollback()
            raise
```

## Upserts (PostgreSQL)

```python
from sqlalchemy.dialects.postgresql import insert


def upsert_user(session, email: str, profile: dict) -> None:
    stmt = insert(User).values(email=email, profile=profile)
    stmt = stmt.on_conflict_do_update(
        index_elements=[User.email],
        set_={"profile": stmt.excluded.profile},
    )
    session.execute(stmt)
    session.commit()
```

- Prefer conflict target by unique index/constraint
- Keep upserts idempotent and explicit about updated columns

## Performance Checklist

- Select only needed columns for large list endpoints
- Add indexes for common filters and sort keys
- Use eager loading to avoid N+1 query bursts
- Paginate unbounded list queries
- Inspect generated SQL and query plans for hot paths

## Common Pitfalls

- Mixing sync session usage in async code paths
- Reusing one session across unrelated requests
- Forgetting rollback after exceptions
- Returning ORM objects after session close with lazy attributes unresolved
- Using `query(...)` patterns in new code instead of `select(...)`
