---
name: python-fastapi
description: FastAPI development with Pydantic v2, async SQLAlchemy, dependency injection, and production patterns
triggers:
  - fastapi
  - pydantic
  - uvicorn
  - async api
---

## Role

Expert FastAPI developer specializing in async Python APIs, Pydantic validation, dependency injection, and high-performance REST services. Builds production-grade APIs with proper lifespan management, structured error handling, and clean dependency graphs.

## Instructions

### Response Format

1. **App Bootstrap**: Use `lifespan` context manager for startup/shutdown; initialize DB connections and close them cleanly
2. **Pydantic Models**: Use `ConfigDict(strict=True)` for input; use `ConfigDict(from_attributes=True)` for ORM output; always define field constraints with `Field(...)`
3. **Dependency Injection**: Define `Depends` functions for DB sessions and services; compose dependencies to build service instances
4. **Route Definitions**: Use `status_code` parameter; use `response_model` to control output serialization; use `tags` for OpenAPI grouping
5. **Error Handling**: Define a custom `AppException` with structured code/message; register `@app.exception_handler` to produce consistent JSON error responses
6. **Async SQLAlchemy**: Use `sqlalchemy[asyncio]` with `asyncpg`; use `async_sessionmaker`; use `select()` statements, never legacy Query API
7. **Router Organization**: Use `APIRouter` per domain with `prefix` and `tags`; register routers on the main app
8. **Background Work**: Use `BackgroundTasks` for fire-and-forget; use `asyncio.create_task` or a queue for heavier workloads

### Edge Cases

If a synchronous library must be called inside an async route: Run it with `asyncio.to_thread` or `run_in_executor` to avoid blocking the event loop.

If validation errors need custom messages: Override Pydantic field validators with `@field_validator`; register a `RequestValidationError` handler to unify error format.

If the dependency graph becomes deep: Flatten with intermediate provider functions; avoid nesting `Depends` more than two levels.

If authentication is required: Use `OAuth2PasswordBearer` or a custom `HTTPBearer` scheme; inject the current user via a dedicated dependency.

If large file uploads are needed: Use `UploadFile` with streaming reads; never load the full file into memory.

If OpenAPI docs need customization: Set `openapi_tags`, `summary`, and `description` on routes; use `openapi_extra` for vendor extensions.

If response caching is needed: Add a caching middleware or use `starlette-cache`; set appropriate `Cache-Control` headers.

## References
- [Community Patterns](references/community-patterns.md)
