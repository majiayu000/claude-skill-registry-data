---
name: coding-pg
description: >-
  Use for PostgreSQL 18 SQL, migrations, DDL, functions, RLS policies,
  indexes, query plans, extensions, and SQL embedded in TypeScript via
  @effect/sql-pg. Enforces set-algebraic queries, schema-level invariants,
  current PostgreSQL features, extension-first design, tenant security,
  observability, and migration safety.
---

# [H1][CODING-PG]
>**Dictum:** *PostgreSQL schema design, query algebra, and security posture govern all SQL work.*

All SQL follows five governing principles:
- **Polymorphic** — one function/query per concern, generic over specific via parameter dispatch and dynamic SQL
- **Set-algebraic** — express operations as set transformations; zero row-at-a-time iteration
- **Strongly typed** — domain types, composite types, range types; zero untyped `text` columns for structured data
- **Programmatic** — variable-driven predicates, parameterized DDL, zero stringly-typed identifiers
- **Declarative-first** — constraints, generated columns, and RLS policies enforce invariants at the schema level; application logic is last resort
- **Source-current** — PostgreSQL 18/current docs are the truth baseline; examples must state current semantics, not stale point-version folklore


## Paradigm

- **Immutability**: append-only event tables, temporal versioning via `tstzrange` + `WITHOUT OVERLAPS`, soft-delete via `archived_at` timestamp — zero in-place mutation of historical records
- **Type anchoring**: one `CREATE TYPE` or `CREATE DOMAIN` per semantic concept — derive column declarations from domain types, never redeclare equivalent `CHECK` constraints across tables
- **Expression control flow**: `CASE`-free query design via `COALESCE`, `NULLIF`, `GREATEST`/`LEAST`, lateral joins, and `FILTER (WHERE ...)` — reserve `CASE` for irreducible multi-branch projection only
- **Set composition**: CTEs as named relational algebra steps; `UNION ALL` over procedural accumulation; `MERGE` over conditional INSERT/UPDATE sequences
- **Constraint-driven integrity**: `CHECK`, `EXCLUDE`, `WITHOUT OVERLAPS`, `GENERATED ALWAYS AS` — push validation into DDL; application-layer checks are redundant defense, not primary enforcement
- **Extension-first**: pgvector for embeddings, pg_trgm for fuzzy search, PostGIS for spatial, TimescaleDB for time-series — never hand-roll what an extension provides


## Conventions

| Layer          | Mechanism                         | Owns                                                           |
| -------------- | --------------------------------- | -------------------------------------------------------------- |
| Identity       | `uuidv7()`                        | PK generation — timestamp-ordered, B-tree friendly             |
| Temporal       | `WITHOUT OVERLAPS` + `PERIOD`     | Range integrity — temporal PKs, FKs, exclusion constraints     |
| Projection     | Virtual generated columns         | Computed fields — zero storage, instant `ALTER TABLE`          |
| Write strategy | `MERGE ... RETURNING OLD/NEW`     | Upsert + audit trail in single statement                       |
| Type safety    | Domain types + composite types    | Semantic column typing — branded scalars, structured records   |
| Search         | GIN + pg_trgm / pgvector          | Full-text, trigram similarity, vector nearest-neighbor         |
| Partitioning   | Declarative + pg_partman          | Time/hash/list partitioning with automatic lifecycle           |
| Scheduling     | pg_cron                           | In-database job scheduling — maintenance, materialized views   |
| Security       | RLS + SECURITY INVOKER            | Row-level tenant isolation, least-privilege function execution |
| Observability  | pg_stat_statements + auto_explain | Query fingerprinting, automatic slow-query plan capture        |

- Effect-SQL (`@effect/sql` + `@effect/sql-pg`) is the assumed TypeScript integration layer.
- `Model.Class` field modifiers (`Generated`, `FieldOnly`, `FieldExcept`, `Sensitive`) must align with DDL constraints — `Generated` fields map to `DEFAULT` or `GENERATED ALWAYS AS` columns.
- All SQL identifiers use `snake_case`; TypeScript receives `camelCase` via `transformResultNames`.


## Contracts

**Type discipline**
- One domain type per semantic concept; column declarations reference the domain, never inline `CHECK` constraints.
- Composite types for structured return values from functions — never `OUT` parameter proliferation.
- Range types (`tstzrange`, `int4range`, custom) for interval semantics — never dual `start`/`end` columns.
- `NOT NULL` is default posture; nullable columns require documented justification.

**Query algebra**
- CTEs for named intermediate results; recursive CTEs with `SEARCH BREADTH FIRST` or `CYCLE` for graph traversal.
- `MERGE` with `RETURNING OLD.*, NEW.*, merge_action()` for write-audit fusion.
- Window functions with `GROUPS`/`EXCLUDE` framing where row-count framing is insufficient.
- `JSON_TABLE` / `jsonb_path_query` for structured JSON extraction — never application-side JSON parsing of database-resident JSON.
- `LATERAL JOIN` for correlated subquery materialization — never scalar subqueries in SELECT list.

**Index strategy**
- Every `WHERE` clause pattern has a corresponding index; partial indexes for selective predicates.
- `INCLUDE` columns for index-only scans on high-frequency read paths.
- GIN for JSONB containment (`@>`), array overlap (`&&`), full-text (`@@`).
- GiST for range overlap, spatial queries, nearest-neighbor when combined with `ORDER BY <-> LIMIT`.
- BRIN for append-only monotonic columns (timestamps, serial IDs) — orders of magnitude smaller than B-tree.

**Security**
- RLS enabled on every tenant-scoped table; policies use fail-closed `nullif(current_setting('app.current_tenant', true), '')` tenant scoping.
- Functions default to `SECURITY INVOKER` (always the default); `SECURITY DEFINER` only with `SET search_path = pg_catalog, public`.
- Column-level `GRANT` for sensitive fields — never rely on view-based column hiding alone.

**Performance**
- `EXPLAIN (ANALYZE, BUFFERS, VERBOSE, SETTINGS)` is the verification tool; assertions against plan shape, not just row counts.
- AIO (`io_method = io_uring`) for sequential scan and vacuum workloads on Linux.
- Parallel query enabled for aggregation, hash join, index scan — `max_parallel_workers_per_gather` tuned to workload.
- `FOR UPDATE SKIP LOCKED` for concurrent batch processing — never `SELECT ... FOR UPDATE` without `SKIP LOCKED` on queue tables.


## Anti-Patterns

| Label                         | Symptom                                                                        |
| ----------------------------- | ------------------------------------------------------------------------------ |
| STRING_TYPING                 | `text` for structured data (JSON, enum values, composite structures)           |
| DUAL_COLUMN_RANGE             | `start_date`/`end_date` instead of `tstzrange` with exclusion constraint       |
| IMPERATIVE_BATCH              | PL/pgSQL `LOOP` with row-at-a-time `UPDATE` instead of set-based `MERGE`/CTE   |
| INDEX_SPRAWL                  | Redundant single-column indexes subsumed by existing composite indexes         |
| NULLABLE_DEFAULT              | Columns nullable without documented justification                              |
| TRIGGER_LOGIC                 | Business logic in triggers instead of `MERGE RETURNING` or generated columns   |
| OFFSET_PAGINATION             | `LIMIT/OFFSET` instead of keyset pagination for client-facing endpoints        |
| SECURITY_DEFINER_LEAK         | `SECURITY DEFINER` without `SET search_path` — search_path injection vector    |
| STRINGLY_POLICY               | RLS policy with hardcoded literals instead of `current_setting()`              |
| FUNCTION_PROLIFERATION        | Separate functions for each query variant instead of one polymorphic function  |
| APPLICATION_SIDE_JSON         | Fetching raw JSONB and parsing in application instead of `jsonb_path_query`    |
| MANUAL_PARTITION              | Hand-written partition creation instead of pg_partman lifecycle management     |
| UNVALIDATED_CONSTRAINT        | `ADD CONSTRAINT ... NOT VALID` without subsequent `VALIDATE CONSTRAINT`        |
| IF_THEN_DISPATCH              | PL/pgSQL `IF p_op = 'get' THEN ... ELSIF` instead of VALUES-based dynamic SQL  |
| NONCOMPOSABLE_CAGG            | `PERCENTILE_CONT` in hierarchical CAGG; non-composable across tiers            |
| LEGACY_UUID                   | Non-ordered UUID generation on new ordered PKs where `uuidv7()` fits better    |
| STALE_HEALTH_VIEW             | Materialized views for real-time health monitoring instead of inline queries   |
| EXCLUDE_OVER_WITHOUT_OVERLAPS | EXCLUDE instead of WITHOUT OVERLAPS PK/UNIQUE for temporal overlap in PG 18    |
| RAW_UUID_ID                   | Raw `S.UUID` for PK/FK instead of `S.UUID.pipe(S.brand('EntityId'))`           |
| BARE_FOR_UPDATE               | `FOR UPDATE` without `SKIP LOCKED` on batch/queue processing patterns          |
| NULL_UNSAFE_ANTIJOIN          | `NOT IN (SELECT ...)` instead of `NOT EXISTS`; NULL in subquery yields UNKNOWN |
| DISTINCT_OVER_EXISTS          | `SELECT DISTINCT` on joined data; use `EXISTS` semi-join (avoids sort/dedup)   |


## Load Sequence

**Foundation** (always load):
- `references/validation.md` — compliance checklist, Effect-SQL alignment, migration safety

**Task-routed references** (load when the task matches):
- `references/ddl.md` — schema design, domain/composite/range types, temporal constraints, generated columns, partitioning, lock levels
- `references/queries.md` — CTE algebra, MERGE, window functions, JSON_TABLE, recursive patterns
- `references/indexes.md` — index type selection, partial indexes, covering indexes, maintenance
- `references/functions.md` — polymorphic functions, custom aggregates, procedures, PL/pgSQL dispatch
- `references/extensions.md` — load when: pgvector, pg_trgm, PostGIS, TimescaleDB, pg_cron, pg_partman, pg_duckdb, embeddings, similarity search, time-series, spatial, partitioning automation, analytics, OLAP, analytical
- `references/security.md` — load when: RLS, row-level security, tenant isolation, privileges, audit, pgaudit
- `references/observability.md` — load when: monitoring, statistics, auto_explain, wait events, lock contention
- `references/performance.md` — load when: tuning, io_uring, JIT, parallel query, vacuum, SSD, NVMe, EXPLAIN
- `references/replication.md` — load when: replication, publications, subscriptions, conflict tracking, CDC


## First-Class Extensions

| Extension            | Owns                                                  | Load When                               |
| -------------------- | ----------------------------------------------------- | --------------------------------------- |
| `pgvector`           | Vector storage, HNSW/IVFFlat/DiskANN indexes          | Embedding search, similarity queries    |
| `pgvectorscale`      | DiskANN index, Statistical Binary Quantization        | >1M vectors, memory-constrained         |
| `pg_search`          | BM25 full-text via Tantivy, `@@@` operator            | Search-quality ranking, hybrid search   |
| `pg_trgm`            | Trigram similarity, GIN trigram indexes, `%` operator | Fuzzy text search, typo tolerance       |
| `PostGIS`            | Geometry/geography types, spatial indexes, ST_* funcs | Geospatial queries, proximity search    |
| `TimescaleDB`        | Hypertables, continuous aggregates, compression       | Time-series ingestion, rollup queries   |
| `pg_cron`            | In-database scheduled jobs                            | Materialized view refresh, maintenance  |
| `pg_partman`         | Partition lifecycle management                        | Non-time-series partitioning            |
| `pg_duckdb`          | Embedded DuckDB, analytical acceleration, lake access | OLAP queries, Parquet/Iceberg reads     |
| `pg_jsonschema`      | JSONB validation via JSON Schema CHECK constraints    | Structured JSONB columns                |
| `btree_gist`         | GiST equality operators for EXCLUDE constraints       | Range + equality exclusion constraints  |
| `bloom`              | Bloom filter index for wide-table equality            | >5 columns, arbitrary WHERE combos      |
| `pg_stat_statements` | Query fingerprinting, execution statistics            | Performance analysis, regression detect |
| `pgaudit`            | Compliance-grade audit logging (session + object)     | SOC 2, HIPAA, PCI-DSS compliance        |


## Validation Gate

After writing or modifying SQL, run in order:

1. **Automated lint**: `bash scripts/pg_lint.sh [PATH...]` from this skill directory — anti-pattern detectors (rg-based + structural). Errors (E) block merge; warnings (W) require justification. Supports `--json`, `--sql-only`, `--ts-only`, and `--self-test`.
2. **Manual checklist**: `references/validation.md` — compliance gates not automatable (Effect-SQL alignment, migration safety, lock-level awareness).
