---
name: sql-expert
description: Deep SQL expertise for query optimization and database design. Use when writing complex queries, optimizing slow queries, designing schemas, understanding.
---

# SQL Expert

Specialized expertise in SQL and relational database design, providing deep guidance on query optimization, indexing strategies, schema design, and database-specific features across PostgreSQL, MySQL, and SQL Server.

## When to Use This Skill

Use this skill for:

- Writing complex SQL queries
- Optimizing slow queries
- Designing database schemas
- Understanding execution plans
- Creating effective indexes
- Database-specific features
- Performance tuning

**Trigger phrases**: "SQL", "database query", "optimize query", "index", "execution plan", "schema design", "PostgreSQL", "MySQL", "SQL Server"

## What This Skill Does

Provides SQL expertise including:

- **Query Optimization**: Rewriting queries for performance
- **Index Strategy**: Designing effective indexes
- **Schema Design**: Normalization, data modeling
- **Execution Plans**: Reading and understanding plans
- **Database Features**: DB-specific capabilities
- **Performance Tuning**: Identifying and fixing bottlenecks

## Instructions

### Step 1: Analyze Query Performance

**Understanding Execution Plans**:

```sql
-- PostgreSQL
EXPLAIN ANALYZE
SELECT u.name, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON o.user_id = u.id
WHERE u.created_at > '2024-01-01'
GROUP BY u.id, u.name;

-- MySQL
EXPLAIN FORMAT=JSON
SELECT ...

-- SQL Server
SET STATISTICS IO ON;
SET STATISTICS TIME ON;
SELECT ...
```

**Reading Execution Plans**:

| Operation | Good Sign | Bad Sign |
|-----------|-----------|----------|
| Index Scan | Using covering index | Full table scan when index exists |
| Seq Scan | Small table | Large table with selective WHERE |
| Nested Loop | Small inner table | Large tables on both sides |
| Hash Join | Large tables, equality join | Not enough memory |
| Sort | Indexed order | Large sort without index |

### Step 2: Optimize Common Query Patterns

**Avoid SELECT ***:

```sql
-- Bad: Fetches all columns
SELECT * FROM users WHERE status = 'active';

-- Good: Only needed columns
SELECT id, name, email FROM users WHERE status = 'active';
```

**Use EXISTS Instead of IN for Subqueries**:

```sql
-- Potentially slow with large subquery result
SELECT * FROM products
WHERE category_id IN (SELECT id FROM categories WHERE active = true);

-- Better: EXISTS stops at first match
SELECT * FROM products p
WHERE EXISTS (
    SELECT 1 FROM categories c
    WHERE c.id = p.category_id AND c.active = true
);
```

**Optimize JOINs**:

```sql
-- Bad: Joining on non-indexed columns
SELECT o.*, p.name
FROM orders o
JOIN products p ON p.sku = o.product_sku;

-- Good: Join on indexed foreign key
SELECT o.*, p.name
FROM orders o
JOIN products p ON p.id = o.product_id;

-- Use appropriate join type
-- INNER JOIN: Need matches in both tables
-- LEFT JOIN: Need all from left, matches from right
-- Don't use LEFT JOIN if you actually need INNER JOIN
```

**Avoid Functions on Indexed Columns**:

```sql
-- Bad: Function prevents index usage
SELECT * FROM users WHERE YEAR(created_at) = 2024;

-- Good: Range condition uses index
SELECT * FROM users
WHERE created_at >= '2024-01-01' AND created_at < '2025-01-01';

-- Bad: Function on column
SELECT * FROM users WHERE LOWER(email) = 'user@example.com';

-- Good: Use functional index (PostgreSQL) or store lowercase
CREATE INDEX idx_users_email_lower ON users (LOWER(email));
-- Or store email in lowercase
```

### Step 3: Design Effective Indexes

**Index Types**:

```sql
-- B-tree (default): Equality, range queries
CREATE INDEX idx_users_email ON users(email);

-- Composite: Multiple columns (order matters!)
CREATE INDEX idx_orders_user_date ON orders(user_id, created_at);
-- Good for: WHERE user_id = ? AND created_at > ?
-- Good for: WHERE user_id = ?
-- Bad for: WHERE created_at > ? (user_id not in query)

-- Partial index: Subset of rows
CREATE INDEX idx_active_users ON users(email) WHERE status = 'active';

-- Covering index: Includes all needed columns
CREATE INDEX idx_orders_covering ON orders(user_id, created_at)
INCLUDE (total, status);

-- GIN/Full-text: Text search, arrays, JSONB
CREATE INDEX idx_products_tags ON products USING GIN(tags);
CREATE INDEX idx_products_search ON products USING GIN(to_tsvector('english', name || ' ' || description));
```

**Index Strategy Guidelines**:

| Query Pattern | Index Strategy |
|--------------|----------------|
| `WHERE col = ?` | Single column B-tree |
| `WHERE col1 = ? AND col2 = ?` | Composite (col1, col2) |
| `WHERE col1 = ? ORDER BY col2` | Composite (col1, col2) |
| `WHERE col IN (?, ?, ?)` | Single column B-tree |
| `WHERE col LIKE 'prefix%'` | B-tree (prefix only) |
| `WHERE col LIKE '%substring%'` | GIN trigram |
| `WHERE col @> '{"key": "value"}'` | GIN on JSONB |

### Step 4: Optimize Specific Patterns

**Pagination**:

```sql
-- Bad: OFFSET is slow for large offsets
SELECT * FROM products ORDER BY id LIMIT 20 OFFSET 10000;

-- Good: Keyset pagination (cursor-based)
SELECT * FROM products
WHERE id > 10000
ORDER BY id
LIMIT 20;

-- For complex ordering, use indexed columns
SELECT * FROM products
WHERE (created_at, id) > ('2024-01-15', 5000)
ORDER BY created_at, id
LIMIT 20;
```

**Aggregations**:

```sql
-- Slow: Aggregating large table
SELECT category_id, COUNT(*) FROM products GROUP BY category_id;

-- Better: Maintain materialized view or counter table
CREATE MATERIALIZED VIEW category_counts AS
SELECT category_id, COUNT(*) as product_count
FROM products GROUP BY category_id;

-- Or use approximate counts
SELECT reltuples::bigint AS estimate
FROM pg_class WHERE relname = 'products';
```

**Batch Operations**:

```sql
-- Bad: Many individual inserts
INSERT INTO logs (message) VALUES ('log1');
INSERT INTO logs (message) VALUES ('log2');
-- ... thousands more

-- Good: Batch insert
INSERT INTO logs (message) VALUES
('log1'), ('log2'), ('log3'), ... ;

-- Better: Use COPY (PostgreSQL) or LOAD DATA (MySQL)
COPY logs (message) FROM '/path/to/data.csv' CSV;

-- For updates, batch with CTEs
WITH batch AS (
    SELECT id FROM products WHERE needs_update = true LIMIT 1000
)
UPDATE products SET updated_at = NOW()
WHERE id IN (SELECT id FROM batch);
```

### Step 5: Schema Design Best Practices

**Normalization Levels**:

```sql
-- 1NF: Atomic values, no repeating groups
-- Bad: Repeating columns
CREATE TABLE orders (
    id INT,
    product1_id INT, product1_qty INT,
    product2_id INT, product2_qty INT
);

-- Good: Separate table
CREATE TABLE orders (id INT PRIMARY KEY);
CREATE TABLE order_items (
    order_id INT REFERENCES orders(id),
    product_id INT,
    quantity INT
);

-- 3NF: No transitive dependencies
-- Bad: city depends on zip, not directly on id
CREATE TABLE customers (
    id INT,
    name VARCHAR(100),
    zip VARCHAR(10),
    city VARCHAR(100)  -- Derived from zip
);

-- Good: Separate lookup
CREATE TABLE zipcodes (zip VARCHAR(10) PRIMARY KEY, city VARCHAR(100));
CREATE TABLE customers (
    id INT,
    name VARCHAR(100),
    zip VARCHAR(10) REFERENCES zipcodes(zip)
);
```

**Strategic Denormalization**:

```sql
-- When to denormalize:
-- 1. Read-heavy with complex joins
-- 2. Aggregations computed frequently
-- 3. Performance critical paths

-- Example: Storing computed total
CREATE TABLE orders (
    id INT PRIMARY KEY,
    user_id INT,
    total DECIMAL(10,2),  -- Denormalized sum of items
    created_at TIMESTAMP
);

-- Keep consistent with trigger
CREATE FUNCTION update_order_total() RETURNS TRIGGER AS $$
BEGIN
    UPDATE orders SET total = (
        SELECT SUM(quantity * price)
        FROM order_items WHERE order_id = NEW.order_id
    ) WHERE id = NEW.order_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

### Step 6: Database-Specific Features

**PostgreSQL**:

```sql
-- JSONB for semi-structured data
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    data JSONB NOT NULL
);
CREATE INDEX idx_events_data ON events USING GIN(data);

-- Query JSONB
SELECT * FROM events WHERE data @> '{"type": "click"}';
SELECT data->>'user_id' as user_id FROM events;

-- Window functions
SELECT
    name,
    department,
    salary,
    AVG(salary) OVER (PARTITION BY department) as dept_avg,
    RANK() OVER (ORDER BY salary DESC) as salary_rank
FROM employees;

-- CTEs and recursive queries
WITH RECURSIVE org_tree AS (
    SELECT id, name, manager_id, 0 as depth
    FROM employees WHERE manager_id IS NULL

    UNION ALL

    SELECT e.id, e.name, e.manager_id, t.depth + 1
    FROM employees e
    JOIN org_tree t ON e.manager_id = t.id
)
SELECT * FROM org_tree;

-- Full-text search
SELECT * FROM products
WHERE to_tsvector('english', name || ' ' || description)
      @@ to_tsquery('english', 'wireless & headphones');
```

**MySQL**:

```sql
-- Generated columns
CREATE TABLE products (
    id INT PRIMARY KEY,
    price DECIMAL(10,2),
    tax_rate DECIMAL(4,2),
    total_price DECIMAL(10,2) GENERATED ALWAYS AS (price * (1 + tax_rate)) STORED
);

-- JSON functions
SELECT
    id,
    JSON_EXTRACT(metadata, '$.category') as category
FROM products
WHERE JSON_CONTAINS(metadata, '"electronics"', '$.tags');

-- Full-text search
ALTER TABLE products ADD FULLTEXT(name, description);
SELECT * FROM products
WHERE MATCH(name, description) AGAINST('wireless headphones' IN NATURAL LANGUAGE MODE);
```

**SQL Server**:

```sql
-- Window functions with ROWS/RANGE
SELECT
    date,
    amount,
    SUM(amount) OVER (
        ORDER BY date
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) as rolling_7day
FROM transactions;

-- JSON support
SELECT
    id,
    JSON_VALUE(data, '$.name') as name,
    JSON_QUERY(data, '$.addresses') as addresses
FROM customers
WHERE JSON_VALUE(data, '$.status') = 'active';

-- Temporal tables (system-versioned)
CREATE TABLE products (
    id INT PRIMARY KEY,
    name NVARCHAR(100),
    price DECIMAL(10,2),
    valid_from DATETIME2 GENERATED ALWAYS AS ROW START,
    valid_to DATETIME2 GENERATED ALWAYS AS ROW END,
    PERIOD FOR SYSTEM_TIME (valid_from, valid_to)
) WITH (SYSTEM_VERSIONING = ON);

-- Query historical data
SELECT * FROM products FOR SYSTEM_TIME AS OF '2024-01-01';
```

## Best Practices

- **Profile before optimizing** - Use EXPLAIN ANALYZE
- **Index selectively** - Indexes have write overhead
- **Avoid SELECT *** - Specify needed columns
- **Use appropriate data types** - Smaller is faster
- **Batch large operations** - Don't update 1M rows at once
- **Monitor slow queries** - Log and review regularly
- **Test with production-like data** - Volume matters
- **Keep statistics updated** - ANALYZE/UPDATE STATISTICS

## Common Patterns

### Pattern 1: Upsert (Insert or Update)

```sql
-- PostgreSQL
INSERT INTO products (id, name, price)
VALUES (1, 'Widget', 9.99)
ON CONFLICT (id) DO UPDATE
SET name = EXCLUDED.name, price = EXCLUDED.price;

-- MySQL
INSERT INTO products (id, name, price)
VALUES (1, 'Widget', 9.99)
ON DUPLICATE KEY UPDATE
name = VALUES(name), price = VALUES(price);

-- SQL Server
MERGE INTO products AS target
USING (VALUES (1, 'Widget', 9.99)) AS source (id, name, price)
ON target.id = source.id
WHEN MATCHED THEN UPDATE SET name = source.name, price = source.price
WHEN NOT MATCHED THEN INSERT (id, name, price) VALUES (source.id, source.name, source.price);
```

### Pattern 2: Running Totals

```sql
SELECT
    date,
    amount,
    SUM(amount) OVER (ORDER BY date) as running_total
FROM transactions;
```

### Pattern 3: Gap and Island Detection

```sql
-- Find consecutive date ranges
WITH numbered AS (
    SELECT
        date,
        date - (ROW_NUMBER() OVER (ORDER BY date) * INTERVAL '1 day') as grp
    FROM events
)
SELECT
    MIN(date) as start_date,
    MAX(date) as end_date,
    COUNT(*) as consecutive_days
FROM numbered
GROUP BY grp
ORDER BY start_date;
```

## Quality Checklist

- [ ] Query uses indexes effectively (EXPLAIN verified)
- [ ] No SELECT * in production queries
- [ ] JOINs are on indexed columns
- [ ] No functions on indexed columns in WHERE
- [ ] Large operations are batched
- [ ] Pagination uses keyset method
- [ ] Appropriate indexes created
- [ ] Query tested with production data volume

## Related Skills

- `performance-review` - Database performance assessment
- `code-quality` - SQL code standards
- `security-review` - SQL injection prevention
- `terraform-specialist` - Database infrastructure

---

**Version**: 1.0.0
**Last Updated**: January 2026
**Based on**: Use the Index, Luke; awesome-claude-code-subagents patterns


### Iterative Refinement Strategy
This skill is optimized for an iterative approach:
1. **Execute**: Perform the core steps defined above.
2. **Review**: Critically analyze the output (coverage, quality, completeness).
3. **Refine**: If targets aren't met, repeat the specific implementation steps with improved context.
4. **Loop**: Continue until the definition of done is satisfied.
