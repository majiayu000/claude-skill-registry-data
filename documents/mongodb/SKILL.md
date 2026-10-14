---
name: mongodb
description: "MongoDB operations: document modeling, indexing, transactions, aggregation, replica sets. Use for MongoDB work; research version docs before relying on behavior."
---

# mongodb

Model by access pattern: documents shaped like the reads that fetch them.
## Inspection

Collect access patterns, document shapes, growth, consistency needs, and current slow-operation evidence.

## Decision rules

Embed for read-together, reference for shared/mutable; shard key on cardinality + locality evidence; transactions short, retried-safe.


## Activate when

- Designing MongoDB collections, indexes, aggregations, or operating replica sets.

## Do NOT activate for

- Relational workloads better served by Postgres/MySQL (see fundamentals).

## Procedure

1. Version: detect server version; research in https://www.mongodb.com/docs/ for that version (transactions, indexes, and aggregation stages are version-gated).
2. Modeling: embed for read-together, reference for shared/mutable; avoid unbounded arrays; shard key chosen with cardinality + locality evidence.
3. Indexes: compound order (equality → sort → range), covered queries where hot, TTL/sparse/partial where semantics fit; confirm with explain plans.
4. Transactions: multi-document only where needed, kept short; retryable writes understood; idempotent application layer regardless.
5. Operations: replica-set health, backups with restore drills, connection pooling, slow-operation profiling.
6. Security: least-privilege roles, network binding restricted, auth on, sensitive fields encrypted/masked.
7. Verify: explain evidence, migration rehearsal, restore drill, concurrency test on transactional paths.

## References
- `../fundamentals/`, `../database-security/`.
- Registry: `../../research/documentation-search/references/framework-registry.yaml` (mongodb).

## Failure modes

Unbounded arrays; missing indexes found via slow logs; multi-doc transactions held open; shard key on low-cardinality field.

## Escalation

Relational fit → databases/postgres-operations, mysql; security → databases/database-security.
