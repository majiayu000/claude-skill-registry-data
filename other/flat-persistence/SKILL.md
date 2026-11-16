---
name: flat-persistence
description: Use when a flat-layered service reads or writes a datastore — its table definitions, its component-owned settings class, the repository class that owns each write's transaction and builds its statements, and where its migration history lives. Owns one data-access package per store named for its technology, the SQLAlchemy Core binding of `persistence`'s store-generic rules, application-minted time-ordered keys, the settings class and engine factory the process definition builds, and one migration directory per store at the distribution root, only where the service owns the schema. Transaction ownership, driver-error translation, constraint names, conflicts and ordering, batched writes, cursor reads and safe migrations are `persistence`'s. A hexagonal service's repository adapter behind a port is `hex-persistence`, in the `pyhouse-hex` plugin; the repository root hosting a data-access library several distributions share is `python-workspace`. - Also when asked for an upsert, an `ON CONFLICT` clause, a repository class in a flat service, a second store beside the first, a constraint naming convention, a migration for a flat service or where its files go, deduplicating writes, or where a service's SQL is allowed to live.
---

# Flat Persistence — one package per store owns the data access

The package a `flat-layered` service keeps its data access in — the *data access* role kind in that
skill's import contract — named for the store's technology: `postgres/` for the relational store the
templates bind. It holds the table definitions, the write path and the mapping from stored rows back to
the service's own types. Where the service owns the store's schema, its migration history is data, not code, and
sits at the distribution root under `migrations/` in a directory named for the same store.

**Load `persistence` before writing any file below**; the templates satisfy its rules and do not
restate them. It owns the store-generic obligations — the declared transaction owner, translation at
this package's edge, generated constraint names, the pure row mapping, stored types, conflicts and
ordering, deduplication left to the store, batched writes, paged reads, and migrations — and which of
them bind, answered once there from the store's properties. This skill adds the flat family's shape
around them — one package per store, its settings class and engine factory, the key policy and where
the history lives — and binds all of it to one stack.

Its own rules carry preconditions of the same kind. Rule 6 holds wherever the schema is versioned by
migrations at all, rule 2 wherever the service mints keys, and the rest for any store.

The default subject is **one distribution with one store**. **A service with a second store has a second
package** (rule 5), answering `persistence`'s questions for itself. Where several distributions share
one store, the package becomes a library they all depend on and rule 4 says what that changes.

## When to use vs. neighbours

- The obligations any store's data access meets, whatever the family — transaction ownership,
  driver-error translation, constraint names, row mapping, stored types, conflicts and ordering, cursor
  reads, safe schema changes → `persistence`; this skill binds them.
- The service's own modules and role packages around this one — the settings and logging modules at the
  package root, the clients, the work units → `flat-layered`, which owns the import contract this
  package sits inside, the rule that each configured component declares its own settings class, and the
  no-`Protocol` rule this skill applies to the datastore.
- Several distributions sharing one repository, and where a shared data-access library sits inside it →
  `python-workspace`.
- What triggers a run and hands this package its connection handle → `flat-entrypoint`.
- Testing these tables and the repository class against the real datastore →
  `flat-test-persistence`.
- The container, migration and isolation fixtures those tests run on → `flat-test-integration-setup`.
- The store's dependencies and the relational migration environment laid once, before the first
  revision → `flat-project-setup`; the toolchain → `python-toolchain`.
- The exception classes the translator produces, and what context they carry → `exception-catalog`.
- What the repository class is called → `naming`, whose data-access suffix is `Repository`.
- Module layout, `__all__`, and the `__init__.py` re-exports every table module needs →
  `python-packaging`.
- The declared type a row is mapped into before it leaves this package → `python-style` owns the rule
  that a record crossing a boundary is a declared type; `flat-layered` says which package declares it.
- The service enforces business invariants that must outlive a change of datastore → not this skill, and
  not this family: that is `hex-persistence`, in the `pyhouse-hex` plugin, where the repository sits
  behind a port. `architecture-choice` settles which family applies before either.

## Template(s) — SQLAlchemy Core, asyncpg, Alembic

```
src/myapp/postgres/
├── __init__.py            # re-exports the repository class, the settings and the engine factory
├── metadata.py            # the one MetaData, carrying the naming convention
├── postgres_settings.py   # this package's own settings class
├── engine.py              # the engine factory
├── foo_table.py           # the Table definitions
└── foo_repository.py      # the class that owns each write's transaction and builds its statements

alembic.ini                # only where this service owns the schema — `flat-project-setup`
migrations/                # only where this service owns the schema
└── postgres/
    ├── env.py             # laid once — `flat-project-setup`
    ├── script.py.mako
    └── versions/          # one revision per schema change
```

A second store adds one sibling package, `src/myapp/<store>/`, and — only where its schema is
versioned — one sibling migration directory, `migrations/<store>/`, and edits neither of the first's;
`<store>` is that store's technology name — `clickhouse`, `mongodb`, `opensearch` (rule 5).

The full file templates live in three topic files beside this one, one per group of artifacts in that
layout. Only this file is loaded automatically, so open the one you need:

- **Read `SETUP.md`** before writing the metadata module, the settings class, the engine factory or a
  migration revision — it binds rules 3, 4, 5 and 6, and `persistence` rules 7, 19 and 20.
- **Read `TABLE.md`** before defining a table, a column or a key — it binds rule 2, and `persistence`
  rules 7, 9 and 13.
- **Read `REPOSITORY.md`** before writing the repository class, its error translator, its row mapper or
  a write that spans statements — it binds rules 1 and 7, and `persistence` rules 1, 2, 4–8 and
  15–17, and says in prose what `persistence` rule 21 comes to on this stack.

## Other bindings

- **The ORM (declarative mapping plus a session).** Mapped classes replace the table objects and the
  session replaces the connection; the declared transaction owner, the driver-error translation with its
  mandatory fallback, the row mapping, the constraint-name contract and the factory-built engine are all
  unchanged. What you give up is the thing the primary binding is chosen for: with Core the SQL that runs
  is the SQL in the file, so a write's cost is readable at the call site and lazy loading cannot appear
  behind an attribute access. A batched write is where this bites (`persistence` rule 21) — an ORM
  project writes it with the session's own bulk-insert API, never as mapped objects saved in a loop.
- **Another engine or driver.** The dialect-specific column types, the driver exception the translator
  matches on and the read-back clause all change together; which rules bind, and how a backend with no
  conflict clause resolves one, are `persistence`'s (its precondition table, rules 15–17).
- **Another store's migration tool.** A store whose schema is versioned keeps its history in
  `migrations/<store>/` and applies it with a tool that already speaks that store — a multi-database
  runner such as `golang-migrate` or Flyway, or the store's own — as a deploy step beside
  `alembic upgrade head`. The directory, the deploy-step ordering and the expand-then-contract discipline
  of `persistence` rule 19 are unchanged; only the file format and the command differ.
- **This package as a separate distribution, shared by several others.** The templates are unchanged,
  the settings class in `SETUP.md` included — it is already this component's own. What changes is where
  its prefix comes from: no longer one service's stem but the shared package's own
  (`MYSCHEMA_POSTGRES_`), because every dependant now reads the same variables and none of them owns the
  component. It also gains its own migration command run from its own directory, and a standing
  restriction that the distributions importing it define no table of their own (`python-workspace`).
- **A platform that supplies one connection URL.** The class in `SETUP.md` holds one secret-typed `url`
  field in place of the five connection fields. A validator on the raw input, before the secret type wraps
  it, normalizes the URL to what the async driver accepts — its scheme, and the query parameters it spells
  differently (`sslmode` becomes asyncpg's `ssl`, or the first connection fails) (`python-settings`
  rule 12); `dsn` returns it, so no consumer changes. The deployment maps the platform's `DATABASE_URL`
  onto `MYAPP_POSTGRES_URL`, in its own declaration where the repository holds one (`python-settings`
  rule 2).

## Rules

1. **No `Protocol` over the datastore** — `flat-layered` rule 3, whose sticky dependency it is.
2. **Every surrogate key this service mints is a time-ordered identifier minted application-side by one
   function every table shares.** A random identifier scatters rows inserted together across the index
   for no benefit, and a database-side default means the writer cannot know the id it just created
   without reading it back. One table diverging onto a different scheme splits the schema's id policy in
   two.
3. **The engine is built by a factory that takes the connection string**, called by the process
   definition and never by a module in this package (`flat-entrypoint` rule 14; never at import,
   `python-packaging` rule 8).
4. **Where several distributions share a store, exactly one of them owns its schema and its migration
   history** (`python-workspace` rule 3). A service reading a store it does not own follows
   `persistence`'s schema-ownership row, and its suite creates that schema from its metadata
   (`flat-test-integration-setup`).
5. **Two stores never share a package, a settings class or a migration history; each store's package
   is named for its technology (`postgres/`, `clickhouse/`) and has its own connection factory:** they
   differ in which of `persistence`'s rules bind, in their drivers' failure types and in how their
   schema changes, and one package holding both turns every one of those differences into a
   branch inside it. Work that writes to both is handed both packages' objects by the process
   definition, like any other dependency, and a unit writing to both is made whole by retrying it to
   completion, each write idempotent by its key (`persistence` rule 3).
6. **A store's migration history is data at the distribution root, one directory per store named for
   it — never inside the package under `src/` — and it ships with whatever applies it.** A built
   distribution carries the package and not the root, so the deployable that runs migrations carries the
   directory itself: an image copies `migrations/` beside the installed package, or the migration job
   runs from the source tree. A hand-written runner, where `persistence` rule 19 calls for one, lives in
   that store's data-access package and takes the migration directory as a parameter rather than finding
   it through the package's import path.
7. **Each repository class builds its own statements from its own declared type.** What several
   classes in one package share is the store's — the driver-error translation (`persistence` rule 5) —
   never a write helper taking a table, rows as mappings and conflict columns, which moves every class's
   statement out of the class that owns it and its rows back to untyped mappings.

## Hard stops

- The relational migration environment or a baseline revision is being laid → stop, use
  `flat-project-setup`; this skill owns the revisions that follow it.
- The service has business invariants that must outlive a change of datastore → stop, this family is the
  wrong one; `architecture-choice` decides, and the repository goes behind a port (`hex-persistence`, in
  the `pyhouse-hex` plugin).
