---
name: Database
description: Design and operate databases avoiding common scaling, reliability, and data integrity traps.
metadata: {"clawdbot":{"emoji":"🗃️","os":["linux","darwin","win32"]}}
---

# Database Gotchas

## Connection Traps
- Connection pools exhausted = app hangs silently — set max connections, monitor pool usage
- Each Lambda/serverless invocation may open new connection — use connection pooling proxy (RDS Proxy, PgBouncer)
- Connections left open block schema changes — `ALTER TABLE` waits for all transactions
- Idle connections consume memory — set connection timeout, kill idle connections

## Transaction Gotchas
- Long transactions hold locks and bloat MVCC — keep transactions short
- Read-only transactions still take snapshots — can block vacuum/cleanup in Postgres
- Implicit autocommit varies by database — explicit BEGIN/COMMIT is safer
- Deadlocks from inconsistent lock ordering — always lock tables/rows in same order
- Lost updates from read-modify-write without locking — use SELECT FOR UPDATE or optimistic locking

## Schema Changes
- Adding column with default rewrites entire table in old MySQL/Postgres — use NULL default, backfill, then alter
- Index creation locks writes in some databases — use CONCURRENTLY in Postgres, ONLINE in MySQL 8+
- Renaming column breaks running application — add new column, migrate, drop old
- Dropping column with active queries causes errors — deploy code change first, then schema change
- Foreign key checks slow bulk inserts — disable constraints, insert, re-enable

## Backup and Recovery
- Logical backups (pg_dump, mysqldump) lock tables or miss concurrent writes — use consistent snapshot
- Point-in-time recovery requires WAL/binlog retention — configure before you need it
- Backup verification: restore regularly — backups that can't restore aren't backups
- Replication lag during backup can cause inconsistency — backup from replica, verify consistency

## Replication Traps
- Replication lag means stale reads — check lag before trusting replica data
- Writes to replica corrupt replication — make replicas read-only
- Schema changes can break replication — replicate schema changes, don't apply separately
- Split-brain after failover loses writes — use fencing/STONITH to prevent
- Promoting replica doesn't redirect connections — application must reconnect to new primary

## Query Patterns
- N+1 queries from ORM lazy loading — eager load relationships or batch queries
- Missing indexes on foreign keys slows joins and cascading deletes
- Large IN clauses become slow — batch into multiple queries or use temp table
- COUNT(*) on large tables is slow — use approximate counts or cache
- SELECT without LIMIT on unbounded data risks OOM

## Data Integrity
- Application-level unique checks have race conditions — use database constraints
- Check constraints often disabled for "flexibility" then data corrupts — keep them on
- Orphan rows from missing foreign keys — add constraints retroactively, clean up first
- Timezone confusion: store UTC, convert on display — never store local time without zone
- Floating point for money causes rounding errors — use DECIMAL or integer cents

## Scaling Limits
- Single table over 100M rows needs sharding strategy — plan before you hit it
- Autovacuum falling behind causes table bloat — monitor dead tuple ratio
- Query planner statistics stale after bulk changes — ANALYZE after large imports
- Connection count doesn't scale linearly — more connections = more lock contention
- Disk IOPS often bottleneck before CPU — monitor I/O wait
