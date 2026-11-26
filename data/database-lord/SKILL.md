---
name: database-lord
always: true
description: Architect-level database mastery for PostgreSQL, MySQL, MariaDB, MongoDB, Redis, SQLite, SQL Server, Oracle, ClickHouse. Do not use for database migration lord tasks — use `database-migration-lord` instead.
triggers:
  - database lord
  - database

---
[SKILL] database-lord
[OBJ] Design, performance-tune, optimize, and operate relational/document/key-value/analytical databases via Context7.
[RULES]
1. [CMD] IDs: PostgreSQL `/websites/postgresql_17` source `/postgres/postgres`; MySQL `/websites/dev_mysql_doc` source `/mysql/mysql-server`; MariaDB `/websites/mariadb` source `/mariadb/server`; MongoDB `/websites/mongodb_manual` source `/mongodb/mongo`; Redis `/redis/docs` source `/redis/redis-doc`; SQLite `/websites/devdocs_io_sqlite` source `/sqlite/sqlite`; SQL Server `/microsoftdocs/sql-docs`; Oracle `/websites/oracle_en_database_oracle_oracle-database_19`; ClickHouse `/websites/clickhouse` source `/clickhouse/clickhouse-docs`; DuckDB `/duckdb/duckdb-web` source `/duckdb/duckdb`; Meilisearch `/websites/meilisearch`; TiDB `/pingcap/docs` source `/pingcap/tidb`; Prisma `/prisma/web` source `/prisma/prisma`.
2. [CMD] Delegate deep MariaDB design, Galera, migration, and optimization questions to `mariadb-lord`.
3. [REQ] Route every question through pillars: design, performance, optimization, operations.
4. [REQ] Query Context7 with user's full question + topic (design, performance, optimization, operations).
5. [REQ] Use concrete engine terms: WAL, LSN, xid, MVCC, B+Tree, LSM, page, extent, heap tuple, buffer pool, plan node, cost, selectivity, latch, deadlock.
6. [REQ] Cross-engine answers query both IDs and explain design rationale.
7. [REQ] Engine selection by access pattern: Postgres = default relational (extensibility, JSONB when needed); MySQL/MariaDB = read-heavy/ecosystem-fit; SQLite = embedded/edge/file-per-tenant; Redis = cache/queue/ephemeral (not primary store without persistence plan); MongoDB = document-shaped data with real scale-out need; ClickHouse/DuckDB = analytics (columnar). State the access pattern that drove the pick.
8. [REQ] Schema design: normalize to 3NF then denormalize deliberately for measured read patterns; constraints enforce truth at the DB layer (NOT NULL, UNIQUE, CHECK, FK); surrogate + natural keys chosen per table; NULLs mean "unknown" — never magic sentinel values.
9. [REQ] Indexing discipline: indexes exist for query patterns — composite column order follows (equality → range), leftmost-prefix rule respected; every index costs writes — audit unused ones; partial/covering indexes for hot selective queries; `EXPLAIN ANALYZE` before and after, always.
10. [REQ] Transactions: isolation level chosen explicitly (read committed default; serializable where anomaly math requires), transaction scope minimal (no user think-time inside), deadlock retry handling in the app, advisory locks for mutual exclusion patterns.
11. [REQ] MVCC reality: long transactions pin old versions → bloat (Postgres vacuum, autovacuum tuned not disabled); replication lag is a consistency contract — reads-after-writes must pin to primary or accept staleness explicitly.
12. [REQ] Migrations: versioned, reversible or explicitly irreversible-flagged, expand-contract for zero-downtime, batched for large tables, lock-timeout aware (`lock_timeout` set), concurrent index builds on prod.
13. [REQ] Connection discipline: pooling (PgBouncer/proxysql) sized to real concurrency — connections ≠ parallelism; statement timeouts everywhere; idle-in-transaction reaped.
14. [REQ] Operations: WAL/PITR backups (not just dumps), restore drills scheduled, replication monitored (lag + slot bloat), vacuum/maintenance automated, slow-query log reviewed on cadence.
15. [REQ] Analytics split: OLTP engines don't serve dashboards — replicate to columnar (ClickHouse/DuckDB/read replica) once reporting queries hurt OLTP.
16. [PROHIBIT] Storing hot-path state in the DB (queues, sessions — that's Redis/queue), `SELECT *` in app code, N+1 (count queries per request — alert on >~20), unbounded connections, schema changes without lock analysis, or trusting ORM defaults blind (check generated SQL on hot paths).
