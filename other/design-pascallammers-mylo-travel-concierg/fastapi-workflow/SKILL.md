---
name: fastapi-workflow
description: FastAPI framework workflow guidelines. Activate when working with FastAPI projects, uvicorn, or FastAPI-specific patterns.
location: user
---

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in RFC 2119.

# FastAPI Workflow

## Tool Grid

| Task | Tool | Command |
|------|------|---------|
| Run dev | Uvicorn | `uvicorn app.main:app --reload` |
| Test | pytest + httpx | `uv run pytest` |
| Docs | Built-in | `/docs` or `/redoc` |
| Lint | Ruff | `uv run ruff check .` |
| Format | Ruff | `uv run ruff format .` |
| Type check | mypy | `uv run mypy .` |

---

## Project Structure

```
project/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app instance
│   ├── config.py            # BaseSettings configuration
│   ├── dependencies.py      # Shared Depends() callables
│   ├── exceptions.py        # Custom exception handlers
│   ├── middleware.py        # Custom middleware
│   ├── models/              # SQLAlchemy/Pydantic models
│   │   ├── __init__.py
│   │   ├── domain.py        # SQLAlchemy ORM models
│   │   └── schemas.py       # Pydantic schemas
│   ├── routers/             # APIRouter modules
│   │   ├── __init__.py
│   │   ├── users.py
│   │   └── items.py
│   ├── services/            # Business logic layer
│   │   └── __init__.py
│   └── db/                  # Database configuration
│       ├── __init__.py
│       └── session.py
├── tests/
│   ├── conftest.py          # Fixtures
│   └── test_*.py
├── pyproject.toml
└── .env
```

---

## Dependency Injection

Dependencies MUST use `Depends()` for:
- Database sessions
- Authentication/authorization
- Configuration access
- Shared services

```python
from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.config import Settings, get_settings

router = APIRouter()

# Database session dependency
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

# Settings dependency
def get_settings() -> Settings:
    return Settings()

# Service with injected dependencies
class UserService:
    def __init__(
        self,
        db: AsyncSession = Depends(get_db),
        settings: Settings = Depends(get_settings),
    ):
        self.db = db
        self.settings = settings

# Route using dependency
@router.get("/users/{user_id}")
async def get_user(
    user_id: int,
    service: UserService = Depends(),
) -> UserResponse:
    return await service.get_user(user_id)
```

### Dependency Caching

- Dependencies are cached per-request by default
- Use `Depends(get_db, use_cache=False)` to disable caching when needed

---

## Pydantic Validation

Request and response models MUST use Pydantic BaseModel or dataclasses.

```python
from pydantic import BaseModel, Field, EmailStr, ConfigDict
from datetime import datetime

# Request schema
class UserCreate(BaseModel):
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=100)
    age: int = Field(..., ge=0, le=150)

# Response schema with ORM mode
class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    name: str
    created_at: datetime

# Nested models
class UserWithItems(UserResponse):
    items: list[ItemResponse] = []
```

### Validation Rules

- MUST define explicit Field constraints for all user inputs
- MUST use `from_attributes=True` for ORM model conversion
- SHOULD use EmailStr, HttpUrl, and other specialized types
- MUST NOT expose internal fields in response models

---

## Configuration with BaseSettings

All configuration MUST use Pydantic BaseSettings.

```python
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Database
    database_url: str
    database_pool_size: int = 5

    # API
    api_prefix: str = "/api/v1"
    debug: bool = False

    # Security
    secret_key: str
    access_token_expire_minutes: int = 30

@lru_cache
def get_settings() -> Settings:
    return Settings()
```

### Configuration Rules

- MUST NOT hardcode secrets or environment-specific values
- MUST use `.env` files for local development
- SHOULD use `@lru_cache` for settings singleton
- Environment variables MUST override `.env` values

---

## Async Database Access

Database operations MUST be async using SQLAlchemy 2.0+ async.

```python
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

# Engine setup
engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
    pool_size=settings.database_pool_size,
)

async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Dependency
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
```

### Database Rules

- MUST use async drivers (asyncpg, aiosqlite)
- MUST handle session lifecycle in dependencies
- SHOULD use `expire_on_commit=False` for async sessions
- MUST NOT use synchronous database calls

---

## Router Organization

Routers MUST be organized by domain with clear prefixes and tags.

```python
# app/routers/users.py
from fastapi import APIRouter, Depends, status

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate) -> UserResponse:
    ...

@router.get("/{user_id}")
async def get_user(user_id: int) -> UserResponse:
    ...
```

```python
# app/main.py
from fastapi import FastAPI
from app.routers import users, items
from app.config import get_settings

settings = get_settings()

app = FastAPI(
    title="My API",
    version="1.0.0",
    openapi_url=f"{settings.api_prefix}/openapi.json",
)

app.include_router(users.router, prefix=settings.api_prefix)
app.include_router(items.router, prefix=settings.api_prefix)
```

### Router Rules

- MUST use descriptive tags for OpenAPI grouping
- MUST define common responses at router level
- SHOULD use status codes from `fastapi.status`
- Routers SHOULD NOT contain business logic

---

## Exception Handling

```python
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse

# Custom exception
class NotFoundError(Exception):
    def __init__(self, resource: str, id: int):
        self.resource = resource
        self.id = id

# Exception handler
@app.exception_handler(NotFoundError)
async def not_found_handler(request: Request, exc: NotFoundError) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={"detail": f"{exc.resource} with id {exc.id} not found"},
    )

# Usage in route
@router.get("/{user_id}")
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)) -> UserResponse:
    user = await db.get(User, user_id)
    if not user:
        raise NotFoundError("User", user_id)
    return user
```

### Exception Rules

- MUST use HTTPException for standard HTTP errors
- SHOULD define custom exceptions for domain errors
- MUST register exception handlers on app instance
- MUST NOT expose internal errors to clients

---

## Testing with TestClient

```python
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.main import app
from app.db.session import get_db
from app.config import get_settings, Settings

# Override settings
def get_settings_override() -> Settings:
    return Settings(database_url="sqlite+aiosqlite:///:memory:")

app.dependency_overrides[get_settings] = get_settings_override

@pytest.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac

@pytest.mark.asyncio
async def test_create_user(client: AsyncClient):
    response = await client.post(
        "/api/v1/users/",
        json={"email": "test@example.com", "name": "Test", "age": 25},
    )
    assert response.status_code == 201
    assert response.json()["email"] == "test@example.com"
```

### Testing Rules

- MUST use `httpx.AsyncClient` for async tests
- MUST override dependencies for test isolation
- SHOULD use in-memory database for unit tests
- MUST test all response status codes

---

## Background Tasks

```python
from fastapi import BackgroundTasks

async def send_notification(email: str, message: str) -> None:
    # Async notification logic
    ...

@router.post("/users/")
async def create_user(
    user: UserCreate,
    background_tasks: BackgroundTasks,
) -> UserResponse:
    new_user = await create_user_in_db(user)
    background_tasks.add_task(send_notification, user.email, "Welcome!")
    return new_user
```

### Background Task Rules

- SHOULD use for non-blocking operations (email, notifications)
- MUST NOT use for critical operations requiring confirmation
- For complex jobs, SHOULD use Celery or similar task queue

---

## Middleware

```python
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
import time

class TimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.perf_counter()
        response = await call_next(request)
        duration = time.perf_counter() - start
        response.headers["X-Process-Time"] = str(duration)
        return response

app.add_middleware(TimingMiddleware)

# CORS middleware
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Middleware Rules

- MUST add CORS middleware for browser clients
- SHOULD add request timing for observability
- Middleware MUST NOT block the event loop
- Order matters: add most critical middleware last

---

## OpenAPI Documentation

```python
from fastapi import FastAPI

app = FastAPI(
    title="My API",
    description="API for managing resources",
    version="1.0.0",
    terms_of_service="https://example.com/terms/",
    contact={
        "name": "API Support",
        "url": "https://example.com/support",
        "email": "support@example.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
)

# Route documentation
@router.get(
    "/{user_id}",
    summary="Get a user by ID",
    description="Retrieve detailed user information by their unique identifier.",
    response_description="The user object",
    responses={
        404: {"description": "User not found"},
        422: {"description": "Validation error"},
    },
)
async def get_user(user_id: int) -> UserResponse:
    """
    Get a user with all their details.

    - **user_id**: The unique identifier of the user
    """
    ...
```

### Documentation Rules

- MUST provide summary and description for all routes
- SHOULD document all possible response codes
- MUST use docstrings for detailed parameter descriptions
- Schemas SHOULD have Field descriptions

---

## Security Patterns

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await db.get(User, user_id)
    if user is None:
        raise credentials_exception
    return user

# Protected route
@router.get("/me")
async def read_users_me(current_user: User = Depends(get_current_user)) -> UserResponse:
    return current_user
```

### Security Rules

- MUST use OAuth2 or API key authentication for protected routes
- MUST validate and decode tokens in dependencies
- MUST NOT store plaintext passwords
- SHOULD use HTTPS in production
