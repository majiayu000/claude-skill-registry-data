---
name: scaffold-fullstack-web
description: >-
  Load this skill when starting or scaffolding a new fullstack web app (Python service + web
  frontend in one repo): laying out the backend and frontend trees side by side and writing a
  combined .gitignore. Trigger when the user says "start/scaffold a fullstack web app" or sets up a
  monorepo with both a FastAPI backend and a Svelte/React frontend.
compatibility: >-
  Requires both toolchains, since this scaffolds a Python service and a web frontend side by side:
  Python 3.12+ with `uv` for the backend, and `bun` (or Node.js 20+ with npm) for the frontend,
  plus network access to PyPI and the npm registry. Running the stack also needs a reachable
  PostgreSQL instance. None of these is assumed installed.
---

# Scaffold a Fullstack Web App

A fullstack repo is the composition of a Python service and a web frontend. Scaffold each side per its
own skill, then place them side by side.

```
project/
├── backend/                # see scaffold-python-service
│   ├── app/{api,core,models,services,db}/
│   └── tests/{unit,integration,system}/
├── frontend/               # see scaffold-web-frontend
│   └── src/{lib,routes}/
├── migrations/             # Alembic
└── .gitignore              # combined entries below
```

Keep the two stacks independently buildable and testable — the backend exposes an API; the frontend
consumes it through its `src/lib/api` client. Do not share runtime code across the boundary.

## Combined .gitignore

```
# Python
.venv/
__pycache__/
*.pyc
*.egg-info/
.coverage
.pytest_cache/
.mypy_cache/
.ruff_cache/
*.db

# Node / frontend
node_modules/
.svelte-kit/

# Build output (both)
dist/
build/

# Secrets / env
.env
.env.*
!.env.example

# OS
.DS_Store
```
