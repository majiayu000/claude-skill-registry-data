---
name: fastapi
description: Use when building APIs with FastAPI. Covers dependency injection, Pydantic v2 validation, async database access, authentication, background tasks, and testing.
metadata:
  category: backend
  version: 1.0.0
  tags: [fastapi, python, pydantic, async, api]
---

# FastAPI

## Purpose

Build FastAPI services that use the framework's strengths — declarative validation and dependency injection — without falling into its two standard traps: blocking calls inside `async def`, and business logic in the route handler.

## When to Use

- Building or reviewing a FastAPI application.
- Structuring dependencies, authentication, and database sessions.
- Diagnosing latency that appears only under concurrency.
- Writing tests for FastAPI endpoints.

## Capabilities

- Route and router organization.
- Pydantic v2 models for request, response, and settings.
- Dependency injection with scoped lifecycles.
- Async SQLAlchemy sessions, correctly scoped per request.
- Authentication and authorization dependencies.
- Testing with `httpx.AsyncClient` and dependency overrides.

## Inputs

- The API contract and the data layer.
- Whether the workload is I/O-bound (nearly always) or CPU-bound.

## Outputs

- Thin route handlers delegating to service functions.
- Response models that control exactly what is serialized.
- A test suite that overrides dependencies rather than mocking internals.

## Workflow

1. **Define the schemas** — Separate request, response, and internal models. Never return an ORM object directly; a `response_model` is your defense against leaking a password hash.
2. **Build the dependencies** — Database session, current user, feature flags. These are the injection points that make the app testable.
3. **Keep handlers thin** — Parse, authorize, delegate, return. Business logic lives in a service module that knows nothing about HTTP.
4. **Get async right** — In an `async def` handler, every I/O call must be awaited. A blocking call there stalls the entire event loop, not just that request.
5. **Test through the app** — `httpx.AsyncClient` with `app.dependency_overrides` gives you real routing, real validation, and a fake database.

## Best Practices

- A blocking call inside `async def` (a sync DB driver, `requests`, `time.sleep`) blocks every concurrent request on that worker. If a handler must call blocking code, define it as `def` — FastAPI runs it in a thread pool.
- Always set `response_model`. Without it, whatever your service returns is what the client sees, including fields you added last week.
- Use `Annotated[Session, Depends(get_session)]` — it keeps signatures readable and reusable.
- Validate settings with `pydantic-settings` at startup. Fail to boot on a bad config rather than at 3am on the first request that touches it.
- `BackgroundTasks` runs in the same process and dies with it. For anything that must not be lost, use a real queue.
- Mount routers by domain, not by HTTP verb.

## Examples

**Dependency-injected handler and an overridable test:**

```python
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter(prefix="/orders", tags=["orders"])

SessionDep = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post("", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
async def create_order(
    payload: OrderCreate,
    session: SessionDep,
    user: CurrentUser,
) -> Order:
    try:
        return await orders.place(session, customer_id=user.id, items=payload.items)
    except InsufficientInventory as e:
        raise HTTPException(status.HTTP_409_CONFLICT, detail=str(e)) from e
```

```python
@pytest.fixture
async def client(session: AsyncSession) -> AsyncIterator[AsyncClient]:
    app.dependency_overrides[get_session] = lambda: session
    app.dependency_overrides[get_current_user] = lambda: User(id="usr_test")
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c
    app.dependency_overrides.clear()
```

## Notes

- Pydantic v2 is roughly an order of magnitude faster than v1 on validation, but `Config` classes, validators, and `.dict()` all changed. Do not mix idioms.
- `@lru_cache` on a settings factory is the standard way to make configuration a singleton dependency.
- FastAPI's generated OpenAPI schema is only as good as your response models and status codes. Treat the generated docs as a review artifact.
