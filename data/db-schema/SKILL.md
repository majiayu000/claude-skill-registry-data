---
name: db-schema
description: >
  Design a database schema for a given domain or feature. Auto-invoke when
  the user says "design the schema for", "what tables do we need for",
  "model the database for", or "ER design for X".
allowed-tools: Read, Write, Glob
argument-hint: <domain-or-feature-description>
---
 
# DB Schema Skill
 
Design a normalised, production-ready database schema for: `$ARGUMENTS`
 
## Step 1 — Read the DB Process File
Always read `@~/.claude/process/db_process.md` before generating anything.
 
## Step 2 — Identify Entities and Relationships
List:
- All entities (nouns in the domain)
- Relationships between them with cardinality (1:1, 1:N, M:N)
- Key attributes per entity
 
Present this entity list before writing any DDL. Wait for approval.
 
## Step 3 — Define the Schema
 
For each table:
 
```sql
-- Table: <table_name>
-- Purpose: <what this represents>
CREATE TABLE <table_name> (
  id          BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  -- or: id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
 
  -- FK columns next
  <fk_col>    BIGINT UNSIGNED NOT NULL,
 
  -- domain columns
  ...
 
  -- audit columns always last
  created_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  deleted_at  TIMESTAMP NULL DEFAULT NULL  -- include only if soft-delete applies
 
  CONSTRAINT fk_<table>_<ref> FOREIGN KEY (<fk_col>) REFERENCES <ref_table>(id) ON DELETE RESTRICT
);
```
 
### Rules (from db_process.md)
- Normalise to 3NF — denormalise only with a documented reason written as a SQL comment
- Use `DECIMAL(19, 4)` for monetary values — never `FLOAT` or `DOUBLE`
- Use `TIMESTAMP` for datetimes, always stored in UTC
- Boolean columns prefixed with `is_` or `has_`
- Join tables for M:N: `<table_a>_<table_b>` (alphabetical order, e.g. `order_products`)
- Never store comma-separated values in a column
 
## Step 4 — Define Indexes
 
After tables, list all indexes with justification:
 
```sql
-- Indexes for <table_name>
CREATE INDEX idx_<table>_<col> ON <table>(<col>);        -- FK index (always)
CREATE INDEX idx_<table>_<col> ON <table>(<col>);        -- query: WHERE status = ?
CREATE UNIQUE INDEX uq_<table>_<col> ON <table>(<col>);  -- uniqueness constraint
```
 
For each index, write a comment explaining which query pattern it supports.
 
## Step 5 — Flag Design Decisions
 
Call out explicitly:
- Any denormalisation decisions and why
- Soft-delete strategy (if used): which tables, how it's enforced at app layer
- UUID vs auto-increment choice and rationale
- Any columns that look like they might grow into a separate table later
- Multi-tenancy: if applicable, identify which tables need `tenant_id` and how it's indexed
 
## Step 6 — Write Migration File
 
Generate a migration file in the project's migration format:
- Laravel → `database/migrations/<timestamp>_create_<table>_table.php`
- Node.js → check for Knex, Prisma, or TypeORM and match the format
- Go → check for golang-migrate and produce `.sql` migration files
 
## Output
- Write schema to `docs/db/<domain>-schema.md` with the ER description + DDL
- Write the migration file(s) to the appropriate location
- Print a summary: tables created, relationships, indexes added, decisions flagged
 
