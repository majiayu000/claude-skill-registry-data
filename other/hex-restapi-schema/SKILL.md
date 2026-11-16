---
name: hex-restapi-schema
description: Use when a REST request or response body gains or changes a field — the pydantic models in `restapi/schemas/<resource>.py` (`FooResponse`, `FooListResponse`, `FooCreateRequest`, `FooUpdateRequest`), PATCH `T | None = None` semantics, pagination shape, schema exports. Not the domain entity they mirror (`hex-domain-model`) and not the route that maps them (`hex-restapi-endpoint`).
---

# Hex REST — API Schema

Produces one resource's schema module — the declared HTTP wire format for that resource, written here as pydantic models. The module is the boundary itself: domain entities never cross the wire, and schemas never cross into application or domain code.

## When to use vs. neighbours

- Per-resource Pydantic schemas (request/response), including a field added to or removed from a body → this skill.
- The route that consumes these schemas and maps them field by field → `hex-restapi-endpoint`.
- The entity, value object, enum or filter record these models mirror — never imported here beyond enums → `hex-domain-model`.
- Cross-cutting `ErrorResponse` / `error_responses()` in `restapi/schemas/errors.py` → `hex-restapi-app`; which of those codes a route advertises → `hex-restapi-endpoint`.
- The handlers beneath this delivery layer, and the command DTO carrying the same partial-update contract → `hex-application`.
- The container beneath this delivery layer → `hex-wiring`.
- The four schema names and any field name → `naming`; `__all__` and the wildcard re-export into `schemas/__init__.py` → `python-packaging`.
- Asserting a response body in a test → `hex-test-restapi-endpoint`.

## Template — pydantic

### File location

```
src/myapp/restapi/schemas/foos.py        # the resource's schemas
src/myapp/restapi/schemas/__init__.py        # update to re-export
```

The module holds several classes on purpose: one resource's request and response models are a closed set of declarations that change together, the case `python-packaging` lets share a module named for the set. A nested model used only by this resource's bodies lives in the same file.

### Schema module

```python
from collections.abc import Sequence
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field

__all__ = [
    "FooCreateRequest",
    "FooListResponse",
    "FooResponse",
    "FooUpdateRequest",
]


class FooResponse(BaseModel):
    id: UUID
    name: str
    note: str | None


class FooListResponse(BaseModel):
    items: Sequence[FooResponse]
    total: int
    limit: int
    offset: int


class FooCreateRequest(BaseModel):
    name: Annotated[str, Field(min_length=1)]  # mirrors Foo's non-empty-name invariant
    note: str | None = None


class FooUpdateRequest(BaseModel):
    name: Annotated[str | None, Field(min_length=1)] = None
    note: str | None = None
```

Absent and `null` both parse to `None`, which leaves the field unchanged (rule 6).

## Other bindings

- **msgspec `Struct`, or attrs with a conversion layer.** The declarations and the constraint spelling
  change — a `Meta` annotation or a validator argument instead of `Field`, an explicit decode step
  instead of model construction. Unchanged: the four names, the in-file order, the partial-update
  contract, the one-pagination-shape rule, and the ban on domain types crossing into the module.
- **A plain dataclass plus an explicit validation step.** Honest only with the validation step actually
  written: something must reject a wrong shape *before* the handler sees it and must feed the published
  API document. A bare dataclass does neither, so rule 4 has nothing to attach to and the boundary stops
  being a boundary.
- **Whatever the web framework parses bodies and generates its schema from.** If the framework
  understands one model library only, that library is the binding: swapping it means supplying the
  parse-and-document step yourself, not renaming a base class.

## Rules

### Naming

1. **A CRUD resource's bodies take four names, and no other suffix** (`naming` for the shared rules).

| Schema | Purpose |
|--------|---------|
| `FooResponse` | Single-entity GET / POST / PATCH response |
| `FooListResponse` | List GET response — `items` + the resource's pagination fields (offset: `total`/`limit`/`offset`; cursor: `next_cursor`/`limit`), matching `hex-domain-model` |
| `FooCreateRequest` | POST body |
| `FooUpdateRequest` | PATCH body — every field `T \| None = None` |

Do **not** introduce alternate suffixes (`Dto`, `Schema`, `In`, `Out`). Another operation's body or response is `Foo<Operation>Request` / `Foo<Operation>Response` (`naming`'s role suffixes) in the same module, and a nested object is its own model (rule 11).

### Class form

2. **Each schema is a flat, self-contained declaration of one wire shape.** No shared base carrying "common fields" across resources — repetition is intentional. The file must read top to bottom as the JSON a client will see, with no field inherited from out of frame.
3. **Order in the file:** `Response`, `ListResponse`, `CreateRequest`, `UpdateRequest`, then any nested model. Reads above writes; single above list.

### Validation

4. **Only request schemas constrain their input, and the constraint is declared on the field** (`python-style`, *Validation models*). A response carries no constraint: its data already passed the domain's invariants.
   **Every bound restates a limit the domain already has** — an entity invariant, a value object's range, the width a field is persisted at. Restating it is intentional (schemas are wire contracts, and rejecting at the edge beats a 500 later); *inventing* it is not. A number with no domain behind it is a guess that will disagree with the domain the first time either moves.
5. **A field constraint enforces input *shape* — length, range, pattern — never a business rule.** The test: a constraint that has to read another field, another aggregate, or the clock is a business rule, and it belongs on an entity or a policy. Only what can be checked from the one value in front of you belongs here; no computed property or validator method encodes a rule either.

### PATCH semantics

6. **Every field on `*UpdateRequest` is `T | None = None`**, and `None` is "leave unchanged".
7. **`*CreateRequest` lists required fields without `None`**, and gives a default only to an input that is genuinely optional. A create body with every field optional is an update body.

### `*ListResponse`

8. **`*ListResponse` carries the resource's pagination shape — whichever one its filter record uses** (`hex-domain-model`'s one-pagination-shape rule for filter records picks exactly one), never a third:
   - **offset paging** → `items: Sequence[FooResponse]`, `total: int`, `limit: int`, `offset: int`.
   - **cursor paging** → `items: Sequence[FooResponse]`, `next_cursor: str | None`, `limit: int`.
   The route `hex-restapi-endpoint` builds constructs whichever shape the filter uses, so the schema must match it (see `hex-restapi-endpoint`'s cursor-list note). Don't mix the two.

### What never goes in a schema file

9. **No domain types beyond enums.** `FooResponse` does not import the `Foo` entity, and a value object crosses as its primitive fields, mapped in the route.
10. **No persistence concerns.** Nothing that builds a schema straight from a stored row or mapped object — no ORM mode, no from-row constructor, no storage library's column types. A schema that can construct itself from the database has tied the wire format to the table, and the two then have to move together.
11. **No bare `dict` or `list` field standing in for a nested object.** A nested body is its own model in this file, declared and ordered like any other; a `dict` field publishes a hole in the wire contract that no generated document can describe. `python-style` owns the declared-record rule.

### Existing cross-cutting request schemas

12. **A request schema several resources share that already exists in its own module is reused**, never re-declared per resource. None is presumed: most apps have none, so don't assume one exists.

## Inlined typing / import rules

See `python-style` and `python-packaging` for the shared typing and import rules.

- **Allowed:** `pydantic`, stdlib (`uuid`, `collections.abc`, `datetime`, `decimal`, `typing`), and **domain enums only** (`FooCategory`, `Role`).
- **Forbidden:** domain entities, value objects and other dataclasses, repositories, application handlers, infrastructure types. Routers map field-by-field; the schema must not know about `Foo` the entity.
- **No `from __future__ import annotations`** (`python-style` — the model library reads annotations at runtime).
- **No `Optional[...]`** — `T | None` (`python-style`).

## Package wiring

After writing the module, update `restapi/schemas/__init__.py`:

```python
from . import errors, foos
from .errors import *
from .foos import *

__all__ = errors.__all__ + foos.__all__
```

`errors` is `hex-restapi-app`'s and stays; each resource module joins it in alphabetical order.

See `python-packaging` for package re-exports and `__all__` composition.

## Hard stops

- Asked to change `ErrorResponse` or `error_responses()` in `restapi/schemas/errors.py` → stop, use `hex-restapi-app`.
- Asked to map a schema to a command, or a result to a schema → stop, use `hex-restapi-endpoint`; the route maps field by field.
