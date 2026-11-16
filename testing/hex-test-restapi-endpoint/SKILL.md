---
name: hex-test-restapi-endpoint
description: Use when testing one REST endpoint through the real ASGI app — one file per endpoint under `tests/integration/api/<resource>/`, asserting the success body and each advertised error code, with per-resource fixtures in a sibling `conftest.py`. Not properties discovered across all routes at once (`hex-test-app-invariants`), not the auth half — a token verifier's unit test, 401/403, role rejection, cross-tenant 404 (`hex-test-restapi-auth`) — and not the fixtures themselves (`hex-test-integration-setup`).
---

# Hex Test — REST API Endpoint

Consult `test-principles` for the testing constitution. Where this skill contradicts `test-principles`, the constitution wins.

Produces one integration-test file per endpoint. Self-contained: every test in the file constructs its own state by calling factory fixtures or POSTing through the API; no cross-test state, no shared registries, no cross-file edits when a new endpoint is added.

## When to use vs. neighbours

- A new or modified endpoint added by `hex-restapi-endpoint` → this skill.
- A new resource introduces several endpoints (create + list + get + update + delete) → invoke this skill once per endpoint file; sibling files share a per-resource `conftest.py`.
- The `tests/integration/conftest.py` itself (rollback, container fixtures, `container`, `real_app`) → `hex-test-integration-setup` (one-shot).
- The auth half — the `authenticated_client` factory and its signing-key fixtures, a route driven as an authenticated caller, a role rejection or a cross-tenant 404, the token verifier's own unit test → `hex-test-restapi-auth` (auth apps only; this skill is complete without it).
- The route-side auth dependency, the role gate and the 401/403 codes a route advertises because of them → `hex-restapi-auth`.
- Cross-cutting "every advertised error code carries the catalogue's shape" / CORS / request-size → `hex-test-app-invariants` (one-shot; discovers by walking the app's published document).
- Repository contract (real DB, no HTTP) → `hex-test-repository-contract`.
- Pure domain unit test → `hex-test-domain`.
- The testing constitution these rules defer to — speed targets, fixture placement, the mocking prohibition → `test-principles`.
- A structural invariant enforced by a grep firewall at compile time rather than over HTTP → `test-architecture-rule`.

## Template(s) — pytest, httpx2 over an in-process ASGI transport, FastAPI

```
tests/integration/api/<resource>/
├── conftest.py                                  # per-resource fixtures (sibling-shared)
└── test_<verb>_<noun>.py                        # one file per endpoint
```

**The templates below are the primary, auth-free form** — a public route, or any route in an app that
declares no auth. An authenticated route is the same file driven through an authenticated client
instead of the plain one, and `hex-test-restapi-auth` carries those variants along with the role and
tenancy assertions that only exist when there is a caller to have a role.

### `test_<verb>_<noun>.py` — the endpoint test

```python
from fastapi import FastAPI
from httpx2 import ASGITransport, AsyncClient

from myapp.domain.exceptions import ValidationError


async def test_create_foo_returns_the_created_foo(real_app: FastAPI) -> None:
    transport = ASGITransport(app=real_app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.post("/foos", json={"name": "alpha"})

    assert response.status_code == 201
    assert response.json()["name"] == "alpha"


async def test_create_foo_empty_body_returns_422(real_app: FastAPI) -> None:
    transport = ASGITransport(app=real_app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.post("/foos", json={})

    assert response.status_code == 422
    assert response.json()["code"] == ValidationError.code
```

The plain `AsyncClient` over `real_app` is the sanctioned client for a route with no auth dependency
(`hex-test-restapi-auth` rule 4). Every error path for the same endpoint lives in this file too, each
asserted by `code` (Rule 8) — here the `422` an empty create body produces. A `404` on an `{id}` route,
and a `409` where the aggregate carries a uniqueness constraint, are further tests of the same shape.
Where the route transfers a file, the test also asserts the media type and disposition the route sets,
never a fixed download shape.

### Per-resource `conftest.py` — relational seed factory, SQLAlchemy

A raw `INSERT` is legitimate setup here: `hex-test-repository-contract` rule 9 bans it only in a test of the repository under test, where seeding behind the subject would prove nothing. An endpoint test's subject is the route, so the fastest honest way to put a row in front of it is to write one. The `make_foo` factory below seeds via a raw SQL `INSERT` through `session_factory` — that is the **relational-store** variant, valid when the resource is backed by a relational store. A resource backed by a client-style store (redis / a document store / …) has no `session_factory` and no SQL table: seed it either by **POSTing through the API** (drive the create endpoint, then test against the result) or via the **store's own client** in the fixture. Pick the path from the resource's datastore kind; don't reach for `INSERT INTO` when there is no SQL table.

```python
import uuid
from collections.abc import Awaitable, Callable

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


@pytest.fixture
def make_foo(session_factory: async_sessionmaker[AsyncSession]) -> Callable[..., Awaitable[uuid.UUID]]:
    async def _make(*, name: str | None = None) -> uuid.UUID:
        foo_id = uuid.uuid4()
        async with session_factory() as session:
            await session.execute(
                text("INSERT INTO foos(id, name) VALUES(:id, :name)"),
                {"id": str(foo_id), "name": name or f"foo-{foo_id}"},
            )
            await session.commit()
        return foo_id

    return _make
```

## Other bindings

- **Another way to drive the app.** An in-process ASGI transport is one; a framework's own test client,
  or a live server on a loopback port, are the others. What changes is how the client is constructed and
  whether the app's start-up events run — an out-of-process server runs them, an in-process transport may
  not, so a test that depends on start-up wiring has to arrange it. One file per endpoint, the by-value
  body assertion, the error-code assertion and per-test factory fixtures are unchanged.

## Rules

1. **One file per endpoint, named for its operation** (`test_create_foo.py`) — the subject is one route, not the router module. It holds the happy path and one test for each error code the route advertises (`hex-restapi-endpoint`); in an auth app the `401` and `403` are `hex-test-restapi-auth`'s. No mega-files spanning a whole resource.
2. **Assert the success body by value** — the fields the request set and those the operation promises to derive or leave alone. A framework that enforces the declared response model on the way out already turns a drifted body into a `500`; validate the whole body only where a route bypasses that model (a raw response).
3. **No cross-cutting registries but one.** Adding a new endpoint touches exactly one new test file. The one sanctioned table is the auth probe's public set: in an auth app, a route meant to be public is also named there (`hex-test-restapi-auth`). The discovered global checks — "every advertised error code carries the catalogue's shape", and in an auth app "every operation not declared public refuses an anonymous or untrusted caller" — are owned by `hex-test-app-invariants` and `hex-test-restapi-auth`, and derive their inputs from the app's published document and its resolved routes; there is no hand-maintained endpoint table to extend.
4. **Each test builds its own state** — `make_foo`, or a POST through the API; fixed natural keys and exact counts follow `test-principles`, *Assert strength*.
5. **An order assertion is reliable only where the seeded rows differ in the sort key**: a store that stamps rows inside one transaction can give them all one instant (`test-principles`, reliability 4), so sort by a key the test sets, or assert the set of ids. A mutation whose response carries no state (a `204` delete) is followed by a read through the API that proves the effect — the row's `404`, and a second row still served.
6. **The client is entered as a context manager, never assigned.** Bare-assigning it leaks the transport, and the leak surfaces as an unrelated test failing later in the session.
7. **Per-resource fixtures live in the sibling `conftest.py`.** Factory fixtures (`make_foo`) return one fresh row per call — a default for a unique column differs per call.
8. **Error responses are asserted by `code`, not by message.** `assert response.json()["code"] == ValidationError.code` — message text drifts, the `code` constant is the contract. The actual HTTP status is asserted separately.
9. **Mocking.** Follow `test-principles` for the mocking prohibition. If a test needs to mock, it isn't an integration test; move it to a domain unit test (`hex-test-domain`) or to a handler test over fakes (`hex-test-application-handler`), which is also where a compensating handler's undo is pinned.

## Inlined typing / import rules

- `pytest`, `httpx2`, `fastapi`, `myapp.domain.exceptions`. No `myapp.application.*` or `myapp.infrastructure.*` imports — the test drives over HTTP, not by reaching in.
- Full annotations on every signature, tests included — `-> None` on every test, every fixture parameter typed. `python-style` owns annotation policy and admits no test carve-out.
- No `from __future__ import annotations`.

## Hard stops

- Nothing up-tree builds the app on the test's own infrastructure bindings (`real_app` under this catalogue's binding) → stop, use `hex-test-integration-setup`; the missing thing is the guarantee, not the fixture name.
- Asked to register the new endpoint in a hand-maintained route or expectation table so a global check sees it → stop, use `hex-test-app-invariants`; the global checks derive their inputs from the running app, so a new route joins them with nothing to update. The auth probe's public set is the one exception (rule 3).
- A test asserts a role rejection or a cross-tenant 404 here → stop, use `hex-test-restapi-auth`; those assertions need a caller identity this skill does not mint.
- A test asserts on a response field that is not in the Pydantic response schema → stop, use `hex-restapi-schema` to extend the schema first.
- A test uses a plain `AsyncClient` for a request to a route that attaches an auth dependency → stop, use `hex-test-restapi-auth`'s authenticated client; a plain client on a gated route tests the rejection, not the endpoint.
