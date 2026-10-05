---
name: database
description: Design and review persistence, queries, schemas, transactions, and data access using framework-agnostic database principles.
metadata:
  internal: true
---

# Database

Use this skill for persistence, queries, schema changes, migrations, transactions, data integrity, and data-access behavior.

This skill is language, ORM, and database framework agnostic.

## Data Integrity

Enforce important invariants at the strongest practical layer.

Use appropriate:

- constraints
- uniqueness rules
- foreign keys
- nullability
- validation
- transaction boundaries

Application validation does not replace database integrity where concurrent writes can violate an invariant.

## Queries

Prefer structured and parameterized query mechanisms.

Avoid:

- unbounded reads
- unnecessary columns
- repeated identical queries
- N+1 access patterns
- avoidable full scans
- query construction from untrusted input

Inspect the actual workload before adding optimization complexity.

## Transactions

Use transactions when multiple operations must succeed or fail as one logical change.

Keep transaction scopes as small as practical.

Consider:

- partial failure
- retries
- deadlocks
- external side effects
- long-running work

Do not hold database transactions open while performing unnecessary external operations.

## Concurrency

When correctness depends on concurrent access, explicitly consider:

- lost updates
- duplicate creation
- stale reads
- locking
- atomic operations
- optimistic concurrency
- idempotency

Do not assume application-level checks remain valid between read and write.

## Schema Changes

Schema changes should consider:

- backwards compatibility
- existing data
- nullability
- defaults
- index creation
- rollout ordering
- rollback strategy
- large table impact

For risky migrations, prefer staged changes.

## Data Access Boundaries

Keep persistence concerns separate from unrelated presentation or transport logic.

Avoid leaking database-specific details throughout the application when an established data-access boundary exists.

## Verification

Relevant checks may include:

- correct persisted state
- constraint enforcement
- transaction rollback
- concurrent behavior
- query count
- execution plan
- migration safety
- backwards compatibility

## Framework Adaptation

Use the project's native ORM/query/database mechanisms when suitable.

Stack-specific guidance may provide implementation details but must not weaken data-integrity requirements.