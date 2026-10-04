---
name: agency-project
description: Provides architecture knowledge for the Social Media Agency SaaS platform. Use when exploring the codebase, adding features, debugging, or asking about project structure, tech stack, conventions, database schema, or design system.
---

# Social Media Agency — Project Architecture

## Project Context

Social Media Agency is a full-service SaaS platform for social media agencies. Agencies subscribe and manage multiple client accounts, plan campaigns, create AI-powered content, schedule posts across platforms, run approval workflows, and track analytics — all from a single dashboard. The platform is platform-agnostic by design: social media integrations are abstracted so new platforms can be added without changing the core. Sold as "Agency as a Service" with tiered subscriptions via Stripe.

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend Framework | FastAPI (Python 3.12+) |
| Package Manager | uv (lockfile: uv.lock) |
| Task Runner | Nox + nox-uv |
| Linter / Formatter | Ruff |
| Type Checker | mypy (strict mode) |
| Frontend Framework | Next.js 14 (App Router), React 18, TypeScript |
| Database | PostgreSQL 16, SQLAlchemy 2.0 (async), Alembic |
| Cache / Queue | Redis, Celery |
| Auth | JWT (python-jose) + OAuth2 (Google SSO) |
| UI Components | shadcn/ui, Radix UI, Tailwind CSS |
| State Management | Zustand, TanStack Query |
| Charts | Recharts |
| LLM | OpenAI GPT-4o (primary), Claude (fallback) |
| Image Generation | OpenAI DALL-E 3 |
| Billing | Stripe (subscriptions + usage metering) |
| Media Storage | AWS S3 / MinIO |
| Email | AgentMail (client comms + outreach) |
| Deployment | Docker, Docker Compose, GitHub Actions |
| Monitoring | Sentry, Prometheus, Grafana |

## Project Structure

```
social-media-agency/
├── backend/
│   ├── src/agency/                    # Python package (src-layout)
│   │   ├── __init__.py
│   │   ├── main.py                    # FastAPI app factory
│   │   ├── config.py                  # Pydantic Settings
│   │   ├── dependencies.py            # DI: DB, current_user, org
│   │   ├── routers/
│   │   │   ├── health.py
│   │   │   ├── auth.py
│   │   │   ├── organizations.py
│   │   │   ├── clients.py
│   │   │   ├── campaigns.py
│   │   │   ├── content.py
│   │   │   ├── calendar.py
│   │   │   ├── platforms.py
│   │   │   ├── approvals.py
│   │   │   ├── analytics.py
│   │   │   ├── assets.py
│   │   │   ├── reports.py
│   │   │   └── billing.py
│   │   ├── services/
│   │   │   ├── ai_engine.py           # LLM content generation
│   │   │   ├── content_service.py
│   │   │   ├── campaign_service.py
│   │   │   ├── scheduling_service.py
│   │   │   ├── analytics_service.py
│   │   │   ├── platform_service.py    # Platform integration abstraction
│   │   │   ├── approval_service.py
│   │   │   ├── asset_service.py
│   │   │   └── billing_service.py
│   │   ├── models/
│   │   │   ├── database.py            # SQLAlchemy async engine
│   │   │   ├── tables.py             # ORM models
│   │   │   └── schemas.py            # Pydantic request/response
│   │   ├── middleware/
│   │   │   ├── tenant.py              # Multi-tenant context
│   │   │   └── auth.py
│   │   ├── workers/                   # Celery tasks
│   │   │   ├── publishing_worker.py   # Post publishing
│   │   │   ├── analytics_worker.py    # Metrics sync
│   │   │   ├── report_worker.py       # Client report generation
│   │   │   └── email_worker.py
│   │   ├── integrations/              # Platform connectors
│   │   │   ├── base.py                # Abstract platform interface
│   │   │   ├── instagram.py
│   │   │   ├── facebook.py
│   │   │   ├── twitter.py
│   │   │   ├── linkedin.py
│   │   │   └── tiktok.py
│   │   ├── websocket/
│   │   │   ├── notifications.py       # Real-time notifications
│   │   │   └── collaboration.py       # Live content editing
│   │   └── utils/
│   │       └── logger.py              # structlog setup
│   ├── alembic/
│   ├── tests/
│   ├── pyproject.toml                 # Single source of truth (deps, tools, config)
│   ├── uv.lock
│   ├── noxfile.py
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── app/                       # Next.js App Router
│   │   │   ├── (auth)/
│   │   │   │   ├── login/page.tsx
│   │   │   │   └── signup/page.tsx
│   │   │   ├── (dashboard)/
│   │   │   │   ├── layout.tsx         # Sidebar + topbar shell
│   │   │   │   ├── page.tsx           # Overview / home
│   │   │   │   ├── clients/
│   │   │   │   ├── campaigns/
│   │   │   │   ├── content/
│   │   │   │   ├── calendar/
│   │   │   │   ├── analytics/
│   │   │   │   ├── assets/
│   │   │   │   ├── approvals/
│   │   │   │   └── settings/
│   │   │   └── reports/
│   │   │       └── [reportId]/page.tsx
│   │   ├── components/
│   │   │   ├── ui/                    # shadcn/ui primitives
│   │   │   ├── content/               # Content editor, preview, AI tools
│   │   │   ├── calendar/              # Calendar views, drag-drop
│   │   │   ├── analytics/             # Charts, KPI cards, tables
│   │   │   ├── campaigns/             # Campaign cards, timelines
│   │   │   └── layout/                # Sidebar, topbar, mobile nav
│   │   ├── lib/
│   │   │   ├── api.ts                 # Typed API client
│   │   │   ├── socket.ts              # WebSocket client
│   │   │   └── utils.ts               # cn() helper
│   │   ├── hooks/
│   │   │   ├── use-content.ts
│   │   │   ├── use-campaigns.ts
│   │   │   └── use-auth.ts
│   │   └── types/
│   │       └── index.ts
│   ├── public/
│   ├── package.json
│   └── Dockerfile
├── db/
│   ├── init.sql                       # Schema DDL
│   └── seed.sql                       # Demo data
├── docker/
│   └── docker-compose.yml
├── .cursor/skills/                    # Cursor AI skills
├── .github/workflows/
├── .env.example
└── README.md
```

## Database Schema

| Table | Purpose | Key Columns |
|-------|---------|-------------|
| `organization` | Agency tenant | id (UUID), name, domain, settings (JSON) |
| `users` | Agency team members | id (UUID), org_id (FK), email, role, password_hash |
| `subscription` | Stripe billing | id (UUID), org_id (FK), stripe_subscription_id, plan_tier, clients_limit, posts_limit |
| `client` | Managed client/brand | id (UUID), org_id (FK), brand_name, industry, description, logo_url, settings (JSON) |
| `platform_account` | Connected social account | id (UUID), client_id (FK), platform, account_handle, access_token_enc, status |
| `campaign` | Marketing campaign | id (UUID), client_id (FK), org_id (FK), name, objective, start_date, end_date, status, budget (JSON) |
| `content` | Content piece (post) | id (UUID), campaign_id (FK), client_id (FK), org_id (FK), body, media_urls (JSON), hashtags (JSON), platform, status, scheduled_at |
| `content_schedule` | Publishing schedule entry | id (UUID), content_id (FK), platform_account_id (FK), scheduled_at, published_at, external_post_id, status |
| `approval` | Approval workflow entry | id (UUID), content_id (FK), reviewer_id (FK), status, feedback, decided_at |
| `asset` | Media library item | id (UUID), org_id (FK), client_id (FK), filename, s3_key, mime_type, size_bytes, tags (JSON) |
| `analytics_snapshot` | Performance metrics | id (UUID), platform_account_id (FK), content_id (FK), date, impressions, reach, engagement, clicks, followers_delta (JSON) |
| `client_report` | Generated client report | id (UUID), client_id (FK), period_start, period_end, metrics_summary (JSON), ai_insights, report_url |

## User Roles (RBAC)

| Role | Permissions |
|------|-------------|
| Admin | Full org access, billing, user management, all clients |
| Manager | Manage clients, campaigns, approve content, view analytics |
| Content Creator | Create/edit content, upload assets, request approvals |
| Viewer | Read-only access to content, analytics, and reports |

## User Journeys

### Agency Owner Flow
```
Sign up → Create org → Subscribe (Stripe) → Add team members
  → Add client → Connect client's social accounts
  → Create campaign → Assign content creators
  → Review & approve content → Track analytics → Send client reports
```

### Content Creator Flow
```
Log in → View assigned clients/campaigns → Create content (AI-assisted)
  → Upload media assets → Schedule posts → Submit for approval
  → Revise if needed → Content auto-publishes at scheduled time
```

### Client Report Flow
```
Analytics sync runs (Celery) → Aggregate metrics per client
  → AI generates insights → Report PDF created
  → Email sent via AgentMail with report attached
```

## Design System

- **Background**: Slate-50 to white gradient (light theme primary)
- **Primary accent**: Indigo-600 (#4f46e5)
- **Success**: Emerald-500 (#10b981)
- **Warning**: Amber-500 (#f59e0b)
- **Danger**: Red-500 (#ef4444)
- **Text**: Slate-900 primary, Slate-500 secondary
- **Font**: Inter (body + headings)
- **Cards**: `bg-white border border-slate-200 rounded-xl shadow-sm`
- **Calendar**: Full-width grid with drag-drop support, color-coded by platform/client

## Environment Variables

| Variable | Scope | Purpose |
|----------|-------|---------|
| `DATABASE_URL` | Backend | PostgreSQL async connection |
| `REDIS_URL` | Backend | Redis connection |
| `JWT_SECRET` | Backend | Token signing |
| `OPENAI_API_KEY` | Backend | GPT-4o for AI content + DALL-E |
| `ANTHROPIC_API_KEY` | Backend | Claude fallback |
| `STRIPE_SECRET_KEY` | Backend | Stripe API |
| `STRIPE_WEBHOOK_SECRET` | Backend | Webhook verification |
| `AWS_ACCESS_KEY_ID` | Backend | S3 media storage |
| `AWS_SECRET_ACCESS_KEY` | Backend | S3 media storage |
| `S3_BUCKET_NAME` | Backend | Media bucket |
| `AGENTMAIL_API_KEY` | Backend | AgentMail email API |
| `AGENTMAIL_DEFAULT_DOMAIN` | Backend | Custom email domain |
| `NEXT_PUBLIC_API_URL` | Frontend | Backend API base URL |
| `NEXT_PUBLIC_STRIPE_KEY` | Frontend | Stripe publishable key |

## Naming Conventions

| Used for | Style | Example |
|----------|-------|---------|
| Python package, files | snake_case | `agency`, `ai_engine.py` |
| Python classes | PascalCase | `ContentService`, `CampaignResponse` |
| API routes | kebab-case | `/api/v1/platform-accounts` |
| DB tables | snake_case | `platform_account`, `content_schedule` |
| Next.js components | PascalCase | `ContentEditor.tsx`, `KPICard.tsx` |
| Next.js pages/dirs | kebab-case | `campaigns/`, `[reportId]/` |
| CSS/Tailwind | kebab-case | `text-slate-900`, `bg-indigo-600` |
| Env vars | UPPER_SNAKE_CASE | `OPENAI_API_KEY` |

## Key Rules

1. **Always use `src/` layout** for the Python backend package
2. **`pyproject.toml` is the single source of truth** for deps, tools, and config
3. **Use `uv` for package management** — `uv sync` to install, `uv lock` to update
4. **Use `nox` for task automation** — `uv run nox -s test`, `uv run nox -s lint`
5. **Use `ruff` for linting and formatting** — replaces flake8, isort, black
6. **Use `mypy` in strict mode** — full type checking
7. **Never mix secrets with structural config** — `.env` for secrets only
8. **Always use structlog** — never `print()`
9. **Every tenant-scoped table has `org_id`** — multi-tenant isolation
10. **Frontend and backend are independently deployable**
11. **All API routes versioned** under `/api/v1/`
12. **Platform integrations are pluggable** — implement the abstract `PlatformConnector` interface
13. **Content must go through approval workflow** before publishing
14. **Analytics are synced via background workers** — never block API requests
