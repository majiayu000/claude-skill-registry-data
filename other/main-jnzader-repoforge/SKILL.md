---
name: add-main-endpoints
description: >
  Middleware and health endpoints for RepoForge Web application.
  Trigger: when initializing or extending the FastAPI main application.
license: Apache-2.0
metadata:
  author: repoforge
  version: "1.0"
complexity: low
token_estimate: 450
dependencies: []
related_skills: [add-repo-endpoint, add-user-model]
load_priority: high
---

<!-- L1:START -->
# add-main-endpoints

One sentence: Adds middleware and health check endpoints to the FastAPI app.

**Trigger**: when setting up the RepoForge Web application main entry point.
<!-- L1:END -->

<!-- L2:START -->
## Quick Reference

| Task | Pattern |
|------|---------|
| Add middleware | `add-middleware-pattern` |
| Health check | `health-endpoint-pattern` |
<!-- L2:END -->

<!-- L3:START -->
## Critical Patterns (Detailed)

### Pattern: correlation_id_middleware

Injects a unique correlation ID into each request context for distributed tracing.

```python
@app.middleware("http")
async def correlation_id_middleware(request: Request, call_next):
    import uuid
    request.state.correlation_id = str(uuid.uuid4())
    response = await call_next(request)
    response.headers["X-Correlation-ID"] = request.state.correlation_id
    return response
```

### Pattern: health endpoint

Provides basic and detailed health check endpoints for monitoring and load balancer checks.

```python
async def health() -> dict:
    return {"status": "ok"}

async def health_detailed() -> dict:
    return {"status": "ok", "database": "connected"}
```
## When to Use

- Adding request tracing and monitoring to the RepoForge Web app
- Configuring health checks for Docker container orchestration

## Commands

```bash
docker compose up -d repoforge
```

## Anti-Patterns

### Don't: Skip middleware setup

Omitting `correlation_id_middleware` or `security_headers_middleware` leaves the application vulnerable to request forgery and removes tracing capability.

```python
# BAD: Missing middleware registration
# app.add_middleware(...)  # not called
```
<!-- L3:END -->