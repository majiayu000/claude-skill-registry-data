---
name: fastapi
description: FastAPI patterns, Pydantic v2 integration, dependency injection, middleware, background tasks, and production deployment
layer: domain
category: backend
triggers:
  - "fastapi"
  - "fast api"
  - "pydantic"
  - "uvicorn"
  - "starlette"
  - "python api"
inputs:
  - "API design requirements"
  - "Authentication/authorization needs"
  - "Performance targets"
outputs:
  - "FastAPI route implementations"
  - "Dependency injection patterns"
  - "Production deployment configurations"
linksTo:
  - python
  - postgresql
  - mongodb
  - redis
  - websockets
  - microservices
linkedFrom:
  - error-handling
  - authentication
  - testing
preferredNextSkills:
  - postgresql
  - redis
  - python
fallbackSkills:
  - django
  - nodejs
riskLevel: low
memoryReadPolicy: selective
memoryWritePolicy: none
sideEffects: []
---

# FastAPI Domain Skill

## Purpose

Provide expert-level guidance on building production-grade APIs with FastAPI, including Pydantic v2 integration, dependency injection patterns, middleware, background tasks, WebSocket support, and deployment strategies.

## Key Patterns

### 1. Application Factory Pattern

```python
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Manage application lifecycle: startup and shutdown."""
    # Startup
    app.state.db_pool = await create_db_pool()
    app.state.redis = await create_redis_client()
    yield
    # Shutdown
    await app.state.db_pool.close()
    await app.state.redis.close()

def create_app() -> FastAPI:
    app = FastAPI(
        title="My API",
        version="1.0.0",
        lifespan=lifespan,
        docs_url="/docs" if settings.ENVIRONMENT != "production" else None,
        redoc_url=None,
    )

    # Middleware (order matters -- last added = first executed)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register routers
    app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
    app.include_router(items.router, prefix="/api/v1/items", tags=["items"])

    return app

app = create_app()
```

### 2. Dependency Injection

```python
from typing import Annotated
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# Database session dependency
async def get_db(request: Request) -> AsyncGenerator[AsyncSession, None]:
    async with request.app.state.db_pool() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise

# Authentication dependency
security = HTTPBearer()

async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> User:
    token = credentials.credentials
    payload = verify_jwt(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
    user = await db.get(User, payload["sub"])
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return user

# Role-based access control
def require_role(*roles: str):
    async def _check_role(
        user: Annotated[User, Depends(get_current_user)],
    ) -> User:
        if user.role not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        return user
    return _check_role

# Type aliases for cleaner signatures
DB = Annotated[AsyncSession, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_user)]
AdminUser = Annotated[User, Depends(require_role("admin"))]
```

### 3. Pydantic v2 Schemas

```python
from pydantic import BaseModel, Field, ConfigDict, field_validator
from datetime import datetime

# Base schema with common config
class BaseSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,  # ORM mode
        str_strip_whitespace=True,
        validate_default=True,
    )

# Request schemas
class CreateItemRequest(BaseSchema):
    name: str = Field(..., min_length=1, max_length=200)
    description: str | None = Field(None, max_length=2000)
    price: int = Field(..., gt=0, description="Price in cents")
    tags: list[str] = Field(default_factory=list, max_length=10)

    @field_validator("tags")
    @classmethod
    def normalize_tags(cls, v: list[str]) -> list[str]:
        return [tag.lower().strip() for tag in v if tag.strip()]

class UpdateItemRequest(BaseSchema):
    name: str | None = Field(None, min_length=1, max_length=200)
    description: str | None = None
    price: int | None = Field(None, gt=0)

# Response schemas
class ItemResponse(BaseSchema):
    id: str
    name: str
    description: str | None
    price: int
    tags: list[str]
    created_at: datetime
    updated_at: datetime

class PaginatedResponse[T](BaseSchema):
    items: list[T]
    total: int
    page: int
    per_page: int
    pages: int
```

### 4. Route Handlers

```python
from fastapi import APIRouter, Query, Path, status
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("", response_model=PaginatedResponse[ItemResponse])
async def list_items(
    db: DB,
    user: CurrentUser,
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    search: str | None = Query(None, min_length=1, max_length=100),
) -> PaginatedResponse[ItemResponse]:
    """List items with pagination and optional search."""
    query = select(Item).where(Item.owner_id == user.id)

    if search:
        query = query.where(Item.name.ilike(f"%{search}%"))

    total = await db.scalar(select(func.count()).select_from(query.subquery()))
    items = await db.scalars(
        query.offset((page - 1) * per_page).limit(per_page)
    )

    return PaginatedResponse(
        items=[ItemResponse.model_validate(i) for i in items],
        total=total,
        page=page,
        per_page=per_page,
        pages=(total + per_page - 1) // per_page,
    )

@router.post("", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def create_item(
    body: CreateItemRequest,
    db: DB,
    user: CurrentUser,
) -> ItemResponse:
    """Create a new item."""
    item = Item(**body.model_dump(), owner_id=user.id)
    db.add(item)
    await db.flush()
    return ItemResponse.model_validate(item)

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(
    item_id: str = Path(...),
    db: DB = ...,
    user: CurrentUser = ...,
) -> None:
    """Delete an item by ID."""
    item = await db.get(Item, item_id)
    if item is None or item.owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    await db.delete(item)
```

### 5. Exception Handling

```python
from fastapi import Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError

class AppError(Exception):
    def __init__(self, message: str, code: str, status: int = 400) -> None:
        self.message = message
        self.code = code
        self.status = status

@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status,
        content={
            "error": {"code": exc.code, "message": exc.message}
        },
    )

@app.exception_handler(ValidationError)
async def validation_error_handler(request: Request, exc: ValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "details": exc.errors(include_url=False),
            }
        },
    )
```

### 6. Background Tasks and Rate Limiting

```python
from fastapi import BackgroundTasks
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@router.post("/send-email")
@limiter.limit("5/minute")
async def send_email(
    request: Request,
    body: SendEmailRequest,
    background_tasks: BackgroundTasks,
    user: CurrentUser,
) -> dict[str, str]:
    background_tasks.add_task(send_email_task, body.to, body.subject, body.body)
    return {"status": "queued"}
```

## Best Practices

1. **Use `Annotated` types** for dependency injection -- cleaner signatures
2. **Use `lifespan`** context manager instead of deprecated `on_startup`/`on_shutdown`
3. **Validate all inputs** with Pydantic -- never trust client data
4. **Use `status` constants** from `fastapi` instead of magic numbers
5. **Version your API** with URL prefixes (`/api/v1/`)
6. **Return proper HTTP status codes** -- 201 for creation, 204 for deletion
7. **Use `response_model`** to control serialization and filter sensitive fields
8. **Configure CORS** properly -- never use `allow_origins=["*"]` in production
9. **Disable `/docs` in production** unless behind authentication
10. **Use connection pooling** for all external services

## Common Pitfalls

| Pitfall | Impact | Fix |
|---------|--------|-----|
| Not using `async def` for I/O routes | Thread pool exhaustion | Always `async def` for DB/HTTP calls |
| Blocking calls in async handlers | Event loop blocked | Use `asyncio.to_thread()` for sync libs |
| Missing `await` on async operations | Returns coroutine instead of result | Enable `ruff` rule for unawaited coroutines |
| Not closing DB sessions on error | Connection leaks | Use `try/finally` or dependency teardown |
| Exposing internal errors to clients | Security risk | Custom exception handlers, never expose tracebacks |
| Circular imports in large apps | ImportError | Use application factory pattern, lazy imports |

## Production Deployment

```bash
# Uvicorn with proper settings
uvicorn app.main:app \
  --host 0.0.0.0 \
  --port 8000 \
  --workers 4 \
  --loop uvloop \
  --http httptools \
  --log-level info \
  --access-log \
  --proxy-headers \
  --forwarded-allow-ips='*'
```
