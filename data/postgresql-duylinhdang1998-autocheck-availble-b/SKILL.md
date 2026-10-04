---
name: postgresql
description: Production PostgreSQL expertise from Amazon/Netflix engineers. Use when designing database schemas, writing complex SQL queries, optimizing query performance with EXPLAIN ANALYZE, creating indexes, setting up replication, configuring connection pooling (PgBouncer), implementing migrations, or tuning PostgreSQL for high throughput. Triggers on PostgreSQL, Postgres, SQL queries, database schema, indexes, migrations, or relational database optimization.
---

# PostgreSQL - Production Database Expertise

**Purpose**: Master PostgreSQL for building scalable, reliable data storage systems

**Agent**: Amazon Cloud Architect / Netflix Backend Architect
**Use When**: Designing database schemas, optimizing queries, or building data-intensive applications

---

## Overview

PostgreSQL is the world's most advanced open-source relational database, offering ACID compliance, complex queries, and extensibility.

**Core Features**:
- ACID compliance (reliability)
- Advanced data types (JSON, arrays, hstore)
- Full-text search
- Geospatial data (PostGIS)
- Transactions and concurrency
- Extensible (custom functions, types)

---

## Core Concepts

### 1. Data Types

```sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  name TEXT NOT NULL,
  age INTEGER CHECK (age >= 0),
  balance DECIMAL(10, 2) DEFAULT 0.00,
  is_active BOOLEAN DEFAULT true,
  metadata JSONB,
  tags TEXT[],
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

### 2. Indexes for Performance

```sql
-- B-tree index (default, good for = and range queries)
CREATE INDEX idx_users_email ON users(email);

-- Partial index (index subset of rows)
CREATE INDEX idx_active_users ON users(email)
WHERE is_active = true;

-- Composite index (multiple columns)
CREATE INDEX idx_users_name_email ON users(name, email);

-- GIN index (for JSONB, arrays, full-text search)
CREATE INDEX idx_users_metadata ON users USING GIN(metadata);
CREATE INDEX idx_users_tags ON users USING GIN(tags);

-- Check indexes
\d users
```

### 3. Constraints

```sql
CREATE TABLE orders (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  total DECIMAL(10, 2) NOT NULL CHECK (total >= 0),
  status VARCHAR(20) NOT NULL CHECK (status IN ('pending', 'paid', 'shipped')),
  created_at TIMESTAMP DEFAULT NOW(),
  CONSTRAINT unique_user_order UNIQUE (user_id, created_at)
);
```

### 4. Relationships

```sql
-- One-to-Many
CREATE TABLE posts (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id),
  title TEXT NOT NULL,
  content TEXT
);

-- Many-to-Many
CREATE TABLE posts_tags (
  post_id INTEGER REFERENCES posts(id),
  tag_id INTEGER REFERENCES tags(id),
  PRIMARY KEY (post_id, tag_id)
);

-- Join query
SELECT posts.*, users.name as author_name
FROM posts
INNER JOIN users ON posts.user_id = users.id;
```

---

## Query Optimization

### 1. Use EXPLAIN ANALYZE

```sql
-- Check query performance
EXPLAIN ANALYZE
SELECT * FROM users WHERE email = 'john@example.com';

-- Look for:
-- - Seq Scan (bad) → add index
-- - Index Scan (good)
-- - Execution time
```

### 2. Avoid N+1 Queries

```sql
-- ❌ Bad: N+1 problem (multiple queries)
SELECT * FROM users; -- 1 query
-- Then for each user:
SELECT * FROM posts WHERE user_id = ?; -- N queries

-- ✅ Good: Single query with JOIN
SELECT users.*,
       json_agg(posts) as posts
FROM users
LEFT JOIN posts ON posts.user_id = users.id
GROUP BY users.id;
```

### 3. Use Proper Indexes

```sql
-- Slow without index
SELECT * FROM orders WHERE created_at > '2024-01-01';

-- Fast with index
CREATE INDEX idx_orders_created_at ON orders(created_at);
```

### 4. Limit Results

```sql
-- Pagination
SELECT * FROM users
ORDER BY created_at DESC
LIMIT 20 OFFSET 40; -- Page 3 (20 per page)

-- Better: Use cursor-based pagination
SELECT * FROM users
WHERE id > 100 -- Last ID from previous page
ORDER BY id
LIMIT 20;
```

---

## Advanced Features

### 1. JSONB Operations

```sql
-- Insert JSONB data
INSERT INTO users (email, name, metadata)
VALUES ('john@example.com', 'John', '{"age": 30, "city": "NYC"}');

-- Query JSONB
SELECT * FROM users
WHERE metadata->>'city' = 'NYC';

-- Update JSONB
UPDATE users
SET metadata = metadata || '{"premium": true}'
WHERE id = 1;

-- JSONB index for fast queries
CREATE INDEX idx_users_metadata_city
ON users((metadata->>'city'));
```

### 2. Array Operations

```sql
-- Insert array
INSERT INTO users (email, name, tags)
VALUES ('jane@example.com', 'Jane', ARRAY['admin', 'developer']);

-- Query array
SELECT * FROM users WHERE 'admin' = ANY(tags);
SELECT * FROM users WHERE tags @> ARRAY['admin']; -- Contains

-- Array functions
SELECT * FROM users WHERE array_length(tags, 1) > 2;
```

### 3. Full-Text Search

```sql
-- Add tsvector column
ALTER TABLE posts ADD COLUMN search_vector tsvector;

-- Create index
CREATE INDEX idx_posts_search
ON posts USING GIN(search_vector);

-- Update search vector
UPDATE posts
SET search_vector = to_tsvector('english', title || ' ' || content);

-- Search
SELECT * FROM posts
WHERE search_vector @@ to_tsquery('english', 'postgresql & performance');

-- With ranking
SELECT *, ts_rank(search_vector, query) AS rank
FROM posts, to_tsquery('english', 'postgresql') query
WHERE search_vector @@ query
ORDER BY rank DESC;
```

### 4. Transactions

```sql
BEGIN;

UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;

-- If everything is OK
COMMIT;

-- If error occurred
-- ROLLBACK;
```

### 5. Window Functions

```sql
-- Row number
SELECT
  name,
  salary,
  ROW_NUMBER() OVER (ORDER BY salary DESC) as rank
FROM employees;

-- Running total
SELECT
  date,
  amount,
  SUM(amount) OVER (ORDER BY date) as running_total
FROM sales;

-- Partition by category
SELECT
  category,
  product,
  price,
  AVG(price) OVER (PARTITION BY category) as avg_category_price
FROM products;
```

---

## Best Practices

### 1. Use Connection Pooling

```typescript
// With Prisma
const prisma = new PrismaClient({
  datasources: {
    db: {
      url: process.env.DATABASE_URL
    }
  },
  // Connection pool settings
  log: ['query', 'error', 'warn'],
})

// With node-postgres
import { Pool } from 'pg'

const pool = new Pool({
  host: 'localhost',
  port: 5432,
  database: 'mydb',
  user: 'postgres',
  password: 'password',
  max: 20, // Max clients in pool
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
})

const result = await pool.query('SELECT * FROM users WHERE id = $1', [1])
```

### 2. Use Prepared Statements (Prevent SQL Injection)

```sql
-- ❌ Bad: SQL injection vulnerability
SELECT * FROM users WHERE email = 'user_input';

-- ✅ Good: Parameterized query
SELECT * FROM users WHERE email = $1;
```

```typescript
// Node.js example
const email = req.body.email

// ✅ Safe from SQL injection
const result = await pool.query(
  'SELECT * FROM users WHERE email = $1',
  [email]
)
```

### 3. Regular VACUUM and ANALYZE

```sql
-- Reclaim storage and update statistics
VACUUM ANALYZE users;

-- Auto-vacuum (configure in postgresql.conf)
autovacuum = on
```

### 4. Monitor Performance

```sql
-- Long-running queries
SELECT pid, now() - query_start as duration, query
FROM pg_stat_activity
WHERE state = 'active'
ORDER BY duration DESC;

-- Kill long query
SELECT pg_terminate_backend(pid);

-- Table sizes
SELECT
  schemaname,
  tablename,
  pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

---

## Common Patterns

### Soft Delete

```sql
ALTER TABLE users ADD COLUMN deleted_at TIMESTAMP;

-- Soft delete
UPDATE users SET deleted_at = NOW() WHERE id = 1;

-- Query only active records
SELECT * FROM users WHERE deleted_at IS NULL;

-- Create view for active records
CREATE VIEW active_users AS
SELECT * FROM users WHERE deleted_at IS NULL;
```

### Audit Trail

```sql
CREATE TABLE audit_log (
  id SERIAL PRIMARY KEY,
  table_name VARCHAR(50),
  record_id INTEGER,
  action VARCHAR(20), -- INSERT, UPDATE, DELETE
  old_data JSONB,
  new_data JSONB,
  user_id INTEGER,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Trigger function
CREATE OR REPLACE FUNCTION audit_trigger_func()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO audit_log (table_name, record_id, action, old_data, new_data)
  VALUES (
    TG_TABLE_NAME,
    NEW.id,
    TG_OP,
    row_to_json(OLD),
    row_to_json(NEW)
  );
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Attach trigger
CREATE TRIGGER users_audit_trigger
AFTER INSERT OR UPDATE OR DELETE ON users
FOR EACH ROW EXECUTE FUNCTION audit_trigger_func();
```

### UUID Primary Keys

```sql
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE products (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name TEXT NOT NULL,
  price DECIMAL(10, 2)
);
```

---

## Migrations

```sql
-- migrations/001_create_users.sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  name TEXT NOT NULL
);

-- migrations/002_add_created_at.sql
ALTER TABLE users ADD COLUMN created_at TIMESTAMP DEFAULT NOW();

-- migrations/003_add_index.sql
CREATE INDEX idx_users_email ON users(email);
```

With Prisma:
```bash
npx prisma migrate dev --name add_user_table
npx prisma migrate deploy # Production
```

---

## Backup & Restore

```bash
# Backup
pg_dump -U postgres mydb > backup.sql
pg_dump -U postgres -Fc mydb > backup.dump  # Compressed

# Restore
psql -U postgres mydb < backup.sql
pg_restore -U postgres -d mydb backup.dump

# Backup to remote
pg_dump -U postgres mydb | gzip | ssh user@remote 'cat > backup.sql.gz'
```

---

**Remember**: PostgreSQL is powerful but needs tuning. Use indexes wisely, avoid N+1 queries, and monitor performance regularly.

**Created**: 2026-02-04
**Maintained By**: Amazon Cloud Architect
**Version**: PostgreSQL 14+
