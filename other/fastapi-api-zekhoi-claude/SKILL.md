---
name: fastapi-api
description: Implement or change HTTP endpoints in a FastAPI application following FastAPI's conventions and the project's own patterns, with Pydantic request and response models, dependency-injected authentication, correct status codes, and TestClient tests. Use when the user asks to add, change, or fix a route, router, dependency, or API endpoint in a project that uses FastAPI. Do not use for Flask, Django, or other frameworks, for reviewing code (use agent-kit:code-review), or for database query review (use agent-kit:sqlalchemy-review).
---

# FastAPI API implementation

## 1. Learn the application's structure

- Find how the app is built (`FastAPI()` instance or a `create_app` factory), how routers are included (`APIRouter`, `prefix`, `tags`), and the Pydantic major version (v2 `model_config`, `model_dump`; v1 `Config`, `dict`).
- Note existing dependencies for the database session, the current user, and permissions, exception handlers, and settings management.
- Read an existing route and its tests, and follow them, including sync or `async` style.

## 2. Implement the route

- Add the route to the matching `APIRouter`. Separate input and output models (`UserCreate`, `UserRead`) and set `response_model` or a return annotation so fields such as password hashes are never serialized. Output models that validate ORM objects need `model_config = ConfigDict(from_attributes=True)` (v1: `orm_mode = True`).
- Use path, query, and body parameters with types and constraints (`Annotated[int, Path(gt=0)]`, `Field`) so FastAPI validates input and returns 422 on bad data.
- Raise `HTTPException` (or the project's error types) with the right status for missing resources and client mistakes; set `status_code=201` on creation and 204 with no body on deletion.
- Get the session, current user, and permissions through `Depends`, never globals. Protect anything not explicitly public; if no authentication exists and the endpoint exposes user data, say so and ask before shipping it unprotected.
- Do not call blocking I/O (sync database drivers, `requests`, `time.sleep`) inside `async def`; use `def` endpoints or async libraries.
- Use the project's logger, never `print`, and never log credentials or tokens.

## 3. Test

- Test through `fastapi.testclient.TestClient` or `httpx.AsyncClient` with `ASGITransport`, overriding dependencies with `app.dependency_overrides` and clearing them after each test.
- Cover the success response and its shape, validation failures (422), missing resources (404), and authorization failures where relevant.
- Run the project's tests and type checker.

## 4. Report

Summarize the routes added or changed, the models and dependencies used, the tests and their results, and any assumptions, such as authentication decisions, that the user should confirm.

## Examples

- Use: "Add a POST /users/{id}/deactivate endpoint." "Add pagination to GET /orders."
- Skip: "Review app/routes/users.py." (code review) "Add a Flask blueprint." (other framework)
