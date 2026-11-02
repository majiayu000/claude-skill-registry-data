---
name: database-query-optimizer
description: Advanced database query optimization, EXPLAIN ANALYZE interpretation, indexing strategies, and deadlock prevention. Use when debugging slow SQL queries, analyzing query plans, designing composite or partial indexes, or resolving database connection bottlenecks.
allowed-tools: Read, Write, Edit, Glob, Grep
version: 1.0
category: database-sql-relational
---

# Database Query Optimizer

> **EXPLAIN ANALYZE Interpretation, Indexing Architecture & High-Throughput SQL Tuning**

---

## 🏗️ Core Principles

| Principle | Rule |
|-----------|------|
| **Analyze the Plan, Don't Guess** | Always run `EXPLAIN (ANALYZE, BUFFERS)` to see actual execution times, sequential scans, buffer hits, and disk spills. |
| **Index for Selectivity** | Put the most selective equality columns first in composite indexes (Equality, Range, Sort - ESR rule). |
| **Partial Indexes for Active Data** | When filtering on flags like `status = 'pending'`, use partial indexes (`WHERE status = 'pending'`) to save index size and memory. |
| **Covering Indexes** | Include frequently selected columns (`INCLUDE (col1, col2)`) to allow Index-Only Scans without touching table heap pages. |
| **Pagination via Keyset (Cursor)** | Never use large `OFFSET` values (`OFFSET 100000`). Use keyset pagination (`WHERE id > last_seen_id ORDER BY id LIMIT 20`). |

---

## 📋 Reading EXPLAIN ANALYZE Output

```sql
EXPLAIN (ANALYZE, BUFFERS) 
SELECT id, title, created_at 
FROM orders 
WHERE customer_id = 42 AND created_at >= '2026-01-01'
ORDER BY created_at DESC 
LIMIT 25;
```

### Key Metrics to Look For:
1. **`Seq Scan` on Large Table**: Missing index. Add `INDEX idx_orders_customer_date ON orders(customer_id, created_at DESC)`.
2. **`Buffers: shared hit=12 read=450`**: High `read` indicates disk I/O; high `hit` means queries are served from RAM buffer pool.
3. **`Sort Method: external merge Disk`**: Memory limit exceeded (`work_mem`). Sort spilled to disk. Increase `work_mem` for batch sessions or optimize sort index.

---

## 📋 Deadlock Prevention Pattern

- Always acquire locks or update rows in consistent deterministic order across all application transactions (e.g., sort IDs before running `UPDATE ... WHERE id IN (...)`).
- Keep transactions as short as possible; never make network calls or external API requests while holding open a database transaction.

---

## ❌ Anti-Patterns

- ❌ Using functions in `WHERE` clauses that invalidate indexes: `WHERE DATE(created_at) = '2026-01-01'` instead of range queries `WHERE created_at >= '2026-01-01' AND created_at < '2026-01-02'`.
- ❌ Indexing low-cardinality boolean columns globally (creates bloated, unused indexes).
- ❌ Running `SELECT *` across multi-table joins.
