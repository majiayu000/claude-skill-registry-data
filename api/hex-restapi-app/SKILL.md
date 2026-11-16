---
name: hex-restapi-app
description: Use when bootstrapping a FastAPI shell once per project, or changing request handling shared by every route — `restapi/main.py`, `restapi/error_handler.py`, `restapi/schemas/errors.py`, app lifecycle, CORS, middleware, central error translation and the HTTP status each error class maps to. Not one resource's router (`hex-restapi-endpoint`) or its wire models (`hex-restapi-schema`).
---

# Hex REST App

The shell every route lands inside, and the middleware layers that wrap it. The shell is laid once per project so subsequent work (`hex-restapi-endpoint`, `hex-restapi-schema`) has somewhere to go; a middleware is added whenever a cross-cutting per-request concern appears. After bootstrap, the only file this skill ever touches again is `restapi/main.py` (when a router or a middleware is registered), and a router's line is normally folded into the consuming skill.

## When to use vs. neighbours

- Laying the FastAPI entrypoint for the first time, or adding a middleware that wraps every route → this skill.
- A new router added afterwards, or logic for one route → `hex-restapi-endpoint`, a thin route over an application handler that also `app.include_router(...)`s itself.
- A resource's request/response models added into the `schemas/` package this skill creates → `hex-restapi-schema`.
- A new domain exception is plumbed → `exception-catalog` (creates/extends `domain/exceptions.py`); the HTTP status it answers with is this skill's `STATUS_BY_ERROR`, where a refinement needs no entry of its own.
- A middleware introducing a new HTTP status → this skill, *Registering a middleware's status* under `## Middleware`.
- Authenticating a caller or gating a route on a role → `hex-restapi-auth`; route auth is a FastAPI dependency, not a middleware, and it is optional — this shell is complete without it.
- Which error codes a route advertises → `hex-restapi-endpoint`.
- Constructing or extending the composition root this shell attaches → `hex-wiring`.
- Creating the application handlers routes receive from it → `hex-application`.
- Whether the service should be hexagonal at all → `architecture-choice`; the project substrate and dependencies around this shell, and the migration bootstrap where the service owns a relational schema → `hex-project-setup`; lint and type-check configuration → `python-toolchain`.
- An HTTP service with no rules of its own to protect — internal CRUD over its store, a webhook, a proxy → `flat-entrypoint`'s HTTP trigger shape, in the `pyhouse-flat` plugin, once `architecture-choice` has settled the family.
- Middleware class naming and the `restapi/middleware/` package layout → `naming` and `python-packaging`.
- The app-construction smoke test, the CORS-preflight and request-size-limit checks → `hex-test-app-invariants`.

**This is the app shell; per-resource work lands inside it.** Produced once per project. `hex-restapi-endpoint` and `hex-restapi-schema` add their routers and schema modules into the `main.py` / `schemas/` this skill creates, and the advertised codes in `hex-restapi-endpoint` extend routes the shell hosts — so the shell must already exist when they run. That is a structural precondition (the artifacts depend on the shell), not a fixed run-schedule this skill dictates. **The shell presumes no declared middleware** — no CORS, no request-size cap, no request id. The notes under `main.py` say where they are wired in, and the middleware section below is the form each one takes.

## Template(s) — FastAPI, dishka-wired, structlog logging

**The shell presumes no authentication.** The templates below are the complete file set for a service with no auth at all — a service whose routes need no caller identity: a public API, an internal worker-facing one, or one behind a gateway that passes nothing inward. The translator is a bare `MyappError` dispatcher with no auth import and no auth branch, and there is no `restapi/dependencies.py`: FastAPI's home for shared route dependencies has no occupant until something needs one. An app that declares auth adds what `hex-restapi-auth` states.

```
src/myapp/restapi/
├── __init__.py
├── main.py
├── error_handler.py
└── schemas/
    ├── __init__.py
    └── errors.py
```

### `restapi/main.py`

```python
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from dishka import AsyncContainer
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from myapp.containers import create_container, resolve_settings
from myapp.logging import configure_logging

from .error_handler import UnexpectedErrorMiddleware, register_error_handlers

__all__ = ["create_app"]


@asynccontextmanager
async def _lifespan(app: FastAPI) -> AsyncGenerator[None]:
    container: AsyncContainer = app.state.dishka_container
    await resolve_settings(container)
    yield
    await container.close()


def create_app(container: AsyncContainer | None = None) -> FastAPI:
    configure_logging()
    app = FastAPI(title="myapp", lifespan=_lifespan)

    app.add_middleware(UnexpectedErrorMiddleware)
    register_error_handlers(app)

    setup_dishka(container=container or create_container(), app=app)
    return app
```

Notes:

- **`configure_logging()` runs first**, before the composition root is built — the process's one logging setup (`python-logging` rule 3), which `hex-project-setup` lays. The server is pointed at the factory (`uvicorn --factory myapp.restapi.main:create_app`), never at a module-level `app`, which would build the composition root at import; so the setup runs after the server has configured its own loggers and takes them over, and their records reach the one stream in its format. A process that builds the app itself passes the server `log_config=None`. Each test builds the app again, which rule 3 makes safe.
- **`lifespan` makes two calls into the composition root and nothing else.** On startup, `resolve_settings` — `hex-wiring` rule 2's check that every settings class is built before the process serves, placed by rule 4 below — so a missing variable stops the process, uvicorn reporting the startup failure and exiting, instead of answering `500` on the first request that needs it; the construct smoke builds the app and never reaches it (`hex-test-app-invariants`). On shutdown, closing the composition root: each long-lived handle declares its own release beside its construction (`hex-wiring`) and runs in reverse order of construction, so this file never names a datastore or a settings class and never grows a per-app variant; an app that opens nothing disposable still closes cleanly.
- **The catch-all, `UnexpectedErrorMiddleware`, is added first**, which makes it the innermost layer: every declared middleware wraps it, so the failure it logs carries the logging context bound outside it, and its `500` leaves through every layer, CORS included, like any other response.
- **Where browsers call the API cross-origin, add `CORSMiddleware` last of the declared middleware, with every value from settings** — the outermost of them, so every response, a middleware's rejection included, carries its headers; never a literal origin, and never a `"*"` default, which is the deployment's decision made where it can no longer make it. A header a page's script must read, such as a download's `Content-Disposition`, is listed in its `expose_headers` setting.
- **No other middleware is presumed** — not even a request-size cap. A declared one is added after the catch-all and before CORS, all of them before the error handlers are registered (`## Middleware`). Starlette wraps the last-added outermost, and `setup_dishka` then adds dishka's scope middleware outside every declared one (rule 10).
- **`setup_dishka` is called last**, after the routers are included: it attaches the composition root to the app (as `app.state.dishka_container`) and installs the middleware that opens and closes a per-request scope. Every construction path must reach it before the app is served.
- **The `container` parameter is the test seam.** `hex-test-integration-setup`'s `real_app` add-on passes its `container` fixture — a composition root built with test bindings; production passes nothing and gets `create_container()`.
- **Routers are included between the error handlers and `setup_dishka`.** The template includes none; each `hex-restapi-endpoint` invocation adds its router's import at the top of the file and its own `app.include_router(...)` line there.

### `restapi/error_handler.py`

```python
import structlog
from fastapi import FastAPI, Request
from fastapi.exception_handlers import http_exception_handler
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, Response
from starlette.exceptions import HTTPException
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from myapp.domain.exceptions import MyappError, NotFoundError, ValidationError

from .schemas.errors import ErrorResponse, status_for

__all__ = ["UnexpectedErrorMiddleware", "register_error_handlers"]

log = structlog.get_logger()


class UnexpectedErrorMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self._app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self._app(scope, receive, send)
            return
        started = False

        async def send_tracking_start(message: Message) -> None:
            nonlocal started
            if message["type"] == "http.response.start":
                started = True
            await send(message)

        try:
            await self._app(scope, receive, send_tracking_start)
        except Exception as exc:
            if started:
                raise
            log.error(
                "request_crashed",
                error=exc.__class__.__name__,
                path=scope["path"],
                method=scope["method"],
                exc_info=exc,
            )
            body = ErrorResponse(code="INTERNAL_ERROR", message="Internal server error")
            response = JSONResponse(status_code=500, content=body.model_dump(mode="json"))
            await response(scope, receive, send)


def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(MyappError)
    async def _handle_domain_error(request: Request, exc: MyappError) -> JSONResponse:
        status = status_for(exc)
        body = ErrorResponse(code=exc.code, message=str(exc), context=exc.context).model_dump(mode="json")
        level = log.warning if status < 500 else log.error
        level(
            "request_failed",
            code=exc.code,
            status=status,
            path=request.url.path,
            method=request.method,
            context=body["context"],
        )
        return JSONResponse(status_code=status, content=body)

    @app.exception_handler(RequestValidationError)
    async def _handle_invalid_request(request: Request, exc: RequestValidationError) -> JSONResponse:
        fields = [".".join(str(part) for part in error["loc"]) for error in exc.errors()]
        translated = ValidationError("request validation failed", {"fields": fields})
        return await _handle_domain_error(request, translated)

    @app.exception_handler(HTTPException)
    async def _handle_unrouted(request: Request, exc: HTTPException) -> Response:
        if exc.status_code != 404:
            return await http_exception_handler(request, exc)
        return await _handle_domain_error(request, NotFoundError("no route serves this path"))
```

The translator stays minimal forever. New domain exceptions plug in without touching this file — the
handler renders the body off the attributes `exception-catalog` defines and takes the status from
`status_for`.

**The framework's own input rejection is translated, not left in the framework's shape.** FastAPI
rejects a malformed path parameter, query parameter or body before any route runs, and by default
answers with its own `{"detail": [...]}` body — a second error shape beside the `ErrorResponse` every
route advertises for the input-validation status (`hex-restapi-endpoint`). The request-validation
handler turns that rejection into the catalogue's `ValidationError` and hands it to the domain handler,
so it is rendered in the one place everything else is (`exception-catalog` rule 13) and logged there
once (`python-logging`), with the catalogue's code and the status it maps to. `context` names the rejected fields by
location (`body.name`, `path.id`) and never echoes the input values, which may carry a secret. It is a
translation of the framework's exception into the catalogue, not a branch in the translator, so rule 3's
cap is untouched.
This is why the shell needs `ValidationError` in the catalogue alongside `MyappError`.

**An unknown path is translated too.** The router answers a path no route serves with Starlette's
`HTTPException`, which the domain handler never receives, so it would leave in the framework's
`{"detail": ...}` shape and be logged nowhere. `_handle_unrouted` turns that `404` into the catalogue's
`NotFoundError` and hands it to the domain handler; a method the path does not serve (`405`) stays in the
framework's shape and is never advertised.

**An unexpected failure is caught in the ASGI layer, by `UnexpectedErrorMiddleware`**, because FastAPI's
handler for bare `Exception` re-raises to the server, which logs it a second time. The catch-all logs it
once and answers `INTERNAL_ERROR` itself; once the response has started no body can follow, so it
re-raises unlogged, and the server, which then drops the connection, logs it once.

**This module is the entrypoint's one error log** (`hex-architecture`, *Who logs, by layer*); it binds
`python-logging`'s level guide as 4xx → `warning`, 5xx and non-catalogue → `error`.

`INTERNAL_ERROR` is minted by no catalogue class, and deliberately so: by definition none was raised. It
is a constant of this template, not a new catalogue entry.

**The catalogue classes the shell and the routes need.** The root is the project's own (`MyappError`,
`exception-catalog`) and carries no status. `ValidationError` and `NotFoundError` serve the handlers
above, and `NotFoundError` `hex-restapi-endpoint`'s routes too; each class is added under `exception-catalog` only
when something raises it, and its status joins `STATUS_BY_ERROR` below in the same change —
`hex-restapi-auth` adds 401 and 403, a translated constraint 409.

### `restapi/schemas/errors.py`

```python
from typing import Any

from pydantic import BaseModel, Field

from myapp.domain.exceptions import MyappError, NotFoundError, ValidationError

__all__ = ["ErrorResponse", "MIDDLEWARE_ERRORS", "STATUS_BY_ERROR", "error_responses", "status_for"]


class ErrorResponse(BaseModel):
    code: str
    message: str
    context: dict[str, object] = Field(default_factory=dict)


STATUS_BY_ERROR: dict[type[MyappError], int] = {NotFoundError: 404, ValidationError: 422}

MIDDLEWARE_ERRORS: dict[str, int] = {"INTERNAL_ERROR": 500}


def status_for(exc: MyappError) -> int:
    return next(
        (STATUS_BY_ERROR[error_class] for error_class in type(exc).__mro__ if error_class in STATUS_BY_ERROR),
        500,
    )


def error_responses(*codes: int) -> dict[int | str, dict[str, Any]]:
    known = set(STATUS_BY_ERROR.values()) | set(MIDDLEWARE_ERRORS.values())
    unknown = [code for code in codes if code not in known]
    if unknown:
        raise ValueError(f"HTTP statuses no mapped error class or middleware produces: {unknown}")
    # Exactly FastAPI's `responses=` type; a narrower value type fails strict mypy at the decorator.
    out: dict[int | str, dict[str, Any]] = {code: {"model": ErrorResponse} for code in codes}
    return out
```

`STATUS_BY_ERROR` is the one place a catalogue class meets an HTTP status. `status_for` is `exception-catalog` rule 13's ancestry lookup, so a refinement (`FooNotFoundError`) needs no entry, and a class nothing maps answers `500`, as the root. The statuses a route may advertise are that map's values and `MIDDLEWARE_ERRORS`', `500` aside, which every route can produce.

A response entry carries no description: the framework fills in the status's standard phrase.

`MIDDLEWARE_ERRORS` registers the codes emitted with no catalogue class behind them. `INTERNAL_ERROR` is always present: the catch-all answers with it when no catalogue class was raised at all, and its entry pins the code string clients key on; `500` itself is never advertised (`hex-restapi-endpoint`). An entry is added when a declared middleware introduces a code (*Registering a middleware's status*, below) — a size cap's `PAYLOAD_TOO_LARGE` → 413.

This file is the **single source of truth** for the error wire-shape, the status map, the `error_responses(...)` helper and `MIDDLEWARE_ERRORS`. `hex-restapi-endpoint` only *references* it — it never writes to it or restates this template.

### `restapi/schemas/__init__.py`

```python
from . import errors
from .errors import *

__all__ = errors.__all__
```

Per-resource schema modules (e.g. `foos.py`) are added later by `hex-restapi-schema`. Each holds one resource's request and response models together — a closed set of declarations named for what it describes, which `python-packaging` lets share a module — and package updates follow `python-packaging`.

### `restapi/__init__.py`

```python
```

Empty file — see the entrypoint carve-out in `hex-architecture`.

## Middleware

ASGI middleware follows `naming` and `python-packaging` under `restapi/middleware/`, handling a
cross-cutting request/response concern that belongs to no single route — a correlation id, a body-size
cap, rate limiting, timing. That list is open, not a fixed catalog.

A middleware that rejects returns its error before awaiting the wrapped app; a pass-through one — a
request id bound into the logging context, a timer — always awaits it, and clears any per-request
context it set in a `finally`. A request-size cap, where the app declares one, is
`MaxRequestSizeMiddleware(app, max_bytes)` — the class name and keyword `hex-test-app-invariants` finds
it by — rejecting on the declared `Content-Length` with `PAYLOAD_TOO_LARGE`; a chunked body or a client
that misstates its length passes it, so the absolute ceiling belongs to the edge (*Other bindings*).

### How this binding spells the middleware obligations — raw ASGI, Starlette

Each line below is one obligation from `## Rules` in this stack's spelling; none of them is an
obligation of its own.

- **A raw ASGI class, the catch-all's form** (rule 7). `__init__(self, app: ASGIApp, <config…>)` stores `app` plus the config on
  `self`; `async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None`. Configuration
  arrives as constructor keyword arguments passed at `app.add_middleware(Cls, **config)`, and the
  constructor validates them there.
- **Pass non-`http` scopes straight through** (rule 8) —
  `if scope["type"] != "http": await self._app(scope, receive, send); return`. Lifespan and websocket
  scopes must not be intercepted.
- **Reject before the wrapped app** (rule 9) — `return` **before** `await self._app(...)`, with the body
  built from `ErrorResponse`.
- **Starlette wraps the last-added outermost** (rule 10). Each `app.add_middleware(...)` call wraps the
  app as a new **outermost** layer, so of the middleware `create_app` declares, the **last** one added is
  the first to see a request and the last to touch a response — and `setup_dishka`, called after all of
  them, adds dishka's scope middleware outside every one.

### Registering a middleware's status

A status a middleware emits with no `MyappError` behind it — otherwise it is a class under
`exception-catalog` and an entry in `STATUS_BY_ERROR` — is added to `MIDDLEWARE_ERRORS` under its code
string before any route advertises it (`hex-restapi-endpoint`), and the middleware's `ErrorResponse`
carries that same code (rule 9).

## Other bindings

### Middleware

- **A framework with its own middleware abstraction** — Litestar, Django, or a decorator-based hook.
  Unchanged: transport-only scope, configuration fixed and validated at wiring time, the shared error
  body with a registered code, and a deliberate order. What changes: the class shape and how
  non-matching traffic is passed through.
- **A reverse proxy or gateway in front of the app.** A concern that is purely about bytes on the wire —
  a size ceiling, a request id — may live there instead of in the app, and then no middleware is written
  at all. Unchanged: the status it returns still needs a registered code if a client can see it
  (*Registering a middleware's status*, above), and the app keeps its own defence in depth where the edge can be
  bypassed.

### Dependency injection

- **`dependency-injector`.** The shell, the middleware order, the error handlers and the schemas are unchanged. What changes is the two ends of the composition root: `create_app` attaches it to `app.state` itself rather than calling an integration's setup function, and `_lifespan` must dispose each long-lived handle **by name** (`await container.engine().dispose()`) — which means this file grows a per-app teardown variant and has to be kept in step with what `containers.py` actually opened. That coupling is the reason the primary binding closes the composition root instead.

## Rules

1. **One-shot.** This skill runs once per project. After bootstrap, this file set is stable; updates to `main.py` go through whichever skill needs them (typically `hex-restapi-endpoint` appending an `include_router(...)` line).
2. **A route may advertise only a status `STATUS_BY_ERROR` or `MIDDLEWARE_ERRORS` holds, and never `500`**; the map is this boundary's, under `exception-catalog` rules 6 and 13.
3. **The translator stays minimal.** `restapi/error_handler.py` has **at most one** `isinstance` branch — the primary template this skill publishes has none, and an app that declares auth adds exactly one, for the RFC-7235 challenge (`hex-restapi-auth`). All other behaviour comes from the `MyappError` subclass and its mapped status, so new behaviour is a new subclass — and, where its status differs from its parent's, one map entry — never a new branch. The framework's own rejection of malformed input is translated into the catalogue's validation class, and its answer to an unknown path into the not-found class, each rendered by the same handler — a translation, not a second branch — so a route's advertised input-validation response is the body the client actually receives.
4. **`lifespan` runs the settings check `hex-wiring` rule 2 requires on startup and closes the composition root once on shutdown, and nothing else.** The check sits in the startup hook, not in building the app, because the server completes startup before it accepts a connection while building the app reads no environment. *What* the close releases is decided where each resource is constructed (`hex-wiring`), so `main.py` never names a datastore or a settings class. No business logic.
5. **`main.py` resolves nothing itself and never exposes the composition root for others to resolve from**; the startup check it calls is the composition root's own. How a route receives its handler is `hex-restapi-endpoint`'s.

6. **A middleware is transport-level and nothing else.** Bytes, headers, timing, the logging context.
   Anything that needs a domain entity, a repository or an application handler is not a middleware.
   Naming and module layout follow `naming` and `python-packaging`, under `restapi/middleware/` — all
   but the catch-all, which completes the error handlers in `error_handler.py`.
7. **A middleware's configuration is fixed and validated at wiring time.** It holds the wrapped
   application plus its configuration and nothing else, built once; every per-request value — the
   request id, the declared content length — is a local, never stored on the instance. A bad
   configuration value fails when the app is assembled, not mid-request.
8. **A middleware acts only on the kind of traffic it is for, and passes every other kind through
   untouched.** An HTTP concern must not intercept the framework's startup, shutdown or non-HTTP
   connections; a middleware that swallows one of those breaks a part of the app it was never about.
9. **A middleware that rejects a request emits the app's own error body, with a registered code.** Same
   `{"code", "message", "context"}` shape the central translator emits, built through the shared schema
   rather than hand-rolled, carrying the status it owns and a **stable** machine-readable code — the
   API contract and `MIDDLEWARE_ERRORS` in `schemas/errors.py` key on that string
   (`hex-restapi-endpoint`). A middleware that does not reject always reaches the wrapped app.
10. **The order middlewares see a request in is chosen, not inherited.** Which one sees the raw request
    first is a decision the app makes — a size cap has to see it before anything has read the body —
    and it is written according to whatever wrapping rule the framework applies to the order they are
    registered in. The relative order is the consuming app's decision; that it was decided is not.

## Inlined typing / import rules

- Middleware: ASGI types from `starlette.types` (`ASGIApp`, `Scope`, `Receive`, `Send`; add `Message` only
  when `__call__` wraps `receive` / `send`).
- A middleware that rejects emits its body through the shared
  `ErrorResponse` schema (`from ..schemas.errors import ErrorResponse`) — never hand-roll the
  `{"code", "message", "context"}` dict, so the wire shape stays single-sourced.
- Typing follows `python-style`, logging `python-logging`.

## Package wiring

For `restapi/__init__.py` and `restapi/middleware/__init__.py`, follow `python-packaging`, with the entrypoint carve-out in `hex-architecture`.

## Hard stops

- `domain/exceptions.py` does not exist yet → stop, use `exception-catalog` bootstrap first.
- `myapp/containers.py` does not exist yet → stop, use `hex-wiring` first.
- `lifespan` is asked to dispose a named engine or client → stop, declare that release beside the resource's construction in `hex-wiring`.
- A concern is for one route rather than all → stop, use `hex-restapi-endpoint` plus a handler.
- A middleware needs a domain entity, a repository or an application handler → stop, use `hex-application` for application logic.
- A middleware authenticates or authorizes → stop, use `hex-restapi-auth`; caller authentication is a route dependency, not a middleware.
