---
name: tzurot-db-vector
description: PostgreSQL and pgvector patterns for Tzurot v3. Use when writing Prisma queries, migrations, or vector operations. Covers connection management and Railway-specific considerations.
lastUpdated: '2026-01-21'
---

# Tzurot v3 Database & Vector Memory

**Use this skill when:** Working with database queries, pgvector similarity search, migrations, or connection pool management.

## Quick Reference

```bash
# Check migration status (applied, pending, failed)
pnpm ops db:status                   # Local database
pnpm ops db:status --env dev         # Railway development
pnpm ops db:status --env prod        # Railway production

# Run migrations
pnpm ops db:migrate                  # Local (interactive)
pnpm ops db:migrate --env dev        # Railway dev
pnpm ops db:migrate --env prod --force  # Railway prod (requires --force)

# Inspect database state (tables, indexes, migrations) - local only
pnpm ops db:inspect
pnpm ops db:inspect --table memories
pnpm ops db:inspect --indexes

# Create migration with automatic drift sanitization
pnpm ops db:safe-migrate

# Drift detection and fix (NON-DESTRUCTIVE) - local only
pnpm ops db:check-drift
pnpm ops db:fix-drift <migration_name>
```

## Core Principles

1. **Connection pooling** - Use Prisma singleton, Railway limit is 100 connections
2. **Typed queries** - Use Prisma, avoid raw SQL where possible
3. **Migration-first** - Schema changes via Prisma migrations
4. **Vector indexing** - Use ivfflat for fast similarity search
5. **Review migrations** - Prisma tries to DROP pgvector indexes

## Connection Management

```typescript
// ✅ GOOD - Reuse singleton from common-types
import { getPrismaClient } from '@tzurot/common-types';

class PersonalityService {
  constructor(private prisma = getPrismaClient()) {}
}

// ❌ BAD - Creates new connection every time
async getPersonality() {
  const prisma = new PrismaClient(); // Don't do this!
}
```

**Pool configuration:** `connectionLimit = 20` per service (3 services = 60, leaving headroom)

## 🚨 Protected Indexes (CRITICAL)

### Known Drift Patterns

Prisma can't represent these indexes and tries to "fix" them:

| Index                         | Type           | Why It's Protected                                |
| ----------------------------- | -------------- | ------------------------------------------------- |
| `idx_memories_embedding`      | IVFFlat vector | Prisma doesn't support `Unsupported` type indexes |
| `memories_chunk_group_id_idx` | Partial B-tree | Prisma can't represent `WHERE` clauses            |

### The Problem

When creating migrations, Prisma generates dangerous statements:

```sql
DROP INDEX "idx_memories_embedding";  -- 100x slower queries!
CREATE INDEX "memories_chunk_group_id_idx" ON "memories"("chunk_group_id");  -- Fails: already exists
```

### The Solution: Use Safe Migration Script

```bash
# PREFERRED - Automatically sanitizes drift patterns
pnpm ops db:safe-migrate
```

This script:

1. Runs `prisma migrate dev --create-only`
2. Removes known drift patterns from `prisma/drift-ignore.json`
3. Reports what was sanitized
4. Shows the clean migration for review

### Manual Migration Workflow

If you must create migrations manually:

```bash
# 1. Generate only
npx prisma migrate dev --create-only --name your_name

# 2. REVIEW the SQL - delete any lines matching:
#    - DROP INDEX "idx_memories_embedding"
#    - DROP INDEX "memories_chunk_group_id_idx"
#    - CREATE INDEX "memories_chunk_group_id_idx" (without WHERE)
cat prisma/migrations/<timestamp>/migration.sql

# 3. Apply
npx prisma migrate dev
```

### Recovering Protected Indexes

```sql
-- IVFFlat vector index (if dropped)
CREATE INDEX IF NOT EXISTS idx_memories_embedding
ON memories USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 50);

-- Partial index for chunk groups (if dropped/replaced)
DROP INDEX IF EXISTS "memories_chunk_group_id_idx";
CREATE INDEX "memories_chunk_group_id_idx" ON "memories"("chunk_group_id")
WHERE "chunk_group_id" IS NOT NULL;
```

## Vector Operations

### Storing Embeddings

```typescript
const embeddingStr = `[${embedding.join(',')}]`;
await prisma.$executeRaw`
  INSERT INTO memories (id, "personalityId", content, embedding, "createdAt")
  VALUES (gen_random_uuid(), ${id}::uuid, ${content}, ${embeddingStr}::vector, NOW())
`;
```

### Similarity Search

```typescript
// Cosine distance: 0 = identical, 2 = opposite
const results = await prisma.$queryRaw<SimilarMemory[]>`
  SELECT id, content, 1 - (embedding <-> ${embeddingStr}::vector) as similarity
  FROM memories
  WHERE "personalityId" = ${personalityId}::uuid
  ORDER BY embedding <-> ${embeddingStr}::vector
  LIMIT ${limit}
`;
```

## Migration Workflow

### The One True Workflow

```bash
# 1. Create (don't apply)
npx prisma migrate dev --create-only --name descriptive_name

# 2. Review SQL - remove any DROP INDEX for vector indexes
cat prisma/migrations/<timestamp>/migration.sql

# 3. Apply
npx prisma migrate deploy
```

### Idempotent Migrations

```sql
-- ✅ GOOD - Safe to run multiple times
DROP TRIGGER IF EXISTS my_trigger ON my_table;
CREATE TRIGGER my_trigger...

DROP FUNCTION IF EXISTS my_function() CASCADE;
CREATE OR REPLACE FUNCTION my_function()...

CREATE INDEX IF NOT EXISTS idx_name ON table(column);

-- ❌ BAD - Fails if exists
CREATE TRIGGER my_trigger...
CREATE INDEX idx_name ON table(column);
```

### Anti-Patterns

| ❌ Don't                             | ✅ Instead                           |
| ------------------------------------ | ------------------------------------ |
| Run SQL manually then mark applied   | Use `migrate deploy`                 |
| Edit applied migrations              | Create new migration to fix          |
| Use `railway run prisma migrate dev` | Run locally with `.env` DATABASE_URL |

## 🔧 Migration Drift Resolution (IMPORTANT)

### What Is Drift?

Drift occurs when a migration file is modified after being applied to the database. Prisma stores a checksum of each migration in `_prisma_migrations` and compares it when running new migrations.

**Common causes:**

- Formatting changes (Prettier, trailing whitespace)
- Adding comments
- Git merge conflicts resolved differently
- Accidental edits

### Detecting Drift

```bash
# Check all migrations for drift (local only)
pnpm ops db:check-drift

# Output shows:
# ✅ 20251201221930_add_share_ltm_flag: OK
# ❌ 20251213200000_add_tombstones: DRIFT DETECTED
#    DB:   2c6cb23b9477f0cea8df...
#    File: ac8449de6c87c14856f9...
```

### Fixing Drift Non-Destructively

**When safe to fix (update checksum):**

- Formatting/whitespace changes only
- Added comments
- No actual SQL logic changes

```bash
# Fix specific migration(s) - local only
pnpm ops db:fix-drift <migration_name>

# Example:
pnpm ops db:fix-drift 20251213200000_add_tombstones
```

This updates the checksum in `_prisma_migrations` to match the current file.

**When NOT to fix (create new migration):**

- Actual SQL logic was changed
- Table/column definitions differ from what was applied
- Indexes or constraints were modified

### Why NOT Use `prisma migrate reset`?

`prisma migrate reset` **DESTROYS ALL DATA**. Never use it on a shared development or production database. The non-destructive approach preserves all data while fixing the checksum mismatch.

### Why NOT Use `prisma migrate resolve`?

`prisma migrate resolve --applied` marks a migration as applied without running it. This is dangerous because:

- It doesn't verify the schema matches
- It can leave the database in an inconsistent state
- It's meant for disaster recovery, not routine drift

### Preventing Drift

1. **Don't edit applied migrations** - Create new ones instead
2. **Use `--create-only`** - Review before applying
3. **Run drift check in CI** - Catch issues early
4. **Commit migration files immediately** - Before they can drift

## Database Scripts

Available via `pnpm ops db:*`:

```bash
# Check migration status (supports --env local|dev|prod)
pnpm ops db:status
pnpm ops db:status --env dev

# Run migrations (supports --env, --force for prod)
pnpm ops db:migrate
pnpm ops db:migrate --env prod --force

# Inspect database state (local only)
pnpm ops db:inspect
pnpm ops db:inspect --table <name>
pnpm ops db:inspect --indexes

# Create migration with automatic drift sanitization
pnpm ops db:safe-migrate

# Check/fix migration checksum drift (local only)
pnpm ops db:check-drift
pnpm ops db:fix-drift <migration_name>
```

### ⚠️ Prisma db execute Limitation

`npx prisma db execute` runs SQL but **does not show query results**. It only shows "Script executed successfully."

**Use `db:inspect` instead** for visibility, or use raw `$queryRaw` in a script:

```typescript
// To see actual query results, use a script with Prisma client
const result = await prisma.$queryRaw`SELECT * FROM admin_settings`;
console.log(JSON.stringify(result, null, 2));
```

## Query Patterns

```typescript
// ✅ Use include to avoid N+1
const personalities = await prisma.personality.findMany({
  include: { llmConfig: true },
});

// ✅ Cursor-based pagination for large datasets
const messages = await prisma.conversationHistory.findMany({
  take: limit + 1,
  cursor: cursor ? { id: cursor } : undefined,
  skip: cursor ? 1 : 0,
  orderBy: { createdAt: 'desc' },
});
```

## Railway-Specific Notes

### Running Scripts Against Railway Databases

Use `ops run` to execute any script with Railway credentials injected:

```bash
# Generic pattern
pnpm ops run --env dev <command>

# Run a one-off script directly (no npm script needed)
pnpm ops run --env dev tsx scripts/src/db/backfill-local-embeddings.ts

# Run Prisma Studio against Railway
pnpm ops run --env dev npx prisma studio

# Shortcut from root
pnpm with-env dev tsx scripts/src/db/backfill-local-embeddings.ts
```

**How it works**: Fetches `DATABASE_PUBLIC_URL` from Railway via CLI and injects it as `DATABASE_URL`.

**When to use npm scripts vs direct execution:**

- One-off scripts → `tsx scripts/src/db/script.ts` (direct execution)
- Reusable scripts → `pnpm --filter pkg run script` (npm script)

### Migration Deployment

- Migrations run on api-gateway startup (via `prisma migrate deploy`)
- Push migration files to git → Railway auto-deploys
- For manual migrations: `pnpm ops db:migrate --env dev`

## PGLite Schema Regeneration

Integration tests use PGLite (in-memory PostgreSQL via WASM). After Prisma schema changes:

```bash
# Regenerate PGLite schema from current Prisma migrations
./scripts/testing/regenerate-pglite-schema.sh

# Output: packages/test-utils/schema/pglite-schema.sql
```

This generates SQL that PGLite executes to create the same schema as your production database.

**📚 See**: `tzurot-testing` skill for integration test patterns, `docs/reference/testing/PGLITE_SETUP.md` for full setup.

## Related Skills

- **tzurot-types** - Prisma schema and type definitions
- **tzurot-observability** - Query logging
- **tzurot-architecture** - Database service placement
- **tzurot-testing** - PGLite integration test patterns

## References

- Prisma docs: https://www.prisma.io/docs
- pgvector docs: https://github.com/pgvector/pgvector
- Schema: `prisma/schema.prisma`
- Drift docs: `docs/database/PRISMA_DRIFT_ISSUES.md`
