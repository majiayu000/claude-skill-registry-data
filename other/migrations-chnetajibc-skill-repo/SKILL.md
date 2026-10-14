---
name: migrations
description: "Migrations: expand-migrate-contract, separate schema vs data migrations, down-migration or explicit irreversible, rollback plan, zombie-code removal."
---

# migrations

Migrate without downtime and without fear: expand, move, contract — each step deployable alone.

## Activate when

- Changing schemas, backfilling data, renaming fields, or removing old code paths.

## Do NOT activate for

- Greenfield schema (see architecture/data-modeling); deploy mechanics (see backend/production-readiness).

## Inspection

Current schema, target schema, existing data volume/shape, running application versions, and who reads the changing columns.

## Decision rules

- Expand→migrate→contract: additive change first (deploy), backfill + dual-read/write (deploy), cutover + remove old (deploy). Never break the running version in one step.
- Schema migrations separate from data migrations (different failure modes, different rollback).
- Every migration ships a down-path or an explicit irreversible note with owner sign-off; destructive changes (drop column/table) only after the contract phase proves no readers.
- Renames are add-copy-remove, never `RENAME` in one deploy.

## Procedure

1. Write forward + backward scripts; rehearse on a production-shaped copy.
2. Deploy phase by phase with verification gates (row counts, checksums, dual-read agreement).
3. Remove the old path + its code (zombie-code sweep) only after cutover metrics confirm.
4. Verify: up+down rehearsed, app works at every intermediate phase, rollback drill recorded.

## Failure modes

- Locking rewrites on huge tables without batching; backfill without idempotency re-run; dropping columns the old release still reads; untested down-paths.

## Escalation

Engine specifics → databases/*; zero-downtime strategy disputes → architecture/api-design (compat) + production-readiness.

## References

- Related: `../database-design/`, `../transactions/`, `../../databases/fundamentals/`.
