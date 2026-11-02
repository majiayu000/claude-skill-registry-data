---
name: database-migration-safety
description: "Reviews database schema and data migrations for safe deployment and rollback. Use when changing tables, indexes, constraints, RLS policies, or persisted application data."
---

# Database Migration Safety

## Use when
A migration works on a tiny local database but locks production tables, loses data, or becomes impossible to roll back.

## Workflow
1. Describe data volume, write rate, constraints, indexes, locks, nullability, old/new application versions, and required maintenance windows.
2. Prefer expand-migrate-contract phases when old and new app versions may overlap; backfill in observable bounded batches.
3. Check transaction semantics, lock duration, retry safety, RLS/security behavior, and how partial progress is detected.
4. Test forward migration, interruption/resume, old-client compatibility, verification queries, and a realistic rollback or roll-forward recovery.

## Required output
A migration risk review, rollout/rollback sequence, verification SQL, and operational monitoring plan.

## Validation
- No required data is dropped before backfill/verification succeeds.
- Large data changes are bounded, resumable, and observable.
- Security policies and application compatibility remain correct during deployment.

## Guardrails
Never run destructive production migration commands without backups, approved change control, and a tested recovery plan.
