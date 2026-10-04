---
name: thalarch-data-sql
description: >
  Database and SQL engineering for relational persistence, migrations, transactions, query
  correctness, indexing, pagination, ORM behavior, and data-safe rollout. Use when code touches
  schemas, queries, transactions, repositories/ORMs, migrations, or database performance.
---

# Thalarch Data / SQL

Database changes are data changes. Treat correctness, compatibility, rollback/roll-forward, and
production scale as first-class constraints.

## Preflight

Identify:

- database engine/version where known;
- ORM/query layer;
- migration framework;
- transaction model;
- schema ownership;
- production rollout constraints;
- query/test tooling.

Do not write engine-specific syntax based on memory if the actual engine/version can be confirmed.

## Query correctness

Review:

- stable ordering;
- null semantics;
- duplicate/cardinality behavior;
- joins and fan-out;
- transaction isolation assumptions;
- race/lost-update behavior;
- timezone/collation/encoding where relevant;
- parameterization of untrusted values.

Never concatenate untrusted input into SQL identifiers/expressions without an explicit safe
allowlist/escaping mechanism appropriate to the engine.

## ORM discipline

Inspect generated/actual query behavior when performance or correctness depends on it.

Watch for:

- N+1 queries;
- accidental eager loading;
- lazy loads outside a valid session/context;
- row explosion from joins;
- unintended cascades;
- entity equality/identity mistakes;
- transaction boundaries hidden by repository helpers.

A unit test with a mocked repository does not prove ORM/database semantics.

## Migrations

For production-compatible changes, prefer staged expand/migrate/contract patterns when old and
new application versions may overlap.

Before a destructive or locking migration, consider:

- table/index size;
- lock duration;
- backfill strategy;
- nullable/default behavior;
- concurrent writers;
- retry/restartability;
- rollback vs roll-forward plan;
- replication/online-DDL constraints.

Never assume a migration is safe merely because it succeeds on an empty test database.

## Performance

Use query plans/metrics before adding indexes or rewriting queries.

Check:

- selectivity and index order;
- full scans;
- sort/hash spills;
- repeated round trips;
- pagination strategy;
- connection-pool saturation;
- transaction duration;
- cache consistency.

Every new index has write/storage/maintenance cost.

## Testing

Prefer real-database integration evidence for behavior that depends on SQL engine semantics,
constraints, transactions, or ORM mappings. Use containerized/test DB infrastructure already
present in the project when possible.

## Verification

Report separately:

- schema/migration validation;
- query/ORM integration tests;
- performance evidence;
- production rollout assumptions that remain `UNVERIFIED`.
