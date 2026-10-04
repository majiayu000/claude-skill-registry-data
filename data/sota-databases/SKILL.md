---
name: sota-databases
description: >-
  State-of-the-art database engineering rules (2026) for designing, building,
  and auditing data layers. Covers engine selection, schema modeling,
  migrations, query and index craft, transactions and concurrency, reliability
  and scale, security, and vector/AI workloads. Use when designing a new data
  layer, writing or reviewing schemas/migrations/queries, debugging slow or
  contended database workloads, or auditing an existing database for
  correctness, performance, and security. Not for ETL or streaming data
  pipelines — use sota-data-engineering. Trigger keywords: database, SQL,
  Postgres, schema, migration, index, query, ORM, transaction, NoSQL, Redis,
  vector DB, pgvector, replication, partitioning, connection pool, RLS,
  EXPLAIN, deadlock, sharding, caching, SurrealDB, SurrealQL, Qdrant,
  multi-model, graph database.
---

# SOTA Databases

Expert-level rules for the full lifecycle of a data layer: choosing an engine,
modeling data, evolving schemas safely, writing efficient queries, handling
concurrency, operating reliably at scale, securing data, and supporting
vector/AI workloads. Postgres is the reference engine; rules call out where
other systems (MySQL, Redis, document/columnar/vector stores) differ.

This skill operates in two modes. Determine the mode from the user's intent,
then load the relevant `rules/` files per the index below. Do not load all
files preemptively — pick by task.

## BUILD mode

Use when designing or implementing: new schemas, migrations, queries, ORM
layers, caching, job queues, or database infrastructure.

1. **Engine and model first.** Read `rules/01-choosing-and-modeling.md` before
   writing any DDL. Default to Postgres unless a rule there says otherwise.
2. **Every schema change is a migration.** Never hand the user raw DDL to run
   ad hoc; produce migration files following `rules/02-schema-migrations.md`
   (expand/contract, lock-aware, reversible-or-documented).
3. **Design indexes with the queries, not after.** When writing a query that
   will run in production, state which index serves it. Follow
   `rules/03-queries-and-indexes.md`.
4. **State the concurrency story.** For any write path: idempotency, isolation
   level, locking strategy, retry behavior (`rules/04-transactions-concurrency.md`).
5. **Operational defaults are part of the design.** Pooling, backups,
   monitoring hooks, and retention are not "later" items
   (`rules/05-reliability-and-scale.md`, `rules/06-security-and-compliance.md`).
6. Prefer boring, well-trodden patterns. Novelty in the data layer is a cost,
   not a feature.

## AUDIT mode

Use when reviewing an existing schema, migration set, query workload, ORM
usage, or database configuration.

Procedure:
1. Inventory: engine + version, schema (tables, indexes, constraints),
   migration tooling, ORM, pooling setup, backup/replication config.
2. Load the rules files matching what exists (e.g., no vectors → skip 07).
3. Check each rule; report deviations as findings. Verify claims against the
   actual schema/queries — never report a finding you have not confirmed in
   the code or DDL.

Severity conventions:
- **CRITICAL** — data loss, corruption, or breach is likely or already
  possible: untested/missing backups, SQL injection, unconstrained deletes,
  missing FK causing orphaned money/auth rows, RLS bypass, plaintext secrets.
- **HIGH** — production incident waiting to happen: non-CONCURRENT index on a
  hot table, table rewrite migration without expand/contract, missing unique
  constraint under concurrent writes, unbounded long transactions, no
  lock_timeout in migrations, offset pagination on large tables in hot paths.
- **MEDIUM** — correctness or performance debt: N+1 queries, SELECT *, missing
  composite index for a known query, soft delete without partial indexes,
  natural primary keys, missing updated_at/audit trail where required.
- **LOW** — hygiene: naming inconsistencies, missing comments on cryptic
  columns, redundant indexes, suboptimal types (e.g., varchar(255) cargo cult).

Finding format (one per finding):
```
[SEVERITY] <short title>
Where: <file:line | table/column | migration id>
Rule: <rules file + rule heading>
Evidence: <the offending DDL/SQL/code, quoted>
Impact: <what breaks, when, under what load>
Fix: <concrete change — exact SQL/DDL/code where possible>
```
Order findings by severity. End with a summary table: count per severity, and
the top 3 fixes by risk-reduction-per-effort.

## Rules index

| File | Read this when... |
|------|-------------------|
| `rules/01-choosing-and-modeling.md` | Picking an engine (SQL vs NoSQL/KV/columnar/time-series/vector); designing tables; deciding normalization, JSONB usage, primary keys, soft deletes, audit/history tables, ledgers and account balances, multi-tenancy, or **how absence is encoded (`NULL`/omitted property vs an in-band sentinel)**. |
| `rules/02-schema-migrations.md` | Writing or reviewing any migration; altering hot tables; planning zero-downtime schema changes; backfills; setting up migration tooling or testing. |
| `rules/03-queries-and-indexes.md` | Writing/reviewing queries or ORM code; reading EXPLAIN ANALYZE; choosing index types or composite column order; pagination; N+1 suspicion; CTEs and window functions. |
| `rules/04-transactions-concurrency.md` | Anything with concurrent writes: isolation levels, locking (FOR UPDATE, SKIP LOCKED, advisory), job queues, idempotency, deadlocks, long transactions, connection pooling. |
| `rules/05-reliability-and-scale.md` | Backups/PITR, replication and read replicas, partitioning, vacuum/bloat, monitoring, capacity planning, sharding decisions, Redis caching patterns and distributed locks. |
| `rules/06-security-and-compliance.md` | DB roles and grants, RLS, encryption at rest/in transit, SQL injection surface, PII columns, data retention and GDPR-style deletion. |
| `rules/07-vector-and-ai.md` | Embeddings, semantic/hybrid search, pgvector vs dedicated vector DBs (incl. Qdrant exposure hardening), embedding model versioning and re-indexing. |
| `rules/08-surrealdb-multimodel.md` | Building on or auditing SurrealDB: DEFINE ACCESS auth, system users and least privilege, parameterized SurrealQL, SCHEMAFULL + PERMISSIONS, capability flags, indexes, multi-model (embed/reference/graph edges), backups. |

## Top 10 non-negotiables

Violations of these are at minimum HIGH severity in AUDIT mode and must not be
introduced in BUILD mode.

1. **Postgres until proven otherwise.** A second datastore needs a written
   reason that Postgres (with JSONB, partitioning, pgvector, LISTEN/NOTIFY)
   cannot meet — not a vibe.
2. **No natural primary keys.** Surrogate keys only: `bigint GENERATED ALWAYS
   AS IDENTITY` internally, UUIDv7 when IDs are exposed or generated
   client-side. Never email, SSN, slug, or composite business fields as PK.
3. **Expand/contract, always.** No migration may break the currently deployed
   application version. Add → migrate code → backfill → contract, as separate
   deploys.
4. **Lock-aware DDL on hot tables.** `CREATE INDEX CONCURRENTLY`, `SET
   lock_timeout`, batched backfills, `NOT VALID` + `VALIDATE CONSTRAINT`.
   Never an unbounded `ALTER TABLE` rewrite or blocking index build on a
   table with traffic.
5. **Constraints in the database, not only the app.** Uniqueness, foreign
   keys, NOT NULL, and CHECK live in the schema. Application-level "validation
   only" uniqueness is a race condition, not a constraint.
6. **Every production query has a known index.** If you cannot name the index
   a query uses (or justify a seq scan), the query is not done. Keyset
   pagination, no `SELECT *`, no N+1.
7. **Idempotent writes on every retryable path.** Unique keys, upserts, or
   idempotency keys — any write that a client, queue, or webhook may retry
   must be safe to execute twice.
8. **A backup that has not been restored is not a backup.** PITR configured,
   restores rehearsed, RPO/RTO stated. Replication is not backup.
9. **Least privilege at the database.** The app role owns no schema, cannot
   DROP, and cannot read tables it does not use. Migrations run as a separate
   role. No superuser connection strings in app config.
10. **Transactions are short.** No network calls, no user waits, no batch
    loops inside a transaction. Long transactions cause bloat, lock queues,
    and replication lag — treat any transaction over ~1s as a design bug.
    (PG17+ `transaction_timeout` is a backstop far above that; it kills the
    session.)
