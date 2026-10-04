---
name: migration-safety
description: Safe migration patterns for databases, APIs, libraries, and data transformations with zero-downtime techniques and mandatory rollback planning.
compatibility: opencode
metadata:
  audience: migration-engineer, platform-delivery-lead
  purpose: migration-guidance
---
## What I do

Provide actionable guidance for planning and executing migrations safely. Every migration — schema, data, API, or library — must have a tested rollback path, a monitoring plan, and a strategy that avoids downtime.

## When to use me

Load this skill when planning or executing any migration: database schema changes, data transformations, API version transitions, or library upgrades. The migration-engineer and platform-delivery-lead should load this before writing or reviewing a migration spec.

## Core principle

Every migration is a contract with production. You are changing something that running systems depend on. The cost of a failed migration is not "we fix it tomorrow" — it's data loss, broken clients, or extended downtime. Plan accordingly.

## Zero-downtime migration techniques

### Expand-contract (preferred for most migrations)

The safest general-purpose pattern. Three phases:

1. **Expand**: Add the new structure alongside the old one. Both coexist. Old code continues to work unchanged.
2. **Migrate**: Move data/traffic/consumers to the new structure. Verify correctness.
3. **Contract**: Remove the old structure after all consumers have migrated and a soak period has passed.

Never collapse these into one step. The expand phase is your safety net — if anything goes wrong during migration, you still have the old structure intact.

### Blue-green

Run two complete environments in parallel. Route traffic to the new environment after verification. Keep the old environment warm for instant rollback.

Use blue-green when:
- The migration involves infrastructure changes, not just code
- You need to verify the entire stack, not just individual components
- Rollback must be instantaneous (seconds, not minutes)

### Feature flags

Gate new behavior behind a flag. Roll out gradually — 1%, 10%, 50%, 100%. Monitor error rates at each stage.

Use feature flags when:
- The migration is behavioral (new logic, new data flow) rather than structural (new schema)
- You want to decouple deployment from activation
- You need per-user or per-tenant rollout control

## Database migration safety

### Backwards-compatible schema changes

Every schema migration must be backwards-compatible with the currently deployed application code. The deployment sequence is: deploy schema change, then deploy application code. If the schema change breaks existing code, you have a window of failure between the two deployments.

**Safe operations:**
- Add a nullable column
- Add a new table
- Add an index (use `CREATE INDEX CONCURRENTLY` on PostgreSQL to avoid locks)
- Widen a column type (e.g., `VARCHAR(50)` to `VARCHAR(100)`)

**Unsafe operations (require expand-contract):**
- Rename a column — instead, add new column, backfill, update code, drop old column
- Remove a column — instead, stop reading it in code, deploy, then drop it in a later migration
- Change a column type to something narrower or incompatible
- Add a NOT NULL constraint to an existing column — instead, add a CHECK constraint first, backfill nulls, then add NOT NULL
- Drop a table that any code still references

### Rollback strategies

Every migration script must have a corresponding rollback script. Test the rollback on a copy of production data before running the forward migration.

- **Additive migrations** (add column, add table): Rollback is dropping the addition. Simple but verify no code depends on it yet.
- **Data migrations** (backfill, transform): Rollback requires preserving the original data. Either keep the old column until the migration is confirmed, or take a logical backup of affected rows before transforming.
- **Destructive migrations** (drop column, drop table): These are irreversible. Only execute after a soak period confirms nothing depends on the dropped structure. Always take a backup immediately before.

### Lock management

Long-running migrations on large tables can acquire locks that block reads/writes. Mitigate this:
- Use online DDL tools (`pt-online-schema-change` for MySQL, `pg_repack` for PostgreSQL) for large table alterations
- Set statement timeouts on migration connections so a stuck migration doesn't hold locks indefinitely
- Schedule lock-acquiring migrations during low-traffic windows
- Monitor lock wait times during execution

## Data transformation patterns

### Batch processing

Never transform all rows in a single transaction. Process in batches:
- Choose a batch size that completes in under 1 second per batch
- Commit after each batch to release locks and allow checkpointing
- Track progress (last processed ID or timestamp) so the job can resume after interruption
- Add a configurable sleep between batches to reduce load on the database

### Idempotent transforms

Every data transformation must be safe to run multiple times. If the job crashes at batch 5,000 and restarts from batch 4,900, the overlapping rows must not be corrupted.

Design for idempotency:
- Use `INSERT ... ON CONFLICT DO UPDATE` instead of blind inserts
- Guard updates with a condition: `UPDATE ... WHERE status != 'migrated'`
- Use a migration status column or tracking table to mark processed rows

### Validation

Before, during, and after:
- **Before**: Count rows, sample data, verify assumptions about data shape
- **During**: Log batch progress, error counts, and skipped rows. Stop on unexpected error rates.
- **After**: Run validation queries comparing old and new data. Verify row counts match. Spot-check edge cases (nulls, empty strings, extreme values, unicode).

## API version migration

### Parallel running

When migrating an API version:
1. Deploy the new version alongside the old one (e.g., `/v2/users` alongside `/v1/users`)
2. Route new consumers to v2. Existing consumers stay on v1.
3. Monitor both versions. Compare response shapes, error rates, latency.
4. Set a deprecation date for v1. Communicate it to consumers.
5. After all consumers have migrated, remove v1.

### Consumer coordination

- Identify all consumers before starting. Check API keys, access logs, documentation.
- Notify consumers with a concrete timeline: "v1 will stop accepting requests on [date]."
- Provide a migration guide showing the v1-to-v2 mapping for every endpoint and field.
- Monitor v1 traffic. Do not remove v1 until traffic reaches zero or the deprecation deadline passes.

### Deprecation timelines

- Internal APIs: minimum 2 sprint cycles between deprecation notice and removal
- External APIs: minimum 3 months, preferably 6
- Add deprecation headers (`Deprecation`, `Sunset`) to v1 responses during the transition

## Library upgrade strategies

### Incremental upgrades

Never skip major versions. If you're on v2 and need v5, upgrade v2→v3→v4→v5 sequentially. Each step should be a separate commit with passing tests.

### Adapter patterns

When a library's API changes significantly between versions, introduce an adapter layer:
1. Create a thin wrapper around the current library usage
2. Migrate all call sites to use the wrapper
3. Swap the wrapper's internals to the new library version
4. Remove the wrapper once the new API is stable and well-understood

### Compatibility shims

For breaking changes in function signatures or behavior:
- Write shim functions that translate old call patterns to new ones
- Mark shims with `@deprecated` or equivalent so they get cleaned up
- Set a deadline for removing shims — they are temporary bridges, not permanent fixtures

## Rollback planning

**Every migration must have a documented rollback plan.** This is non-negotiable.

The rollback plan must answer:
1. **Trigger**: What conditions indicate the migration has failed? (error rate spike, data inconsistency, consumer complaints)
2. **Procedure**: Step-by-step instructions to revert. No "undo the migration" hand-waving — specific commands, scripts, or deployment steps.
3. **Data recovery**: If the migration transformed data, how do you restore the original state?
4. **Timeline**: How long does the rollback take? Is it seconds (feature flag), minutes (revert deployment), or hours (restore from backup)?
5. **Verification**: How do you confirm the rollback succeeded?

Test the rollback before running the migration. If you can't test it, you're not ready to migrate.

## Monitoring during migration

### What to watch

- **Error rates**: Both application errors and database errors. Compare to baseline.
- **Latency**: P50, P95, P99. Migrations that add load can spike tail latency.
- **Lock waits**: Database lock wait times and deadlock counts.
- **Queue depths**: If the migration generates async work, watch queue backlogs.
- **Consumer health**: If migrating an API, monitor downstream consumer error rates.
- **Disk space**: Data migrations can temporarily double storage requirements.

### When to abort

Abort the migration if:
- Error rate exceeds 2x baseline for more than 5 minutes
- P99 latency exceeds 3x baseline
- Any deadlock that isn't automatically resolved
- Data validation checks fail on a sample batch
- Disk usage approaches capacity limits

Aborting is not failure — it's professionalism. A migration that's aborted and retried after investigation is far better than one that's pushed through and causes an incident.
