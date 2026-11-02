---
name: save-schema-migration
description: "Plans backward-compatible game save schema changes and migrations. Use when entities, chunks, world metadata, player data, or serialization formats change."
---

# Save Schema Migration

## Use when
A new engine build cannot load existing worlds safely or corrupts data during a partial upgrade.

## Workflow
1. Inventory persisted fields and invariants, assign an explicit schema version, and document defaults for missing fields.
2. Write pure migrations from each supported version to the next; do not mix migration with normal gameplay initialization.
3. Preserve the original save until the migrated copy passes validation and can be reopened successfully.
4. Test old fixtures, interrupted migration, unknown future versions, corrupted records, and migration idempotency.

## Required output
A schema-version table, migration functions, backup/rollback policy, and fixture matrix.

## Validation
- Existing fixtures remain readable or fail with an actionable message.
- Migration does not mutate the original before successful verification.
- Unknown versions never get overwritten by an older executable.

## Guardrails
Never delete or rewrite the only copy of a user's world as a side effect of attempting to open it.
