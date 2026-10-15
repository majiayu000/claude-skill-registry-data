---
name: deprecation-and-migration
description: "Retire APIs or migrate consumers and persistent data across releases."
license: MIT
metadata:
  author: Addy Osmani and Skillz contributors
  source: addyosmani/agent-skills
  source-commit: 1401c8b8030e023baeebb31781a6653fe8e93026
  adaptation: curated-rewrite
  owner: software-factory
  risk: high
  capabilities: addyosmani,deprecation-and-migration
---

# Deprecation and migration

Use this workflow when retiring interfaces, moving consumers, or changing
persistent data across releases. For a private API whose callers deploy
together, prefer one verified change over an unnecessary compatibility layer.

## Decide what must survive

Inventory callers, background workers, scheduled jobs, old clients, exports,
stored records, and replay queues. Search source and available usage evidence;
absence of logs is not proof of no consumers. Identify the owner, reason for
retirement, required behavior, migration cost, and authorized scope.

A replacement must cover the use cases being retained. Intentionally retiring
a feature may have no replacement; that needs an explicit product decision and
a data disposition plan. Do not invent a retirement deadline or notify users
without authorization.

## Choose a migration path

Choose the least machinery that preserves compatibility during rollout:

- Move all owned, jointly deployed callers in one change when safe.
- Use a temporary adapter when independently deployed callers must coexist.
- Route a bounded cohort to a replacement when production comparison is needed.
- Use expand, migrate, and contract phases for incompatible persistent schemas.

Every temporary path needs an owner, a removal condition, and evidence of
remaining use. Keep new writes consistent with whichever rollback path is
promised. Do not mirror money-moving side effects into both implementations.

## Persistent data

Read [the migration checks](references/data-migrations.md) before schema edits
or backfills. Inspect the actual engine/version, table sizes, workload, and
deployment order. Adding a column or index can still lock a busy table or
consume enough capacity to disrupt service.

Separate code rollback from data recovery. A destructive down migration may
discard valid new data and is not automatically a safe recovery plan. Use a
tested reverse operation when appropriate; otherwise document a forward fix,
restore procedure, recovery limits, and the point after which rollback changes.

## Complete and verify

Verify each migrated cohort with behavior checks and data reconciliation.
Observe consumers over a window that covers delayed jobs and supported client
versions. Remove old paths only after usage evidence and deployment state meet
the agreed retirement criteria. Remove obsolete flags, configuration, and
tests while retaining tests for preserved behavior and historical decisions.

Report phase, evidence, remaining consumers, and recovery limits. Local code
and migration files do not authorize a production backfill, destructive schema
operation, announcement, or deployment.

Reference: [PostgreSQL ALTER TABLE](https://www.postgresql.org/docs/current/sql-altertable.html).
