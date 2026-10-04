---
name: database-migrations
description: Database migration best practices for schema changes, data migrations, rollbacks, and zero-downtime deployments across PostgreSQL, MySQL, and common ORMs (Prisma, Drizzle, Kysely, Django, TypeORM, golang-migrate).
mcp: codebase-memory-mcp
---

# /supergraph:database-migrations

Safe, reversible database schema changes for production systems.

Announce: "🗄️ /supergraph:database-migrations — checking blast radius and migration safety..."

## When to Activate

- Creating or altering database tables
- Adding/removing columns or indexes
- Running data migrations (backfill, transform)
- Planning zero-downtime schema changes
- Setting up migration tooling for a new project

## Steps

### 1. Check blast radius (MANDATORY before writing any migration)
Use `CBM_PROJECT`: `search_graph` schema/model symbols, `trace_path` inbound and
data-flow, then validated `dependencies`, `hubs`, and `test-gaps` recipes.
Schema changes to hub tables (e.g. `users`, `orders`) ripple through repositories, queries, services. If blast radius > 20 files → STOP and discuss with user.

**Serena symbol-level impact (optional):**
```
mcp__serena__find_referencing_symbols(symbol=<column_or_model_name>)
```
Finds ORM field references that graph tools see only at file level — e.g. a Prisma field rename that `query_graph` sees as "file touched" but Serena sees as "12 usages in service layer". Skip if Serena unavailable.

### 2. Choose migration pattern
Select the appropriate pattern from the sections below (PostgreSQL, Prisma, Drizzle, etc.) based on detected project type from `.supergraph-env`.

### 3. Write migration
Follow Migration Safety Checklist before writing SQL/ORM migration code.

### 4. Verify flows
After migration written:
Use `trace_path(project=CBM_PROJECT, mode="data_flow")` and the `dependencies`
recipe. Empty results are `unavailable` evidence requiring Serena/filesystem
fallback, not invented flows.
All data flows still intact? Application code updated to match schema?

### 5. Report
```
✅ /supergraph:database-migrations
- Pattern: [expand-contract | add-column | add-index | data-migration | ...]
- Blast radius: N files | Hub tables: [list/none]
- Safety checklist: PASS | BLOCKED (list issues)
- Next: /supergraph:tdd → /supergraph:fix → /supergraph:verify
```

## Core Principles

1. **Every change is a migration** — never alter production databases manually
2. **Migrations are forward-only in production** — rollbacks use new forward migrations
3. **Schema and data migrations are separate** — never mix DDL and DML in one migration
4. **Test migrations against production-sized data** — a migration that works on 100 rows may lock on 10M
5. **Migrations are immutable once deployed** — never edit a migration that has run in production

## Migration Safety Checklist

Before applying any migration:

- [ ] Migration has both UP and DOWN (or is explicitly marked irreversible)
- [ ] No full table locks on large tables (use concurrent operations)
- [ ] New columns have defaults or are nullable (never add NOT NULL without default)
- [ ] Indexes created concurrently (not inline with CREATE TABLE for existing tables)
- [ ] Data backfill is a separate migration from schema change
- [ ] Tested against a copy of production data
- [ ] Rollback plan documented

> Full ORM examples (PostgreSQL, Prisma, Drizzle, Kysely, Django, golang-migrate): [REFERENCE.md](./REFERENCE.md)

## Anti-Patterns

| Anti-Pattern                         | Why It Fails                         | Better Approach                             |
| ------------------------------------ | ------------------------------------ | ------------------------------------------- |
| Manual SQL in production             | No audit trail, unrepeatable         | Always use migration files                  |
| Editing deployed migrations          | Causes drift between environments    | Create new migration instead                |
| NOT NULL without default             | Locks table, rewrites all rows       | Add nullable, backfill, then add constraint |
| Inline index on large table          | Blocks writes during build           | CREATE INDEX CONCURRENTLY                   |
| Schema + data in one migration       | Hard to rollback, long transactions  | Separate migrations                         |
| Dropping column before removing code | Application errors on missing column | Remove code first, drop column next deploy  |

## Rules

- ALWAYS check blast radius before writing any migration — hub table changes need user approval
- NEVER alter production databases manually — every change goes through migration files
- NEVER mix DDL and DML in one migration — separate schema changes from data migrations
- NEVER add NOT NULL column without a default to existing tables — locks and rewrites all rows
- ALWAYS create indexes with CONCURRENTLY on live tables
- ALWAYS test against production-sized data before deploying
- NEVER edit a migration that has already run in production — create a new one
- Use expand-contract pattern for zero-downtime column renames and removals
