---
name: mysql-pitfalls
description: "Use when writing or reviewing MySQL 8.x (InnoDB) schema, queries or migrations: JSON columns and the -> and ->> operators, indexing JSON, utf8mb4 index key length limits, default case-insensitive collation, range partitioning and its key and foreign key restrictions, retention by dropping partitions, replica lag and read-your-writes, max_execution_time and lock wait timeouts, INSERT ... ON DUPLICATE KEY UPDATE locking, online DDL algorithms that rebuild a table, and the prerequisites of gh-ost."
---

# mysql-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for the MySQL 8.x behaviours that differ from what a developer used to
PostgreSQL or an ORM's defaults would assume: a JSON operator that returns quoted text, an index key that is too
long only on utf8mb4, a partitioned table that refuses a foreign key, a lock timeout of one year, and an `ALTER`
that copies the whole table. The premise: **MySQL's defaults and limits are documented and specific, so a rule
that names the number is checkable and a rule that says "be careful" is not**.

## When
- A JSON column is queried, compared or indexed, or a long string column is indexed.
- A table is partitioned, or retention is implemented by deleting old rows.
- A read must see a write just made through a replica, or a query or lock needs a timeout.
- An `ALTER TABLE` runs against a large table, or a shadow-table tool such as gh-ost is considered.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | JSON, collation and index key length: `->` vs `->>`, indexing JSON, key limits, default collation | a JSON column, a text index or a string comparison is written | [`01-json-collation-keys.md`](./references/01-json-collation-keys.md) |
| 2 | Partitioning, replicas and timeouts: partition keys, retention, lag, read-your-writes, timeout variables, upsert locks | a table is partitioned, replicas serve reads, or a timeout or lock error appears | [`02-partitioning-replicas-timeouts.md`](./references/02-partitioning-replicas-timeouts.md) |
| 3 | DDL that rebuilds and gh-ost prerequisites: online DDL algorithms, VARCHAR boundary, generated columns, foreign keys, shadow-table limits | an `ALTER TABLE` touches a large table or a schema change tool is chosen | [`03-rebuilding-ddl-and-gh-ost.md`](./references/03-rebuilding-ddl-and-gh-ost.md) |

## Output / checkpoint
Each rule was exercised on the target version: a JSON query was checked with `EXPLAIN` against its index (§1.1),
a migration was run with an explicit `ALGORITHM` clause so that an unsupported combination fails instead of
copying (§3.1), and a retention job was run against a scratch table partitioned the same way (§2.1). A rule
checked by reading documentation only is not verified.

## Guardrails
- Never expect `->` to return unquoted text: use `->>` or an explicit cast to a native type (§1.1).
- Never create a foreign key on, or to, a partitioned InnoDB table (§2.1).
- Never leave `lock_wait_timeout` at its default in a migration session (§2.3).
- Never run an `ALTER TABLE` on a large table without an explicit `ALGORITHM` and `LOCK` clause (§3.1).
- Versions: each rule names the MySQL version it needs; the manual read is MySQL 8.4. Nothing was run while
  writing this block.
- General migration discipline belongs to `devops-conventions`; ORM migration review is in
  `prisma-ops-and-test-hygiene` §1.4 and `jpa-hibernate-pitfalls`.

## Origin
Rewritten from the MySQL 8.4 Reference Manual (facts only, no text copied), the gh-ost documentation and the
strong_migrations README (MIT), read 2026-10-08. 🟡: never run by us; open points are in
[`references/origin.md`](./references/origin.md). Overlaps with `skills/sql-conventions` §7 and `skills/devops-conventions` (2026-10-19); cross-referenced, not merged.
