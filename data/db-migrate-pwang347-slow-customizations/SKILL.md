---
name: db-migrate
description: Create a database migration. Use when changing schema, adding tables, or modifying columns.
disable-model-invocation: true
---

# Database Migration

Create a new reversible database migration.

## Steps

1. Determine next migration number from `backend/migrations/`
2. Create `backend/migrations/TIMESTAMP_description.ts`
3. Follow the [migration template](./template.ts)
4. Implement both `up()` and `down()` functions
5. Test rollback: run `npm run migrate:down` then `npm run migrate:up`

See [conventions.md](./conventions.md) for naming and patterns.

Arguments: $ARGUMENTS — description of what the migration does
