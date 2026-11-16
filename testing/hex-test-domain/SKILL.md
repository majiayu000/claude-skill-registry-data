---
name: hex-test-domain
description: Use when testing a domain entity, value object, enum or domain service with stdlib, `pytest` and `myapp.domain` — no IO, no fixtures, no container, and an orchestrator service run on the in-memory fake of its port. Covers identity equality, one test per invariant and the pinned enum member set; a frozen value object with neither an invariant nor a normalized equality gets no test file at all. Not for writing the domain object itself — `hex-domain-model` or `hex-domain-service`.
---

# Hex Test — Domain

Consult `test-principles` for the testing constitution. Where this skill contradicts `test-principles`, the constitution wins.

The four kinds of test the domain layer takes: stdlib plus `pytest` plus `myapp.domain.*`, and for an
orchestrator service the hand-written fake of its port.

## When to use vs. neighbours

Inside this skill, by what is under test — the four templates under `## Template(s)`. Outside it:

- An application command or query handler → `hex-test-application-handler`.
- An in-memory fake under `tests/unit/fakes/` → `hex-test-application-handler`.
- A grep-firewall architectural rule → `test-architecture-rule`.
- The infrastructure adapter implementing a protocol a service depends on → `hex-test-repository-contract` (repository) or `hex-test-capability-adapter` (capability). A normalizing function is tested here when it is pure domain logic with no library behind it; one that delegates to an external library sits behind a capability port, and its adapter is `hex-test-capability-adapter`'s.
- The handler that *uses* a service, end to end → `hex-test-restapi-endpoint`.
- The domain object itself rather than its test → `hex-domain-model` (entity, value object, enum) or `hex-domain-service`.
- Anything that needs a fixture, a container or a database — "add a testcontainer fixture for Postgres" included → `hex-test-integration-setup`; nothing in this skill takes a fixture.
- The no-mocks rule and the pure-unit speed target → `test-principles`.

## Template(s) — pytest, stdlib dataclass domain objects

Inside this skill, by what is under test:

- A `@dataclass` entity with UUID identity → **Entity**.
- A frozen value object **with** `__post_init__` invariants or a normalized equality → **Value object**.
- A `StrEnum` / `Enum` member set → **Enum**.
- A domain service with injected protocols, or the module-level function a pure transformation takes
  instead of a class (`hex-domain-service`) → **Domain service**.

File placement mirrors the source file (`test-principles`): the test for
`domain/<subdomain>/<module>.py` is `tests/unit/domain/<subdomain>/test_<module>.py`, whatever kind of
object the module holds — `foo.py` → `test_foo.py`, `foo_status.py` → `test_foo_status.py`,
`foo_uniqueness_service.py` → `test_foo_uniqueness_service.py`. The file name adds no suffix the
module name does not already carry.

The enum below is `FooStatus`, a `StrEnum` of `ALPHA` and `BETA`.

### Entity — standard

```python
import uuid

import pytest

from myapp.domain.exceptions import ValidationError
from myapp.domain.foos import Foo


def _foo(*, id: uuid.UUID | None = None, name: str = "Test", note: str | None = None) -> Foo:
    return Foo(id=id or uuid.uuid4(), name=name, note=note)


def test_equality_by_id() -> None:
    shared_id = uuid.uuid4()
    foo = _foo(id=shared_id, name="alpha")
    same_id = _foo(id=shared_id, name="beta")
    other = _foo(name="alpha")

    assert foo == same_id
    assert foo != other
    assert hash(foo) == hash(same_id)
    assert hash(foo) != hash(other)


def test_name_must_be_non_empty() -> None:
    with pytest.raises(ValidationError) as exc_info:
        _foo(name="")
    assert exc_info.value.context["field"] == "name"
```

The builder spreads **only the entity's real declared fields** — `id` plus its domain fields — because a
domain test constructs the subject the way the domain layer declares it and knows nothing of what a
store adds around it. Two things it must therefore not carry: `created_at` / `updated_at`, which are not
entity fields at all (`hex-domain-model`, Entity rule 6 — the store maintains them), so `Foo(created_at=...)` fails; and any `import datetime` that exists only to feed them.
`datetime` enters the file **only** when the entity genuinely declares a datetime domain field.

### Value object — invariants

```python
import pytest

from myapp.domain.exceptions import ValidationError
from myapp.domain.foos import FooQuota


def test_field_b_must_be_non_negative() -> None:
    with pytest.raises(ValidationError) as exc_info:
        FooQuota(field_a="alpha", field_b=-1)
    assert exc_info.value.context["field"] == "field_b"
```

A value object that stores a raw input beside its normalized form and compares by the normalized field
(`hex-domain-model`) adds one equality test: two instances with the same normalized field and different
raw inputs are equal and hash alike (rule 9).

### Enum — values plus rejection

```python
import pytest

from myapp.domain.foos import FooStatus


def test_values() -> None:
    assert FooStatus.ALPHA == "ALPHA"
    assert FooStatus.BETA == "BETA"

    with pytest.raises(ValueError, match="GAMMA"):
        FooStatus("GAMMA")
```

An enum may carry a pure method over its own values; its test adds that method at, above and below
the bar. The rank-ordered `Role` in `hex-restapi-auth` is the worked one.

### Domain service — orchestrator, on the fake of its port

```python
import uuid

import pytest

from myapp.domain.exceptions import FooConflictError
from myapp.domain.foos import Foo, FooUniquenessService
from tests.unit.fakes import FakeFooRepository


def _service(existing_names: list[str] | None = None) -> FooUniquenessService:
    foos = [Foo(id=uuid.uuid4(), name=name) for name in existing_names or []]
    return FooUniquenessService(repository=FakeFooRepository(items=foos))


async def test_assert_name_available_raises_when_taken() -> None:
    service = _service(["alpha"])
    with pytest.raises(FooConflictError) as exc_info:
        await service.assert_name_available("alpha")
    assert exc_info.value.context["field"] == "name"


async def test_assert_name_available_passes_when_free() -> None:
    service = _service([])
    await service.assert_name_available("alpha")  # does not raise
```

## Rules

### All four kinds

1. **A domain test is synchronous unless the thing under test is awaited.** Only a test of an async
   method is declared async; making the rest async buys nothing and hides which subjects do IO-shaped
   work. Async configuration and markers → `test-principles`.
2. The no-mocks contract — no `MagicMock` or `AsyncMock` → `test-principles`. The domain has no IO to
   stub, and where a stand-in is needed (a service's injected protocol) it is hand-written — the port's
   fake, or a class for a narrow protocol (rule 15).
3. Test what the author wrote, never what the data model already guarantees → `test-principles`, assert
   strength. In the domain that means the constructor's invariants, the computed properties and the
   methods, and never the equality, hash or immutability a frozen `@dataclass` supplies — nor log
   output: the domain layer logs nothing at all (`hex-architecture`, *Who logs, by layer*), so a test
   asserts the return value or the raised exception.
4. **One test per invariant, and a rejection test asserts the failure's machine-readable field key,
   never its message** → `test-principles` *Assert strength* recipe 6. Several failure modes of the
   *same* invariant group under one test named after that invariant; two different invariants never
   share a test.

### Entity

5. **The four-line identity-equality block is the contract**: equality by id only, and `hash` agreeing
   with `eq`. Do not paraphrase it.
6. **`_<entity>(*, <field>: <type> = <valid default>, …)` is a module-level `def`** with one
   keyword-only, annotated parameter per declared field and valid defaults, so construction with no
   arguments succeeds. It takes nothing the entity does not declare — `created_at` / `updated_at` are
   the usual case: the store maintains them, so they are not entity fields (`hex-domain-model`, Entity
   rule 6). **No logic in it beyond a fresh id** — it is a dumb spreader, and computation
   belongs in the tests.
7. **A computed property or method gets its own `test_*`** named after the rule — but only when the entity
   actually declares one. Do not add a lifecycle or archive test to an entity that has no such property;
   that is a per-aggregate feature, not a default.

### Value object

8. **Write no file for a value object that declares no invariant of its own and no custom equality.**
   There is nothing the author wrote left to pin (rule 3).
9. **A normalized-equality test pins the rule, not Python's `==`**: two instances with the same
   normalized field must be equal even when their raw fields differ, and `hash` must agree.
10. **No builder.** Value objects are small — pass the fields directly.

### Enum

11. **Pin every member with an explicit assertion**, one line each. The database and the wire format
    depend on these strings, so a silent rename must break the test.
12. **Never loop over members.** `for member in FooStatus: assert member.value == member.name` masks the very bug it
    looks like it catches — a renamed value still passes.
13. **Always include the unknown-value rejection**:
    `with pytest.raises(ValueError, match="<unknown>"): FooStatus("<unknown>")` proves the enum is
    closed — the value in the message is the only thing distinguishing the failure (`test-principles`
    *Assert strength* recipe 6).
14. **One `test_*` per pure-logic method**, named after the method, asserting every relevant
    input/output pair; a boolean is asserted as `test-principles` states (`is True` / `is False`).

### Domain service

15. **An orchestrator runs on the fake of the port it takes.** A service that takes the whole
    repository port (`IFooRepository`) is built on `FakeFooRepository` from `tests.unit.fakes`
    (`hex-test-application-handler`): under a strict type checker a stand-in must satisfy the whole
    protocol, and that fake already does, with the real adapter's exception contract. A minimal inline
    class is allowed only when the service's parameter is a protocol declaring exactly the methods it
    calls — it then implements that protocol and nothing more, which keeps the narrow dependency
    surface visible. Where that fake does not exist yet, write it first under
    `hex-test-application-handler` (its `FAKES.md`).
16. **The `_service(...)` factory returns the constructed service**, hiding the collaborator plumbing
    from each test body.
17. **One `test_*` per behaviour of each method**, named so the test name *is* the behaviour's one-line statement —
    `test_assert_name_available_raises_when_taken`, `test_assert_name_available_passes_when_free`.
18. **A domain function is called directly.** It has no instance to construct, share or fake.
19. **A normalizing function has `test_idempotent`** — parametrized over a few representative inputs,
    asserting `f(f(x)) == f(x)`, one reported case per input (`test-principles`, *When to
    parametrize*). Idempotence is part of the normalization contract.

## Inlined typing / import rules

Identical for all four kinds:

- Stdlib (`uuid`, and `datetime` only when genuinely needed) plus `pytest` plus `myapp.domain.*`, and
  `tests.unit.fakes` for an orchestrator's collaborators. No infrastructure, no application, no restapi,
  no Pydantic, no SQLAlchemy.
- Full annotations on a builder or factory and on an inline stub class. Tests are
  `def test_*() -> None` or `async def test_*() -> None`.
- No `from __future__ import annotations`.

## Hard stops

- A test here needs a database, an HTTP endpoint or blob storage → stop, use
  `hex-test-repository-contract`, `hex-test-restapi-endpoint` or `hex-test-capability-adapter`.
- The value object declares no invariant of its own and no custom equality → stop, produce no file
  (rule 8).
