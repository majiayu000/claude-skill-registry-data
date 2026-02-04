---
name: sql-dao
description: SQL data access best practices for AIRBot reviewers
license: MIT
---

## Mission
- Guard database performance and correctness by enforcing disciplined DAO/DAL patterns.
- Catch regressions that risk outages: unbounded queries, missing indexes, unsafe scripts, or misuse of replicas.

## Query Execution Standards
- Require explicit column selection (`SELECT col1, col2`) rather than `SELECT *`.
- Prefer synchronous flows within `jdbi.inTransaction {}`; avoid mixing suspend calls inside transactions.
- Enforce batching (`@SqlBatch`, `@BatchChunkSize(2000)`) for bulk inserts/updates and chunk large `WHERE IN` arguments (SQL Server limit ~2200 params).
- Validate pagination on read-heavy endpoints; flag unbounded fetches or N+1 loops.
- Ensure blocking annotations (`@BlockingClass`, `@BlockingCall`) exist for DAL/Repo classes and consumers.
- Confirm master vs. replica usage: critical writes/reads hit master; replica lag can reach 30 minutes.

## Indexing & Performance
- Request evidence of supporting indexes for new predicates, sort columns, and pagination keys.
- Encourage use of table aliases/prefixes in JOINs to maintain clarity.
- For new queries, verify index coverage and that `updated_at` timestamps update alongside data mutations.
- Demand UTC handling for timestamps and rely on the database (`CURRENT_TIMESTAMP`) to set them.

## Schema & DDL Expectations
- Ensure PRs document DDL changes and keep migrations incremental/backward compatible.
- Require `created_at`/`updated_at` columns, primary keys, and consider unique constraints where appropriate.
- Prefer `NVARCHAR` over `VARCHAR`; align column nullability with Kotlin model nullability.
- Advocate for foreign keys to avoid orphaned rows and use online/resumable index operations.

## Scripts & Data Ops
- Scripts should live in dedicated packages, run transactional logic in managers/DAL, and treat CLI entrypoints as thin wrappers.
- Verify bulk update scripts log progress, support `mockRun`, wrap per-row mutations in try/catch, and notify stakeholders before production runs.

## Related Stores
- Cosmos DB batches should rely on `BulkExecutor`; discourage ad-hoc parallel loops.
- RedisCache2 usage must reuse clients, keep TTLs under 6 hours, and avoid local caches that cannot be invalidated.

## Tooling Tips
- `Grep` for `SELECT *`, `@SqlBatch`, `inTransaction`, or `AsyncResponse` inside DAO code to ensure patterns align.
- `Read` migration files and DAL implementations to confirm pagination, batching, and index handling.
- `Glob` `*Dao.kt`, `*Repository.kt`, `*Script.kt` to review related data access or scripting changes together.
