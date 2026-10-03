---
name: database-optimization
description: Optimize database queries, schemas, and configurations for performance. Analyze execution plans, index strategies, and tuning techniques.
triggers:
- /database optimize
- /query tuning
---

# Database Optimization

This skill covers database performance optimization including query tuning, indexing strategies, schema design, and configuration tuning for relational and NoSQL databases.

## When to use this skill

Use this skill when you need to:
- Optimize slow-performing queries
- Design efficient database schemas
- Implement effective indexing strategies
- Tune database configuration parameters
- Scale database performance

## Prerequisites

- Database access and query permissions
- Understanding of execution plans
- Access to monitoring tools (Query Store, pg_stat_statements)
- Knowledge of database internals

## Guidelines

### Query Optimization

**Analyze Execution Plans**
```sql
-- SQL Server
SET SHOWPLAN_XML ON;
GO
SELECT * FROM orders WHERE customer_id = 123;
GO

-- PostgreSQL
EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)
SELECT * FROM orders WHERE customer_id = 123;

-- MySQL
EXPLAIN FORMAT=JSON
SELECT * FROM orders WHERE customer_id = 123;
```

**Common Query Anti-Patterns**
- SELECT * (fetch only needed columns)
- Implicit type conversions
- Functions on indexed columns
- Missing JOIN predicates
- N+1 query problems

**Optimization Techniques**
- Use appropriate JOIN types
- Filter early with WHERE clauses
- Leverage covering indexes
- Batch operations when possible
- Use query hints sparingly

### Indexing Strategies

**Index Types**
- **B-Tree**: Default, good for equality and range queries
- **Hash**: Exact match lookups
- **GIN/GiST**: Full-text search, JSON, arrays (PostgreSQL)
- **Bitmap**: Low cardinality columns
- **Partial**: Index subset of data
- **Composite**: Multi-column indexes

**Index Design Principles**
```sql
-- Covering index example
CREATE INDEX idx_orders_covering 
ON orders (customer_id, status, created_at)
INCLUDE (total_amount, shipping_address);

-- Partial index example  
CREATE INDEX idx_active_users
ON users (last_login)
WHERE is_active = TRUE;
```

**Index Maintenance**
- Monitor index fragmentation
- Rebuild/reorganize regularly
- Remove unused indexes
- Update statistics frequently

### Schema Optimization

**Normalization vs Denormalization**
- Normalize for OLTP (reduce redundancy)
- Denormalize for OLAP (improve read performance)
- Use materialized views for complex aggregations

**Data Types**
- Use smallest appropriate data types
- Avoid nullable columns when possible
- Use ENUM/ CHECK constraints for validation
- Consider JSON for flexible schemas

**Partitioning**
```sql
-- PostgreSQL range partitioning
CREATE TABLE events (
    id bigint,
    event_time timestamp,
    data jsonb
) PARTITION BY RANGE (event_time);

CREATE TABLE events_2024_q1 PARTITION OF events
FOR VALUES FROM ('2024-01-01') TO ('2024-04-01');
```

### Configuration Tuning

**PostgreSQL Key Parameters**
```ini
shared_buffers = 25% of RAM
effective_cache_size = 75% of RAM
work_mem = available RAM / max_connections / 2
maintenance_work_mem = 512MB
max_parallel_workers_per_gather = 4
random_page_cost = 1.1  # For SSD
```

**MySQL Key Parameters**
```ini
innodb_buffer_pool_size = 70-80% of RAM
innodb_log_file_size = 1-2GB
innodb_flush_log_at_trx_commit = 2  # Balance safety/performance
max_connections = 500
query_cache_type = 1  # For read-heavy workloads
```

### Monitoring and Diagnostics

**Identify Slow Queries**
```sql
-- PostgreSQL pg_stat_statements
SELECT query, calls, mean_time, total_time
FROM pg_stat_statements
ORDER BY total_time DESC
LIMIT 10;

-- SQL Server Query Store
SELECT qst.query_text_id, qst.query_sql_text,
       qsrs.avg_duration, qsrs.count_executions
FROM sys.query_store_query_text qst
JOIN sys.query_store_runtime_stats qsrs 
    ON qst.query_text_id = qsrs.query_id
ORDER BY qsrs.avg_duration DESC;
```

**Performance Metrics**
- Buffer hit ratio (target > 99%)
- Query response times (p50, p95, p99)
- Lock wait time
- Connection pool utilization
- Disk I/O operations

### Caching Strategies

**Query Result Caching**
- Application-level caching (Redis)
- Database query cache (MySQL)
- Materialized views
- Result set caching

**Connection Pooling**
- Use connection poolers (PgBouncer, HikariCP)
- Size pools appropriately
- Monitor connection leaks

## Examples

See the `examples/` directory for:
- `query-optimization.sql` - Before/after query examples
- `index-strategies.sql` - Various indexing patterns
- `partitioning-setup.sql` - Table partitioning examples
- `monitoring-queries.sql` - Performance monitoring scripts

## References

- [PostgreSQL performance tuning](https://wiki.postgresql.org/wiki/Performance_Optimization)
- [SQL Server query tuning](https://docs.microsoft.com/sql/relational-databases/performance/)
- [MySQL optimization](https://dev.mysql.com/doc/refman/8.0/en/optimization.html)
- [Use the Index, Luke](https://use-the-index-luke.com/)
