---
name: api-design-patterns
description: REST API design — versioning, pagination, error responses, idempotency, rate limiting, OpenAPI spec
triggers:
  - api design
  - rest api best practice
  - api versioning
  - api pagination
  - api error response
  - api rate limiting
  - openapi spec
  - api idempotency
  - http api patterns
  - fastapi design
do_not_use_for:
  - API security — use api-security-gate
  - GraphQL — use graphql-patterns
  - WebSockets — use websocket-patterns
see_also:
  - error-handling-patterns
  - type-safety-patterns
  - database-patterns
---

# API Design Patterns

## Versioning

```python
# URL versioning — simplest, most visible
# /v1/users, /v2/users

from fastapi import APIRouter, FastAPI

app = FastAPI()
v1 = APIRouter(prefix="/v1")
v2 = APIRouter(prefix="/v2")

@v1.get("/users/{user_id}")
async def get_user_v1(user_id: str) -> UserV1Response: ...

@v2.get("/users/{user_id}")
async def get_user_v2(user_id: str) -> UserV2Response: ...

app.include_router(v1)
app.include_router(v2)
```

## Consistent Error Response Shape

```python
from pydantic import BaseModel
from fastapi import Request
from fastapi.responses import JSONResponse
from typing import Any

class ErrorResponse(BaseModel):
    error: str           # machine-readable code
    message: str         # human-readable
    detail: Any = None   # additional context
    request_id: str = "" # for support

# Global exception handler
@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    status_map = {
        "NOT_FOUND": 404,
        "VALIDATION_ERROR": 422,
        "UNAUTHORIZED": 401,
        "FORBIDDEN": 403,
        "CONFLICT": 409,
    }
    return JSONResponse(
        status_code=status_map.get(exc.code, 500),
        content=ErrorResponse(
            error=exc.code,
            message=str(exc),
            request_id=request.headers.get("X-Request-ID", ""),
        ).model_dump(),
    )
```

## Pagination: Cursor-Based

```python
from pydantic import BaseModel
from typing import Generic, TypeVar

T = TypeVar("T")

class PageResponse(BaseModel, Generic[T]):
    data: list[T]
    next_cursor: str | None      # None = no more pages
    total: int | None = None     # optional, expensive to compute

@v1.get("/posts", response_model=PageResponse[PostResponse])
async def list_posts(
    cursor: str | None = None,
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
) -> PageResponse[PostResponse]:
    posts = get_posts_after_cursor(db, cursor, limit + 1)
    has_more = len(posts) > limit
    return PageResponse(
        data=[PostResponse.from_orm(p) for p in posts[:limit]],
        next_cursor=encode_cursor(posts[limit - 1]) if has_more else None,
    )
```

## Idempotency Keys

```python
from fastapi import Header
from typing import Annotated

@v1.post("/charges", response_model=ChargeResponse, status_code=201)
async def create_charge(
    body: CreateChargeRequest,
    idempotency_key: Annotated[str | None, Header(alias="Idempotency-Key")] = None,
    db: Session = Depends(get_db),
) -> ChargeResponse:
    if idempotency_key:
        # Return cached result if key already used
        cached = get_cached_response(db, idempotency_key)
        if cached:
            return cached

    charge = process_charge(body)

    if idempotency_key:
        cache_response(db, idempotency_key, charge, ttl=86400)

    return charge
```

## Rate Limiting

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@v1.post("/auth/login")
@limiter.limit("5/minute")
async def login(request: Request, body: LoginRequest) -> TokenResponse: ...

@v1.get("/search")
@limiter.limit("100/minute;1000/hour")
async def search(request: Request, q: str) -> SearchResponse: ...
```

## Request/Response DTOs (separate from DB models)

```python
from pydantic import BaseModel, Field
from datetime import datetime

# Never expose ORM model directly — use DTO
class UserCreateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: str = Field(pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")
    password: str = Field(min_length=8)

class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    created_at: datetime
    # ← no password_hash, no internal flags

    model_config = {"from_attributes": True}  # from ORM model

@v1.post("/users", response_model=UserResponse, status_code=201)
async def create_user(body: UserCreateRequest) -> UserResponse:
    user = User(name=body.name, email=body.email, hashed_pw=hash(body.password))
    db.add(user)
    db.commit()
    return UserResponse.model_validate(user)
```

## OpenAPI Docs Enrichment

```python
@v1.post(
    "/orders",
    response_model=OrderResponse,
    status_code=201,
    summary="Create a new order",
    description="Creates an order with line items. Idempotent via Idempotency-Key header.",
    responses={
        201: {"description": "Order created"},
        409: {"description": "Duplicate idempotency key"},
        422: {"description": "Validation error"},
    },
    tags=["orders"],
)
async def create_order(body: CreateOrderRequest) -> OrderResponse: ...
```

## Anti-Fake-Pass Checks

- URL versioning `/v1/` requires maintaining both versions simultaneously during migration
- Cursor-based pagination: cursor must be opaque (base64 encoded ID) — never expose raw ID as cursor
- `status_code=201` on POST — don't return 200 for resource creation
- DTO != ORM model — never return the ORM object directly (leaks all fields)
- Rate limiting by IP fails behind load balancer — use `X-Forwarded-For` header as key
- `Idempotency-Key` TTL must match client retry window (24h is standard)
