---
name: cassandra
description: Cassandra — partition keys, CQL, consistency levels, CLI.
---

# Cassandra Reference

## When to Load
Load when the project uses Cassandra or ScyllaDB (signal: `cassandra-driver`, `cassandra-python-driver`, `datastax-astra`, `cassandra:` in docker-compose, `CASSANDRA_HOST` env var).

## CLI Connection

```bash
# cqlsh (bundled with Cassandra):
cqlsh "$CASSANDRA_HOST" "${CASSANDRA_PORT:-9042}" \
  -u "$CASSANDRA_USER" -p "$CASSANDRA_PASSWORD"

# with TLS:
cqlsh "$CASSANDRA_HOST" 9142 --ssl \
  -u "$CASSANDRA_USER" -p "$CASSANDRA_PASSWORD"

# DataStax Astra (cloud):
cqlsh -b "$ASTRA_BUNDLE_PATH" -u "$ASTRA_CLIENT_ID" -p "$ASTRA_SECRET"
```

Key inspection commands:
```sql
DESCRIBE KEYSPACES;
DESCRIBE TABLES;
DESCRIBE TABLE keyspace.table;
SELECT * FROM system.local;               -- node info, rack, DC
SELECT * FROM system.peers;              -- cluster topology
TRACING ON;                              -- trace next query for latency breakdown
```

## Data Model — Think in Queries

Cassandra requires query-driven data modeling. Unlike relational databases, denormalization is expected.

**Primary key anatomy:**
```sql
PRIMARY KEY ((partition_key), clustering_col1, clustering_col2)
```
- **Partition key**: determines which node holds the data; must appear in every query (`WHERE partition_key = ?`)
- **Clustering columns**: physical sort order within the partition; enable range queries
- All data within a partition is stored together; partitions should stay under ~100 MB

**Design rules:**
1. Know your queries before designing the table
2. One table per query pattern is normal
3. Avoid large partitions (millions of rows in one partition → hotspot)
4. Avoid unbounded clustering columns — add a time-bucket to partition key if inserting time series

## CQL Essentials

```sql
-- Create table with TTL:
CREATE TABLE user_sessions (
  user_id   UUID,
  session_id UUID,
  data      TEXT,
  PRIMARY KEY (user_id, session_id)
) WITH default_time_to_live = 86400;

-- Insert with per-row TTL:
INSERT INTO user_sessions (user_id, session_id, data)
VALUES (?, ?, ?) USING TTL 3600;

-- Lightweight transaction (compare-and-set):
INSERT INTO users (id, email) VALUES (?, ?) IF NOT EXISTS;
UPDATE users SET email = ? WHERE id = ? IF email = ?;
```

## Consistency Levels

| Level | Reads from | Writes to | Trade-off |
|-------|-----------|-----------|-----------|
| `ONE` | 1 replica | 1 replica | Fastest; risk of stale reads |
| `QUORUM` | Majority | Majority | Strong consistency across DC |
| `LOCAL_QUORUM` | Majority in local DC | Majority in local DC | Low latency in multi-DC |
| `ALL` | All replicas | All replicas | Strongest; not fault-tolerant |
| `EACH_QUORUM` | Quorum per DC | Quorum per DC | Geo-distributed writes |

Strong consistency rule: `read CL + write CL > replication factor`
- RF=3, write `QUORUM` (2) + read `QUORUM` (2) = 4 > 3 → strongly consistent

Default recommendation: write `LOCAL_QUORUM`, read `LOCAL_QUORUM` for most OLTP workloads.

## Compaction Strategies

| Strategy | Best for |
|----------|----------|
| `SizeTieredCompactionStrategy` (default) | Write-heavy; infrequent reads; heavy data |
| `LeveledCompactionStrategy` | Read-heavy; predictable read latency; smaller SSTables |
| `TimeWindowCompactionStrategy` | Time series with TTL; groups SSTables by time window |

Change strategy: `ALTER TABLE t WITH compaction = {'class': 'LeveledCompactionStrategy'};`

## Secondary Indexes & Materialized Views

- **Secondary indexes**: avoid on high-cardinality columns or on columns used without the partition key — causes scatter reads across all nodes
- **Materialized Views**: maintained by Cassandra; trades write overhead for read convenience; use carefully (risk of write amplification and consistency lag)
- **SAI (Storage-Attached Index)**: Cassandra 4.x / DataStax; column-level index without full-table scatter; prefer over legacy secondary indexes

## Tombstones & Deletion

- Deletes write a **tombstone** (not an immediate removal); tombstones are removed during compaction
- Excessive tombstones (> 100k per read) cause read timeouts — monitor with `nodetool tpstats`
- Use TTL instead of explicit deletes for time-expiring data
- Never issue `TRUNCATE` in production without checking dependent materialized views

## Common Gotchas

| Gotcha | Fix |
|--------|-----|
| `ALLOW FILTERING` in query | Re-model the table for the query or add a SAI index |
| Hotspot partition (one partition grows unbounded) | Add a time-bucket to the partition key |
| Lightweight transactions (IF NOT EXISTS) slow | Use sparingly — they use Paxos; not for hot paths |
| Reading with `IN` on partition key | May cause coordinator hotspot; prefer parallel single-partition reads |
| `nodetool repair` not scheduled | Run weekly on each node; skipping causes inconsistency and tombstone accumulation |
