---
name: postgres-partitioning-uuid-v7
description: Design PostgreSQL partitions and pruning around UUIDv7.
---

# PostgreSQL partitioning with UUIDv7

Read applicable `AGENTS.md` and their declared adapter alias, otherwise
`.agents/skills/postgres-partitioning-uuid-v7/SKILL.md` from the repository root if present.
Local policy overrides these defaults; do not reload an already-read adapter or canonical skill.

For schema names, references, and canonical table shapes, read
[postgres-schema-design](../postgres-schema-design/SKILL.md).

Partition only after lifecycle, retention, and query predicates show that it helps.

- Treat a UUIDv7 as time ordered. Where the meaning matters, keep an explicit business timestamp.
- Align the partition key, primary key, indexes, constraints, and query predicates so partition
  pruning is observable.
- Add a parent lower bound to a read of a `RANGE (id)` child table by its parent's UUIDv7 id
  (`id >= min_uuidv7(parent time - skew)`) only when both hold: every writer sets the parent column
  at insert, to a parent that already exists, and never re-points it to a newer parent; and nothing
  mints child ids from a historical time (imports, backfills, seeds). Counterexample: articles
  clustered into a story created later are older than their parent, and the bound silently drops
  them. See [parent lower bound](references/partition-lifecycle.md#parent-lower-bound).
- A statement that must read every partition declares that, with a reason, on the statement. Do not
  use a table-wide exemption: it also silences every future query on that table. See
  [cross-partition reads](references/partition-lifecycle.md#declaring-cross-partition-reads).
- Plan creation, retention, migration, and verification as one deployable lifecycle. Include
  rollback and independent-reader compatibility.
- Read [partition lifecycle](references/partition-lifecycle.md) before a schema or retention
  migration.

Consumer wrapper owns: partition intervals, migration tooling, retention policy, and deploy
sequencing.
