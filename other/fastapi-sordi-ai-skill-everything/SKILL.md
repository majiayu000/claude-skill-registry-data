---
name: fastapi
description: Apply when building FastAPI endpoints, Pydantic models, or async APIs. Covers routing, dependency injection, error handling, testing, and OpenAPI hygiene.
license: MIT
version: 1.0.0
tokens_target: 2000
triggers:
  - fastapi endpoint
  - pydantic model
  - async api
loads_after:
  - python
supersedes: []
---

# Sub-Skill: FastAPI

**Purpose:** Prevent common FastAPI and Pydantic mistakes. Apply these rules whenever writing or reviewing FastAPI route handlers, Pydantic schemas, or async API code.

---

## Rules

1. **Always** declare request and response bodies as Pydantic models — never use raw `dict` or `Any` for I/O. Reference: ERR-2026-025

2. **Always** use Pydantic v2 syntax (`model_config`, `model_dump`, `model_validate`) unless the project explicitly pins Pydantic v1 (`pydantic<2` in requirements). Reference: ERR-2026-025

3. **Always** declare route handlers as `async def` unless the handler calls blocking I/O that cannot be awaited; use `run_in_executor` for blocking calls inside async handlers.

4. **Always** specify an explicit `response_model` on every route decorator so FastAPI filters and validates the response shape.

5. **Always** use `status_code` on the route decorator (`@app.post("/items", status_code=201)`) rather than constructing a `Response` object just to set the status.

6. **Never** raise bare `Exception` in route handlers; raise `HTTPException` with a meaningful `status_code` and `detail` string, or define a custom exception with an exception handler.

7. **Always** register exception handlers via `@app.exception_handler(MyError)` for domain errors rather than catching them inside every route.

8. **Use** `Depends()` for shared logic (auth, DB sessions, pagination params) — never duplicate the same logic across multiple route functions.

9. **Prefer** `APIRouter` with a `prefix` and `tags` list to group related endpoints; register routers with `app.include_router()` rather than defining all routes on the app object.

10. **Always** configure CORS via `CORSMiddleware` with an explicit `allow_origins` list; never use `allow_origins=["*"]` in production.

11. **Use** the `lifespan` context manager (FastAPI ≥ 0.93) for startup/shutdown logic instead of the deprecated `@app.on_event("startup")` / `@app.on_event("shutdown")` decorators.

12. **Always** use `BackgroundTasks` (injected via `Depends` or as a route parameter) for fire-and-forget work; never `asyncio.create_task` inside a route without a lifecycle guard.

13. **Avoid** exposing internal field names in OpenAPI by setting `model_config = ConfigDict(populate_by_name=True)` and using `alias` or `alias_generator` when the wire format differs from the Python attribute name.

14. **Use** `pydantic-settings` (`BaseSettings`) for configuration; never read `os.environ` directly inside route handlers or dependency functions.

15. **Always** test FastAPI routes with `TestClient` (sync) or `AsyncClient` from `httpx` (async); never spin up a real server in unit tests.

16. **Ensure** path operation functions declare only the parameters they actually use; unused `Request` injections or stale `Depends` imports are dead code and confuse readers.

17. **Before** adding a new route, check whether an existing router already owns that resource prefix; adding routes to the wrong router breaks OpenAPI tag grouping.

18. **Never** store mutable state in module-level variables inside route modules; use dependency-injected singletons or `app.state` instead.

---

## See also

- `skills/python/SKILL.md`
- `skills/code-quality/SKILL.md`
