---
name: hex-restapi-endpoint
description: Use when adding or changing one REST route, or creating a resource's router file `restapi/routers/<resource>.py` — thin routes over application handlers, a route that carries a file, dishka handler injection, route ordering, and which error codes the route advertises. Owns the per-operation code sets and advertise-only-what-you-produce. The pydantic models are `hex-restapi-schema`; the auth dependency and the `401` / `403` that follow it are `hex-restapi-auth`.
---

# Hex — REST API Endpoint

Produces one HTTP endpoint for one resource. Routers grow incrementally — this skill adds one route at a time. A "router file" exists once per resource; subsequent endpoint additions extend it.

**Read the sibling `CONTRACTS.md` in this skill's own directory before choosing what a route advertises
in `responses=error_responses(...)`.** It carries the per-operation code sets and the helper the
decorator draws on; only `SKILL.md` is loaded automatically.

## When to use vs. neighbours

- One new endpoint or modification of an existing one, including one that carries a file → this skill.
- Pydantic request/response schemas this route maps to and from → `hex-restapi-schema`.
- The `responses=error_responses(...)` declaration and which codes belong in it → this skill, in the sibling `CONTRACTS.md`.
- Defining a new error class, and boundary translation → `exception-catalog`; the status it answers with → `hex-restapi-app`'s `STATUS_BY_ERROR`, needed only where it differs from its parent's.
- Attaching an auth dependency to a route, and the `401` / `403` that follow it → `hex-restapi-auth`.
- The shell this router registers into — `restapi/main.py`, its middleware, and the registry for a status a middleware introduces → `hex-restapi-app`.
- The composition root that binds the handler this route injects → `hex-wiring`.
- Testing this route through the real app → `hex-test-restapi-endpoint`; the OpenAPI and app-construction properties discovered across all routes → `hex-test-app-invariants`.
- Route, module and helper identifiers → `naming`; `__all__` and the router export → `python-packaging`.

## Template(s) — FastAPI router, dishka-injected

### File location

```
src/myapp/restapi/routers/foos.py
```

One router file per resource holds **all** of that resource's endpoint functions; the file declares the `APIRouter`, defines each endpoint function (ordered per Route ordering), and is registered once in `src/myapp/restapi/main.py` via `app.include_router(...)`. The skeleton below is the whole-file shape; an endpoint function is the per-route shape that follows it.

`route_class=DishkaRoute` on the router is what injects every `FromDishka[...]` parameter below it, so it is declared once per file and no route carries an injection decorator.

### Skeleton — router file

```python
from typing import Annotated
from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Query
from fastapi.responses import Response

from myapp.application.foos import (
    CreateFooCommand,
    CreateFooHandler,
    DeleteFooCommand,
    DeleteFooHandler,
    GetFooHandler,
    GetFooQuery,
    ListFoosHandler,
    ListFoosQuery,
    UpdateFooCommand,
    UpdateFooHandler,
)
from myapp.domain.foos import FooListFilter

from ..schemas import (
    FooCreateRequest,
    FooListResponse,
    FooResponse,
    FooUpdateRequest,
    error_responses,
)

__all__ = ["router"]

_MAX_PAGE_SIZE = 100

router = APIRouter(prefix="/foos", tags=["foos"], route_class=DishkaRoute)
```

The skeleton imports what the CRUD routes below use.

**The route templates below are auth-free** — every route in an app that declares no auth, and the
public routes of one that does. An authenticated route is derived by `hex-restapi-auth`'s `ROUTES.md`.

### `list` (paginated read) — pagination shape mirrors `hex-domain-model`

**A page size is always bounded and always defaulted** — an unbounded `limit` lets one request ask for the whole table. The *ceiling* is the app's decision and a named module-level constant in the router file (`_MAX_PAGE_SIZE` in the skeleton), because `Query(...)` bounds are evaluated when the route function is defined and cannot be injected per request; an app picks a ceiling its list query can serve in one round trip. The *default* is the filter's (`hex-domain-model`), read off `FooListFilter.limit` — a class-level default only an unslotted dataclass has — so the number is stated once, and the route passes `limit` to the filter explicitly. `ge=1` on the page size and `ge=0` on the offset are not tunable — a zero-row page and a negative offset are meaningless at any ceiling.

```python
@router.get("", response_model=FooListResponse, responses=error_responses(422))
async def list_foos(
    handler: FromDishka[ListFoosHandler],
    limit: Annotated[int, Query(ge=1, le=_MAX_PAGE_SIZE)] = FooListFilter.limit,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> FooListResponse:
    result = await handler.execute(
        ListFoosQuery(filter=FooListFilter(limit=limit, offset=offset)),
    )
    return FooListResponse(
        items=[FooResponse(id=foo.id, name=foo.name, note=foo.note) for foo in result.items],
        total=result.total,
        limit=limit,
        offset=offset,
    )
```

**Every filter field a caller may set is a query parameter of the same name and type** — a sort is its
domain enum, which answers an unknown value with the input-validation status — and each is passed to the
filter; a filter field no parameter reaches is dead down to the repository. Where they take the signature
past `python-toolchain`'s positional cap, the query parameters and the auth dependency are keyword-only,
after a bare `*`.

A filter that pages by cursor instead (`hex-domain-model`, filter rule 5) takes a `cursor` query parameter in place of `offset`, passes it into the filter, and returns `next_cursor` in place of `total`/`offset`; `FooListResponse` (`hex-restapi-schema`) matches whichever shape the filter uses.

### `get` (single read)

```python
@router.get("/{id}", response_model=FooResponse, responses=error_responses(404, 422))
async def get_foo(
    id: UUID,
    handler: FromDishka[GetFooHandler],
) -> FooResponse:
    foo = await handler.execute(GetFooQuery(id=id))
    return FooResponse(id=foo.id, name=foo.name, note=foo.note)
```

### `create` (with post-write read-back)

```python
@router.post(
    "",
    response_model=FooResponse,
    status_code=201,
    responses=error_responses(409, 422),  # 409 only where Foo has a unique field
)
async def create_foo(
    body: FooCreateRequest,
    handler: FromDishka[CreateFooHandler],
    get_handler: FromDishka[GetFooHandler],
) -> FooResponse:
    new_id = await handler.execute(
        CreateFooCommand(name=body.name, note=body.note),
    )
    foo = await get_handler.execute(GetFooQuery(id=new_id))
    return FooResponse(id=foo.id, name=foo.name, note=foo.note)
```

### `update` (PATCH with read-back)

```python
@router.patch(
    "/{id}",
    response_model=FooResponse,
    responses=error_responses(404, 409, 422),  # 409 only where Foo has a unique field
)
async def update_foo(
    id: UUID,
    body: FooUpdateRequest,
    handler: FromDishka[UpdateFooHandler],
    get_handler: FromDishka[GetFooHandler],
) -> FooResponse:
    await handler.execute(UpdateFooCommand(id=id, name=body.name, note=body.note))
    foo = await get_handler.execute(GetFooQuery(id=id))
    return FooResponse(id=foo.id, name=foo.name, note=foo.note)
```

### `delete` (204)

```python
@router.delete(
    "/{id}",
    status_code=204,
    responses=error_responses(404, 422),
)
async def delete_foo(
    id: UUID,
    handler: FromDishka[DeleteFooHandler],
) -> Response:
    await handler.execute(DeleteFooCommand(id=id))
    return Response(status_code=204)
```

`409` joins the set only where another aggregate can reference a `Foo`, so a delete can find it still in
use.

### Route ordering — FastAPI declaration order

FastAPI resolves a request against the routes **in declaration order**, which makes the reachability
obligation (rule 13) a property of where a route sits in the file. A literal sibling of `/{id}` —
`/search`, or any other collection-level action — declared after `/{id}` is captured by it: the
literal matches `{id}`, fails its UUID validation, and the request answers `422` before any handler
runs; the literal route is never reached.

**Declare every literal collection-level path above the `/{id}` routes**, whatever its method. When
extending an existing router file, place a new literal route **above** the `get` / `update` / `delete`
routes for `/{id}`.

A framework that resolves by specificity instead has no such ordering to get wrong: the obligation is
unchanged, and nothing in the file's layout can violate it.

## Other bindings

- **`dependency-injector`.** Everything above the signature is unchanged — decorators, status codes, route ordering, the no-`try/except` rule, read-back. What changes is that the route takes `request: Request` back and, inside the body, reaches the composition root hanging off the app state and calls the binding whose **attribute name** is the snake_case form of the handler class. That spelling becomes a contract with `hex-wiring` that nothing enforces. The router then needs no `route_class`.
- **A route-scoped injection decorator instead of the router's route class.** Where a route cannot go through the router — a websocket handler, or a `Depends` factory such as the auth dependency in `hex-restapi-auth` — the same `FromDishka[...]` parameter is injected by decorating that function with `@inject`. Use it only there; a decorator on an ordinary HTTP route means the router is missing its `route_class`.

## Rules

### Router file

1. **One module per resource.** File naming follows `naming`.
2. **Only `router` is public**; export mechanics follow `python-packaging`.
3. **`prefix` is the resource word, plural, as the file name has it — one casing for every path, kebab-case unless the API already has another** (`/foo-bars`).
4. **`tags=[...]` echoes the resource word.**

### Parameter order (load-bearing for readability, not FastAPI)

5. **Parameters go in one order** — path parameters (`id: UUID`), then body (`body: FooCreateRequest`), then injected handlers (`handler: FromDishka[CreateFooHandler]`), which carry no default and so must precede every defaulted parameter anyway, then query parameters with defaults (`limit`, `offset`), and the auth dependency **last** (`_` or `user`) when the route has one — `hex-restapi-auth`.

### Status codes (defaults)

6. **The operation fixes the success status and the return type.**

| Operation | Decorator | Return type |
|-----------|-----------|-------------|
| `GET` list | default 200 | `FooListResponse` |
| `GET` single | default 200 | `FooResponse` |
| `POST` create | `status_code=201` | `FooResponse` (read-back) |
| `PATCH` update | default 200 | `FooResponse` (read-back) |
| `DELETE` | `status_code=204` | `Response(status_code=204)` |

For 204 endpoints, the function return annotation is `-> Response` and the body is `return Response(status_code=204)`. **Do not return `None`** — the 204 then lives in the decorator alone, and a decorator that loses its `status_code=204` answers 200 with a JSON `null` body instead of failing visibly.

### What the route advertises

The per-operation code sets and the helper are in the sibling `CONTRACTS.md`; registering a middleware's status is `hex-restapi-app`'s.

7. **Routes only advertise.** A route never builds an error response itself: one translator owns the error body's shape, and a hand-built body is the copy that drifts from it. The error catalogue and boundary translation are `exception-catalog`'s; logging is `python-logging`'s.
8. **Advertise exactly what the route can produce.** The set follows from the operation — which domain exceptions its handler can raise, which middleware sits in front of it, and whether it takes any validated input. A code that cannot occur is removed — an auth code follows the auth dependency (`hex-restapi-auth` rule 7); a code that can occur and is missing makes the published document wrong in the direction clients notice last.
9. **Never hand-write the advertisement mapping** — `responses={404: {...}}` typed out at the decorator. Always go through the helper, because the helper is what checks the code against the set of codes something can actually produce; a hand-written entry is the one path by which a status nothing raises reaches the document, and the helper rejects a status nothing maps or registers (`hex-restapi-app`).
10. **A route taking any validated input advertises the input-validation status.** Path parameter, query parameter, filter, pagination or body — any of them can be rejected before the handler runs, so the document must say so. It is *any-input* validation, not body validation: a lone `{id}` produces it, and only a parameterless, body-less route omits it. Where the framework publishes a response of its own for that status, the decorator still names it: the framework's entry describes the framework's error body, not the one the app sends.

### Handler injection

```python
handler: FromDishka[ListFoosHandler],
```

11. **The handler is injected per request, by its concrete class** — never by binding name, never at module level (`hex-wiring`; `hex-architecture` rule 8). The concrete class is also what gives the type checker `execute`, and a module-level resolution would defeat the per-test composition root.
12. **A response needing fields the command's result does not carry is a read-back** through the matching query handler, or the query's result DTO is extended (`hex-application`). For create/update with read-back, take `handler` and `get_handler` as two separate injected parameters with distinct names.

### Route reachability

13. **Every route the file declares must be the one a matching request actually reaches.** A path a more general sibling can also match is dead, and it fails silently — the wrong handler runs and answers, so there is no routing error to see. Where the framework resolves paths by a rule the file's own layout can violate — declaration order, a first-match table — satisfying that rule is part of writing the route. The FastAPI spelling is under `### Route ordering` above.

### What never goes in a route

14. **No `try/except`.** Domain exceptions propagate to the central error handler. The only sanctioned exception is rule 21.
15. **No logging.** Which layer logs is `hex-architecture`'s; the event's shape is `python-logging`'s.
16. **No business logic, no policy checks, no domain construction beyond mapping body→command.** Constructing the entity is the handler's job.
17. **No infrastructure imports.** Only `application/*` and `domain/*` types.
18. **No `Depends` factories at module level.** The auth pair is the one exception, and `require_role` is still called inline at each route (`hex-restapi-auth` rule 5).

### Routes that carry a file — only where the resource has one

19. **The route moves the bytes and does nothing else with them.** An upload's bytes go onto the
    command unparsed; a download's bytes, or its stream, come back from the handler untransformed.
    Parsing, generating and storing them are the handler's and an adapter's (`hex-application`,
    `hex-capability-adapter`); the route never writes to or serves from a path on disk.
20. **An upload is bounded before the framework reads it.** The framework reads the whole body before
    the route runs, so the bound sits ahead of it — the app's request-size middleware on the declared
    length, whose status the route then advertises, or the edge; a bounded read in the route only keeps
    an over-size file out of memory.
21. **A body part the framework does not validate is validated in the route, and its rejection
    translated.** A JSON document carried in a form field beside a file is parsed with its wire model,
    and the model library's error becomes the catalogue's validation class, naming the fields by
    location and never echoing a value. This is rule 14's one exception; a JSON-only route never needs it.
22. **A binary response states its media type, and the published document describes it as that type,
    never as a JSON model.** A header a cross-origin page must read is exposed where the app declares
    CORS (`hex-restapi-app`).

## Inlined typing / import rules

- `Annotated` from `typing`; `UUID` from `uuid`.
- `DishkaRoute`, `FromDishka` from `dishka.integrations.fastapi`. `Request` is **not** imported unless a route genuinely reads the raw request; reaching the composition root is not such a reason.
- `APIRouter`, `Query` from `fastapi`; `Response` from `fastapi.responses`.
- Application handlers imported through the subpackage (`from myapp.application.foos import ...`) — see `python-packaging` for the collapsed-import convention.
- `error_responses` from `..schemas`.
- Full annotations on every parameter and on the return type; no `from __future__ import annotations` (`python-style`).

## Package wiring

### When the router file is new

After adding the route(s), register the router in `src/myapp/restapi/main.py`: the import goes at the top of the file, and the `app.include_router(...)` line between `register_error_handlers(app)` and `setup_dishka(...)` (`hex-restapi-app`):

```python
from .routers.foos import router as foos_router

app.include_router(foos_router)
```

`restapi/routers/__init__.py` stays empty — every route module exports a colliding `router`
(`hex-architecture`, entrypoint carve-out).

## Hard stops

- A route is asked to catch a domain exception and translate it → stop, use `hex-restapi-app`: a different status is an entry in `STATUS_BY_ERROR`, a new failure a class under `exception-catalog`.
- A third auth dependency type, or any other auth machinery, is proposed → stop, use `hex-restapi-auth`; this skill declares the codes a route advertises, not the auth layer behind them.
- Asked for the request or response models a route maps → stop, use `hex-restapi-schema`.
