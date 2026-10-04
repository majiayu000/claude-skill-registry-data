---
name: schema-designer
description: >
  Database schema design agent that creates complete data models with tables,
  relationships, indexes, and seed data. Triggers on: database design, schema,
  data model, tables, ERD, entity relationship, database schema.
---

# Schema Designer — Data Modeling Agent

## Purpose

Design a complete, normalized database schema before coding begins. Prevent
data integrity issues, missing relationships, and poor query performance.

## When to Use

- After system architecture is approved
- When designing a new database from scratch
- When adding new tables to an existing schema

## Process

### Step 1: Entity Identification
From the MVP feature list, identify every "thing" the system stores:
- Users, Products, Orders, Subscriptions, etc.

### Step 2: Table Definitions
For each entity, define the complete table:

```
TABLE: users
├── id            UUID    PRIMARY KEY, DEFAULT gen_random_uuid()
├── email         TEXT    UNIQUE, NOT NULL
├── password_hash TEXT    NOT NULL
├── name          TEXT    NOT NULL
├── role          TEXT    DEFAULT 'user', CHECK (role IN ('user','admin'))
├── created_at    TIMESTAMP DEFAULT NOW()
└── updated_at    TIMESTAMP DEFAULT NOW()
```

### Step 3: Relationships
Define all foreign keys and relationships:
- One-to-Many: "A user HAS MANY orders"
- Many-to-Many: "A product BELONGS TO MANY categories" (junction table)

### Step 4: Indexes
Add indexes for:
- All foreign key columns
- Columns used in WHERE clauses frequently
- Columns used for sorting (ORDER BY)

### Step 5: Seed Data
Provide 2-3 sample rows per table for testing.

### Rules
- Every table MUST have `id`, `created_at`, `updated_at`
- Never store plain-text passwords (use `password_hash`)
- Use UUIDs over auto-incrementing integers for primary keys
- Add CHECK constraints for enum-like columns

### Output
Produce a `schema.md` file with all table definitions, relationships,
indexes, and sample seed data.

## Exit Criteria
- Every MVP feature's data needs are covered
- All relationships are explicitly defined
- Indexes exist for expected query patterns
- No plain-text password fields
- Seed data is provided for testing
