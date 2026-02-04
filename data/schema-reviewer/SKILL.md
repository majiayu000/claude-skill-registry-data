---
name: schema-reviewer
description: |
  WHEN: Database schema review, table design, normalization, constraints, index planning
  WHAT: Normalization analysis + Constraint validation + Index strategy + Data types + Relationship design
  WHEN NOT: Query optimization → sql-optimizer, ORM code → orm-reviewer
---

# Schema Reviewer Skill

## Purpose
Reviews database schema design for normalization, constraints, indexes, and best practices.

## When to Use
- Database schema review
- Table design review
- Normalization check
- Index planning
- Constraint validation

## Project Detection
- Schema files (`.sql`, `schema.prisma`)
- Migration files
- Entity definitions
- Database documentation

## Workflow

### Step 1: Analyze Schema
```
**Database**: PostgreSQL/MySQL
**Tables**: 15
**Relationships**: 1:N, N:M
**Normalization**: 3NF
```

### Step 2: Select Review Areas
**AskUserQuestion:**
```
"Which areas to review?"
Options:
- Full schema review (recommended)
- Normalization and design
- Constraints and integrity
- Index strategy
- Data type optimization
multiSelect: true
```

## Detection Rules

### Normalization
| Check | Recommendation | Severity |
|-------|----------------|----------|
| Repeating groups | Move to separate table | HIGH |
| Partial dependency | Apply 2NF | MEDIUM |
| Transitive dependency | Apply 3NF | MEDIUM |
| Over-normalization | Consider denormalization for reads | LOW |

```sql
-- BAD: 1NF violation (repeating groups)
CREATE TABLE orders (
    id INT PRIMARY KEY,
    product1_id INT,
    product1_qty INT,
    product2_id INT,
    product2_qty INT,
    product3_id INT,
    product3_qty INT
);

-- GOOD: Normalized with separate table
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(id),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INT NOT NULL REFERENCES orders(id),
    product_id INT NOT NULL REFERENCES products(id),
    quantity INT NOT NULL CHECK (quantity > 0),
    price DECIMAL(10,2) NOT NULL
);

-- BAD: 2NF violation (partial dependency)
CREATE TABLE order_items (
    order_id INT,
    product_id INT,
    product_name VARCHAR(100),  -- Depends only on product_id!
    quantity INT,
    PRIMARY KEY (order_id, product_id)
);

-- GOOD: Product name in products table only
CREATE TABLE order_items (
    order_id INT REFERENCES orders(id),
    product_id INT REFERENCES products(id),
    quantity INT NOT NULL,
    PRIMARY KEY (order_id, product_id)
);
```

### Constraints
| Check | Recommendation | Severity |
|-------|----------------|----------|
| Missing PRIMARY KEY | Add primary key | CRITICAL |
| Missing FOREIGN KEY | Add for relationships | HIGH |
| No NOT NULL | Add where appropriate | MEDIUM |
| No CHECK constraints | Validate data at DB level | MEDIUM |
| Missing UNIQUE | Add for natural keys | HIGH |

```sql
-- BAD: No constraints
CREATE TABLE users (
    id INT,
    email VARCHAR(255),
    status VARCHAR(20)
);

-- GOOD: Proper constraints
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    status VARCHAR(20) NOT NULL DEFAULT 'active'
        CHECK (status IN ('active', 'inactive', 'banned')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- With proper foreign keys
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(id)
        ON DELETE RESTRICT  -- Prevent user deletion with orders
        ON UPDATE CASCADE,
    status VARCHAR(20) NOT NULL DEFAULT 'pending'
        CHECK (status IN ('pending', 'processing', 'shipped', 'delivered', 'cancelled')),
    total DECIMAL(12,2) NOT NULL CHECK (total >= 0)
);
```

### Data Types
| Check | Recommendation | Severity |
|-------|----------------|----------|
| VARCHAR for all strings | Use appropriate types | MEDIUM |
| INT for monetary values | Use DECIMAL | HIGH |
| FLOAT for money | Use DECIMAL | CRITICAL |
| TEXT without limit | Consider VARCHAR with limit | LOW |
| Missing timezone | Use TIMESTAMPTZ | HIGH |

```sql
-- BAD: Poor data type choices
CREATE TABLE products (
    id INT,
    price FLOAT,              -- Precision issues!
    quantity VARCHAR(10),     -- Should be INT
    created_at TIMESTAMP,     -- No timezone!
    description TEXT          -- Unlimited
);

-- GOOD: Appropriate data types
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    sku VARCHAR(50) NOT NULL UNIQUE,
    name VARCHAR(200) NOT NULL,
    price DECIMAL(10,2) NOT NULL CHECK (price >= 0),
    quantity INT NOT NULL DEFAULT 0 CHECK (quantity >= 0),
    description TEXT,  -- OK for long text
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Use ENUMs for fixed values (PostgreSQL)
CREATE TYPE order_status AS ENUM (
    'pending', 'processing', 'shipped', 'delivered', 'cancelled'
);

CREATE TABLE orders (
    status order_status NOT NULL DEFAULT 'pending'
);
```

### Index Strategy
| Check | Recommendation | Severity |
|-------|----------------|----------|
| No index on FK | Add index | HIGH |
| No index on filter columns | Add index | HIGH |
| Too many single-column indexes | Use composite | MEDIUM |
| Missing unique index | Add for unique constraints | HIGH |

```sql
-- Index planning
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(id),
    status VARCHAR(20) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Foreign key index (not automatic in PostgreSQL!)
CREATE INDEX idx_orders_user_id ON orders(user_id);

-- Composite index for common queries
-- WHERE status = ? ORDER BY created_at DESC
CREATE INDEX idx_orders_status_created ON orders(status, created_at DESC);

-- Partial index for specific cases
CREATE INDEX idx_orders_pending ON orders(created_at)
WHERE status = 'pending';

-- Cover index (includes all needed columns)
CREATE INDEX idx_orders_user_summary ON orders(user_id, status, total);
```

### Relationship Design
| Check | Recommendation | Severity |
|-------|----------------|----------|
| N:M without junction table | Create junction table | CRITICAL |
| Self-reference without depth | Add level/path column | MEDIUM |
| Circular references | Redesign relationships | HIGH |

```sql
-- N:M relationship with junction table
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL
);

CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE product_categories (
    product_id INT NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    category_id INT NOT NULL REFERENCES categories(id) ON DELETE CASCADE,
    PRIMARY KEY (product_id, category_id)
);

-- Hierarchical data (adjacency list)
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    parent_id INT REFERENCES categories(id),
    level INT NOT NULL DEFAULT 0,
    path LTREE  -- PostgreSQL ltree extension
);

-- Create index for hierarchical queries
CREATE INDEX idx_categories_path ON categories USING GIST (path);
```

### Audit Columns
```sql
-- Standard audit columns
CREATE TABLE entities (
    id SERIAL PRIMARY KEY,
    -- ... business columns ...
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_by INT REFERENCES users(id),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_by INT REFERENCES users(id),
    deleted_at TIMESTAMPTZ,  -- Soft delete
    deleted_by INT REFERENCES users(id)
);

-- Auto-update trigger
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_updated_at
    BEFORE UPDATE ON entities
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at();
```

## Response Template
```
## Database Schema Review Results

**Database**: PostgreSQL 15
**Tables**: 12 | **Relationships**: 8

### Normalization
| Status | Table | Issue |
|--------|-------|-------|
| HIGH | orders | Repeating product columns |

### Constraints
| Status | Table | Issue |
|--------|-------|-------|
| CRITICAL | users | Missing PRIMARY KEY |
| HIGH | orders | Missing FOREIGN KEY to users |

### Data Types
| Status | Table.Column | Issue |
|--------|--------------|-------|
| CRITICAL | products.price | Using FLOAT instead of DECIMAL |

### Indexes
| Status | Table | Issue |
|--------|-------|-------|
| HIGH | orders.user_id | Missing index on foreign key |

### Recommended Changes
```sql
-- Add missing primary key
ALTER TABLE users ADD PRIMARY KEY (id);

-- Fix price data type
ALTER TABLE products
ALTER COLUMN price TYPE DECIMAL(10,2);

-- Add foreign key index
CREATE INDEX idx_orders_user_id ON orders(user_id);
```
```

## Best Practices
1. **Normalization**: 3NF default, denormalize for performance
2. **Constraints**: PK, FK, NOT NULL, CHECK, UNIQUE
3. **Data Types**: DECIMAL for money, TIMESTAMPTZ for time
4. **Indexes**: FK columns, filter columns, composites
5. **Audit**: created_at, updated_at, soft delete

## Integration
- `sql-optimizer`: Query performance
- `migration-checker`: Migration safety
- `orm-reviewer`: ORM mapping
