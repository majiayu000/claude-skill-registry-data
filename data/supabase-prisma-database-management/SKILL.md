---
name: supabase-prisma-database-management
description: This skill should be used when managing database schema, migrations, and seed data using Prisma ORM with Supabase PostgreSQL. Apply when setting up Prisma with Supabase, creating migrations, seeding data, configuring shadow database for migration preview, adding schema validation to CI, or managing database changes across environments.
---

# Supabase + Prisma Database Management

## Overview

Manage database schema, migrations, and seed data using Prisma ORM with Supabase PostgreSQL, including shadow database configuration, seed files, and automated schema checks in CI.

## Installation and Setup

### 1. Install Prisma

Install Prisma CLI and client:

```bash
npm install -D prisma
npm install @prisma/client
```

### 2. Initialize Prisma

Initialize Prisma in your project:

```bash
npx prisma init
```

This creates:
- `prisma/schema.prisma` - Database schema definition
- `.env` - Environment variables (add `DATABASE_URL`)

### 3. Configure Supabase Connection

Get your Supabase database URL from:
- Supabase Dashboard > Project Settings > Database > Connection String > URI

Add to `.env`:

```env
# Transaction pooler for Prisma migrations
DATABASE_URL="postgresql://postgres:[YOUR-PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres"

# Session pooler for queries (with pgBouncer)
DIRECT_URL="postgresql://postgres:[YOUR-PASSWORD]@db.[PROJECT-REF].supabase.co:6543/postgres?pgbouncer=true"
```

Update `prisma/schema.prisma` to use both URLs:

```prisma
datasource db {
  provider  = "postgresql"
  url       = env("DIRECT_URL")
  directUrl = env("DATABASE_URL")
}
```

**Why two URLs?**
- `DATABASE_URL`: Direct connection for migrations (required)
- `DIRECT_URL`: Pooled connection for application queries (optional, better performance)

### 4. Configure Shadow Database (Required for Migrations)

For migration preview and validation, configure a shadow database in `prisma/schema.prisma`:

```prisma
datasource db {
  provider  = "postgresql"
  url       = env("DIRECT_URL")
  directUrl = env("DATABASE_URL")
  shadowDatabaseUrl = env("SHADOW_DATABASE_URL")
}
```

Add to `.env`:

```env
SHADOW_DATABASE_URL="postgresql://postgres:[PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres"
```

**Note**: Supabase free tier allows using the same database for shadow. For production, use a separate database.

## Schema Definition

### 1. Define Your Schema

Edit `prisma/schema.prisma` using the example from `assets/example-schema.prisma`. This example includes:

- User profiles with auth integration
- Timestamps with `@default(now())` and `@updatedAt`
- Relations between entities
- Indexes for performance
- Unique constraints

Key Prisma features:
- `@id @default(uuid())` - Auto-generated UUIDs
- `@default(now())` - Automatic timestamps
- `@updatedAt` - Auto-update on modification
- `@@index([field])` - Database indexes
- `@relation` - Define relationships

### 2. Link to Supabase Auth

To integrate with Supabase Auth, reference the `auth.users` table:

```prisma
model Profile {
  id        String   @id @db.Uuid
  email     String   @unique
  // Other fields...

  // This doesn't create a foreign key, just documents the relationship
  // The actual user exists in auth.users (managed by Supabase)
}
```

**Important**: Don't create a foreign key to `auth.users` as it's in a different schema. Handle the relationship in application logic.

## Migrations

### 1. Create Migration

After defining/modifying schema, create a migration:

```bash
npx prisma migrate dev --name add_profiles_table
```

This:
- Generates SQL migration in `prisma/migrations/`
- Applies migration to database
- Regenerates Prisma Client
- Runs seed script (if configured)

### 2. Review Migration SQL

Always review generated SQL in `prisma/migrations/[timestamp]_[name]/migration.sql`:

```sql
-- CreateTable
CREATE TABLE "Profile" (
    "id" UUID NOT NULL,
    "email" TEXT NOT NULL,
    -- ...

    CONSTRAINT "Profile_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "Profile_email_key" ON "Profile"("email");
```

Make manual adjustments if needed before applying to production.

### 3. Apply Migrations in Production

For production deployments:

```bash
npx prisma migrate deploy
```

This applies pending migrations without prompts or seeds.

**CI/CD Integration**: Add to your deployment pipeline:

```yaml
# Example GitHub Actions step
- name: Run migrations
  run: npx prisma migrate deploy
  env:
    DATABASE_URL: ${{ secrets.DATABASE_URL }}
```

### 4. Reset Database (Development Only)

To reset database to clean state:

```bash
npx prisma migrate reset
```

This:
- Drops database
- Creates database
- Applies all migrations
- Runs seed script

**Warning**: This deletes all data. Only use in development.

## Seeding Data

### 1. Create Seed Script

Create `prisma/seed.ts` using the template from `assets/seed.ts`. This script:

- Uses Prisma Client to insert data
- Creates initial users, settings, or reference data
- Can be run manually or after migrations
- Supports idempotent operations (safe to run multiple times)

### 2. Configure Seed in package.json

Add seed configuration to `package.json`:

```json
{
  "prisma": {
    "seed": "ts-node --compiler-options {\"module\":\"CommonJS\"} prisma/seed.ts"
  }
}
```

Install ts-node for TypeScript execution:

```bash
npm install -D ts-node
```

### 3. Run Seed Manually

Execute seed script:

```bash
npx prisma db seed
```

Seed runs automatically after `prisma migrate dev` and `prisma migrate reset`.

### 4. Idempotent Seeding

Make seeds safe to run multiple times using upsert:

```typescript
await prisma.user.upsert({
  where: { email: 'admin@example.com' },
  update: {}, // No updates if exists
  create: {
    email: 'admin@example.com',
    name: 'Admin User',
  },
});
```

## Prisma Client Usage

### 1. Generate Client

After schema changes, regenerate Prisma Client:

```bash
npx prisma generate
```

This updates `node_modules/@prisma/client` with types matching your schema.

### 2. Use in Next.js Server Components

Create a Prisma client singleton using `assets/prisma-client.ts`:

```typescript
import { prisma } from '@/lib/prisma';

export default async function UsersPage() {
  const users = await prisma.profile.findMany();

  return (
    <ul>
      {users.map((user) => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  );
}
```

### 3. Use in Server Actions

```typescript
'use server';

import { prisma } from '@/lib/prisma';
import { revalidatePath } from 'next/cache';

export async function createProfile(formData: FormData) {
  const name = formData.get('name') as string;

  await prisma.profile.create({
    data: {
      name,
      email: formData.get('email') as string,
    },
  });

  revalidatePath('/profiles');
}
```

## CI/CD Integration

### 1. Add Schema Validation to CI

Create `.github/workflows/schema-check.yml` using the template from `assets/github-workflows-schema-check.yml`. This workflow:

- Runs on pull requests
- Validates schema syntax
- Checks for migration drift
- Ensures migrations are generated
- Verifies Prisma Client generation

### 2. Migration Deployment

Add migration step to deployment workflow:

```yaml
- name: Apply database migrations
  run: npx prisma migrate deploy
  env:
    DATABASE_URL: ${{ secrets.PROD_DATABASE_URL }}
```

### 3. Environment-Specific Databases

Use different database URLs for each environment:

```env
# Development
DATABASE_URL="postgresql://localhost:5432/dev"

# Staging
DATABASE_URL="postgresql://staging-db.supabase.co:5432/postgres"

# Production
DATABASE_URL="postgresql://prod-db.supabase.co:5432/postgres"
```

## Best Practices

### Schema Design

1. **Use UUIDs for IDs**: Better for distributed systems
2. **Add Timestamps**: Track `createdAt` and `updatedAt`
3. **Define Indexes**: Improve query performance on filtered fields
4. **Use Enums**: Type-safe status/role fields
5. **Validate at DB Level**: Use unique constraints and checks

### Migration Management

1. **Review Before Applying**: Always check generated SQL
2. **Name Descriptively**: Use clear migration names
3. **Keep Atomic**: One logical change per migration
4. **Test Locally First**: Verify migrations work before production
5. **Never Modify Applied Migrations**: Create new ones instead

### Prisma Client

1. **Use Singleton Pattern**: Prevent connection exhaustion
2. **Close in Serverless**: Disconnect after operations
3. **Type Everything**: Leverage Prisma's TypeScript types
4. **Use Select**: Only fetch needed fields
5. **Batch Operations**: Use `createMany`, `updateMany` for bulk ops

## Troubleshooting

**Migration fails with "relation already exists"**: Reset development database with `npx prisma migrate reset`. For production, manually fix conflicts.

**Prisma Client out of sync**: Run `npx prisma generate` after schema changes.

**Connection pool exhausted**: Use connection pooling via `DIRECT_URL` with pgBouncer.

**Shadow database errors**: Ensure shadow database URL is correct and accessible. For Supabase free tier, same DB can be used.

**Type errors after schema changes**: Restart TypeScript server in IDE after `prisma generate`.

## Resources

### scripts/

No executable scripts needed for this skill.

### references/

- `prisma-best-practices.md` - Comprehensive guide to Prisma patterns, performance optimization, and common pitfalls
- `supabase-integration.md` - Specific considerations for using Prisma with Supabase, including RLS integration

### assets/

- `example-schema.prisma` - Complete schema example with common patterns (auth, timestamps, relations, indexes)
- `seed.ts` - Idempotent seed script template for initial data
- `prisma-client.ts` - Singleton Prisma Client for Next.js to prevent connection exhaustion
- `github-workflows-schema-check.yml` - CI workflow for schema validation and migration checks
