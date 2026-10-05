---
name: database-design
description: Database design expertise including schema modeling, normalization, indexing strategies, migration patterns, and query optimization. Use when designing.
---

# Database Design

Comprehensive guidance for designing relational and non-relational database schemas, applying normalization theory, building effective indexing strategies, writing performant queries, and executing safe schema migrations across PostgreSQL, MySQL, and document stores.

## When to Use This Skill

Use this skill for:

- Designing new database schemas from business requirements
- Normalizing or intentionally denormalizing existing schemas
- Creating indexing strategies for read-heavy or write-heavy workloads
- Analyzing and optimizing slow queries with EXPLAIN plans
- Planning zero-downtime schema migrations
- Choosing between relational, document, graph, or time-series databases
- Implementing partitioning, sharding, or replication topologies
- Reviewing connection pooling and resource management
- Designing audit trails, soft deletes, or temporal data models

**Trigger phrases**: "database design", "schema design", "normalization", "indexing strategy", "query optimization", "EXPLAIN plan", "database migration", "schema migration", "denormalization", "partitioning", "connection pooling", "ER diagram"

## What This Skill Does

Provides production-grade database patterns including:

- **Schema Modeling**: Entity-relationship design, normalization forms (1NF through BCNF), denormalization trade-offs
- **Indexing**: B-tree, hash, GIN, GiST, composite, partial, and covering index strategies
- **Query Optimization**: EXPLAIN analysis, N+1 prevention, join strategies, query planning
- **Migrations**: Schema versioning, backward-compatible changes, zero-downtime deployment
- **Database Selection**: Relational vs document vs graph vs time-series decision framework
- **Operational**: Connection pooling, partitioning, replication, backup strategies

## Instructions

### Step 1: Gather Requirements and Model Entities

Begin by identifying entities, their attributes, and the relationships between them. Translate business language into a conceptual model before writing any DDL.

**Entity-Relationship Analysis Checklist**:

1. List all nouns in the business domain (these become candidate entities)
2. Identify attributes for each entity (columns)
3. Determine relationships and their cardinality (1:1, 1:N, M:N)
4. Mark required vs optional attributes (NOT NULL constraints)
5. Identify natural keys vs surrogate keys

**Example: E-Commerce Domain Model**:

```
┌──────────────┐     1:N     ┌──────────────┐     N:1     ┌──────────────┐
│   Customer   │────────────▶│    Order      │◀───────────│   Product    │
├──────────────┤             ├──────────────┤             ├──────────────┤
│ id (PK)      │             │ id (PK)      │             │ id (PK)      │
│ email (UQ)   │             │ customer_id  │             │ sku (UQ)     │
│ name         │             │ status       │             │ name         │
│ created_at   │             │ total        │             │ price        │
└──────────────┘             │ created_at   │             │ category_id  │
                             └──────┬───────┘             └──────────────┘
                                    │ 1:N
                             ┌──────▼───────┐
                             │  Order Item  │
                             ├──────────────┤
                             │ id (PK)      │
                             │ order_id     │
                             │ product_id   │
                             │ quantity     │
                             │ unit_price   │
                             └──────────────┘
```

**PostgreSQL Schema from the Model**:

```sql
-- Use UUID primary keys for distributed-friendly design
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE customers (
    id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email       VARCHAR(255) NOT NULL UNIQUE,
    name        VARCHAR(200) NOT NULL,
    created_at  TIMESTAMPTZ  NOT NULL DEFAULT now(),
    updated_at  TIMESTAMPTZ  NOT NULL DEFAULT now()
);

CREATE TABLE products (
    id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    sku         VARCHAR(50)  NOT NULL UNIQUE,
    name        VARCHAR(300) NOT NULL,
    price       NUMERIC(12,2) NOT NULL CHECK (price >= 0),
    category_id UUID REFERENCES categories(id),
    created_at  TIMESTAMPTZ  NOT NULL DEFAULT now()
);

CREATE TABLE orders (
    id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    customer_id UUID NOT NULL REFERENCES customers(id),
    status      VARCHAR(20) NOT NULL DEFAULT 'pending'
                CHECK (status IN ('pending','confirmed','shipped','delivered','cancelled')),
    total       NUMERIC(14,2) NOT NULL DEFAULT 0 CHECK (total >= 0),
    created_at  TIMESTAMPTZ  NOT NULL DEFAULT now()
);

CREATE TABLE order_items (
    id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    order_id    UUID NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    product_id  UUID NOT NULL REFERENCES products(id),
    quantity    INT  NOT NULL CHECK (quantity > 0),
    unit_price  NUMERIC(12,2) NOT NULL CHECK (unit_price >= 0),
    UNIQUE (order_id, product_id)
);
```

### Step 2: Apply Normalization Rules

Normalization eliminates redundancy and prevents update anomalies. Apply each form sequentially.

**First Normal Form (1NF)**: Every column holds atomic values; no repeating groups.

```sql
-- VIOLATION: comma-separated tags in a single column
CREATE TABLE products_bad (
    id   SERIAL PRIMARY KEY,
    name TEXT,
    tags TEXT  -- 'electronics,sale,featured'
);

-- 1NF FIX: separate junction table
CREATE TABLE products (
    id   SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE tags (
    id   SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE product_tags (
    product_id INT REFERENCES products(id),
    tag_id     INT REFERENCES tags(id),
    PRIMARY KEY (product_id, tag_id)
);
```

**Second Normal Form (2NF)**: Every non-key column depends on the entire primary key (relevant for composite keys).

```sql
-- VIOLATION: product_name depends only on product_id, not on (order_id, product_id)
CREATE TABLE order_items_bad (
    order_id     INT,
    product_id   INT,
    product_name TEXT,   -- depends only on product_id
    quantity     INT,
    PRIMARY KEY (order_id, product_id)
);

-- 2NF FIX: move product_name to the products table
CREATE TABLE order_items (
    order_id   INT REFERENCES orders(id),
    product_id INT REFERENCES products(id),
    quantity   INT NOT NULL,
    PRIMARY KEY (order_id, product_id)
);
-- product_name lives in products table only
```

**Third Normal Form (3NF)**: No transitive dependencies (non-key column depends on another non-key column).

```sql
-- VIOLATION: city depends on zip_code, not directly on customer_id
CREATE TABLE customers_bad (
    id       SERIAL PRIMARY KEY,
    name     TEXT,
    zip_code VARCHAR(10),
    city     TEXT           -- transitively dependent via zip_code
);

-- 3NF FIX: extract zip-to-city mapping
CREATE TABLE zip_codes (
    zip_code VARCHAR(10) PRIMARY KEY,
    city     TEXT NOT NULL,
    state    VARCHAR(2) NOT NULL
);

CREATE TABLE customers (
    id       SERIAL PRIMARY KEY,
    name     TEXT NOT NULL,
    zip_code VARCHAR(10) REFERENCES zip_codes(zip_code)
);
```

**Boyce-Codd Normal Form (BCNF)**: Every determinant is a candidate key. Relevant when a table has overlapping composite candidate keys.

**When to Denormalize**:

| Scenario | Denormalization Technique | Trade-off |
|----------|--------------------------|-----------|
| Read-heavy dashboards | Materialized views | Stale data between refreshes |
| Frequently joined columns | Redundant column copy | Must sync on update |
| Aggregation queries | Pre-computed summary tables | Write amplification |
| High-traffic lookups | Caching layer (Redis) | Cache invalidation complexity |

### Step 3: Design an Indexing Strategy

Indexes accelerate reads but slow writes. Choose index types based on query patterns.

**Index Type Selection Guide**:

| Index Type | Use Case | PostgreSQL Syntax |
|-----------|----------|-------------------|
| B-tree (default) | Equality, range, sorting | `CREATE INDEX ...` |
| Hash | Equality only (rare) | `CREATE INDEX ... USING hash` |
| GIN | Full-text search, JSONB, arrays | `CREATE INDEX ... USING gin` |
| GiST | Geometric, range types, nearest-neighbor | `CREATE INDEX ... USING gist` |
| BRIN | Very large, naturally ordered tables | `CREATE INDEX ... USING brin` |

**Composite Index Design** (column order matters):

```sql
-- Query: WHERE customer_id = ? AND status = ? ORDER BY created_at DESC
-- Rule: equality columns first, then range/sort columns
CREATE INDEX idx_orders_customer_status_date
    ON orders (customer_id, status, created_at DESC);
```

**Partial Index** (index only relevant rows):

```sql
-- Only index active orders (80% of queries target non-cancelled orders)
CREATE INDEX idx_orders_active
    ON orders (customer_id, created_at DESC)
    WHERE status != 'cancelled';
```

**Covering Index** (includes all columns the query needs):

```sql
-- Query: SELECT email, name FROM customers WHERE email = ?
-- Covering index avoids heap lookup
CREATE INDEX idx_customers_email_covering
    ON customers (email) INCLUDE (name);
```

**JSONB Indexing** (PostgreSQL):

```sql
-- GIN index for JSONB containment queries (@>)
CREATE INDEX idx_products_metadata
    ON products USING gin (metadata);

-- Targeted path index for a specific key
CREATE INDEX idx_products_metadata_color
    ON products ((metadata->>'color'));
```

### Step 4: Optimize Queries with EXPLAIN

Use `EXPLAIN ANALYZE` to understand query execution and identify bottlenecks.

**Reading EXPLAIN Output (PostgreSQL)**:

```sql
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT o.id, o.total, c.email
FROM orders o
JOIN customers c ON c.id = o.customer_id
WHERE o.status = 'pending'
  AND o.created_at > now() - INTERVAL '7 days'
ORDER BY o.created_at DESC
LIMIT 50;
```

**Example Output and Analysis**:

```
Limit  (cost=0.72..125.40 rows=50 width=72) (actual time=0.05..1.23 rows=50 loops=1)
  -> Nested Loop  (cost=0.72..5420.18 rows=2170 width=72) (actual time=0.05..1.20 rows=50 loops=1)
       -> Index Scan Backward using idx_orders_active on orders o
            (cost=0.43..2890.12 rows=2170 width=48) (actual time=0.03..0.45 rows=50 loops=1)
              Filter: (status = 'pending' AND created_at > ...)
       -> Index Scan using customers_pkey on customers c
            (cost=0.29..1.17 rows=1 width=24) (actual time=0.01..0.01 rows=1 loops=50)
              Index Cond: (id = o.customer_id)
Planning Time: 0.35 ms
Execution Time: 1.45 ms
Buffers: shared hit=198
```

**Key Metrics to Watch**:

| Metric | Good | Investigate |
|--------|------|-------------|
| Seq Scan on large table | < 1K rows | > 10K rows |
| Nested Loop | Small inner set | Large inner set |
| Sort | In-memory | On-disk (work_mem too small) |
| Buffers shared read | Low | High (data not in cache) |
| Rows removed by filter | Low ratio | High ratio (index not selective) |

**Preventing N+1 Queries**:

```sql
-- BAD: N+1 pattern (1 query for orders + N queries for items)
-- Application code: for order in orders: fetch items(order.id)

-- GOOD: single JOIN query
SELECT o.id, o.total, oi.product_id, oi.quantity
FROM orders o
JOIN order_items oi ON oi.order_id = o.id
WHERE o.customer_id = $1
ORDER BY o.created_at DESC;

-- GOOD: lateral join for "top N per group"
SELECT o.id, items.*
FROM orders o
CROSS JOIN LATERAL (
    SELECT oi.product_id, oi.quantity
    FROM order_items oi
    WHERE oi.order_id = o.id
    ORDER BY oi.quantity DESC
    LIMIT 3
) items
WHERE o.customer_id = $1;
```

### Step 5: Plan Schema Migrations

Safe migrations require backward compatibility, reversibility, and zero-downtime awareness.

**Migration Versioning with a Tool (e.g., Flyway, Alembic, Knex)**:

```
migrations/
  V001__create_customers.sql
  V002__create_products.sql
  V003__create_orders.sql
  V004__add_customer_phone.sql
  V005__add_orders_shipped_at.sql
```

**Zero-Downtime Migration Pattern: Adding a Column**:

```sql
-- Step 1: Add column as nullable (no lock, backward compatible)
ALTER TABLE customers ADD COLUMN phone VARCHAR(20);

-- Step 2: Backfill in batches (avoid long-running transactions)
UPDATE customers SET phone = 'unknown'
WHERE phone IS NULL AND id IN (
    SELECT id FROM customers WHERE phone IS NULL LIMIT 10000
);

-- Step 3: Add NOT NULL constraint (only after all rows populated)
ALTER TABLE customers ALTER COLUMN phone SET NOT NULL;

-- Step 4: Add default for future inserts
ALTER TABLE customers ALTER COLUMN phone SET DEFAULT '';
```

**Zero-Downtime Migration Pattern: Renaming a Column**:

```sql
-- NEVER do: ALTER TABLE customers RENAME COLUMN name TO full_name;
-- This breaks application code that references "name".

-- SAFE approach (expand-contract pattern):
-- Phase 1: Add new column, copy data, create trigger
ALTER TABLE customers ADD COLUMN full_name VARCHAR(200);
UPDATE customers SET full_name = name;

CREATE OR REPLACE FUNCTION sync_customer_name() RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' OR TG_OP = 'UPDATE' THEN
        NEW.full_name = COALESCE(NEW.full_name, NEW.name);
        NEW.name = COALESCE(NEW.name, NEW.full_name);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_sync_name BEFORE INSERT OR UPDATE ON customers
FOR EACH ROW EXECUTE FUNCTION sync_customer_name();

-- Phase 2: Deploy application reading from full_name
-- Phase 3: Drop old column and trigger after all consumers migrated
ALTER TABLE customers DROP COLUMN name;
DROP TRIGGER trg_sync_name ON customers;
DROP FUNCTION sync_customer_name();
```

**Alembic Migration Example (Python/SQLAlchemy)**:

```python
"""Add phone column to customers.

Revision ID: a1b2c3d4
Revises: z9y8x7w6
"""
from alembic import op
import sqlalchemy as sa

revision = 'a1b2c3d4'
down_revision = 'z9y8x7w6'

def upgrade():
    op.add_column('customers', sa.Column('phone', sa.String(20), nullable=True))

def downgrade():
    op.drop_column('customers', 'phone')
```

### Step 6: Choose the Right Database Engine

**Decision Framework**:

| Requirement | Best Fit | Examples |
|-------------|----------|---------|
| ACID transactions, complex JOINs | Relational | PostgreSQL, MySQL |
| Flexible schema, nested documents | Document | MongoDB, CouchDB |
| Relationship traversal (social graphs) | Graph | Neo4j, Amazon Neptune |
| Time-ordered metrics, IoT data | Time-series | TimescaleDB, InfluxDB |
| Key-value caching, sessions | Key-value | Redis, DynamoDB |
| Full-text search, analytics | Search engine | Elasticsearch, OpenSearch |

**PostgreSQL vs MySQL Quick Comparison**:

```sql
-- PostgreSQL: richer type system, JSONB, CTEs, window functions
-- Supports partial indexes, GIN/GiST, LISTEN/NOTIFY
SELECT id, name,
       ROW_NUMBER() OVER (PARTITION BY category_id ORDER BY price DESC) as rank
FROM products;

-- MySQL: widely deployed, simpler replication setup
-- InnoDB for ACID; supports JSON type since 5.7
SELECT id, name,
       ROW_NUMBER() OVER (PARTITION BY category_id ORDER BY price DESC) as row_rank
FROM products;
```

### Step 7: Configure Connection Pooling and Operational Patterns

**PgBouncer Configuration Example**:

```ini
; pgbouncer.ini
[databases]
myapp = host=127.0.0.1 port=5432 dbname=myapp

[pgbouncer]
listen_port = 6432
listen_addr = 0.0.0.0
auth_type = md5
auth_file = /etc/pgbouncer/userlist.txt

; Pool sizing: connections = (2 * cpu_cores) + disk_spindles
pool_mode = transaction
default_pool_size = 25
max_client_conn = 200
min_pool_size = 5
reserve_pool_size = 5
reserve_pool_timeout = 3

; Timeouts
server_idle_timeout = 600
client_idle_timeout = 0
query_timeout = 30
```

**Application-Level Pooling (Node.js with pg)**:

```javascript
const { Pool } = require('pg');

const pool = new Pool({
  host: process.env.DB_HOST,
  port: 5432,
  database: 'myapp',
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  max: 20,                  // max connections in pool
  idleTimeoutMillis: 30000, // close idle connections after 30s
  connectionTimeoutMillis: 5000,
  statement_timeout: 30000, // kill queries after 30s
});

// Graceful shutdown
process.on('SIGTERM', async () => {
  await pool.end();
  process.exit(0);
});
```

**Table Partitioning (PostgreSQL)**:

```sql
-- Range partitioning by date (ideal for time-series or log data)
CREATE TABLE events (
    id         UUID NOT NULL DEFAULT uuid_generate_v4(),
    event_type VARCHAR(50) NOT NULL,
    payload    JSONB,
    created_at TIMESTAMPTZ NOT NULL
) PARTITION BY RANGE (created_at);

-- Create monthly partitions
CREATE TABLE events_2026_01 PARTITION OF events
    FOR VALUES FROM ('2026-01-01') TO ('2026-02-01');
CREATE TABLE events_2026_02 PARTITION OF events
    FOR VALUES FROM ('2026-02-01') TO ('2026-03-01');
CREATE TABLE events_2026_03 PARTITION OF events
    FOR VALUES FROM ('2026-03-01') TO ('2026-04-01');

-- Index each partition (automatically inherited)
CREATE INDEX idx_events_type_date ON events (event_type, created_at DESC);

-- Automate partition creation with pg_partman
CREATE EXTENSION pg_partman;
SELECT partman.create_parent('public.events', 'created_at', 'native', 'monthly');
```

## Best Practices

- **Always use constraints**: CHECK, NOT NULL, UNIQUE, and FOREIGN KEY constraints prevent bad data at the source
- **Prefer UUID or BIGSERIAL over SERIAL**: UUIDs work well in distributed systems; BIGSERIAL avoids 32-bit overflow
- **Use TIMESTAMPTZ, not TIMESTAMP**: Always store timestamps with timezone to avoid ambiguity
- **Index foreign keys**: Every FK column should have a supporting index for JOIN performance
- **Name objects consistently**: Use `snake_case` for tables and columns; prefix indexes with `idx_`
- **Version your schema**: Use migration tools (Flyway, Alembic, Knex) rather than ad-hoc DDL scripts
- **Test migrations against production-size data**: A migration that takes 2 seconds on 1,000 rows may lock the table for 20 minutes on 10 million rows
- **Monitor slow queries**: Enable `pg_stat_statements` or MySQL slow query log in all environments
- **Keep transactions short**: Long transactions hold locks and block other operations
- **Use read replicas for analytics**: Route reporting queries to replicas to protect primary write performance

## Common Patterns

### Pattern 1: Soft Deletes with Filtered Index

```sql
-- Add a deleted_at column instead of actually deleting rows
ALTER TABLE customers ADD COLUMN deleted_at TIMESTAMPTZ;

-- Partial index so active-record queries ignore deleted rows
CREATE INDEX idx_customers_active_email
    ON customers (email)
    WHERE deleted_at IS NULL;

-- Application query automatically uses the filtered index
SELECT * FROM customers WHERE email = $1 AND deleted_at IS NULL;
```

### Pattern 2: Audit Trail with Trigger

```sql
CREATE TABLE audit_log (
    id         BIGSERIAL PRIMARY KEY,
    table_name VARCHAR(100) NOT NULL,
    record_id  UUID NOT NULL,
    action     VARCHAR(10) NOT NULL,  -- INSERT, UPDATE, DELETE
    old_data   JSONB,
    new_data   JSONB,
    changed_by VARCHAR(100),
    changed_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE OR REPLACE FUNCTION audit_trigger_fn() RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO audit_log (table_name, record_id, action, old_data, new_data, changed_by)
    VALUES (
        TG_TABLE_NAME,
        COALESCE(NEW.id, OLD.id),
        TG_OP,
        CASE WHEN TG_OP IN ('UPDATE','DELETE') THEN to_jsonb(OLD) END,
        CASE WHEN TG_OP IN ('INSERT','UPDATE') THEN to_jsonb(NEW) END,
        current_setting('app.current_user', true)
    );
    RETURN COALESCE(NEW, OLD);
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER audit_customers
    AFTER INSERT OR UPDATE OR DELETE ON customers
    FOR EACH ROW EXECUTE FUNCTION audit_trigger_fn();
```

### Pattern 3: Optimistic Locking

```sql
-- Add a version column for conflict detection
ALTER TABLE products ADD COLUMN version INT NOT NULL DEFAULT 1;

-- Update with version check (application retries on 0 rows affected)
UPDATE products
SET price = $1, version = version + 1
WHERE id = $2 AND version = $3;
-- If rowcount == 0, another writer changed the row; re-read and retry
```

### Pattern 4: Materialized View for Dashboards

```sql
CREATE MATERIALIZED VIEW mv_daily_sales AS
SELECT
    date_trunc('day', o.created_at)::DATE AS sale_date,
    COUNT(DISTINCT o.id) AS order_count,
    SUM(o.total) AS revenue,
    COUNT(DISTINCT o.customer_id) AS unique_customers
FROM orders o
WHERE o.status != 'cancelled'
GROUP BY 1;

CREATE UNIQUE INDEX idx_mv_daily_sales_date ON mv_daily_sales (sale_date);

-- Refresh concurrently (no read lock) on a schedule
REFRESH MATERIALIZED VIEW CONCURRENTLY mv_daily_sales;
```

## Quality Checklist

- [ ] Entity-relationship model documented before writing DDL
- [ ] All tables have a primary key (UUID or BIGSERIAL)
- [ ] Foreign key constraints defined for every relationship
- [ ] CHECK constraints enforce domain rules (positive prices, valid statuses)
- [ ] Schema is in 3NF (intentional denormalization documented with rationale)
- [ ] Indexes exist for all foreign keys and common query patterns
- [ ] EXPLAIN ANALYZE run on critical queries with production-like data
- [ ] No N+1 query patterns in application code
- [ ] Migration scripts are versioned and tested with rollback
- [ ] Zero-downtime migration strategy for production deployments
- [ ] Connection pooling configured with appropriate limits
- [ ] Timestamps use TIMESTAMPTZ (not TIMESTAMP)
- [ ] Naming conventions are consistent (snake_case, `idx_` prefixes)

## Related Skills

- `sql-expert` - Advanced SQL query writing and optimization
- `cloud-architect` - Managed database service selection (RDS, Cloud SQL, Aurora)
- `cicd-architect` - Running migrations in deployment pipelines
- `performance-review` - Identifying database-related performance bottlenecks

---

**Version**: 1.0.0
**Last Updated**: March 2026

### Iterative Refinement Strategy
This skill is optimized for an iterative approach:
1. **Execute**: Perform the core steps defined above.
2. **Review**: Critically analyze the output (coverage, quality, completeness).
3. **Refine**: If targets aren't met, repeat the specific implementation steps with improved context.
4. **Loop**: Continue until the definition of done is satisfied.
