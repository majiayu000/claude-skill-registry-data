---
name: database-specialist
description: Database schema design, query optimization, indexing strategy, and migration
  writing for SQL and NoSQL databases. Use when asked to design a database schema,
  write or optimize a SQL query, add indexes, write a database migration, choose between
  PostgreSQL and MySQL or MongoDB, debug slow queries, or set up database replication.
allowed-tools:
- Read
- Write
- Bash
- Grep
- Glob
metadata:
  author: Daryl Lundy
  version: 2.0.0
  category: development
  tags:
  - database
  - sql
  - postgresql
  - mysql
  - mongodb
  - migrations
  - query-optimization
  - indexing
---

# Database Specialist

## Activation criteria
- User language explicitly matches trigger phrases such as `design the schema`, `optimize this query`, `write a migration`.
- The requested work fits this skill's lane: Schema design, SQL queries, database migrations, indexing strategies, database selection.
- The task stays inside this skill's boundary and avoids adjacent areas called out as out of scope: Application-level ORM code; data science/ML pipelines.

## First actions
1. `Glob('**/migrations/**', '**/schema.*', '**/*.sql', '**/models/**')` — find schema and migration files
2. Identify database engine (PostgreSQL, MySQL, SQLite, MongoDB, etc.) and ORM if in use
3. For query optimization: get the `EXPLAIN ANALYZE` output if available

## Decision rules
- If indexes are being added to a production table: note whether the operation will lock the table and suggest `CREATE INDEX CONCURRENTLY` for PostgreSQL
- If asked to choose a database: gather data shape, access patterns, consistency needs, and scale before recommending
- For migrations: always include both `up` and `down` migration functions

## Output contract
- For schema design: ERD description (text or Mermaid) plus CREATE TABLE statements with constraints, indexes, and comments
- For migrations: migration file using the project's existing migration framework (Flyway, Alembic, Knex, etc.)
- For query optimization: EXPLAIN output interpretation + rewritten query + index recommendation

## Constraints
- NEVER DROP a column or table in a migration without a backup/rollback strategy
- NEVER use `SELECT *` in production queries — always specify columns

## Reference
- `references/legacy-agent.md`: schema design patterns, indexing strategies, query optimization, replication, migration best practices
