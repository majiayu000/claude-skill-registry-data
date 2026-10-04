---
name: migration-specialist
description: Database migrations, framework version upgrades, and data transformation
  workflows. Use when asked to write a database migration, upgrade a framework to
  a new major version, migrate data between schemas or databases, handle a breaking
  change in a dependency, or plan a zero-downtime schema change.
allowed-tools:
- Read
- Write
- Bash
- Grep
- Glob
metadata:
  author: Daryl Lundy
  version: 2.0.0
  category: operations
  tags:
  - migration
  - database-migration
  - framework-upgrade
  - data-transformation
  - zero-downtime
---

# Migration Specialist

## Activation criteria
- User language explicitly matches trigger phrases such as `write a migration`, `upgrade to version X`, `migrate the schema`.
- The requested work fits this skill's lane: Writing migrations, zero-downtime schema changes, framework version upgrades, data transformations.
- The task stays inside this skill's boundary and avoids adjacent areas called out as out of scope: Application code changes after migration (use relevant language skill).

## First actions
1. `Glob('**/migrations/**', '**/alembic/**', '**/flyway/**', '**/knexfile.*')` — find migration framework
2. `Read` the latest migration file to understand naming convention and current schema state
3. Identify: migration framework, database engine, and whether zero-downtime is required

## Decision rules
- All migrations need both `up` and `down` functions
- For zero-downtime column additions: add nullable first, backfill, then add constraint in a separate migration
- For DROP operations: require explicit confirmation; always include a rollback path

## Output contract
- Migration file using the project's existing framework and naming convention
- `up()` and `down()` both implemented
- For large data migrations: include a dry-run mode or progress logging

## Constraints
- NEVER DROP a column or table in the same migration that removes the code using it — do it in a subsequent release
- Scope boundary: application code changes for a migration belong to the relevant language skill

## Reference
- `references/legacy-agent.md`: migration patterns, zero-downtime strategies, data transformation, framework upgrade guides
