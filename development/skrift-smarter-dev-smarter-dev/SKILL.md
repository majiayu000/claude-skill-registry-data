---
name: skrift
description: "Help working with Skrift CMS codebases - a Python async CMS built on Litestar with WordPress-style conventions. Use for creating controllers, models, hooks, pages, and templates."
---

# Skrift CMS Development Guide

Skrift is a lightweight async Python CMS built on Litestar, featuring WordPress-style template resolution, a hook/filter extensibility system, and SQLAlchemy async database access.

## Current Project State

**Configuration:**
!`cat app.yaml 2>/dev/null || echo "No app.yaml found"`

**Controllers:**
!`ls skrift/controllers/*.py 2>/dev/null | head -10`

**Models:**
!`ls skrift/db/models/*.py 2>/dev/null | head -10`

**Services:**
!`ls skrift/db/services/*.py 2>/dev/null | head -10`

**Templates:**
!`ls templates/*.html 2>/dev/null | head -10 || echo "No custom templates"`

## Quick Reference

### Core Architecture

- **Framework**: Litestar (async Python web framework)
- **Database**: SQLAlchemy async with Advanced Alchemy
- **Templates**: Jinja2 with WordPress-style template hierarchy + optional themes (see `/skrift-theming`)
- **Config**: YAML (app.yaml) + environment variables (.env)
- **Auth**: OAuth providers + role-based permissions (see `/skrift-auth`)
- **Forms**: Pydantic-backed with CSRF (see `/skrift-forms`)
- **Hooks**: WordPress-style extensibility (see `/skrift-hooks`)
- **Notifications**: Real-time SSE with pluggable backends (see `/skrift-notifications`)
- **Observability**: Optional Logfire tracing and structured logging (see `/skrift-observability`)
- **OAuth2 Server**: Hub/spoke identity federation (see `/skrift-oauth2`)

### AppDispatcher Pattern

```
                    ┌─────────────────────────────┐
                    │      AppDispatcher          │
                    │  (skrift/asgi.py)           │
                    └─────────────┬───────────────┘
                                  │
              ┌───────────────────┼───────────────────┐
              │                   │                   │
              ▼                   ▼                   ▼
     ┌────────────────┐   ┌────────────┐   ┌────────────────┐
     │   Setup App    │   │  /static   │   │   Main App     │
     │  (/setup/*)    │   │   Files    │   │  (everything)  │
     └────────────────┘   └────────────┘   └────────────────┘
```

- `setup_locked=False`: /setup/* routes active, checks DB for setup completion
- `setup_locked=True`: All traffic goes to main app, /setup/* returns 404
- Main app is lazily created after setup completes (no restart needed)
- Entry point: `skrift.asgi:app` (created by `create_dispatcher()`)

### Key Files

| File | Purpose |
|------|---------|
| `skrift/asgi.py` | AppDispatcher, app creation, middleware loading |
| `skrift/config.py` | Settings management, YAML config loading |
| `skrift/cli.py` | CLI commands (serve, secret, db) |
| `skrift/middleware/` | Security headers middleware |
| `skrift/lib/hooks.py` | WordPress-like hook/filter system |
| `skrift/lib/template.py` | Template resolution with fallbacks and theme support |
| `skrift/lib/theme.py` | Theme discovery, metadata parsing |
| `skrift/db/base.py` | SQLAlchemy Base class (UUIDAuditBase) |
| `skrift/forms/` | Form system (CSRF, validation, rendering) |
| `skrift/auth/` | Guards, roles, permissions |
| `skrift/lib/notifications.py` | Real-time notification service (SSE) |
| `skrift/lib/notification_backends.py` | Pluggable backends (InMemory, Redis, PgNotify) |
| `skrift/lib/observability.py` | Logfire observability facade (tracing, logging) |
| `skrift/db/models/notification.py` | StoredNotification model for DB-backed backends |

### Configuration System

```
.env (loaded early) → app.yaml (with $VAR interpolation) → Settings (Pydantic)
```

Environment-specific: `app.yaml` (production), `app.dev.yaml` (development), `app.test.yaml` (testing). Set via `SKRIFT_ENV`.

```yaml
db:
  url: $DATABASE_URL
  pool_size: 5
  echo: false
  schema: myschema  # optional; PostgreSQL only — prefixes all tables

auth:
  redirect_base_url: "https://example.com"
  providers:
    google:
      client_id: $GOOGLE_CLIENT_ID
      client_secret: $GOOGLE_CLIENT_SECRET
      scopes: ["openid", "email", "profile"]

session:
  cookie_domain: null

theme: my-theme  # default theme (overridden by admin UI)

controllers:
  - skrift.controllers.auth:AuthController
  - skrift.controllers.web:WebController

redis:
  url: $REDIS_URL
  prefix: "myapp"

notifications:
  backend: ""  # empty = InMemoryBackend; or "module:ClassName"

logfire:
  enabled: true
  service_name: my-site
  console: true  # prints spans to console

security_headers:
  content_security_policy: "default-src 'self'"

middleware:
  - myapp.middleware:create_logging_middleware
```

### CLI Commands

```bash
skrift serve --reload --port 8080
skrift serve --subdomain blog --port 8081  # serve single subdomain site
skrift secret --write .env
skrift db upgrade head
skrift db downgrade -1
skrift db revision -m "desc" --autogenerate
```

## Database Layer

All models inherit from `skrift.db.base.Base` (provides `id` UUID, `created_at`, `updated_at`):

```python
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column
from skrift.db.base import Base

class MyModel(Base):
    __tablename__ = "my_models"
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
```

### Core Models

| Model | Table | Purpose |
|-------|-------|---------|
| `User` | `users` | User accounts |
| `OAuthAccount` | `oauth_accounts` | Linked OAuth providers (`access_token`, `refresh_token`) |
| `Role` | `roles` | Permission roles |
| `Page` | `pages` | Content pages |
| `PageRevision` | `page_revisions` | Content history |
| `Setting` | `settings` | Key-value site settings |
| `StoredNotification` | `stored_notifications` | Persistent notifications with `mode` column (Redis/PgNotify backends) |

Sessions injected via `db_session: AsyncSession` parameter in handlers.

### Content Negotiation

Page views support `Accept: text/markdown` — returns raw `page.content` instead of rendered HTML. Works for all page types (WebController and page type factory routes).

## Creating a Controller

```python
from litestar import Controller, get, post
from litestar.response import Template as TemplateResponse
from sqlalchemy.ext.asyncio import AsyncSession

class MyController(Controller):
    path = "/my-path"

    @get("/")
    async def list_items(self, db_session: AsyncSession) -> TemplateResponse:
        items = await item_service.list_items(db_session)
        return TemplateResponse("items/list.html", context={"items": items})
```

Register in `app.yaml`:
```yaml
controllers:
  - myapp.controllers:MyController
```

## Creating a Service

```python
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

async def get_by_id(db_session: AsyncSession, item_id: UUID) -> MyModel | None:
    result = await db_session.execute(select(MyModel).where(MyModel.id == item_id))
    return result.scalar_one_or_none()

async def create_item(db_session: AsyncSession, name: str) -> MyModel:
    item = MyModel(name=name)
    db_session.add(item)
    await db_session.commit()
    await db_session.refresh(item)
    return item
```

## Template Resolution

WordPress-style hierarchy with fallbacks and optional theme support:

```python
from skrift.lib.template import Template

# Tries: page-about.html -> page.html
template = Template("page", "about")

# Tries: post-news-2024.html -> post-news.html -> post.html
template = Template("post", "news", "2024")

# Without theme
return template.render(TEMPLATE_DIR, page=page)

# With theme (searches theme dirs first)
return template.render(TEMPLATE_DIR, theme_name="my-theme", page=page)
```

Search order (with active theme):
1. `themes/<active>/templates/` (active theme)
2. `./templates/` (project root — user overrides)
3. `skrift/templates/` (package — defaults)

Template globals: `now()`, `site_name()`, `site_tagline()`, `site_copyright_holder()`, `site_copyright_start_year()`, `active_theme()`, `themes_available()`. Filter: `markdown`.

For full theming details, see `/skrift-theming`.

## Middleware

```python
from litestar.middleware import AbstractMiddleware

class LoggingMiddleware(AbstractMiddleware):
    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            print(f"Request: {scope['method']} {scope['path']}")
        await self.app(scope, receive, send)

def create_logging_middleware(app):
    return LoggingMiddleware(app=app)
```

Register in `app.yaml`:
```yaml
middleware:
  - myapp.middleware:create_logging_middleware
  - factory: myapp.middleware:create_rate_limit
    kwargs:
      requests_per_minute: 100
```

## Security

`skrift/middleware/security.py` — ASGI middleware injecting CSP, HSTS, X-Frame-Options, etc. Configured via `SecurityHeadersConfig`. Pre-encoded at creation time. HSTS excluded in debug mode.

Static files: `/static/` with same priority as templates (project root, then package).

## Error Handling

Custom exception handlers in `skrift/lib/exceptions.py`. Templates: `error.html`, `error-404.html`, `error-500.html`.

## Testing

```python
from litestar.testing import TestClient

async def test_list_items(client, db_session):
    item = await item_service.create(db_session, name="Test")
    response = client.get("/items")
    assert response.status_code == 200
    assert "Test" in response.text
```

## Related Skills

For deep-dive guidance on specific subsystems:
- **`/skrift-hooks`** — Hook/filter extensibility, custom hook points, built-in hooks
- **`/skrift-forms`** — Form system, CSRF, field customization, template rendering
- **`/skrift-auth`** — OAuth flow, guard system, roles, permissions
- **`/skrift-theming`** — Theme discovery, template/static resolution, per-request switching, RESOLVE_THEME hook
- **`/skrift-notifications`** — SSE protocol, pluggable backends, group keys, dismiss patterns
- **`/skrift-observability`** — Logfire integration, structured tracing, instrumentation
- **`/skrift-oauth2`** — OAuth2 Authorization Server, hub/spoke identity federation, Skrift provider
