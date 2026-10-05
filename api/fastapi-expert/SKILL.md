---
name: fastapi-expert
description: Deep FastAPI expertise for async API development, dependency injection, Pydantic models, middleware, and testing. Use when building Python APIs with.
---

# FastAPI Expert

Specialized expertise in FastAPI development, providing deep guidance on async API design, Pydantic v2 model patterns, dependency injection, middleware, background tasks, WebSocket support, async database integration, testing strategies, OpenAPI customization, and production deployment.

## When to Use This Skill

Use this skill for:

- Designing RESTful APIs with path, query, and body parameters
- Building Pydantic v2 models with validators, computed fields, and serialization
- Implementing dependency injection hierarchies and scoped dependencies
- Writing middleware for CORS, authentication, rate limiting, and logging
- Running background tasks and WebSocket connections
- Integrating async databases (SQLAlchemy async, Tortoise ORM)
- Testing with TestClient, async fixtures, and dependency overrides
- Customizing OpenAPI schema and documentation
- Deploying with uvicorn, gunicorn, and Docker

**Trigger phrases**: "fastapi", "fast api", "pydantic", "python api", "async api", "uvicorn", "python rest api", "fastapi dependency injection", "fastapi middleware", "fastapi testing"

## What This Skill Does

Provides FastAPI expertise including:

- **Route Design**: Path parameters, query parameters, request body, response models
- **Pydantic v2**: Model validators, computed fields, serialization aliases, discriminated unions
- **Dependency Injection**: Sub-dependencies, yield dependencies, scoped lifetimes
- **Middleware**: CORS, authentication, rate limiting, request timing
- **Background Tasks**: Async background work, task queues
- **WebSockets**: Real-time connections with connection management
- **Database**: SQLAlchemy async sessions, repository pattern, migrations
- **Testing**: TestClient, httpx async client, dependency overrides, factory fixtures
- **Deployment**: uvicorn, gunicorn workers, Docker, health checks

## Instructions

### Step 1: Structure a FastAPI Project

**Recommended project layout**:

```
src/
  app/
    __init__.py
    main.py               # Application factory
    config.py             # Settings with Pydantic
    dependencies.py       # Shared dependencies
    middleware.py          # Custom middleware
    models/
      __init__.py
      user.py             # SQLAlchemy models
      post.py
    schemas/
      __init__.py
      user.py             # Pydantic request/response schemas
      post.py
      common.py           # Shared schemas (pagination, errors)
    routers/
      __init__.py
      users.py            # /users endpoints
      posts.py            # /posts endpoints
      auth.py             # /auth endpoints
    services/
      __init__.py
      user_service.py     # Business logic
      auth_service.py
    db/
      __init__.py
      session.py          # Database session management
      base.py             # SQLAlchemy Base
tests/
  conftest.py             # Shared fixtures
  test_users.py
  test_auth.py
  factories.py            # Test data factories
```

**Application factory**:

```python
# src/app/main.py
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.db.session import engine
from app.db.base import Base
from app.middleware import TimingMiddleware
from app.routers import users, posts, auth


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    # Startup: create tables (use Alembic in production)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown: dispose engine
    await engine.dispose()


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version="1.0.0",
        docs_url="/docs" if settings.debug else None,
        redoc_url="/redoc" if settings.debug else None,
        lifespan=lifespan,
    )

    # Middleware (order matters: last added = first executed)
    app.add_middleware(TimingMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Routers
    app.include_router(auth.router, prefix="/auth", tags=["auth"])
    app.include_router(users.router, prefix="/users", tags=["users"])
    app.include_router(posts.router, prefix="/posts", tags=["posts"])

    return app


app = create_app()
```

**Settings with Pydantic**:

```python
# src/app/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    app_name: str = "My API"
    debug: bool = False
    database_url: str = "postgresql+asyncpg://user:pass@localhost:5432/mydb"
    secret_key: str = "change-me-in-production"
    access_token_expire_minutes: int = 30
    cors_origins: list[str] = ["http://localhost:3000"]


settings = Settings()
```

### Step 2: Design Pydantic v2 Schemas

```python
# src/app/schemas/user.py
from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator, computed_field


class UserBase(BaseModel):
    """Shared fields for user schemas."""
    email: EmailStr
    display_name: Annotated[str, Field(min_length=2, max_length=50)]


class UserCreate(UserBase):
    """Schema for creating a user."""
    password: Annotated[str, Field(min_length=8, max_length=128)]

    @field_validator("password")
    @classmethod
    def password_complexity(cls, v: str) -> str:
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        return v


class UserUpdate(BaseModel):
    """Schema for partial user updates."""
    display_name: str | None = None
    email: EmailStr | None = None


class UserResponse(UserBase):
    """Schema for user responses (excludes password)."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    is_active: bool

    @computed_field
    @property
    def member_since_days(self) -> int:
        return (datetime.utcnow() - self.created_at).days


class UserListResponse(BaseModel):
    """Paginated user list."""
    data: list[UserResponse]
    total: int
    page: int
    page_size: int
    has_next: bool
```

**Discriminated union for polymorphic responses**:

```python
from typing import Literal
from pydantic import BaseModel


class TextNotification(BaseModel):
    type: Literal["text"] = "text"
    message: str


class ImageNotification(BaseModel):
    type: Literal["image"] = "image"
    image_url: str
    caption: str | None = None


class ActionNotification(BaseModel):
    type: Literal["action"] = "action"
    message: str
    action_url: str
    action_label: str


# FastAPI automatically generates correct OpenAPI schema
Notification = TextNotification | ImageNotification | ActionNotification
```

### Step 3: Implement Dependency Injection

```python
# src/app/dependencies.py
from typing import Annotated, AsyncGenerator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.db.session import async_session_factory
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Yield a database session and ensure it is closed."""
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


# Type alias for cleaner signatures
DbSession = Annotated[AsyncSession, Depends(get_db)]


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: DbSession,
) -> User:
    """Decode JWT and return the authenticated user."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
        user_id: int | None = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await db.get(User, user_id)
    if user is None or not user.is_active:
        raise credentials_exception
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


async def require_admin(user: CurrentUser) -> User:
    """Sub-dependency: require admin role."""
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return user


AdminUser = Annotated[User, Depends(require_admin)]
```

### Step 4: Build Route Handlers

```python
# src/app/routers/users.py
from fastapi import APIRouter, HTTPException, Query, status

from app.dependencies import CurrentUser, AdminUser, DbSession
from app.schemas.user import UserCreate, UserUpdate, UserResponse, UserListResponse
from app.services.user_service import UserService

router = APIRouter()


@router.get("", response_model=UserListResponse)
async def list_users(
    db: DbSession,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    search: str | None = Query(default=None, max_length=100),
):
    """List users with pagination and optional search."""
    service = UserService(db)
    users, total = await service.list_users(
        page=page, page_size=page_size, search=search
    )
    return UserListResponse(
        data=users,
        total=total,
        page=page,
        page_size=page_size,
        has_next=(page * page_size) < total,
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(user: CurrentUser):
    """Get the authenticated user's profile."""
    return user


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: DbSession):
    """Get a user by ID."""
    service = UserService(db)
    user = await service.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(data: UserCreate, db: DbSession):
    """Create a new user account."""
    service = UserService(db)
    existing = await service.get_by_email(data.email)
    if existing:
        raise HTTPException(status_code=409, detail="Email already registered")
    return await service.create(data)


@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, data: UserUpdate, user: CurrentUser, db: DbSession):
    """Update a user (self or admin)."""
    if user.id != user_id and user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    service = UserService(db)
    updated = await service.update(user_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return updated


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, admin: AdminUser, db: DbSession):
    """Delete a user (admin only)."""
    service = UserService(db)
    deleted = await service.delete(user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
```

### Step 5: Middleware Patterns

```python
# src/app/middleware.py
import time
import logging
from collections import defaultdict

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class TimingMiddleware(BaseHTTPMiddleware):
    """Log request duration for every endpoint."""

    async def dispatch(self, request: Request, call_next) -> Response:
        start = time.perf_counter()
        response = await call_next(request)
        duration_ms = (time.perf_counter() - start) * 1000
        response.headers["X-Process-Time-Ms"] = f"{duration_ms:.1f}"
        logger.info(
            "%s %s completed in %.1fms (status %d)",
            request.method,
            request.url.path,
            duration_ms,
            response.status_code,
        )
        return response


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Simple in-memory rate limiter (use Redis in production)."""

    def __init__(self, app, requests_per_minute: int = 60):
        super().__init__(app)
        self.rpm = requests_per_minute
        self.requests: dict[str, list[float]] = defaultdict(list)

    async def dispatch(self, request: Request, call_next) -> Response:
        client_ip = request.client.host if request.client else "unknown"
        now = time.time()
        window_start = now - 60

        # Clean old entries and count recent requests
        self.requests[client_ip] = [
            t for t in self.requests[client_ip] if t > window_start
        ]

        if len(self.requests[client_ip]) >= self.rpm:
            return Response(
                content='{"detail":"Rate limit exceeded"}',
                status_code=429,
                media_type="application/json",
                headers={"Retry-After": "60"},
            )

        self.requests[client_ip].append(now)
        return await call_next(request)
```

### Step 6: Database Integration (SQLAlchemy Async)

```python
# src/app/db/session.py
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.config import settings

engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
    pool_size=20,
    max_overflow=10,
    pool_pre_ping=True,
)

async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
```

```python
# src/app/models/user.py
from datetime import datetime

from sqlalchemy import String, Boolean, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    display_name: Mapped[str] = mapped_column(String(50))
    hashed_password: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(20), default="user")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
```

```python
# src/app/services/user_service.py
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.services.auth_service import hash_password


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, user_id: int) -> User | None:
        return await self.db.get(User, user_id)

    async def get_by_email(self, email: str) -> User | None:
        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def list_users(
        self, page: int, page_size: int, search: str | None
    ) -> tuple[list[User], int]:
        query = select(User).where(User.is_active.is_(True))
        count_query = select(func.count()).select_from(User).where(
            User.is_active.is_(True)
        )

        if search:
            pattern = f"%{search}%"
            query = query.where(
                User.display_name.ilike(pattern) | User.email.ilike(pattern)
            )
            count_query = count_query.where(
                User.display_name.ilike(pattern) | User.email.ilike(pattern)
            )

        total = (await self.db.execute(count_query)).scalar() or 0
        offset = (page - 1) * page_size
        result = await self.db.execute(
            query.offset(offset).limit(page_size).order_by(User.created_at.desc())
        )
        return list(result.scalars().all()), total

    async def create(self, data: UserCreate) -> User:
        user = User(
            email=data.email,
            display_name=data.display_name,
            hashed_password=hash_password(data.password),
        )
        self.db.add(user)
        await self.db.flush()
        await self.db.refresh(user)
        return user

    async def update(self, user_id: int, data: UserUpdate) -> User | None:
        user = await self.get_by_id(user_id)
        if not user:
            return None
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)
        await self.db.flush()
        await self.db.refresh(user)
        return user

    async def delete(self, user_id: int) -> bool:
        user = await self.get_by_id(user_id)
        if not user:
            return False
        await self.db.delete(user)
        return True
```

### Step 7: Background Tasks and WebSockets

**Background tasks**:

```python
from fastapi import BackgroundTasks

async def send_welcome_email(email: str, name: str) -> None:
    """Simulate sending an email (replace with real email service)."""
    # await email_client.send(to=email, subject="Welcome!", body=f"Hello {name}")
    logger.info("Welcome email sent to %s", email)


@router.post("/register", status_code=201)
async def register(
    data: UserCreate,
    background_tasks: BackgroundTasks,
    db: DbSession,
):
    service = UserService(db)
    user = await service.create(data)
    background_tasks.add_task(send_welcome_email, user.email, user.display_name)
    return UserResponse.model_validate(user)
```

**WebSocket endpoint**:

```python
from fastapi import WebSocket, WebSocketDisconnect


class ConnectionManager:
    """Manage active WebSocket connections."""

    def __init__(self):
        self.active: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active:
            await connection.send_text(message)


manager = ConnectionManager()


@router.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Message: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast("A user left the chat")
```

### Step 8: Testing

**Shared fixtures**:

```python
# tests/conftest.py
import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.db.base import Base
from app.dependencies import get_db
from app.main import create_app

TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


@pytest_asyncio.fixture(autouse=True)
async def setup_db():
    """Create tables before each test, drop after."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def db_session() -> AsyncSession:
    async with TestSessionLocal() as session:
        yield session


@pytest_asyncio.fixture
async def client(db_session: AsyncSession):
    """Provide an async test client with overridden DB dependency."""
    app = create_app()

    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()
```

**Route tests**:

```python
# tests/test_users.py
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_user(client: AsyncClient):
    response = await client.post("/users", json={
        "email": "test@example.com",
        "display_name": "Test User",
        "password": "Str0ngPass!",
    })
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["display_name"] == "Test User"
    assert "hashed_password" not in data     # Verify password is excluded
    assert "id" in data


@pytest.mark.asyncio
async def test_create_user_duplicate_email(client: AsyncClient):
    payload = {
        "email": "dupe@example.com",
        "display_name": "User One",
        "password": "Str0ngPass!",
    }
    await client.post("/users", json=payload)
    response = await client.post("/users", json={**payload, "display_name": "User Two"})
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_create_user_weak_password(client: AsyncClient):
    response = await client.post("/users", json={
        "email": "weak@example.com",
        "display_name": "Weak User",
        "password": "nodigits",
    })
    assert response.status_code == 422       # Validation error


@pytest.mark.asyncio
async def test_list_users_pagination(client: AsyncClient):
    # Create 3 users
    for i in range(3):
        await client.post("/users", json={
            "email": f"user{i}@example.com",
            "display_name": f"User {i}",
            "password": "Str0ngPass!",
        })

    response = await client.get("/users", params={"page": 1, "page_size": 2})
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) == 2
    assert data["total"] == 3
    assert data["has_next"] is True
```

### Step 9: Deployment

**uvicorn with gunicorn (production)**:

```bash
# Direct uvicorn (development)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# gunicorn with uvicorn workers (production)
gunicorn app.main:app \
  --worker-class uvicorn.workers.UvicornWorker \
  --workers 4 \
  --bind 0.0.0.0:8000 \
  --timeout 120 \
  --access-logfile -
```

**Dockerfile**:

```dockerfile
FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

FROM base AS deps
COPY pyproject.toml uv.lock ./
RUN pip install uv && uv sync --frozen --no-dev

FROM base AS runner
COPY --from=deps /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

COPY src/ ./src/

# Non-root user
RUN addgroup --system --gid 1001 appgroup && \
    adduser --system --uid 1001 --ingroup appgroup appuser
USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

CMD ["gunicorn", "app.main:app", \
     "--worker-class", "uvicorn.workers.UvicornWorker", \
     "--workers", "4", \
     "--bind", "0.0.0.0:8000"]
```

**Health check endpoint**:

```python
@app.get("/health", include_in_schema=False)
async def health_check(db: DbSession):
    """Health check that verifies database connectivity."""
    try:
        await db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception:
        return Response(
            content='{"status":"unhealthy","database":"disconnected"}',
            status_code=503,
            media_type="application/json",
        )
```

## Best Practices

- **Use async endpoints for I/O-bound operations**: database queries, HTTP calls, file I/O
- **Define response models explicitly**: prevents leaking internal fields (e.g., hashed_password)
- **Use Annotated type aliases for dependencies**: `DbSession`, `CurrentUser` keep signatures clean
- **Validate all input with Pydantic schemas**: never trust raw request data
- **Use dependency injection, not global state**: makes testing trivial with overrides
- **Commit in the dependency, not the route**: the `get_db` dependency should commit on success and rollback on error
- **Keep routes thin**: delegate business logic to service classes
- **Use structured logging**: include request ID, user ID, and duration in log entries
- **Pin dependency versions**: use `uv.lock` or `pip-compile` for reproducible builds

## Common Patterns

### Pattern 1: Repository Pattern with Service Layer

```python
# Separate data access (repository) from business logic (service)
class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def find_by_id(self, user_id: int) -> User | None:
        return await self.db.get(User, user_id)

    async def find_by_email(self, email: str) -> User | None:
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def save(self, user: User) -> User:
        self.db.add(user)
        await self.db.flush()
        await self.db.refresh(user)
        return user


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def register(self, data: UserCreate) -> User:
        existing = await self.repo.find_by_email(data.email)
        if existing:
            raise ValueError("Email already registered")
        user = User(
            email=data.email,
            display_name=data.display_name,
            hashed_password=hash_password(data.password),
        )
        return await self.repo.save(user)
```

### Pattern 2: Pagination Helper

```python
from typing import TypeVar, Generic, Sequence
from pydantic import BaseModel

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    data: Sequence[T]
    total: int
    page: int
    page_size: int
    has_next: bool
    has_prev: bool

    @classmethod
    def create(
        cls, data: Sequence[T], total: int, page: int, page_size: int
    ) -> "PaginatedResponse[T]":
        return cls(
            data=data,
            total=total,
            page=page,
            page_size=page_size,
            has_next=(page * page_size) < total,
            has_prev=page > 1,
        )
```

## Quality Checklist

- [ ] All endpoints have explicit `response_model` definitions
- [ ] Input validation uses Pydantic schemas (not manual checks)
- [ ] Passwords are hashed (bcrypt/argon2), never stored in plain text
- [ ] JWT tokens have expiration times and are validated on every request
- [ ] Database sessions are managed via dependency injection with proper cleanup
- [ ] Background tasks do not block the event loop (use async or thread pool)
- [ ] CORS is configured with specific origins (not wildcard in production)
- [ ] Tests use dependency overrides for database isolation
- [ ] Health check endpoint verifies database connectivity
- [ ] Dockerfile uses non-root user and multi-stage build
- [ ] OpenAPI schema is reviewed and reflects actual API contract
- [ ] Rate limiting is applied to authentication endpoints

## Related Skills

- `python-cleanup` - Python code quality and cleanup patterns
- `unit-tests` - General unit testing strategies
- `api-documentation` - API documentation standards
- `kubernetes-expert` - Container orchestration for API deployment
- `security-review` - Security review for API endpoints

---

**Version**: 1.0.0
**Last Updated**: March 2026

### Iterative Refinement Strategy
This skill is optimized for an iterative approach:
1. **Execute**: Perform the core steps defined above.
2. **Review**: Critically analyze the output (coverage, quality, completeness).
3. **Refine**: If targets aren't met, repeat the specific implementation steps with improved context.
4. **Loop**: Continue until the definition of done is satisfied.
