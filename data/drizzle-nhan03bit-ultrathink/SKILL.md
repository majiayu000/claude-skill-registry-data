---
name: drizzle
description: Drizzle ORM type-safe queries, schema definitions, migrations, relations, transactions, and performance patterns
layer: domain
category: database
triggers:
  - "drizzle"
  - "drizzle orm"
  - "drizzle kit"
  - "drizzle schema"
  - "drizzle query"
inputs:
  - "Data model requirements"
  - "Query patterns"
  - "Migration needs"
outputs:
  - "Drizzle schema definitions"
  - "Type-safe query implementations"
  - "Migration configurations"
linksTo:
  - postgresql
  - nodejs
  - graphql
  - microservices
linkedFrom:
  - error-handling
  - testing
preferredNextSkills:
  - postgresql
  - nodejs
  - redis
fallbackSkills:
  - prisma
  - supabase
riskLevel: low
memoryReadPolicy: selective
memoryWritePolicy: none
sideEffects: []
---

# Drizzle ORM Domain Skill

## Purpose

Provide expert-level guidance on Drizzle ORM, including schema definitions, type-safe queries, relational queries, migrations with Drizzle Kit, transactions, prepared statements, and performance optimization. Drizzle is SQL-first: if you know SQL, you know Drizzle.

## Why Drizzle

- **Zero overhead**: Generates SQL at build time, no runtime query parsing
- **SQL-like API**: `select().from().where()` maps directly to SQL
- **Full type safety**: Schema types flow through all queries
- **Serverless-friendly**: Lightweight, no heavy runtime, works with edge functions
- **Relational queries**: Prisma-like `with` syntax for nested data

## Key Patterns

### 1. Schema Definition

```typescript
// db/schema/users.ts
import {
  pgTable, text, timestamp, boolean, integer, uuid,
  uniqueIndex, index, pgEnum, check, primaryKey,
} from 'drizzle-orm/pg-core';
import { relations, sql } from 'drizzle-orm';

// Enums
export const roleEnum = pgEnum('role', ['admin', 'member', 'viewer']);

// Tables
export const users = pgTable('users', {
  id: uuid('id').primaryKey().defaultRandom(),
  email: text('email').notNull(),
  name: text('name').notNull(),
  role: roleEnum('role').notNull().default('member'),
  isActive: boolean('is_active').notNull().default(true),
  credits: integer('credits').notNull().default(0),
  createdAt: timestamp('created_at', { withTimezone: true }).notNull().defaultNow(),
  updatedAt: timestamp('updated_at', { withTimezone: true }).notNull().defaultNow()
    .$onUpdate(() => new Date()),
  deletedAt: timestamp('deleted_at', { withTimezone: true }),
}, (table) => [
  uniqueIndex('users_email_idx').on(table.email),
  index('users_role_created_idx').on(table.role, table.createdAt),
  index('users_active_idx').on(table.email).where(
    sql`${table.isActive} = true AND ${table.deletedAt} IS NULL`
  ),
  check('credits_non_negative', sql`${table.credits} >= 0`),
]);

export const posts = pgTable('posts', {
  id: uuid('id').primaryKey().defaultRandom(),
  title: text('title').notNull(),
  slug: text('slug').notNull().unique(),
  content: text('content').notNull(),
  published: boolean('published').notNull().default(false),
  publishedAt: timestamp('published_at', { withTimezone: true }),
  authorId: uuid('author_id').notNull().references(() => users.id, { onDelete: 'cascade' }),
  viewCount: integer('view_count').notNull().default(0),
  tags: text('tags').array(),
  createdAt: timestamp('created_at', { withTimezone: true }).notNull().defaultNow(),
  updatedAt: timestamp('updated_at', { withTimezone: true }).notNull().defaultNow()
    .$onUpdate(() => new Date()),
}, (table) => [
  index('posts_author_published_idx').on(table.authorId, table.published),
  index('posts_published_date_idx').on(table.published, table.publishedAt),
]);

export const categories = pgTable('categories', {
  id: uuid('id').primaryKey().defaultRandom(),
  name: text('name').notNull().unique(),
  slug: text('slug').notNull().unique(),
});

export const postsToCategories = pgTable('posts_to_categories', {
  postId: uuid('post_id').notNull().references(() => posts.id, { onDelete: 'cascade' }),
  categoryId: uuid('category_id').notNull().references(() => categories.id, { onDelete: 'cascade' }),
  assignedAt: timestamp('assigned_at', { withTimezone: true }).notNull().defaultNow(),
}, (table) => [
  // Composite primary key
  primaryKey({ columns: [table.postId, table.categoryId] }),
]);

// Relations (for relational query API)
export const usersRelations = relations(users, ({ many, one }) => ({
  posts: many(posts),
  profile: one(profiles, {
    fields: [users.id],
    references: [profiles.userId],
  }),
}));

export const postsRelations = relations(posts, ({ one, many }) => ({
  author: one(users, {
    fields: [posts.authorId],
    references: [users.id],
  }),
  categories: many(postsToCategories),
}));

export const postsToCategoriesRelations = relations(postsToCategories, ({ one }) => ({
  post: one(posts, {
    fields: [postsToCategories.postId],
    references: [posts.id],
  }),
  category: one(categories, {
    fields: [postsToCategories.categoryId],
    references: [categories.id],
  }),
}));
```

### 2. Database Client Setup

```typescript
// db/index.ts
import { drizzle } from 'drizzle-orm/node-postgres';
import { Pool } from 'pg';
import * as schema from './schema';

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  max: 20,
  idleTimeoutMillis: 30_000,
  connectionTimeoutMillis: 5_000,
});

export const db = drizzle(pool, {
  schema,
  logger: process.env.NODE_ENV === 'development',
});

// For serverless (Neon, Vercel Postgres)
import { neon } from '@neondatabase/serverless';
import { drizzle as drizzleNeon } from 'drizzle-orm/neon-http';

const sql = neon(process.env.DATABASE_URL!);
export const db = drizzleNeon(sql, { schema });

// Type exports
export type Database = typeof db;
export type User = typeof schema.users.$inferSelect;
export type NewUser = typeof schema.users.$inferInsert;
```

### 3. Query Patterns

```typescript
import { eq, and, or, gt, lt, desc, asc, sql, ilike, inArray, isNull, count, avg } from 'drizzle-orm';

// Basic CRUD
// Select with filtering
const activeAdmins = await db
  .select()
  .from(users)
  .where(
    and(
      eq(users.role, 'admin'),
      eq(users.isActive, true),
      isNull(users.deletedAt),
    )
  )
  .orderBy(desc(users.createdAt))
  .limit(20);

// Select specific columns
const userEmails = await db
  .select({ id: users.id, email: users.email, name: users.name })
  .from(users)
  .where(eq(users.isActive, true));

// Insert with returning
const [newUser] = await db
  .insert(users)
  .values({
    email: 'jane@example.com',
    name: 'Jane Doe',
    role: 'member',
  })
  .returning();

// Bulk insert
await db.insert(users).values([
  { email: 'a@example.com', name: 'Alice' },
  { email: 'b@example.com', name: 'Bob' },
]);

// Update
const [updated] = await db
  .update(users)
  .set({ name: 'Jane Updated', role: 'admin' })
  .where(eq(users.id, userId))
  .returning();

// Upsert (INSERT ... ON CONFLICT)
await db
  .insert(users)
  .values({ email: 'jane@example.com', name: 'Jane', credits: 100 })
  .onConflictDoUpdate({
    target: users.email,
    set: { credits: sql`${users.credits} + 100` },
  });

// Delete
await db.delete(users).where(eq(users.id, userId));

// Joins
const postsWithAuthors = await db
  .select({
    postId: posts.id,
    title: posts.title,
    authorName: users.name,
    authorEmail: users.email,
  })
  .from(posts)
  .innerJoin(users, eq(posts.authorId, users.id))
  .where(eq(posts.published, true))
  .orderBy(desc(posts.createdAt))
  .limit(20);

// Subqueries
const subquery = db
  .select({ authorId: posts.authorId, postCount: count().as('post_count') })
  .from(posts)
  .where(eq(posts.published, true))
  .groupBy(posts.authorId)
  .as('post_counts');

const prolificAuthors = await db
  .select({
    name: users.name,
    email: users.email,
    postCount: subquery.postCount,
  })
  .from(users)
  .innerJoin(subquery, eq(users.id, subquery.authorId))
  .where(gt(subquery.postCount, 10))
  .orderBy(desc(subquery.postCount));

// Aggregations
const stats = await db
  .select({
    role: users.role,
    count: count(),
    avgCredits: avg(users.credits),
  })
  .from(users)
  .where(eq(users.isActive, true))
  .groupBy(users.role);
```

### 4. Relational Queries (Prisma-like API)

```typescript
// Nested queries with the relational API
const usersWithPosts = await db.query.users.findMany({
  where: eq(users.isActive, true),
  columns: {
    id: true,
    name: true,
    email: true,
  },
  with: {
    posts: {
      where: eq(posts.published, true),
      orderBy: [desc(posts.createdAt)],
      limit: 5,
      columns: {
        id: true,
        title: true,
        slug: true,
        createdAt: true,
      },
      with: {
        categories: {
          with: {
            category: true,
          },
        },
      },
    },
    profile: true,
  },
  orderBy: [desc(users.createdAt)],
  limit: 20,
});

// Find first
const user = await db.query.users.findFirst({
  where: eq(users.email, 'jane@example.com'),
  with: { profile: true },
});
```

### 5. Transactions and Prepared Statements

```typescript
// Transaction
async function transferCredits(fromId: string, toId: string, amount: number) {
  return db.transaction(async (tx) => {
    const [sender] = await tx
      .select({ credits: users.credits })
      .from(users)
      .where(eq(users.id, fromId))
      .for('update'); // SELECT ... FOR UPDATE

    if (!sender || sender.credits < amount) {
      throw new Error('Insufficient credits');
      // Transaction auto-rolls back on throw
    }

    await tx
      .update(users)
      .set({ credits: sql`${users.credits} - ${amount}` })
      .where(eq(users.id, fromId));

    await tx
      .update(users)
      .set({ credits: sql`${users.credits} + ${amount}` })
      .where(eq(users.id, toId));

    return { success: true };
  });
}

// Prepared statements (reusable, optimized)
const getUserByEmail = db
  .select()
  .from(users)
  .where(eq(users.email, sql.placeholder('email')))
  .prepare('get_user_by_email');

const user = await getUserByEmail.execute({ email: 'jane@example.com' });

// Dynamic where builder
function buildFilter(params: {
  search?: string;
  role?: string;
  active?: boolean;
}) {
  const conditions = [];

  if (params.search) {
    conditions.push(
      or(
        ilike(users.name, `%${params.search}%`),
        ilike(users.email, `%${params.search}%`),
      )
    );
  }

  if (params.role) {
    conditions.push(eq(users.role, params.role));
  }

  if (params.active !== undefined) {
    conditions.push(eq(users.isActive, params.active));
  }

  return conditions.length > 0 ? and(...conditions) : undefined;
}
```

### 6. Migrations with Drizzle Kit

```typescript
// drizzle.config.ts
import { defineConfig } from 'drizzle-kit';

export default defineConfig({
  schema: './db/schema/*',
  out: './db/migrations',
  dialect: 'postgresql',
  dbCredentials: {
    url: process.env.DATABASE_URL!,
  },
  verbose: true,
  strict: true,
});
```

```bash
# Generate migration from schema changes
npx drizzle-kit generate

# Apply migrations
npx drizzle-kit migrate

# Open Drizzle Studio (database GUI)
npx drizzle-kit studio

# Push schema directly (development only)
npx drizzle-kit push
```

## Best Practices

1. **Use the SQL-like API** for complex queries, relational API for nested reads
2. **Define relations** even if you only use the SQL API -- enables relational queries later
3. **Use `$inferSelect` and `$inferInsert`** for type exports, not manual type definitions
4. **Use prepared statements** for frequently executed queries
5. **Use `sql.placeholder()`** for dynamic but safe parameterized queries
6. **Colocate schema with feature** -- e.g., `features/users/schema.ts`
7. **Use `drizzle-kit generate`** for migrations, not `push` in production
8. **Add indexes** in the table definition, not as afterthoughts
9. **Use `.returning()`** after insert/update to avoid extra SELECT queries
10. **Use `for('update')`** in transactions to prevent race conditions

## Common Pitfalls

| Pitfall | Impact | Fix |
|---------|--------|-----|
| Missing `relations()` definitions | Relational queries fail | Define relations for all foreign keys |
| Using `push` in production | Data loss risk | Use `generate` + `migrate` in production |
| Not using `.returning()` | Extra SELECT query needed | Chain `.returning()` on insert/update |
| Missing indexes on foreign keys | Slow joins | Add `index()` on all FK columns |
| Not handling `undefined` in dynamic filters | Invalid SQL generated | Use conditional array building with `and()` |
| Forgetting `$onUpdate` for `updatedAt` | Stale timestamps | Add `.$onUpdate(() => new Date())` |
| Using raw SQL without `sql` template | SQL injection risk | Always use `sql\`...\`` tagged template |
