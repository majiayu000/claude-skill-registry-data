---
name: migration-and-schema-harness
description: Manage database, schema, and API evolution safely. Use when a repo has migrations, database schemas, public API schemas, seed data, fixtures, compatibility requirements, rollback conventions, or needs scripts/check-migrations.
---

# Migration And Schema Harness

## Purpose

Make schema changes reversible, validated, and compatible with tests, fixtures, and release plans.

## Inspect First

- database config, migrations, schema files, API schemas, seed data, fixtures, ORM config, migration scripts, release docs, and CI

## Procedure

1. Identify schema ownership.
   - Database tables, API contracts, event schemas, generated clients, and fixtures.

2. Define migration rules.
   - Forward migration expectations.
   - Rollback or mitigation expectations.
   - Backward compatibility requirements.
   - Seed and fixture update rules.

3. Add checks.
   - Create target repo `scripts/check-migrations`.
   - Use `scripts/check_migrations.py` for lightweight inventory.
   - Keep dependency, build, and generated directories excluded by default; use `--include-ignored` only to debug scanner behavior.
   - Include migration checks in `scripts/validate` when relevant.

4. Document.
   - `docs/development/migrations.md`
   - Link release rollback notes when migrations affect deployment.

## Validation

- Run migration validation commands when safe.
- Confirm fixtures and seeds match schema changes.
- Confirm rollback or mitigation notes exist.

## Completion Criteria

- Agents know how to change schemas without breaking compatibility or release safety.
