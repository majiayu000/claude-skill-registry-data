---
name: sql-optimization
description: "Always start with EXPLAIN ANALYZE to understand execution:"
---

# SQL Optimization (Verbose)

## Core Patterns

### Query Execution Plans
Always start with EXPLAIN ANALYZE to understand execution:
```sql
EXPLAIN ANALYZE 
SELECT o.order_id, o.total, c.name
FROM orders o
JOIN customers c ON o.customer_id = c.id
WHERE o.created_at > '2026-01-01'
ORDER BY o.total DESC
LIMIT 100;
```

Look for:
- **Seq Scan**: Full table scan (avoid for large tables)
- **Index Scan**: Uses index (good)
- **Index Cond**: Filters applied via index (excellent)
- **Filter**: Filters applied after scan (less efficient)

### Index Strategy
```sql
-- Single column index (simple filtering)
CREATE INDEX idx_orders_customer ON orders(customer_id);

-- Multi-column index (multiple conditions)
CREATE INDEX idx_orders_date_status ON orders(created_at, status);

-- Partial index (condition built-in)
CREATE INDEX idx_active_orders ON orders(customer_id) 
WHERE status IN ('pending', 'processing');

-- Expression index (for computed values)
CREATE INDEX idx_age_calc ON customers(EXTRACT(YEAR FROM age(birth_date)));
```

### Avoiding N+1 Problems
```python
# ❌ BAD: N+1 queries (1 + 1000)
orders = db.query("SELECT * FROM orders LIMIT 1000")
for order in orders:
    customer = db.query("SELECT * FROM customers WHERE id = ?", order.customer_id)
    # Query fired 1000 times!

# ✅ GOOD: Single query with join
orders = db.query("""
  SELECT o.*, c.name, c.email
  FROM orders o
  JOIN customers c ON o.customer_id = c.id
  LIMIT 1000
""")
```

### Pagination Patterns
```sql
-- Avoid OFFSET for large datasets (expensive)
SELECT * FROM orders LIMIT 100 OFFSET 100000;  -- Slow!

-- Use keyset pagination instead
SELECT * FROM orders 
WHERE order_id > 100000
LIMIT 100;  -- Fast!
```

### Common Anti-Patterns

**SELECT * (avoid):**
```sql
-- ❌ Fetches unused columns, wastes bandwidth
SELECT * FROM orders WHERE customer_id = 123;

-- ✅ Fetch only needed columns
SELECT order_id, total, status FROM orders WHERE customer_id = 123;
```

**Functions in WHERE clause:**
```sql
-- ❌ Can't use index
SELECT * FROM orders WHERE YEAR(created_at) = 2026;

-- ✅ Uses index
SELECT * FROM orders 
WHERE created_at >= '2026-01-01' 
  AND created_at < '2027-01-01';
```

**Wildcard at start:**
```sql
-- ❌ Can't use index
SELECT * FROM customers WHERE name LIKE '%john%';

-- ✅ Uses index (prefix match)
SELECT * FROM customers WHERE name LIKE 'john%';
```

## Query Optimization Checklist

- [ ] Use EXPLAIN ANALYZE
- [ ] Add indexes on filtered columns
- [ ] Avoid N+1 queries with joins
- [ ] Use appropriate data types
- [ ] Avoid functions in WHERE
- [ ] Use LIMIT for pagination
- [ ] Monitor slow query logs
