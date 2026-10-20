---
name: write-fastapi-endpoints
description: >-
  Load this skill when writing FastAPI endpoints, services, or middleware: paths, status codes,
  error shapes, dependency injection, layer boundaries, logs, metrics, /health, CORS, rate limits.
  Auto-load when a route handler, domain exception, or log call is written.
disable-model-invocation: false
user-invocable: false
compatibility: >-
  Requires Python 3.12+ with `fastapi`, `pydantic`, `structlog`, and an ASGI server (`uvicorn`)
  installed as project dependencies via `uv sync` - none is assumed to be present globally. Running
  the app needs `uv` on PATH and a free local port. Exporting traces additionally needs a reachable
  OTLP collector endpoint; without one, logging still works and tracing is a no-op.
license: Apache-2.0
---

# Write FastAPI Endpoints

Write each endpoint as a thin route over a service, with one error contract and the service's
cross-cutting concerns wired in. Done when the route follows the layer boundaries and every error
leaves in the response shape below.

## Procedure

1. Pick the URL, method, and status code, and declare a `response_model`.
2. Keep the route handler thin: validate through a Pydantic model, call a service injected with
   `Depends`, return the result.
3. Raise a domain exception from the service and map it to HTTP once, in a global handler.
4. Log with structlog, carry the `correlation_id`, and keep the metrics and `/health` current.

## Rules

### REST API design

#### URL conventions

- Lowercase, hyphen-separated path segments: `/user-profiles`
- Plural nouns for collections: `/sessions`
- Nested resources for ownership: `/sessions/{id}/messages`. A resource that exists but belongs
  to another user returns the same status as a missing one, so the response never confirms it
  exists.
- No verbs in URLs — HTTP methods express the action. A non-CRUD action is a sub-resource:
  `POST /resources/{id}/archive`

#### HTTP status codes

Standard semantics apply. The choices this service makes explicitly:

- `409 Conflict` for an existing resource or an illegal state transition
- `422 Unprocessable Entity` for Pydantic validation failures
- `429 Too Many Requests` when a rate limit is exceeded
- `503 Service Unavailable` when a dependency is down (DB, upstream timeout)

Do not return `200` for errors. Do not return `500` for user input errors.

#### Error response shape

```json
{
  "error": {
    "code": "resource_not_found",
    "message": "Resource with ID res_abc123 does not exist.",
    "correlation_id": "req_xyz789"
  }
}
```

| Field            | Description                                          |
| ---------------- | ---------------------------------------------------- |
| `code`           | Machine-readable, snake_case, stable across versions |
| `message`        | Human-readable, safe to display                      |
| `correlation_id` | Propagated from the request for log tracing          |

#### Pagination

Every collection endpoint is paginated from its first release, because adding it later is a
breaking change for every client that read the whole list.

- Cursor-based by default: `GET /sessions?limit=50&cursor=<opaque>`. `limit` defaults to 50 and is
  capped at 100 with a Pydantic `Field(le=100)`, so a client cannot ask for the whole table.
- Response shape: `{ "items": [...], "next_cursor": "..." }`, with `next_cursor` `null` on the last
  page. The cursor is opaque to clients (base64 of the last row's sort key), so its contents can
  change without a version bump.
- The sort key is unique and stable, such as `(created_at, id)`, so rows inserted mid-scan are
  neither skipped nor repeated. The query is a keyset scan (see `ceh-python-service:write-postgresql-code`).
- Offset pagination (`?page=`) only for small, admin-only lists, where a page shifting under
  concurrent inserts does no harm.

#### API versioning

Prefer backward-compatible additions (new optional fields, new endpoints). Only version when a breaking change cannot be avoided. When required: use a URL prefix (`/v2/resources`), maintain `/v1/` for a documented deprecation period, and record the timeline in `ARCHITECTURE.md` Key Decisions.

During the deprecation period, every `/v1/` response carries `Deprecation: true` and a `Sunset`
header with the removal date (RFC 8594), so clients find out from the API, not from a changelog
they never read. Removing a field, renaming one, or making an optional request field required are
breaking changes. Adding an optional field or a new endpoint is not.

#### Headers

| Header                           | Direction          | Purpose                        |
| -------------------------------- | ------------------ | ------------------------------ |
| `X-Correlation-ID`               | Request + Response | Request tracing                |
| `Content-Type: application/json` | Both               | Required on all JSON endpoints |

### Layer boundaries

Each layer has one job. Route handlers are thin: validate input, call a service, return output.

- Route handlers contain no business logic — they call services.
- Services contain no SQL — they call the database layer. The database layer contains no business logic.
- One mutation path per aggregate — if multiple services could write the same entity, route them through a single state manager.

```python
router = APIRouter(prefix="/sessions", tags=["sessions"])


@router.post("", status_code=201, response_model=SessionResponse)
async def create_session(
    body: CreateSessionRequest,
    service: SessionService = Depends(get_session_service),
) -> SessionResponse:
    return await service.create(body.topic)
```

### Dependency injection

All dependencies in `app/core/dependencies.py`. Never instantiate services inside route handlers.

```python
@lru_cache
def get_settings() -> Settings:
    return Settings()


async def get_session_service(
    pool: asyncpg.Pool = Depends(get_db_pool),
    settings: Settings = Depends(get_settings),
) -> SessionService:
    return SessionService(pool=pool, settings=settings)
```

`@lru_cache` captures the environment at the first call, so a test that sets env vars after import
silently reads the old settings, database URL included. Override `get_settings` through
`app.dependency_overrides`, or call `get_settings.cache_clear()` in a fixture that runs first.

### Lifespan for startup and shutdown

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Pool sizing per ceh-python-service:write-postgresql-code (min_size=5, max_size=20, command_timeout=30)
    app.state.db_pool = await asyncpg.create_pool(
        settings.database_url, min_size=5, max_size=20, command_timeout=30
    )
    yield
    await app.state.db_pool.close()


app = FastAPI(lifespan=lifespan)
```

Do not use the deprecated `@app.on_event("startup")`.

### Response model

Declare `response_model=SomePydanticModel` on every route and return model instances.

### Middleware order

Register in this order (FastAPI processes in reverse registration order):

1. Correlation ID middleware (outermost)
2. CORS middleware
3. Rate limiting middleware
4. Request logging middleware (innermost)

### Correlation IDs

Every request carries a `correlation_id`:

- Generated at the API boundary if absent from request headers
- Bound to every log entry via `structlog.contextvars`
- Returned in the `X-Correlation-ID` response header
- Included in API error response bodies

```python
@app.middleware("http")
async def correlation_id_middleware(request: Request, call_next):
    # generate_id: prefixed ID helper, see ceh-python-service:write-postgresql-code
    correlation_id = request.headers.get("X-Correlation-ID", generate_id("req"))
    request.state.correlation_id = correlation_id
    with structlog.contextvars.bound_contextvars(correlation_id=correlation_id):
        response = await call_next(request)
    response.headers["X-Correlation-ID"] = correlation_id
    return response
```

### CORS configuration

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,  # from config — never wildcard in production
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE"],
    allow_headers=["Content-Type", "Authorization", "X-Correlation-ID"],
)
```

Never use `allow_origins=["*"]` in production.

A cookie that more than one endpoint sets (register, login, refresh) gets identical `path`,
`samesite`, `secure`, and `domain` everywhere. Different parameters create two cookies, and the
browser sends only one of them.

### Rate limiting

Apply to all mutating endpoints and expensive read endpoints. Return `429 Too Many Requests` with a `Retry-After` header when exceeded. Apply per session on mutation endpoints (e.g. 10 req/min).

### Input validation

- All request bodies validated through Pydantic models — reject with `422` on failure
- Use `ConfigDict(extra='forbid')` on models receiving externally-sourced input (API requests, LLM output), so an unknown field fails loudly instead of being dropped and hiding a typo or an injected key
- All LLM output must pass schema validation before any state mutation

### Global exception handlers

Register domain-to-HTTP mappings once in `app/core/middleware.py`:

```python
@app.exception_handler(SessionNotFoundError)
async def handler(request: Request, exc: SessionNotFoundError):
    return JSONResponse(
        status_code=404,
        content={
            "error": {
                "code": "session_not_found",
                "message": str(exc),
                "correlation_id": getattr(request.state, "correlation_id", None),
            }
        },
    )
```

The `correlation_id` comes from the correlation-ID middleware (registered outermost). Include it so
the body matches the error contract above (`code` / `message` / `correlation_id`).

### Exception hierarchy

Define in `app/core/exceptions.py`:

```python
class AppError(Exception):
    """Base exception for all application errors."""


class SessionNotFoundError(AppError): ...


class DomainValidationError(AppError):
    def __init__(self, reason: str) -> None:
        self.reason = reason
        super().__init__(reason)
```

- Services raise domain exceptions; global handlers map them to HTTP — never per-route
- Never raise `HTTPException` inside a service layer
- Never swallow exceptions silently with bare `except:`

### Structured logging

All log output is structured JSON. Never use `print()` or unstructured interpolation.

```python
import structlog

log = structlog.get_logger()

log.info("request_completed", endpoint="/resources", status=200, duration_ms=42)
log.warning("upstream_timeout", service="payment-api", attempt=2)
log.error("database_connection_failed", host=settings.db_host, error=str(e))
```

| Level     | Use for                                       |
| --------- | --------------------------------------------- |
| `DEBUG`   | Detailed diagnostics (disabled in production) |
| `INFO`    | Normal operations                             |
| `WARNING` | Unexpected but recoverable                    |
| `ERROR`   | Failures requiring attention                  |

Do not log at `INFO` on every request — use `DEBUG` for high-frequency events. Per-request counts
and latency already live in the metrics below, so an `INFO` line per request only adds volume.

**Never log:** secrets, tokens, passwords, PII, raw user-provided content, or full external API responses.

### Required metrics

| Metric                      | Type      | Labels                              |
| --------------------------- | --------- | ----------------------------------- |
| `requests_total`            | Counter   | `endpoint`, `method`, `status_code` |
| `request_duration_ms`       | Histogram | `endpoint`, `method`                |
| `errors_total`              | Counter   | `error_type`, `endpoint`            |
| `external_calls_total`      | Counter   | `service`, `status`                 |
| `external_call_duration_ms` | Histogram | `service`                           |

Use Prometheus-compatible instrumentation (`prometheus-fastapi-instrumentator` or equivalent).

### Health check endpoint

```
GET /health
```

Returns `200` when healthy:

```json
{ "status": "ok", "database": "ok", "version": "1.4.2" }
```

Returns `503` when any critical dependency is unavailable:

```json
{ "status": "degraded", "database": "error", "version": "1.4.2" }
```

Must verify actual database connectivity — not just process liveness. Used by load balancers, deployment pipelines, and rollback automation.
