---
name: database-migration
description: "Execute database migrations across ORMs and platforms with zero-downtime strategies, data transformation, and rollback procedures. Use when migrating databases, changing schemas, performing data transformations, or implementing zero-downtime deployment strategies."
stacks: [postgresql, mysql, sqlite, nodejs, typescript]
tags: [database, migration, orm, sequelize, typeorm, prisma, zero-downtime, rollback]
metadata:
  model: inherit
---
## Usage

Loaded automatically when its description matches the active task. The body below provides the working context.


## Use this skill when
- Migrating between different ORMs (Sequelize, TypeORM, Prisma)
- Performing schema transformations: adding columns, renaming, changing types
- Moving data between databases or database versions
- Implementing rollback procedures for failed migrations
- Designing zero-downtime deployment strategies for schema changes
- Refactoring data models with backward compatibility constraints

## Do not use this skill when
- The task is unrelated to database migration or schema changes
- You only need query optimization without schema changes — use postgresql skill
- You need database server setup or administration

## Purpose
This skill covers schema and data migrations across major ORMs and databases, with emphasis on zero-downtime strategies, safe rollback procedures, and correct multi-step patterns for breaking changes.

## Capabilities

### ORM Migration Patterns

**Sequelize**: Uses `up`/`down` functions with `queryInterface` methods (`createTable`, `addColumn`, `removeColumn`, `renameColumn`, `changeColumn`). Run with `npx sequelize-cli db:migrate`, rollback with `db:migrate:undo`.

**TypeORM**: Uses classes implementing `MigrationInterface` with `up(queryRunner)` and `down(queryRunner)` methods. `QueryRunner` provides `createTable`, `dropTable`, `addColumn`, `dropColumn` methods. Run with `npm run typeorm migration:run`, rollback with `migration:revert`.

**Prisma**: Schema-first approach — edit `schema.prisma`, then `npx prisma migrate dev --name description` generates and applies the migration SQL. Production deployment uses `npx prisma migrate deploy` (never `migrate dev`).

### Schema Transformation Patterns

**Adding columns safely**: Always provide a `defaultValue` when adding a `NOT NULL` column to an existing table — otherwise the migration fails on populated databases. The `down` migration removes the column.

**Renaming columns (zero-downtime)**: Never rename directly — this is a breaking change. Use the 3-step expand/migrate/contract pattern:
1. Add the new column (both old and new app code can work)
2. Deploy application code that reads from new column, writes to both
3. Backfill data from old column to new column in a migration
4. Deploy application code that only writes to new column
5. Remove the old column in a final migration

**Changing column types**: For large tables, use the shadow column pattern: add a new column of the target type, copy and transform data with a `CAST`, drop the old column, rename the new column. Never use `ALTER COLUMN` type change on large tables in production — it locks the table.

### Data Transformation

**Batch processing**: For large datasets, never transform all rows in a single transaction — this locks the table for the entire duration. Process in batches of 1000-10000 rows with commit between batches to release locks.

**Complex transformations**: Query existing records, apply business logic transformation, and write back with parameterized queries — avoid raw string interpolation in SQL to prevent injection.

**Idempotency**: Write transformations that are safe to re-run — use `WHERE new_column IS NULL` conditions so re-running only processes unprocessed rows.

### Rollback Strategies

**Transaction-based rollback**: Wrap the entire migration in an explicit transaction with commit at the end and rollback on exception. Most DDL operations support transactional execution in PostgreSQL (unlike MySQL).

**Checkpoint/backup rollback**: Create a backup table (`CREATE TABLE users_backup AS SELECT * FROM users`) before destructive migrations. If the migration fails verification, restore from backup and drop the migration artifact.

**Verification step**: After migration, run a verification query (e.g., check for unexpected NULLs in a non-nullable column) before committing. Fail fast rather than letting corrupt data propagate.

### Zero-Downtime Migrations

**Blue-Green strategy** — the 5-phase approach for any breaking change:
1. Add new schema element (backward compatible with current code)
2. Deploy code that writes to both old and new schema
3. Backfill historical data from old to new
4. Deploy code that reads from new schema only
5. Remove old schema element

This ensures no downtime because each deploy is backward compatible with both the schema before and after the deployment.

**Non-breaking changes** that are always safe to apply without a deployment gate: adding nullable columns, adding tables, adding indexes (use CONCURRENTLY in PostgreSQL), adding foreign keys with NOT VALID then VALIDATE separately.

**Breaking changes** that always require a deployment strategy: removing columns, renaming columns, changing column types, adding non-nullable columns without defaults, changing index definitions.

### Cross-Database Compatibility

**PostgreSQL vs MySQL differences**: PostgreSQL supports `JSONB` (preferred over `JSON`), `ARRAY` types, transactional DDL, and `CREATE INDEX CONCURRENTLY`. MySQL uses `JSON` without binary optimization, lacks array types, and has limited transactional DDL. Write dialect-aware migration code using ORM's dialect detection.

**Type mapping**: Match PostgreSQL `JSONB` to MySQL `JSON`; match PostgreSQL `TEXT` to MySQL `TEXT` (not `VARCHAR(255)`); handle timestamp timezone differences explicitly.

## Behavioral Traits
- Always implement a `down` migration for every `up` migration — rollback must be possible
- Test migrations on staging with production-equivalent data before applying to production
- Use transactions wherever the database supports transactional DDL
- Create a backup before any destructive migration in production
- Break large migrations into small, incremental steps that can each be rolled back independently
- Use zero-downtime patterns for all schema changes in production systems with active traffic

## Important Constraints
- **Never `migrate dev` in production** — Prisma's `migrate dev` drops and recreates the shadow database; use `migrate deploy` in production
- **Test rollback procedures** — a `down` migration that has never been tested is not a rollback strategy
- **NULL values in CHECK constraints** — NULLs pass all CHECK constraints in SQL (three-valued logic); combine with NOT NULL if the check must apply to all rows
- **Foreign key constraints on rename** — drop FK constraints before removing/renaming referenced columns, then recreate after
- **Index creation locking** — use `CREATE INDEX CONCURRENTLY` in PostgreSQL to avoid table locks during index creation on large tables
- **Batch size** — never transform millions of rows in a single transaction; use batched commits to avoid long-running locks

## Best Practices Summary
1. Every `up()` needs a corresponding `down()` — always
2. Test on staging with realistic data volume before production
3. Use transactions for atomic migrations where supported
4. Back up before any irreversible migration in production
5. Break migrations into small, independently reversible steps
6. Monitor for errors during deployment and have a rollback plan ready
7. Document why the migration exists and how to verify it succeeded
8. Write idempotent migrations that are safe to re-run

## Common Pitfalls
- Not testing rollback procedures before production deployment
- Making breaking schema changes without a zero-downtime strategy
- Forgetting to handle NULL values when adding constraints
- Not considering index performance impact of new columns or type changes
- Ignoring foreign key constraints during renames or drops
- Trying to migrate too much data in a single transaction (causes lock timeouts)
