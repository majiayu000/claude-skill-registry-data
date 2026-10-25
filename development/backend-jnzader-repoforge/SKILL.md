---
name: backend-layer
description: >
  Python FastAPI backend layer for RepoForge Web. Handles HTTP routing, middleware, authentication, rate limiting, and database migrations. Owns all server-side request processing and API endpoints.
  Trigger: When working in backend/ directory and its main responsibility
license: Apache-2.0
metadata:
  author: repoforge
  version: "1.0"
  complexity: medium
  token_estimate: 1200
  dependencies: []
  related_skills: [frontend-layer, build_modules-layer]
  load_priority: high
---

<!-- L1:START -->
# backend-layer

The Python FastAPI backend layer for RepoForge Web, handling HTTP routing, middleware, authentication, rate limiting, and database migrations. Owns all server-side request processing and API endpoints.

**Trigger**: When working in `backend/` directory — adding routes, modifying middleware, debugging authentication, or extending API endpoints.
<!-- L1:END -->

<!-- L2:START -->
## Quick Reference

| Task | Pattern |
|------|---------|
| Run migrations | `cd apps/server && alembic upgrade head` |
| Start server | `uvicorn apps.server.main:app --reload` |
| Test endpoints | `pytest apps/server/tests/` |

## Critical Patterns (Summary)
- **Middleware Chain**: FastAPI middleware runs in order — correlation_id → request_logging → security_headers. Each must call `call_next` to pass control.
- **Settings Fail-Fast**: `Settings` from `config.py` validates required env vars on startup; missing vars cause immediate exit.

## Critical Patterns (Detailed)

### Middleware Chain

FastAPI middleware executes in declaration order. Each handler must invoke `call_next` to forward the request; omitting this breaks the chain and returns 500 errors.

```python
@app.middleware("http")
async def security_headers_middleware(request: Request, call_next):  # noqa: ANN001
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response
```

### Settings Fail-Fast

```python
from apps.server.app.config import Settings

settings = Settings()  # Raises ValueError if required vars missing
```

## When to Use

- Adding new HTTP routes or API endpoints
- Modifying request validation or authentication flow
- Configuring rate limits or adding middleware
- Running or writing database migrations

## Adding a New middleware

1. Create `<name>.py` in `apps/server/app/middleware/`
2. Export a FastAPI dependency or middleware function following existing pattern
3. Add to middleware chain in `apps/server/app/main.py` if needed
4. Verify with `pytest apps/server/tests/middleware/`

## Commands

```bash
cd apps/server && alembic upgrade head       # Run migrations
uvicorn apps.server.main:app --reload        # Start dev server
pytest apps/server/tests/                    # Run test suite
```

## Anti-Patterns

### Don't: Skip `call_next` in middleware

```python
@app.middleware("http")
async def bad_middleware(request: Request, call_next):
    # BUG: Missing call_next — request never proceeds
    return JSONResponse({"error": "chain broken"}, status_code=500)
```

**Why**: Without calling `call_next`, the middleware short-circuits the entire request pipeline, returning a 500 error to the client and breaking all downstream handlers.

<!-- L3:END -->