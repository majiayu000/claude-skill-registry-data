---
name: hex-test-application-handler
description: Use when unit-testing a CQRS command or query handler against in-memory fakes, or when writing one of those fakes — this skill owns `tests/unit/fakes/`, so a request for a fake repository or a fake `ICan<Verb>` capability lands here rather than on either adapter-test skill. Also covers failure injection through an inline `_RaiseXxxRepository` subclass, and the test that a failed side effect after the store write leaves the command succeeded. Not the real adapter against a real backend (`hex-test-repository-contract`, `hex-test-capability-adapter`) nor the handler over HTTP (`hex-test-restapi-endpoint`).
---

# Hex Test — Application Handler (unit)

Consult `test-principles` for the testing constitution. Where this skill contradicts `test-principles`, the constitution wins.

Produces one unit-test file per handler module. Runs in milliseconds against in-memory fakes. Coverage targets the happy path plus every domain exception the handler propagates and — for compensating-transaction handlers — the post-failure undo, and, where a side effect follows the store write, a failed effect that leaves the command succeeded.

## When to use vs. neighbours

- A new or modified handler under `application/<subdomain>/`, or a fake it needs under `tests/unit/fakes/` → this skill (write the fake first).
- A fake for a capability port (`ICan<Verb>`) as much as for a repository (`IFooRepository`) → this skill; it owns both, which is why a bare "write me a fake" lands here and not on an adapter-test skill.
- One-off failure injection for a single handler test → this skill — declare a `_RaiseXxxRepository(FakeFooRepository)` subclass at the handler test module scope instead of extending the fake.
- A test that drives the handler through the HTTP surface → `hex-test-restapi-endpoint` (integration, not unit); as an authenticated caller → `hex-test-restapi-auth`.
- A test for a domain entity, value object, enum or service → `hex-test-domain`.
- A real-backend test of the repository the fake stands in for → `hex-test-repository-contract`; of a capability adapter → `hex-test-capability-adapter`. The fake's exception contract is copied verbatim from whichever of those pins it.
- The real adapter itself → `hex-persistence` (relational), `hex-store-repository` (client store) or `hex-capability-adapter`.
- The domain protocol the fake matches → `hex-domain-ports`; the handler under test → `hex-application`.
- Any container, engine or session fixture — this layer has none and needs none → `hex-test-integration-setup`.
- The substitution ladder that permits a fake at all, and the no-mocks rule → `test-principles`.

## Template(s) — pytest, hand-written in-memory fakes

### Handler unit-test file location

```
tests/unit/application/
└── test_<verb>_<noun>_handler.py        # mirrors the handler module's filename
```

One file per handler. Compensating-transaction assertions live in the file for the handler that performs the compensation, not in a separate file.

### `create` handler

```python
import pytest  # only where Foo has a natural key

from myapp.application.foos import CreateFooCommand, CreateFooHandler
from myapp.domain.exceptions import FooConflictError  # only where Foo has a natural key
from tests.unit.fakes import FakeFooRepository


async def test_assigns_uuid_and_stores() -> None:
    repository = FakeFooRepository()
    handler = CreateFooHandler(repository=repository)

    foo_id = await handler.execute(CreateFooCommand(name="alpha"))

    stored = await repository.get_by_id(foo_id)
    assert stored.name == "alpha"
    assert stored.id == foo_id


# only where Foo has a natural key
async def test_duplicate_name_raises_conflict() -> None:
    repository = FakeFooRepository()
    handler = CreateFooHandler(repository=repository)
    await handler.execute(CreateFooCommand(name="alpha"))

    with pytest.raises(FooConflictError) as exc_info:
        await handler.execute(CreateFooCommand(name="alpha"))

    assert exc_info.value.context["constraint"] == "uq_foos_name"  # only with a relational adapter
```

### `update` handler — partial update, an absent field left as it was

```python
import uuid

import pytest

from myapp.application.foos import UpdateFooCommand, UpdateFooHandler
from myapp.domain.exceptions import NotFoundError
from myapp.domain.foos import Foo
from tests.unit.fakes import FakeFooRepository


async def test_partial_update_leaves_unspecified_fields_untouched() -> None:
    foo_id = uuid.uuid4()
    repository = FakeFooRepository(items=[Foo(id=foo_id, name="alpha", note="kept")])

    await UpdateFooHandler(repository=repository).execute(UpdateFooCommand(id=foo_id, name="beta"))

    stored = await repository.get_by_id(foo_id)
    assert stored.name == "beta"
    assert stored.note == "kept"  # not given on the command, so left as it was
    assert repository.updated == [foo_id]


async def test_update_unknown_id_raises_not_found() -> None:
    handler = UpdateFooHandler(repository=FakeFooRepository())
    missing = uuid.uuid4()

    with pytest.raises(NotFoundError) as exc_info:
        await handler.execute(UpdateFooCommand(id=missing, name="beta"))

    assert exc_info.value.context["id"] == str(missing)
```

### One-off failure injection

Only where another aggregate references `Foo` without a cascade, the delete handler's in-use case is
driven by a module-scope `_RaiseInUseFooRepository(FakeFooRepository)` overriding `delete` alone (rule 6) and
raising the class, message and `context` the real adapter's delete raises for that reference — a
relational adapter's includes the FK constraint name (Fakes rule 6); the test asserts it propagates
unchanged.

### `list` query handler — sort + pagination

```python
import uuid

from myapp.application.foos import ListFoosHandler, ListFoosQuery
from myapp.domain.foos import Foo, FooListFilter, FooSort
from tests.unit.fakes import FakeFooRepository


async def test_sorted_by_name() -> None:
    repository = FakeFooRepository(
        items=[
            Foo(id=uuid.uuid4(), name="b"),
            Foo(id=uuid.uuid4(), name="c"),
            Foo(id=uuid.uuid4(), name="a"),
        ]
    )
    handler = ListFoosHandler(repository=repository)

    result = await handler.execute(
        ListFoosQuery(filter=FooListFilter(sort=FooSort.NAME_ASC, limit=2)),
    )

    assert [foo.name for foo in result.items] == ["a", "b"]
    assert result.total == 3
```

**Seed 3, page 2 — the page size is smaller than the seeded set on purpose.** At `limit=10` over
three rows the page holds every match, so the same asserts pass a handler that never applies the
bound and one that returns `len(items)` as `total`. 3 and 2 are the smallest pair that reds both.
Each field the filter narrows by gets one more test that seeds a row the filter excludes and asserts it
is absent from both `items` and `total` — which is also what proves the fake honours the filter (Fakes
rule 5).

### `compensating-transaction` handler

Where a handler undoes an external write when a later step fails (`hex-application`, Compensation), its tests live in
that handler's file and drive it over the external write's call record. The template — two tests, the
undo and a failed undo — sits beside the storage fake in `FAKES.md`.

## Fake repository and capability templates

Produces one in-memory stand-in class for a domain protocol. Handler unit tests under `tests/unit/application/` use this fake instead of the real `infrastructure/` adapter. The fake satisfies the protocol **structurally** — no `(IFooRepository)` inheritance, no `@runtime_checkable` registration.

### File location and naming

```
tests/unit/fakes/
├── __init__.py                                 # re-exports every fake (python-packaging)
└── fake_<aggregate_snake>_repository.py        # class FakeFooRepository
```

For capabilities the fake takes the name the real adapter takes after its technology prefix
(`hex-conventions`): the capability's role noun when it has one — `FakeFooStorage` for `ICanStoreFoos`
— and otherwise the protocol name minus `ICan`. The module is the class name snaked:
`fake_foo_storage.py`.

`tests/unit/fakes/` is a package like any other: each fake module declares `__all__`, the package
`__init__.py` re-exports them under `python-packaging`'s contract, and handler tests import from the
package:

```python
from tests.unit.fakes import FakeFooRepository
```

Living under `tests/` is what keeps fakes out of production import graphs; the re-export only spares
each test from knowing the file layout. `tests.unit.fakes` resolves against the
distribution's own root — in a single distribution, through `python-toolchain`'s
`[tool.pytest.ini_options]` block; in a workspace, `python-workspace`.

**Read `FAKES.md`** in this skill's directory before writing or extending a fake under
`tests/unit/fakes/` — the CRUD repository fake and the test that pins its copy contract; its storage and
compensation sections only where a handler compensates (`hex-application`, Compensation). Only
`SKILL.md` is loaded automatically.

## Rules

Consult `test-principles` for the testing constitution, `naming` for names, `python-style` for typing and comments, `python-logging` for logging, `python-packaging` for packaging and imports, and `exception-catalog` for the error catalogue and boundary translation.

### Handler tests

1. **Where the command carries `caller_id`, add a module-level `_CALLER`** — the issuer's opaque subject, a `str` — and pass `caller_id=_CALLER` in every construction. The templates carry none: a command has `caller_id` only where its entrypoint authenticates the caller (`hex-application`).
2. **AAA structure follows `test-principles`.** Arrange — construct fake(s) and handler. Act — call `handler.execute(...)`. Assert — read state back through the fake or assert raised exception.
3. **Read state back via fake's domain methods** (`await repository.get_by_id(...)`), not via attribute peeking on `repository._store`.
4. **A failure case pins the exception's context** (`test-principles` *Assert strength* recipe 6); the fake carries the real adapter's (Fakes rule 6), so asserting the class alone passes a fake with the wrong payload.
5. **Compensation tests assert call-record state**, not implementation details. For a storage capability, `storage.uploads` and `storage.deletes` are the observation surface. Assert the right key was undone, in the right order, for the right reason — but never assert that a specific Python call site invoked them.
6. **One-off failure injection is `test-principles` rung 4 with the fake as its base** — an inline `_RaiseXxxRepository(FakeFooRepository)` at module scope overriding exactly the method under test, never re-stubbing the whole protocol.
7. **A concrete domain-service dependency is the real service built on the fakes of its ports**; a module-scope subclass overriding one method (`test-principles` rung 4) only injects a failure the fakes cannot produce — never a protocol extracted for the test, a `# type: ignore` or a mock.
8. **A handler test's stand-in is a fake from `tests/unit/fakes/`; where the one it needs does not exist, write it there first.** Never improvise a stand-in at the test site, reach for a mock, or weaken the assertion so it is not needed — the fake's value is that its exception contract matches the real adapter's, and an improvised stub silently does not.

### Assert strength on a handler over fakes

The recipes that hold for any test — assert a survivor rather than an empty result, seed a second row where one cannot prove scoping, pick a non-constant input for an echoed field, assert no side effect on a reject path, exercise a non-boundary case as well as the boundary, and expect the narrowest class on a raise path — are `test-principles`'. One is specific to a handler driven through in-memory fakes:

- **Pin PERSISTED state, not the in-memory entity.** Assert the write happened via the fake's `updated` call-record (`assert repository.updated == [id]`) AND read the value back (`(await repository.get_by_id(id)).name == "beta"`). The fake returns a COPY and records updates (the `Fakes` rules below), so a body that mutates the entity but never calls `update()` **reds**. Asserting on the entity object the handler mutated in place pins nothing (it observes the in-memory mutation, not the persist).

### Coverage checklist (one `test_*` per case — `test-principles` owns when not to parametrize)

#### `create` handler

- `test_assigns_uuid_and_stores` — handler returns a `UUID`; `get_by_id` returns the entity with expected fields and that same id.
- `test_duplicate_<unique_field>_raises_conflict` — for every uniqueness constraint enforced by the repository, assert the repository's conflict class (`FooConflictError`) on the second attempt with `exc_info.value.context["constraint"] == "<full_constraint_name>"` where the adapter is relational.
- Field normalization (when applicable): assert the stored entity has the normalized form (`strip`, `upper`), not the raw input.

#### `create` handler a delivered unit drives

Only where a consumer or another inbound adapter calls the handler with a unit delivered at least once
(`at-least-once-delivery`, rule 3; `hex-architecture`'s consumer line) — there the command carries the
id (`hex-application` command handler rule 6), so `test_assigns_uuid_and_stores` becomes
`test_stores_under_the_commands_id`, asserting the returned and stored id equal the command's:

- `test_a_redelivered_create_changes_nothing` — handle the same command, carrying the unit's id, twice;
  assert both calls return the unit's id, the second raises nothing, and `get_by_id(<the unit's id>)`
  returns the entity the first wrote. The fake resolves a conflict on its own id as the real adapter
  does (Fakes rule 6), so a fake that raises there, or a handler that mints its own id, reds.
- The inbound adapter's own obligation — the unit acknowledged once the handler returns, returned
  unacknowledged when it raises — is tested where the project tests that adapter, through the
  adapter's function that handles one unit, never here (`at-least-once-delivery` rule 1;
  `flat-test-entrypoint` rule 6, in the `pyhouse-flat` plugin, is an example).

#### `update` handler

- `test_partial_update_leaves_unspecified_fields_untouched` — set one field and leave another out; assert the one left out is **unchanged** and the one set is updated. This is the partial-update contract.
- `test_update_unknown_id_raises_not_found`.
- `test_update_duplicate_<unique_field>_raises_conflict` — renaming row B to row A's name raises `FooConflictError` — only where Foo has a natural key.

#### `delete` handler

- `test_delete_removes` — happy path; `get_by_id` after delete raises `NotFoundError`.
- `test_delete_unknown_id_raises_not_found`.
- `test_delete_<resource>_in_use_propagates` — only where another aggregate references this one without a cascade. An inline `_RaiseInUseFooRepository` raises the class, message and `context` the real adapter's delete raises for that reference (a relational adapter's includes the FK constraint name); assert it propagates unchanged.

#### `get` / single-read query handler

- `test_returns_entity_when_present` — load the fake with one entity; the handler returns it intact.
- `test_returns_none_or_raises_when_absent` — match the handler's contract (`Entity | None` returns `None`; `Entity` returns raises `NotFoundError`).

#### `list` query handler

- `test_sorted_by_<order_key>` — load the fake with deliberately unsorted entities (vary both primary and secondary sort keys); assert the order of `result.items` is exactly the expected sequence.
- `test_pagination_offset_limit` — load N > limit entities; call with `limit=L, offset=O`; assert `len(result.items) == L` and `result.total == N`.

#### `compensating-transaction` handler

- `test_store_failure_undoes_the_<external_write>` — the store write raises the catalogue exception its real adapter raises; assert the external write's call record shows each write that landed before the failure undone, and the caller receives that same failure.
- `test_failed_undo_still_raises_the_original_failure` — the undo raises too; assert the original failure propagates, not the undo's, and the undo was still attempted. Both injected failures are catalogue classes (Fakes rules 6 and 8), so the test tells them apart by which call raised, never by class alone.

#### handler with a side effect after the store write

- `test_<effect>_failure_leaves_the_<command>_succeeded` — only where the handler runs a side effect after the store write (`hex-application`, After the store write): an inline subclass, at module scope, of the fake the call after the write reaches — the effect's own, or the hand-off's where the effect is handed to something that retries it — raises the catalogue exception its real adapter raises; assert the handler returns normally (the id, for a create), the write reads back from the repository fake, and the call was attempted, on that fake's call record. The one log line the handler owes is not asserted (Hard prohibitions).
- `test_store_failure_skips_the_<effect>` — same condition: the repository fake's write raises the catalogue exception its real adapter raises; assert that very failure propagates and the effect's call record is empty. A `try` that also covers the write, or an effect sent before it, reds here.

### Hard prohibitions (across all handler-unit tests)

- **No assertions on what the handler logged** — `test-principles` owns the rule; here it bites because a handler that logs the right success event and never calls `update()` would otherwise pass. Assert the returned value and the persisted state. Which layer may log at all → `hex-architecture`.
- Timing and unit-test isolation follow `test-principles`. The whole file should run in well under a second.

### Fakes

1. **No inheritance from the protocol.** Structural matching is verified by the type checker — no `@runtime_checkable` registration, no `isinstance` check.
2. **One state field per collection** — `self._store: dict[UUID, <Entity>]` keyed by id. No secondary indexes, no shadow caches. Queries scan the dict — the data set is tiny.
3. **Constructor takes `items: list[<Entity>] | None = None`** with `or []` fallback so the empty-fake call site is terse: `FakeFooRepository()`.
4. **Every method is `async def`**, even when there's nothing to await — the protocol says async; the fake matches.
5. **`list(*, filter: <FilterRecord>)` is keyword-only** and applies a deterministic sort matching the real repository's `ORDER BY`. Handler tests assert exact order — sort, don't return insertion order.
   - **A fake method MUST honour every filtering / scoping parameter it declares — never ignore one.** If the filter declares `name`, a status set or a parent id, the fake filters `_store` by it. A fake that accepts a parameter and ignores it makes that contract **uncatchable** — the assert for it can never be strong. The fake's filtering need not be efficient, just correct: a wrong body that ignores the same parameter must produce a different result against the fake.
6. **The exception contract is copied verbatim from the real adapter.** Copy the class, message and `context` keys the real adapter sets — for a relational adapter that includes the constraint name — and no more. Where the aggregate has a natural key, the relational adapter (`hex-persistence`) raises `FooConflictError("foo name already exists", {"field": "name", "constraint": "uq_foos_name"})` — context carries `field` and `constraint` and nothing else, so the fake matches it exactly. Adding a key the real adapter never sets (e.g. `"value"`) is the silent drift this rule exists to prevent: a handler test asserting that key passes against the fake and fails against the real adapter. Where a create a delivered unit drives resolves a conflict on its own id as nothing to do (`hex-persistence` `REPOSITORY.md` rule 8), the fake's `create` returns without effect when the id is already stored, checked before any natural key, as the real adapter's insert does.
7. **Cascades match the schema.** When the real schema has `ON DELETE CASCADE`, the fake removes the dependent rows: it holds the owned children in a second dict keyed by id, and its `delete` drops every child whose parent id matches before dropping the parent. Skipping the cascade in the fake produces a green unit test that a failing integration test then catches — defeats the point.
8. **Default-happy-path only.** No `fail_next_create=True` flags or `_should_raise` knobs, and no failure the default fake cannot know about — an in-use rejection needs a cross-aggregate reference the in-memory fake does not model. A one-off failure is an inline subclass at the handler test's module scope (handler rule 6):

```python
class _RaiseUpstreamFooRepository(FakeFooRepository):
    async def create(self, foo: Foo) -> None:
        raise UpstreamError("the datastore could not complete the operation", {"id": str(foo.id)})
```

Call records — `updated`, a capability fake's call list, a storage fake's `uploads` / `deletes` — observe; they never inject failure.

9. **Never hand back the object the caller passed in — copy on write and on read, and record every `update()`.** The real repository round-trips through the database: a mutation is persisted **only** by an explicit `update()`, and a later read returns the persisted row, not the caller's object. A fake that stores and returns the same instance aliases it, so a handler that mutates the entity **in place and never calls `update()`** still sees its change on the next read — the mutate-but-never-persist bug passes green and no persistence assertion can pin it. So copy on write (`self._store[id] = replace(foo)`) and on read (`return replace(self._store[id])`) — a shallow copy via `dataclasses.replace`, deep only when a field is itself mutable and the test mutates through it — and keep an `updated: list[UUID]` call record.
10. **A handler that takes a unit of work is tested with a fake unit of work** that hands out the fake repositories and records whether it committed. Writes made through it are visible *outside* the unit of work only on commit — inside it, reads see its own writes, as the real session does — and leaving the block without a commit discards them. The test asserts that the writes read back from outside the unit of work only once it has committed, and that an exception raised inside the block leaves nothing committed — a fake whose repositories write straight through passes a handler that never commits, or commits half its writes before failing.
11. **The fake declares exactly the methods its port declares**; a narrower port gets a narrower fake, and the list, count and conflict branches go with the methods that need them.

### What a fake must not do

- **No production imports beyond `myapp.domain`.** Fakes import domain entities, value objects, enums, and exceptions. Never `myapp.infrastructure`, `myapp.application`, `myapp.restapi`.
- **No IO** — apply `test-principles` for isolation and determinism.
- **No third-party imports** other than what stdlib + `myapp.domain` + `pytest` require.
- **No state retained across instances.** No class variables, no module-level caches. Each `FakeFooRepository()` constructs a fresh `_store`.
- Packaging follows `python-packaging` and the fake-specific inlined import rules below.

## Inlined typing / import rules

- Fakes import the standard library and `myapp.domain.*` only; handler tests add `pytest`, `myapp.application.*` and `tests.unit.fakes`, and never `myapp.infrastructure.*` or `myapp.restapi.*`. Each fake module declares `__all__` and `tests/unit/fakes/__init__.py` re-exports it (`python-packaging`); tests import from the package.
- `X | None`, full annotations on every fake method, builder and inline subclass.
- No `from __future__ import annotations`.

## Hard stops

- A handler test needs a real database → stop, use `hex-test-repository-contract` (or `hex-test-capability-adapter` for a capability); needs the HTTP surface — it constructs the app or imports `myapp.restapi.*` → stop, use `hex-test-restapi-endpoint`.
- The real adapter's exception contract cannot be located → stop, the fake's contract is copied, not invented; pin it first with `hex-test-repository-contract` or `hex-test-capability-adapter`.
