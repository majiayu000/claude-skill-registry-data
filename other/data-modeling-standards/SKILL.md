---
name: data-modeling-standards
description: >
  Use when designing, creating, or modifying database schemas, data structures, or
  data models. This skill provides standardized data modeling practices ensuring
  consistency, integrity, and maintainability across all data stores.
---

# Data Modeling Standards

## Overview
This skill defines data modeling standards for consistent, performant, and maintainable database schemas. Good data models prevent data integrity issues, enable efficient queries, and make future changes manageable.

## When to Use
- When designing new database tables or collections
- When modifying existing schemas (adding/removing columns)
- When reviewing data architecture decisions
- When choosing between SQL and NoSQL for new data
- When designing data migrations
- **Don't use when:** Working with temporary or throwaway data with no persistence needs

## Core Procedures

### Step 1: Design Principles
Apply these to all data models:
- **Normalized:** Eliminate redundancy (3NF minimum unless justified)
- **Named Clearly:** Tables as nouns (plural), columns as attributes (singular)
- **Typed Strictly:** Use specific types (not generic text/blob where possible)
- **Constrained:** Define NOT NULL, UNIQUE, FOREIGN KEY where applicable
- **Indexed Strategically:** Index columns used in WHERE, JOIN, ORDER BY

### Step 2: Naming Conventions
| Element | Convention | Example |
|---------|------------|---------|
| Tables | lowercase_plural_nouns | `users`, `orders`, `order_items` |
| Columns | lowercase_snake_case | `first_name`, `created_at` |
| Primary Keys | `id` (or `{table}_id`) | `id`, `user_id` |
| Foreign Keys | `{referenced_table}_id` | `company_id`, `agent_id` |
| Indexes | `idx_{table}_{columns}` | `idx_users_email` |
| Constraints | `fk/pk/ck/uk_{table}_{columns}` | `fk_orders_user_id` |

### Step 3: Column Standards
Every table should have:
```sql
id          UUID PRIMARY KEY          -- or SERIAL/bigint
created_at  TIMESTAMP NOT NULL DEFAULT NOW()
updated_at  TIMESTAMP NOT NULL DEFAULT NOW()
```

Additional standards:
- Use `BOOLEAN` for true/false (not integers)
- Use `TEXT` for unlimited strings, `VARCHAR(n)` for fixed max
- Use `DECIMAL` for financial amounts (not FLOAT)
- Use `JSONB` for flexible/semi-structured data (PostgreSQL)
- Use `ENUM` or lookup tables for fixed value sets
- Always store timestamps in UTC

### Step 4: Relationship Design
- **One-to-Many:** Foreign key on the "many" side
- **Many-to-Many:** Junction table with two foreign keys, composite primary key
- **Self-Referencing:** Foreign key to same table (e.g., manager_id → users.id)
- Always define ON DELETE behavior (CASCADE, SET NULL, RESTRICT)

### Step 5: Migration Practices
- Always write forward migrations (no backward-only)
- Each migration is atomic and reversible (with down migration)
- Test migrations on copy of production data
- Never drop columns in same migration as adding replacement
- Data migrations separate from schema migrations
- Lock strategy for concurrent deployments

## Quality Checklist
- [ ] Tables follow naming conventions
- [ ] All tables have id, created_at, updated_at
- [ ] Foreign keys defined with ON DELETE behavior
- [ ] Indexes exist on frequently queried columns
- [ ] Data types are specific and appropriate
- [ ] Constraints prevent invalid data states
- [ ] Migration is reversible and tested
- [ ] No data loss in schema changes

## Error Handling
- **Error:** Migration fails on production
  **Response:** Rollback immediately using down migration, diagnose in staging
- **Error:** Schema change causes data loss
  **Response:** Write data migration first, preserve data in new structure, verify before dropping old

## Cross-Team Integration
**Related Skills:** database-schema-management, api-design-standards, secrets-handling, regression-prevention
**Used By:** Database agents, backend engineers, data engineers, infrastructure teams