---
name: database-architect
description: "Universal standards for relational and NoSQL database modeling, non-blocking zero-downtime migrations, composite index ordering, and ACID transaction safety."
---

# Database Architecture & Migration Protocol

When designing tables, writing queries, creating indexes, or executing database migrations, adhere strictly to these engineering rules.

---

## 1. Zero-Downtime Migration Discipline

Never execute destructive or locking schema changes in a single operation:

1. **Expanding Columns (Additive Phase)**:
   - Add new nullable columns or columns with defaults:
     `ALTER TABLE orders ADD COLUMN status_code VARCHAR(32) DEFAULT 'pending';`
2. **Backfill Phase**:
   - Backfill data in batched chunks (e.g. 500-1000 rows at a time) to prevent table locks and replication lag.
3. **Dual-Writing / Transition Phase**:
   - Application writes to both old and new columns, reading from the new column with fallback to old.
4. **Contracting Phase (Cleanup)**:
   - Remove deprecated columns only after all services have ceased reading from them:
     `ALTER TABLE orders DROP COLUMN legacy_status;`

---

## 2. Indexing Strategy & Composite Rules

### The Equality-Range-Sort Rule
When creating composite indexes for filtering and sorting, arrange columns in this precise sequence:
1. **Equality columns**: Fields filtered with `=` or `IN`.
2. **Sort columns**: Fields used in `ORDER BY`.
3. **Range columns**: Fields filtered with `<`, `>`, `<=`, `>=`, `BETWEEN`.

Example query:
```sql
SELECT id, total FROM orders WHERE organization_id = 'org_1' AND created_at >= '2026-01-01' ORDER BY created_at DESC;
```
Optimal composite index:
```sql
CREATE INDEX idx_orders_org_created ON orders (organization_id, created_at DESC);
```

### Prevention of Redundant Indexes
Do not create index `(a)` if index `(a, b)` already exists. Leftmost prefix matching allows queries on `a` alone to leverage `(a, b)`.

---

## 3. Query Optimization & N+1 Eradication

1. **Eliminate N+1 Queries**:
   - Always load relationships using explicit `JOIN`, batch loading (e.g. `WHERE id IN (...)`), or DataLoader patterns.
2. **Select Only Required Columns**:
   - Never use `SELECT *` in production services. Enforce explicit column projection to reduce network I/O and enable index-only covering scans.
3. **Use EXPLAIN ANALYZE**:
   - Run `EXPLAIN ANALYZE` on any query touching high-velocity tables (>100k rows) to verify index usage and detect sequential table scans.

---

## 4. Concurrency & Transaction Safety

1. **Pessimistic vs Optimistic Locking**:
   - Use optimistic locking with version columns (`version INT DEFAULT 1`) for high-concurrency read-heavy operations:
     `UPDATE accounts SET balance = balance - 100, version = version + 1 WHERE id = 42 AND version = 3;`
   - Use `SELECT ... FOR UPDATE` only when strict pessimistic reservation is mandatory (e.g. seat booking inventory).
2. **Keep Transactions Short**:
   - Never perform external HTTP requests, file uploads, or third-party API calls inside database transaction blocks.
