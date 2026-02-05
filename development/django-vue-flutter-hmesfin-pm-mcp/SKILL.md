---
name: django-vue-flutter
description: |
  Comprehensive guide for developing full-stack applications using the Django + Vue.js + Flutter starter template.
  Use this skill when creating new projects from the fullstack-starter-djvurn template, or when working on projects that follow this architecture.

  Covers: Django app creation, DRF API development, Vue.js components, Flutter mobile development, database migrations,
  API client generation, testing (TDD), type safety (mypy, TypeScript), code quality enforcement, and Docker-based workflows.

  Trigger patterns: "create new Django app", "add API endpoint", "build Vue component", "setup Flutter feature",
  "write tests for", "run migrations", "generate API client", "type check", "follow TDD"
---

# Django + Vue.js + Flutter Fullstack Development

## Overview

This skill guides development with the fullstack-starter-djvurn template: a Docker-based monorepo with Django (DRF) backend, Vue.js (TypeScript) frontend, and Flutter mobile app.

**Template location**: `\\wsl.localhost\Ubuntu\home\hmesfin\dev\templates\fullstack-starter-djvurn`

## Core Architecture

### Stack Components
- **Backend**: Django 5.x + DRF + Celery + PostgreSQL + Redis
- **Frontend**: Vue 3 + TypeScript + Vite + Shadcn-vue + Tailwind v4
- **Mobile**: Flutter + Expo + TypeScript
- **Infrastructure**: Docker Compose (local/staging/production)
- **Package Management**: Backend uses `uv`, Frontend uses `npm`

### Key Architectural Decisions
1. **Monorepo structure**: `backend/`, `frontend/`, `mobile/` at root level
2. **API-only backend**: Django serves only API endpoints + admin (no template views)
3. **Custom User model**: Email-based auth (`apps.users.User`, no username)
4. **Auto-generated API clients**: OpenAPI schema → TypeScript client
5. **UUID primary keys**: Recommended for API-exposed models
6. **All services in Docker**: Including Vite dev server

## Mandatory Development Standards

### 1. File Size Limit: 500 Lines Maximum
- **Enforcement**: No file should exceed 500 lines
- **When approaching limit**: Split into multiple files or modules
- **Backend**: Split large views into multiple ViewSets, models into separate files
- **Frontend**: Split large components, create composables, extract utilities
### 2. Strict TDD (Test-Driven Development)
- **RED-GREEN-REFACTOR cycle mandatory**
  1. **RED**: Write failing test first
  2. **GREEN**: Write minimal code to pass
  3. **REFACTOR**: Improve code while keeping tests green
- **No production code without tests**: Every function, view, component gets tests
- **Test files co-located**:
  - Backend: `apps/<app>/tests.py` or `apps/<app>/tests/`
  - Frontend: `src/<feature>/__tests__/<component>.test.ts`
  - Mobile: `src/<feature>/__tests__/<component>.test.tsx`

### 3. Strict Typing
- **Backend (Python)**:
  - Type hints for all functions/methods
  - Run `docker compose run --rm django mypy apps` before commits
  - Configure in `backend/pyproject.toml`
- **Frontend (TypeScript)**:
  - Strict mode enabled in `tsconfig.json`
  - No `any` types without explicit reason
  - Run `docker compose run --rm frontend npm run type-check`
- **Mobile (TypeScript)**:
  - Strict mode enabled
  - Props and state explicitly typed

### 4. Efficiency Tools Usage
- **API Client Generation**: Always use `npm run generate:api` after backend changes
- **Code Quality**: Pre-commit hooks for linting, formatting, type checking
- **Docker**: All commands run via `docker compose run --rm <service>`

## Project Structure Reference

See `references/PROJECT_STRUCTURE.md` for complete directory layout and file organization patterns.

## Development Workflows

### Starting a New Project

**Process**:
1. Copy template: `cp -r templates/fullstack-starter-djvurn new-project-name`
2. Update configuration (see `references/NEW_PROJECT_SETUP.md`)
3. Initialize git: `cd new-project-name && git init`
4. Start services: `docker compose up -d`
5. Create superuser: `docker compose run --rm django python manage.py createsuperuser`

### Creating a New Django App

**TDD Workflow**:

1. **Plan the app** (models, endpoints, functionality)
2. **Create app structure**:
   ```bash
   docker compose run --rm django python manage.py startapp <app_name> backend/apps/<app_name>
   ```
3. **Write model tests first** (`backend/apps/<app_name>/tests.py`):
   ```python
   import pytest
   from apps.<app_name>.models import ModelName

   @pytest.mark.django_db
   class TestModelName:
       def test_create_instance(self):
           # Test should FAIL initially (RED)
           instance = ModelName.objects.create(name="Test")
           assert instance.name == "Test"
   ```
4. **Run tests** (verify they FAIL): `docker compose run --rm django pytest apps/<app_name>/`
5. **Create models** (`backend/apps/<app_name>/models.py`):
   ```python
   import uuid
   from django.db import models
   from typing import Optional  # Type hints

   class ModelName(models.Model):
       id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
       name: str = models.CharField(max_length=255)  # Type annotation
       created = models.DateTimeField(auto_now_add=True)
       modified = models.DateTimeField(auto_now=True)

       def __str__(self) -> str:
           return self.name
   ```
6. **Add to INSTALLED_APPS** (`backend/config/settings/base.py`)
7. **Create and run migrations**:
   ```bash
   docker compose run --rm django python manage.py makemigrations
   docker compose run --rm django python manage.py migrate
   ```
8. **Run tests** (should PASS now - GREEN)
9. **Add serializers, views, register with router** (see `references/DRF_PATTERNS.md`)
10. **Type check**: `docker compose run --rm django mypy apps/<app_name>/`

### Adding API Endpoints

**Complete workflow in `references/API_WORKFLOW.md`**

**Quick reference**:
1. Write serializer tests (TDD)
2. Create serializer with type hints
3. Write ViewSet tests
4. Create ViewSet
5. Register in `backend/config/api_router.py`
6. Regenerate frontend client: `docker compose run --rm frontend npm run generate:api`
7. Type check both: `docker compose run --rm django mypy apps && docker compose run --rm frontend npm run type-check`

### Creating Vue.js Components

**TDD workflow**:
1. **Write component tests first**
2. **Run tests** (should FAIL): `docker compose run --rm frontend npm run test`
3. **Create component** with strict TypeScript
4. **Run tests** (should PASS)
5. **Type check**: `docker compose run --rm frontend npm run type-check`
6. **File size check**: Keep under 500 lines

**See `references/VUE_COMPONENT_PATTERNS.md` for complete examples**

### Database Migrations

**Process**:
1. Modify models in `backend/apps/<app>/models.py`
2. Run tests to ensure model logic works
3. Generate migration: `docker compose run --rm django python manage.py makemigrations`
4. Review migration file
5. Apply: `docker compose run --rm django python manage.py migrate`
6. Regenerate API client: `docker compose run --rm frontend npm run generate:api`

### Flutter Features

**See `references/REACT_NATIVE_PATTERNS.md` for mobile development workflows**

## Code Quality Enforcement

### Running Tests

**Backend**:
```bash
# All tests
docker compose run --rm django pytest

# Specific app
docker compose run --rm django pytest apps/<app_name>/

# With coverage
docker compose run --rm django pytest --cov=apps --cov-report=html
```

**Frontend**:
```bash
# Unit tests
docker compose run --rm frontend npm run test

# E2E tests (Playwright)
docker compose run --rm frontend npm run test:e2e

# Coverage
docker compose run --rm frontend npm run test:coverage
```

**Mobile**:
```bash
docker compose run --rm mobile npm run test
```

### Type Checking

**Backend (mypy)**:
```bash
# Type check entire backend
docker compose run --rm django mypy apps

# Specific app
docker compose run --rm django mypy apps/<app_name>
```

**Frontend**:
```bash
docker compose run --rm frontend npm run type-check
```

**Mobile**:
```bash
docker compose run --rm mobile npm run type-check
```

### Linting & Formatting

**Backend** (Ruff):
```bash
# Check
docker compose run --rm django ruff check apps

# Fix
docker compose run --rm django ruff check apps --fix

# Format
docker compose run --rm django ruff format apps
```

**Frontend** (ESLint + Prettier):
```bash
# Lint
docker compose run --rm frontend npm run lint

# Format
docker compose run --rm frontend npm run format
```

## Common Patterns

### API Client Usage Pattern

**After regenerating API client** (`npm run generate:api`):

```typescript
import { projectsList, projectsCreate } from '@/api/sdk.gen'
import { apiClient } from '@/lib/api-client'

// Fetch data
const response = await projectsList({ client: apiClient })

// Create
const newProject = await projectsCreate({
  client: apiClient,
  body: { name: 'New Project', status: 'active' }
})

// Error handling (CRITICAL for generated SDK)
if (response && 'error' in response && response.error) {
  throw response  // SDK returns errors instead of throwing
}
```

### Composable Pattern

```typescript
// src/composables/useProjects.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/vue-query'
import { projectsList, projectsCreate } from '@/api/sdk.gen'
import { apiClient } from '@/lib/api-client'

export function useProjects() {
  const queryClient = useQueryClient()

  const { data, isLoading } = useQuery({
    queryKey: ['projects'],
    queryFn: () => projectsList({ client: apiClient })
  })

  const createMutation = useMutation({
    mutationFn: (data) => projectsCreate({ client: apiClient, body: data }),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['projects'] })
  })

  return { projects: data, isLoading, createProject: createMutation.mutate }
}
```

### Type Checking

**Backend**: `docker compose run --rm django mypy apps`
**Frontend**: `docker compose run --rm frontend npm run type-check`
**Mobile**: `docker compose run --rm mobile npm run type-check`

### Linting & Formatting

**Backend (Ruff)**:
- Check: `docker compose run --rm django ruff check apps`
- Fix: `docker compose run --rm django ruff check apps --fix`

**Frontend (ESLint)**:
- Lint: `docker compose run --rm frontend npm run lint`
- Format: `docker compose run --rm frontend npm run format`

## Quick Reference

### Essential Commands

**Start services**: `docker compose up -d`
**View logs**: `docker compose logs -f <service>`
**Stop services**: `docker compose down`
**Run tests**: `docker compose run --rm <service> <test-command>`
**Shell access**: `docker compose exec <service> bash`

### Key Files

- Django settings: `backend/config/settings/`
- API router: `backend/config/api_router.py`
- Frontend API client: `frontend/src/api/` (auto-generated)
- Environment vars: `.envs/.local/`

### Documentation

For detailed patterns, workflows, and examples, see:
- `references/PROJECT_STRUCTURE.md` - Directory organization
- `references/API_WORKFLOW.md` - Complete API development flow
- `references/DRF_PATTERNS.md` - Django REST Framework patterns
- `references/VUE_COMPONENT_PATTERNS.md` - Vue.js best practices
- `references/REACT_NATIVE_PATTERNS.md` - Mobile development
- `references/TESTING_PATTERNS.md` - TDD workflows and examples
- `references/TYPE_SAFETY.md` - Type checking guidelines
- `references/NEW_PROJECT_SETUP.md` - Project initialization

## TDD Checklist

Before committing code, verify:
- [ ] All tests written BEFORE implementation
- [ ] All tests passing
- [ ] Type checking passes (mypy + TypeScript)
- [ ] No files over 500 lines
- [ ] Linting passes
- [ ] API client regenerated (if backend changed)
