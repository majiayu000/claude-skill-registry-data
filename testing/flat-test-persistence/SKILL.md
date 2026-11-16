---
name: flat-test-persistence
description: Use when testing a flat-layered service's data-access package against the real datastore — its tables and the repository class that owns its transactions — pinning the generated constraint name where the translator branches on it, the catalogue exception a driver error is translated into on each write and read the class has, what each read returns, and each write's conditional contract where it has one — an upsert's update set from both sides, an ordering-stamp guard where writes for one key can arrive out of order, an empty update set, a batch's chunk edge and same-key inputs, a paged read's tied edge, a multi-statement write's atomicity. Consumes the container and isolation fixtures rather than laying them (`flat-test-integration-setup`). Not the function a trigger calls that reaches this write path, which is `flat-test-entrypoint`, and not a hexagonal `IFooRepository` adapter, which is `hex-test-repository-contract`, in the `pyhouse-hex` plugin.
---

# Flat Test — Data-Access Contract

Consult `test-principles` for the testing constitution. Where this skill contradicts `test-principles`,
the constitution wins.

One integration-test file per repository class, under the distribution's own `tests/integration/`,
driven against the **real** datastore from `flat-test-integration-setup`. This is the only level that
can catch what the data-access package exists to guarantee: that a conflict updates the columns it
claims to, that a read returns what the store holds, and that a driver error arrives as the service's own
exception.

Where several distributions share one data-access library, the files sit with that library's own tests
instead — `myschema/tests/integration/` — and nothing else changes.

**The isolation fixture follows the declared transaction owner** (`test-principles` reliability
rule 2): `connection` for every assertion query and for a callable that accepts a connection; the `engine`
fixture handed to the repository class's constructor, with `truncate_all` cleaning up, for one that
opens its own — asserting through a fresh connection only where its own rollback is under test
(rule 10).

## When to use vs. neighbours

- A pure function in the data-access package — a connection-string builder, the row mapper → not this
  skill; it is a unit test with no fixtures at all.
- The container, migration and isolation fixtures themselves → `flat-test-integration-setup`; this skill
  consumes `connection`, `engine` and `truncate_all` and lays none of its own.
- Writing the tables, repository class and migrations under test → `flat-persistence`.
- The work a trigger calls reaching this write path as part of a run → `flat-test-entrypoint`; this skill tests
  the write path, that one tests the wiring above it.
- The client feeding these rows → `flat-test-service-client`.
- A static "no package outside the data-access package constructs a statement" rule →
  `test-architecture-rule`.
- The shared groundwork — fixture placement, assertion strength, reliability → `test-principles`.
- The adapter sits behind a domain repository protocol → `hex-test-repository-contract`, in the
  `pyhouse-hex` plugin.

## Template — the repository class's contract (pytest, SQLAlchemy async over Postgres)

`tests/integration/test_foo_repository.py`:

```python
from uuid import UUID

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncEngine

from myapp.exceptions import StorageWriteRejectedError
from myapp.postgres import FooRepository
from myapp.postgres.foo_table import foo_table
from myapp.schemas import Foo, FooExternalId


def _a_foo(external_id: str = "alpha", name: str = "first") -> Foo:
    return Foo(external_id=FooExternalId(external_id), name=name)


# only where a write updates on conflict
async def test_a_second_write_of_one_external_id_updates_the_set_and_keeps_the_rest(
    engine: AsyncEngine,
    connection: AsyncConnection,
) -> None:
    repository = FooRepository(engine)
    await repository.upsert(_a_foo(name="first"))
    first_id: UUID = (await connection.execute(select(foo_table.c.id))).scalar_one()

    await repository.upsert(_a_foo(name="second"))

    rows = (await connection.execute(select(foo_table.c.id, foo_table.c.name))).all()
    assert [tuple(row) for row in rows] == [(first_id, "second")]


async def test_a_value_the_store_refuses_arrives_as_the_catalogue_error(engine: AsyncEngine) -> None:
    with pytest.raises(StorageWriteRejectedError) as exc_info:
        await FooRepository(engine).upsert(_a_foo(name="nul\x00"))

    assert exc_info.value.context == {"sqlstate": "22021", "constraint": None}
```

The tests drive the class a caller uses and assert through `connection`, a query against the store.

The first test pins the declared update set from both sides in one comparison: one row, not two; the
name the set covers changed; the id it does not cover kept the value the first write minted.

The translation test forces the write through the public method a caller uses, refused by the store
itself — a NUL character, which a Postgres text value cannot hold, is SQLSTATE `22021` in the
data-exception class — so no constraint had to be invented for the test.

Where a write resolves a conflict by doing nothing, the file gains the no-op test of rule 5; where it
spans statements, the atomicity test of rule 10; where a method takes a batch, the two tests of rule 6;
where writes for one key can arrive out of order, the test of rule 13; and a test of what each read
returns, rule 14, wherever the class reads.

## Other bindings

- **The ORM in place of Core.** Mapped classes replace the table objects and the session replaces the
  connection; every rule below is unchanged, because each pins a property of the stored data rather than
  of the statement that wrote it. Assertions still read the store back (rule 1) — through a fresh query,
  not through the session's identity map, which can hand back the object just written without it ever
  having reached the datastore.
- **Another engine or dialect.** The upsert spelling, the generated constraint names and the driver
  errors a violation raises change together; the contract questions — idempotence, the update set from
  both sides, the translated exception — do not. Where the dialect has no single-statement upsert, the
  repository's *contract* is still the subject and the test pins whatever its write does instead.
- **How the datastore is provisioned** — a disposable container, a pre-provisioned throwaway database, an
  in-process engine. That choice belongs to `flat-test-integration-setup`, which names its trade-offs;
  nothing in these files changes with it except that an in-process engine of a different dialect
  invalidates rules 2 and 3.

## Rules

1. **This level runs against the real store, substitutes nothing below the repository class, and
   asserts through a query against the store** — `test-principles`, *Datastore contract* rule 1.
2. **Where the translator branches on a constraint's name, pin that name** — `test-principles`,
   *Datastore contract* rule 2.
3. **A unique constraint the translator branches on is tested on the plain insert *and*, where the
   class has one, on the conflict-resolution path** — `test-principles`, *Datastore contract* rule 3.
4. **Where a write updates on conflict, test its declared update set from both sides.** The second write must change what the set names
   *and* leave every column outside it alone — that is the whole contract of an upsert, and both are
   pinned, whether in one comparison or two.
5. **An empty update set means "do nothing on conflict".** Where a write declares one, test it as a
   no-op that raises nothing and changes nothing; a write that meets a key already recorded and must
   leave it alone relies on exactly that.
6. **Where a method takes a batch, it carries the two tests `test-principles`, *Datastore contract*
   rule 7, states** — a chunk edge crossed and two inputs sharing one key in one call.
7. **A forced driver error asserts the catalogue exception the data-access package produces, on each
   write and read the class has** — `test-principles`, *Datastore contract* rule 4. A read
   with no input the store can refuse takes reliability rule 6's one exception.
8. **Where the store assigns a timestamp, assert it as `test-principles` reliability rule 4 states.**
9. **Ordering is asserted only where the query guarantees it.** Add an explicit order clause to any
   query whose result is compared to a list; a relational store promises no insertion order, and a test
   that passes on two rows fails on two hundred.
10. **Where one write spans statements, it has an atomicity test** that forces its last statement to fail
    through a constraint the schema declares, expects the narrowest catalogue exception that constraint
    produces, and asserts through a fresh connection that the earlier statements left nothing behind —
    never through `connection`, whose own transaction cannot observe another connection's rollback. Without it
    a refactor splitting the statements into two transactions passes every test.
11. **Where a run walks a table in pages, a test crosses a page edge where the ordering column ties.**
12. **A test arranges every row it asserts on as `test-principles` *Datastore contract* rule 5 states** —
    the service's declared type written through the repository class, or through the schema's own table
    object where the class has no write for it — and, where the subject opens its own connection,
    committed before it runs (`flat-test-integration-setup`).
13. **Where writes for one key can arrive out of order, the test `test-principles`, *Datastore contract*
    rule 6, states**; the update-set test's second write then carries the newer stamp, so it holds with
    the guard.
14. **Each read the class has is tested on what it returns** — `test-principles`, *Datastore contract*
    rule 9 — its rows arranged as rule 12 states.

## Hard stops

- The constraint under test does not exist in a migration yet → stop, add the revision first
  (`flat-persistence`); a test asserting a constraint the schema never had passes for the wrong reason.
- The adapter sits behind a domain repository protocol → stop, use `hex-test-repository-contract`, in
  the `pyhouse-hex` plugin.
