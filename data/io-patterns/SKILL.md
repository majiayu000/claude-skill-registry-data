---
name: python-io
description: Python I/O patterns. Use when working with async, HTTP clients, database sessions, SQLModel, dependency injection, or concurrency.
---

# Python I/O Patterns

## HTTP Clients

- **Must** use `httpx.AsyncClient` for all async HTTP requests
- **Must** type responses with Pydantic models at the call boundary
- **Must** create client in FastAPI lifespan, close on shutdown
- **Must** set explicit timeouts on all requests
- **Never** create a new client per request—reuse a singleton

## Async Rules

- **Must** use async for network I/O (HTTP, database, queues)
- **Must** set explicit timeouts on all network I/O—no implicit infinite waits
- **Should** use `asyncio.TaskGroup` (3.11+) over bare `gather()` for structured concurrency
- **Should** use `Semaphore` to limit concurrency in bulk operations
- **Avoid** async for CPU-bound work—use `asyncio.to_thread()`
- **Never** block the event loop with sync I/O
- **Never** catch and ignore `asyncio.CancelledError`—let it propagate

## Database Sessions (SQLModel + Async)

- **Must** use async sessions with `async_sessionmaker` and `AsyncSession`
- **Must** use one session per request, managed via `Depends()`
- **Must** set `expire_on_commit=False` for async sessions
- **Should** separate read and write session factories if using read replicas
- **Never** share sessions across requests or store in global state

## Dependency Injection

- **Must** use FastAPI `Depends()` for request-scoped dependencies
- **Must** initialize singletons (HTTP clients, config) in lifespan
- **Should** use `Annotated` types for cleaner dependency signatures (e.g., `SessionDep = Annotated[AsyncSession, Depends(get_session)]`)
- **Should** rely on `Depends()` caching—same dependency in a request tree returns same instance
