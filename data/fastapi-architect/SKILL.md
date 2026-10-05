---
name: fastapi-architect
version: 1.0.2
description: Framework-specific delta on rest-api-architect — FastAPI 0.136 on Python 3.14. Feature layout, Pydantic v2 request/response separation, async DI with lifespan, URL-prefix versioning, RFC 9457 errors, in-house OAuth2+JWT or external IdP. Read rest-api-architect first for the cross-cutting REST conventions. Use when scaffolding or reviewing a FastAPI service.
---

# FastAPI Architecture

Targets **FastAPI 0.136** on **Python 3.14**. Companion to [python-architect](../../languages/python-architect/SKILL.md) and [sql-architect](../../databases/sql-architect/SKILL.md) (data access via `psycopg + .sql files`). Implementation skeletons in [RECIPES.md](RECIPES.md); pinned deps in [STACK.md](STACK.md).

## 1. Project structure — feature-based

One folder per bounded context. Each feature owns its router, service, repo, schemas, and SQL files. Full tree in [RECIPES.md](RECIPES.md).

- **`router.py`** depends on `service.py`; never reaches into `repo.py` directly.
- **`service.py`** is pure Python — no FastAPI imports. Easy to unit-test.
- **`schemas.py`** holds Pydantic models — never reused as ORM models or DB rows.

## 2. Routing & versioning

- **URL-prefix versioning:** `/v1/users`, `/v1/orders`. Mount each version's routers under a `v1_router = APIRouter(prefix="/v1")`. Deprecate by mounting `/v2` alongside, never by mutating `/v1`.
- **One `APIRouter` per feature**, included in `main.py`.
- **Tags** match feature folder names (`tags=["users"]`) — drives OpenAPI grouping.
- **Path parameter types in the signature** (`user_id: UUID`) — FastAPI validates and parses for free.
- **Response model declared per route** (`response_model=UserResponse`) — sets the contract and trims extra fields automatically.
- **Status codes explicit** (`status_code=status.HTTP_201_CREATED`).

## 3. Pydantic schemas — separate request and response

Three shapes per resource: `<Resource>Create` (POST body), `<Resource>Update` (PATCH partial), `<Resource>Response` (response body). Example in [RECIPES.md](RECIPES.md).

- **`extra="forbid"`** on every request model. Unknown fields are an error, not silent acceptance.
- **`SecretStr` / `SecretBytes`** for passwords, tokens. Stops accidental logging.
- **`Field(..., examples=[...])`** drives OpenAPI examples — clients get usable defaults.
- **Never reuse the same model for request and response.** Read-only fields leak into PATCH payloads otherwise.
- **Pydantic v2 validators:** `@field_validator` for per-field, `@model_validator(mode="after")` for cross-field invariants.

## 4. Dependency injection

- **Single source of shared state via `Depends`.** DB connections, HTTP clients, auth subjects — all injected, never imported as module-level globals.
- **Async dependencies** for anything I/O-bound: `async def get_db() -> AsyncIterator[AsyncConnection]: ...`.
- **Sub-dependencies** for layered composition: `get_current_user` depends on `decode_token` depends on `get_settings`. FastAPI resolves the graph and caches per-request.
- **Use type aliases** to keep route signatures clean (see [RECIPES.md](RECIPES.md)).

## 5. Lifespan & startup

Lifespan context is the only place to open/close shared resources (DB pool, HTTP client, cache, message bus). Never in module-level code or `@app.on_event` (deprecated). Settings loaded at startup, validated once via `pydantic-settings`. Skeleton in [RECIPES.md](RECIPES.md).

## 6. Authentication & authorization

**Patterns** (in-house JWT vs external IdP, Argon2id, JWT lifetimes, JWKS verification, switching criterion) live in [rest-api-architect/AUTH_PATTERNS.md](../../protocols/rest-api-architect/AUTH_PATTERNS.md). FastAPI-specific implementation:

- **Pattern A — in-house OAuth2 + JWT** uses FastAPI's `OAuth2PasswordBearer` + `pyjwt` + `argon2-cffi`. Dependency skeleton in [RECIPES.md](RECIPES.md).
- **Pattern B — external IdP** uses `pyjwt`'s `PyJWKClient` for JWKS verification; cache via `@lru_cache`. Verify `aud` and `iss` explicitly.
- **Authorization is route-level via dependencies, not middleware** — `dependencies=[Depends(require_scope("users:delete"))]` on the route. Skeleton in [RECIPES.md](RECIPES.md).

## 7. Error handling — RFC 9457 Problem Details

Every error returns `application/problem+json` with a standardised shape (per [rest-api-architect §7](../../protocols/rest-api-architect/SKILL.md#7-error-contracts--rfc-9457-problem-details)). Handler skeleton in [RECIPES.md](RECIPES.md).

- **One handler per domain-exception family.** Never let `HTTPException` and your custom exceptions return different shapes.
- **Validation errors** (`RequestValidationError`) get their own handler that maps Pydantic's error list into `Problem.detail`.
- **Never leak stack traces** in `detail`. Log them server-side with a correlation id; reference the id in the response.

## 8. Middleware

Order matters — outermost middleware sees the request first.

1. **CORS** (`CORSMiddleware`) — first, so preflights short-circuit before auth.
2. **Compression** (`GZipMiddleware`, min_size=1000).
3. **Request ID** (custom) — generate a UUID per request, attach to logs and response header.
4. **Logging** (custom) — structured logs with method, path, status, latency, request id.
5. **Auth** is a **dependency**, not middleware — per-route, lets unauthenticated endpoints (login, health) coexist cleanly.

## 9. Background tasks

- **`BackgroundTasks`** for genuinely fire-and-forget work that's tied to one response (sending a confirmation email, writing a metric). The task runs after the response is sent but in the same process — failures are invisible to the client.
- **Anything serious** (retryable, distributed, scheduled) belongs in a real task queue — flag for a future `task-queue-architect` skill. `BackgroundTasks` is not a queue.

## 10. Testing

- **`TestClient`** for end-to-end synchronous tests against the ASGI app.
- **`httpx.AsyncClient` with `ASGITransport`** for async tests that need to exercise async dependencies fully.
- **Override dependencies in tests** via `app.dependency_overrides[get_db] = ...`. Reset after the test.
- **DB fixtures:** run migrations into a per-test schema, or wrap each test in a rolled-back transaction (faster).
- **Snapshot the OpenAPI spec** in CI: `assert app.openapi() == json.load(open("tests/openapi.snapshot.json"))`. Catches accidental contract changes.

## 11. OpenAPI & docs

- **Tags, summaries, descriptions on every route.** They drive the rendered docs and SDK code generation.
- **`responses={...}`** to document non-default status codes with their shapes (`401`, `403`, `404`, `422`).
- **`include_in_schema=False`** on internal endpoints (health, metrics, debug).
- **Customise the spec** in `app.openapi()` to add `info.contact`, `servers`, `securitySchemes` — these aren't FastAPI defaults.

## 12. Performance

- **All routes are `async def`** unless they call a synchronous library and you've decided not to wrap it.
- **Never `time.sleep`, `requests`, or other blocking calls inside `async def`.** Block-detection: `asyncio.get_event_loop().slow_callback_duration = 0.1` in dev.
- **Run sync I/O in a thread:** `await asyncio.to_thread(blocking_fn, args)`.
- **Connection pooling:** open the DB pool once in `lifespan` (see §5); never `psycopg.connect()` per request.
- **`response_model_exclude_unset=True`** when returning a large model with many optional fields — avoids serialising defaults.
- **Pagination** at the API layer mirrors the SQL pattern (see [sql-architect §4](../../databases/sql-architect/SKILL.md)): cursor over offset.
