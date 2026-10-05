---
name: mk:database
description: "Design and safely evolve data models, database schemas, migrations, queries, indexes, and ORM data-access boundaries. Use for data-model, migration, query, index, ORM schema, or datastore-selection tasks. Discover the existing engine and migration source before proposing syntax."
version: 2.0.0
argument-hint: '[model|migration|query|index|orm|store] [description]'
source: local
allowed-tools:
  - Bash
  - Read
  - Edit
  - Write
  - Glob
  - Grep
keywords:
  - data-model
  - schema
  - migration
  - query
  - index
  - orm
  - datastore-selection
  - data-invariants
  - backfill
  - recovery
when_to_use: Use when designing a data model, changing a schema, writing or reviewing a migration, diagnosing a slow query, choosing an index, shaping the ORM data-access boundary, or selecting a datastore. NOT for API contracts (mk:api-design-principles), service or handler code (mk:backend-development), infrastructure and deployment (mk:devops), or the security verdict.
user-invocable: true
owner: portability
criticality: high
status: active
runtime: portable
---

# Database

Data invariants first, engine syntax second. Discover what the repository already runs before
proposing anything.

## Ownership

| Owner | Owns | Does NOT own |
|---|---|---|
| `mk:api-design-principles` | Interface contract: resource/type/message shape, error and authorization *requirements*, compatibility and deprecation, consumer discovery | Implementation, persistence, security verdict, release |
| `mk:backend-development` | End-to-end backend change: discovery, classification, service/handler/integration work | Contract authorship, schema/SQL, security verdict, deploy |
| `mk:database` | Data invariants, schema, migration and recovery, query/index evidence, ORM data-access boundary | API contract, authorization verdict, infrastructure execution |
| `mk:devops` | Infrastructure-as-code, containers, CI, runtime config, deployment safety design, rollback, incident diagnosis | Deploy approval and execution, security verdict, code root-cause, schema semantics |

Routing rules — identical in all four skills:

- **Contract-only API question → `mk:api-design-principles`**, even in the middle of a task
  owned by another skill. "Contract" means what a consumer can observe: field set, error
  shape, status semantics, pagination, versioning. Extending an endpoint without changing
  any of those is not a contract change.
- **End-to-end backend change → `mk:backend-development`**, which invokes the API skill only
  when a new, public, or breaking contract is in scope.
- **A message-based change (event, webhook, RPC) splits**: the message contract belongs to
  `mk:api-design-principles`; the producer or consumer implementation belongs to
  `mk:backend-development`.
- **Schema, migration, query, index, or ORM work → `mk:database`.** No other skill writes a
  migration or generic SQL.
- **Infrastructure, containers, delivery, or deployment safety → `mk:devops`.**
- **An unscoped performance request is triaged by evidence, never by guess**:
  `mk:backend-development` locates where the time actually goes, then hands a query or index
  question to `mk:database` and a capacity or runtime question to `mk:devops`. No skill
  invents the target.
- **Code root cause → `mk:investigate`.** `mk:devops` owns the operational picture — what
  changed, where it fails, which signal proves it — and hands the defect over.
- **An auth-sensitive change**: the owning skill states the *requirement*; the security
  workflow owns the verdict.
- **Any production effect → `mk:ship` or a human.**

## Workflow

### 1. Discover the source of truth

Read, in this order, and stop guessing as soon as evidence appears: the dependency manifest,
the schema or model definitions, the migration directory and its tool, the ORM configuration,
the call sites that query, the data tests and fixtures, and the active plan.

Record the engine, its version if the repository states one, the migration tool, and whether
an ORM owns the schema. **There is no default engine.** If the repository does not say, ask —
proposing syntax for the wrong engine wastes the whole answer.

### 2. Classify

| Class | Load |
|---|---|
| Data model or schema change | `references/schema-design.md` |
| Migration, backfill, or recovery | `references/migration-patterns.md` |
| Slow query, index choice, access-path question | `references/query-optimization.md` |
| Datastore or ORM selection | The section below; no reference needed |

### 3. State invariants before syntax

Write these down before a line of schema. Mark anything unknown as unknown rather than
filling it in:

- **Entity and lifecycle** — what it represents, how it is created, changed, and ended.
- **Identity and uniqueness** — what makes a row the same row, and what must never duplicate.
- **Tenancy and authorization boundary** — who may see a row, and where that is enforced.
- **Retention and personal data** — what must be deleted or anonymized, and when.
- **Consistency need** — what must be true at the same instant versus what may converge.
- **Known access patterns** — the reads and writes that actually happen, with rough shape.
- **Performance baseline** — current size and timing, when the task is about performance.

An invariant nobody can state is the finding. Report it.

### 4. Design proportional to the evidence

Model the invariants, then let the engine's capabilities shape the syntax. Normalize or
denormalize only with a stated query, consistency, or evolution rationale — never
speculatively, in either direction. Choose an index from the filter, join, and ordering
evidence gathered above, weighed against its write cost; an index with no query behind it is
overhead.

Follow the naming, key, and timestamp conventions the repository already uses. Where a
convention is absent, propose one and say it is a proposal.

### 5. Evolve safely

For any change to a table that already holds data, state: compatibility with the code that
is currently running, the locking or runtime behavior on this engine at this size, the
backfill approach if one is needed, the signal that proves it worked, and the recovery path
— a reverse migration **or** a documented forward recovery.

An expand → migrate/backfill → contract sequence fits most non-trivial changes on a live
table. Use it where it fits; say why when it does not.

Never run a reset, drop, backfill, or migration against a live or production database.
Prepare it and hand execution to `mk:ship` or a human.

### 6. Validate and hand off

Validate on a disposable database with synthetic, non-personal fixtures. Copying production
data into another environment is a data-protection decision for the user, not a testing
technique to recommend.

Hand off with: engine evidence, invariants, the change, the migration and its recovery path,
the query/index evidence, and what remains unproven.

## Datastore and ORM selection

Only when the project is greenfield or the user explicitly asks to change stores.

Decide from the invariants in step 3, not from familiarity: the shape of the data and its
relationships, the consistency requirement, the read and write patterns, the operational
capability the team actually has, and what the rest of the system already runs. Adding a
second store adds a second operational burden — it needs a reason beyond convenience.

An ORM is a data-access boundary, not the data model. Keep the invariants expressed in the
database where the database can enforce them, let the ORM express access, and expect to drop
to the query language for anything the ORM shapes badly. Whichever the repository already
uses is the one to use.

## Security constraint

Never build a query by string interpolation or template concatenation. Use the parameter
mechanism the driver or ORM provides — this is a blocked pattern, not a style preference.

Never log, print, or copy personal data while investigating. A row that reproduces a bug can
be described by its shape.

## References

| File | Load when |
|---|---|
| `references/schema-design.md` | Modelling entities, keys, relationships, tenancy, or constraints |
| `references/migration-patterns.md` | Changing a table that holds data; backfills; recovery |
| `references/query-optimization.md` | A query is slow, or an index decision needs evidence |

## Gotchas

Each is conditional on the engine the repository actually runs. Confirm the engine before
applying one.

- **Adding a `NOT NULL` column without a default can rewrite the whole table.** On
  PostgreSQL before 12 it takes an exclusive lock for the rewrite. Add the column nullable,
  backfill in batches, then add the constraint — on PostgreSQL 12 and later that final step
  is a validating scan, not a rewrite. Other engines differ; check yours.
- **A plain index build blocks writes on PostgreSQL.** The concurrent form avoids it but
  cannot run inside a transaction block and can leave an invalid index if it fails. Other
  engines have their own online-DDL rules — MySQL's depend on the algorithm chosen, and
  SQLite rewrites the table for most schema changes.
- **Cascading delete removes child rows with no error.** Audit every cascading foreign key
  before any bulk delete, in any engine that supports them.
- **The analysing form of `EXPLAIN` executes the statement.** Never run it on an
  `INSERT`/`UPDATE`/`DELETE` outside a transaction you will roll back; plain `EXPLAIN` is the
  safe form for a mutating statement.
- **Pool exhaustion looks like a slow query, not a pool error.** Callers wait until a
  timeout fires while connections sit idle in an open transaction. Check for connections
  held past their work before optimizing the query.
- **A default isolation level of read-committed permits non-repeatable reads** — two reads in
  one transaction can disagree. Financial and inventory logic needs a stricter level, chosen
  explicitly. Engines differ in their default and in what each level actually guarantees.
- **SQLite serializes writers and rewrites tables for most `ALTER`s.** That is fine for its
  intended workloads; it only becomes a problem where write concurrency or online DDL is
  required. Do not treat it as a reason to propose a different engine.
