---
name: hex-domain-ports
description: Use when defining a `typing.Protocol` port in the domain — the `I`-prefixed interface adapters satisfy structurally, `IFooRepository` for one aggregate root's data access or `ICan<Verb>` for a single external action. The interface, not its implementation — that is `hex-persistence`, `hex-store-repository` or `hex-capability-adapter`.
paths: ["**/domain/**"]
---

# Hex — Domain Ports

The domain's outbound interfaces. Both are `typing.Protocol` modules holding method signatures and
nothing else; infrastructure satisfies them **structurally** (`hex-architecture` rule 7).

## When to use vs. neighbours

- Aggregate-root data access — CRUD plus aggregate-specific reads → **repository protocol** (`IFooRepository`), in this skill.
- A single action that does IO or talks to an external system — file rendering, token verification, blob storage, a third-party gateway call → **capability protocol** (`ICan<Verb>`), in this skill.
- A pure-CPU operation a third-party library performs — JWT signature verification, rendering bytes through a document library → **capability protocol**, with a sync method instead of async; the domain cannot import the library, and the port is how it uses one.
- Pure-CPU logic the standard library can do — trimming, case-folding, a stdlib URL normalization → no port; a value object's construction (`hex-domain-model`) or a module-level domain function (`hex-domain-service`).
- The entity, value object, enum or filter record the signatures mention → `hex-domain-model`. `FooKind`, which the capability port below returns, is an enum of that skill's `StrEnum` form, in `domain/foos/foo_kind.py`.
- A rule needing cross-aggregate state, which *consumes* these protocols → `hex-domain-service`.
- A concrete repository implementation → `hex-persistence` (a relational store) or `hex-store-repository` (a client-style store). The protocol itself is store-agnostic; the choice is made by store profile (`hex-conventions` block B).
- A concrete capability implementation → `hex-capability-adapter`.
- An in-memory fake satisfying one of these protocols in a unit test → `hex-test-application-handler`.
- Binding a concrete implementation to the protocol by type → `hex-wiring`.
- The token-verifier port, its adapter and the route dependency that resolves it → `hex-restapi-auth`; it is the sync shape, bound to auth, and exists only in an app whose entrypoint authenticates.
- The `i_` and `i_can_` filename prefixes and the rest of the identifier derivation → `naming`.
- The command or query handler that consumes one of these protocols → `hex-application`.
- The reversing method a compensating handler calls on one of these ports (`delete` beside `upload`) → a port method like any other, which raises on failure; the handler-side guard that tolerates its failure is `hex-application`'s (Compensation).

## Template(s) — stdlib `typing.Protocol`

### Repository protocol

```python
from collections.abc import Sequence
from typing import Protocol
from uuid import UUID

from .foo import Foo
from .foo_list_filter import FooListFilter

__all__ = ["IFooRepository"]


class IFooRepository(Protocol):
    async def list(self, *, filter: FooListFilter) -> Sequence[Foo]: ...
    async def count(self, *, filter: FooListFilter) -> int: ...
    async def get_by_id(self, id: UUID) -> Foo: ...
    async def get_by_name(self, name: str) -> Foo | None: ...
    async def create(self, foo: Foo) -> None: ...
    async def update(self, foo: Foo) -> None: ...
    async def delete(self, id: UUID) -> None: ...
```

### Repository protocol — a store that answers only some reads

A port declares what its store can answer, never more. A key-value store reaches a record by its key and
nothing else, so a `Baz` kept there is created, fetched by id and deleted — a `list`, a `count` or a
`get_by_name` would need a secondary index the store does not keep. Its repository port is still
`IBazRepository`, and simply declares those three: a repository port may be narrower than full CRUD, and
a handler that needs a read the port lacks needs the aggregate on a store that can answer it:

```python
from typing import Protocol
from uuid import UUID

from .baz import Baz

__all__ = ["IBazRepository"]


class IBazRepository(Protocol):
    async def create(self, baz: Baz) -> None: ...
    async def get_by_id(self, id: UUID) -> Baz: ...
    async def delete(self, id: UUID) -> None: ...
```

An index kept beside the authoritative store is the same rule again: its own narrower port, whose verbs
are what that index answers.

### Capability protocol — a third-party gateway call (async, the default in an event-loop program)

```python
from typing import Protocol

from .foo import Foo
from .foo_kind import FooKind

__all__ = ["ICanClassifyFoos"]


class ICanClassifyFoos(Protocol):
    async def classify(self, foo: Foo) -> FooKind: ...
```

### Capability protocol — a reversible action (the forward operation and its undo)

```python
from typing import Protocol

__all__ = ["ICanStoreFoos"]


class ICanStoreFoos(Protocol):
    async def upload(self, key: str, body: bytes) -> None: ...
    async def delete(self, key: str) -> None: ...
```

Reading the stored bytes back is a second action, so it is a second port, which one adapter may also
satisfy (`hex-capability-adapter`).

A pure-CPU port backed by a third-party library declares its method sync (`def`, not `async def`);
otherwise it has the same form.

## Rules

Two shapes, and the split is about mental model rather than size: a **repository** is the collection of
one aggregate root, a **capability** is a single action the domain needs but cannot perform itself.

- Aggregate-root data access — CRUD plus aggregate-specific reads → **repository protocol**.
- A single action that does IO or talks to an external system — file rendering, blob storage, a
  third-party gateway call → **capability protocol**.
- A pure-CPU operation that needs a third-party library — verifying a signature, rendering in-memory
  bytes through a document library → **capability protocol**, with a sync method instead of async.
  Pure-CPU logic the standard library can do is not a port at all: it lives in the domain, as a value
  object's construction or a module-level domain function.

The protocol itself is store-agnostic; the choice is made by store profile (`hex-conventions` block B).

### File location and naming

| | Path | Class |
|---|---|---|
| Repository | `src/myapp/domain/foos/i_foo_repository.py` | `IFooRepository` |
| Capability | `src/myapp/domain/foos/i_can_<verb>.py` | `ICan<Verb>` |

Follow `naming` for protocol names and prefixes, and `python-packaging` for module boundaries.

Place a capability where its primary input lives. Cross-cutting ones — auth, observability — go in their
own subdomain package (`domain/auth/`, `domain/observability/`).

### Both shapes

1. **A port is a structural interface with no behaviour** — method signatures and nothing else. Declare
   it with `typing.Protocol` (`python-style` owns the declaration form and runtime checking), never an
   abstract base class: a base class makes satisfaction a matter of inheritance, and the point of a port
   is that an adapter the domain has never heard of satisfies it.
2. **No default implementations and no docstring standing in for one.** A body the adapter inherits is
   behaviour that escaped the layer that owns it. Comments and docstrings follow `python-style`.
3. **Parameters and return types are domain types or primitives.** Never a database row, an SDK object
   or a validation model: a port typed in an adapter's vocabulary drags that library into every caller,
   and the domain then cannot be imported without it.
4. **Infrastructure satisfies the port structurally** — the adapter neither inherits nor imports it
   (`hex-architecture` rule 7).
5. **No class-level state and no helper methods.** Both belong to the adapter — a helper on the port is a
   decision the domain has taken on the adapter's behalf, and every adapter then inherits it.

### Repository protocol

1. **Every method carries the same mode, and the mode is the program's.** A repository method reaches a
   store, so in a program that runs an event loop it is `async` — there a sync signature forces every
   future adapter to either block the loop or break the contract. A program that runs no event loop — a
   synchronous batch job, a single-command entrypoint that returns — declares the port sync throughout,
   and the templates above are the async mode. What is not negotiable is **uniformity within one port**:
   never a mix, because the mode is part of every signature an adapter and a caller must match, and
   changing it later changes both sides at once.
2. **Keyword-only arguments for `list`, `count` and any multi-parameter method**; positional only on a
   single-parameter lookup such as `get_by_id(id)`. Two positional parameters of the same type are
   silently swappable at the call site and no checker catches it — a one-parameter lookup cannot be.
3. **The return shape states what "missing" means, and the adapter has no say in it:**
   - `get_by_id` fails when missing — never `Foo | None`; the error class is `exception-catalog`'s.
   - `get_by_<other>` may return `Foo | None`, and does so exactly when "not found" is a normal outcome.
   - `list` returns a read-only view (`Sequence[Foo]`) — see `python-style` for why a read-only return
     type is not the same as a `list`.
   - `create` / `update` / `delete` return `None`. A write that returns data is a query in disguise.
4. **A port declares the methods some handler calls.** A method no use case reaches is not declared,
   however standard — the template is a CRUD service's full set.
5. **Every method belongs to the one aggregate's collection.** Single actions sharing no collection
   mental model — more than about three of them is the sign — are one or more capability protocols, not
   repository methods.

### Capability protocol

1. **One method is the default; two is the maximum**, and only when the pair is one reversible action —
   `upload` plus `delete` on the same key. Three or more means the port has stopped being one action:
   split it, or model it as a repository.
2. **In a program that awaits its IO, async unless the operation is pure CPU.** Anything that may do IO
   is `async`; sync is reserved for work that provably cannot block — cryptographic, parsing and
   encoding helpers. Getting this wrong is only discovered under load, because the sync port cannot be
   widened without changing every caller. A program that runs no event loop has no such split — every
   method is sync — and the split returns the moment one is introduced, which is why the distinction is
   worth recording even there (`hex-domain-service` states the same condition for a service method).

## Inlined typing / import rules

Follow `python-style` and `python-packaging`; the load-bearing slice is:

- **`class IName(Protocol)` from `typing`.** Never `abc.ABC`, never a concrete base class.
- **No `@runtime_checkable`** unless the codebase genuinely does `isinstance(x, IFoo)`. Default off.
- Stdlib only — `typing`, `collections.abc`, `uuid`, `datetime` — plus relative domain imports. No
  third-party. No `from __future__ import annotations`.
- `X | None`. `Sequence[T]` from `collections.abc` for read-only views.
- Full annotations on every parameter and every return type.
- No comments unless a non-obvious *why*; one short line at most.

## Package wiring

Follow `python-packaging` for package exports and `hex-architecture` for layer placement.

## Hard stops

- Asked for the class that implements a port → stop, use `hex-persistence` or `hex-store-repository`
  for a repository, `hex-capability-adapter` for a capability.
- Asked for a port over pure-CPU logic the standard library can do → stop, there is no port; use
  `hex-domain-model` or `hex-domain-service`.
