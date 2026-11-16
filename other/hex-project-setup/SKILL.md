---
name: hex-project-setup
description: Use when laying a hexagonal project down once — which libraries its core, its entrypoints, its stores and its features bring, the floors this family's templates rely on, and the Alembic bootstrap the revision chain cannot start without (config, environment, and a baseline only over a schema that already exists). The src layout, ruff and mypy, the line length and the dependency-floor discipline every Python project shares are `python-toolchain`'s. Never per feature — the per-change migration revision is `hex-persistence`, runtime DI bindings are `hex-wiring`, and what a settings class declares is `python-settings`.
---

# Hexagonal Project Setup — dependency substrate, migration bootstrap

What a hexagonal project needs *once*, beyond the toolchain every Python project carries: the libraries
its layers bring, and the migration bootstrap. None of it recurs per feature. The project file itself —
src layout, ruff, mypy, dependency declarations — is `python-toolchain`'s; the derivation rules that do
recur are `hex-conventions`; the layer boundaries are `hex-architecture`.

## When to use vs. neighbours

- Adding a dependency, or justifying one of this family's floors → block A.
- Laying migrations for the first time on a project that has none → block B.
- The `pyproject.toml` tables, the src layout, the linter and type checker, the sanctioned
  suppressions, the line length, and whether any dependency may carry a floor → `python-toolchain`.
- The *per-change* migration revision that pairs with a schema edit → `hex-persistence`, not here;
  this skill covers only the bootstrap that lets the chain start.
- Where a file goes and what it is called → `hex-conventions`.
- Layer boundaries → `hex-architecture`; packaging mechanics → `python-packaging`.
- Module files, `__all__` and the re-export contract inside the package → `python-packaging`.
- The runtime DI bindings → `hex-wiring`; the environment-backed settings classes → `python-settings`, each shown beside the adapter that reads it. This skill stops at which libraries exist.
- The interpreter floor → `python-style`.
- Whether the project should be hexagonal or flat-layered at all → `architecture-choice`; settle that before laying this down.
- A multi-service uv workspace rather than a single package → `python-workspace`.

## A. Stack substrate by role — uv

`pyproject.toml` is `python-toolchain`'s template, laid the way that skill lays it; it carries the core
substrate plus whatever each entrypoint package and each infrastructure adapter needs,
each added with `uv add` or `uv add --dev`.

- **Core substrate** (always present, whatever the program is): the settings library, the
  dependency-injection library, and the structured logger. Every hexagonal program reads configuration,
  composes its adapters at one root, and logs — a worker, a batch job and a single-command CLI included.
  `myapp.logging.configure_logging` is the service's one logging setup (`python-logging` rule 3): where
  the service has none yet, it is written there once, safe to run again, and every entrypoint calls it
  before anything logs.
- **Entrypoint substrate** (whatever the entrypoint packages the project actually has require, and
  nothing else): an HTTP entrypoint brings its web framework, that framework's server, and the
  validation library its wire schemas are written in; a queue or scheduled entrypoint brings its broker
  or scheduler client; a CLI entrypoint brings its argument parser, which may be the standard library
  and therefore nothing at all. A project with no HTTP entrypoint carries no web framework and no
  server — the same trigger rule as a feature extra, applied to the entrypoint layer.
- **Relational substrate** (only when a relational store backs a repository): the ORM/Core library with
  its async extra and the async driver — and the migration tool only when the store's schema is one
  this service owns. A service that only reads a table another owns carries no migration tool.
- **Feature-triggered extras** — a package required only because some endpoint or adapter uses a specific
  feature. Multipart form handling is the canonical example: a web framework typically imports its
  multipart library at app-construct time for any form route, and without it constructing the app raises
  — which lint, type-check and the unit tier do **not** catch. An app with no such endpoint must not
  carry it.
- **Dev** (always present): the test runner and its async plugin, the linter and the type checker.
  Triggered alongside them: the container library, once an integration tier drives a real backing
  service, and a transport test client for each entrypoint the suite drives over its own transport — an
  HTTP test client belongs to a project with HTTP routes to call. An adapter that calls an HTTP API
  brings no interception library: its test stubs the transport with the HTTP client's own
  (`hex-test-capability-adapter`).
- **Test-bootstrap extras** follow the same trigger rule as feature extras: a suite that mints
  asymmetric-signature tokens needs the crypto library that generates the keypair; a project verifying
  symmetric or opaque tokens generates no keypair and must **not** carry it. A dev dependency nothing
  imports is a stray package.
- **SDK packages are not listed as substrate** — each rides along with the adapter that needs it.

Every entry is a name; a floor is written only at a known breaking boundary with the API beside it
(`python-toolchain` rule 9), and an adapter's SDK takes one on exactly the same terms. The async test
plugin's floor is `python-toolchain`'s.

An adapter that calls an HTTP API, and the HTTP test client, bring `httpx2>=2` — 2.0 is the first
release carrying the client API, and the only earlier one is an empty 0.0.0 placeholder.

The FastAPI floor is written only where the app declares auth: the auth probe (`hex-test-restapi-auth`) walks the
app's resolved operations through `fastapi.routing.iter_route_contexts`, which first ships in 0.137.2,
and from 0.137.0 an included router is a single `_IncludedRouter` entry in `app.routes`, so a walk over
`app.routes` alone no longer reaches the operations. Below 1.0 a release's minor is its breaking segment,
so the floor names the release that shipped the API rather than a major:

```toml
[project]
dependencies = [
    "fastapi>=0.137.2",  # iter_route_contexts, the resolved-route walk the auth probe relies on
]
```

## B. Relational migration bootstrap (write-once) — Alembic over SQLAlchemy and Postgres

Laid **only for a relational store whose schema this service owns**, the same trigger as the migration
tool and the first table. The migration tool owns the revision chain, but the chain cannot start — and
`alembic upgrade head` cannot run — without the **config** (pure glue, rewritten freely), and over a
database that already holds objects, a **baseline revision** (write-once). Without the config the
integration suite dies at setup with `No 'script_location' key found`. Nothing in lint, type-check or the unit tier catches that; only a real
run against a database does.

The three config files are complete glue. `alembic.ini`, at the tree root:

```ini
[alembic]
script_location = migrations
prepend_sys_path = src
```

`migrations/env.py` runs async and in online mode only — the app is always migrated against a live
connection, so offline mode is refused rather than half-supported:

```python
import asyncio

from alembic import context
from sqlalchemy import Connection

import myapp.infrastructure.postgres.tables  # noqa: F401
from myapp.infrastructure.postgres import PostgresSettings, create_engine
from myapp.infrastructure.postgres.metadata import metadata
from myapp.logging import configure_logging

target_metadata = metadata


def _run(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


async def _run_online() -> None:
    engine = create_engine(PostgresSettings())
    try:
        async with engine.connect() as connection:
            await connection.run_sync(_run)
    finally:
        await engine.dispose()


if context.is_offline_mode():
    raise RuntimeError("offline migrations are not supported")
configure_logging()
asyncio.run(_run_online())
```

The engine is disposed however the run ends. The migration run is a process like the others, so the
environment calls the service's one logging setup (block A); left unconfigured, the tool's records reach
no configured handler.

`migrations/script.py.mako` is the template `alembic init -t async migrations` writes — run once from
the tree root, with the `alembic.ini` and `env.py` it also writes replaced by the two above and its
`README` deleted — with three edits, so that every revision `alembic revision` renders passes the linter and `python-style`: its revision identifiers are annotated
`str | Sequence[str] | None` with `Sequence` from `collections.abc`, never `typing.Union` or
`typing.Sequence`; `import sqlalchemy as sa` moves ahead of `from alembic import op`, the order the
linter's import sort requires; and the tool's explanatory comments go (`python-style`, Comments).
Nothing else in it changes.

Where the chain is rooted, and when a baseline exists at all, is `persistence` rule 20; under Alembic
it is spelled as follows. **On a greenfield project `migrations/versions/` starts empty**, and the first
table the project adds is autogenerated and reviewed like every later one; Alembic gives it no parent,
and `alembic upgrade head` and `downgrade base` already succeed on an empty chain. **Over a database that
already holds objects**, the baseline revision is created only while `migrations/versions/` carries no
`*.py` yet, with no parent, its objects spelled out in `op` calls and never `metadata.create_all`,
importing nothing from `src/` — neither the metadata nor the table registrar — and each existing database is marked with `alembic stamp <baseline revision>`; a fresh one — the integration
suite's — runs it like any revision.

**Every subsequent migration is a real revision** (`uv run alembic revision --autogenerate -m "<change>"`)
— see `hex-persistence` for the per-change form.

`migrations/` lives at the tree root, outside `src/` and `tests/`: linted, not type-checked
(`python-toolchain` rule 2). `env.py` is a composition root, so it constructs the settings class itself
(`python-settings` rule 13).

**This block sanctions two lint suppressions, the ones `python-toolchain` rule 5 leaves to it.** The
inline unused-import suppression on `env.py`'s registration import: it exists only for its side effect,
and without it the linter deletes it and autogenerate stops seeing the schema. And the per-file
statement-count ignore on `migrations/**/versions/*.py`, the line `python-toolchain`'s template marks: a
revision's body is generated DDL, one statement per column and constraint, not authored logic, and a
wide table is not a function to split; every other bound stays on for revisions.

## Other bindings

- **Another package manager.** poetry or pdm replace `uv add`; the substrate by role, the SDK riding
  with its adapter and the floor with its API are unchanged. The rest is `python-toolchain`'s.
- **Another migration tool.** The config file, the revision template and the autogenerate command all
  change; the environment logging through the service's one configuration, the chain's root and its
  baseline (`persistence` rule 20), and the mandatory reverse operation do not.

## Rules

1. Select dependencies by block A's core substrate plus its entrypoint, store and feature triggers;
   include an SDK only with its adapter. A feature's package or an entrypoint's framework is added only
   to an app that has that feature or entrypoint: a dependency nothing imports is a stray package. Every
   entrypoint calls the service's one logging setup, `myapp.logging.configure_logging`, written once
   where the service has none, before anything logs.
2. Write a floor — an SDK's or a substrate library's — only at the documented breaking boundary the
   project's code relies on, under `python-toolchain` rule 9; block A's one is this family's.
3. Take everything else in the project file from `python-toolchain` — the src layout, the development
   group, the linter and type-checker configuration with its written bounds and sanctioned
   suppressions, the line length — and the interpreter floor from `python-style`.
4. Add the complete migration configuration only for a relational store whose schema this service owns.
5. Root the chain as `persistence` rule 20 says, spelled under Alembic in block B. Every table the
   project adds is its own revision under `hex-persistence`.
6. The migration environment disposes its engine however the run ends, refuses offline mode, and calls
   the service's one logging setup (rule 1); the revision template renders `python-style`'s annotation
   forms in the linter's import order.

## Hard stops

- The project file's lint, type-check or layout settings are being chosen here → stop, use
  `python-toolchain`.
- A table the project is adding is being written into the baseline → stop, the baseline holds only what
  already existed; the new table is its own autogenerated, reviewed revision (`hex-persistence`).
- A baseline, empty or not, is being written for a greenfield project → stop, the first table's
  autogenerated revision is the root (`hex-persistence`).
- Migrations are being laid for a relational store this service only reads → stop, the schema's owner
  versions it.
- The project is flat-layered → stop, use `flat-project-setup`, in the `pyhouse-flat` plugin.
