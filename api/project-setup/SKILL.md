---
name: python-project-setup
description: Python project setup guide. Use when creating a new Python project, configuring uv, setting up pyproject.toml, or bootstrapping a FastAPI service.
---

# Python Project Setup

## New Project Checklist

1. `uv init --package my-project`
2. Set `.python-version` to `>= 3.12`
3. Configure `pyproject.toml` (see `references/pyproject.template.toml`)
4. Create `src/{package}/` layout
5. Set up `tests/` with `conftest.py`
6. Add CI checks for `ruff format`, `ruff check`, `ty check`

## Rules

- **Must** use `uv` for package management
- **Must** use `src/` layout with package name matching project
- **Must** use lifespan for FastAPI startup/shutdown (not `@app.on_event`)
- **Must** add health check endpoint at `/health`
- **Must** use `pydantic-settings` with `.env` file support for config
- **Must** validate all environment variables at startup (fail fast)
- **Never** use `os.getenv()` directly—always go through settings model
- **Should** use versioned routers (`/api/v1/`)

See `references/pyproject.template.toml` for full project configuration.
See `references/fastapi-bootstrap.md` for minimal working FastAPI app.
