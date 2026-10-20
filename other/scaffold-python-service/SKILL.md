---
name: scaffold-python-service
description: >-
  Load this skill when starting or scaffolding a new Python (FastAPI) web service: creating the
  initial directory layout, layer boundaries, base config, and .gitignore. Trigger when the user
  says "start/scaffold a FastAPI service", "new Python backend project", or sets up a fresh service
  repo. For a library use scaffold-python-library; for the frontend use scaffold-web-frontend.
compatibility: >-
  Requires Python 3.12+ and the `uv` package manager on PATH, plus network access to PyPI for the
  first `uv sync`. `ruff`, `mypy`, `pytest`, and `alembic` arrive as dev/project dependencies, not
  from a global install. Running the scaffolded service needs a reachable PostgreSQL instance;
  `git` is needed only to initialise the repo.
---

# Scaffold a Python Service

Organize by concern, not by file type. Each layer has one job.

```
project/
├── backend/
│   ├── app/
│   │   ├── api/           # Thin route handlers — validate input, call service, return output
│   │   ├── core/          # Config, dependencies, exceptions, middleware
│   │   ├── models/        # Pydantic request/response + domain models
│   │   ├── services/      # Business logic — no HTTP, no SQL
│   │   └── db/            # Database queries — SQL only, no business logic
│   └── tests/
│       ├── unit/
│       ├── integration/
│       └── system/
├── migrations/            # Database migrations (Alembic)
├── pyproject.toml
└── .gitignore
```

## Hard Layer Rules

- Route handlers contain no business logic — they call services
- Services contain no SQL — they call the database layer
- Database layer contains no business logic — it executes SQL
- One mutation path per aggregate — if multiple services could write the same table, define a single state manager

## Initial Config

- `pyproject.toml` with uv, ruff, mypy, pytest config — see `ceh-python-service:python-service-environment`.
- Web service deps: `fastapi`, `uvicorn[standard]`, `pydantic-settings`, `asyncpg`, `alembic`, `structlog`.

## Agent instruction file

Claude Code reads `CLAUDE.md`, **not** `AGENTS.md`. If the repo already has an `AGENTS.md` for
other coding agents, do not duplicate it — create a `CLAUDE.md` that imports it, so both tools
read one source:

```markdown
@AGENTS.md
```

Add any Claude-specific instructions below the import. A symlink also works, but on Windows it
needs Administrator or Developer Mode, so prefer the import. If there is no `AGENTS.md`, just
write `CLAUDE.md` directly.

## .gitignore

```
.venv/
.env
.env.*
!.env.example
__pycache__/
*.pyc
*.egg-info/
.coverage
.pytest_cache/
.mypy_cache/
.ruff_cache/
dist/
build/
*.db
.DS_Store
```
