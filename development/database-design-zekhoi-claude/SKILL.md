---
name: kit-database-design
description: Design or review relational database schemas, relationships, constraints, indexes, and migrations. Use when the user asks to model new data, change a schema, write or review a migration, or diagnose a schema-level integrity or indexing problem. Do not use for general query debugging without a schema change, or for non-relational stores unless the user asks.
---

# Database design

## 1. Understand the domain and the current schema

- Identify the entities, their relationships and cardinality, the invariants that must always hold, and the main read and write access patterns.
- Read the existing schema, migrations, ORM or query-builder models, and naming conventions. Use the project's migration tool and style.

## 2. Model

- Normalize to avoid duplicated facts; denormalize only for a measured or clearly stated access need.
- Choose types that match the data: exact numerics for money, timezone-aware timestamps where times cross zones, appropriately sized text, and enums or lookup tables per project convention.
- Decide nullability deliberately. A column is `NOT NULL` unless absence has a meaning.
- Enforce invariants in the database where possible: primary keys, foreign keys with intentional `ON DELETE` behavior, unique constraints, and check constraints.

## 3. Index

- Index foreign keys and columns used in frequent filters, joins, and sorts. Order composite index columns by how queries filter.
- Avoid redundant indexes; every index costs writes and storage.
- Back each unique business rule with a unique index or constraint.

## 4. Migrate safely

- Write forward migrations, and reversible ones where the tool supports it.
- For existing data: add nullable columns or defaults first, backfill in batches, then add constraints. Avoid long locks on large tables; use the database's online options where available.
- Never drop or rename columns that deployed code still reads. Use expand and contract across deploys.
- Do not run migrations against shared or production databases without explicit instruction.

## 5. Report

Present the schema or migration, explain each constraint and index, list data-migration and locking risks, and state how it was verified, for example by applying the migration to a local database and running tests.

## Examples

- Use: "Design tables for team invitations." "Review this migration that adds a status column to orders."
- Skip: "Why is this query returning duplicates?" with no schema change (debugging)
