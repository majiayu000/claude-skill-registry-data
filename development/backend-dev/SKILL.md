---
name: backend-dev
description: FastAPI backend development with SQLAlchemy 2.0, Pydantic v2, and async Python. Use for API endpoints, database models, migrations, authentication, and background tasks.
---

# Backend Development Skill

**Activation:** FastAPI, SQLAlchemy, Pydantic, async Python, database operations

> **CRITICAL: Container-First Execution**
>
> **NEVER** run Python commands directly on the host. Always use Docker:
> ```bash
> # WRONG - will fail
> pytest tests/
> ruff check app/
>
> # RIGHT - use Docker
> docker compose exec backend pytest tests/
> docker compose exec backend ruff check app/
> ```
> See `.claude/rules/container-execution.md` for full details.

## Stack Overview

| Component | Technology | Version Policy |
|-----------|-----------|----------------|
| Framework | FastAPI | Latest stable |
| ORM | SQLAlchemy 2.0 | Async with mapped_column |
| Validation | Pydantic v2 | BaseModel schemas |
| Migrations | Alembic | Async driver |
| Auth | OAuth2 + JWT | Tone 3000 integration |
| Queue | TaskIQ | Redis backend |
| Database | PostgreSQL | Async via asyncpg |

## Architecture Pattern

```
app/
├── api/           # Route handlers (thin layer)
│   ├── auth.py    # OAuth endpoints
│   ├── shootouts.py
│   ├── jobs.py
│   └── ws.py      # WebSocket handlers
├── core/          # Configuration & shared
│   ├── config.py  # Settings from env
│   ├── security.py
│   ├── database.py
│   └── tone3000.py # API client
├── models/        # SQLAlchemy models
├── schemas/       # Pydantic schemas
├── services/      # Business logic
└── tasks/         # Background jobs
```

## Key Patterns

### 1. Route Handler (Thin Controller)

```python
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/shootouts", tags=["shootouts"])

@router.get("/{shootout_id}", response_model=ShootoutRead)
async def get_shootout(
    shootout_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> Shootout:
    """Get a shootout by ID."""
    shootout = await db.get(Shootout, shootout_id)
    if not shootout or shootout.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shootout not found"
        )
    return shootout
```

### 2. SQLAlchemy 2.0 Models

```python
from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    tone3000_id: Mapped[int] = mapped_column(unique=True, index=True)
    username: Mapped[str] = mapped_column(String(100))

    # Relationships
    shootouts: Mapped[list["Shootout"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )

class Shootout(Base):
    __tablename__ = "shootouts"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(String(200))
    config_json: Mapped[str] = mapped_column(Text)

    user: Mapped["User"] = relationship(back_populates="shootouts")
```

### 3. Pydantic Schemas

```python
from pydantic import BaseModel, ConfigDict

class ShootoutBase(BaseModel):
    title: str
    config_json: str

class ShootoutCreate(ShootoutBase):
    pass

class ShootoutRead(ShootoutBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
```

### 4. Dependency Injection

```python
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import async_session_maker

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> User:
    """Decode JWT and return current user."""
    payload = decode_token(token)
    user = await db.execute(
        select(User).where(User.tone3000_id == payload["sub"])
    )
    user = user.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user
```

### 5. Background Tasks (TaskIQ)

```python
from taskiq import TaskiqScheduler
from taskiq_redis import ListQueueBroker, RedisAsyncResultBackend

broker = ListQueueBroker(url="redis://redis:6379")
broker.with_result_backend(RedisAsyncResultBackend(redis_url="redis://redis:6379"))

@broker.task
async def process_shootout(job_id: str, shootout_id: int) -> str:
    """Process a shootout through the pipeline."""
    await update_job_status(job_id, "running", progress=0)

    # Process...
    await update_job_status(job_id, "running", progress=50)

    await update_job_status(job_id, "completed", progress=100)
    return output_path
```

## Database Operations

### Queries

```python
from sqlalchemy import select
from sqlalchemy.orm import selectinload

# Get with eager loading
stmt = (
    select(Shootout)
    .where(Shootout.user_id == user_id)
    .options(selectinload(Shootout.jobs))
    .order_by(Shootout.created_at.desc())
)
result = await db.execute(stmt)
shootouts = result.scalars().all()

# Pagination
stmt = (
    select(Shootout)
    .offset(skip)
    .limit(limit)
)
```

### Transactions

```python
async with db.begin():
    db.add(shootout)
    job = Job(shootout_id=shootout.id, status="pending")
    db.add(job)
    # Commits on exit, rolls back on exception
```

## Migrations (Alembic)

```bash
# Create migration
docker compose exec backend alembic revision --autogenerate -m "add jobs table"

# Apply migrations
docker compose exec backend alembic upgrade head

# Rollback
docker compose exec backend alembic downgrade -1
```

## Error Handling

```python
from fastapi import HTTPException, status

class AppError(Exception):
    """Base application error."""

class NotFoundError(AppError):
    """Resource not found."""

class UnauthorizedError(AppError):
    """User not authorized."""

# In routes
@router.get("/{id}")
async def get_item(id: int, db: AsyncSession = Depends(get_db)):
    item = await db.get(Item, id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item {id} not found"
        )
    return item
```

## Quality Commands

```bash
# Lint
docker compose exec backend ruff check app/

# Type check
docker compose exec backend mypy app/

# Test
docker compose exec backend pytest tests/

# All checks
just check-backend
```

## Resources

See `resources/` for detailed guides:
- `tone3000-integration.md` - OAuth and API patterns
- `taskiq-patterns.md` - Background job patterns
- `websocket-progress.md` - Real-time updates
