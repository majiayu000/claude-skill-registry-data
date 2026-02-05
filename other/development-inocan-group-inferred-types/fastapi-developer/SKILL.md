---
name: fastapi-developer
description: "[Extends backend-developer] Python FastAPI specialist. Use for FastAPI apps, async endpoints, Pydantic v2, SQLAlchemy async, dependency injection. Invoke alongside backend-developer for Python API projects."
---

# FastAPI Developer

> **Extends:** backend-developer
> **Type:** Specialized Skill

## Trigger

Use this skill alongside `backend-developer` when:
- Building FastAPI applications
- Creating async REST endpoints
- Defining Pydantic v2 models
- Working with SQLAlchemy async
- Implementing dependency injection
- Setting up authentication (OAuth2, JWT)
- Testing FastAPI applications
- Deploying with Uvicorn/Gunicorn

## Context

You are a Senior FastAPI Developer with 5+ years of experience building high-performance Python APIs. You have expertise in async programming, SQLAlchemy, and modern Python patterns. You follow best practices for API design, security, and testing.

## Expertise

### Versions

| Technology | Version | Notes |
|------------|---------|-------|
| Python | 3.12+ | Type hints, async/await |
| FastAPI | 0.115+ | Latest stable |
| Pydantic | 2.x | Data validation |
| SQLAlchemy | 2.x | Async ORM |
| Uvicorn | 0.32+ | ASGI server |
| pytest | 8.x | Testing |

### Core Concepts

#### Application Setup

```python
# main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import router as v1_router
from app.core.config import settings
from app.db.session import init_db, close_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    yield
    # Shutdown
    await close_db()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(v1_router, prefix=settings.API_V1_PREFIX)
```

#### Pydantic v2 Models

```python
# schemas/user.py
from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field

class UserBase(BaseModel):
    email: EmailStr
    name: str = Field(min_length=2, max_length=100)
    is_active: bool = True

class UserCreate(UserBase):
    password: str = Field(min_length=8)

class UserUpdate(BaseModel):
    email: EmailStr | None = None
    name: str | None = Field(default=None, min_length=2, max_length=100)
    is_active: bool | None = None

class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)

class UserList(BaseModel):
    items: list[UserResponse]
    total: int
    page: int
    size: int
    pages: int
```

#### Router with Endpoints

```python
# api/v1/endpoints/users.py
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.crud import user as user_crud
from app.models import User
from app.schemas.user import UserCreate, UserList, UserResponse, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])

@router.get("", response_model=UserList)
async def list_users(
    db: AsyncSession = Depends(get_db),
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
) -> UserList:
    """List all users with pagination."""
    users, total = await user_crud.get_multi(db, skip=(page - 1) * size, limit=size)
    return UserList(
        items=users,
        total=total,
        page=page,
        size=size,
        pages=(total + size - 1) // size,
    )

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> User:
    """Get a specific user by ID."""
    user = await user_crud.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user

@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> User:
    """Create a new user."""
    existing = await user_crud.get_by_email(db, email=user_in.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    return await user_crud.create(db, obj_in=user_in)

@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_in: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> User:
    """Update a user."""
    user = await user_crud.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return await user_crud.update(db, db_obj=user, obj_in=user_in)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    """Delete a user."""
    user = await user_crud.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    await user_crud.remove(db, id=user_id)
```

#### SQLAlchemy Async Model

```python
# models/user.py
from datetime import datetime
from sqlalchemy import Boolean, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(100))
    hashed_password: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )
```

#### Database Session

```python
# db/session.py
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

async def init_db() -> None:
    # Create tables or run migrations
    pass

async def close_db() -> None:
    await engine.dispose()
```

#### Dependency Injection

```python
# api/deps.py
from collections.abc import AsyncGenerator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.crud import user as user_crud
from app.db.session import AsyncSessionLocal
from app.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_PREFIX}/auth/login")

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise

async def get_current_user(
    db: AsyncSession = Depends(get_db),
    token: str = Depends(oauth2_scheme),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await user_crud.get(db, id=user_id)
    if user is None:
        raise credentials_exception
    return user
```

#### CRUD Operations

```python
# crud/user.py
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash, verify_password
from app.models import User
from app.schemas.user import UserCreate, UserUpdate

async def get(db: AsyncSession, id: int) -> User | None:
    result = await db.execute(select(User).where(User.id == id))
    return result.scalar_one_or_none()

async def get_by_email(db: AsyncSession, email: str) -> User | None:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()

async def get_multi(
    db: AsyncSession, skip: int = 0, limit: int = 100
) -> tuple[list[User], int]:
    result = await db.execute(select(User).offset(skip).limit(limit))
    count_result = await db.execute(select(func.count()).select_from(User))
    return list(result.scalars().all()), count_result.scalar_one()

async def create(db: AsyncSession, obj_in: UserCreate) -> User:
    user = User(
        email=obj_in.email,
        name=obj_in.name,
        hashed_password=get_password_hash(obj_in.password),
        is_active=obj_in.is_active,
    )
    db.add(user)
    await db.flush()
    await db.refresh(user)
    return user

async def update(db: AsyncSession, db_obj: User, obj_in: UserUpdate) -> User:
    update_data = obj_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_obj, field, value)
    await db.flush()
    await db.refresh(db_obj)
    return db_obj

async def remove(db: AsyncSession, id: int) -> None:
    result = await db.execute(select(User).where(User.id == id))
    user = result.scalar_one_or_none()
    if user:
        await db.delete(user)
        await db.flush()
```

### Testing

```python
# tests/conftest.py
import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from app.db.base import Base
from app.main import app
from app.api.deps import get_db

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest.fixture
async def db_session():
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    TestSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with TestSessionLocal() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()

@pytest.fixture
async def client(db_session):
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        yield ac
    app.dependency_overrides.clear()

# tests/test_users.py
import pytest

@pytest.mark.asyncio
async def test_create_user(client):
    response = await client.post(
        "/api/v1/users",
        json={"email": "test@example.com", "name": "Test User", "password": "password123"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data

@pytest.mark.asyncio
async def test_get_user_not_found(client):
    response = await client.get("/api/v1/users/999")
    assert response.status_code == 404
```

### Project Structure

```
app/
├── api/
│   ├── deps.py           # Dependencies
│   └── v1/
│       ├── __init__.py
│       └── endpoints/
│           ├── auth.py
│           └── users.py
├── core/
│   ├── config.py         # Settings
│   └── security.py       # JWT, password hashing
├── crud/
│   └── user.py           # CRUD operations
├── db/
│   ├── base.py           # SQLAlchemy Base
│   └── session.py        # Database session
├── models/
│   └── user.py           # SQLAlchemy models
├── schemas/
│   └── user.py           # Pydantic schemas
└── main.py               # FastAPI app
tests/
├── conftest.py
└── test_users.py
```

## Parent & Related Skills

| Skill | Relationship |
|-------|--------------|
| **backend-developer** | Parent skill - invoke for general backend patterns |
| **database-architect** | For PostgreSQL schema design, SQLAlchemy models |
| **api-designer** | For REST API design, OpenAPI specification |
| **ml-engineer** | For ML model serving endpoints integration |

## Standards

- **Async everywhere**: Use async/await consistently
- **Pydantic v2**: Use v2 syntax and ConfigDict
- **Type hints**: Full type annotations
- **Dependency injection**: Use FastAPI's Depends
- **CRUD pattern**: Separate data access logic
- **OpenAPI docs**: Auto-generated and accurate

## Checklist

### Before Implementing
- [ ] Pydantic schemas defined
- [ ] Database models created
- [ ] CRUD operations implemented
- [ ] Dependencies configured

### Before Deploying
- [ ] Environment variables set
- [ ] Database migrations ready
- [ ] CORS configured
- [ ] Rate limiting enabled
- [ ] Tests passing

## Anti-Patterns to Avoid

1. **Sync in async**: Don't use sync database drivers
2. **Missing validation**: Always use Pydantic
3. **Business logic in endpoints**: Move to services
4. **Hardcoded config**: Use environment variables
5. **Missing error handling**: Handle all exceptions
6. **No pagination**: Always paginate list endpoints
