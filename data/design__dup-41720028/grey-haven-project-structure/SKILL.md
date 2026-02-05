---
name: grey-haven-project-structure
description: Organize Grey Haven projects following standard structures for TanStack Start (frontend) and FastAPI (backend). Use when creating new projects, organizing files, or refactoring project layout.
# v2.0.43: Skills to auto-load for project work
skills:
  - grey-haven-code-style
# v2.0.74: Tools for project organization
allowed-tools:
  - Read
  - Write
  - Bash
  - Grep
  - Glob
  - TodoWrite
---

# Grey Haven Project Structure

Follow Grey Haven Studio's standardized project structures for **TypeScript/React** (TanStack Start) and **Python/FastAPI** projects.

## Frontend Structure (TanStack Start + React 19)

Based on `cvi-template` - TanStack Start, React 19, Drizzle, Better-auth.

### Directory Layout

```
project-root/
├── .claude/                     # Claude Code configuration
├── .github/workflows/           # GitHub Actions (CI/CD)
├── public/                      # Static assets
├── src/
│   ├── routes/                  # TanStack Router file-based routes
│   │   ├── __root.tsx          # Root layout
│   │   ├── index.tsx           # Homepage
│   │   ├── _authenticated/     # Protected routes group
│   │   │   ├── _layout.tsx    # Auth layout wrapper
│   │   │   ├── dashboard.tsx  # /dashboard
│   │   │   └── profile.tsx    # /profile
│   │   └── auth/               # Auth routes
│   │       ├── login.tsx      # /auth/login
│   │       └── signup.tsx     # /auth/signup
│   ├── lib/
│   │   ├── components/          # React components
│   │   │   ├── ui/             # Shadcn UI (PascalCase)
│   │   │   ├── auth/           # Auth components
│   │   │   ├── layout/         # Layout components
│   │   │   └── shared/         # Shared components
│   │   ├── server/              # Server-side code
│   │   │   ├── schema/         # Drizzle schema (snake_case)
│   │   │   ├── functions/      # Server functions
│   │   │   ├── auth.ts         # Better-auth config
│   │   │   └── db.ts           # Database connections
│   │   ├── config/              # Configuration
│   │   │   ├── env.ts          # Environment validation
│   │   │   └── auth.ts         # Auth configuration
│   │   ├── middleware/          # Route middleware
│   │   ├── hooks/               # Custom React hooks (use-*)
│   │   ├── utils/               # Utility functions
│   │   └── types/               # TypeScript types
│   └── tests/
│       ├── unit/               # Vitest unit tests
│       ├── integration/        # Vitest integration tests
│       └── e2e/                # Playwright E2E tests
├── migrations/                  # Drizzle migrations
├── .env.example                 # Example environment variables
├── .prettierrc                  # Prettier (90 chars, double quotes)
├── .eslintrc                    # ESLint (any allowed, strict off)
├── tsconfig.json                # TypeScript (~/* path alias)
├── commitlint.config.cjs        # Commitlint (100 char header)
├── drizzle.config.ts            # Drizzle ORM config
├── vite.config.ts               # Vite configuration
├── vitest.config.ts             # Vitest test configuration
├── package.json                 # Dependencies (use bun!)
└── README.md                    # Project documentation
```

### Key Frontend Patterns

#### Path Imports - Always Use ~/* Alias

```typescript
// ✅ Correct - Use ~/* path alias
import { Button } from "~/lib/components/ui/button";
import { getUserById } from "~/lib/server/functions/users";
import { env } from "~/lib/config/env";
import { useAuth } from "~/lib/hooks/use-auth";

// ❌ Wrong - Relative paths
import { Button } from "../../lib/components/ui/button";
```

#### File Naming Conventions

- **Components**: PascalCase (`UserProfile.tsx`, `LoginForm.tsx`)
- **Routes**: lowercase with hyphens (`user-profile.tsx`, `auth/login.tsx`)
- **Utilities**: camelCase or kebab-case (`formatDate.ts`, `use-auth.ts`)
- **Server functions**: camelCase (`auth.ts`, `users.ts`)
- **Schema files**: plural lowercase (`users.ts`, `organizations.ts`)

#### Component Structure Order

```typescript
import { useState } from "react";                    // 1. External imports
import { useQuery } from "@tanstack/react-query";
import { Button } from "~/lib/components/ui/button"; // 2. Internal imports
import { getUserById } from "~/lib/server/functions/users";

interface UserProfileProps {                         // 3. Types/Interfaces
  userId: string;
}

export default function UserProfile({ userId }: UserProfileProps) { // 4. Component
  const [editing, setEditing] = useState(false);    // 5. State hooks

  const { data: user } = useQuery({                 // 6. Queries/Mutations
    queryKey: ["user", userId],
    queryFn: () => getUserById(userId),
    staleTime: 60000,
  });

  const handleSave = () => {                        // 7. Event handlers
    // ...
  };

  return (                                          // 8. JSX
    <div>
      <h1>{user?.full_name}</h1>
      <Button onClick={handleSave}>Save</Button>
    </div>
  );
}
```

## Backend Structure (FastAPI + Python)

Based on `cvi-backend-template` - FastAPI, SQLModel, Alembic.

### Directory Layout

```
project-root/
├── .github/workflows/           # GitHub Actions
├── app/
│   ├── __init__.py
│   ├── main.py                  # FastAPI app entry point
│   ├── routers/                 # API routers (endpoints)
│   │   ├── __init__.py
│   │   ├── auth.py             # /auth routes
│   │   ├── users.py            # /users routes
│   │   └── health.py           # /health routes
│   ├── services/                # Business logic layer
│   │   ├── __init__.py
│   │   ├── user_service.py
│   │   ├── auth_service.py
│   │   └── billing_service.py
│   ├── db/                      # Database layer
│   │   ├── __init__.py
│   │   ├── models/              # SQLModel models (snake_case)
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── tenant.py
│   │   │   └── organization.py
│   │   ├── repositories/        # Data access layer
│   │   │   ├── __init__.py
│   │   │   ├── base.py         # Base repository
│   │   │   └── user_repository.py
│   │   └── session.py          # Database sessions
│   ├── schemas/                 # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── user.py             # UserCreate, UserResponse
│   │   ├── auth.py             # AuthRequest, AuthResponse
│   │   └── common.py           # Shared schemas
│   ├── middleware/              # FastAPI middleware
│   │   ├── __init__.py
│   │   ├── auth.py             # JWT verification
│   │   └── tenant.py           # Tenant context
│   ├── core/                    # Core configuration
│   │   ├── __init__.py
│   │   ├── config.py           # Settings (Doppler)
│   │   ├── security.py         # Password hashing, JWT
│   │   └── deps.py             # FastAPI dependencies
│   └── utils/                   # Utility functions
│       ├── __init__.py
│       └── format.py
├── tests/                       # Pytest tests
│   ├── __init__.py
│   ├── unit/                   # @pytest.mark.unit
│   ├── integration/            # @pytest.mark.integration
│   └── e2e/                    # @pytest.mark.e2e
├── alembic/                     # Alembic migrations
│   ├── versions/
│   └── env.py
├── .env.example                 # Example environment variables
├── .env                         # Local environment (gitignored)
├── pyproject.toml              # Ruff, mypy, pytest config
├── alembic.ini                 # Alembic configuration
├── Taskfile.yml                # Task runner commands
├── requirements.txt            # Production dependencies
├── requirements-dev.txt        # Development dependencies
└── README.md                   # Project documentation
```

### Key Backend Patterns

#### Import Organization (Automatic with Ruff)

```python
"""Module docstring describing purpose."""

# 1. Standard library imports
import os
from datetime import datetime
from typing import Optional
from uuid import UUID

# 2. Third-party imports
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select

# 3. Local imports
from app.db.models.user import User
from app.db.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserResponse
```

#### File Naming Conventions

- **Modules**: snake_case (`user_service.py`, `auth_middleware.py`)
- **Models**: PascalCase class, snake_case file (`User` in `user.py`)
- **Tests**: `test_` prefix (`test_user_service.py`)

#### Repository Pattern (with Tenant Isolation)

```python
# app/db/repositories/base.py
from typing import Generic, TypeVar, Optional
from uuid import UUID
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")

class BaseRepository(Generic[T]):
    """Base repository with CRUD and tenant isolation."""

    def __init__(self, session: AsyncSession, model: type[T]):
        self.session = session
        self.model = model

    async def get_by_id(self, id: UUID, tenant_id: UUID) -> Optional[T]:
        """Get by ID with automatic tenant filtering."""
        result = await self.session.execute(
            select(self.model)
            .where(self.model.id == id)
            .where(self.model.tenant_id == tenant_id)
        )
        return result.scalar_one_or_none()
```

#### Service Layer Pattern

```python
# app/services/user_service.py
from uuid import UUID
from app.db.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserResponse

class UserService:
    """User business logic."""

    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def create_user(self, data: UserCreate, tenant_id: UUID) -> UserResponse:
        """Create new user with validation."""
        existing = await self.user_repo.get_by_email(data.email_address, tenant_id)
        if existing:
            raise ValueError("Email already registered")

        user = await self.user_repo.create(data, tenant_id)
        return UserResponse.model_validate(user)
```

## Supporting Documentation

All supporting files are under 500 lines per Anthropic best practices:

- **[examples/](examples/)** - Complete project examples
  - [frontend-directory-structure.md](examples/frontend-directory-structure.md) - Full TanStack Start structure
  - [backend-directory-structure.md](examples/backend-directory-structure.md) - Full FastAPI structure
  - [component-structure.md](examples/component-structure.md) - React component patterns
  - [repository-pattern.md](examples/repository-pattern.md) - Repository with tenant isolation
  - [service-pattern.md](examples/service-pattern.md) - Service layer examples
  - [INDEX.md](examples/INDEX.md) - Examples navigation

- **[reference/](reference/)** - Structure references
  - [file-naming.md](reference/file-naming.md) - Naming conventions
  - [import-organization.md](reference/import-organization.md) - Import ordering rules
  - [path-aliases.md](reference/path-aliases.md) - Path alias configuration
  - [INDEX.md](reference/INDEX.md) - Reference navigation

- **[templates/](templates/)** - Copy-paste ready templates
  - [tanstack-start-project/](templates/tanstack-start-project/) - Frontend scaffold
  - [fastapi-project/](templates/fastapi-project/) - Backend scaffold

- **[checklists/](checklists/)** - Structure checklists
  - [project-setup-checklist.md](checklists/project-setup-checklist.md) - New project setup
  - [refactoring-checklist.md](checklists/refactoring-checklist.md) - Structure refactoring

## When to Apply This Skill

Use this skill when:
- Creating new Grey Haven projects
- Organizing files in existing projects
- Refactoring project layout
- Setting up directory structure
- Deciding where to place new files
- Onboarding new team members to project structure

## Template Reference

These patterns are from Grey Haven's production templates:
- **Frontend**: cvi-template (TanStack Start + React 19)
- **Backend**: cvi-backend-template (FastAPI + Python)

## Critical Reminders

1. **Path aliases**: Always use ~/* for TypeScript imports
2. **File naming**: Components PascalCase, modules snake_case
3. **Import order**: External → Internal → Local
4. **Component structure**: Imports → Types → Component → Hooks → Handlers → JSX
5. **Tenant isolation**: Repository pattern includes tenant_id filtering
6. **Database fields**: snake_case in schema files (NOT camelCase)
7. **Test organization**: unit/, integration/, e2e/ directories
8. **Configuration**: Doppler for all environment variables
9. **Routes**: TanStack file-based routing in src/routes/
10. **Backend layers**: Routers → Services → Repositories → Models
