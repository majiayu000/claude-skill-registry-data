---
name: init-deep
description: "Generate hierarchical AGENTS.md files per directory. Use for context-specific instructions throughout projects."
context: fork
globs: []
alwaysApply: false
---

# Init-Deep — Hierarchical Context Generation

Use this skill to generate `AGENTS.md` files at each directory level in the project. Agents automatically read the relevant AGENTS.md when working in that directory.

---

## What It Generates

```
project/
├── AGENTS.md              # Project-wide context (stack, conventions, commands)
├── src/
│   ├── AGENTS.md          # src-specific context (architecture, patterns)
│   ├── routes/
│   │   ├── AGENTS.md      # Routes context (endpoint patterns, auth)
│   │   └── users/
│   │       └── AGENTS.md  # Users context (user-specific patterns)
│   ├── services/
│   │   └── AGENTS.md      # Services context (service layer patterns)
│   └── models/
│       └── AGENTS.md      # Models context (ORM patterns, relationships)
├── tests/
│   └── AGENTS.md          # Tests context (test patterns, fixtures)
└── migrations/
    └── AGENTS.md          # Migrations context (Alembic patterns)
```

---

## Usage

```
/init-deep [--max-depth=3]
```

| Option | Default | Description |
|--------|---------|-------------|
| `--max-depth` | 3 | Maximum directory depth to generate AGENTS.md |

---

## AGENTS.md Template

Each AGENTS.md contains:

```markdown
# <Directory> Context

## Purpose
What this directory contains and its role in the project.

## Patterns
Common patterns used in this directory.

## Conventions
Naming, structure, and style conventions.

## Key Files
Important files in this directory and what they do.

## Related Directories
Parent and child directories and their relationships.
```

---

## Example: src/routes/AGENTS.md

```markdown
# Routes Context

## Purpose
FastAPI route definitions. Each route file maps to an endpoint group.

## Patterns
- Router pattern: `router = APIRouter(prefix="/users", tags=["users"])`
- Dependency injection: `db: AsyncSession = Depends(get_db)`
- Response models: `response_model=UserResponse`
- Error handling: `raise HTTPException(status_code=404, detail="...")`

## Conventions
- One router per resource (users.py, products.py, reviews.py)
- Endpoints: list (GET /), create (POST /), read (GET /{id}), update (PATCH /{id}), delete (DELETE /{id})
- Use snake_case for route paths, camelCase for JSON
- All endpoints must be async

## Key Files
- `users.py` — User CRUD endpoints
- `auth.py` — Authentication endpoints (login, register, refresh)
- `reviews.py` — Product review endpoints

## Related Directories
- Parent: `src/` — Application source
- Sibling: `src/services/` — Business logic (routes call services)
- Sibling: `src/models/` — Database models (routes use models via services)
```

---

## How Agents Use AGENTS.md

When an agent reads or edits a file, the system walks up the directory tree and injects all AGENTS.md files found:

```
Agent reads: src/routes/users/get_user.py
  ↓
Walk up: src/routes/users/AGENTS.md → inject
  ↓
Walk up: src/routes/AGENTS.md → inject
  ↓
Walk up: src/AGENTS.md → inject
  ↓
Walk up: AGENTS.md (root) → inject
  ↓
Agent now has full context for the file it's working on
```

---

## When to Run

- New project setup
- After major restructuring
- When adding new directories
- When conventions change

---

## Relationship with Codemap

| Skill | Purpose | Output |
|-------|---------|--------|
| `codemap` | Generate codebase map | Directory tree + entry points |
| `init-deep` | Generate context files | AGENTS.md per directory |

Codemap shows the structure. Init-deep fills each directory with context.
