---
name: ecc-postgres-patterns
description: Quick reference for PostgreSQL best practices. Use when writing SQL queries, designing database schemas, configuring indexes, implementing Row Level Security, setting up connection pooling, or troubleshooting slow queries.
version: "1.0.0"
verified_date: 2026-06-01
category: database
---

# PostgreSQL Patterns

## Purpose
Provide a highly optimized, high-fidelity PostgreSQL query design, database schema configuration, index optimization, and performance monitoring diagnostics guide.

## When to Use This Skill
- Designing schema datatypes and constraints for database tables.
- Building composite, GIN, BRIN, covering, or partial indexes.
- Implementing optimized Row Level Security (RLS) policies.
- Running diagnostics to identify slow queries, table bloat, or missing foreign key indexes.

## Output Format / Delivery
Provide highly optimized SQL query scripts, index configurations, or RLS policies. Ensure composite indexes prioritize equality columns before range columns, and timeouts are systematically configured.

## Behavior Rules
1. **Never use random UUIDs or generic varchar(255) as default datatypes** without a domain reason — favor `bigint`/`text` or structured maps.
2. **Never build indexes concurrently inside transactions** — concurrent indexes must run in isolated connections.
3. **Always wrap RLS policy user-id subqueries in SELECT statements** to allow Postgres to compile and cache them efficiently.
4. **Never query without statement and transaction timeouts** — prevent connection exhaustion in production.

## Maintenance Notes
This skill is locked for PostgreSQL v15+ features. Update when new major postgres releases introduce advanced core indexing structures.

---

## Phase 1: PostgreSQL Quick Reference Cheat Sheets

### Index Cheat Sheet

| Query Pattern | Index Type | Example |
|--------------|------------|---------|
| `WHERE col = value` | B-tree (default) | `CREATE INDEX idx ON t (col)` |
| `WHERE col > value` | B-tree | `CREATE INDEX idx ON t (col)` |
| `WHERE a = x AND b > y` | Composite | `CREATE INDEX idx ON t (a, b)` |
| `WHERE jsonb @> '{}'` | GIN | `CREATE INDEX idx ON t USING gin (col)` |
| `WHERE tsv @@ query` | GIN | `CREATE INDEX idx ON t USING gin (col)` |
| Time-series ranges | BRIN | `CREATE INDEX idx ON t USING brin (col)` |

### Data Type Quick Reference

| Use Case | Correct Type | Avoid |
|----------|-------------|-------|
| IDs | `bigint` | `int`, random UUID |
| Strings | `text` | `varchar(255)` |
| Timestamps | `timestamptz` | `timestamp` |
| Money | `numeric(10,2)` | `float` |
| Flags | `boolean` | `varchar`, `int` |

---

## Phase 2: Common PostgreSQL Query Patterns

**Composite Index Order:**
```sql
-- Equality columns first, then range columns
CREATE INDEX idx ON orders (status, created_at);
-- Works for: WHERE status = 'pending' AND created_at > '2024-01-01'
```

**Covering Index:**
```sql
CREATE INDEX idx ON users (email) INCLUDE (name, created_at);
-- Avoids table lookup for SELECT email, name, created_at
```

**Partial Index:**
```sql
CREATE INDEX idx ON users (email) WHERE deleted_at IS NULL;
-- Smaller index, only includes active users
```

**RLS Policy (Optimized):**
```sql
CREATE POLICY policy ON orders
  USING ((SELECT auth.uid()) = user_id);  -- Wrap in SELECT!
```

**UPSERT:**
```sql
INSERT INTO settings (user_id, key, value)
VALUES (123, 'theme', 'dark')
ON CONFLICT (user_id, key)
DO UPDATE SET value = EXCLUDED.value;
```

**Cursor Pagination:**
```sql
SELECT * FROM products WHERE id > $last_id ORDER BY id LIMIT 20;
-- O(1) vs OFFSET which is O(n)
```

**Queue Processing:**
```sql
UPDATE jobs SET status = 'processing'
WHERE id = (
  SELECT id FROM jobs WHERE status = 'pending'
  ORDER BY created_at LIMIT 1
  FOR UPDATE SKIP LOCKED
) RETURNING *;
```

---

## Phase 3: Diagnostic and Configuration Patterns

### Anti-Pattern Detection

```sql
-- Find unindexed foreign keys
SELECT conrelid::regclass, a.attname
FROM pg_constraint c
JOIN pg_attribute a ON a.attrelid = c.conrelid AND a.attnum = ANY(c.conkey)
WHERE c.contype = 'f'
  AND NOT EXISTS (
    SELECT 1 FROM pg_index i
    WHERE i.indrelid = c.conrelid AND a.attnum = ANY(i.indkey)
  );

-- Find slow queries
SELECT query, mean_exec_time, calls
FROM pg_stat_statements
WHERE mean_exec_time > 100
ORDER BY mean_exec_time DESC;

-- Check table bloat
SELECT relname, n_dead_tup, last_vacuum
FROM pg_stat_user_tables
WHERE n_dead_tup > 1000
ORDER BY n_dead_tup DESC;
```

### Configuration Template

```sql
-- Connection limits (adjust for RAM)
ALTER SYSTEM SET max_connections = 100;
ALTER SYSTEM SET work_mem = '8MB';

-- Timeouts
ALTER SYSTEM SET idle_in_transaction_session_timeout = '30s';
ALTER SYSTEM SET statement_timeout = '30s';

-- Monitoring
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- Security defaults
REVOKE ALL ON SCHEMA public FROM public;

SELECT pg_reload_conf();
```
