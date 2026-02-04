---
name: rwsdk-database-do
description: Use when working with rwsdk/db for SQLite Durable Objects - covers setup with migrations, type-safe queries with Kysely, CRUD operations, joins, seeding, and migration rollback handling in Cloudflare Workers environments
---

# rwsdk Database DO

## Overview

rwsdk/db provides SQLite databases using Durable Objects with type-safe queries via Kysely. Each database instance runs in isolated Durable Objects with schema types inferred directly from migrations. No code generation needed - TypeScript understands your schema automatically.

## When to Use

Use when:

- Building Cloudflare Workers apps needing SQL databases
- Want runtime database creation with minimal setup
- Need isolated database instances (multi-tenant, modular components)
- Prefer SQL query builder over ORMs
- Working with rwsdk framework

Don't use when:

- Need globally distributed low-latency reads (single location limitation)
- Require production-grade backup features (preview feature)
- Complex ORM requirements outweigh simplicity benefits

## Quick Setup (5 Files)

### 1. Define Migrations (`db/migrations.ts`)

```typescript
import { type Migrations } from 'rwsdk/db';

export const migrations = {
  '001_initial_schema': {
    async up(db) {
      await db.schema
        .createTable('todos')
        .addColumn('id', 'text', (col) => col.primaryKey())
        .addColumn('text', 'text', (col) => col.notNull())
        .addColumn('completed', 'integer', (col) => col.notNull().defaultTo(0))
        .addColumn('createdAt', 'text', (col) => col.notNull())
        .execute();
    },
    async down(db) {
      // CRITICAL: Use .ifExists() for SQLite's non-transactional DDL
      await db.schema.dropTable('todos').ifExists().execute();
    },
  },
} satisfies Migrations;
```

### 2. Create Database Instance (`db/db.ts`)

```typescript
import { env } from 'cloudflare:workers';
import { type Database, createDb } from 'rwsdk/db';
import { type migrations } from '@/db/migrations';

// Export inferred types
export type AppDatabase = Database<typeof migrations>;
export type Todo = AppDatabase['todos'];

// Create database instance
export const db = createDb<AppDatabase>(
  env.APP_DURABLE_OBJECT,
  'todo-database' // unique key for this instance
);
```

### 3. Create Durable Object Class (`db/durableObject.ts`)

```typescript
import { SqliteDurableObject } from 'rwsdk/db';
import { migrations } from '@/db/migrations';

export class AppDurableObject extends SqliteDurableObject {
  migrations = migrations;
}
```

### 4. Export from Worker (`worker.ts`)

```typescript
export { AppDurableObject } from '@/db/durableObject';
// ... rest of worker code
```

### 5. Configure Wrangler (`wrangler.toml`)

```toml
[durable_objects]
bindings = [
  { name = "APP_DURABLE_OBJECT", class_name = "AppDurableObject" }
]

[[migrations]]
tag = "v1"
new_sqlite_classes = ["AppDurableObject"]
```

## Type Inference

Types are automatically inferred from migrations - no code generation:

```typescript
// TypeScript knows all columns and types
const user = await db.selectFrom('users').selectAll().executeTakeFirst();
// Type: { id: string, username: string } | undefined
```

## CRUD Operations Reference

| Operation      | Pattern                                 | Example                                                                              |
| -------------- | --------------------------------------- | ------------------------------------------------------------------------------------ |
| **Insert**     | `insertInto().values().execute()`       | `await db.insertInto("todos").values(todo).execute()`                                |
| **Select**     | `selectFrom().selectAll().execute()`    | `await db.selectFrom("todos").selectAll().execute()`                                 |
| **Select One** | `selectFrom().executeTakeFirst()`       | `await db.selectFrom("todos").where("id", "=", id).executeTakeFirst()`               |
| **Update**     | `updateTable().set().where().execute()` | `await db.updateTable("todos").set({ completed: 1 }).where("id", "=", id).execute()` |
| **Delete**     | `deleteFrom().where().execute()`        | `await db.deleteFrom("todos").where("id", "=", id).execute()`                        |

## Joins and Nested Data

Use Kysely helpers for ORM-like nested results:

```typescript
import { jsonObjectFrom } from 'kysely/helpers/sqlite';

const posts = await db
  .selectFrom('posts')
  .selectAll('posts')
  .select((eb) => [
    jsonObjectFrom(
      eb
        .selectFrom('users')
        .select(['id', 'username'])
        .whereRef('users.id', '=', 'posts.userId')
    ).as('author'),
  ])
  .execute();

// Result: [{ id: "post-123", title: "...", author: { id: "...", username: "..." } }]
```

## Database Seeding

Create seed script with default export:

```typescript
// scripts/seed.ts
import { db } from '@/db/db';

export default async () => {
  console.log('🌱 Seeding...');
  await db.deleteFrom('todos').execute();

  await db
    .insertInto('todos')
    .values([
      {
        id: crypto.randomUUID(),
        text: 'First todo',
        completed: 0,
        createdAt: new Date().toISOString(),
      },
    ])
    .execute();

  console.log('✓ Seeded');
};
```

Add to `package.json`:

```json
{
  "scripts": {
    "seed": "rwsdk worker-run ./src/scripts/seed.ts"
  }
}
```

Run: `npm run seed`

## Migration Timing

Migrations run when `createDb()` is called:

- **Development**: On dev server start
- **Production**: During deployment (initial request triggers migration)

## Migration Failures and Rollback

**CRITICAL**: SQLite doesn't support transactional DDL. Failed migrations can leave partial state.

**Automatic behavior**: Failed `up()` triggers `down()` automatically

**Write defensive down() functions**:

```typescript
async down(db) {
  // Always use .ifExists() in case up() partially failed
  await db.schema.dropTable("posts").ifExists().execute();
  await db.schema.dropTable("users").ifExists().execute();
}
```

**Why auto-rollback**: Returns database to known-good state since manual intervention isn't feasible in isolated runtime environments.

## Common Mistakes

| Mistake                                       | Fix                                                         |
| --------------------------------------------- | ----------------------------------------------------------- |
| **Missing `.ifExists()` in down()**           | Always use `.ifExists()` for rollback safety                |
| **Forgetting to export DO from worker**       | Add `export { AppDurableObject }` to worker file            |
| **Wrong wrangler.toml binding name**          | Match `env.APP_DURABLE_OBJECT` to wrangler binding name     |
| **Multiple DB instances without unique keys** | Each `createDb()` call needs unique key parameter           |
| **Not awaiting `.execute()`**                 | All Kysely queries must end with `.execute()`               |
| **Accessing tables before migrations run**    | Module-level `createDb()` ensures migrations run on startup |

## API Quick Reference

**createDb()**

```typescript
createDb<T>(
  durableObjectNamespace: DurableObjectNamespace,
  key: string
): Database<T>
```

**Migration structure**

```typescript
{
  "001_migration_name": {
    async up(db) { /* create schema */ },
    async down(db) { /* undo with .ifExists() */ }
  }
} satisfies Migrations
```

**Type exports**

```typescript
export type AppDatabase = Database<typeof migrations>;
export type TableName = AppDatabase['tableName'];
```

## Performance Notes

- **Latency**: Single-location execution (not globally distributed)
- **Isolation**: Perfect for modular components, multi-tenant apps
- **Scale**: Can create multiple instances with different keys for geographic distribution
- **Backups**: No built-in backup features (implement external replication for critical data)

## Complete Kysely Documentation

For full query builder capabilities, see [Kysely docs](https://kysely.dev/docs). Everything in Kysely works with rwsdk/db.

## Real-World Patterns

**Multiple database instances**:

```typescript
const userDb = createDb(env.DO, 'users');
const analyticsDb = createDb(env.DO, 'analytics'); // isolated
```

**Type-safe table access**:

```typescript
type User = AppDatabase['users']; // Inferred from migrations
const users: User[] = await db.selectFrom('users').selectAll().execute();
```

**Conditional queries**:

```typescript
let query = db.selectFrom('posts').selectAll();
if (userId) {
  query = query.where('userId', '=', userId);
}
const posts = await query.execute();
```
