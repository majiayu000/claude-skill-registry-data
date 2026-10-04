---
name: database-migrations
description: Database migration best practices across PostgreSQL, MySQL, and common ORMs (Prisma, Drizzle, Kysely, Django, TypeORM, golang-migrate) — schema changes, data migrations, rollbacks, and zero-downtime deployments.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Database Migration Patterns

Safe, reversible database schema changes for production systems.

## When to Activate

- Creating or altering database tables
- Adding/removing columns or indexes
- Running data migrations (backfills, transformations)
- Planning zero-downtime schema changes
- Setting up migration tooling for a new project

## Core Principles

1. **Every change is a migration** — never modify production databases by hand
2. **Migrations are forward-only in production** — roll back with a new forward migration
3. **Separate schema and data migrations** — don't mix DDL and DML in one migration
4. **Test migrations against production-sized data** — a migration that works on 100 rows can lock up on 10M
5. **Migrations are immutable after deployment** — never edit a migration that has already run in production

## Migration Safety Checklist

Before applying a migration:

- [ ] Migration has both UP and DOWN (or is explicitly marked irreversible)
- [ ] No full-table lock on large tables (use concurrent operations)
- [ ] New columns are nullable or have a default (never add NOT NULL without a default)
- [ ] Indexes are created concurrently (never inline on CREATE TABLE for existing tables)
- [ ] Data backfills are a separate migration from the schema change
- [ ] Tested against a copy of production-sized data
- [ ] Rollback plan documented

## PostgreSQL Patterns

### Adding a Column Safely

```sql
-- GOOD: Nullable column, no lock
ALTER TABLE users ADD COLUMN avatar_url TEXT;

-- GOOD: Column with a default (Postgres 11+ is instant, no rewrite)
ALTER TABLE users ADD COLUMN is_active BOOLEAN NOT NULL DEFAULT true;

-- BAD: NOT NULL without a default on an existing table (forces a full rewrite)
ALTER TABLE users ADD COLUMN is_active BOOLEAN NOT NULL;
```

See the documentation for further detail.
