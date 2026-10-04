---
name: python-fastapi-setup
description: "FastAPI service setup: app/main.py, API routers, pydantic-settings, lifespan/app.state services, middleware, health checks, pytest/TestClient, Uvicorn, Gunicorn/uvicorn-worker, Docker/Compose. Use for scaffolding or modernizing Python API services; skip for Flask/Django-only, frontend-only, non-Python APIs, or Supabase-specific work."
---

# Python FastAPI Setup

## Overview

Create or modernize FastAPI services around a small repeatable structure:

```text
app/main.py -> app/core/config.py -> app/api/v1/endpoints/ -> middleware -> tests -> deployment
```

Prefer direct startup commands, typed settings, explicit lifespan ownership for process-level resources, and a minimal test suite. Keep the scaffold boring on purpose: a future maintainer should be able to find the app, settings, routers, health check, and startup command without hunting through wrapper scripts.

## Workflow

1. Classify the workspace before writing files.
   - Treat the target as greenfield if it is empty or the user asks for a new service.
   - Treat it as existing if it has Python source, `pyproject.toml`, `requirements.txt`, an ASGI app, tests, Docker files, CI, or git history.
   - For existing projects, inventory the current entrypoint, router layout, dependency manager, settings pattern, middleware, tests, deployment files, and startup commands before editing.

2. For greenfield scaffolds, run the bundled script from this skill directory:

```bash
python3 scripts/scaffold_fastapi_project.py \
  --name inventory_api \
  --out /path/to/inventory_api
```

   - The scaffold always generates `gunicorn.conf.py`, Docker, and Compose files for a production-ready default.
   - The scaffold script renders reusable project and deployment configuration from `assets/` for `pyproject.toml`, Docker, Compose, and Gunicorn. Update those assets when the shared standard changes; update the Python script when generation logic, arguments, app files, or dependency policy change.
   - Read `references/python-fastapi-blueprint.md` before changing generated files or adding new script options.

3. For existing projects, patch conservatively.
   - Preserve working endpoints and behavior.
   - Before moving routes, record the existing endpoint contract: path, method, status code, response shape, sample payloads, headers, and any query/path parameters visible in the current code or tests.
   - Add or update regression tests for those existing contracts before or during the refactor. The tests should assert the old payloads and status codes, not newly invented placeholder data.
   - Move toward `app/main.py` only when it improves clarity or matches the user's request.
   - Retire wrapper launchers such as `run_service.py` after replacing them with documented direct commands.
   - Keep the repo's dependency manager unless there is a clear reason to change it.
   - Add only the modules and settings the service actually uses.
   - Do not replace legacy route payloads, IDs, names, or response field types with new sample fixtures just because the code moved into a cleaner module.

4. Keep app composition in one place.
   - Export the ASGI app as `app = create_app()` or `app = FastAPI(...)` from `app/main.py`.
   - Register routers, middleware, and lifespan from `app/main.py`.
   - Use FastAPI lifespan for startup/shutdown resources such as connection pools, long-lived clients, thread pools, background processors, model handles, or service instances.
   - Store process-level instances on `app.state` and expose them through typed dependency accessors instead of making endpoints know raw `app.state` keys.

5. Centralize settings.
   - Prefer `pydantic-settings` with a small `Settings` class in `app/core/config.py`.
   - Use an `lru_cache` settings getter when settings are read repeatedly.
   - Keep `.env.example` safe: placeholders and local defaults only, no secrets.

6. Split routers predictably.
   - Put route modules under `app/api/v1/endpoints/` for new services unless the repo already has a better convention.
   - Keep `/health` lightweight and available at the root path unless the existing service defines a different health contract.
   - Add domain routers only when requested or clearly needed.

7. Choose deployment commands by environment.
   - Local development: `uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload`
   - Local smoke test: `uvicorn app.main:app --host 0.0.0.0 --port 8000`
   - Production default: use Gunicorn with the external `uvicorn-worker` package, for example `gunicorn -c gunicorn.conf.py app.main:app`.
   - Container default: run the same Gunicorn command from `gunicorn.conf.py`; let Kubernetes, Compose, or the platform replicate containers.
   - Do not use `uvicorn.workers.UvicornWorker` in new code; Uvicorn documents that module as deprecated.

8. Add tests and validation.
   - Add at least one `TestClient` test for `/health`.
   - For existing projects, add regression tests for each migrated legacy endpoint whose behavior the user asked to preserve.
   - Keep baseline tests free of network, database, or cloud dependencies.
   - Run the strongest available checks and report skipped checks with the missing dependency.

## Default Structure

Prefer this layout for greenfield services:

```text
app/
  __init__.py
  main.py
  core/
    __init__.py
    config.py
  api/
    __init__.py
    v1/
      __init__.py
      router.py
      dependencies.py
      endpoints/
        __init__.py
        health.py
  middleware/
    __init__.py
    request_context.py
tests/
  test_health.py
pyproject.toml
gunicorn.conf.py
Dockerfile
docker-compose.yml
.dockerignore
.env.example
.gitignore
README.md
```

Add CI, database modules, schemas, services, or auth only when the user asks for them or the existing project already needs them.

## File Standards

### `app/main.py`

- Own app creation, lifespan, middleware, and router registration.
- Keep business logic out of the entrypoint.
- Use a `create_app()` factory when tests or configuration need a fresh app instance.

### `app/core/config.py`

- Own typed settings and environment loading.
- Keep settings flat until the service has enough domains to justify nesting.
- Ignore unknown environment keys so local `.env` files can contain unrelated variables without breaking imports.

### `app/api/v1/dependencies.py`

- Own FastAPI dependency functions and typed accessors.
- Read process-level services from `request.app.state`.
- Avoid constructing expensive services inside endpoint functions.

### `app/middleware/`

- Keep custom middleware focused.
- Include request ID middleware when traceability matters.
- Add CORS only for browser-facing APIs or when requested.

### `pyproject.toml`

- Keep runtime dependencies separate from optional dev/prod extras.
- Include unpinned `fastapi`, `uvicorn[standard]`, `pydantic-settings`, `gunicorn`, and `uvicorn-worker` for the default scaffold so pip resolves current compatible releases.

### Docker Files

- Build from an official Python slim image unless the repo has a stronger base-image standard.
- Use exec-form `CMD`.
- Prefer one process per container.
- Add a health check against `/health`.

## Validation

Use the strongest checks that work locally:

```bash
python3 -m py_compile app/main.py app/core/config.py app/api/v1/router.py app/api/v1/endpoints/health.py
python3 -m pytest
uvicorn app.main:app --host 0.0.0.0 --port 8000
curl -fsS http://127.0.0.1:8000/health
```

```bash
gunicorn -c gunicorn.conf.py app.main:app
curl -fsS http://127.0.0.1:8000/health
```

If the user wants container verification, run:

```bash
docker build -t fastapi-smoke .
docker run --rm -p 8000:8000 fastapi-smoke
curl -fsS http://127.0.0.1:8000/health
```

Do not claim validation that did not run. If `fastapi`, `uvicorn`, `pytest`, Docker, or Gunicorn are missing, report the exact skipped command and the missing tool.

## References

- Read `references/python-fastapi-blueprint.md` when choosing layout, lifespan/dependency patterns, deployment commands, Docker behavior, or eval expectations.
- Read `scripts/scaffold_fastapi_project.py` before changing generated files or adding script options.
- Read `assets/` before changing generated `pyproject.toml`, Docker, Compose, or Gunicorn configuration; treat those files as templates and keep service-specific values behind `@PLACEHOLDER@` variables.
