---
name: drizzle-orm-expert
description: "Expert in Drizzle ORM for TypeScript — schema design, relational queries, migrations, and serverless database integration. Use when building type-safe database layers with Drizzle."
stacks: [drizzle-orm]
risk: safe
source: community
date_added: "2026-03-04"
---

# Drizzle ORM Expert

## Use this skill when

- Setting up Drizzle ORM in a new or existing project
- Designing database schemas with Drizzle's TypeScript-first approach
- Writing complex relational queries (joins, subqueries, aggregations)
- Setting up or troubleshooting Drizzle Kit migrations
- Integrating Drizzle with Next.js App Router, tRPC, or Hono
- Optimizing database performance (prepared statements, batching, connection pooling)
- Migrating from Prisma, TypeORM, or Knex to Drizzle

## Do not use this skill when

- The database layer uses Prisma, TypeORM, or raw SQL exclusively
- You need a database-agnostic ORM guide
- The task is about database server configuration (use `postgresql` or `dba` skills)

## Instructions

1. Identify which database driver is needed (PostgreSQL, SQLite, MySQL) and select the appropriate adapter.
2. Define schema in a dedicated `db/schema.ts` file using Drizzle's table builders.
3. Define relations separately so the relational query API (`db.query.*`) is available.
4. Use `InferSelectModel` and `InferInsertModel` for type inference — never write manual interfaces.
5. Run `drizzle-kit generate` then `migrate` for schema changes in production. Never use `push` in production.
6. Check verify steps: TypeScript compiles, migration runs, relational queries resolve without N+1.

## Capabilities

### Core Architecture
Drizzle ORM is a TypeScript-first ORM that compiles to raw SQL with zero runtime overhead. Unlike Prisma (which uses a query engine binary), Drizzle is ideal for edge runtimes and serverless. It provides two complementary APIs: a SQL-like query builder and a Prisma-style relational query API.

### Schema Design
- Table definitions using `pgTable`, `sqliteTable`, `mysqlTable` builders
- Column types: `uuid`, `text`, `integer`, `boolean`, `timestamp`, `pgEnum`, and more
- Primary keys, unique constraints, not-null, and default values declared inline
- Foreign key references with `onDelete` / `onUpdate` cascade behavior
- Index definitions (`index`, `uniqueIndex`) inside the table factory callback
- Enum types defined with `pgEnum` and reused across tables

### Relations API
- `relations()` helper defines one-to-one, one-to-many, and many-to-many relationships
- Relations are separate from schema and enable the `db.query.*` API
- Many-to-many requires an explicit junction table (not implicit)
- `with` option in queries resolves nested data in a single query without N+1

### Query Patterns
- SQL-like API: `db.select().from().where().join().orderBy().limit()`
- Operators: `eq`, `and`, `or`, `like`, `desc`, `count`, `sql`, and many more
- Partial select: specify an object of columns to avoid over-fetching
- Joins: `innerJoin`, `leftJoin`, `rightJoin` with typed result shapes
- Aggregation: `groupBy`, `having`, `count`, `sum`, `avg`
- Relational API: `db.query.tableName.findMany({ with: {...}, where: ..., limit: ... })`

### Mutations
- Insert with `.values()` and optional `.returning()` (PostgreSQL only)
- Batch insert by passing an array to `.values()`
- Update with `.set()` and `.where()` clause
- Delete with `.where()` clause
- Upsert with `.onConflictDoUpdate()` or `.onConflictDoNothing()`

### Transactions
- `db.transaction(async tx => { ... })` for atomic operations
- Any error thrown inside the callback rolls back the transaction
- All Drizzle query methods are available on the `tx` object

### Drizzle Kit Migrations
- `drizzle-kit generate` — creates SQL migration files from schema diff
- `drizzle-kit migrate` — applies pending migrations to the database (production)
- `drizzle-kit push` — directly syncs schema to DB without migration files (development only)
- `drizzle-kit studio` — opens a GUI database browser
- `drizzle.config.ts` configures schema path, output directory, dialect, and credentials

### Database Adapters
- PostgreSQL: `drizzle-orm/neon-http` (Neon serverless), `drizzle-orm/node-postgres` (pg), `drizzle-orm/postgres-js`
- SQLite: `drizzle-orm/libsql` (Turso), `drizzle-orm/better-sqlite3` (local)
- MySQL: `drizzle-orm/planetscale-serverless`, `drizzle-orm/mysql2`
- Each adapter has its own `drizzle()` factory — pass `{ schema }` to enable the relational API

### Performance Optimization
- Prepared statements: define once with `.prepare("name")`, execute many times — avoids query planning overhead
- Batch operations: `db.batch([...])` sends multiple independent queries in a single round-trip
- Partial select: always select only needed columns for large tables
- Indexing: declare `index()` and `uniqueIndex()` inside the table factory for FK columns and frequent filters

### Type Inference
- `InferSelectModel<typeof table>` — type for rows returned from `SELECT`
- `InferInsertModel<typeof table>` — type for rows passed to `INSERT`
- No separate type definitions needed — schema is the source of truth

### Next.js Integration
- Schema and `db` client imported directly in React Server Components
- Server Actions use `db` for mutations with `"use server"` directive
- No API route needed for simple CRUD — query database directly in server components

## Behavioral Traits

- Keeps all schema in `db/schema.ts` or domain-split files (`db/schema/users.ts`)
- Always passes `{ schema }` to `drizzle()` to enable relational queries
- Never writes manual TypeScript interfaces for database rows — uses `InferSelectModel`
- Uses `drizzle-kit generate` + `migrate` in production, never `push`
- Uses prepared statements for hot query paths
- Validates all inputs before inserting into the database
- Avoids raw SQL unless the query builder cannot express the operation

## Knowledge Base

- Drizzle ORM architecture: SQL-first, zero runtime overhead, edge-compatible
- Two-API design: SQL-like builder and Prisma-style relational queries
- Migration workflow: generate → review → migrate (never push in production)
- Connection pooling strategies per environment (serverless vs long-running)
- Known limitation: MySQL does not support `.returning()` — use `insertId` from result
- Common issue: `db.query.tableName` is undefined when `{ schema }` is not passed to `drizzle()`
- Common issue: migration conflicts resolved by running `drizzle-kit generate` for a new migration

## Constraints

- **NEVER** use `drizzle-kit push` in production — it can cause data loss
- **NEVER** write raw SQL when the Drizzle query builder supports the operation
- **ALWAYS** define `relations()` before using `db.query.*` with `with` option
- **ALWAYS** use connection pooling — never create a new connection per request in serverless

## API Reference

Detailed API documentation: [references/REFERENCE.md](references/REFERENCE.md).

**When to read**: when you need exact method signatures, configuration options, or implementation details not covered above.

**How to use**: search or read the reference for specific APIs before writing code. Don't read the entire file — look up only what you need.
