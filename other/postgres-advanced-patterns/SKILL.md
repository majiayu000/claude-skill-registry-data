---
name: postgres-advanced-patterns
description: Advanced PostgreSQL patterns for performance optimization, complex queries, indexing strategies, and database design
license: MIT
metadata:
  source: affaan-m/everything-claude-code
  adapted-by: ai-skills
  category: database
---

# PostgreSQL Advanced Patterns

Advanced patterns for high-performance PostgreSQL database design, querying, and optimization.

## Performance Optimization

### 1. Effective Indexing

```sql
-- B-tree index for equality and range queries
CREATE INDEX idx_users_email ON users(email);

-- Partial index for filtered queries
CREATE INDEX idx_active_users ON users(email) WHERE active = true;

-- Composite index for multiple columns
CREATE INDEX idx_orders_user_date ON orders(user_id, created_at DESC);

-- GiST index for full-text search
CREATE INDEX idx_products_search ON products USING GiST(to_tsvector('english', name || ' ' || description));

-- GIN index for JSON queries
CREATE INDEX idx_metadata_gin ON events USING GIN(metadata);
```

### 2. Query Optimization

```sql
-- Use EXPLAIN ANALYZE to understand query plans
EXPLAIN ANALYZE
SELECT * FROM orders WHERE user_id = 123;

-- Avoid SELECT *
SELECT id, name, email FROM users WHERE active = true;

-- Use EXISTS instead of IN for large subqueries
SELECT * FROM users u
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.user_id = u.id);

-- Batch operations instead of loops
INSERT INTO logs (event, created_at)
SELECT unnest(ARRAY['login', 'logout', 'update']), NOW();
```

### 3. Connection Pooling

```typescript
import { Pool } from 'pg';

const pool = new Pool({
  max: 20,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});

// Use pool for queries
const result = await pool.query('SELECT * FROM users WHERE id = $1', [userId]);
```

## Advanced Query Patterns

### Window Functions

```sql
-- Running totals
SELECT 
  date,
  amount,
  SUM(amount) OVER (ORDER BY date) as running_total
FROM transactions;

-- Row numbering with partitions
SELECT 
  user_id,
  purchase_date,
  amount,
  ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY purchase_date DESC) as purchase_rank
FROM purchases;

-- Moving averages
SELECT 
  date,
  price,
  AVG(price) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) as moving_avg_7d
FROM stock_prices;
```

### Common Table Expressions (CTEs)

```sql
-- Recursive CTE for hierarchical data
WITH RECURSIVE org_chart AS (
  SELECT id, name, manager_id, 1 as level
  FROM employees
  WHERE manager_id IS NULL
  
  UNION ALL
  
  SELECT e.id, e.name, e.manager_id, oc.level + 1
  FROM employees e
  JOIN org_chart oc ON e.manager_id = oc.id
)
SELECT * FROM org_chart ORDER BY level, name;

-- Multiple CTEs for complex queries
WITH 
  active_users AS (
    SELECT id FROM users WHERE active = true
  ),
  recent_orders AS (
    SELECT user_id, COUNT(*) as order_count
    FROM orders
    WHERE created_at > NOW() - INTERVAL '30 days'
    GROUP BY user_id
  )
SELECT u.id, u.name, COALESCE(ro.order_count, 0) as recent_orders
FROM active_users au
JOIN users u ON au.id = u.id
LEFT JOIN recent_orders ro ON u.id = ro.user_id;
```

### JSON Operations

```sql
-- Query JSON columns
SELECT data->>'name' as name, 
       data->'address'->>'city' as city
FROM customers
WHERE data->>'status' = 'active';

-- JSON aggregation
SELECT user_id,
       json_agg(json_build_object('id', id, 'title', title)) as posts
FROM posts
GROUP BY user_id;

-- JSON path queries
SELECT * FROM events
WHERE metadata @> '{"type": "purchase"}';
```

## Database Design Patterns

### 1. Partitioning

```sql
-- Range partitioning by date
CREATE TABLE events (
  id BIGSERIAL,
  event_type TEXT,
  created_at TIMESTAMP NOT NULL
) PARTITION BY RANGE (created_at);

CREATE TABLE events_2026_01 PARTITION OF events
FOR VALUES FROM ('2026-01-01') TO ('2026-02-01');

CREATE TABLE events_2026_02 PARTITION OF events
FOR VALUES FROM ('2026-02-01') TO ('2026-03-01');
```

### 2. Materialized Views

```sql
-- Create materialized view for expensive queries
CREATE MATERIALIZED VIEW user_stats AS
SELECT 
  user_id,
  COUNT(DISTINCT order_id) as total_orders,
  SUM(amount) as total_spent,
  MAX(created_at) as last_order_date
FROM orders
GROUP BY user_id;

-- Refresh periodically
REFRESH MATERIALIZED VIEW CONCURRENTLY user_stats;

-- Create index on materialized view
CREATE INDEX idx_user_stats_user_id ON user_stats(user_id);
```

### 3. Constraints and Validation

```sql
-- Check constraints
ALTER TABLE products
ADD CONSTRAINT price_positive CHECK (price > 0);

-- Exclusion constraints
CREATE TABLE bookings (
  room_id INT,
  during TSRANGE,
  EXCLUDE USING GIST (room_id WITH =, during WITH &&)
);

-- Domain types for reusable constraints
CREATE DOMAIN email_address AS TEXT
CHECK (VALUE ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$');

CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email email_address NOT NULL UNIQUE
);
```

## Transactions and Concurrency

### Transaction Isolation

```sql
-- Serializable transactions for critical operations
BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE;
SELECT * FROM accounts WHERE id = 1 FOR UPDATE;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;

-- Repeatable read for consistent snapshots
BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ;
SELECT SUM(balance) FROM accounts;
-- Consistent view maintained throughout transaction
COMMIT;
```

### Row-Level Locking

```sql
-- Pessimistic locking
SELECT * FROM orders WHERE id = 123 FOR UPDATE;

-- Shared lock for read-only access
SELECT * FROM products WHERE id = 456 FOR SHARE;

-- Skip locked rows
SELECT * FROM queue WHERE processed = false
FOR UPDATE SKIP LOCKED
LIMIT 10;
```

## Monitoring and Maintenance

### Query Performance

```sql
-- Find slow queries
SELECT query, mean_exec_time, calls
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 10;

-- Check index usage
SELECT schemaname, tablename, indexname, idx_scan
FROM pg_stat_user_indexes
ORDER BY idx_scan ASC;

-- Table bloat
SELECT schemaname, tablename, 
       pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

### Maintenance Tasks

```sql
-- Vacuum and analyze
VACUUM ANALYZE users;

-- Reindex
REINDEX TABLE users;

-- Update statistics
ANALYZE users;
```

## Best Practices

1. **Always use parameterized queries** to prevent SQL injection
2. **Create indexes on foreign keys** for join performance
3. **Use connection pooling** for better resource management
4. **Monitor query performance** with pg_stat_statements
5. **Regular VACUUM and ANALYZE** for statistics
6. **Use appropriate transaction isolation levels**
7. **Avoid N+1 queries** with proper joins or batching
8. **Implement retry logic** for transaction conflicts

## Integration Points

Complements:
- **backend-implementation-patterns**: For API data access
- **tdd-workflow**: For database testing
- **verification-loop**: For query performance checks
- **security-implementation-guide**: For secure queries
