---
name: hex-test-app-invariants
description: Use when testing a property of the assembled HTTP app itself rather than one route's own behaviour — a check that needs no edit when an endpoint is added or removed — or the construct smoke any entrypoint gets. Covers the catalogue's error shape on every error code the published OpenAPI document advertises, the CORS preflight and the request-size limit where the app configures them, and the app-construction smoke, each built with `create_app()` and taking its inputs from the app rather than from a maintained list; a service with no HTTP entrypoint keeps only the smoke, for its own entrypoint. A single endpoint's test is `hex-test-restapi-endpoint`; the anonymous-caller probe and every token fixture are `hex-test-restapi-auth`'s.
---

# Hex Test — App Invariants

Consult `test-principles` for the testing constitution. Where this skill contradicts `test-principles`, the constitution wins.

One-shot per project. An HTTP app gets up to four files under `tests/unit/restapi/`, each of which builds the app with `create_app()` and asserts a single global property; a service with no HTTP entrypoint gets only the construct smoke, for its own entrypoint (rule 10). None of them needs to be edited when an endpoint is added or removed. None needs a store, so none waits on the integration suite's containers. An app that declares auth gains one more discovered invariant — every protected route rejects an anonymous caller — which is `hex-test-restapi-auth`'s.

## When to use vs. neighbours

- Laying the cross-cutting tests for the first time → this skill.
- A per-endpoint integration test → `hex-test-restapi-endpoint`.
- The integration fixtures, `real_app` among them → `hex-test-integration-setup`; nothing here takes them.
- The every-protected-route-rejects-an-anonymous-caller probe, and the fixtures that mint tokens → `hex-test-restapi-auth` (auth apps only; nothing here consumes them — see Rule 8).
- The route-side `error_responses(...)` declaration that puts the catalogue's shape on each advertised code → `hex-restapi-endpoint`, in its sibling `CONTRACTS.md`; the 401/403 half of it → `hex-restapi-auth`.
- A grep-firewall static rule → `test-architecture-rule` (compile-time, not runtime).
- The testing constitution — markers, async mode, the mocking prohibition → `test-principles`.

## Template(s) — pytest, FastAPI, httpx2 over an in-process ASGI transport

```
tests/unit/restapi/
├── test_app_constructs.py                   # always
├── test_openapi_advertises_error_codes.py   # always
├── test_cors.py                             # only if CORS is configured
└── test_request_size_limit.py               # only if a size-cap middleware is declared
```

### `test_app_constructs.py`

```python
from myapp.restapi.main import create_app


def test_app_constructs_and_renders_openapi() -> None:
    app = create_app()
    assert app.openapi()["paths"]
```

### `test_openapi_advertises_error_codes.py`

```python
from typing import Any

import pytest

from myapp.restapi.main import create_app

_ERROR_SCHEMA_REF = "#/components/schemas/ErrorResponse"
_HTTP_METHODS = frozenset({"get", "put", "post", "delete", "patch", "options", "head", "trace"})


def _operations() -> list[tuple[str, str]]:
    paths: dict[str, dict[str, Any]] = create_app().openapi()["paths"]
    return [(method, path) for path, item in paths.items() for method in item if method in _HTTP_METHODS]


def pytest_generate_tests(metafunc: pytest.Metafunc) -> None:
    # a fixture cannot feed parametrization
    if "method" in metafunc.fixturenames and "path" in metafunc.fixturenames:
        cases = _operations()
        metafunc.parametrize("method,path", cases, ids=[f"{method.upper()} {path}" for method, path in cases])


def test_the_walk_found_operations_to_check() -> None:
    # an empty parameter set is reported as skipped
    assert _operations(), "no API operation was published, so nothing was checked"


def test_every_advertised_error_code_carries_the_error_schema(method: str, path: str) -> None:
    responses: dict[str, dict[str, Any]] = create_app().openapi()["paths"][path][method]["responses"]

    off_shape = {
        code
        for code, response in responses.items()
        if code.isdigit()
        and int(code) >= 400
        and response.get("content", {}).get("application/json", {}).get("schema") != {"$ref": _ERROR_SCHEMA_REF}
    }

    assert off_shape == set(), "published without the catalogue's error shape"
```

### `test_cors.py`

```python
from typing import Any, cast

from fastapi import FastAPI
from httpx2 import ASGITransport, AsyncClient

from myapp.restapi.main import create_app


def _configured_origin(app: FastAPI) -> str | None:
    # Starlette's `Middleware.kwargs` is untyped; cast rather than silence mypy.
    for middleware in app.user_middleware:
        if getattr(middleware.cls, "__name__", "") == "CORSMiddleware":
            origins = cast(dict[str, Any], middleware.kwargs).get("allow_origins", [])
            return origins[0] if origins else None
    return None


async def test_cors_preflight_echoes_a_configured_origin() -> None:
    app = create_app()
    origin = _configured_origin(app)
    assert origin is not None, "CORS is configured but the app under test allows no origin"

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver") as client:
        response = await client.options(
            "/",
            headers={"Origin": origin, "Access-Control-Request-Method": "GET"},
        )

    assert response.headers.get("access-control-allow-origin") == origin
```

### `test_request_size_limit.py`

```python
from typing import Any, cast

from fastapi import FastAPI
from httpx2 import ASGITransport, AsyncClient

from myapp.restapi.main import create_app

_BODY_METHODS = ("post", "put", "patch")


def _max_request_bytes(app: FastAPI) -> int | None:
    for middleware in app.user_middleware:
        if getattr(middleware.cls, "__name__", "") == "MaxRequestSizeMiddleware":
            max_bytes = cast(dict[str, Any], middleware.kwargs).get("max_bytes")
            return max_bytes if isinstance(max_bytes, int) else None
    return None


def _body_operation(app: FastAPI) -> tuple[str, str] | None:
    paths: dict[str, dict[str, Any]] = app.openapi()["paths"]
    for path, item in paths.items():
        methods = [method for method in _BODY_METHODS if "requestBody" in item.get(method, {})]
        if methods and "{" not in path:
            return methods[0].upper(), path
    return None


async def test_oversize_payload_returns_413() -> None:
    app = create_app()
    limit = _max_request_bytes(app)
    assert limit is not None, "the size-cap middleware is missing from the app under test"
    operation = _body_operation(app)
    assert operation is not None, "a size cap is declared but no operation accepts a body"
    method, path = operation

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver") as client:
        response = await client.request(
            method,
            path,
            content=b"x" * (limit + 1),
            headers={"Content-Type": "application/octet-stream"},
        )

    assert response.status_code == 413
```

A health or info endpoint is tested like any endpoint (`hex-test-restapi-endpoint`).

## Other bindings

- **Another web framework.** Every rule here survives the swap; reading the CORS origin and the size
  cap off the running app rather than freezing them stays the rule, and only the attribute they are read
  from is the framework's.
- **A framework that generates no API document.** The error-shape check then has nothing to walk and
  that file is not written. The construct smoke still is, and the CORS preflight and the size-limit
  probe where the app configures them.

## Rules

Consult `test-principles` for the testing constitution.

1. **Every test discovers its inputs from the app itself** — never from a hand-maintained route or expectation table, and never from a value frozen into the test. The operations come off the app's published document; the CORS origin is read off the app's CORS configuration, never the source app's dev origin, and `allow_credentials` is not assumed; the size cap, and the operation the probe posts to, are read off the app's own middleware and document, the probe sending one byte past the cap. A probe file exists only where its feature is configured (rule 9), so the feature being absent from the app is a failure, as an empty walk is (rule 3). The cost of adding a new endpoint must be zero in this directory.
2. **Walk the operations the app publishes, under the path its document is keyed on**, never a key assembled by hand out of a router prefix and a decorator argument — under FastAPI, the paths of `create_app().openapi()`.
3. **One reported case per discovered operation, and a walk that discovers nothing is a failure, not a pass** → `test-principles`, *When to parametrize*. An app whose routers are never wired lands there, and the non-empty assertion is the only thing between that and a green run.
4. **Every published error response carries the app's own error schema.** An advertised code whose body is the framework's own — FastAPI's validation model on a `422` the route never declared, where the app's validation handler answers with the catalogue's shape (`hex-restapi-app`) — fails.
5. **Each file holds one invariant.** Don't merge `test_cors.py` and `test_request_size_limit.py` even though both are tiny — failures in one don't mask the other, and the file names list the invariants.
6. **CORS test uses an OPTIONS preflight.** Asserting on a GET response's `Access-Control-Allow-Origin` is a softer test; the preflight is the one browsers actually consult.
7. **Request-size test uses raw bytes**, not JSON-encoded data, to bypass schema validation and hit the middleware directly. Otherwise the response is `422` (validation) before the middleware sees the body.
8. **No authenticated client here.** Every test in this skill reads the published document or probes an unauthenticated path. A test here that needs a token is either the auth probe (`hex-test-restapi-auth`) or a per-endpoint concern (`hex-test-restapi-endpoint`).
9. **Emit only the files the app's features justify.** In an HTTP app, `test_app_constructs.py` and `test_openapi_advertises_error_codes.py` are always produced; `test_cors.py` only where the app configures CORS; and `test_request_size_limit.py` only with a size-cap middleware — a CORS policy and a size cap are deployment choices (`hex-restapi-app`), not defaults every app has. A file whose module-level imports name something the app does not have fails at collection time and takes down the whole `tests/unit/restapi/` package — which is also why the auth probe is `hex-test-restapi-auth`'s and is emitted only by an app that declares auth.
10. **`test_app_constructs.py` is the always-emitted construct smoke of every HTTP app.** It builds the app with `create_app()` and forces the whole document with `app.openapi()` — sync, no fixtures, no `await`: `create_app` builds the composition root but resolves nothing — the settings check runs at the server's startup, which building the app never reaches (`hex-restapi-app`) — so it reads no environment and opens nothing, and a test needing a fixture would no longer run with no Docker daemon, the environment where the other gates pass and a construct-time dependency gap (`python-multipart`, …) slips through. It is structural (green on freshly laid routes), so every app gets it, auth or not. A service with no HTTP entrypoint keeps the obligation in `tests/unit/test_<entrypoint>_constructs.py`: build the composition root and the entrypoint object as its launcher does, and resolve nothing from the graph, the launcher's startup settings check (`hex-wiring` rule 2) included — resolution reads settings and opens clients, which this layer must not — and write none of the other files.

## Inlined typing / import rules

- `pytest`, `fastapi`, `httpx2`, `myapp.restapi.main`.
- Full annotations on every helper.
- No `from __future__ import annotations`.

## Hard stops

- Asked to fold a per-endpoint test into one of these files → stop, these files hold discovered global properties only; a single endpoint's behaviour belongs to `hex-test-restapi-endpoint`.
- Asked for an authentication probe here → stop, use `hex-test-restapi-auth`; it owns that invariant and is emitted only by an app that declares auth.
