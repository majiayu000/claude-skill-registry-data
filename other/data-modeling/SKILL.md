---
name: data-modeling
description: "Extendable data models: identity, lifecycle, constraints, indexes, transactions, versioning, migrations, deletion, auditing. Ship schema+queries+indexes together."
---

# data-modeling

Model for the queries you'll run, constrain what must never happen, and ship schema with its indexes.

## Activate when

- Designing tables/documents, constraints, indexes, or reviewing data-layer changes (engine-agnostic).

## Do NOT activate for

- Engine operations (see databases/*); domain rules (see domain-modeling).

## Inspection

Collect the access patterns (reads, writes, hot paths), growth estimates, consistency needs, and the current schema + slow-query evidence.

## Decision rules

- Identity: stable surrogate keys for references; natural keys only with uniqueness proof.
- Constraints in the database for invariants that must survive application bugs (uniqueness, FKs, CHECKs, not-null).
- Indexes matched to EXPLAIN output, not guessed; every index pays write cost — drop unused ones on evidence.
- Lifecycle: created/updated timestamps, versioning where concurrent edits collide, soft vs hard delete decided per audit needs, audit trail where compliance demands.
- Transactions sized to the workflow; migrations expand→migrate→contract.

## Procedure

1. Write the queries first, then the schema that serves them; EXPLAIN before merging.
2. Add constraints + indexes with the migration; include rollback.
3. Cover invariants with DB-level tests where the engine allows, else integration tests.
4. Verify: migration up+down on scratch data, EXPLAIN clean, no N+1 on hot paths.

## Failure modes

- EAV soup; missing FKs "for performance" without measurement; unbounded JSON blobs queried by regex; migrations without rollback; soft-delete breaking uniqueness.

## Escalation

Engine specifics → databases/postgres-operations, mysql, redis, mongodb; roles/security → databases/database-security.

## References

- Related: `../domain-modeling/`, `../../backend/database-design/`, `../../backend/migrations/`.
