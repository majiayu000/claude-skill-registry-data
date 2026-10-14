---
name: fundamentals
description: "Reusable database fundamentals: substrate choice, normalization, isolation, locking, migrations, pooling, backups, least privilege. Use for any database decision before engine specifics."
---

# fundamentals

Choose the substrate by access pattern, then apply the same operational discipline everywhere.

## Activate when

- Picking relational vs document vs KV/cache, designing schemas, or reviewing any data-layer change.

## Do NOT activate for

- Engine specifics (see postgres-operations, mysql, redis, mongodb); credential handling (see database-security).

## Procedure

1. Substrate: relational when relationships are queryable and schema known; document when access is aggregate-shaped; KV/cache when access is key→value with no joins. Name the access pattern before choosing.
2. Model: identity, ownership, lifecycle, invariants; normalization by default, denormalization only for measured reads.
3. Correctness: transactions with the isolation level the workflow needs; locking chosen deliberately (optimistic vs pessimistic); migrations expand→migrate→contract with down-paths.
4. Operations: connection pooling sized to workload, statement timeouts, backups with restore drills, replication lag awareness.
5. Security: least-privilege roles, read-only agents, destructive-query guards (see database-security).
6. Verify: migration up+down on scratch, slow-query log reviewed, concurrent-worker test where locking is used.

## References
- Engine leaves: `../postgres-operations/`, `../mysql/`, `../redis/`, `../mongodb/`; `../database-security/`.
