---
name: codemap
description: "Generate codebase maps with directory trees and relationships. Use for onboarding and architecture documentation."
context: fork
---

# Codemap — Codebase Cartography

## When to Use
- Onboarding to a new codebase
- Planning large refactors
- Documenting architecture
- Understanding dependencies between modules

## How to Generate

### 1. Directory Tree
```bash
tree -I 'node_modules|.git|__pycache__|*.pyc|.venv|dist|build' -L 3
```

### 2. Entry Points
Identify main entry points:
- `package.json` → `main`, `bin`
- `pyproject.toml` → `scripts`
- `src/main.py`, `src/index.ts`, `app.py`
- Dockerfiles, docker-compose.yml

### 3. Module Map
For each significant directory, document:
- Purpose
- Key files
- Dependencies (imports from other modules)
- Public API surface

### 4. Relationship Graph
Show how modules connect:
```
frontend/ → api/ (HTTP calls)
backend/ → database/ (SQLAlchemy models)
worker/ → queue/ (Redis/RabbitMQ)
```

## Output Format

```markdown
# Codemap: <Project Name>

## Entry Points
- `src/main.py` — FastAPI application
- `scripts/migrate.sh` — Database migration runner

## Directory Structure
```
src/
├── api/          # REST endpoints
├── services/     # Business logic
├── models/       # Database schemas
└── utils/        # Shared utilities
```

## Module Relationships
| Module | Depends On | Used By |
|--------|-----------|---------|
| api/ | services/, models/ | — (top level) |
| services/ | models/, utils/ | api/ |
| models/ | — | api/, services/ |

## Key Files
| File | Purpose | Lines |
|------|---------|-------|
| src/api/auth.py | Authentication endpoints | 120 |
| src/services/user.py | User business logic | 200 |
```

## Maintenance
- Regenerate when directory structure changes significantly
- Update after major refactors
- Keep in `/memories/repo/codemap.md` (Tier 1 memory)
