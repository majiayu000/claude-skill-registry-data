---
name: agency-backend
description: Build and maintain the Social Media Agency FastAPI backend with production best practices. Use when creating API endpoints, services, middleware, Pydantic schemas, or backend configuration.
---

# Social Media Agency FastAPI Backend

## Application Factory

Always use the factory pattern. Never create `app = FastAPI()` at module level.

```python
# src/agency/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from agency.config import get_settings
from agency.routers import (
    health, auth, organizations, clients, campaigns,
    content, calendar, platforms, approvals, analytics,
    assets, reports, billing,
)
from agency.middleware.tenant import TenantMiddleware

def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title="Social Media Agency API",
        version="1.0.0",
        docs_url="/api/docs" if settings.debug else None,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
        allow_headers=["Authorization", "Content-Type"],
    )
    app.add_middleware(TenantMiddleware)

    for router in [
        health, auth, organizations, clients, campaigns,
        content, calendar, platforms, approvals, analytics,
        assets, reports, billing,
    ]:
        app.include_router(router.router, prefix="/api/v1")

    return app

app = create_app()
```

## Configuration

```python
# src/agency/config.py
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    app_env: str = "dev"
    debug: bool = False
    database_url: str
    redis_url: str = "redis://localhost:6379"
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    stripe_secret_key: str = ""
    stripe_webhook_secret: str = ""
    s3_bucket_name: str = ""
    aws_access_key_id: str = ""
    aws_secret_access_key: str = ""
    agentmail_api_key: str = ""
    agentmail_default_domain: str = ""
    cors_origins: list[str] = ["http://localhost:3000"]

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}

@lru_cache
def get_settings() -> Settings:
    return Settings()
```

## Router Pattern

Domain logic lives in services, not routers. Routers are thin wrappers.

```python
# src/agency/routers/clients.py
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query
from agency.dependencies import get_current_user, get_db, get_org_id
from agency.models.schemas import (
    ClientCreateRequest, ClientResponse, ClientListResponse,
)
from agency.services.content_service import ContentService

router = APIRouter(prefix="/clients", tags=["Clients"])

@router.post("", response_model=ClientResponse, status_code=status.HTTP_201_CREATED)
async def create_client(
    request: ClientCreateRequest,
    user=Depends(get_current_user),
    db=Depends(get_db),
    org_id: UUID = Depends(get_org_id),
):
    service = ContentService(db)
    return await service.create_client(org_id=org_id, created_by=user["sub"], data=request)

@router.get("", response_model=ClientListResponse)
async def list_clients(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    user=Depends(get_current_user),
    db=Depends(get_db),
    org_id: UUID = Depends(get_org_id),
):
    service = ContentService(db)
    return await service.list_clients(org_id=org_id, page=page, per_page=per_page)

@router.get("/{client_id}", response_model=ClientResponse)
async def get_client(
    client_id: UUID,
    user=Depends(get_current_user),
    db=Depends(get_db),
    org_id: UUID = Depends(get_org_id),
):
    service = ContentService(db)
    client = await service.get_client(org_id=org_id, client_id=client_id)
    if not client:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Client not found")
    return client
```

## Dependencies (DI)

```python
# src/agency/dependencies.py
from uuid import UUID
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from agency.config import get_settings
from agency.models.database import get_session_factory

security = HTTPBearer()

async def get_db():
    factory = get_session_factory()
    async with factory() as session:
        yield session

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    settings = get_settings()
    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm],
        )
        return payload
    except JWTError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid token")

async def get_org_id(request: Request) -> UUID:
    org_id = getattr(request.state, "org_id", None)
    if not org_id:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Organization context required")
    return org_id

def require_role(*allowed_roles: str):
    async def checker(user: dict = Depends(get_current_user)):
        if user.get("role") not in allowed_roles:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Insufficient permissions")
        return user
    return checker
```

## Pydantic Schemas

```python
# src/agency/models/schemas.py
from uuid import UUID
from datetime import datetime, date
from pydantic import BaseModel, Field, EmailStr
from enum import Enum

class ContentStatus(str, Enum):
    DRAFT = "draft"
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    SCHEDULED = "scheduled"
    PUBLISHED = "published"
    REJECTED = "rejected"

class CampaignStatus(str, Enum):
    PLANNING = "planning"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    ARCHIVED = "archived"

class ClientCreateRequest(BaseModel):
    brand_name: str = Field(..., min_length=2, max_length=200)
    industry: str = Field(..., min_length=2, max_length=100)
    description: str = Field(default="")
    website_url: str | None = None
    contact_email: EmailStr | None = None

class ClientResponse(BaseModel):
    id: UUID
    org_id: UUID
    brand_name: str
    industry: str
    description: str
    logo_url: str | None
    website_url: str | None
    contact_email: str | None
    platform_accounts_count: int = 0
    active_campaigns_count: int = 0
    created_at: datetime

class ClientListResponse(BaseModel):
    items: list[ClientResponse]
    total: int
    page: int
    per_page: int

class CampaignCreateRequest(BaseModel):
    client_id: UUID
    name: str = Field(..., min_length=3, max_length=200)
    objective: str = Field(default="")
    start_date: date
    end_date: date
    budget: dict = Field(default_factory=dict)

class ContentCreateRequest(BaseModel):
    campaign_id: UUID | None = None
    client_id: UUID
    platform: str = Field(..., min_length=1)
    body: str = Field(default="")
    hashtags: list[str] = Field(default_factory=list)
    media_urls: list[str] = Field(default_factory=list)
    scheduled_at: datetime | None = None

class ContentResponse(BaseModel):
    id: UUID
    campaign_id: UUID | None
    client_id: UUID
    org_id: UUID
    platform: str
    body: str
    hashtags: list[str]
    media_urls: list[str]
    status: ContentStatus
    scheduled_at: datetime | None
    published_at: datetime | None
    created_at: datetime
    approval_status: str | None = None

class ContentListResponse(BaseModel):
    items: list[ContentResponse]
    total: int
    page: int
    per_page: int

class AnalyticsResponse(BaseModel):
    impressions: int
    reach: int
    engagement: int
    clicks: int
    followers_delta: int
    period_start: date
    period_end: date
    breakdown: list[dict] = Field(default_factory=list)
```

## Error Response Convention

```python
raise HTTPException(status.HTTP_400_BAD_REQUEST, "Validation failed: ...")
raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid token")
raise HTTPException(status.HTTP_403_FORBIDDEN, "Insufficient permissions")
raise HTTPException(status.HTTP_404_NOT_FOUND, "Resource not found")
raise HTTPException(status.HTTP_429_TOO_MANY_REQUESTS, "Rate limit exceeded")
```

FastAPI serializes this as `{"detail": "message"}`.

## Health Checks

```python
# src/agency/routers/health.py
from fastapi import APIRouter, Depends
from agency.dependencies import get_db

router = APIRouter(prefix="/health", tags=["Health"])

@router.get("")
async def health():
    return {"status": "healthy", "service": "agency-api"}

@router.get("/db")
async def health_db(db=Depends(get_db)):
    await db.execute("SELECT 1")
    return {"status": "healthy", "database": "connected"}
```

## Content Generation Endpoint

```python
# src/agency/routers/content.py (AI-powered content creation)
@router.post("/generate", response_model=ContentGenerateResponse)
async def generate_content(
    request: ContentGenerateRequest,
    user=Depends(get_current_user),
    db=Depends(get_db),
    org_id: UUID = Depends(get_org_id),
):
    service = ContentService(db)
    return await service.generate_content(
        org_id=org_id,
        client_id=request.client_id,
        platform=request.platform,
        topic=request.topic,
        tone=request.tone,
        content_type=request.content_type,
    )
```

## Background Tasks (Celery)

```python
# src/agency/workers/publishing_worker.py
from celery import Celery
from agency.config import get_settings

settings = get_settings()
celery_app = Celery("agency", broker=settings.redis_url)

@celery_app.task
def publish_scheduled_content(content_id: str):
    """Publish content to the target platform at the scheduled time."""
    ...

@celery_app.task
def sync_platform_analytics(platform_account_id: str):
    """Pull latest analytics from the platform API."""
    ...

@celery_app.task
def generate_client_report(client_id: str, period_start: str, period_end: str):
    """Generate and email a performance report for a client."""
    ...
```

## Checklist for New Endpoints

1. Create or add to router in `src/agency/routers/`
2. Choose auth level: authenticated / admin-only / manager+
3. Create Pydantic request/response schemas in `models/schemas.py`
4. Add domain logic to a service in `services/`
5. Always filter by `org_id` for tenant isolation
6. Add rate limiting for public-facing endpoints
7. Log with structlog — never `print()`
8. Write tests in `tests/`

## Key Rules

1. **Never hardcode secrets** — all secrets via `Settings`
2. **Always version API routes** — prefix with `/api/v1/`
3. **Always validate inputs** — Pydantic `Field` constraints
4. **Always use async** — `asyncpg`, `httpx.AsyncClient`
5. **Domain logic in services** — routers are thin wrappers
6. **Multi-tenant isolation** — every query filters by `org_id`
7. **Log with structlog** — never `print()`
8. **Content goes through approval** — enforce status transitions
9. **Platform integrations are pluggable** — use the `PlatformConnector` interface
10. **All dashboard endpoints require JWT** — always validate token
