---
name: fastapi-sqlmodel-crud-patterns
description: >
  Standard patterns for building and maintaining CRUD APIs with
  FastAPI and SQLModel: models, routers, database access, and
  error handling in a reusable way.
---

# FastAPI + SQLModel CRUD Patterns Skill

## When to use this Skill

Use this Skill whenever you are:

- Creating or modifying CRUD (Create, Read, Update, Delete) endpoints
  in a FastAPI application that uses SQLModel for persistence.
- Designing new resources (e.g. Task, UserProfile, Project, Order)
  and their REST endpoints.
- Refactoring existing API code to be more consistent and reliable.
- Adding tests or changing database access patterns related to CRUD.

This Skill must work for **any** FastAPI + SQLModel project, not just
a single repository.

## Core goals

- Keep CRUD code **consistent, predictable, and easy to reuse** across
  many projects.
- Separate concerns:
  - Models (SQLModel) in one place.
  - Routers (FastAPI endpoints) in another.
  - Database session management in a dedicated module.
- Use **clear REST semantics** (HTTP verbs, status codes, resource paths).
- Provide **strong typing** via SQLModel and Pydantic models.
- Handle errors and not-found cases cleanly, without crashes. [web:53][web:59]

## Architecture assumptions

- Web framework: FastAPI.
- ORM: SQLModel (sync or async, but pick one style per project).
- Database: Any SQL database supported by SQLModel (e.g. PostgreSQL). [web:53][web:57]
- Structure:
  - `db.py` or similar: session creation and engine.
  - `models.py` or `models/`: SQLModel models.
  - `routers/` or `routes/`: FastAPI routers per resource.
  - `main.py`: FastAPI app entrypoint registering routers.

The exact filenames can differ between projects; the patterns stay the same.

## Resource and endpoint conventions

- Each logical resource (e.g. `Task`, `Item`, `User`) should have its
  own router module, for example:

  - `routers/tasks.py` with a `APIRouter(prefix="/tasks", tags=["tasks"])`.

- Typical REST endpoints per resource:

  - `GET /<resource>` → list items.
  - `POST /<resource>` → create item.
  - `GET /<resource>/{id}` → get single item.
  - `PUT /<resource>/{id}` → replace item.
  - `PATCH /<resource>/{id}` → partial update (optional).
  - `DELETE /<resource>/{id}` → delete item. [web:53][web:59]

- Resource names should be plural in paths (`/tasks`, `/users`), with
  singular nouns used in model/type names (`Task`, `User`).

## Models and schemas

- Use SQLModel models for database tables, with:

  - Primary key fields (`id` or similar).
  - Optional timestamps (e.g. `created_at`, `updated_at`) when useful.
  - Reasonable defaults and constraints (e.g. `nullable`, `max_length`).

- When needed, define separate Pydantic/SQLModel schemas for:

  - Create input (e.g. `TaskCreate`) – fields required for creation.
  - Update input (e.g. `TaskUpdate`) – optional fields for partial updates.
  - Response model (e.g. `TaskRead`) – what the API returns.

- Avoid exposing internal-only fields (e.g. secrets) in response models.

## Database session handling

- Provide a shared dependency for DB sessions, for example:

  - `get_session()` in `db.py` that yields a `Session` object.

- Use `Depends(get_session)` in routers to access the database.

- Do not create database engines or sessions directly inside routers
  or endpoint functions. Keep connection logic centralized. [web:53][web:57]

## CRUD behaviour patterns

For each resource, the default CRUD behaviour should follow this pattern:

- **Create** (`POST`):

  - Validate input using a dedicated schema if needed.
  - Construct the SQLModel instance from the validated data.
  - Add and commit the instance using the shared session.
  - Refresh the instance to return updated fields (e.g. autoincrement id).

- **List** (`GET` collection):

  - Return a list of items, optionally with pagination, filtering, or
    sorting based on query parameters.
  - Avoid returning unbounded, huge result sets when possible.

- **Get** (`GET` single):

  - Fetch the item by primary key.
  - If not found, raise `HTTPException(status_code=404)` with a clear
    message.

- **Update** (`PUT`/`PATCH`):

  - Load the existing item; if not found, return 404.
  - Apply allowed changes from the input schema.
  - Commit and refresh before returning the updated item.

- **Delete** (`DELETE`):

  - Load the existing item; if not found, return 404.
  - Either hard-delete or soft-delete depending on the project’s rules.
  - Return appropriate status (e.g. 204 No Content for hard delete).

## Error handling

- Never let database or Python exceptions leak directly to clients.
  Use `HTTPException` with appropriate status codes and simple, safe
  error messages. [web:53][web:59]

- Common error cases:

  - Resource not found → 404.
  - Validation errors → 422 (FastAPI will handle many of these).
  - Unauthorized/forbidden (if auth is applied) → 401/403.

- Log details server-side if needed, but keep responses simple.

## Typing and response models

- Always declare response models in router decorators when practical:

  - `response_model=TaskRead` or `List[TaskRead]`.

- This improves:

  - OpenAPI docs.
  - Type checking in clients.
  - Clarity of what each endpoint returns.

- Avoid returning raw dicts or mixing data shapes; keep responses
  consistent.

## Filtering, sorting, and pagination (optional)

- When adding filtering/sorting:

  - Use query parameters (e.g. `status`, `sort_by`, `order`).
  - Document default behaviours and limits in the resource spec.

- For pagination:

  - Use standard patterns like `limit` and `offset` or page/size pairs.
  - Enforce maximum limits to avoid performance issues.

## Things to avoid

- Creating engines or sessions inside endpoint functions.
- Mixing business logic, validation, and database operations in large
  monolithic functions; prefer small helpers where appropriate.
- Returning raw SQLModel instances that include internal fields that
  should not be exposed.
- Using inconsistent status codes for the same error conditions.

## References inside the repo

When present, this Skill should align with:

- `db.py` or equivalent – engine and `get_session` dependency.
- `models.py` or `models/` – SQLModel models for resources.
- `routers/` or `routes/` – resource-specific routers.

If these files are missing, propose creating them using these patterns
rather than inventing a new, ad-hoc CRUD style for each resource.
