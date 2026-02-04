---
name: data-modeling-patterns
description: Database schema design and data modeling patterns including normalization principles (1NF-5NF), denormalization trade-offs, entity relationship design, indexing strategies, schema evolution, and domain-driven design patterns. Activates when designing new database schemas, refactoring data models, discussing normalization vs denormalization decisions, planning schema migrations, or modeling complex domain entities. Use when creating new tables/collections, redesigning existing schemas, evaluating relationship patterns, or making data integrity decisions.
---

# Data Modeling Patterns

## Overview

Data models are the foundation of every application. Get them right, and your application scales smoothly. Get them wrong, and you're stuck with expensive migrations and workarounds.

This skill provides systematic approaches to database schema design, from normalization principles to performance trade-offs, helping you make informed modeling decisions upfront.

**When to use this skill:**
- Designing new database schemas or tables
- Refactoring existing data models
- Evaluating normalization vs denormalization trade-offs
- Planning schema migrations and evolution
- Modeling complex domain entities and relationships
- Optimizing query performance through schema design

---

## Quick Decision Framework

### 1. Start with Your Access Patterns

**Most important question**: How will you query this data?

```
Common access patterns → Schema design choices:
├─ Frequent joins across tables → Normalized (3NF)
├─ High read volume, rare writes → Denormalized
├─ Complex aggregations → Materialized views or denormalization
├─ Real-time queries → Indexed columns, partition keys
└─ Historical tracking → Event sourcing or audit tables
```

### 2. Choose Normalization Level

| Normalization Level | When to Use | Trade-offs |
|-------------------|-------------|------------|
| **1NF** (Atomic values) | Always - baseline | None, always do this |
| **2NF** (No partial dependencies) | Most cases | Minimal overhead |
| **3NF** (No transitive dependencies) | Default for OLTP | Standard approach, good balance |
| **BCNF** (Strict 3NF) | Data integrity critical | Slightly more complex |
| **4NF/5NF** (Multi-valued dependencies) | Rare - only when many-to-many relationships complex | Query complexity increases |
| **Denormalized** | High read volume, read performance critical | Write complexity, data redundancy |

**Rule of thumb**: Start with 3NF, denormalize only with evidence of performance issues.

---

## Core Modeling Patterns

### Pattern 1: Normalized Schema (3NF)

**When to use:**
- Transactional systems (OLTP)
- Data integrity is critical
- Frequent updates to data
- Storage efficiency matters
- Standard relational databases (PostgreSQL, MySQL)

**Example: E-commerce Order System**

```sql
-- 3NF: Separate tables for each entity, no redundancy

-- Users table (1 entity = 1 table)
CREATE TABLE users (
    user_id         UUID PRIMARY KEY,
    email           VARCHAR(255) UNIQUE NOT NULL,
    username        VARCHAR(100) UNIQUE NOT NULL,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Products table (separate entity)
CREATE TABLE products (
    product_id      UUID PRIMARY KEY,
    name            VARCHAR(255) NOT NULL,
    description     TEXT,
    base_price      DECIMAL(10,2) NOT NULL,
    category_id     UUID REFERENCES categories(category_id),
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Orders table (no redundant data from users/products)
CREATE TABLE orders (
    order_id        UUID PRIMARY KEY,
    user_id         UUID REFERENCES users(user_id) NOT NULL,
    status          VARCHAR(50) NOT NULL,
    total_amount    DECIMAL(10,2) NOT NULL,  -- Computed from order_items
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Order items (junction table for many-to-many)
CREATE TABLE order_items (
    order_item_id   UUID PRIMARY KEY,
    order_id        UUID REFERENCES orders(order_id) NOT NULL,
    product_id      UUID REFERENCES products(product_id) NOT NULL,
    quantity        INTEGER NOT NULL CHECK (quantity > 0),
    unit_price      DECIMAL(10,2) NOT NULL,  -- Snapshot price at order time
    UNIQUE (order_id, product_id)  -- Prevent duplicate items
);
```

**Benefits:**
- ✅ No data duplication (single source of truth)
- ✅ Easy updates (change product price in one place)
- ✅ Data integrity enforced by foreign keys
- ✅ Storage efficient

**Trade-offs:**
- ❌ Requires joins to get complete data
- ❌ More complex queries
- ❌ Slower for read-heavy workloads

**Normalization checklist:**
- [ ] **1NF**: All columns contain atomic values (no arrays, no JSON)
- [ ] **2NF**: No partial dependencies (every non-key column depends on entire primary key)
- [ ] **3NF**: No transitive dependencies (non-key columns don't depend on other non-key columns)

---

### Pattern 2: Denormalized Schema (Read-Optimized)

**When to use:**
- Read-heavy workloads (10:1 or higher read:write ratio)
- Query performance critical (sub-100ms response time)
- Acceptable data redundancy
- Analytics/reporting systems (OLAP)
- NoSQL databases (MongoDB, DynamoDB)

**Example: Product Catalog (Denormalized)**

```sql
-- Denormalized: Embed related data to avoid joins

CREATE TABLE product_catalog (
    product_id          UUID PRIMARY KEY,
    name                VARCHAR(255) NOT NULL,
    description         TEXT,
    base_price          DECIMAL(10,2) NOT NULL,

    -- Denormalized category data (duplicated across products)
    category_id         UUID,
    category_name       VARCHAR(100),  -- Duplicated!
    category_path       VARCHAR(500),  -- e.g., "Electronics > Computers > Laptops"

    -- Denormalized inventory data
    stock_quantity      INTEGER,  -- Duplicated from inventory table
    warehouse_location  VARCHAR(100),  -- Duplicated!

    -- Denormalized aggregate metrics
    total_sales         INTEGER DEFAULT 0,  -- Computed, updated periodically
    average_rating      DECIMAL(3,2),  -- Computed from reviews
    review_count        INTEGER DEFAULT 0,  -- Computed

    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for common queries
CREATE INDEX idx_category ON product_catalog(category_id);
CREATE INDEX idx_price ON product_catalog(base_price);
CREATE INDEX idx_rating ON product_catalog(average_rating);
```

**Benefits:**
- ✅ Fast queries (no joins needed)
- ✅ Simple SQL (SELECT * FROM product_catalog WHERE...)
- ✅ Scales for reads (can cache entire rows)

**Trade-offs:**
- ❌ Data duplication (category_name stored in every product)
- ❌ Update complexity (change category_name → update all products)
- ❌ Data staleness risk (aggregates may be out of sync)
- ❌ Storage overhead

**When to denormalize:**
- Read:write ratio > 10:1
- Query performance requirements < 100ms
- Data changes infrequently (e.g., category names)
- Can tolerate eventual consistency

---

### Pattern 3: Hybrid (Normalized Core + Denormalized Views)

**When to use:**
- Need both data integrity and query performance
- Can use materialized views or caching layer
- Want best of both worlds

**Example: Orders with Materialized View**

```sql
-- Normalized core tables (source of truth)
CREATE TABLE orders (...);  -- As in Pattern 1
CREATE TABLE order_items (...);
CREATE TABLE products (...);
CREATE TABLE users (...);

-- Materialized view for read performance
CREATE MATERIALIZED VIEW order_details_mv AS
SELECT
    o.order_id,
    o.created_at,
    o.status,
    o.total_amount,
    u.user_id,
    u.email,
    u.username,
    json_agg(
        json_build_object(
            'product_id', p.product_id,
            'product_name', p.name,
            'quantity', oi.quantity,
            'unit_price', oi.unit_price
        )
    ) AS items
FROM orders o
JOIN users u ON o.user_id = u.user_id
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
GROUP BY o.order_id, u.user_id;

-- Refresh strategy
CREATE INDEX idx_order_created ON order_details_mv(created_at);
REFRESH MATERIALIZED VIEW CONCURRENTLY order_details_mv;  -- Periodic refresh
```

**Benefits:**
- ✅ Write to normalized tables (data integrity)
- ✅ Read from materialized view (fast queries)
- ✅ Best of both worlds

**Trade-offs:**
- ❌ View refresh overhead (minutes to hours)
- ❌ Stale data between refreshes
- ❌ More complexity (manage refresh schedule)

**Refresh strategies:**
- **Incremental**: Refresh only changed rows (CONCURRENTLY)
- **Scheduled**: Nightly refresh for reports
- **On-demand**: Trigger refresh after writes
- **Near real-time**: Use triggers or change data capture (CDC)

---

## Relationship Patterns

### One-to-Many (Most Common)

**Example**: User → Orders (one user, many orders)

```sql
CREATE TABLE users (
    user_id UUID PRIMARY KEY,
    ...
);

CREATE TABLE orders (
    order_id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(user_id) NOT NULL,  -- Foreign key
    ...
);

-- Query: Get user's orders
SELECT * FROM orders WHERE user_id = ?;

-- Index on foreign key for performance
CREATE INDEX idx_orders_user ON orders(user_id);
```

**Guidelines:**
- Always index the foreign key (user_id)
- Consider cascade delete: `ON DELETE CASCADE` (delete user → delete orders)
- Or restrict: `ON DELETE RESTRICT` (can't delete user with orders)

---

### Many-to-Many

**Example**: Products ↔ Tags (products have tags, tags have products)

```sql
-- Entities
CREATE TABLE products (
    product_id UUID PRIMARY KEY,
    ...
);

CREATE TABLE tags (
    tag_id UUID PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);

-- Junction table (associate products with tags)
CREATE TABLE product_tags (
    product_id UUID REFERENCES products(product_id) ON DELETE CASCADE,
    tag_id UUID REFERENCES tags(tag_id) ON DELETE CASCADE,
    PRIMARY KEY (product_id, tag_id)  -- Composite primary key
);

-- Query: Get products with tag "electronics"
SELECT p.*
FROM products p
JOIN product_tags pt ON p.product_id = pt.product_id
JOIN tags t ON pt.tag_id = t.tag_id
WHERE t.name = 'electronics';

-- Indexes
CREATE INDEX idx_product_tags_product ON product_tags(product_id);
CREATE INDEX idx_product_tags_tag ON product_tags(tag_id);
```

**Guidelines:**
- Use composite primary key (prevents duplicates)
- Index both foreign keys
- Consider adding metadata to junction table (e.g., created_at, priority)

---

### One-to-One (Rare)

**Example**: User → UserProfile (one user, one profile)

**Pattern 1: Separate table (for optional/large data)**
```sql
CREATE TABLE users (
    user_id UUID PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    ...
);

CREATE TABLE user_profiles (
    user_id UUID PRIMARY KEY REFERENCES users(user_id) ON DELETE CASCADE,
    bio TEXT,
    avatar_url VARCHAR(500),
    ...  -- Large/optional fields
);
```

**When to use separate table:**
- Profile fields optional (not all users have profiles)
- Profile data is large (TEXT columns, JSON blobs)
- Different access patterns (rarely need profile data)

**Pattern 2: Single table (for mandatory/small data)**
```sql
CREATE TABLE users (
    user_id UUID PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    bio TEXT,  -- Just include in users table
    avatar_url VARCHAR(500),
    ...
);
```

**When to use single table:**
- Profile always exists for every user
- Profile fields small/fixed-size
- Always queried together

---

### Self-Referencing (Hierarchies)

**Example**: Employee → Manager (employees manage other employees)

```sql
CREATE TABLE employees (
    employee_id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    manager_id UUID REFERENCES employees(employee_id),  -- Self-reference
    ...
);

-- Query: Get employee's manager
SELECT e.*, m.name AS manager_name
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.employee_id
WHERE e.employee_id = ?;

-- Query: Get all reports (recursive CTE)
WITH RECURSIVE reports AS (
    -- Base case: direct reports
    SELECT employee_id, name, manager_id, 1 AS level
    FROM employees
    WHERE manager_id = ?  -- Manager's ID

    UNION ALL

    -- Recursive case: reports of reports
    SELECT e.employee_id, e.name, e.manager_id, r.level + 1
    FROM employees e
    JOIN reports r ON e.manager_id = r.employee_id
)
SELECT * FROM reports ORDER BY level, name;
```

**Alternative: Adjacency List + Path (Optimized Reads)**
```sql
CREATE TABLE employees (
    employee_id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    manager_id UUID REFERENCES employees(employee_id),
    manager_path UUID[],  -- [CEO_id, VP_id, Director_id, Manager_id]
    ...
);

-- Query: Get all reports (simple array query)
SELECT * FROM employees WHERE ? = ANY(manager_path);

-- Trade-off: Faster reads, more complex writes (update path on reparenting)
```

---

## Indexing Strategy

### When to Add Indexes

**Always index:**
- Primary keys (automatic)
- Foreign keys (manually add)
- Columns in WHERE clauses (frequent filters)
- Columns in JOIN conditions
- Columns in ORDER BY (sorting)

**Example: Order queries**
```sql
-- Frequent queries → Need indexes

-- Query 1: Get user's orders
SELECT * FROM orders WHERE user_id = ?;
-- Index: CREATE INDEX idx_orders_user ON orders(user_id);

-- Query 2: Recent orders
SELECT * FROM orders WHERE created_at > ? ORDER BY created_at DESC;
-- Index: CREATE INDEX idx_orders_created ON orders(created_at DESC);

-- Query 3: Orders by status
SELECT * FROM orders WHERE status = 'pending';
-- Index: CREATE INDEX idx_orders_status ON orders(status);

-- Query 4: User's recent orders (composite)
SELECT * FROM orders WHERE user_id = ? AND created_at > ?;
-- Index: CREATE INDEX idx_orders_user_created ON orders(user_id, created_at DESC);
```

### Index Types

**B-Tree (Default)**: Most common, good for ranges, sorting
```sql
CREATE INDEX idx_price ON products(base_price);  -- Range queries (price > 10)
```

**Hash**: Equality only, faster for exact matches
```sql
CREATE INDEX idx_email ON users USING HASH(email);  -- WHERE email = ?
```

**GIN (Generalized Inverted Index)**: Full-text search, JSONB, arrays
```sql
CREATE INDEX idx_tags ON products USING GIN(tags);  -- Array contains queries
CREATE INDEX idx_metadata ON products USING GIN(metadata);  -- JSONB queries
```

**Partial Index**: Index subset of rows (save space)
```sql
-- Only index active users
CREATE INDEX idx_active_users ON users(user_id) WHERE status = 'active';
```

**Composite Index**: Multiple columns (order matters!)
```sql
-- Good for: WHERE user_id = ? AND created_at > ?
CREATE INDEX idx_user_created ON orders(user_id, created_at);

-- NOT good for: WHERE created_at > ? (doesn't use user_id part)
```

### Index Trade-offs

**Benefits:**
- ✅ Faster queries (10-1000x speedup)
- ✅ Efficient sorting and filtering

**Costs:**
- ❌ Slower writes (update index on INSERT/UPDATE/DELETE)
- ❌ Storage overhead (indexes take disk space)
- ❌ Maintenance overhead (vacuum, reindex)

**Rule of thumb**:
- Add index if query slow (>100ms) AND runs frequently (>100/day)
- Remove unused indexes (monitor with pg_stat_user_indexes)

---

## Schema Evolution Patterns

### Pattern 1: Backward-Compatible Changes (Safe)

**Add nullable column:**
```sql
-- Safe: Existing rows get NULL, no migration needed
ALTER TABLE products ADD COLUMN tags TEXT[];
```

**Add table:**
```sql
-- Safe: New table doesn't affect existing queries
CREATE TABLE product_images (...);
```

**Add index:**
```sql
-- Safe: Improves performance, no data changes
CREATE INDEX idx_products_category ON products(category_id);
```

---

### Pattern 2: Backward-Incompatible Changes (Risky)

**Remove column:**
```sql
-- RISKY: Breaks code that reads this column
ALTER TABLE products DROP COLUMN old_field;

-- Migration strategy:
-- 1. Remove code that uses old_field (deploy)
-- 2. Wait 1 week (verify no errors)
-- 3. Drop column (deploy schema change)
```

**Rename column:**
```sql
-- RISKY: Breaks code that references old name
ALTER TABLE products RENAME COLUMN old_name TO new_name;

-- Migration strategy:
-- 1. Add new column with new_name
-- 2. Backfill data (new_name = old_name)
-- 3. Update code to use new_name (deploy)
-- 4. Remove old column after 1 week
```

**Change column type:**
```sql
-- RISKY: May lose data or fail validation
ALTER TABLE products ALTER COLUMN price TYPE DECIMAL(12,2);  -- Was DECIMAL(10,2)

-- Migration strategy:
-- 1. Create new column (price_new DECIMAL(12,2))
-- 2. Backfill: UPDATE products SET price_new = price
-- 3. Update code to use price_new (deploy)
-- 4. Drop old column, rename new (deploy)
```

---

### Pattern 3: Online Migrations (Zero Downtime)

**Strategy**: Use triggers to keep old and new schemas in sync

```sql
-- Step 1: Add new column
ALTER TABLE products ADD COLUMN new_price DECIMAL(12,2);

-- Step 2: Backfill existing data (batched, don't lock table)
UPDATE products SET new_price = old_price WHERE new_price IS NULL LIMIT 1000;
-- Repeat until done

-- Step 3: Create trigger (keep in sync during transition)
CREATE TRIGGER sync_price
AFTER INSERT OR UPDATE ON products
FOR EACH ROW
EXECUTE FUNCTION sync_price_trigger();

-- Step 4: Deploy code that writes to both old_price and new_price

-- Step 5: Verify new_price matches old_price (no drift)

-- Step 6: Deploy code that reads from new_price only

-- Step 7: Remove trigger, drop old_price column
```

---

## Domain-Driven Design Patterns

### Entity Pattern

**Definition**: Object with unique identity (can change attributes, identity stays same)

**Example**: User
```sql
CREATE TABLE users (
    user_id UUID PRIMARY KEY,  -- Identity
    email VARCHAR(255) NOT NULL,  -- Attributes (can change)
    username VARCHAR(100) NOT NULL,
    ...
);

-- User identity (user_id) never changes
-- Attributes (email, username) can be updated
```

---

### Value Object Pattern

**Definition**: Object defined by attributes (no identity, immutable)

**Example**: Address (embedded in user table)
```sql
CREATE TABLE users (
    user_id UUID PRIMARY KEY,
    email VARCHAR(255) NOT NULL,

    -- Address value object (no separate identity)
    address_line1 VARCHAR(255),
    address_line2 VARCHAR(255),
    address_city VARCHAR(100),
    address_state VARCHAR(50),
    address_zip VARCHAR(20),
    address_country VARCHAR(50),
    ...
);

-- Alternative: Use JSONB for value objects
CREATE TABLE users (
    user_id UUID PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    address JSONB,  -- {"line1": "...", "city": "...", ...}
    ...
);
```

**When to embed vs separate table:**
- **Embed** (columns or JSONB): Small, always queried together, no relationships to other entities
- **Separate table**: Large, optional, has relationships, frequently joined

---

### Aggregate Pattern

**Definition**: Cluster of entities/value objects with consistency boundary

**Example**: Order aggregate (Order + OrderItems)
```sql
-- Aggregate root
CREATE TABLE orders (
    order_id UUID PRIMARY KEY,  -- Aggregate ID
    user_id UUID NOT NULL,
    status VARCHAR(50) NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    ...
);

-- Aggregate members (can't exist without order)
CREATE TABLE order_items (
    order_item_id UUID PRIMARY KEY,
    order_id UUID REFERENCES orders(order_id) ON DELETE CASCADE,  -- Cascade!
    product_id UUID NOT NULL,
    quantity INTEGER NOT NULL,
    ...
);

-- Consistency rule: Total amount = sum(order_items.quantity * unit_price)
-- Enforced by application logic, validated with triggers/constraints
```

**Aggregate guidelines:**
- All changes go through aggregate root (Order)
- Members can't be modified independently (OrderItems always via Order)
- Cascade delete (delete Order → delete OrderItems)
- Maintain invariants (total_amount consistency)

---

## Anti-Patterns to Avoid

### ❌ EAV (Entity-Attribute-Value) Anti-Pattern

**Problem**: Generic key-value schema kills SQL performance

**Bad example:**
```sql
-- DON'T DO THIS
CREATE TABLE entity_attributes (
    entity_id UUID NOT NULL,
    attribute_name VARCHAR(100) NOT NULL,
    attribute_value TEXT,
    PRIMARY KEY (entity_id, attribute_name)
);

-- Nightmare queries:
SELECT
    MAX(CASE WHEN attribute_name = 'name' THEN attribute_value END) AS name,
    MAX(CASE WHEN attribute_name = 'price' THEN attribute_value END) AS price,
    ...
FROM entity_attributes
WHERE entity_id = ?;
```

**Solution**: Use proper columns or JSONB
```sql
-- Option 1: Proper columns
CREATE TABLE products (
    product_id UUID PRIMARY KEY,
    name VARCHAR(255),
    price DECIMAL(10,2),
    ...
);

-- Option 2: JSONB for truly dynamic attributes
CREATE TABLE products (
    product_id UUID PRIMARY KEY,
    name VARCHAR(255),
    price DECIMAL(10,2),
    metadata JSONB  -- Dynamic attributes
);
```

---

### ❌ God Table Anti-Pattern

**Problem**: Single table with 50+ columns, no clear focus

**Bad example:**
```sql
-- DON'T DO THIS
CREATE TABLE everything (
    id UUID PRIMARY KEY,
    -- User fields
    email VARCHAR(255),
    username VARCHAR(100),
    -- Address fields
    address_line1 VARCHAR(255),
    address_city VARCHAR(100),
    -- Order fields
    last_order_date TIMESTAMP,
    total_orders INTEGER,
    -- ... 40 more columns
);
```

**Solution**: Normalize into focused tables
```sql
CREATE TABLE users (...);  -- User-specific fields
CREATE TABLE addresses (...);  -- Address fields
CREATE TABLE order_summary (...);  -- Aggregated order data
```

---

### ❌ Premature Denormalization

**Problem**: Denormalize before measuring performance

**When developers denormalize early:**
- "Joins are slow" (without evidence)
- "We need fast reads" (without requirements)
- "NoSQL is faster" (without benchmarks)

**Solution**:
1. Start normalized (3NF)
2. Measure actual query performance
3. Denormalize ONLY if:
   - Query >100ms AND
   - Runs >100x/day AND
   - Tried indexes/caching first

---

### ❌ Missing Foreign Key Constraints

**Problem**: Orphaned records, data integrity issues

**Bad example:**
```sql
-- DON'T DO THIS (no foreign key)
CREATE TABLE orders (
    order_id UUID PRIMARY KEY,
    user_id UUID NOT NULL,  -- No REFERENCES constraint
    ...
);

-- Result: Orphaned orders (user deleted, orders remain)
```

**Solution**: Always use foreign keys
```sql
CREATE TABLE orders (
    order_id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(user_id) ON DELETE RESTRICT,  -- Enforce referential integrity
    ...
);
```

**Exception**: Denormalized tables where data intentionally duplicated

---

## Testing Data Models

### Validation Checklist

- [ ] **Normalized to 3NF** (unless performance justifies denormalization)
- [ ] **Foreign keys** defined with appropriate ON DELETE behavior
- [ ] **Indexes** on foreign keys and frequent WHERE/ORDER BY columns
- [ ] **Unique constraints** on business keys (email, username, etc.)
- [ ] **NOT NULL** on required fields
- [ ] **CHECK constraints** for data validation (price > 0, quantity > 0)
- [ ] **Default values** for created_at, updated_at timestamps
- [ ] **Primary keys** are immutable (UUID or BIGSERIAL)

### Performance Testing

```sql
-- Explain query performance
EXPLAIN ANALYZE SELECT * FROM orders WHERE user_id = ?;

-- Check for sequential scans (bad for large tables)
-- Look for "Seq Scan" → Add index
-- Look for "Index Scan" → Good

-- Monitor unused indexes
SELECT * FROM pg_stat_user_indexes WHERE idx_scan = 0;
```

---

## Decision Checklist

When designing a new schema:

1. **Identify entities and relationships**
   - [ ] What are the core entities? (User, Product, Order, etc.)
   - [ ] What are the relationships? (One-to-many, many-to-many)
   - [ ] What are the access patterns? (How will I query this?)

2. **Choose normalization level**
   - [ ] Start with 3NF (default)
   - [ ] Denormalize only with performance evidence

3. **Define constraints**
   - [ ] Primary keys (UUID or BIGSERIAL)
   - [ ] Foreign keys with ON DELETE behavior
   - [ ] Unique constraints (business keys)
   - [ ] NOT NULL (required fields)
   - [ ] CHECK constraints (validation)

4. **Plan indexing strategy**
   - [ ] Index all foreign keys
   - [ ] Index WHERE clause columns
   - [ ] Index ORDER BY columns
   - [ ] Consider composite indexes for common query patterns

5. **Design for evolution**
   - [ ] Use nullable columns for future expansion
   - [ ] Version your schema (migration scripts)
   - [ ] Plan backward-compatible changes

---

## Summary

### Key Principles

1. **Start normalized (3NF), denormalize with evidence**
2. **Design for access patterns, not just entities**
3. **Index foreign keys and WHERE/ORDER BY columns**
4. **Use foreign key constraints for data integrity**
5. **Plan for schema evolution (backward compatibility)**
6. **Test query performance, optimize bottlenecks**

### Common Patterns

- **OLTP (transactional)**: Normalized (3NF)
- **OLAP (analytics)**: Denormalized or materialized views
- **Hybrid**: Normalized core + denormalized views/caches

### When to Denormalize

- Read:write ratio > 10:1
- Query performance requirements < 100ms
- Data changes infrequently
- Can tolerate eventual consistency

**Remember**: Data models are expensive to change. Invest time upfront to design them right.
