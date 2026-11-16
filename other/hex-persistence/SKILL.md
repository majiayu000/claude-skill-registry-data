---
name: hex-persistence
description: Use when one hexagonal service's own relational layer changes — the `Table` and its constraints, the repository adapter satisfying a domain repository protocol, the paired Alembic revision, or the store's settings class with its engine and repository binding — or when one command must write two or more repositories atomically through a unit of work. Owns the SQLAlchemy Core templates binding `persistence`'s store-generic rules — the shared naming convention, the entity mapper, the integrity-error translator — the adapter's standalone and unit-of-work-managed forms, the port's read contract, the paired revision, and the unit-of-work protocol, implementation and handler form. Not compensation for an external write (`hex-application`), not a flat-layered service's data-access package, which binds the same rules with no port in front of it (`flat-persistence`, in the `pyhouse-flat` plugin), and not a nonrelational store (`hex-store-repository`).
paths: ["**/infrastructure/**", "**/alembic/**", "**/migrations/**", "**/domain/uow/**"]
---

# Hexagonal Persistence (relational)

The table, the repository that queries it, and the migration that ships it, kept together because the
constraint names are one contract across all three (`persistence` rule 7).

**Load `persistence` before writing any file below**; the templates satisfy its rules and do not
restate them. The rules here are the hexagonal shape around them: an adapter behind a port, its two
constructor forms, the paired revision and the unit of work.

For a non-relational store — a key-value, cache or document backend — use the client-repository form
instead. The store profile decides which applies (`hex-conventions` block B).

## When to use vs. neighbours

- The obligations any store's data access meets, whatever the family — transaction ownership,
  driver-error translation, constraint names, row mapping, stored types and indexes, conflicts and
  ordering, safe schema changes → `persistence`; this skill binds them.
- A persistent table, its columns, constraints or indexes → `TABLE.md`.
- The adapter satisfying a domain repository protocol on a relational store → `REPOSITORY.md`.
- The migration pairing with a schema change → `REVISION.md`.
- The `IFooRepository` protocol file the adapter is written against → `hex-domain-ports`.
- Why the adapter satisfies that protocol structurally and never inherits it → `hex-architecture`.
- The one-time migration bootstrap — config, `env.py`, and a baseline only over a schema that already
  exists → `hex-project-setup`.
- A repository on a client-style store — key-value, document, or an index kept beside the authoritative
  store, reached through an injected SDK client instead of the shared engine → `hex-store-repository`.
- Tables, upserts and migrations in a flat-layered service's own data-access package, reached
  directly rather than through a port → `flat-persistence`, in the `pyhouse-flat` plugin.
- The store's settings class and its container binding → `REPOSITORY.md`; what a settings class
  declares → `python-settings`; lifetimes, declaration order and the base they merge into → `hex-wiring`.
- The engine and session factories the binding calls → `REPOSITORY.md`, beside the settings class.
- A command writing two or more repositories that must commit together — the unit-of-work protocol, its
  implementation and binding, and the handler form that opens it → `UNIT_OF_WORK.md`.
- What the relay delivering an outbox row owes → `at-least-once-delivery` rule 6.
- An external write undone when a later store write fails (compensation) → `hex-application`.
- The exception classes the translator raises → `exception-catalog`.
- The integration test that drives this adapter against a real database → `hex-test-repository-contract`.
- A data-only migration (`backfill_*`, `seed_*`) with no DDL → its own revision file; this skill covers
  DDL only.
- Asked for an ORM, a declarative base or relationships → still this skill: the templates here
  are Core, and an ORM project satisfies the rules here and `persistence`'s through the ORM bullet under
  `## Other bindings`; do not copy a Core template into a mapped class.

## Template(s) — SQLAlchemy Core, asyncpg, Alembic

```
src/myapp/infrastructure/postgres/
├── postgres_settings.py           # PostgresSettings
├── engine.py                      # engine and session factories — REPOSITORY.md
├── metadata.py                    # the shared MetaData with naming_convention
├── tables/
│   ├── __init__.py                # import the new module and name it in __all__ (no wildcard)
│   └── foos.py                    # the Table
└── repositories/
    ├── __init__.py                # re-export the new module
    └── foo_repository.py          # the adapter

migrations/versions/
└── <revision>_create_foos.py      # authored via `alembic revision`, hand-edited to the rules below
```

The full file templates live in topic files, one per artifact in that layout plus one for the unit of
work. **Read the topic file for the artifact before writing or changing it** — only this file is
loaded automatically:

- **`TABLE.md`** — the naming convention, the table template, and the column, foreign-key, index,
  constraint, child-table and default rules.
- **`REPOSITORY.md`** — the two constructor forms, the session, read, mutation,
  translation and mapping rules, the shared-mapper extraction threshold, and the store's settings class
  with its engine factories and container binding.
- **`REVISION.md`** — the revision template, the drift check and the downgrade rule.
- **`UNIT_OF_WORK.md`** — only where a command writes two or more repositories atomically, an aggregate
  and an outbox row among them: the protocol in `domain/uow/`, its implementation beside the repositories, its
  binding, and the handler form that opens it.

## Other bindings

- **The ORM (declarative mapping plus a session).** Mapped classes replace the table objects and the
  session's identity map replaces explicit statements; the port conformance, the transaction-ownership
  split, the integrity-error translation, the row-to-entity mapping and the constraint-name contract are
  all unchanged. What you give up is the thing the primary binding is chosen for: with Core the SQL that
  runs is the SQL in the file, so a query's cost is readable at the call site and lazy loading cannot
  appear behind an attribute access. Under the ORM the mapped class is *not* the domain entity — keep the
  two separate and keep the mapper, or the domain grows a persistence dependency.
- **Another engine or driver.** Every rule here and in `persistence` holds; the dialect-specific column
  types, the SQLSTATE codes and the attribute path the translator reads the constraint name through all
  change together. The skill states that coupling where it bites (`REPOSITORY.md`), because it is the
  one place a driver swap is not mechanical.
- **A platform that supplies one connection URL.** The class in `REPOSITORY.md` holds one secret-typed
  `url` field in place of the five connection fields. A validator on the raw input, before the secret type
  wraps it, normalizes the URL to what the async driver accepts — its scheme, and the query parameters it
  spells differently (`sslmode` becomes asyncpg's `ssl`, or the first connection fails) (`python-settings`
  rule 12); `dsn` returns it, so no consumer changes. The deployment maps the platform's `DATABASE_URL`
  onto `MYAPP_POSTGRES_URL`, in its own declaration where the repository holds one (`python-settings`
  rule 2).

## Rules

1. **The adapter satisfies the port structurally** (`hex-architecture` rule 7). Signatures match the
   protocol exactly — keyword-only markers and async/sync mode included.
2. **Each of `persistence` rule 1's two forms is its own class.** A standalone adapter opens its own
   session and commits only on a mutation; a unit-of-work-managed one receives the unit of work's live
   session and never commits or rolls back. A class that would need both call styles is two adapters.
3. **The read contract is the port's.** Fetch-by-identity raises rather than returning nothing, a
   secondary lookup may return an optional, a list returns a sequence ordered by *the caller's* chosen
   sort, a count returns an integer. A hardcoded default order that ignores the filter's sort is a bug,
   not a default.
4. **A schema change is a coordinated pair in one commit** — the table definition and one new
   migration. What the migration itself owes — a deploy step compatible with the running code, a
   reversing downgrade proven by the round trip, a generated draft reviewed before commit — is
   `persistence` rules 19 and 20.
5. **A unit of work exists only where one command writes two or more repositories that must commit
   together, and there is one per transactional scope, never one per aggregate.** Every repository that
   may join the transaction is a member of the same domain protocol, typed by its port. A second one is
   earned only by a genuinely different scope and is named for that scope's role, never for its backend.
6. **One unit of work per `execute`, opened by the handler from an injected zero-argument factory.**
   Never shared across calls, never pooled: a shared one merges two callers' writes into one
   transaction, so one caller's failure rolls back the other's work. The composition root binds the
   factory, never an instance (`hex-wiring`).
7. **Commit is explicit and the last statement in the block; leaving it any other way rolls back.**
   An effect after the block follows `hex-application`, After the store write. Nothing inside the
   block catches — only compensation wraps it (`hex-application`) — and a failed unit of work is not
   retried in the handler: the transaction is unusable once a statement in it failed.

## Inlined typing / import rules

Table module:

- The schema-construction names from the library root; dialect-specific types from the dialect module;
  the shared metadata imported relatively from `..metadata`.

Repository module:

- Domain imports absolute (`from myapp.domain.foos import Foo`); the table relative
  (`from ..tables.foos import foos_table`). **Never import the protocol the adapter satisfies**
  (`hex-architecture` rule 7).
- Import only the domain exceptions this repository actually raises, not the whole catalogue.
- Type the driver's row so the mapper needs no ignore comment. Under the primary binding that is
  `.mappings()` → `RowMapping` accessed by key (`row["id"]`); never type a row as `object` with attribute
  access, which forces an ignore at every column. Where the library's own typing is too loose to read a
  field off — the affected-row count is the standing case — **narrow once with a cast, never silence with
  an ignore**.
- Parameters keep their domain types; never downcast to `dict`.

Both:

- No `from __future__ import annotations` (`python-style`). Full annotations on every method. No comments
  unless the *why* is non-obvious (`python-style`).

## Package wiring

`tables/__init__.py` must import the new table module and name it in `__all__` —
`from . import foos` beside `__all__ = ["foos"]` — otherwise migration autogenerate cannot see the table,
and the linter reads the bare import as unused and removes it. A table module's public name is a bare
object, not a class, so it is not wildcarded into the package (`python-packaging` carve-out 3); the
repository imports it from its own module (`from ..tables.foos import foos_table`).
`repositories/__init__.py` re-exports the new adapter class with the usual
`from . import foo_repository` + wildcard. `metadata.py`'s public name is a bare
`MetaData`, so it is not wildcarded into `infrastructure/postgres/__init__.py` either (`python-packaging`
carve-out 3 — `metadata` would shadow its own module, which the type checker rejects as a redefinition
and which breaks the package's `metadata.__all__` at import): the package re-exports its other modules
and leaves `metadata` out of both the import line and the `__all__` sum. The tables and the migration
environment import it from its module (`from ..metadata import metadata`,
`from myapp.infrastructure.postgres.metadata import metadata`). Mechanics: `python-packaging`.

## Hard stops

- A unit of work is asked to span two backends (a table plus object storage or a cache) → stop, that is
  compensation in `hex-application`, not a unit of work.
- Asked to mint an id inside the repository → stop, use `hex-application`, which owns the identity
  scheme (Command handler rule 6) and its one store-minted exception.
- The change includes a data migration (`backfill_*`, `seed_*`) → stop, that is a separate revision
  file; this skill covers DDL only.
