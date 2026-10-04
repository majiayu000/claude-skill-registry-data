---
name: fastapi-route-change
description: Use when adding or changing FastAPI routes, dependencies, middleware, or API response behavior.
---

# FastAPI Route Change

Follow `AGENTS.md` first.

## Workflow

1. Inspect neighboring route modules in `pubtator_link/api/routes/` and reuse existing dependency and error-response patterns.
2. Keep route handlers thin; place business behavior in `pubtator_link/services/`.
3. Validate request and response shapes with Pydantic models instead of ad hoc dictionaries.
4. Cover route behavior under `tests/test_routes/` and service behavior under `tests/unit/`.
5. For hosted-facing changes, check CORS, request-size, rate-limit, URL safety, and logging implications.
6. Run the focused route/service tests, then `make ci-local` before handoff.
