---
name: postgresql-optimization
description: PostgreSQL database optimization workflow for query tuning, indexing strategies, performance analysis, and production database management.
stacks:
  - postgresql
tags:
  - postgresql
  - performance
category: granular-workflow-bundle
risk: safe
source: personal
date_added: 2026-02-27
---

## Use this skill when

- Optimizing slow PostgreSQL queries
- Designing or reviewing indexing strategies
- Analyzing database performance and identifying bottlenecks
- Tuning PostgreSQL server configuration
- Managing production database maintenance (VACUUM, ANALYZE, bloat)
- Setting up monitoring and alerting for database health

## Do not use this skill when

- You need schema design guidance — use postgresql skill
- The bottleneck is at the application layer, not the database
- You require a DB-agnostic optimization guide

## Instructions

1. Identify the performance problem: slow query, missing index, configuration, or maintenance issue
2. Measure current state with EXPLAIN ANALYZE before making any changes
3. Apply targeted fix at the appropriate layer (index, query rewrite, config, maintenance)
4. Verify improvement with a second EXPLAIN ANALYZE
5. Monitor over time to confirm the fix holds under load

## Capabilities

### Phase 1: Performance Assessment
- Check PostgreSQL version and available features
- Review current configuration (shared_buffers, work_mem, effective_cache_size, autovacuum)
- Identify slow queries via pg_stat_statements or slow query log
- Analyze resource usage: CPU, memory, disk I/O
- Map bottleneck category: scan type, join strategy, I/O, locking, vacuum lag

### Phase 2: Query Analysis
- Read EXPLAIN output: understand node types (Seq Scan, Index Scan, Hash Join, Nested Loop)
- Read EXPLAIN ANALYZE output: compare estimated vs actual row counts (planner miscalibration indicates stale statistics)
- Identify expensive operations: high cost nodes, high actual rows, large loops
- Find optimization opportunities: missing index, suboptimal join order, unnecessary sorts

### Phase 3: Indexing Strategy
- Identify queries doing sequential scans on large tables
- Create B-tree indexes for equality/range queries and ORDER BY
- Add composite indexes with most selective column first
- Use partial indexes for hot subsets (WHERE status = 'active')
- Use covering indexes with INCLUDE for index-only scans
- Use GIN for JSONB containment, arrays, full-text search
- Use GiST for ranges and exclusion constraints
- Review pg_stat_user_indexes: unused indexes waste write performance and bloat

### Phase 4: Query Optimization
- Rewrite subqueries as JOINs where the planner struggles
- Use CTEs (WITH ...) for readability and sequential execution control
- Break up complex queries with multiple CTEs rather than deeply nested subqueries
- Implement proper pagination: offset for small datasets, cursor for large feeds
- Use LIMIT in subqueries to help the planner bound work
- Avoid functions on indexed columns in WHERE — prevents index use

### Phase 5: Configuration Tuning
- shared_buffers: 25% of total RAM; higher for dedicated DB servers
- work_mem: memory per sort/hash operation per connection; multiply by max_connections to estimate peak
- effective_cache_size: total memory PostgreSQL can assume is available for caching; set to 50-75% of RAM
- checkpoint_completion_target: 0.9 to spread checkpoint I/O
- max_wal_size: increase if checkpoint frequency is too high
- autovacuum_vacuum_scale_factor / autovacuum_analyze_scale_factor: decrease for large tables (0.01-0.05)

### Phase 6: Maintenance
- Regular VACUUM to reclaim dead tuples from updates/deletes
- VACUUM ANALYZE after large data changes to update planner statistics
- Monitor table bloat: pg_stat_user_tables, pg_total_relation_size, pgstattuple extension
- Check autovacuum activity: pg_stat_user_tables.last_autovacuum, n_dead_tup
- REINDEX CONCURRENTLY for bloated indexes without table lock

### Phase 7: Monitoring
- pg_stat_statements: track most time-consuming queries across the database
- pg_stat_user_tables: track table access patterns, dead tuples, vacuum timing
- pg_stat_user_indexes: track index usage and identify unused indexes
- pg_locks: identify lock contention causing query slowdowns
- Prometheus with postgres_exporter + Grafana dashboards for ongoing visibility

## Behavioral Traits
- Always measures before and after with EXPLAIN ANALYZE
- Distinguishes between sequential scan on small table (fine) vs large table (problem)
- Checks pg_stat_statements before hypothesizing about slow queries
- Tests index creation with CREATE INDEX CONCURRENTLY to avoid locking production writes
- Validates autovacuum is running before recommending manual VACUUM
- Checks for stale statistics (large planner estimation errors) before rewriting queries
- Treats configuration changes as hypotheses — verifies with monitoring data

## Knowledge Base

### EXPLAIN Output Interpretation
- Seq Scan on large table: missing or unused index
- Index Scan but slow: index not selective enough, or high row count returned
- Nested Loop with large outer table: consider Hash Join via enable_nestloop=off for testing
- Hash Join out of memory: work_mem too low, or query returns too many rows
- Sort with Disk: work_mem too low for this sort operation
- High actual vs estimated rows: stale statistics, run ANALYZE
- Very low estimated rows on high actual: pg_statistics histogram buckets too small (increase statistics target)

### Index Selection Guide
- Equality + range on one column: B-tree
- Multiple equality columns: composite B-tree, most selective first
- JSONB containment: GIN
- Full-text search: GIN on tsvector
- Range overlap, scheduling: GiST on range type
- Hot subset (WHERE x = constant): partial index
- Avoid reading heap for included columns: covering index with INCLUDE
- Time-series, very large, naturally ordered: BRIN

### Common Performance Anti-Patterns
- Function on indexed column in WHERE: `WHERE LOWER(email) = ?` without expression index
- Implicit type cast in WHERE: `WHERE id = '123'` when id is integer
- SELECT * on wide tables: fetches columns never used, prevents index-only scans
- OFFSET-based pagination on large tables: database scans all preceding rows
- IN clause with hundreds of values: consider temporary table or ANY(ARRAY[...])
- Unnecessary ORDER BY in subqueries
- Correlated subqueries executing once per outer row

### Optimization Checklist
- Slow queries identified via pg_stat_statements
- EXPLAIN ANALYZE run before and after changes
- All FK columns have explicit indexes
- Composite index column order reviewed
- Unused indexes removed (check pg_stat_user_indexes)
- Configuration tuned for workload type (OLTP vs analytics)
- Autovacuum monitored and tuned for table size
- Monitoring active with alerting on slow queries and replication lag

## Constraints
- Never disable autovacuum in production
- Never run VACUUM FULL during business hours (locks the entire table)
- Never create indexes without CONCURRENTLY on production tables serving live traffic
- Never tune configuration without measuring the current baseline first
- Always test configuration changes on staging before applying to production
- Never REINDEX without CONCURRENTLY on production
