---
name: agency-database
description: Set up and maintain PostgreSQL database, SQLAlchemy async models, Alembic migrations, multi-tenant queries, and Redis caching for the Social Media Agency. Use when working with database schemas, migrations, ORM models, queries, or caching.
---

# Social Media Agency Data Layer

## Database Schema

```sql
-- db/init.sql

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS organization (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    domain VARCHAR(255),
    settings JSONB DEFAULT '{}',
    agentmail_inbox_id VARCHAR(255),
    agentmail_email VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    org_id UUID NOT NULL REFERENCES organization(id) ON DELETE CASCADE,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'viewer',   -- 'admin', 'manager', 'content_creator', 'viewer'
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS subscription (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    org_id UUID NOT NULL REFERENCES organization(id) ON DELETE CASCADE,
    stripe_customer_id VARCHAR(255),
    stripe_subscription_id VARCHAR(255),
    plan_tier VARCHAR(50) NOT NULL DEFAULT 'free',  -- 'free', 'starter', 'professional', 'enterprise'
    clients_limit INTEGER DEFAULT 3,
    posts_limit INTEGER DEFAULT 30,
    posts_used INTEGER DEFAULT 0,
    current_period_start TIMESTAMPTZ,
    current_period_end TIMESTAMPTZ,
    status VARCHAR(50) DEFAULT 'active',            -- 'active', 'past_due', 'cancelled'
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS client (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    org_id UUID NOT NULL REFERENCES organization(id) ON DELETE CASCADE,
    brand_name VARCHAR(255) NOT NULL,
    industry VARCHAR(100),
    description TEXT DEFAULT '',
    website_url VARCHAR(500),
    contact_email VARCHAR(255),
    logo_url TEXT,
    settings JSONB DEFAULT '{}',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS platform_account (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    client_id UUID NOT NULL REFERENCES client(id) ON DELETE CASCADE,
    org_id UUID NOT NULL REFERENCES organization(id),
    platform VARCHAR(50) NOT NULL,                  -- 'instagram', 'facebook', 'twitter', 'linkedin', 'tiktok'
    account_handle VARCHAR(255) NOT NULL,
    display_name VARCHAR(255),
    access_token_enc TEXT,                          -- encrypted OAuth token
    refresh_token_enc TEXT,
    token_expires_at TIMESTAMPTZ,
    followers_count INTEGER DEFAULT 0,
    status VARCHAR(30) DEFAULT 'connected',         -- 'connected', 'expired', 'disconnected'
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS campaign (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    client_id UUID NOT NULL REFERENCES client(id) ON DELETE CASCADE,
    org_id UUID NOT NULL REFERENCES organization(id),
    name VARCHAR(255) NOT NULL,
    objective TEXT DEFAULT '',
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    budget JSONB DEFAULT '{}',                      -- {"total": 5000, "spent": 1200, "currency": "USD"}
    status VARCHAR(30) DEFAULT 'planning',          -- 'planning', 'active', 'paused', 'completed', 'archived'
    tags JSONB DEFAULT '[]',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS content (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    campaign_id UUID REFERENCES campaign(id) ON DELETE SET NULL,
    client_id UUID NOT NULL REFERENCES client(id) ON DELETE CASCADE,
    org_id UUID NOT NULL REFERENCES organization(id),
    created_by UUID REFERENCES users(id),
    platform VARCHAR(50) NOT NULL,
    body TEXT DEFAULT '',
    hashtags JSONB DEFAULT '[]',
    media_urls JSONB DEFAULT '[]',
    ai_generated BOOLEAN DEFAULT FALSE,
    status VARCHAR(30) DEFAULT 'draft',             -- 'draft', 'pending_approval', 'approved', 'scheduled', 'published', 'rejected', 'failed'
    scheduled_at TIMESTAMPTZ,
    published_at TIMESTAMPTZ,
    external_post_id VARCHAR(255),                  -- ID on the target platform
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS approval (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    content_id UUID NOT NULL REFERENCES content(id) ON DELETE CASCADE,
    requested_by UUID NOT NULL REFERENCES users(id),
    reviewer_id UUID REFERENCES users(id),
    status VARCHAR(30) DEFAULT 'pending',           -- 'pending', 'approved', 'rejected'
    feedback TEXT,
    requested_at TIMESTAMPTZ DEFAULT NOW(),
    decided_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS asset (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    org_id UUID NOT NULL REFERENCES organization(id) ON DELETE CASCADE,
    client_id UUID REFERENCES client(id) ON DELETE SET NULL,
    uploaded_by UUID REFERENCES users(id),
    filename VARCHAR(500) NOT NULL,
    s3_key VARCHAR(1000) NOT NULL,
    mime_type VARCHAR(100) NOT NULL,
    size_bytes BIGINT DEFAULT 0,
    tags JSONB DEFAULT '[]',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS analytics_snapshot (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    platform_account_id UUID NOT NULL REFERENCES platform_account(id) ON DELETE CASCADE,
    content_id UUID REFERENCES content(id) ON DELETE SET NULL,
    date DATE NOT NULL,
    impressions INTEGER DEFAULT 0,
    reach INTEGER DEFAULT 0,
    engagement INTEGER DEFAULT 0,
    clicks INTEGER DEFAULT 0,
    shares INTEGER DEFAULT 0,
    comments INTEGER DEFAULT 0,
    likes INTEGER DEFAULT 0,
    followers_delta INTEGER DEFAULT 0,
    extra JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS client_report (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    client_id UUID NOT NULL REFERENCES client(id) ON DELETE CASCADE,
    org_id UUID NOT NULL REFERENCES organization(id),
    period_start DATE NOT NULL,
    period_end DATE NOT NULL,
    metrics_summary JSONB DEFAULT '{}',
    ai_insights TEXT,
    report_url TEXT,                                -- S3 URL for PDF
    sent_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_users_org ON users(org_id);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_client_org ON client(org_id);
CREATE INDEX idx_platform_account_client ON platform_account(client_id);
CREATE INDEX idx_platform_account_org ON platform_account(org_id);
CREATE INDEX idx_campaign_client ON campaign(client_id);
CREATE INDEX idx_campaign_org ON campaign(org_id);
CREATE INDEX idx_campaign_status ON campaign(status);
CREATE INDEX idx_content_client ON content(client_id);
CREATE INDEX idx_content_org ON content(org_id);
CREATE INDEX idx_content_campaign ON content(campaign_id);
CREATE INDEX idx_content_status ON content(status);
CREATE INDEX idx_content_scheduled ON content(scheduled_at);
CREATE INDEX idx_approval_content ON approval(content_id);
CREATE INDEX idx_approval_status ON approval(status);
CREATE INDEX idx_asset_org ON asset(org_id);
CREATE INDEX idx_asset_client ON asset(client_id);
CREATE INDEX idx_analytics_account ON analytics_snapshot(platform_account_id);
CREATE INDEX idx_analytics_date ON analytics_snapshot(date);
CREATE INDEX idx_analytics_content ON analytics_snapshot(content_id);
CREATE INDEX idx_report_client ON client_report(client_id);
CREATE INDEX idx_subscription_org ON subscription(org_id);
```

## Seed Data

```sql
-- db/seed.sql

INSERT INTO organization (id, name, domain) VALUES
('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', 'Demo Agency', 'demoagency.com');

INSERT INTO users (org_id, email, password_hash, full_name, role) VALUES
('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', 'admin@demoagency.com', '$2b$12$PLACEHOLDER_HASH', 'Admin User', 'admin'),
('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', 'creator@demoagency.com', '$2b$12$PLACEHOLDER_HASH', 'Content Creator', 'content_creator');

INSERT INTO subscription (org_id, plan_tier, clients_limit, posts_limit, status) VALUES
('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', 'professional', 25, 500, 'active');

INSERT INTO client (org_id, brand_name, industry, description) VALUES
('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', 'Sunrise Coffee', 'Food & Beverage',
 'Local artisan coffee roaster with 3 locations. Focus on organic, fair-trade beans and community engagement.');
```

## SQLAlchemy Async Setup

```python
# src/agency/models/database.py
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from agency.config import get_settings

def get_engine():
    settings = get_settings()
    return create_async_engine(settings.database_url, echo=settings.debug, pool_size=10)

def get_session_factory():
    return async_sessionmaker(get_engine(), class_=AsyncSession, expire_on_commit=False)
```

## SQLAlchemy ORM Models

```python
# src/agency/models/tables.py
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Text, Integer, BigInteger, Numeric, Date
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import DeclarativeBase, relationship

class Base(DeclarativeBase):
    pass

class Organization(Base):
    __tablename__ = "organization"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    domain = Column(String(255))
    settings = Column(JSONB, default={})
    agentmail_inbox_id = Column(String(255))
    agentmail_email = Column(String(255))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    org_id = Column(UUID(as_uuid=True), ForeignKey("organization.id"), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False, default="viewer")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

class Client(Base):
    __tablename__ = "client"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    org_id = Column(UUID(as_uuid=True), ForeignKey("organization.id"), nullable=False)
    brand_name = Column(String(255), nullable=False)
    industry = Column(String(100))
    description = Column(Text, default="")
    website_url = Column(String(500))
    contact_email = Column(String(255))
    logo_url = Column(Text)
    settings = Column(JSONB, default={})
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    platform_accounts = relationship("PlatformAccount", back_populates="client")
    campaigns = relationship("Campaign", back_populates="client")

class PlatformAccount(Base):
    __tablename__ = "platform_account"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    client_id = Column(UUID(as_uuid=True), ForeignKey("client.id"), nullable=False)
    org_id = Column(UUID(as_uuid=True), ForeignKey("organization.id"), nullable=False)
    platform = Column(String(50), nullable=False)
    account_handle = Column(String(255), nullable=False)
    display_name = Column(String(255))
    access_token_enc = Column(Text)
    refresh_token_enc = Column(Text)
    token_expires_at = Column(DateTime(timezone=True))
    followers_count = Column(Integer, default=0)
    status = Column(String(30), default="connected")
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    client = relationship("Client", back_populates="platform_accounts")

class Content(Base):
    __tablename__ = "content"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    campaign_id = Column(UUID(as_uuid=True), ForeignKey("campaign.id"), nullable=True)
    client_id = Column(UUID(as_uuid=True), ForeignKey("client.id"), nullable=False)
    org_id = Column(UUID(as_uuid=True), ForeignKey("organization.id"), nullable=False)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    platform = Column(String(50), nullable=False)
    body = Column(Text, default="")
    hashtags = Column(JSONB, default=[])
    media_urls = Column(JSONB, default=[])
    ai_generated = Column(Boolean, default=False)
    status = Column(String(30), default="draft")
    scheduled_at = Column(DateTime(timezone=True))
    published_at = Column(DateTime(timezone=True))
    external_post_id = Column(String(255))
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    approvals = relationship("Approval", back_populates="content")
```

## Alembic Setup

```bash
cd backend && alembic init alembic
alembic revision --autogenerate -m "description of change"
alembic upgrade head
alembic downgrade -1
```

Configure `alembic/env.py` to use async engine:

```python
# alembic/env.py (key parts)
from agency.models.tables import Base
from agency.config import get_settings

target_metadata = Base.metadata

def get_url():
    settings = get_settings()
    return settings.database_url
```

## Multi-Tenant Query Pattern

Every query on tenant-scoped data MUST filter by `org_id`.

```python
from sqlalchemy import select

# Correct: always filter by org_id
stmt = select(Client).where(
    Client.org_id == org_id,
    Client.is_active == True,
).order_by(Client.created_at.desc())

# WRONG: never query without org_id filter
stmt = select(Client).where(Client.is_active == True)  # TENANT LEAK!
```

## Avoiding N+1 Queries

```python
from sqlalchemy.orm import selectinload

# WRONG: N+1 pattern
for cid in client_ids:
    client = await db.execute(select(Client).where(Client.id == cid))

# CORRECT: Batch load
clients_result = await db.execute(
    select(Client).where(Client.id.in_(client_ids))
)
clients_map = {c.id: c for c in clients_result.scalars().all()}

# Load clients with their platform accounts in one query
stmt = select(Client).where(
    Client.org_id == org_id,
).options(selectinload(Client.platform_accounts))
```

## Redis Caching

```python
import redis.asyncio as redis
import json

class AgencyCache:
    def __init__(self, redis_url: str):
        self.redis = redis.from_url(redis_url)

    async def cache_analytics(self, client_id: str, period: str, data: dict):
        await self.redis.set(
            f"analytics:{client_id}:{period}",
            json.dumps(data),
            ex=900,  # 15 min TTL
        )

    async def get_analytics(self, client_id: str, period: str) -> dict | None:
        data = await self.redis.get(f"analytics:{client_id}:{period}")
        return json.loads(data) if data else None

    async def increment_posts_used(self, org_id: str) -> int:
        key = f"usage:{org_id}:posts"
        return await self.redis.incr(key)

    async def cache_content_preview(self, content_id: str, preview: dict):
        await self.redis.set(
            f"preview:{content_id}",
            json.dumps(preview),
            ex=300,  # 5 min TTL
        )
```

## Key Rules

1. **Always use UUID primary keys** — never auto-increment integers
2. **Every tenant-scoped table has `org_id`** — always filter by it
3. **Use JSONB** for flexible structured data (hashtags, media_urls, budget, settings)
4. **Always add indexes** on FK columns and columns used in WHERE
5. **Always include `created_at`** timestamps
6. **Use parameterized queries** — never string interpolation
7. **Alembic for all schema changes** — never modify DB manually in production
8. **Seed data must be realistic** — use proper UUIDs, real-looking data
9. **Redis for ephemeral state** — analytics cache, usage counters, content previews
10. **Never query in a loop** — use `.in_()` batch queries or `selectinload()`/`joinedload()` to avoid N+1
11. **Encrypt OAuth tokens** — `access_token_enc` and `refresh_token_enc` are encrypted at rest
