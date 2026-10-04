---
name: modern-database-orchestration
description: Type-safe ORM patterns (Prisma, Drizzle), migration safety protocols, schema evolution workflows, and seeding strategies. Use when designing schemas, writing migrations, or integrating ORMs into a project.
version: "1.0.0"
verified_date: 2026-04-30
category: backend
---

# Modern Database Orchestration

## Purpose
Provide specialized, ORM-aware database engineering patterns that go beyond the raw SQL standards in `rules/database.md`. This skill bridges the gap between schema design theory and the practical reality of type-safe ORMs, migration pipelines, and production data evolution.

## When to Use This Skill
Use when:
- Designing or modifying a database schema using Prisma, Drizzle, or TypeORM
- Writing or reviewing migration files
- Setting up database seeding for development or testing
- Debugging ORM query generation or performance issues
- Planning a schema evolution that requires zero-downtime deployment

Do NOT use when:
- Writing raw SQL queries without an ORM (use `rules/database.md` directly)
- The task is purely frontend with no data layer involvement

## Phase 1: ORM Selection & Setup

### Prisma (Recommended Default)
Best for: Greenfield projects, teams wanting strong type safety with minimal SQL knowledge.
```
npx prisma init               # scaffolds schema.prisma + .env
npx prisma db push             # rapid prototyping (no migration file)
npx prisma migrate dev         # production-path migration
npx prisma generate            # regenerate client after schema changes
```

### Drizzle (Alternative)
Best for: Teams wanting SQL-like syntax with full type inference and no code generation step.
```
npx drizzle-kit generate       # generate migration SQL from schema
npx drizzle-kit migrate        # apply migrations
npx drizzle-kit push           # push schema directly (prototyping)
```

### Selection Criteria
| Factor | Prisma | Drizzle |
|--------|--------|---------|
| Type safety | ✅ Generated types | ✅ Inferred types |
| Raw SQL access | Limited (via `$queryRaw`) | Native SQL-like API |
| Migration tooling | Built-in, opinionated | Flexible, SQL-native |
| Learning curve | Low | Medium |
| Bundle size | Larger (engine binary) | Minimal |
| Edge runtime | Requires adapter | Native support |

## Phase 2: Schema Design Workflow

### Schema-First Development
1. **Define the domain model** in the ORM schema file before writing any application code
2. **Run type generation** to get compile-time safety across the entire data layer
3. **Write the data access layer** against the generated types
4. **Never access the database directly from routes or controllers** — always go through a repository/service layer

### Prisma Schema Patterns
```prisma
model User {
  id        String   @id @default(cuid())
  email     String   @unique
  name      String?
  role      Role     @default(USER)
  posts     Post[]
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  @@index([email])
  @@map("users")
}

enum Role {
  USER
  ADMIN
}
```

### Drizzle Schema Patterns
```typescript
export const users = pgTable('users', {
  id: text('id').primaryKey().$defaultFn(() => createId()),
  email: text('email').notNull().unique(),
  name: text('name'),
  role: text('role', { enum: ['USER', 'ADMIN'] }).default('USER').notNull(),
  createdAt: timestamp('created_at', { withTimezone: true }).defaultNow().notNull(),
  updatedAt: timestamp('updated_at', { withTimezone: true }).defaultNow().notNull(),
});
```

## Phase 3: Migration Safety Protocol

### Development Migrations
1. Always use `migrate dev` (Prisma) or `drizzle-kit generate` + `drizzle-kit migrate` (Drizzle)
2. Review the generated SQL before applying — never blindly accept
3. Name migrations descriptively: `add_user_role_column`, not `migration_001`

### Production Migration Rules
1. **Never run `migrate reset` or `db push` against production** — these are Tier 4 blocked commands
2. **Additive-only migrations**: Add columns as nullable or with defaults. Never add a `NOT NULL` column without a default in a single step
3. **Two-phase column removal**:
   - Phase 1: Deploy code that stops reading/writing the column
   - Phase 2: Drop the column in a subsequent migration
4. **Two-phase rename**:
   - Phase 1: Add new column, backfill data, deploy code using new column
   - Phase 2: Drop old column
5. **Index creation**: Always use `CREATE INDEX CONCURRENTLY` on large production tables (Postgres)
6. **Test migrations**: Run against a clone of production data before deploying

### Migration Rollback Strategy
- Every migration should have a documented rollback path
- For Prisma: maintain manual `down.sql` files for critical migrations
- For Drizzle: generate reverse SQL alongside forward migrations
- **Never rely on ORM auto-rollback in production**

## Phase 4: Seeding & Test Data

### Seed Architecture
```typescript
// prisma/seed.ts or drizzle/seed.ts
async function seed() {
  // 1. Clear existing data (dev only, NEVER in production)
  await db.delete(posts);
  await db.delete(users);

  // 2. Create base entities
  const admin = await db.insert(users).values({
    email: 'admin@example.com',
    role: 'ADMIN',
  }).returning();

  // 3. Create dependent entities
  await db.insert(posts).values([
    { title: 'First Post', authorId: admin[0].id },
  ]);
}
```

### Seeding Rules
1. Seeds must be **idempotent** — running twice should not create duplicates
2. Use **fixed IDs** for reference data (roles, categories) to enable stable foreign keys in tests
3. Never seed with real user data or PII
4. Separate **reference data seeds** (always needed) from **sample data seeds** (dev only)

## Phase 5: Query Optimization

### ORM-Specific Pitfalls
1. **N+1 queries**: Always use `include` (Prisma) or `with` (Drizzle) for related data
2. **Select only what you need**: Use `select` to limit returned fields on large tables
3. **Pagination**: Always use cursor-based pagination for large datasets, not offset-based
4. **Transaction boundaries**: Wrap multi-table mutations in explicit transactions
5. **Connection pooling**: Use PgBouncer or built-in pooling for serverless environments

### Debugging Queries
- Prisma: Enable query logging with `log: ['query']` in the client constructor
- Drizzle: Use `.toSQL()` to inspect generated queries before execution
- Always check `EXPLAIN ANALYZE` for slow queries

## Output Format / Delivery
- Schema definitions and migration files
- Data access layer implementations
- Seed scripts
- Query optimization recommendations with before/after `EXPLAIN` output

## Behavior Rules
1. **Schema is the source of truth.** Application code conforms to the schema, not the other way around.
2. **Generated types are sacred.** Never use `any` or type assertions to bypass ORM-generated types.
3. **Migrations are immutable.** Once a migration is committed, it is never modified — create a new migration instead.
4. **Connection strings are secrets.** Never log, commit, or hardcode database URLs.

## Safety Guardrails
1. **ORM Hallucination Patch (inherited from backend-dev-guidelines)**: Cross-reference every ORM method against the actual ORM documentation. Do not invent API methods.
2. **Destructive Migration Patch**: Any migration containing `DROP`, `DELETE`, `TRUNCATE`, or `ALTER COLUMN ... TYPE` must be flagged with an explicit warning before generation.
3. **Raw Query Injection Patch**: When using `$queryRaw` or `sql.raw()`, always use parameterized queries. Never interpolate user input into SQL strings.
4. **Self-Rejection Clause**: If the active project's ORM version or schema cannot be verified, **ABORT OUTPUT** and emit: *"REJECTED: Cannot verify ORM schema — load the schema file before generating queries."*

## Maintenance Notes
- Created 2026-04-30 as part of the Engineering Rigor gap analysis.
- Complements `rules/database.md` (raw SQL standards) with ORM-specific operational patterns.
- Complements `backend-dev-guidelines` (general backend) with specialized data-layer depth.
