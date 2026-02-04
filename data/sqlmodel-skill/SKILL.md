---
name: sqlmodel-skill
description: Reusable SQLModel skill with database models, relationships, sessions, and async operations. Use for Python ORM with SQLModel.
---

# SQLModel Skill

Use this skill when defining database models and performing ORM operations with SQLModel.

## Basic Setup

```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List

# Database connection
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+asyncpg://user:pass@host/db"

engine = create_async_engine(DATABASE_URL, echo=True)

async def get_session() -> AsyncSession:
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
```

## Model Definition

```python
class Task(SQLModel, table=True):
    """Task model for todo application."""
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True, foreign_key="user.id")
    title: str = Field(max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship (if you have User model)
    # owner: "User" = Relationship(back_populates="tasks")
```

## Field Types

```python
from sqlmodel import Field

# Primary key
id: Optional[int] = Field(default=None, primary_key=True)

# String fields
title: str = Field(max_length=200, min_length=1)
email: str = Field(max_length=255, unique=True)

# Numeric fields
price: float = Field(ge=0)
quantity: int = Field(gt=0, le=1000)

# Boolean
is_active: bool = Field(default=True)

# Datetime
created_at: datetime = Field(default_factory=datetime.utcnow)
due_date: Optional[datetime] = Field(default=None)

# Foreign key
user_id: str = Field(foreign_key="user.id", index=True)
```

## Indexes and Constraints

```python
class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)  # Single column index
    title: str
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Table args for composite indexes
    __table_args__ = (
        {"schema": "public"},  # PostgreSQL schema
    )

# Composite index (declare after class)
Task.__table__.create_element(
    Index("idx_user_completed", Task.user_id, Task.completed)
)
```

## Relationships

```python
class User(SQLModel, table=True):
    id: str = Field(primary_key=True)
    email: str = Field(unique=True)
    name: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    tasks: List["Task"] = Relationship(back_populates="owner")

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="user.id", index=True)
    title: str
    completed: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)

    owner: User = Relationship(back_populates="tasks")
```

## CRUD Operations

```python
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

async def create_task(db: AsyncSession, user_id: str, title: str, description: str = None) -> Task:
    task = Task(
        user_id=user_id,
        title=title,
        description=description,
    )
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task

async def get_tasks(db: AsyncSession, user_id: str) -> List[Task]:
    result = await db.execute(
        select(Task).where(Task.user_id == user_id)
    )
    return result.scalars().all()

async def get_task(db: AsyncSession, task_id: int, user_id: str) -> Optional[Task]:
    result = await db.execute(
        select(Task)
        .where(Task.id == task_id)
        .where(Task.user_id == user_id)
    )
    return result.scalar_one_or_none()

async def update_task(db: AsyncSession, task: Task, **kwargs) -> Task:
    for key, value in kwargs.items():
        setattr(task, key, value)
    task.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(task)
    return task

async def delete_task(db: AsyncSession, task: Task) -> bool:
    await db.delete(task)
    await db.commit()
    return True
```

## Pydantic Models for API

```python
from pydantic import BaseModel

# For creating tasks
class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str | None = Field(None, max_length=1000)

# For updating tasks
class TaskUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=200)
    description: str | None = Field(None, max_length=1000)
    completed: bool | None = None

# For API responses
class TaskResponse(TaskCreate):
    id: int
    user_id: str
    completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
```

## Best Practices

1. Use `table=True` for database tables
2. Always use `Optional[]` for nullable fields
3. Provide default values for timestamps
4. Create indexes on frequently queried columns (user_id, status)
5. Use `Relationship` for foreign keys
6. Use `AsyncSession` for async operations
7. Always `commit()` and `refresh()` after creating
8. Use Pydantic models for API input/output separation
