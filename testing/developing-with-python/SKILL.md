---
name: developing-with-python
description: Python 3.11+ development with type hints, async patterns, FastAPI, and pytest
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Python Development Skill

Modern Python 3.11+ development patterns including type hints, async programming, FastAPI, and pytest.

## Core Patterns

### Type Hints

```python
from typing import TypeVar, Generic, Callable, Awaitable
from dataclasses import dataclass
from datetime import datetime

T = TypeVar('T')

@dataclass
class Result(Generic[T]):
    """Generic result wrapper with success/error states."""
    success: bool
    data: T | None = None
    error: str | None = None

    @classmethod
    def ok(cls, data: T) -> 'Result[T]':
        return cls(success=True, data=data)

    @classmethod
    def fail(cls, error: str) -> 'Result[T]':
        return cls(success=False, error=error)


@dataclass
class User:
    id: str
    email: str
    name: str
    created_at: datetime

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'created_at': self.created_at.isoformat(),
        }
```

### Async Patterns

```python
import asyncio
from contextlib import asynccontextmanager
from typing import AsyncIterator

async def fetch_all(urls: list[str]) -> list[dict]:
    """Fetch multiple URLs concurrently."""
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_one(session, url) for url in urls]
        return await asyncio.gather(*tasks, return_exceptions=True)


@asynccontextmanager
async def managed_connection(url: str) -> AsyncIterator[Connection]:
    """Async context manager for database connections."""
    conn = await connect(url)
    try:
        yield conn
    finally:
        await conn.close()


async def process_with_timeout(
    coro: Awaitable[T],
    timeout: float = 30.0
) -> T:
    """Execute coroutine with timeout."""
    return await asyncio.wait_for(coro, timeout=timeout)
```

## FastAPI Patterns

### Application Structure

```python
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field

app = FastAPI(
    title="API",
    version="1.0.0",
    docs_url="/docs",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class UserCreate(BaseModel):
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=100)


class UserResponse(BaseModel):
    id: str
    email: EmailStr
    name: str
    created_at: datetime

    class Config:
        from_attributes = True


@app.post("/users", response_model=UserResponse, status_code=201)
async def create_user(
    data: UserCreate,
    db: Database = Depends(get_db),
) -> UserResponse:
    user = await db.users.create(data.model_dump())
    return UserResponse.model_validate(user)


@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str,
    db: Database = Depends(get_db),
) -> UserResponse:
    user = await db.users.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse.model_validate(user)
```

### Dependency Injection

```python
from functools import lru_cache
from typing import Annotated

class Settings(BaseSettings):
    database_url: str
    redis_url: str
    secret_key: str

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    return Settings()


async def get_db(
    settings: Annotated[Settings, Depends(get_settings)]
) -> AsyncIterator[Database]:
    db = Database(settings.database_url)
    await db.connect()
    try:
        yield db
    finally:
        await db.disconnect()
```

## Testing with pytest

```python
import pytest
from httpx import AsyncClient
from unittest.mock import AsyncMock, patch

@pytest.fixture
async def client(app: FastAPI) -> AsyncIterator[AsyncClient]:
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture
def mock_db() -> AsyncMock:
    return AsyncMock(spec=Database)


@pytest.mark.asyncio
async def test_create_user(client: AsyncClient, mock_db: AsyncMock):
    mock_db.users.create.return_value = {
        "id": "123",
        "email": "test@example.com",
        "name": "Test User",
        "created_at": datetime.now(),
    }

    response = await client.post("/users", json={
        "email": "test@example.com",
        "name": "Test User",
    })

    assert response.status_code == 201
    assert response.json()["email"] == "test@example.com"


@pytest.mark.asyncio
async def test_get_user_not_found(client: AsyncClient, mock_db: AsyncMock):
    mock_db.users.get.return_value = None

    response = await client.get("/users/invalid")

    assert response.status_code == 404
```

## Error Handling

```python
from fastapi import Request
from fastapi.responses import JSONResponse

class AppError(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code


@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.message},
    )


@app.exception_handler(Exception)
async def generic_error_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception("Unhandled exception")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"},
    )
```
