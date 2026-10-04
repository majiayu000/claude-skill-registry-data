---
name: scaffold-project
description: Centralized full-stack project scaffold — bootstraps a complete Python/FastAPI backend skeleton (bootstrap) and scaffolds Next.js (web/) or React Chrome Extension (extension/) frontends (setui) with 11 themes and AI design system intelligence.
---

# Scaffold Project
> *"One command. Full-stack production architecture."*

Initializes a complete, production-ready full-stack application from scratch:
1. **Backend (`bootstrap` tool)**: FastAPI entrypoint, configuration layer, helpers, SQLite/SQLAlchemy database layer, auth system with scoped JWTs, intelligent agent lifecycle & validators, and standard agent rules.
2. **Frontend (`setui` tool)**: Complete Next.js + Tailwind + shadcn/ui frontend (`web/`) or React + Vite Chrome Extension (`extension/`) with 11 built-in themes and AI design system generation via `ui-ux-pro-max`.

---

## How to Use

### 1. Scaffold Backend Skeleton (`bootstrap`)

Initializes the complete backend architecture into an empty project directory:

```bash
human-skills '{
    "tool_name": "bootstrap",
    "tool_args": {
        "destination": "/path/to/new_project"
    }
}'
```

Or via direct curl (no dependencies):
```bash
curl -sSL https://raw.githubusercontent.com/mdnaimul22/human-skills/main/skills/storage/my_skills/scaffold-project/resources/initialize/backend/bootstrap.py | python3
```

### 2. Scaffold Frontend Client (`setui`)

Scaffold a Next.js web application (`web/`) or React Chrome Extension (`extension/`) inside the project root:

```bash
# Basic Next.js frontend (web/)
human-skills '{
    "tool_name": "setui",
    "tool_args": {
        "destination": "/path/to/new_project"
    }
}'

# With AI Design System generation (ui-ux-pro-max)
human-skills '{
    "tool_name": "setui",
    "tool_args": {
        "destination": "/path/to/new_project",
        "action": "frontend",
        "design_query": "beauty spa wellness premium",
        "density": 5,
        "motion": 6
    }
}'

# React + Vite Chrome Extension (extension/)
human-skills '{
    "tool_name": "setui",
    "tool_args": {
        "destination": "/path/to/new_project",
        "action": "chrome-extension",
        "design_query": "developer productivity dashboard"
    }
}'
```

---

## Full-Stack Project Structure

When both backend and frontend are scaffolded:

```
project_root/
├── main.py                  ← FastAPI entry point with auto-kill, health check, lifespan
├── .env                     ← Environment variables (fill from .env.example)
├── .env.example             ← Template for required env vars
├── .models.example          ← Template for AI model providers
├── .gitignore               ← Pre-configured for Python, Node, and secrets
├── README.md
├── LICENSE                  ← MIT License
├── docs/                    ← Documentation & generated brand guidelines
├── logs/                    ← Layer-based rotating logs
├── deploy/nginx/            ← Production Nginx configuration templates
│
├── .agents/rules/           ← Permanent coding standards synced from human-skills
│   ├── coding-standards.md
│   ├── architecture-patterns.md
│   ├── maintenance-testing.md
│   ├── config-path-rules.md
│   ├── config-usage-rules.md
│   ├── helpers-usage-rules.md
│   ├── project-config-example.md
│   ├── project-tree-example.md
│   └── common-git-workflow.md
│
├── src/                     ← Backend application core
│   ├── config/              ← Settings, env, sandboxed file I/O, hierarchical dual logger
│   ├── db/                  ← SQLAlchemy async engine, OwnershipMixin, models, repositories
│   ├── helpers/             ← Rate limiting, exceptions, date utils, port kill switch, tailscale
│   ├── core/                ← Business logic, password hashing, scoped JWTs, intelligent agents
│   │   ├── agents/          ← BaseAgent, AgentFactory, GeneralAgent lifecycle
│   │   └── validators/      ← Domain invariant pipeline
│   ├── providers/           ← External integrations (Email, Google OAuth, LLM rotator, proxy)
│   ├── schema/              ← Pydantic contracts (auth, common envelopes, agent protocols)
│   ├── services/            ← Fan-in use-case orchestration (AuthService, AgentService)
│   └── routers/             ← HTTP endpoints & auth dependencies (/api/auth, /api/agent)
│
├── tests/                   ← Modular test suite (128 passing tests out-of-the-box)
│   ├── core/
│   ├── routers/
│   ├── services/
│   └── helpers/
│
└── web/                     ← Next.js frontend (scaffolded via setui)
    ├── src/
    │   ├── app/             ← App router (layout, globals.css with 11 themes, auth pages)
    │   ├── components/      ← shadcn/ui components (30+ auto-installed), layout, navbar, sidebar
    │   ├── lib/             ← Type-safe FastAPI client (api.ts with JWT Bearer & 422 parsing)
    │   └── hooks/           ← State management (use-sidebar, use-auth with Zustand persist)
    ├── components.json
    ├── tailwind.config.ts
    └── package.json
```

---

## Built-in Auth System

The scaffold ships with a **production-grade authentication system** out of the box:

### Auth Endpoints

| Method | Endpoint | Auth | Purpose |
|:---|:---|:---|:---|
| `POST` | `/api/auth/register` | ❌ | Email signup → sends verification email |
| `GET` | `/api/auth/verify-email` | ❌ | Verify email via token in query |
| `POST` | `/api/auth/login` | ❌ | Email/password login → access + refresh tokens |
| `POST` | `/api/auth/google` | ❌ | Google OAuth login/signup |
| `POST` | `/api/auth/refresh` | ❌ | Rotate access + refresh tokens |
| `POST` | `/api/auth/forgot-password` | ❌ | Request password reset email |
| `POST` | `/api/auth/reset-password` | ❌ | Reset password with token |
| `POST` | `/api/auth/change-password` | ✅ | Change password (authenticated) |
| `GET` | `/api/auth/me` | ✅ | Get current user profile |
| `PATCH` | `/api/auth/me` | ✅ | Update profile (name) |
| `POST` | `/api/auth/logout` | ✅ | Client-side token clear guidance |

### Scoped JWT Tokens

| Purpose | Expiry | Usage |
|:---|:---|:---|
| `access` | 15 minutes | API Authorization header (`Bearer <token>`) |
| `refresh` | 7 days | POST /api/auth/refresh only |
| `verify_email` | 24 hours | Email verification link |
| `reset_password` | 1 hour | Password reset link |

### User ↔ Service Data Ownership

Use `OwnershipMixin` for any model that belongs to a user:

```python
from src.db import Base, TimestampMixin, OwnershipMixin

class Post(Base, TimestampMixin, OwnershipMixin):
    __tablename__ = "posts"
    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=_uuid)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
```

`BaseRepository` provides `list_by_owner(user_id)` and `count_by_owner(user_id)` for scoped queries to prevent IDOR attacks.

---

## Intelligent Agent Architecture

The scaffold includes a production agent framework in `src/core/agents`:
- **BaseAgent**: Abstract base with streaming, retry, and execution lifecycle.
- **AgentFactory**: Configuration-driven agent instantiation.
- **Domain Validators**: Invariant validation pipeline in `src/core/validators`.
- **Agent Router**: HTTP interface at `/api/agent/run` with authentication guards.

---

## Frontend Architecture (`setui`)

- **11 Curated Themes**: Default, Dark, Slate, Neon, Ocean, Cyberpunk, Velvet, Sunset, Forest, Luxury, Custom AI.
- **shadcn/ui Suite**: 30+ pre-configured UI primitives with zero manual initialization needed.
- **FastAPI Client (`src/lib/api.ts`)**: Built-in JWT Bearer header injection, timeout protection, and Pydantic 422 error unpacking.
- **Design Intelligence**: Passing `design_query` auto-generates brand guidelines (`docs/brand-guidelines.md`), design tokens (`design-tokens.json`), and typography pairings.

For comprehensive UI details, see [scaffold-ui.md](file:///home/naimul/human-skills/skills/storage/my_skills/scaffold-project/resources/scaffold-ui.md).

---

## Post-Bootstrap Checklist

- [ ] Copy `.env.example` → `.env` and fill mandatory fields
- [ ] Set `JWT_SECRET` to a strong random value for production
- [ ] Configure SMTP settings for email verification/password reset
- [ ] (Optional) Set `GOOGLE_CLIENT_ID` for Google OAuth
- [ ] Run backend: `python3 main.py` (auto-kills orphaned processes on port 8000)
- [ ] Run frontend: `cd web && npm run dev` (connects to backend at `http://localhost:8000`)
