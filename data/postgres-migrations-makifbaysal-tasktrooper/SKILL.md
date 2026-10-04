---
name: postgres-migrations
category: database
description: Use when changing the database schema - detect the repo's migration tool, ship a new migration in its layout, never edit an applied one, and avoid lock-unsafe DDL on a live table
tech_stack: PostgreSQL
source: ankane/strong_migrations (MIT), sbdchd/squawk (MIT/Apache-2.0), wshobson/agents postgresql-table-design (MIT), adapted
---
# PostgreSQL Migrations

## Overview

Migrations are append-only history that must replay identically on every environment, forever. The cardinal sin is editing a migration that has already run somewhere — it makes environments diverge silently. The second most common mistake is DDL that locks a live table for longer than the app can tolerate.

**Core principle:** a wrong migration is fixed by a NEW migration, never by editing the old one; and `rollback_release` reverts code only, so the schema your migration leaves behind must keep working with the previous release's code until a later task removes what it replaced.

## Detect the repo's migration tool first

| Tool | How to recognise it | Down migration | Outside a transaction |
|---|---|---|---|
| golang-migrate | `*.up.sql` / `*.down.sql` pairs | its own `.down.sql` file | each `CONCURRENTLY` statement needs its own migration file (no implicit transaction wrapping across files) |
| goose | `-- +goose Up` / `-- +goose Down` in one file | same file, `Down` section | `-- +goose NO TRANSACTION` directive |
| Flyway | `V<n>__name.sql` | none in the open-source edition | follow Flyway's own non-transactional DDL rules |
| Liquibase | changesets (XML/YAML/SQL) | `rollback` block | per changeset `runInTransaction` |
| Atlas | `atlas.hcl` + versioned migrations | — | — |
| Up-only numbered SQL | plain numbered `.sql` files, no down files (e.g. this repo's own `server/migrations/`) | none exists — don't invent one | — |

Never introduce a different migration tool into a repo that already has one, and never add down files to a repo that has none — follow what's there (rule repo-conventions-win).

## Rules

- **Never edit an applied migration.** History replays; a divergent edit corrupts environments that already ran it. A wrong migration gets a new one that corrects it.
- **Never rely on Hibernate/JPA auto-DDL** (`hbm2ddl=update`, Quarkus schema generation) outside tests — schema comes from migrations only (java-persistence).
- **Idempotent** where it matters: `IF NOT EXISTS`, `ON CONFLICT`, `WHERE` guards on backfills so a re-run does no harm.
- Add an explicit index for every new query path the code introduces — Postgres does not auto-index foreign-key columns.
- Start DDL in a live-table migration with `SET lock_timeout = '5s';` so a blocked `ALTER` fails fast and visibly instead of queueing behind other locks and blocking every other statement on the table.

## Rollback reality: what `rollback_release` actually does

`rollback_release` reverts the application code only — it never runs a down migration. Two consequences:

1. **Expand/contract.** Ship additive changes first (new nullable/defaulted column, new table, dual-write) so the schema works with both the old and new code; drop what's no longer needed in a *later* task once the old code is gone everywhere.
2. **`rollback_plan` must say whether the down migration is actually safe to run**, because by the time anyone reaches for it, the new schema may already hold data the down migration would silently drop. Write what you'd tell the human, e.g. *"Migration 045 is additive; reverting the code is enough. Do NOT run its down migration — it drops the `priority` column and any values written to it since deploy."* A migration that is purely additive needs no down-migration caveat at all; say that instead.
3. **golang-migrate caveat:** if a commit is reverted and that removes migration 045's files, a database already at version 45 then fails `migrate up` with "no migration found for version 45" — decide whether to keep the schema (most common) and run `migrate ... force 44` to re-sync the tool's bookkeeping, rather than trying to re-apply a file that no longer exists.

## Lock-safety: unsafe vs safe DDL on a live table

| Change | Unsafe (locks / rewrites the table) | Safe |
|---|---|---|
| Add index | `CREATE INDEX` | `CREATE INDEX CONCURRENTLY IF NOT EXISTS` (its own migration, outside a transaction) |
| Foreign key | `ADD CONSTRAINT ... FOREIGN KEY ...` (validates existing rows under lock) | `... NOT VALID`, then `VALIDATE CONSTRAINT` in a later migration |
| `NOT NULL` on an existing column | `ALTER COLUMN ... SET NOT NULL` (full scan under lock on PG <12) | `CHECK (col IS NOT NULL) NOT VALID` → `VALIDATE CONSTRAINT` → `SET NOT NULL` (PG ≥12 skips the re-scan once validated); PG 18 also has `SET NOT NULL ... NOT VALID` directly |
| Add column | A volatile default (`DEFAULT now()`, `DEFAULT random()`) rewrites the table | A constant default is metadata-only since PG 11; for a volatile default, add the column nullable, backfill, then add the default/constraint |
| Change column type | `ALTER COLUMN ... TYPE ...` (table rewrite) | New column + backfill + switch reads/writes, drop the old one later |
| Rename or drop column/table | `RENAME` breaks the previous release's code immediately | Expand/contract: add the new name, dual-write/read, switch, drop later |
| Backfill existing rows | A single large `UPDATE` (long lock, huge transaction) | Batched `UPDATE ... WHERE id IN (SELECT id FROM t WHERE ... LIMIT 5000)`, looped, outside the DDL transaction |

## Types and keys (new tables; existing tables follow the repo's own conventions)

`timestamptz` (never bare `timestamp`); `text` with a `CHECK` constraint instead of `varchar(n)`; `bigint generated always as identity` or `uuid DEFAULT uuidv7()` (PG 18+, time-ordered) / `gen_random_uuid()`; `numeric` for money, never `float`/`money`; `UNIQUE NULLS NOT DISTINCT` where NULL should count toward the uniqueness check (PG 15+).

## Worked Example

Adding a required `priority` column with an index, on golang-migrate:

```sql
-- 043_task_priority.up.sql
ALTER TABLE tasks ADD COLUMN priority TEXT NOT NULL DEFAULT 'medium';

-- 043_task_priority.down.sql
ALTER TABLE tasks DROP COLUMN IF EXISTS priority;
```

```sql
-- 044_task_priority_index.up.sql
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_tasks_priority ON tasks (priority);

-- 044_task_priority_index.down.sql
DROP INDEX CONCURRENTLY IF EXISTS idx_tasks_priority;
```

`NOT NULL ... DEFAULT 'medium'` is a constant default: metadata-only on PG 11+, no table rewrite, every existing row reads as `'medium'`. The index is a separate migration because `CREATE INDEX CONCURRENTLY` cannot run inside the transaction golang-migrate wraps each file in. `rollback_plan`: "045/044 are additive; reverting the code is enough, do not run the down migrations unless the column is confirmed unused."

❌ `CREATE INDEX idx_tasks_priority ON tasks (priority);` inside the same migration as the column add — locks the table for the full index build, and squawk's `require-concurrent-index-creation` flags exactly this.

## Verify

- Lint: `npx --yes squawk-cli <new-file>.sql` (or `pip install squawk-cli`) — fix or explicitly justify every warning it raises (rule IDs like `require-concurrent-index-creation`, `constraint-missing-not-valid`, `adding-required-field`, `changing-column-type`, `renaming-column`, `ban-drop-column`, `prefer-identity`, `prefer-text-field`, `prefer-timestamptz`, `require-timeout-settings` double as a checklist even without running the tool).
- Apply up → down → up (or the repo's own migration test) against a disposable `postgres:18` container before calling it done.
- `psql -c '\d+ <table>'` to confirm the resulting schema matches what you intended.

## Common Mistakes

- Editing an already-applied migration to "fix" it.
- `CREATE INDEX` (not `CONCURRENTLY`) on a table already receiving traffic.
- A new query path with no supporting index.
- A non-idempotent backfill that double-applies on re-run, or one large `UPDATE` instead of batches.
- `rollback_plan` left blank on a migration task, or claiming the down migration is safe without checking whether data was written since deploy.
- `hbm2ddl`/auto-DDL thinking — schema comes from migrations only.

## Red Flags

- The diff modifies an existing migration file instead of adding a new one.
- A `NOT NULL` or type-change migration with no expand/contract story and no mention in `rollback_plan`.
- A column or table rename with no plan for the previous release's code still running against it.
- `squawk` warnings left unaddressed with no comment explaining why.
