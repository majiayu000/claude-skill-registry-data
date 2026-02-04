---
name: migration-strategies
description: Database migration best practices and strategies. Use when managing schema changes.
---

# Migration Strategies Skill

This skill covers database migration patterns and best practices.

## When to Use

Use this skill when:
- Making schema changes
- Deploying database updates
- Handling data migrations
- Planning rollback strategies

## Core Principle

**FORWARD-ONLY, REVERSIBLE** - Migrations should be forward-only in production but designed to be logically reversible.

## Migration Types

### Schema Migrations
- Add/remove tables
- Add/remove columns
- Modify column types
- Add/remove indexes
- Add/remove constraints

### Data Migrations
- Backfill data
- Transform existing data
- Migrate between schemas

## Safe Migration Patterns

### Adding Columns

```sql
-- Safe: Add nullable column
ALTER TABLE users ADD COLUMN phone TEXT;

-- Safe: Add column with default
ALTER TABLE users ADD COLUMN status TEXT DEFAULT 'active';

-- Unsafe: Add NOT NULL without default
-- ALTER TABLE users ADD COLUMN required_field TEXT NOT NULL; -- DON'T DO THIS
```

### Adding Non-Null Columns

```typescript
// Step 1: Add nullable column
await prisma.$executeRaw`ALTER TABLE users ADD COLUMN bio TEXT`;

// Step 2: Backfill data
await prisma.$executeRaw`UPDATE users SET bio = '' WHERE bio IS NULL`;

// Step 3: Add NOT NULL constraint
await prisma.$executeRaw`ALTER TABLE users ALTER COLUMN bio SET NOT NULL`;
```

### Renaming Columns (Zero Downtime)

```typescript
// Step 1: Add new column
await db.schema.alterTable('users').addColumn('full_name', 'text');

// Step 2: Backfill data
await db.update(users).set({ fullName: sql`${users.name}` });

// Step 3: Update application to use new column
// Deploy code that writes to both columns

// Step 4: Stop writing to old column
// Deploy code that only uses new column

// Step 5: Remove old column (separate migration)
await db.schema.alterTable('users').dropColumn('name');
```

### Adding Indexes (Non-Blocking)

```sql
-- PostgreSQL: Create index concurrently
CREATE INDEX CONCURRENTLY users_email_idx ON users(email);

-- Don't do this in production:
-- CREATE INDEX users_email_idx ON users(email); -- Blocks table
```

### Removing Columns

```typescript
// Step 1: Stop reading the column in code
// Deploy code that doesn't read the column

// Step 2: Stop writing the column in code
// Deploy code that doesn't write the column

// Step 3: Remove the column
await db.schema.alterTable('users').dropColumn('old_column');
```

## Prisma Migration Workflow

### Development

```bash
# Create and apply migration
npx prisma migrate dev --name add_phone_to_users

# Reset database (destructive)
npx prisma migrate reset

# Apply without generating
npx prisma db push
```

### Production

```bash
# Apply pending migrations
npx prisma migrate deploy

# Check migration status
npx prisma migrate status
```

### Migration File

```sql
-- prisma/migrations/20240101_add_phone/migration.sql
-- CreateTable
ALTER TABLE "users" ADD COLUMN "phone" TEXT;

-- CreateIndex
CREATE INDEX "users_phone_idx" ON "users"("phone");
```

## Drizzle Migration Workflow

### Generate Migration

```bash
npx drizzle-kit generate:pg
```

### Apply Migration

```typescript
// src/db/migrate.ts
import { migrate } from 'drizzle-orm/postgres-js/migrator';

await migrate(db, { migrationsFolder: './drizzle' });
```

## Data Migration Pattern

```typescript
// migrations/backfill-user-slugs.ts
import { db } from '../src/db';
import { users } from '../src/db/schema';
import { isNull } from 'drizzle-orm';
import slugify from 'slugify';

const BATCH_SIZE = 1000;

async function backfillSlugs(): Promise<void> {
  let processed = 0;

  while (true) {
    const batch = await db
      .select({ id: users.id, name: users.name })
      .from(users)
      .where(isNull(users.slug))
      .limit(BATCH_SIZE);

    if (batch.length === 0) break;

    await db.transaction(async (tx) => {
      for (const user of batch) {
        const slug = slugify(user.name, { lower: true });
        await tx.update(users)
          .set({ slug })
          .where(eq(users.id, user.id));
      }
    });

    processed += batch.length;
    console.log(`Processed ${processed} users`);
  }

  console.log(`Backfill complete. Total: ${processed}`);
}

backfillSlugs().catch(console.error);
```

## Rollback Strategies

### With Prisma

```bash
# Prisma doesn't have built-in rollback
# Instead, create a new migration that reverses changes

# Mark migration as rolled back (doesn't undo changes)
npx prisma migrate resolve --rolled-back 20240101_add_phone
```

### Manual Rollback

```typescript
// migrations/rollback-20240101.ts
import { db } from '../src/db';

async function rollback(): Promise<void> {
  await db.transaction(async (tx) => {
    // Reverse the changes
    await tx.schema.alterTable('users').dropColumn('phone');
  });

  // Update migration table
  await db.delete(migrations)
    .where(eq(migrations.name, '20240101_add_phone'));
}

rollback().catch(console.error);
```

## Zero-Downtime Migration Checklist

1. **Backward compatible** - Old code works with new schema
2. **Forward compatible** - New code works with old schema
3. **Non-blocking** - Use CONCURRENTLY for indexes
4. **Batched** - Process large data in batches
5. **Idempotent** - Safe to run multiple times
6. **Monitored** - Watch for locks and performance

## Migration Testing

```typescript
// migrations/__tests__/add-phone.test.ts
import { describe, it, expect, beforeAll, afterAll } from 'vitest';
import { migrate } from '../add-phone';
import { rollback } from '../rollback-add-phone';
import { setupTestDb, teardownTestDb } from '../../tests/utils';

describe('add-phone migration', () => {
  beforeAll(async () => {
    await setupTestDb();
  });

  afterAll(async () => {
    await teardownTestDb();
  });

  it('adds phone column', async () => {
    await migrate();

    const columns = await db.query(`
      SELECT column_name FROM information_schema.columns
      WHERE table_name = 'users' AND column_name = 'phone'
    `);

    expect(columns.length).toBe(1);
  });

  it('rollback removes phone column', async () => {
    await rollback();

    const columns = await db.query(`
      SELECT column_name FROM information_schema.columns
      WHERE table_name = 'users' AND column_name = 'phone'
    `);

    expect(columns.length).toBe(0);
  });
});
```

## CI/CD Integration

```yaml
# .github/workflows/migrate.yml
name: Database Migration

on:
  push:
    branches: [main]
    paths:
      - 'prisma/migrations/**'

jobs:
  migrate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: '22'

      - run: npm ci

      - name: Run migrations
        run: npx prisma migrate deploy
        env:
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
```

## Best Practices

1. **One change per migration** - Easier to debug and rollback
2. **Test migrations** - Run against production-like data
3. **Backup before migrating** - Always have a restore point
4. **Monitor locks** - Watch for blocking queries
5. **Schedule large migrations** - During low-traffic periods
6. **Document migrations** - Explain why, not just what

## Notes

- Never modify existing migrations after deployment
- Large data migrations should be batched
- Use transactions for consistency
- Always test rollback procedures
