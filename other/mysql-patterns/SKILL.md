---
name: mysql-patterns
description: MySQL database patterns for query optimization, schema design, indexing, and security. Quick reference for common patterns.
---

# MySQL Patterns

Quick reference for MySQL best practices. For detailed guidance, use the `mysql-database-reviewer` agent.

## When to Activate

- Writing SQL queries or migrations
- Designing database schemas
- Troubleshooting slow queries
- Setting up connection pooling
- Implementing multi-tenant isolation

## Quick Reference

### Index Cheat Sheet

| Query Pattern             | Index Type       | Example                               |
| ------------------------- | ---------------- | ------------------------------------- |
| `WHERE col = value`       | B-tree (default) | `CREATE INDEX idx ON t (col)`         |
| `WHERE col > value`       | B-tree           | `CREATE INDEX idx ON t (col)`         |
| `WHERE a = x AND b > y`   | Composite        | `CREATE INDEX idx ON t (a, b)`        |
| `MATCH(...) AGAINST(...)` | FULLTEXT         | `CREATE FULLTEXT INDEX ft ON t (col)` |
| Long string prefix        | Prefix           | `CREATE INDEX idx ON t (col(50))`     |
| Geographic data           | SPATIAL          | `CREATE SPATIAL INDEX idx ON t (col)` |

### Data Type Quick Reference

| Use Case      | Correct Type      | Avoid                        |
| ------------- | ----------------- | ---------------------------- |
| IDs           | `bigint unsigned` | `int`, random UUID as PK     |
| Business code | `varchar(64)`     | `char`, `text`               |
| Strings       | `varchar(n)`      | `text` for short strings     |
| Timestamps    | `datetime`        | `timestamp` (2038 problem)   |
| Money         | `decimal(10,2)`   | `float`, `double`            |
| Flags         | `tinyint`         | `varchar`, `boolean` literal |
| Status        | `tinyint`         | `enum` (hard to modify)      |
| JSON data     | `json`            | `text` for structured data   |

### Common Patterns

**Composite Index Order:**

```sql
-- Equality columns first, then range columns
CREATE INDEX idx_status_created ON t_order (status, created_at);
-- Works for: WHERE status = 'pending' AND created_at > '2024-01-01'
-- Does NOT work for: WHERE created_at > '2024-01-01' alone
```

**Prefix Index (Long Strings):**

```sql
CREATE INDEX idx_url ON t_page (url(100));
-- Index only first 100 characters
```

**Generated Column + Index (JSON):**

```sql
ALTER TABLE t_product
ADD COLUMN brand varchar(100) GENERATED ALWAYS AS (attributes->>'$.brand') STORED;
CREATE INDEX idx_brand ON t_product (brand);
```

**UPSERT (ON DUPLICATE KEY):**

```sql
INSERT INTO t_setting (user_code, `key`, `value`)
VALUES ('u123', 'theme', 'dark')
ON DUPLICATE KEY UPDATE
  `value` = VALUES(`value`),
  updated_at = NOW();
```

**Cursor Pagination:**

```sql
SELECT * FROM t_product WHERE id > ? ORDER BY id LIMIT 20;
-- O(1) vs OFFSET which is O(n)
```

**Queue Processing (MySQL 8.0+):**

```sql
START TRANSACTION;
SELECT * FROM t_job
WHERE status = 'pending'
ORDER BY created_at LIMIT 1
FOR UPDATE SKIP LOCKED;
-- Process job...
UPDATE t_job SET status = 'processing' WHERE id = ?;
COMMIT;
```

**Batch Insert:**

```sql
INSERT INTO t_event (user_code, action) VALUES
  ('u1', 'click'),
  ('u2', 'view'),
  ('u3', 'click');
-- 1 round trip instead of 3
```

### Anti-Pattern Detection

```sql
-- Find tables without primary key
SELECT t.table_name
FROM information_schema.tables t
LEFT JOIN information_schema.key_column_usage k
  ON t.table_schema = k.table_schema
  AND t.table_name = k.table_name
  AND k.constraint_name = 'PRIMARY'
WHERE t.table_schema = DATABASE()
  AND k.constraint_name IS NULL
  AND t.table_type = 'BASE TABLE';

-- Find slow queries (performance_schema)
SELECT DIGEST_TEXT, COUNT_STAR,
  ROUND(AVG_TIMER_WAIT/1000000000, 2) as avg_ms
FROM performance_schema.events_statements_summary_by_digest
WHERE AVG_TIMER_WAIT > 100000000  -- > 100ms
ORDER BY AVG_TIMER_WAIT DESC LIMIT 10;

-- Find unused indexes (sys schema)
SELECT * FROM sys.schema_unused_indexes
WHERE object_schema = DATABASE();

-- Find redundant indexes
SELECT * FROM sys.schema_redundant_indexes
WHERE table_schema = DATABASE();

-- Check table fragmentation
SELECT table_name, data_free,
  ROUND(data_free/(data_length+index_length+data_free)*100, 2) as frag_pct
FROM information_schema.tables
WHERE table_schema = DATABASE() AND data_free > 1000000
ORDER BY data_free DESC;
```

### Configuration Template

```sql
-- Connection limits
SET GLOBAL max_connections = 200;
SET GLOBAL max_user_connections = 50;

-- Timeouts
SET GLOBAL wait_timeout = 300;
SET GLOBAL interactive_timeout = 600;
SET GLOBAL max_execution_time = 30000;  -- 30s query timeout (MySQL 5.7.8+)

-- Slow query log
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 1;
SET GLOBAL log_queries_not_using_indexes = 'ON';

-- InnoDB settings (my.cnf recommended)
-- innodb_buffer_pool_size = 70% of RAM
-- innodb_log_file_size = 256M
-- innodb_flush_log_at_trx_commit = 1
```

### Table Template

```sql
CREATE TABLE `t_example` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT 'PK',
  `example_code` varchar(64) NOT NULL COMMENT 'Business code (UUID)',

  -- Business fields here
  `status` tinyint NOT NULL DEFAULT 1 COMMENT '0-inactive, 1-active',

  -- Audit fields (5 fields)
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Creation time',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Update time',
  `created_by` varchar(64) NOT NULL DEFAULT '' COMMENT 'Creator (user_code)',
  `updated_by` varchar(64) NOT NULL DEFAULT '' COMMENT 'Modifier (user_code)',
  `deleted_at` datetime DEFAULT NULL COMMENT 'Soft delete marker',

  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_example_code` (`example_code`),
  KEY `idx_status` (`status`),
  KEY `idx_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### EXPLAIN Analysis

```sql
EXPLAIN ANALYZE SELECT * FROM t_order WHERE user_code = 'u123';
```

| Indicator         | Problem             | Solution           |
| ----------------- | ------------------- | ------------------ |
| `type: ALL`       | Full table scan     | Add index          |
| `type: index`     | Full index scan     | Check WHERE        |
| `Using filesort`  | Sorting not indexed | Add ORDER BY index |
| `Using temporary` | Temp table          | Optimize GROUP BY  |
| High `rows`       | Poor selectivity    | Review conditions  |

## Related

- Agent: `mysql-database-reviewer` - Full database review workflow

---

_Quick reference for MySQL 5.7+ / 8.0+_
