---
name: data-and-sql
description: Use when writing SQL queries, optimizing database performance, or analyzing data
---

# Data & SQL

Guidelines for SQL optimization, database performance, and data analysis.

## When to Use

- Writing or optimizing SQL queries
- Database performance issues
- Schema design decisions
- Data analysis and insights
- Index strategy planning

## Query Optimization

### Before Writing Queries
1. Clarify the business objective
2. Understand data volume and patterns
3. State any assumptions clearly
4. Consider cost and performance

### Optimization Techniques

| Problem | Solution |
|---------|----------|
| Subqueries | Replace with JOINs |
| Complex logic | Use CTEs for readability |
| Self-joins | Use window functions |
| Row-by-row | Batch operations |
| SELECT * | Specify columns |
| COUNT for existence | Use EXISTS |

### N+1 Query Problem

**Before** (N+1):
```sql
-- 1 query for users, then N queries for posts
SELECT * FROM users WHERE active = true;
-- Then for each: SELECT * FROM posts WHERE user_id = ?;
```

**After** (Single Query):
```sql
SELECT u.id, u.name,
  JSON_AGG(JSON_BUILD_OBJECT('id', p.id, 'title', p.title))
  FILTER (WHERE p.id IS NOT NULL) AS posts
FROM users u
LEFT JOIN posts p ON u.id = p.user_id
WHERE u.active = true
GROUP BY u.id, u.name;
```

## Index Strategy

### Index Types

| Type | Best For | Example |
|------|----------|---------|
| B-Tree | Equality, range, sort | Primary keys, dates |
| Composite | Multi-column WHERE | `(status, created_at)` |
| Partial | Filtered queries | `WHERE status = 'active'` |
| Covering | Index-only scans | Include all SELECT columns |
| GIN/GiST | Full-text, JSON | Text search |

### Index Checklist
- [ ] Primary keys indexed
- [ ] Foreign keys indexed
- [ ] Frequent WHERE columns indexed
- [ ] Composite indexes match query patterns
- [ ] No unused indexes (check stats)
- [ ] Index bloat monitored

### Find Unused Indexes (PostgreSQL)
```sql
SELECT indexname, idx_scan, pg_size_pretty(pg_relation_size(indexrelid))
FROM pg_stat_user_indexes
WHERE idx_scan = 0
ORDER BY pg_relation_size(indexrelid) DESC;
```

## Performance Diagnosis

### Slow Query Analysis
```sql
-- PostgreSQL: Find slow queries
SELECT query, calls, mean_exec_time, max_exec_time
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 10;
```

### Common Issues

| Symptom | Cause | Fix |
|---------|-------|-----|
| Seq scan on large table | Missing index | Add appropriate index |
| Index not used | Stale stats | ANALYZE table |
| Lock contention | Long transactions | Reduce scope |
| Table bloat | Dead tuples | VACUUM or pg_repack |

### EXPLAIN ANALYZE
Always analyze execution plans:
```sql
EXPLAIN ANALYZE
SELECT * FROM orders
WHERE user_id = 123
ORDER BY created_at DESC
LIMIT 10;
```

## Schema Design

### Normalization vs Denormalization

**Normalize when**:
- Data integrity is critical
- Write-heavy workload
- Storage cost matters

**Denormalize when**:
- Read:write ratio > 10:1
- Query performance critical
- Joins are bottleneck

### Schema Checklist
- [ ] Primary keys defined
- [ ] Foreign keys with proper constraints
- [ ] Appropriate data types (not oversized)
- [ ] Indexes for query patterns
- [ ] Timestamps for auditing
- [ ] Migration scripts reversible

## Caching Strategies

### When to Cache
- Expensive queries
- Frequently accessed data
- Semi-static data (tolerate staleness)

### Cache Layers

| Layer | Tool | Use Case |
|-------|------|----------|
| Application | Redis, Memcached | Query results |
| Database | Query cache | Identical queries |
| Materialized View | PostgreSQL | Pre-computed aggregates |

### Materialized View Example
```sql
CREATE MATERIALIZED VIEW user_stats AS
SELECT user_id, COUNT(*) as post_count, MAX(created_at) as last_post
FROM posts
GROUP BY user_id;

CREATE INDEX ON user_stats(user_id);
REFRESH MATERIALIZED VIEW CONCURRENTLY user_stats;
```

## Data Analysis Output

### Findings Format
```markdown
## Summary
Key insight in 1-2 sentences.

## Key Metrics
| Metric | Value | Trend |
|--------|-------|-------|

## Insights
- Finding 1 with supporting data
- Finding 2 with supporting data

## Recommendations
1. Action item with expected impact
2. Suggested follow-up analysis
```

## Migration Best Practices

### Safe Migration Template
```sql
-- Migration: Add index for performance
-- Date: 2025-12-23
-- Ticket: DB-456

-- Forward (non-blocking)
CREATE INDEX CONCURRENTLY idx_posts_user_created
ON posts(user_id, created_at DESC);

-- Rollback
DROP INDEX CONCURRENTLY idx_posts_user_created;

-- Validation
EXPLAIN ANALYZE SELECT * FROM posts WHERE user_id = 1 ORDER BY created_at DESC;
```

### Migration Checklist
- [ ] Tested on production-like data
- [ ] Rollback script ready
- [ ] Zero-downtime (CONCURRENTLY for indexes)
- [ ] Performance impact measured
- [ ] Monitoring in place

## Decision Priority

When optimizing:
1. **Impact** - Measured improvement
2. **Safety** - Reversible, tested
3. **Maintainability** - Understandable
4. **Scalability** - Works at 10x
5. **Cost** - Resource implications
