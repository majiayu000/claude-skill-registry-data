---
name: database-design
description: Use when designing a new schema, writing a migration, adding or auditing indexes, reviewing query performance, choosing between hard delete and soft delete, or establishing database conventions for a project.
---

# Database Design

## Overview

Define the project's schema conventions and migration safety policy *before* migrations land in production. Outputs `.forge/database-design.md` (naming, FK rules, audit columns, soft-delete policy, index strategy, partition strategy, RLS/tenant-scoping rules) and `.forge/migrations-policy.md` (reversibility, idempotency, locking-aware patterns, the query-review checklist). Consumed by `architecture-and-contracts` and `incremental-implementation`.

## When to Use

- A new project starts and the schema is being designed
- A migration is being written that touches a table >1M rows
- An ORM is generating N+1 queries in a hot path
- An audit reveals tables with no FK constraints or missing indexes
- The team is debating soft delete vs hard delete and there's no policy
- A production query is timing out and there's no EXPLAIN process

## When NOT to Use

- Adding a column to a tiny dev-only table where conventions already apply
- Schema-less stores (Mongo, DynamoDB) — see `architecture-and-contracts` data-model section instead
- A migration on an existing project that has documented conventions and the change is local

## Common Rationalizations

| Thought | Reality |
|---------|---------|
| "We can add indexes later" | Missing indexes in production cause outages, not slowdowns. A full table scan on a 50M-row table locks the DB. |
| "Soft delete is always better" | Soft delete without a cleanup job becomes data hoarding. GDPR forces real deletion eventually. |
| "ORMs handle it" | ORMs generate N+1 queries by default. Lazy loading + a loop = production incident. |
| "One big migration is fine" | Irreversible migrations are deployment landmines. Forward-only with a long expand-contract window is the safe path. |
| "We don't need FK constraints, the app enforces it" | The app has bugs. The DB doesn't. FK constraints are the last line of defense against orphan rows. |
| "Let's just denormalize for speed" | Denormalization without a sync job creates two sources of truth that diverge. |

## Red Flags

- `ALTER TABLE large_table ADD COLUMN ... NOT NULL` with no locking review
- Foreign key columns without indexes
- A migration that drops or renames a column without a deprecation window
- Soft delete columns (`deleted_at`) with no cleanup or RLS policy
- ORM `findAll()` followed by `.map(item => item.related)` (N+1)
- A query that scans rows without an EXPLAIN run
- No `created_at` / `updated_at` audit columns
- Multi-tenant tables without RLS or `tenant_id` indexes

## Core Process

### Step 1: Define naming conventions

Write these to `.forge/database-design.md`:
- Tables: `snake_case`, plural (`users`, `task_assignments`)
- Columns: `snake_case`, no abbreviations (`created_at` not `cr_at`)
- Primary keys: `id` (UUIDv7 preferred — sortable, no hot shards)
- Foreign keys: `<table_singular>_id` (`user_id`, `task_id`)
- Indexes: `idx_<table>_<columns>`
- Constraints: `chk_<table>_<rule>`, `unq_<table>_<columns>`
- Audit columns required on every business table: `created_at`, `updated_at` (timestamptz, server-set)

### Step 2: Audit existing schema (if applicable)

Run a check: every FK has an index? every business table has audit columns? every soft-delete table has cleanup? Record violations in `.forge/database-design.md` with an owner and a deadline.

### Step 3: Set migration guardrails

In `.forge/migrations-policy.md`:
- **Reversibility:** every migration has an explicit `down`. Forward-only migrations require an ADR.
- **Idempotency:** `CREATE TABLE IF NOT EXISTS`, `ADD COLUMN IF NOT EXISTS`, `CREATE INDEX IF NOT EXISTS`.
- **Locking-aware:** `CREATE INDEX CONCURRENTLY` on Postgres. Online schema change (gh-ost, pt-osc) for MySQL on large tables. Never `ALTER TABLE` with `ACCESS EXCLUSIVE LOCK` during business hours.
- **Expand-contract pattern:** add new column → backfill → switch reads → drop old column over multiple deploys.
- **Backup before destructive:** any `DROP COLUMN`, `DROP TABLE`, `TRUNCATE`, or destructive `UPDATE` requires a snapshot reference in the PR.

### Step 4: Write the query-review checklist

Append to `.forge/database-design.md`:
- Every hot-path query has been EXPLAINed (Postgres) or `EXPLAIN ANALYZE`d
- No sequential scan on a table >100k rows
- No N+1 — verify with query logs in a test that simulates the loop
- Index used for every JOIN and WHERE condition
- LIMIT used on any user-facing list query
- Pagination uses cursor (not OFFSET) for large tables

### Step 5: Identify partition candidates

Tables likely to exceed 100M rows (events, logs, audit, time-series): plan partitioning *before* they grow. Document the partition key (usually `created_at` range or `tenant_id` hash) and the retention/cleanup job.

### Step 6: Document RLS / tenant-scoping rules

For multi-tenant systems:
- Every business table has `tenant_id` and a Row-Level Security policy
- Application-side defense (every query filters by `tenant_id`) + DB-side defense (RLS) — both, not either-or
- The contract from `architecture-and-contracts` MUST specify which tables are tenant-scoped

### Step 7: Headers

Prepend a `forge:meta` header on both `.forge/database-design.md` and `.forge/migrations-policy.md` (co-output — both share the same `depends_on` + `generated_from`): `generated_by: database-design`, `generated_at: <ISO 8601 UTC with Z>`, `depends_on: [.forge/architecture.md]` — paths only, never hashes, `generated_from: {.forge/architecture.md: <upstream content_hash AT generation time>}`, `content_hash: <sha256 first 8 of THIS file's body>` (each file computes its own). See [forge-dependency-graph](../../references/forge-dependency-graph.md).

## Verification

- [ ] `.forge/database-design.md` written with naming conventions, soft-delete policy, partition strategy
- [ ] `.forge/migrations-policy.md` written with reversibility, idempotency, locking-aware rules
- [ ] Every migration in the codebase is idempotent (`IF NOT EXISTS` or equivalent)
- [ ] Every FK has an index (verified via schema query)
- [ ] Every business table has `created_at` and `updated_at`
- [ ] Every hot-path query has an EXPLAIN attached to the PR (or linked in `.forge/database-design.md`)
- [ ] No migration drops user-visible data without an ADR
- [ ] Multi-tenant tables have RLS policies and `tenant_id` indexes
- [ ] N+1 queries are gone from the codebase (verified by query-count test in CI)
