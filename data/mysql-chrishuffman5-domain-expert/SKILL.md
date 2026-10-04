---
name: mysql
description: "MySQL technology expert covering ALL versions. Deep expertise in InnoDB storage engine, replication, InnoDB Cluster, query optimization, Performance Schema, and operational tuning. WHEN: \"MySQL\", \"InnoDB\", \"Group Replication\", \"InnoDB Cluster\", \"InnoDB ClusterSet\", \"MySQL Shell\", \"MySQL Router\", \"Performance Schema\", \"slow query log\", \"binlog\", \"binary log\", \"mysqld\", \"mysqldump\", \"mysqlbinlog\", \"innodb_buffer_pool\", \"GTID\", \"semi-sync\", \"XtraBackup\"."
license: MIT
---

# MySQL

This skill covers MySQL across all supported versions (8.0, 8.4 LTS, and the 9.x Innovation track). It covers InnoDB internals, replication topologies, query optimization, and operational tuning. For version-specific detail, see the matching file under `references/versions/`.

## When to Use This Skill vs. Version-Specific Guidance

**Use this agent when the question spans versions or is version-agnostic:**
- "How does the InnoDB buffer pool work?"
- "Tune MySQL for a write-heavy workload"
- "Set up async replication with GTIDs"
- "Compare InnoDB indexes vs. covering indexes"
- "Best practices for my.cnf tuning"

**See the matching version reference when the question is version-specific:**
- "MySQL 9.0 VECTOR data type" --> `references/versions/9.x.md`
- "MySQL 8.4 GTID Tags" --> `references/versions/8.4.md`
- "MySQL 8.0 hash joins" --> `references/versions/8.0.md`
- "Migrating from 5.7 to 8.0" --> `references/versions/8.0.md`

## How to Approach Tasks

When you receive a request:

1. **Classify** the request:
   - **Architecture/internals** -- Load `references/architecture.md`
   - **Performance diagnostics** -- Load `references/diagnostics.md`
   - **Configuration/operations** -- Load `references/best-practices.md`
   - **Version-specific feature** -- See the matching `references/versions/<v>.md` file
   - **Comparison with other databases** -- see the `overview` skill

2. **Determine version** -- Ask if unclear. Behavior differs significantly across versions (e.g., hash joins exist only in 8.0.18+, VECTOR type only in 9.0+).

3. **Analyze** -- Apply MySQL-specific reasoning. Reference InnoDB mechanics, the optimizer, replication, and Performance Schema as relevant.

4. **Recommend** -- Provide actionable guidance with specific server variables, SQL, or configuration changes.

5. **Verify** -- Suggest validation steps (EXPLAIN ANALYZE, Performance Schema queries, sys schema views).

## Core Expertise

### InnoDB Storage Engine

InnoDB is MySQL's default transactional storage engine and the foundation for nearly all production workloads:

- **Buffer Pool** -- Caches data and index pages in memory. Uses an LRU list with midpoint insertion (new pages enter at 3/8 from the head, promoting to the head only after a second access within `innodb_old_blocks_time`). Size with `innodb_buffer_pool_size` (target 70-80% of available RAM). Split across `innodb_buffer_pool_instances` for concurrency.
- **Redo Log (WAL)** -- Write-ahead log guaranteeing durability. All modifications are written to the redo log before being applied to data pages. Controlled by `innodb_redo_log_capacity` (8.0.30+) or the older `innodb_log_file_size` * `innodb_log_files_in_group`. Lock-free redo log design in 8.0.
- **Undo Log** -- Stores old row versions for MVCC and rollback. Lives in dedicated undo tablespaces. The purge system reclaims undo space after all transactions that could need those versions complete.
- **Doublewrite Buffer** -- Protects against partial page writes (torn pages). Pages are written to the doublewrite buffer first, then to their final locations. On SSD with atomic writes, can be disabled (`innodb_doublewrite=0`).
- **Change Buffer** -- Caches changes to secondary index pages that are not in the buffer pool, merging them later during reads or background operations. Controlled by `innodb_change_buffer_max_size`.
- **Adaptive Hash Index** -- InnoDB automatically builds hash indexes on frequently accessed B-tree index pages. Monitored via `SHOW ENGINE INNODB STATUS`. Can be disabled with `innodb_adaptive_hash_index=0` if contention on btr_search latches is observed.

### Replication

MySQL offers several replication topologies:

- **Asynchronous Replication** -- The source commits and returns to the client without waiting for any replica to acknowledge. Fastest but risks data loss on source failure. Uses binary log events.
- **Semi-Synchronous Replication** -- The source waits for at least one replica to acknowledge receiving the event before returning to the client (`rpl_semi_sync_source_wait_for_replica_count`). Balances durability and performance.
- **Group Replication (GR)** -- Multi-source replication with built-in consensus (Paxos). Supports single-primary (one writer, multiple readers) or multi-primary mode. Foundation for InnoDB Cluster.

Key replication concepts:
- **Binary Log (binlog)** -- Records all changes. Formats: ROW (default, safest), STATEMENT, MIXED.
- **GTID (Global Transaction Identifiers)** -- `server_uuid:transaction_id`. Simplifies failover and topology changes. Always use for new setups.
- **Relay Log** -- Replica's local copy of binary log events, applied by the SQL/applier thread.
- **Multi-Threaded Replicas** -- `replica_parallel_workers` controls parallelism. Use `replica_parallel_type=LOGICAL_CLOCK` (8.0) or the improved defaults in 8.4+.

### InnoDB Cluster, ClusterSet, and ReplicaSet

- **InnoDB Cluster** -- Integrated HA solution: Group Replication + MySQL Shell (AdminAPI) + MySQL Router. Provides automatic failover, routing, and management.
- **InnoDB ClusterSet** -- Links multiple InnoDB Clusters across regions for disaster recovery with asynchronous replication between clusters.
- **InnoDB ReplicaSet** -- Simpler topology using asynchronous replication (single primary + replicas) managed via MySQL Shell AdminAPI. No automatic failover without MySQL Router.

### MySQL Shell

MySQL Shell (`mysqlsh`) is the advanced client for MySQL:

- **AdminAPI** -- `dba.createCluster()`, `dba.getCluster()`, `cluster.addInstance()`, `cluster.status()` for managing InnoDB Cluster.
- **Upgrade Checker** -- `util.checkForServerUpgrade()` identifies compatibility issues before version upgrades.
- **Dump/Load** -- `util.dumpInstance()`, `util.dumpSchemas()`, `util.loadDump()` for high-performance logical backup and restore with parallelism and chunking.
- **Utilities** -- `util.importTable()` for parallel CSV/TSV import, `util.exportTable()` for export.

### MySQL Router

Lightweight middleware that provides transparent routing to InnoDB Cluster or ReplicaSet nodes:
- Routes read/write traffic to the primary, read-only traffic to secondaries
- Bootstrapped against an InnoDB Cluster: `mysqlrouter --bootstrap root@primary:3306`
- Listens on configurable ports (default: 6446 R/W, 6447 R/O)
- Maintains a dynamic routing table updated from cluster metadata

## Query Optimization

### EXPLAIN

Always use `EXPLAIN` to analyze query execution plans:

```sql
-- Tree format (8.0.16+, most readable)
EXPLAIN FORMAT=TREE SELECT ...;

-- EXPLAIN ANALYZE (8.0.18+, actual execution with timing)
EXPLAIN ANALYZE SELECT ...;

-- Traditional tabular format
EXPLAIN SELECT ...;

-- JSON format (most detail)
EXPLAIN FORMAT=JSON SELECT ...;
```

Key EXPLAIN columns (traditional format):
- **type** -- Access method: `system` > `const` > `eq_ref` > `ref` > `range` > `index` > `ALL` (full table scan)
- **possible_keys** -- Indexes the optimizer considered
- **key** -- Index actually chosen
- **key_len** -- Bytes of the index used (reveals partial index usage)
- **rows** -- Estimated rows to examine
- **filtered** -- Percentage of rows that will pass the WHERE condition
- **Extra** -- Critical flags: `Using index` (covering), `Using filesort`, `Using temporary`, `Using where`

### Optimizer Features

- **Histograms** (8.0+) -- `ANALYZE TABLE t UPDATE HISTOGRAM ON col` provides distribution statistics beyond simple cardinality. Critical for skewed data.
- **Invisible Indexes** (8.0+) -- `ALTER TABLE t ALTER INDEX idx INVISIBLE` tests impact of dropping an index without actually dropping it.
- **Hash Joins** (8.0.18+) -- Used for equi-joins without indexes. The optimizer automatically chooses hash join when appropriate.
- **Descending Indexes** (8.0+) -- `CREATE INDEX idx ON t(col DESC)` for queries with `ORDER BY col DESC`.
- **Functional Indexes** (8.0.13+) -- `CREATE INDEX idx ON t((LOWER(email)))` indexes expressions.

### Index Best Practices

- Use composite indexes with the leftmost prefix rule in mind
- Prefer covering indexes (`SELECT` columns included in the index) to avoid table lookups
- Monitor unused indexes via `sys.schema_unused_indexes`
- Monitor redundant indexes via `sys.schema_redundant_indexes`
- Keep the primary key short (InnoDB clusters data by PK; all secondary indexes carry the PK)

## Diagnostics Overview

### Performance Schema

Performance Schema is MySQL's instrumentation framework. Key tables:

| Table | Purpose |
|---|---|
| `events_statements_summary_by_digest` | Aggregated query statistics (like pg_stat_statements) |
| `file_summary_by_instance` | I/O statistics per file |
| `table_io_waits_summary_by_table` | I/O wait time per table |
| `memory_summary_global_by_event_name` | Memory allocation tracking |
| `threads` | All server threads with current state |
| `data_locks` | Current InnoDB lock information |
| `data_lock_waits` | Lock wait relationships |

### sys Schema

The sys schema provides human-readable views over Performance Schema:

| View | Purpose |
|---|---|
| `statement_analysis` | Top queries by latency, rows examined, tmp tables |
| `host_summary` | Connection and statement stats by host |
| `schema_table_statistics` | Table I/O and latency |
| `innodb_buffer_stats_by_table` | Buffer pool usage per table |
| `schema_unused_indexes` | Indexes never used since last restart |
| `schema_redundant_indexes` | Indexes that duplicate others |

### Slow Query Log

The slow query log captures queries exceeding `long_query_time`:

```ini
slow_query_log = ON
slow_query_log_file = /var/log/mysql/slow.log
long_query_time = 1          # seconds (default 10; set lower)
log_slow_extra = ON          # 8.0.14+: adds Rows_examined, Bytes_sent, etc.
```

Analyze with `pt-query-digest` from Percona Toolkit for aggregated reports.

## Common Pitfalls

1. **utf8 vs utf8mb4** -- MySQL's `utf8` is an alias for `utf8mb3`, which supports only 3-byte characters (no emoji, no supplementary Unicode). Always use `utf8mb4` with `utf8mb4_0900_ai_ci` collation.

2. **caching_sha2_password connector issues** -- MySQL 8.0+ defaults to `caching_sha2_password`. Older connectors and applications may fail to authenticate. Either upgrade the connector, use `mysql_native_password` (deprecated), or ensure TLS/RSA is configured.

3. **GROUP BY implicit sort removed** -- MySQL 8.0 no longer implicitly sorts GROUP BY results. If you relied on sorted output, add an explicit `ORDER BY`. Queries that assumed sorted GROUP BY will return in arbitrary order.

4. **innodb_flush_log_at_trx_commit trade-offs** -- Value `1` (default) flushes redo log to disk on every commit (safest, ACID). Value `2` writes to OS cache on every commit, flushes once per second (risks 1 second of data on OS crash). Value `0` writes and flushes once per second (risks 1 second of data on mysqld crash). Use `1` for production unless you accept the risk.

5. **Large transactions in replication** -- A single large transaction (e.g., `DELETE` millions of rows) blocks replication applier. Break into batches of 1,000-10,000 rows.

6. **Not sizing redo log appropriately** -- Undersized redo log causes aggressive checkpoint flushing and performance stalls. Monitor `Log sequence number` vs `Log flushed up to` in `SHOW ENGINE INNODB STATUS`. Use `innodb_redo_log_capacity` (8.0.30+) or increase `innodb_log_file_size`.

7. **Ignoring InnoDB buffer pool hit ratio** -- If `Innodb_buffer_pool_read_requests` / (`Innodb_buffer_pool_read_requests` + `Innodb_buffer_pool_reads`) is below 99%, the buffer pool is too small.

8. **Default tmp_table_size / max_heap_table_size** -- Defaults (16MB) cause frequent internal temp tables to spill to disk. Monitor `Created_tmp_disk_tables` vs `Created_tmp_tables`. Increase for OLAP-style queries.

## Best Practices Summary

### InnoDB Tuning

```ini
innodb_buffer_pool_size = <70-80% of available RAM>
innodb_buffer_pool_instances = 8         # if buffer pool > 1GB
innodb_flush_log_at_trx_commit = 1       # ACID compliance
innodb_flush_method = O_DIRECT           # avoid double buffering with OS cache
innodb_flush_neighbors = 0               # disable for SSD (coalesce writes unnecessary)
innodb_io_capacity = 2000                # IOPS for background tasks (SSD: 2000+)
innodb_io_capacity_max = 4000            # burst IOPS
innodb_redo_log_capacity = 2G            # 8.0.30+; size for 1-2 hours of peak writes
innodb_file_per_table = ON               # each table gets its own .ibd file
```

### Replication

- Always use GTID (`gtid_mode=ON`, `enforce_gtid_consistency=ON`)
- Enable multi-threaded replicas (`replica_parallel_workers=4-16`)
- Monitor replication lag: `SHOW REPLICA STATUS` -> `Seconds_Behind_Source`
- Use `binlog_format=ROW` (default in 8.0+)

### Security

- Use TLS for all connections (`require_secure_transport=ON`)
- Use roles for privilege management (8.0+)
- `caching_sha2_password` is the default authentication plugin (8.0+)
- Rotate passwords with dual-password support (8.0.14+)
- Encrypt redo log, undo log, and binary log at rest (8.0+)

## Version-specific guidance

| Version | Status | Key Feature | Reference |
|---|---|---|---|
| **MySQL 8.0** | EOL Apr 2026 | Transactional DD, Window Functions, CTEs, Hash Joins | `references/versions/8.0.md` |
| **MySQL 8.4 LTS** | Premier Support ~Apr 2029 | GTID Tags, auto histograms, dedicated_server ON | `references/versions/8.4.md` |
| **MySQL 9.x** | Innovation (short-lived) | VECTOR type, JavaScript Stored Programs | `references/versions/9.x.md` |

## Reference Files

Load these when you need deep knowledge for a specific area:

- `references/architecture.md` -- InnoDB buffer pool, redo log, undo log, doublewrite buffer, change buffer, adaptive hash index, tablespace types. Read for "how does InnoDB work internally" questions.
- `references/diagnostics.md` -- Performance Schema instruments and key tables, sys schema views, EXPLAIN formats and interpretation, slow query log configuration and analysis. Read when troubleshooting performance.
- `references/best-practices.md` -- InnoDB tuning parameters with values, replication best practices, security hardening, backup strategies. Read for configuration and operational guidance.

## Diagnostic Scripts

Ready-made SQL in `scripts/` (MySQL 8.0+, performance_schema/sys), numbered by investigation order. All read-only.

- `scripts/01-processlist-and-locks.sql` -- Sessions plus InnoDB lock-wait chains (sys.innodb_lock_waits)
- `scripts/02-statement-digest.sql` -- Top statements by latency with missing-index signatures
- `scripts/03-innodb-health.sql` -- Buffer pool hit rate, purge lag, lock and tmp-table counters
- `scripts/04-table-sizes.sql` -- Largest tables with index share and fragmentation
