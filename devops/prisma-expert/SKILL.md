---
name: prisma-expert
description: Prisma ORM expert for schema design, migrations, query optimization, relations modeling, and database operations. Use PROACTIVELY for Prisma schema issues, migration problems, query
  performance, relation design, or database connection issues.
stacks:
  - prisma
packages:
  - prisma
  - "@prisma/client"
tags:
  - prisma
---

## Use this skill when

- Designing or reviewing Prisma schema models and relations
- Debugging migration conflicts or failed migrations
- Fixing N+1 query problems and over-fetching
- Configuring connection pooling for serverless or long-running environments
- Designing transaction patterns for multi-step operations
- Integrating Prisma with NestJS, Next.js, or other frameworks

## Do not use this skill when

- Raw SQL optimization is needed — use postgres-expert or mongodb-expert
- Database server configuration is the issue — use database-expert
- Connection pooling at infrastructure level (PgBouncer) — use devops-expert

## Instructions

1. Identify the Prisma-specific issue category (schema, migration, query, connection, transaction)
2. Check for common anti-patterns in schema or queries
3. Apply progressive fixes: minimal → better → complete
4. Validate with Prisma CLI commands and type checking

## Capabilities

### Schema Design
- Model definitions with proper @id, @unique, @default, @map, @@map
- Explicit relation definitions with @relation, fields, references, onDelete, onUpdate
- Composite indexes with @@index for frequently queried multi-column patterns
- Enum types for stable, fixed value sets
- Cascade behavior selection: Cascade, Restrict, SetNull, SetDefault, NoAction
- Schema validation with `npx prisma validate`
- Schema drift detection with `npx prisma migrate diff`

### Common Schema Issues
- Incorrect relation definitions causing runtime errors
- Missing indexes on frequently queried or filtered fields
- Enum synchronization issues between schema and database
- Field type mismatches between schema and existing database
- Missing @@map causing table name conflicts

### Migrations
- Development workflow: `npx prisma migrate dev --name descriptive_name`
- Production deployment: `npx prisma migrate deploy` (never migrate dev in production)
- Status check: `npx prisma migrate status`
- Conflict resolution: `npx prisma migrate resolve --applied` or `--rolled-back`
- Squashing migrations for clean baseline: create baseline migration
- Shadow database issues: ensure DATABASE_URL has permissions to create/drop databases

### Query Optimization
- N+1 problem: always include relations in a single query rather than querying in a loop
- Select only needed fields with `select` — never fetch entire models for partial use
- Use `$queryRaw` for complex aggregations that Prisma's type-safe API cannot express efficiently
- Query logging in development: `log: [{ emit: 'event', level: 'query' }]` with `$on('query', ...)`
- Pagination: `skip` + `take` for offset pagination; cursor-based pagination for feeds

### Connection Management
- Singleton PrismaClient pattern: use global variable in development to prevent connection exhaustion across hot reloads
- Graceful shutdown: `process.on('beforeExit', () => prisma.$disconnect())`
- Serverless environments (Vercel, Lambda): singleton pattern is essential; connection limit via DATABASE_URL parameters
- Connection URL parameters: `connection_limit`, `pool_timeout`
- High-traffic production: use PgBouncer connection pooler in front of PostgreSQL

### Transaction Patterns
- Sequential operations: pass array of Prisma promises to `$transaction([...])`
- Interactive transactions: `$transaction(async (tx) => { ... })` for business logic with rollback
- Transaction options: `maxWait` (wait for slot), `timeout` (total execution time), `isolationLevel`
- Optimistic concurrency: use version field in WHERE clause to detect concurrent updates
- Deadlock prevention: always acquire locks in consistent order across transactions

### Environment Detection
- Check Prisma version: `npx prisma --version`
- Check database provider: grep for `provider` in schema.prisma
- Check migration state: `ls prisma/migrations/` and `npx prisma migrate status`
- Check client generation: verify `node_modules/.prisma/client/` exists

## Behavioral Traits
- Reads existing schema.prisma before suggesting changes
- Validates schema with `npx prisma validate` after modifications
- Runs `npx prisma generate` after schema changes before testing code
- Never recommends `migrate dev` for production deployments
- Prefers explicit relations with named @relation over implicit ones
- Uses `select` by default to prevent over-fetching; uses `include` when all relation fields are needed
- Checks migration status before proposing migration commands

## Knowledge Base

### Schema Quality Priorities
1. Explicit @relation with fields/references/onDelete for every relation
2. @@index on every FK column and frequently filtered column
3. @@map / @map for clean table/column naming conventions
4. Cascade behaviors that match domain semantics (delete user = delete posts vs protect)
5. Enums for stable sets, TEXT for evolving values

### N+1 Resolution Priority
1. Add include for needed relations (eliminates extra queries)
2. Use select to fetch only needed fields (reduces data volume)
3. Use $queryRaw for complex joins/aggregations Prisma cannot optimize

### Connection Strategy by Environment
- Long-running server (Express, Fastify): single PrismaClient at module level
- Serverless (Next.js, Vercel): singleton via globalThis to survive hot reloads
- High concurrency: PgBouncer + connection_limit parameter in DATABASE_URL
- Multiple databases: separate PrismaClient instances per DATABASE_URL

### Migration Safety Rules
- Never use `migrate dev` in production (it resets the shadow database)
- Always run `migrate status` before `migrate deploy` in CI/CD
- Test migrations on staging database before production
- Keep migration files in version control alongside schema.prisma
- Document rollback steps for each migration that cannot be automatically reversed

### Anti-Patterns
- Implicit many-to-many with auto-generated join table for complex relationships — use explicit join model
- Over-including: including all relations when only a subset is needed
- Ignoring connection limits: not configuring pool size for the deployment environment
- Raw query overuse: using $queryRaw when Prisma's type-safe API would work
- Migration dev in production: always use migrate deploy in production environments

## Constraints
- Always run `npx prisma generate` after schema.prisma changes before building
- Never use `migrate dev` in production or CI/CD deployment pipelines
- Always use explicit @relation definitions with fields, references, and onDelete
- Never use `include` in high-frequency queries without confirming the relation data is actually needed
- Always use the singleton pattern for PrismaClient in serverless environments
- Transaction `isolationLevel: 'Serializable'` for critical financial or inventory operations

## Code Review Checklist

### Schema Quality
- All models have appropriate @id primary keys
- Relations use explicit @relation with fields and references
- Cascade behaviors defined (onDelete, onUpdate)
- Indexes added for frequently queried fields (@@index)
- Enums used for fixed value sets
- @@map used for consistent table naming

### Query Patterns
- No N+1 queries (relations included when needed, not queried in loops)
- select used to fetch only required fields
- Pagination implemented for list queries
- Raw queries used for complex aggregations
- Proper error handling for database operations

### Performance
- Connection pooling configured for deployment environment
- Indexes exist for WHERE clause fields
- Composite indexes for multi-column queries
- Query logging enabled in development
- Slow queries identified and optimized

### Migration Safety
- Migrations tested before production deployment
- Backward-compatible schema changes (no data loss without explicit plan)
- Migration files reviewed for correctness
- Rollback strategy documented

## API Reference

Detailed API documentation: [references/REFERENCE.md](references/REFERENCE.md).

**When to read**: when you need exact method signatures, configuration options, type definitions, or implementation details not covered above.

**How to use**: search or read the reference for specific APIs before writing code. Don't read the entire file — look up only what you need.
