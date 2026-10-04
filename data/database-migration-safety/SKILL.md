---
name: database-migration-safety
description: "Use when changing a database schema or transforming persisted data in a live or long-lived application to inspect engine and ORM behavior, plan compatibility across application versions, test against representative data, and define recovery before execution. Trigger for schema migrations, backfills, renames, index changes, or zero-downtime rollout planning."
---

# Database Migration Safety

## Overview

This skill applies when changing a database schema or transforming persisted data in a live or long-lived application. Its intended outcome is to inspect engine and ORM behavior, plan compatibility across application versions, test against representative data, and define recovery before execution.

## When to Use

### Preserved source section: When to Use

Use for schema or data changes in a database that may outlive a deployment. This skill reviews migration safety; it does not authorize applying a migration to production.

## Scope

**Does:** Follow the task boundary stated under When to Use and Instructions.

**Does not:** See the preserved source boundaries below and under Stop Conditions.

### Preserved source section: Guardrails

- Never reset, drop, truncate, or rewrite a real database as a test.
- Do not edit a migration already applied in a shared or production environment; add a new corrective migration instead.
- Stop if table size, lock behavior, backup status, or execution authority is unknown and material to safety.

### Source boundary statements from: When to Use

Use for schema or data changes in a database that may outlive a deployment. This skill reviews migration safety; it does not authorize applying a migration to production.

### Source boundary statements from: Procedure

1. **Inspect the real state.** Read the current schema, migration conventions, engine version, and code paths that read or write affected fields. Do not assume the migration tool's generated plan is safe by default.

## Inputs

**Required:** See the preserved source input guidance below.

**Optional:** Not specified in source skill.

**Prerequisites:** Not specified in source skill.

### Preserved source section: Inputs

- Database engine/version, ORM/migration tool, current schema, and migration history.
- Data volume and shape, query/application dependencies, replication, and traffic patterns.
- Deployment order, old/new application compatibility, maintenance window, backup, and recovery options.
- Authorization for local, staging, or production execution.

## Instructions

### Preserved source section: Procedure

1. **Inspect the real state.** Read the current schema, migration conventions, engine version, and code paths that read or write affected fields. Do not assume the migration tool's generated plan is safe by default.
2. **Classify the change.** Identify locks, rewrites, constraints, index cost, data loss, and whether the operation is reversible. Mark irreversible steps and human decisions explicitly.
3. **Preserve compatibility.** For changes used by a rolling deployment, use an expand-and-contract sequence: introduce compatible schema, deploy code that tolerates both forms, backfill safely, switch reads/writes, then remove obsolete structures in a later release.
4. **Separate schema and data work.** Make backfills restartable, idempotent, observable, and bounded. Use batches and checkpoints where needed; avoid a single unbounded transaction on large tables.
5. **Plan recovery.** Define backup/restore, forward-fix, or compensating migration options. A syntactic DOWN migration is not a reliable rollback if data has already been transformed or discarded.
6. **Test realistically.** Apply migrations to a disposable copy or representative dataset. Measure lock duration and runtime, verify constraints and row counts, test application versions on each side of the change, and simulate interruption where practical.
7. **Stage execution.** Produce preflight checks, monitoring signals, pause conditions, and an operator runbook. Obtain explicit approval for each environment before running writes.
8. **Verify afterward.** Confirm schema version, data invariants, application health, error rates, and cleanup state; record the result and any deferred contract step.

## Decision Rules

The following source conditional guidance is preserved verbatim; no unstated action is inferred.

### Source conditional guidance from: Procedure

5. **Plan recovery.** Define backup/restore, forward-fix, or compensating migration options. A syntactic DOWN migration is not a reliable rollback if data has already been transformed or discarded.

### Source conditional guidance from: Output and Acceptance

Return the migration sequence, compatibility matrix, data/lock risks, test evidence, recovery plan, execution gates, and post-migration checks. Accept readiness only when the sequence is tested against representative data and recovery is credible for the failure modes identified.

### Source conditional guidance from: Guardrails

- Stop if table size, lock behavior, backup status, or execution authority is unknown and material to safety.

## Output Format

### Preserved source section: Output and Acceptance

Return the migration sequence, compatibility matrix, data/lock risks, test evidence, recovery plan, execution gates, and post-migration checks. Accept readiness only when the sequence is tested against representative data and recovery is credible for the failure modes identified.

## Validation Checklist

- [ ] Verify the source-defined success criteria above.

## Edge Cases and Recovery

### Source edge/failure guidance from: Inputs

- Deployment order, old/new application compatibility, maintenance window, backup, and recovery options.

### Source edge/failure guidance from: Procedure

5. **Plan recovery.** Define backup/restore, forward-fix, or compensating migration options. A syntactic DOWN migration is not a reliable rollback if data has already been transformed or discarded.
8. **Verify afterward.** Confirm schema version, data invariants, application health, error rates, and cleanup state; record the result and any deferred contract step.

### Source edge/failure guidance from: Output and Acceptance

Return the migration sequence, compatibility matrix, data/lock risks, test evidence, recovery plan, execution gates, and post-migration checks. Accept readiness only when the sequence is tested against representative data and recovery is credible for the failure modes identified.

## Stop Conditions

### Source stop-related guidance from: Procedure

7. **Stage execution.** Produce preflight checks, monitoring signals, pause conditions, and an operator runbook. Obtain explicit approval for each environment before running writes.

### Source stop-related guidance from: Guardrails

- Stop if table size, lock behavior, backup status, or execution authority is unknown and material to safety.

## Examples

Not specified in source skill. The original provided no input/output example, and none has been invented.

## Success Criteria

### Acceptance criteria from source: Output and Acceptance

Return the migration sequence, compatibility matrix, data/lock risks, test evidence, recovery plan, execution gates, and post-migration checks. Accept readiness only when the sequence is tested against representative data and recovery is credible for the failure modes identified.
