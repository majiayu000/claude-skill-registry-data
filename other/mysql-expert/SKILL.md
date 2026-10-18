---
name: mysql-expert
description: "Design, optimize, and maintain MySQL databases. Covers schema design, indexing strategies, query optimization, replication, and performance tuning."
category: php-frameworks
tags: ['mysql', 'database', 'sql', 'optimization', 'indexing']
complexity: advanced
risk: low
compatibility: [claude-code, antigravity, gemini-cli, cursor, copilot, codex-cli, autohand, kiro]
source: antigravity-official
version: "1.0.0"
date_added: "2026-07-10"
last_updated: "2026-07-10"
---

# MySQL Expert

## Purpose
Build high-performance MySQL databases with optimal schema design, indexing, and query strategies for production workloads.

## Operating Mode
You are a **MySQL DBA and performance engineer**. You diagnose slow queries, design optimal schemas, and implement scaling strategies.

## The Process

### 1️⃣ Schema Design Principles
```sql
-- ✅ Best practices
CREATE TABLE users (
    id          BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    uuid        CHAR(36) NOT NULL,           -- expose UUID, hide internal id
    email       VARCHAR(255) NOT NULL,
    name        VARCHAR(100) NOT NULL,
    status      ENUM('active','inactive','suspended') NOT NULL DEFAULT 'active',
    created_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at  DATETIME NULL,               -- soft deletes
    
    PRIMARY KEY (id),
    UNIQUE KEY uq_users_uuid (uuid),
    UNIQUE KEY uq_users_email (email),
    INDEX idx_users_status (status),
    INDEX idx_users_created (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### 2️⃣ Indexing Strategies
```sql
-- Composite index (order matters: equality first, range last)
CREATE INDEX idx_orders_user_status_date 
    ON orders (user_id, status, created_at);

-- Covering index (include all columns needed)
CREATE INDEX idx_posts_search
    ON posts (status, published_at, id, title, excerpt);

-- Full-text index for search
ALTER TABLE posts ADD FULLTEXT INDEX ft_posts_content (title, body);

-- Query using full-text
SELECT *, MATCH(title, body) AGAINST('laravel api' IN BOOLEAN MODE) AS score
FROM posts
WHERE MATCH(title, body) AGAINST('laravel api' IN BOOLEAN MODE)
ORDER BY score DESC;
```

### 3️⃣ Query Optimization
```sql
-- Analyze slow queries
EXPLAIN ANALYZE
SELECT u.name, COUNT(o.id) as order_count, SUM(o.total) as revenue
FROM users u
INNER JOIN orders o ON o.user_id = u.id
WHERE o.created_at >= '2026-01-01'
  AND o.status = 'completed'
GROUP BY u.id
ORDER BY revenue DESC
LIMIT 10;

-- Use EXPLAIN to check index usage
-- Look for: type=ref or range (good), type=ALL (bad - full scan)

-- Avoid SELECT * in production
-- Avoid functions on indexed columns in WHERE: WHERE YEAR(created_at) = 2026 (BAD)
-- Use: WHERE created_at BETWEEN '2026-01-01' AND '2026-12-31' (GOOD)
```

### 4️⃣ Transactions & Locking
```sql
-- Pessimistic locking (SELECT FOR UPDATE)
START TRANSACTION;
SELECT balance FROM accounts WHERE id = 1 FOR UPDATE;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;

-- Optimistic locking (version column)
UPDATE products SET stock = stock - 1, version = version + 1
WHERE id = 1 AND version = 5;
-- Check affected rows = 1, else retry
```

### 5️⃣ Replication & Scaling
```sql
-- Read replicas configuration
-- Primary: all writes
-- Replica: all reads

-- In application:
-- $db->write()->insert(...);
-- $db->read()->select(...);

-- Partitioning for large tables
ALTER TABLE events PARTITION BY RANGE (YEAR(created_at)) (
    PARTITION p2024 VALUES LESS THAN (2025),
    PARTITION p2025 VALUES LESS THAN (2026),
    PARTITION p2026 VALUES LESS THAN (2027),
    PARTITION pFuture VALUES LESS THAN MAXVALUE
);
```

### 6️⃣ Performance Tuning (my.cnf)
```ini
[mysqld]
innodb_buffer_pool_size = 4G        # 70% of RAM for dedicated MySQL server
innodb_log_file_size = 512M
innodb_flush_log_at_trx_commit = 2  # Slight durability trade-off for performance
query_cache_type = 0                # Disable query cache (deprecated in 8.0)
slow_query_log = 1
slow_query_log_file = /var/log/mysql/slow.log
long_query_time = 1                 # Log queries > 1 second
max_connections = 500
```

### 7️⃣ Backup Strategy
```bash
# Daily full backup with mysqldump
mysqldump --single-transaction --routines --triggers   --all-databases | gzip > backup_$(date +%Y%m%d).sql.gz

# Point-in-time recovery with binary logs
mysqlbinlog /var/log/mysql/mysql-bin.000001 | mysql -u root -p

# Use Percona XtraBackup for hot backups on large DBs
```

## Outputs
1. Optimized schema with proper data types
2. Indexing strategy for all query patterns
3. EXPLAIN analysis of slow queries
4. Replication setup guide
5. Backup and recovery runbook
6. Performance monitoring queries
