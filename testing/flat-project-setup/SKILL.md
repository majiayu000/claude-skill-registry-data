---
name: flat-project-setup
description: Use when laying a flat-layered service down once — which runtime and development libraries each of its roles brings, with the version floors this family's templates rely on, and the relational migration bootstrap (`alembic init -t async` under `migrations/postgres/`, then the generated environment changed to read the connection string at its own composition root and see every table, the revision template changed to the house annotation forms, and a baseline only over a schema that already exists). The src layout, ruff and mypy, the line length and the dependency-floor discipline every Python project shares are `python-toolchain`'s. Never per feature — each later schema revision is `flat-persistence`'s, and the package layout inside `src/` is `flat-layered`'s. A hexagonal project's setup is `hex-project-setup`, in the `pyhouse-hex` plugin. - Also when asked to start a new worker, pipeline or ETL service, which libraries it needs, to add a dependency or justify one of this family's version floors, or to add migrations to a flat service that has none.
---

# Flat Project Setup — dependencies by role, migration bootstrap

What a flat-layered service needs **once**, beyond the toolchain every Python project carries: the
libraries its roles bring, and the migration bootstrap the first revision cannot be written without.
None of it recurs per feature. The project file itself — src layout, ruff, mypy, dependency
declarations — is `python-toolchain`'s; what goes inside `src/myapp/` is `flat-layered`; what a schema
change looks like after the bootstrap is `flat-persistence`.

## When to use vs. neighbours

- Starting a flat service, adding a dependency, or justifying one of this family's floors → block A.
- Laying migrations on a service that has none → block B, once; this skill is one-shot, and
  `flat-persistence`'s revisions and `flat-test-integration-setup`'s migration fixture both depend on it
  having run.
- The `pyproject.toml` tables, the src layout, the linter and type checker, the sanctioned
  suppressions, the line length, and whether any dependency may carry a floor → `python-toolchain`.
- A second store's migration directory beside `migrations/postgres/`, and the tool that applies it →
  `flat-persistence`, which owns where every store's history lives.
- The per-change revision that pairs with a table edit, and what a deploy obliges of it →
  `flat-persistence`.
- The packages inside `src/myapp/`, the settings class each component owns, and the entry point →
  `flat-layered`.
- The pytest configuration block → `python-toolchain`; the fixtures it loads →
  `flat-test-integration-setup`.
- Which version the distribution itself declares, and what changes it → `python-versioning`.
- The interpreter floor, annotation forms, and the comment rules migrations follow → `python-style`.
- `__init__.py` re-exports and import forms → `python-packaging`.
- Several distributions in one repository — the workspace root, settings shared at the root →
  `python-workspace`; each member's libraries are still chosen by this skill.
- The family is not settled → `architecture-choice`. A hexagonal project → `hex-project-setup`, in the
  `pyhouse-hex` plugin.

## A. Dependencies by role — uv

`pyproject.toml` is `python-toolchain`'s template, taken as written; `uv init --package --build-backend
hatch myapp` lays it. Then delete the `main` it writes into `src/myapp/__init__.py` and the
`[project.scripts]` entry that points at it. A service that runs a single process starts it from
`__main__.py`; a service with several processes declares one console script per process in
their place (`flat-layered`). What this family adds is which libraries arrive, each with
`uv add` or `uv add --dev`, and the floors its own templates rely on.

**Dependencies are chosen by the roles the service actually has.** The settings library and the
structured logger are always present — every process reads configuration and logs. The rest arrive with
the role that needs them and not before:

| Role present | Runtime dependencies it brings | Development dependencies it brings |
|---|---|---|
| any | `pydantic`, `pydantic-settings`, `structlog` | `python-toolchain`'s development group, as written |
| a client over HTTP | `httpx2>=2` (2.0: the first release carrying the client API; the only earlier one is an empty 0.0.0 placeholder) | — |
| data access on a relational store | `sqlalchemy[asyncio]>=2` (2.0: inline type annotations under mypy `--strict`), `asyncpg` | `testcontainers[postgres]>=4.15` (4.15: `testcontainers.community`) |
| a relational store whose schema this service owns | `alembic` | — |
| a service that mints row ids | `uuid6` | — |
| an HTTP trigger | `fastapi`, `uvicorn` | `httpx2>=2`, the in-process test client, unless the client-over-HTTP row already brings it |
| a durable-execution engine, once earned | the engine's SDK | the engine's test harness |
| a vendor SDK client | that SDK, with the client that wraps it | whatever double the SDK ships |

A service with no datastore carries no Core library, no driver and no migration tool; one that only
reads a table another service owns carries the Core library and the driver and no migration tool; one
with no HTTP trigger carries no web framework. A dependency nothing imports is a stray package.

**Each floor is written with the API beside it, as a comment on its line** —
`"sqlalchemy[asyncio]>=2",  # 2.0: inline type annotations under mypy --strict`. The three above are
there because this family's templates call exactly those names — httpx2's client, the strictly typed
engine and the container module. A service whose own code
calls none of a floor's names drops the floor and its comment together; one that relies on something
newer raises the floor and names that instead (`python-toolchain` rule 9).

## B. The migration bootstrap — Alembic over SQLAlchemy async

Laid only when the service owns the schema of a relational store, and once. `alembic upgrade head` —
and the integration suite that replays it — cannot run without the config and the environment. The
history lives in `migrations/postgres/`, the directory named for the store it versions, because a second
store's history would sit beside it (`flat-persistence`); `alembic.ini` stays at the distribution root,
beside `pyproject.toml`, where every `alembic` command and the integration suite run from. The tool lays
both, run from the distribution root:

```bash
alembic init -t async migrations/postgres
```

It writes `alembic.ini` with `script_location` already pointing at `migrations/postgres`, and in that
directory `env.py`, `script.py.mako`, a `README` and an empty `versions/`. The `README` is deleted. What
it writes is the tool's generic starting point, not this family's bootstrap; before the first revision,
the generated files are changed to do what follows.

**Nothing in `alembic.ini` names a database.** The `sqlalchemy.url` line `init` writes is deleted, and so
is every logging section — `[loggers]`, `[handlers]`, `[formatters]` and the `[logger_*]`, `[handler_*]`,
`[formatter_*]` sections they list — which only the generated logging setup reads; the rest may stay as
generated.

**The migration environment is the migration run's process definition**, so it is the one place outside
the service's own entrypoints that builds the data-access component's settings. `env.py` is changed so
that:

- the engine comes from the data-access package's engine factory, given the `dsn` that component's own
  settings class derives (`flat-persistence`; `flat-layered` rules 6 and 7), in place of the generated
  engine built from the ini section;
- the engine is disposed however the run ends, not only after a clean one;
- `target_metadata` is the data-access package's one `MetaData`; left at the generated `None`,
  autogenerate refuses to run;
- **every table module is imported, one line each**, because a table module's names are bare objects
  the data-access package does not re-export (`python-packaging`), and autogenerate compares only the
  tables that registered; a new table module adds its line in the same change that adds the module;
- logging is configured as every other process definition of the service configures it — the service's
  own logging setup, called once before the run — in place of the generated `fileConfig` call on
  `alembic.ini`, which would give the tool's records their own handler and format beside the service's
  structured stream (`python-logging` rule 3);
- offline mode is refused rather than half-supported — the generated offline branch is replaced by an
  error, because every migration runs against a live connection;
- the tool's explanatory comments go, as they do from any source file (`python-style`, Comments).

**The revision template is kept as `init` writes it, with three edits: its annotations, its import order
and its comments.** The
generated `script.py.mako` annotates its revision identifiers with `typing.Union` and `typing.Sequence`
and places `from alembic import op` ahead of `import sqlalchemy as sa`, so every revision it rendered
would break `python-style`'s annotation forms and fail the linter's import sort. Its annotations become
`str | Sequence[str] | None` with `Sequence` from `collections.abc`, `import sqlalchemy as sa` moves
ahead of `from alembic import op` — the order the linter's import sort requires — and the tool's
explanatory comments go (`python-style`, Comments); nothing else in it changes.

**This block sanctions two lint suppressions, the ones `python-toolchain` rule 5 leaves to it.** The
inline unused-import suppression on the environment's registration imports: they exist only for their
side effect, and without it the linter deletes them and autogenerate stops seeing the schema. And the
per-file statement-count ignore on `migrations/**/versions/*.py`, the line `python-toolchain`'s template
marks: a revision's body is generated DDL, one statement per column and constraint, not authored logic,
and a wide table is not a function to split; every other bound stays on for revisions.

### The root of the chain

Where a chain is rooted, and when a baseline exists at all, is `persistence` rule 20; under Alembic it
is spelled as follows. **Greenfield, `versions/` starts empty**, and the first table's revision is
autogenerated from the metadata and reviewed like every later change
(`alembic revision --autogenerate -m "<change>"`, as `flat-persistence` makes each); Alembic gives it no
parent, and an empty `upgrade head` and `downgrade base` already succeed before it exists. **Over a
schema that already exists**, the baseline is written into an empty `versions/` with every table, column
and constraint spelled out in `op` calls, never `metadata.create_all`, importing nothing from `src/` —
neither the metadata nor the table modules — and each existing database is marked with `alembic stamp` at the baseline's revision; a fresh one — the integration suite's — runs it
like any revision.

## Other bindings

- **Another package manager.** poetry or pdm replace `uv add`; the roles and what each brings, and the
  floors with their APIs, are unchanged. The rest is `python-toolchain`'s.
- **Another migration tool.** Its init command, config file, revision template and autogenerate
  command change, and so do the lines its generated environment needs changed; the history in
  `migrations/postgres/` at the distribution root, the environment reading the connection string at its
  own composition root, seeing every table and logging through the service's one configuration, the
  chain's root and its baseline (`persistence` rule 20), and a reverse operation in every revision do
  not.

## Rules

1. **Laid once, in `python-toolchain`'s src layout, from the first commit**, with migrations — where the
   service owns the schema of a relational store — at the distribution root beside `src/` and `tests/`,
   in one directory per store named for it, and their config beside the project file.
2. **Dependencies follow the roles the service has.** The settings library and the structured logger
   always; everything else arrives with the role that imports it, and a package nothing imports is
   removed.
3. **A floor is written only where this family's code relies on the API it names**, with that API
   beside it; the table in block A is the family's whole set, and each goes with the code that calls it.
   The floor discipline itself is `python-toolchain` rule 9.
4. **Everything else in the project file is `python-toolchain`'s** — the development group, the linter
   and type-checker configuration with its written bounds and the suppression it sanctions everywhere,
   the line length — and the interpreter floor is `python-style`'s. Block B's two suppressions are
   sanctioned here, and only where block B is laid.
5. **The migration environment reads the connection string through the data-access component's own
   settings class, and only there among migration files.** It is the migration run's process
   definition; the migration config names no database, the variables the environment reads are the
   ones the integration suite sets for it, and the engine it builds is disposed however the run ends.
6. **The migration environment sees the whole schema**: its target is the data-access package's one
   metadata, every table module is imported by it, and a new table module adds its import in the same
   change.
7. **The generated bootstrap is the tool's starting point, not the bootstrap.** Lay it with the tool's
   own init, then change what it wrote to meet rules 5 and 6, configure logging as the service's other
   processes do, refuse offline mode, and render revisions in `python-style`'s forms and the linter's
   import order.
8. **The chain is rooted as `persistence` rule 20 says**, spelled under Alembic as in *The root of the
   chain* above.

## Hard stops

- The project file's lint, type-check or layout settings are being chosen here → stop, use
  `python-toolchain`.
- A baseline revision is being written into a `versions/` that already holds revisions → stop, the chain
  has started; write a revision (`flat-persistence`).
- A baseline, empty or not, is being written for a greenfield schema → stop, the first table's
  autogenerated revision is the root (`flat-persistence`).
- Migrations are being laid on a service that owns no relational schema — none at all, or one it only
  reads → stop, there is nothing for it to version; the schema's owner versions it.
- The service is hexagonal → stop, use `hex-project-setup`, in the `pyhouse-hex` plugin.
