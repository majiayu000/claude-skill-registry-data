---
name: postgresql
description: Design a PostgreSQL-specific schema. Covers best-practices, data types, indexing, constraints, performance patterns, and advanced features
stacks:
  - postgresql
  - sql
packages:
  - pg
  - postgres
tags:
  - postgresql
  - postgres
  - sql
---

## Use this skill when

- Designing a schema for PostgreSQL
- Selecting data types and constraints
- Planning indexes, partitions, or RLS policies
- Reviewing tables for scale and maintainability

## Do not use this skill when

- You are targeting a non-PostgreSQL database
- You only need query tuning without schema changes
- You require a DB-agnostic modeling guide

## Instructions

1. Capture entities, access patterns, and scale targets (rows, QPS, retention)
2. Choose data types and constraints that enforce invariants
3. Add indexes for real query paths and validate with EXPLAIN
4. Plan partitioning or RLS where required by scale or access control
5. Review migration impact and apply changes safely

## Safety

- Avoid destructive DDL on production without backups and a rollback plan
- Use migrations and staging validation before applying schema changes

## Capabilities

### Schema Design
- Primary key selection: `BIGINT GENERATED ALWAYS AS IDENTITY` preferred; UUID only when global uniqueness or opacity is needed
- Normalization to 3NF first; denormalize only for measured, high-ROI reads with proven join performance problems
- NOT NULL on all semantically required columns; DEFAULT values for common cases
- Generated columns (`GENERATED ALWAYS AS (...) STORED`) for computed, indexable fields; PG18+ adds VIRTUAL

### Data Type Selection
- IDs: `BIGINT GENERATED ALWAYS AS IDENTITY`; UUID when merging distributed systems or needing opaque IDs; generate with `uuidv7()` (PG18+) or `gen_random_uuid()`
- Integers: prefer BIGINT; INTEGER for smaller ranges; avoid SMALLINT unless storage is critical
- Floats: prefer DOUBLE PRECISION; use NUMERIC for exact decimal arithmetic (money, prices)
- Strings: prefer TEXT; use CHECK for length limits instead of VARCHAR(n); BYTEA for binary; CITEXT or expression indexes on LOWER() for case-insensitive
- Timestamps: TIMESTAMPTZ always; DATE for date-only; INTERVAL for durations; `now()` for transaction time, `clock_timestamp()` for wall-clock time
- Booleans: BOOLEAN with NOT NULL unless tri-state is required
- Enums: CREATE TYPE AS ENUM for small stable sets (US states, weekdays); TEXT + CHECK or lookup table for evolving business values
- Arrays: TEXT[], INTEGER[] for ordered lists queried by element; GIN index for containment; use junction tables instead for relations
- Range types: daterange, numrange, tstzrange; GiST index; prefer [) bounds convention
- JSONB: preferred over JSON; GIN index; use for optional/semi-structured attributes only; JSON only when key ordering must be preserved
- Network types: INET for IPs, CIDR for networks, MACADDR for MAC addresses
- Text search: TSVECTOR + TSQUERY; always specify language in to_tsvector/to_tsquery; GIN index
- Vector types: pgvector extension for embedding similarity search

### Forbidden Data Types
- `timestamp` without timezone — use TIMESTAMPTZ
- `char(n)` or `varchar(n)` — use TEXT
- `money` type — use NUMERIC
- `timetz` type — use TIMESTAMPTZ
- `timestamptz(0)` with precision — use TIMESTAMPTZ
- `serial` type — use GENERATED ALWAYS AS IDENTITY

### Table Types
- Regular: default, fully durable and logged
- TEMPORARY: session-scoped, auto-dropped, not logged; faster for scratch work
- UNLOGGED: persistent but not crash-safe; faster writes; good for caches and staging data

### Constraints
- PK: implicit UNIQUE + NOT NULL; creates B-tree index
- FK: specify ON DELETE/UPDATE action (CASCADE, RESTRICT, SET NULL, SET DEFAULT); add explicit index on referencing column; use DEFERRABLE INITIALLY DEFERRED for circular FK dependencies
- UNIQUE: allows multiple NULLs by default; use NULLS NOT DISTINCT (PG15+) to restrict to one NULL
- CHECK: NULL values pass three-valued logic; combine with NOT NULL to enforce
- EXCLUDE: prevents overlapping values; requires GiST index; useful for double-booking prevention

### Row-Level Security
- Enable with `ALTER TABLE tbl ENABLE ROW LEVEL SECURITY`
- Create policies with FOR SELECT/INSERT/UPDATE/DELETE and USING/WITH CHECK clauses
- Built-in user-based row-level access control

### Indexing Strategy
- B-tree: default for equality/range queries and ORDER BY
- Composite: leftmost prefix rule; most selective/frequently filtered columns first
- Covering: INCLUDE clause for index-only scans
- Partial: for hot subsets (WHERE status = 'active'); query must include same WHERE clause
- Expression: for computed search keys; expression must match exactly in WHERE clause
- GIN: JSONB containment, arrays, full-text search
- GiST: ranges, geometry, exclusion constraints
- BRIN: very large, naturally ordered time-series data

### Partitioning
- RANGE: time-series data; queries filter on partition key consistently
- LIST: discrete values (regions, categories)
- HASH: even distribution without natural key
- Prefer declarative partitioning or TimescaleDB hypertables; never use table inheritance
- No global UNIQUE constraints on partitioned tables; include partition key in PK/UNIQUE

### JSONB Indexing
- Default GIN: accelerates containment (@>), key existence (?), any/all keys
- jsonb_path_ops opclass: smaller/faster for containment-only workloads; loses key existence support
- Extract scalar fields to generated columns + B-tree index for equality/range queries

### Update-Heavy Tables
- Separate hot/cold columns to minimize bloat
- fillfactor=90 to leave space for HOT updates
- Avoid updating indexed columns (prevents beneficial HOT updates)

### Insert-Heavy Workloads
- Minimize indexes (every index slows inserts)
- Use COPY or multi-row INSERT instead of single-row inserts
- UNLOGGED tables for rebuildable staging data
- Defer index creation for bulk loads

### Upsert Design
- Requires UNIQUE index on conflict target columns
- Use EXCLUDED.column to reference would-be-inserted values
- DO NOTHING faster than DO UPDATE when no actual update is needed

### Safe Schema Evolution
- Transactional DDL: most DDL can be wrapped in BEGIN/ROLLBACK for safe testing
- CREATE INDEX CONCURRENTLY: avoids blocking writes but cannot run in transactions
- Volatile defaults (now(), gen_random_uuid()) cause full table rewrites when added with NOT NULL
- Drop constraints before columns to avoid dependency issues

## Behavioral Traits
- Validates scale and access patterns before designing schema
- Always adds explicit indexes on FK columns (PostgreSQL does NOT auto-index them)
- Never uses deprecated data types (serial, varchar, timestamp, money, timetz)
- Normalizes to 3NF first; denormalizes only with measured proof of need
- Checks migration impact and provides rollback plan for destructive DDL
- Treats JSONB as an escape hatch for semi-structured data, not a replacement for proper columns

## Knowledge Base

### PostgreSQL Gotchas
- Unquoted identifiers are lowercased; avoid quoted or mixed-case names; use snake_case
- UNIQUE allows multiple NULLs; use NULLS NOT DISTINCT (PG15+) to restrict
- FK columns are NOT auto-indexed — add them manually
- No silent coercions: inserting 999 into NUMERIC(2,0) fails with error, not truncation
- Identity sequences have gaps (rollbacks, crashes, concurrent transactions) — this is normal, do not try to fix it
- No clustered PK by default (unlike SQL Server/MySQL InnoDB); CLUSTER is a one-off reorganization
- MVCC: updates/deletes leave dead tuples; vacuum handles them; design to avoid hot wide-row churn

### Useful Extensions
- pgcrypto: crypt() for password hashing
- pg_trgm: fuzzy text search, GIN index for LIKE '%pattern%'
- citext: case-insensitive text type
- btree_gin / btree_gist: mixed-type indexes
- timescaledb: automated partitioning, retention, compression for time-series
- postgis: comprehensive geospatial support
- pgvector: vector similarity search for embeddings
- pgaudit: audit logging for all database activity

## Constraints
- Never design schemas with mutable primary keys
- Never use serial, varchar(n), char(n), timestamp (without timezone), money, or timetz
- Never use JSONB as a replacement for proper relational columns
- Always add explicit indexes on FK columns
- Always specify language in full-text search functions
- Always include ON DELETE/UPDATE actions on FK definitions
- Never use table inheritance for partitioning; use declarative partitioning

## API Reference

Detailed API documentation: [references/REFERENCE.md](references/REFERENCE.md).

**When to read**: when you need exact method signatures, configuration options, type definitions, or implementation details not covered above.

**How to use**: search or read the reference for specific APIs before writing code. Don't read the entire file — look up only what you need.
