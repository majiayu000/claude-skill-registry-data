---
name: optimize-queries
description: Automatically optimize Supabase PostgreSQL queries by analyzing execution plans, adding indexes, and improving RLS policies. Triggers when user mentions slow queries, performance issues, or query optimization.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Query Optimization Skill

Automatically analyze and optimize Supabase database queries for better performance.

## Purpose

This skill analyzes slow-running queries, identifies bottlenecks, and implements optimizations including index creation, RLS policy improvements, and query restructuring.

## When to Use

- User mentions slow query performance
- Requests for database optimization
- Reports of timeout errors
- Asks about improving query speed
- Discusses scalability concerns

## Instructions

1. **Identify Query Issues**
   - Request example of slow query
   - Use EXPLAIN ANALYZE if possible
   - Check for missing indexes
   - Review RLS policy implementation

2. **Analyze Execution Plan**
   - Look for sequential scans
   - Identify expensive operations
   - Check join strategies
   - Evaluate row estimates vs actuals

3. **Recommend Optimizations**
   - Suggest specific indexes with CREATE INDEX statements
   - Optimize RLS policies by wrapping functions in SELECT
   - Recommend query restructuring if needed
   - Suggest materialized views for complex aggregations

4. **Implement Changes**
   - Create migration file with optimizations
   - Test changes in development
   - Measure performance improvements
   - Document optimization decisions

5. **Verify Improvements**
   - Re-run EXPLAIN ANALYZE
   - Compare execution times
   - Check index usage stats
   - Confirm no regressions

## Examples

### Example 1: Add Missing Index
```sql
-- Slow query
SELECT * FROM posts WHERE author_id = '...' AND published = true ORDER BY created_at DESC;

-- Solution: Add composite index
CREATE INDEX CONCURRENTLY idx_posts_author_published_created
  ON posts(author_id, published, created_at DESC)
  WHERE published = true;
```

### Example 2: Optimize RLS Policy
```sql
-- Before: Function called per row
CREATE POLICY "policy" ON table_name
  USING (auth.uid() = user_id);

-- After: Function called once
CREATE POLICY "policy" ON table_name
  USING ((SELECT auth.uid()) = user_id);
```

### Example 3: Materialized View for Aggregations
```sql
CREATE MATERIALIZED VIEW user_stats AS
SELECT
  user_id,
  COUNT(*) as post_count,
  MAX(created_at) as last_post
FROM posts
GROUP BY user_id;

CREATE INDEX ON user_stats(user_id);
REFRESH MATERIALIZED VIEW CONCURRENTLY user_stats;
```

## Output Format

Provide:
1. Analysis of current query performance
2. Specific optimization recommendations with SQL
3. Expected performance improvements
4. Migration script with optimizations
5. Testing instructions
