---
name: flat-test-integration-setup
description: Use when laying the shared fixtures a flat-layered service's integration tests rest on — the suite-owned datastore container, the exact-name safety guard any database the suite did not start must pass, the migration round trip, the session-scoped engine every fixture and test shares one event loop with, the rollback-scoped connection for code that accepts one, and the whole-schema wipe for code that opens its own transaction. Lives in the distribution's own `tests/integration/conftest.py`. Testing the data-access package against that datastore is `flat-test-persistence`; a hexagonal package's conftest hierarchy with a per-test dishka container is `hex-test-integration-setup`, in the `pyhouse-hex` plugin. - Also when asked where a flat service's test fixtures live, how integration tests get a real database, why a test suite must never truncate a developer's database, or why a session-scoped engine needs a session-scoped event loop.
---

# Flat-Layered Test — Integration Setup

Consult `test-principles` for the testing constitution. Where this skill contradicts `test-principles`, the constitution wins.

One-shot per distribution. Everything under its `tests/integration/` depends on this file: the datastore
the suite runs against, the migration history replayed onto it, the engine every test shares, and the two
isolation fixtures. **Its home is the distribution's own `tests/integration/conftest.py`.** A distribution
with no relational store takes none of this file.

**Two isolation fixtures, and which one a test uses follows from the declared transaction owner.** Every
callable in the data-access package either *accepts* a live connection and never commits, or *opens and owns*
one for the whole of its work (`persistence` rule 1). That declaration decides the fixture:

- **`connection`** — a rollback-scoped connection, for anything that *accepts* one: a function in the
  data-access package that takes one, and every assertion query. Fast, nothing reaches disk. Never for
  arranging rows that code which opens its own connection will read or write: those rows are
  uncommitted, so that code cannot see them, and a write to the same key waits on their lock until
  teardown. Such rows are written in `async with engine.begin()`, and `truncate_all` removes them.
- **`truncate_all`** — wipes every table after each test, for anything that *opens and owns* its
  transaction: repository classes, the work a trigger calls, and the wrappers above them. A test's outer transaction
  can neither see nor roll back a connection the code under test opened for itself.

## When to use vs. neighbours

- Laying or changing the fixtures themselves → this skill.
- The pytest configuration block that loads them → `python-toolchain`.
- A test of a table or the repository class → `flat-test-persistence`, which consumes both
  `connection` and `truncate_all` and lays none of its own.
- The work a trigger calls, its wrapper or the orchestration above them → `flat-test-entrypoint`; its code
  owns its transactions, so it takes the wipe.
- An external-system client's own test → `flat-test-service-client`; it needs no datastore and must not
  live under `tests/integration/`.
- Row builders → not this skill; they are module-level `def`s in the test file using them.
- What the data-access package under test contains, and which callables own their transactions →
  `flat-persistence`.
- Where members sit when several distributions share one repository, and the root configuration that
  registers a shared fixture module → `python-workspace`.
- Which scope a fixture takes, which conftest level it belongs at, builders versus fixtures →
  `test-principles`, the constitution. This skill is the flat-family artifact that implements it.
- The project has a domain layer and a dishka composition root → `hex-test-integration-setup`, in the
  `pyhouse-hex` plugin.
- The family itself is unsettled → `architecture-choice`, before either setup skill.

## Template — the shared fixtures (testcontainers, SQLAlchemy async, Alembic)

`tests/integration/conftest.py`:

```python
import os
import subprocess
import sys
from collections.abc import AsyncIterator, Iterator
from pathlib import Path

import pytest
from pydantic import SecretStr
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncEngine

from myapp.postgres import PostgresSettings, create_engine

_CONTAINER_IMAGE = "postgres:<pinned-tag>"  # the major production runs
_DISTRIBUTION_ROOT = Path(__file__).resolve().parents[2]
_SCHEMA_TABLES = text(
    "SELECT string_agg(quote_ident(tablename), ', ') FROM pg_tables"
    " WHERE schemaname = current_schema() AND tablename <> 'alembic_version'"
)


@pytest.fixture(scope="session")
def postgres_settings() -> Iterator[PostgresSettings]:
    from testcontainers.community.postgres import PostgresContainer

    with PostgresContainer(_CONTAINER_IMAGE) as postgres:
        yield PostgresSettings(
            host=postgres.get_container_host_ip(),
            port=int(postgres.get_exposed_port(5432)),
            user=postgres.username,
            password=SecretStr(postgres.password),
            name=postgres.dbname,
        )


def _alembic(settings: PostgresSettings, *args: str) -> None:
    environment = {
        **os.environ,
        "MYAPP_POSTGRES_HOST": settings.host,
        "MYAPP_POSTGRES_PORT": str(settings.port),
        "MYAPP_POSTGRES_USER": settings.user,
        "MYAPP_POSTGRES_PASSWORD": settings.password.get_secret_value(),
        "MYAPP_POSTGRES_NAME": settings.name,
    }
    result = subprocess.run(
        [sys.executable, "-m", "alembic", *args],
        capture_output=True,
        text=True,
        cwd=_DISTRIBUTION_ROOT,
        env=environment,
    )
    assert result.returncode == 0, result.stderr


@pytest.fixture(scope="session")
def _migrated_db(postgres_settings: PostgresSettings) -> PostgresSettings:
    """Up, down to the base and up again, so every downgrade() runs once per session."""
    _alembic(postgres_settings, "upgrade", "head")
    _alembic(postgres_settings, "downgrade", "base")
    _alembic(postgres_settings, "upgrade", "head")
    return postgres_settings


@pytest.fixture(scope="session")
async def engine(_migrated_db: PostgresSettings) -> AsyncIterator[AsyncEngine]:
    engine = create_engine(_migrated_db.dsn)
    try:
        yield engine
    finally:
        await engine.dispose()


@pytest.fixture
async def connection(engine: AsyncEngine) -> AsyncIterator[AsyncConnection]:
    """For anything that accepts a connection; rolled back at teardown."""
    async with engine.connect() as connection:
        transaction = await connection.begin()
        try:
            yield connection
        finally:
            await transaction.rollback()


@pytest.fixture(autouse=True)
async def truncate_all(engine: AsyncEngine) -> AsyncIterator[None]:
    """For code that opens and owns its own transaction; wipes every table afterwards."""
    yield
    async with engine.begin() as cleanup:
        tables: str | None = (await cleanup.execute(_SCHEMA_TABLES)).scalar_one()
        if tables:
            await cleanup.execute(text(f"TRUNCATE {tables} RESTART IDENTITY CASCADE"))
```

**`postgres_settings` yields only the container the suite started**, so nothing it can reach holds data
anyone else wants. Pointing the suite at a database it did not start is a mode of its own, and it arrives with
its guard (`## Other bindings`, rules 2 and 3).

The image tag is a named constant because **the container runs the major version production
runs**, pinned to it, so the suite exercises the planner and DDL surface the migrations will meet. A
floating tag moves the schema under the suite between runs. The exact tag is read from the registry
when it is written (`python-toolchain` rule 12).

**The migration history runs up, down to the base, and up again, once per session.** That round trip is
what proves every revision's `downgrade()` reverses its `upgrade()` (`persistence` rule 20), and the suite
then runs against the schema the history produces. The subprocess runs from the distribution root, where
`alembic.ini` sits, and hands the container's connection details to the migration environment under the
variables that environment reads — the data-access component's own `MYAPP_POSTGRES_` ones
(`flat-project-setup`). The engine comes from the data-access package's own factory, given the settings
object's derived `dsn` (`python-settings` rule 10; rule 5 below).

`truncate_all` is autouse **here** because this conftest is scoped to one directory of integration tests,
all of which reach code that commits. Autouse is also what orders it: pytest sets it up before any fixture
the test requests by name and so finalizes it last, after `connection`'s transaction has rolled back and its
connection returned to the pool — which `TRUNCATE`'s `ACCESS EXCLUSIVE` lock needs (rule 7).

**The wipe asks the store which tables the schema holds**, never the metadata: a `MetaData` knows only
the tables whose modules the session happened to import, so a test run that never imported one leaves
its rows behind for the next test. The migration's own version table is spared, so the schema keeps
the revision it was migrated to. Rows a revision seeds are wiped with the rest; a table whose rows the
migrations own is spared by name beside the version table, or a test arranges the rows it needs. A
history that creates tables in a further schema lists that schema beside `current_schema()`.

No placeholder `MYAPP_POSTGRES_` variables are set for collection: nothing in the service builds
settings or an engine at import (`python-packaging` rule 8), so an unset variable fails only the code
that reads it.

The container library is imported **inside** the fixture that needs it, not at module scope, so a
pure-unit collection pays nothing for it.

## Other bindings

- **One shared instance of these fixtures, where several distributions in one repository share a
  datastore.** The bodies move verbatim into a pytest plugin module beside the tests of the library that
  owns the schema, registered from the repository root's configuration, so every member loads the one
  module instead of a copy each (`python-workspace` carries the root configuration and runs each
  member's suite). Three things
  change and nothing else does: every environment name follows the owning library rather than a
  dependant, the migration subprocess runs from that library's directory, and **nothing in the module is
  autouse** — a plugin is loaded for every collection in the repository, so `truncate_all` keeps its body
  but loses `autouse=True` and each member whose code commits turns it on for its own tests in a
  one-line wrapper fixture.
- **A pre-provisioned throwaway database** — a compose service, a CI service container, one issued per
  branch. `postgres_settings` gains a branch behind a dedicated opt-in flag, carrying rules 2 and 3; the
  migration run, the engine scope and both isolation fixtures are unchanged.
- **An in-process or file-backed engine** (SQLite through an async driver). Cheapest to start, and it
  costs what this level buys: upsert semantics, generated constraint names and transaction behaviour are
  no longer production's, so `flat-test-persistence`'s constraint-name and conflict-path assertions stop
  meaning anything. Never for the data-access package's own suite.
- **A non-relational store**, beside a relational one or alone, gets its own session-scoped container
  and client, and isolates by a per-test namespace deleted at teardown — there is no transaction to roll
  back.
- **Creating the schema from the metadata instead of replaying the migration history.** Faster, and it
  stops testing that the migrations produce the schema the code expects — which is the drift the history
  exists to prevent. Keep the history wherever the migrations are themselves an artifact the project
  ships. **For a store the service reads but another project owns, it is the only choice**: the service
  carries no history for those tables (`persistence`, its schema-ownership row), so `_migrated_db` becomes one
  `metadata.create_all` over the tables the service declares, and the round trip of rule 1 lapses.

## Rules

1. **The migration runs from wherever the schema is defined** — this distribution, or the owning
   library when several share one — with the round trip of `persistence` rule 20; it is the project's
   own schema path `test-principles`, *Datastore contract* rule 8, requires, and a store another
   project owns is created from the metadata instead.
2. **Where the suite can reach a database it did not start, the guard of `test-principles` reliability
   rule 1 lives inside the fixture producing the connection details**, comparing the database name by
   whole-name equality against one project-declared constant. A guard fixture of its own is bypassed by
   whatever reaches for the connection details directly.
3. **Using a datastore the suite did not start is opt-in behind a dedicated flag** (`test-principles`
   reliability rules 1 and 6); raise a named error listing every missing variable.
4. **One pool per run, one transaction per test** — the scopes `test-principles` *Fixture scope rules*
   set. A session-scoped connection would serialize the suite onto one connection.
5. **A test never builds its own pool or calls the engine factory** (`test-principles` reliability rule 6,
   and its one exception). The one session engine is built by the suite's fixture through the data-access
   package's factory — so the suite runs the engine production runs. Tests take the shared fixture and
   pass it explicitly to whatever needs one.
6. **The whole-schema wipe has one body, and it runs after the test rather than before.** Cleaning up
   afterwards means a failing test leaves the datastore inspectable under a debugger, and the next test
   still starts empty. One body wherever it is defined — a second copy is two behaviours waiting to
   diverge. Shared across distributions, it loses autouse (`## Other bindings`).
7. **Do not request the wipe by name in a test that only uses the rollback connection.** The rollback
   already covers it, and a by-name request loses the autouse ordering that keeps the wipe's exclusive
   table lock from meeting the connection's still-open transaction.
8. **Every fixture and test shares the session-scoped engine's one event loop** — `test-principles`,
   *Fixture scope rules*; the two loop-scope lines of `python-toolchain`'s pytest block are that rule here.
9. **Code that opens and owns its transaction is isolated by the wipe, never by a rollback or savepoint
   fixture.** It opens its own connection (`persistence` rule 1), so a savepoint isolates a
   connection nothing under test uses, and the test passes while asserting nothing.

## Hard stops

- The distribution has no relational store → stop; none of these fixtures applies — no transaction to
  roll back, no schema to truncate.
- The code under test sits behind a domain port and a dishka container → stop, use
  `hex-test-integration-setup`, in the `pyhouse-hex` plugin.
