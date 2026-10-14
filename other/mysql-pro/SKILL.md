---
name: mysql-pro
description: MySQL and MariaDB expertise — InnoDB tuning, replication, and query patterns — use when building on or fixing MySQL.
category: database
---

## Overview

MySQL (and its fork MariaDB) powers a huge share of web applications. Its InnoDB
storage engine is transactional and reliable, but MySQL has its own dialect quirks,
replication model, and tuning knobs. This skill covers writing good MySQL SQL and
keeping a MySQL server healthy.

## When to use

- Tuning InnoDB (`innodb_buffer_pool_size`, redo log, adaptive hash)
- Debugging replication lag or GTID issues
- Choosing storage engines, character sets (`utf8mb4`), and collations
- Writing MySQL-dialect SQL (`GROUP_CONCAT`, `ON DUPLICATE KEY UPDATE`, window functions in 8.0+)
- Planning backups with `mysqldump`, Percona XtraBackup, or binary logs

## Core concepts

**InnoDB is the engine; configure it.** `innodb_buffer_pool_size` (typically
50–75% of RAM on a dedicated server) is the single most important setting — it
caches data and indexes. Undersize it and every query hits disk. Also size the
redo log (`innodb_log_file_size`) generously for write-heavy workloads to avoid
checkpoint stalls.

**`utf8mb4` everywhere.** MySQL's `utf8` is a 3-byte subset that cannot store
emoji or many scripts. Always use `utf8mb4` with an appropriate collation
(`utf8mb4_unicode_ci` or the `_0900_` variants in 8.0). Mismatched collations in
joins cause "illegal mix of collations" errors and kill index use.

**Replication is async by default.** Replicas can lag; never read-your-own-write
from a replica without checking lag (`SHOW SLAVE STATUS` / performance schema).
GTID-based replication simplifies failover and topology changes.

**EXPLAIN FORMAT=JSON / ANALYZE.** `EXPLAIN ANALYZE` (8.0.18+) shows actual
execution with timing. Watch for full table scans, filesorts on large result
sets, and temporary tables — the classic MySQL bottlenecks.

**Upserts and idempotent writes.** `INSERT ... ON DUPLICATE KEY UPDATE` and
`REPLACE INTO` (which deletes then inserts — mind foreign keys and triggers)
make retry-safe writes easy. Prefer the former for most cases.

## Practical workflow

1. **Verify the engine and charset:** `SHOW CREATE TABLE` — confirm InnoDB and
   `utf8mb4` before debugging anything else.
2. **Diagnose slow queries** with the slow query log
   (`slow_query_log`, `long_query_time`) and `EXPLAIN ANALYZE`; fix the query or
   add the missing composite index.
3. **Index foreign keys and join columns** — InnoDB requires indexes on foreign
   keys anyway; missing ones cause table locks on parent updates/deletes.
4. **Batch writes:** multi-row `INSERT`s and transactions with many statements
   are far faster than autocommit-per-row. Keep transactions short to avoid
   holding locks and bloating the undo log.
5. **Replication health:** monitor `Seconds_Behind_Master` / replica lag metrics,
   binary log disk usage, and GTID consistency after topology changes.
6. **Backups:** logical (`mysqldump --single-transaction`) for small DBs;
   physical (XtraBackup) for large ones; always keep binary logs for
   point-in-time recovery and test restores regularly.

## Common pitfalls

- **Using MyISAM or the MEMORY engine for durable data** — no crash safety, no
  real transactions. Use InnoDB unless you have a specific, measured reason.
- **`GROUP BY` with non-aggregated columns** — MySQL's lenient default
  (`ONLY_FULL_GROUP_BY` disabled in old versions) returns arbitrary values. Keep
  the strict SQL mode on.
- **Implicit commits:** DDL statements (`ALTER TABLE`) commit the current
  transaction in MySQL — don't mix schema changes into data transactions
  expecting rollback.
- **Big `OFFSET` pagination** (`LIMIT 100000, 20`) — the engine scans and discards
  100k rows. Use keyset pagination (`WHERE id > last_id ORDER BY id LIMIT 20`).
- **Case-sensitivity surprises:** table names are case-sensitive on Linux but not
  on macOS/Windows defaults (`lower_case_table_names`) — standardize lowercase.
- **Ignoring the query cache removal:** the query cache is gone in 8.0; if old
  tuning guides mention it, they're outdated — rely on the buffer pool instead.
