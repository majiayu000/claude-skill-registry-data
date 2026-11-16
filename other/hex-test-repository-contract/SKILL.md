---
name: hex-test-repository-contract
description: Use when testing an aggregate's repository adapter — an `IFooRepository` implementation — against the real backend rather than a fake, in both halves of that contract, relational over Postgres through the `session_factory` rollback fixture (constraints on insert and on update, cascades, the pinned constraint name) and client-store (key-value, document) isolated by a fresh per-test namespace. Not a flat-layered service's storage-package write path, which is `flat-test-persistence`, in the `pyhouse-flat` plugin, not a capability port's adapter, which is `hex-test-capability-adapter`, and not the fixtures it consumes — containers, the migration run and `session_factory` are `hex-test-integration-setup`'s.
---

# Hex Test — Repository Contract

Consult `test-principles` for the testing constitution. Where this skill contradicts `test-principles`, the constitution wins.

One integration-test file per repository adapter, driven against the **real** backend. This layer catches
what unit coverage cannot.

## When to use vs. neighbours

- A repository adapter on a relational store, under `infrastructure/postgres/repositories/` → the **relational** half of this skill.
- A repository adapter on a client-style store (key-value, document), under `infrastructure/<store-kind>/repositories/` → the **client-style** half of this skill.
- An adapter behind an `ICan<Verb>` capability port rather than an `IFooRepository` → `hex-test-capability-adapter`, not this skill — even when it is driven against a container.
- Schema-only checks (an index exists, a migration carries data correctly) → separate flat files under `tests/integration/postgres/` (`test_indexes.py`, `test_<NNNN>_migration.py`) that take the `run_alembic` fixture (`hex-test-integration-setup`), not `session_factory`.
- HTTP-layer integration (route, OpenAPI) → `hex-test-restapi-endpoint`; the authenticated and role-gated variants of those tests → `hex-test-restapi-auth`.
- The rollback `conftest.py`, the session containers and the migration run themselves — including "add a testcontainer fixture for Postgres" → `hex-test-integration-setup`. This skill consumes `session_factory`; it never defines it.
- A pure domain test, with no backend at all → `hex-test-domain`.
- The repository being tested → `hex-persistence` (relational, with `REPOSITORY.md` and `TABLE.md`) or `hex-store-repository` (client store).
- An in-memory fake of the same protocol, for handler unit tests → `hex-test-application-handler`.
- The exceptions the adapter translates integrity errors and SDK errors into → `exception-catalog`.
- Speed targets, fixture placement and the substitution ladder → `test-principles`.
- The write path is a flat-layered service's own data-access package rather than a hexagonal `IFooRepository` adapter → `flat-test-persistence`, in the `pyhouse-flat` plugin; it consumes `flat-test-integration-setup`'s fixtures there, not `session_factory`.

## Template(s) — pytest, testcontainers, SQLAlchemy async over Postgres, redis-py

- **Relational** — real `UNIQUE` and `FK` violations, real `ON DELETE CASCADE` semantics, the
  `IntegrityError`-to-domain-exception translator's constraint-name map, and the `updated_at` the
  repository writes on update.
- **Client-style** (key-value, document) — the entity-record mapping round-trip and the
  SDK-error-to-domain-exception translation the adapter performs at its boundary. There is no SQL
  transaction and no constraint map here, so both the isolation mechanism and the load-bearing assertion
  are different.

The two halves share their purpose and their shape; they differ in isolation, and that difference is the
first thing to get right.

### Isolation — the one thing that differs

**Relational: transaction rollback.** Every test takes `session_factory: async_sessionmaker[AsyncSession]`, the fixture from
`hex-test-integration-setup`. The database is empty at test start and everything the test wrote is
discarded at teardown. No marker, no other DB fixture.

**Client-style: a fresh namespace.** A client store has no nested transaction, so the `session_factory`-rollback model does not apply (the rollback fixture is relational-only). **Each test owns a namespace** (rule 14), created or emptied in a fixture and dropped or emptied at teardown. Which conftest holds that fixture and which holds the session-scoped container is `hex-test-integration-setup`'s scope split, not this skill's.

### Relational

```
tests/integration/postgres/
└── test_<aggregate_snake>_repository.py
```

Default is one file per repository. **Concern-split when the single file stops being navigable** — when finding the test for one method means scrolling past several unrelated concerns, or when a change to one concern keeps forcing rereads of the others. The trigger is that loss of navigability, not a line count: a flat file of twenty near-identical `create` cases stays readable far longer than a short one mixing create, update and filter semantics. When it splits, **the filename names the concern** (`test_<aggregate>_repository_create.py`, `test_<aggregate>_repository_filters.py`), so the split is navigable in the directory listing and not just inside the file.

### Standard CRUD test file — SQLAlchemy async session factory

One test group per method the port declares and no others (rule 1); the conflict tests exist only where
the table has a natural key (`hex-persistence`, `TABLE.md`).

```python
import uuid
from dataclasses import asdict
from datetime import UTC, datetime

import pytest
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from myapp.domain.exceptions import (
    FooConflictError,  # only where Foo has a natural key
    NotFoundError,
    UpstreamError,
)
from myapp.domain.foos import (
    Foo,
    FooListFilter,  # only with a paged list
    FooSort,  # only with a paged list
)
from myapp.infrastructure.postgres.repositories import FooRepository
from myapp.infrastructure.postgres.tables.foos import foos_table

_PLANTED = datetime(2000, 1, 1, tzinfo=UTC)


def _foo(*, name: str = "alpha") -> Foo:
    return Foo(id=uuid.uuid4(), name=name, note="a note")


async def test_create_then_get_returns_every_field(session_factory: async_sessionmaker[AsyncSession]) -> None:
    repository = FooRepository(session_factory=session_factory)
    foo = _foo()

    await repository.create(foo)

    assert asdict(await repository.get_by_id(foo.id)) == asdict(foo)


async def test_get_by_id_of_absent_row_raises_not_found(session_factory: async_sessionmaker[AsyncSession]) -> None:
    repository = FooRepository(session_factory=session_factory)
    missing = uuid.uuid4()

    with pytest.raises(NotFoundError) as exc_info:
        await repository.get_by_id(missing)

    assert exc_info.value.context["id"] == str(missing)


# only where the port declares update
async def test_update_persists_the_new_values(session_factory: async_sessionmaker[AsyncSession]) -> None:
    repository = FooRepository(session_factory=session_factory)
    foo = _foo(name="alpha")
    await repository.create(foo)
    foo.name = "beta"
    foo.note = "another note"

    await repository.update(foo)

    assert asdict(await repository.get_by_id(foo.id)) == asdict(foo)


# only where the port declares update
async def test_update_of_absent_row_raises_not_found(session_factory: async_sessionmaker[AsyncSession]) -> None:
    repository = FooRepository(session_factory=session_factory)
    foo = _foo()

    with pytest.raises(NotFoundError) as exc_info:
        await repository.update(foo)

    assert exc_info.value.context["id"] == str(foo.id)


# only where the port declares delete
async def test_delete_removes_the_row(session_factory: async_sessionmaker[AsyncSession]) -> None:
    repository = FooRepository(session_factory=session_factory)
    foo = _foo()
    await repository.create(foo)

    await repository.delete(foo.id)

    with pytest.raises(NotFoundError) as exc_info:
        await repository.get_by_id(foo.id)

    assert exc_info.value.context["id"] == str(foo.id)


# only where the port declares delete
async def test_delete_of_absent_row_raises_not_found(session_factory: async_sessionmaker[AsyncSession]) -> None:
    repository = FooRepository(session_factory=session_factory)
    missing = uuid.uuid4()

    with pytest.raises(NotFoundError) as exc_info:
        await repository.delete(missing)

    assert exc_info.value.context["id"] == str(missing)


async def test_read_and_write_against_unreachable_store_raise_upstream_error() -> None:
    dead = create_async_engine("postgresql+asyncpg://u:p@127.0.0.1:1/none")  # nothing listening
    foo = _foo()
    try:
        repository = FooRepository(session_factory=async_sessionmaker(dead))
        with pytest.raises(UpstreamError) as read:
            await repository.get_by_id(foo.id)
        with pytest.raises(UpstreamError) as write:
            await repository.create(foo)
    finally:
        await dead.dispose()

    assert read.value.context == {"id": str(foo.id)}
    assert write.value.context == {"id": str(foo.id)}


# only where Foo has a natural key
async def test_duplicate_name_on_insert_raises_conflict(session_factory: async_sessionmaker[AsyncSession]) -> None:
    repository = FooRepository(session_factory=session_factory)
    await repository.create(_foo(name="alpha"))

    with pytest.raises(FooConflictError) as exc_info:
        await repository.create(_foo(name="alpha"))

    assert exc_info.value.context["constraint"] == "uq_foos_name"


# only where Foo has a natural key and the port declares update
async def test_duplicate_name_on_update_raises_conflict(session_factory: async_sessionmaker[AsyncSession]) -> None:
    repository = FooRepository(session_factory=session_factory)
    await repository.create(_foo(name="alpha"))
    second = _foo(name="beta")
    await repository.create(second)

    second.name = "alpha"
    with pytest.raises(FooConflictError) as exc_info:
        await repository.update(second)

    assert exc_info.value.context["constraint"] == "uq_foos_name"


# only where the port declares update
async def test_update_writes_updated_at(session_factory: async_sessionmaker[AsyncSession]) -> None:
    repository = FooRepository(session_factory=session_factory)
    foo = _foo()
    await repository.create(foo)
    async with session_factory() as session:
        await session.execute(update(foos_table).where(foos_table.c.id == foo.id).values(updated_at=_PLANTED))
        await session.commit()
    foo.name = "beta"

    await repository.update(foo)

    async with session_factory() as session:
        written: datetime = (
            await session.execute(select(foos_table.c.updated_at).where(foos_table.c.id == foo.id))
        ).scalar_one()
    assert written > _PLANTED


# only where the port declares a lookup by a natural key
async def test_get_by_name_returns_match(session_factory: async_sessionmaker[AsyncSession]) -> None:
    repository = FooRepository(session_factory=session_factory)
    await repository.create(_foo(name="alpha"))

    loaded = await repository.get_by_name("alpha")
    assert loaded is not None
    assert loaded.name == "alpha"


# only where the port declares a lookup by a natural key
async def test_get_by_name_returns_none_when_absent(
    session_factory: async_sessionmaker[AsyncSession],
) -> None:
    repository = FooRepository(session_factory=session_factory)

    assert await repository.get_by_name("alpha") is None


# only where the port declares a paged, sorted list
async def test_list_respects_pagination_and_sort(session_factory: async_sessionmaker[AsyncSession]) -> None:
    repository = FooRepository(session_factory=session_factory)
    await repository.create(_foo(name="c"))
    await repository.create(_foo(name="a"))
    await repository.create(_foo(name="b"))

    page = await repository.list(filter=FooListFilter(sort=FooSort.NAME_ASC, limit=2, offset=0))
    assert [foo.name for foo in page] == ["a", "b"]


# only where the port declares a paged, sorted list
async def test_count_applies_the_filter(session_factory: async_sessionmaker[AsyncSession]) -> None:
    repository = FooRepository(session_factory=session_factory)
    await repository.create(_foo(name="a"))
    await repository.create(_foo(name="b"))

    assert await repository.count(filter=FooListFilter(name="a")) == 1
```

**Compare every field, never the entity.** An entity's equality is by id (`hex-domain-model`), so
`loaded == foo` passes a repository that maps the id and drops or swaps every other column;
`asdict(...)` on both sides compares what the row actually carried back. The builder gives every
optional field a non-default value, and the update test changes every field `update` writes; otherwise
a column the mapping drops comes back as its default and the comparison passes.

The planting `UPDATE` is not seed data (rule 9): no repository method can set the column, which is the
point.

**Seed 3, page 2.** The page size must be *smaller* than the seeded set or the test proves nothing: at
`limit=3` the page holds every row, so the same assertion passes a repository that ignores the bound
entirely. 3 and 2 are the smallest pair that fails on a missing `LIMIT` and, because the rows are seeded
out of order (`c`, `a`, `b`) and asserted in order, on a missing `ORDER BY` as well.

### `test_migration_round_trip.py` — every revision undoes and redoes

```python
import subprocess
from collections.abc import Callable


def test_migrations_round_trip(
    run_alembic: Callable[..., subprocess.CompletedProcess[str]],
) -> None:
    down = run_alembic("downgrade", "base")
    assert down.returncode == 0, down.stderr

    up = run_alembic("upgrade", "head")
    assert up.returncode == 0, up.stderr
```

The session starts at head, so this is head → base → head against the real database: a `downgrade()`
that fails, or leaves behind an object the next `upgrade()` trips over, reds here. It ends at head, so
the tests that assume head still find it; a suite run in parallel gives it a database of its own.

### Cascade — an owned child collection

For an aggregate that owns a child collection in a table that cascades from its own, rule 7's test
creates the parent, adds a child through the repository, deletes the parent and asserts through the
repository that the parent's child count is zero; a child looked up under the wrong parent raises the
not-found exception. An aggregate with no owned children has neither test.

### Client-style store — redis-py

```
tests/integration/
├── conftest.py                         # + redis_url (session), redis_client (per test, emptied after)
│                                       #   — hex-test-integration-setup's
└── redis/
    └── test_baz_repository.py
```

A client store gives the test an **SDK client** and a **namespace** the test owns. Redis is the worked
binding — `hex-store-repository`'s own — whose adapter fixes its key prefix in code, so the namespace
a test owns is the suite's own container, emptied after each test. The
adapter is `hex-store-repository`'s `BazRepository`, whose `IBazRepository` declares three verbs, so the
contract is those three (rule 1): create, fetch by id and delete, each with its absent-record case, plus
the translation of a store failure on a read and a write.

The fixtures — the Redis container for the run (`redis_url`) and the per-test client whose teardown
empties it (`redis_client`) — are `hex-test-integration-setup`'s, in its `CONFTEST.md`: the client sits
up-tree beside the session half because `container` binds it too. This skill writes only the test
module below.

### `test_baz_repository.py`

```python
import uuid
from dataclasses import asdict

import pytest
from redis.asyncio import Redis

from myapp.domain.bazs import Baz
from myapp.domain.exceptions import NotFoundError, UpstreamError
from myapp.infrastructure.redis.repositories import BazRepository


def _baz(*, name: str = "alpha") -> Baz:
    return Baz(id=uuid.uuid4(), name=name)


async def test_create_then_get_returns_every_field(redis_client: Redis) -> None:
    repository = BazRepository(client=redis_client)
    baz = _baz()

    await repository.create(baz)

    assert asdict(await repository.get_by_id(baz.id)) == asdict(baz)


async def test_create_writes_under_the_documented_key(redis_client: Redis) -> None:
    repository = BazRepository(client=redis_client)
    baz = _baz()

    await repository.create(baz)

    assert await redis_client.exists(f"bazs:{baz.id}") == 1


async def test_get_by_id_of_absent_record_raises_not_found(redis_client: Redis) -> None:
    repository = BazRepository(client=redis_client)
    missing = uuid.uuid4()

    with pytest.raises(NotFoundError) as exc_info:
        await repository.get_by_id(missing)

    assert exc_info.value.context["id"] == str(missing)


async def test_delete_removes_the_record(redis_client: Redis) -> None:
    repository = BazRepository(client=redis_client)
    baz = _baz()
    await repository.create(baz)

    await repository.delete(baz.id)

    with pytest.raises(NotFoundError) as exc_info:
        await repository.get_by_id(baz.id)

    assert exc_info.value.context["id"] == str(baz.id)


async def test_delete_of_absent_record_raises_not_found(redis_client: Redis) -> None:
    repository = BazRepository(client=redis_client)
    missing = uuid.uuid4()

    with pytest.raises(NotFoundError) as exc_info:
        await repository.delete(missing)

    assert exc_info.value.context["id"] == str(missing)


async def test_read_and_write_against_unreachable_store_raise_upstream_error() -> None:
    dead = Redis.from_url("redis://127.0.0.1:1/0")  # nothing listening
    baz = _baz()
    try:
        repository = BazRepository(client=dead)
        with pytest.raises(UpstreamError) as read:
            await repository.get_by_id(baz.id)
        with pytest.raises(UpstreamError) as write:
            await repository.create(baz)
    finally:
        await dead.aclose()

    assert read.value.context["key"] == f"bazs:{baz.id}"
    assert write.value.context["key"] == f"bazs:{baz.id}"
```

The key test reads the raw key through the test's client: an adapter whose key layout drifted would
still round-trip through its own `get_by_id`, and only a read that goes around it proves where the
record landed — which is what every record already stored depends on.

## Other bindings

- **A pre-provisioned database instead of a disposable container.** Provisioning is
  `hex-test-integration-setup`'s (`## Other bindings`); every rule below is unchanged.
- **An in-process engine (SQLite) for speed.** The rollback shape survives; the contract does not.
  Constraint names, cascade semantics and the error the driver raises all differ, so rules 4, 5 and 7 —
  the assertions this layer exists for — would be pinning a database the service never runs on. A smoke
  suite, never the repository contract.
- **Another engine or driver.** The constraint names, the error code and the attribute the adapter's
  translator reads off it change together (`hex-persistence`); what the test must cover — insert *and*
  update on every unique field, one test per cascade, found and not-found per lookup — does not.
- **Another client store** — a document store, a wide-column store, or an index kept beside the
  authoritative store. The SDK client, its testcontainer and the namespace token change (a collection,
  an index, a database); the session/per-test split, the per-test namespace with teardown, the
  round-trip, ordering and translation assertions do not. Where no testcontainers module exists for the store, a pinned
  `DockerContainer` with an explicit wait strategy is the same fixture.

## Rules

Follow `test-principles` for the testing constitution. Follow `naming` for names and `exception-catalog` for the error catalogue and boundary translation.

### Both halves

1. **Exercise exactly the protocol the port declares** — every method, CRUD verbs and the port's own
   alike (`delete_by_<field>`, range/scan), each with its absent-record case, and no test for a method
   the port does not declare. A verb that promises an order asserts that order, not just membership. An
   out-of-order write and a batch write, where the adapter takes them → `test-principles`,
   *Datastore contract* rules 6 and 7.

### Relational

2. **Every test takes the rollback-scoped handle the integration setup provides — `session_factory` under this binding (`hex-test-integration-setup`) — and opens nothing of its own** (`test-principles` reliability rule 6). The one exception is a handle to a store nothing listens on, which writes nothing (rule 4's forced error).
3. Follow `test-principles` for the `_<aggregate>()` builder form. Defaults must be valid; no-override construction succeeds.
4. Every conflict pins its constraint's name on the translated exception → `test-principles`, *Datastore contract* rule 2; here `assert exc_info.value.context["constraint"] == "<constraint_name>"` on the `ConflictError` subclass the translator raises for it (`FooConflictError` for `uq_foos_name`). A forced driver error on a write and a read → *Datastore contract* rule 4.
5. Insert and update paths for every unique field → `test-principles`, *Datastore contract* rule 3. Where
   a create a delivered unit drives does nothing on a conflict on `id` (`hex-persistence`
   `REPOSITORY.md` rule 8), `test_create_with_an_existing_id_changes_nothing` creates a second entity
   sharing the first's id and differing in every other field, and asserts no raise and the stored row
   keeps the first's values, beside the natural-key conflict that still raises.
6. **The update timestamp is not an entity field** (`hex-domain-model`, Entity rule 6), so it is read from the row through the test's own session handle, against a value planted before the act → `test-principles` reliability rule 4.
7. **Every cascade gets its own test**, `test_cascade_delete_removes_<child>` (`test-principles`, *Test naming*). Test the count after parent-delete is zero — only this proves the schema's `ON DELETE CASCADE` works.
8. **Every `get_by_<field>` gets both a found and a not-found test.**
9. Seed data on the table under test goes through the repository's own `create`, never a raw INSERT, and a row `Foo` only references is seeded raw → `test-principles`, *Datastore contract* rule 5; the ban binds only a test of the repository under test.
10. **No web framework, no HTTP client, no DI container in this file.** The test imports the repository class, takes the session factory, calls methods and asserts. Reaching the adapter through a route tests the route as well, and a failure no longer says which of the two is broken; the HTTP surface is `hex-test-restapi-endpoint`'s.
11. **A test that moves the schema takes the migration runner (`run_alembic`, `hex-test-integration-setup`), never the fixture that assumes head**, and lives in its own flat file (`tests/integration/postgres/test_<NNNN>_migration.py`); a downgrade underneath an ordinary repository test takes the rest of its file with it. The round trip `persistence` rule 20 requires is one of those files, always present.
12. **Where the store has a unit of work, its implementation gets one test over `session_factory`**: an exception inside the block leaves nothing from any member, read back through a fresh session; the session-injected form is tested through the unit of work, never with a hand-opened session.

### Client-style store

13. Each test runs against the real store, never a fake or a mock → `test-principles`, *Datastore contract* rule 1; as in the relational half, the file holds no web framework, HTTP client or DI container (rule 10).
14. **Isolate by a per-test namespace, not rollback** (`test-principles` reliability rule 2) — the suite's own container emptied after each test (`redis_client`'s teardown) where the adapter fixes its namespace in code. There is no transaction to roll back, so no `session_factory` here.
15. **The container is session-scoped; the namespace is function-scoped** — `test-principles`, *Fixture scope rules*. A store the environment supplies instead is opted into as `test-principles` reliability rules 1 and 6 state.
16. **Assert the entity↔record mapping round-trips.** What was written comes back as the same entity — every field the record carries, compared field by field, since entity equality is by id. A compound return asserts every element it carries, not just the entity.
17. A forced store failure is asserted on the catalogue's upstream class and the `context` the adapter sets — a write and a read (`test-principles`, *Datastore contract* rule 4) — and an absent record on the not-found class (`exception-catalog`); a store with no constraints has no rule-4 constraint pin.
18. **Assert where the record landed.** The key layout is the adapter's persisted contract (its key prefix is a module constant, `hex-store-repository` rule 5), and an adapter that changes it still round-trips through its own reads; one test reads the raw record through the client, under the key the adapter documents, to prove the layout is the one used.

## Inlined typing / import rules

- No `myapp.application.*`, no `myapp.restapi.*`.
- Full annotations on every test signature including `session_factory: async_sessionmaker[AsyncSession]`.
- Builder `_<aggregate>()` returns the entity type; overrides keyword-only.
- No `from __future__ import annotations`.

Where a client-store test needs the client and a settings object both, they arrive as two fixtures, each
annotated with its own type — never a bare tuple (`python-style`) — and a yielding fixture uses
`AsyncIterator[T]` / `Iterator[T]`.

## Hard stops

- A relational test and nothing up-tree provides a session handle whose writes are discarded when the test ends (`session_factory` under this catalogue's binding), or a client-store test and nothing up-tree provides the store client emptied per test → stop, use `hex-test-integration-setup`; what is missing is the isolation guarantee, not a fixture name.
- A test references FastAPI, `httpx2` or the DI container → stop, use `hex-test-restapi-endpoint`.
- Asked to mock the store SDK or assert against a fake → stop, use `hex-test-application-handler` at the handler-unit layer; this layer drives the real backend.
