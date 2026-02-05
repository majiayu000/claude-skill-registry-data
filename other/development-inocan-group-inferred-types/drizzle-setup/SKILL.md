---
name: drizzle-setup
description: Drizzle ORM configuration and patterns. Use as a lightweight alternative to Prisma.
---

# Drizzle ORM Setup Skill

This skill covers Drizzle ORM setup and patterns for Node.js applications.

## When to Use

Use this skill when:
- Preferring SQL-first approach
- Need lightweight ORM
- Want full SQL control
- Building high-performance APIs

## Core Principle

**SQL-FIRST, TYPE-SAFE** - Drizzle generates TypeScript types from SQL schemas. Full SQL control with type safety.

## Installation

```bash
npm install drizzle-orm postgres
npm install -D drizzle-kit
```

## Schema Definition

```typescript
// src/db/schema.ts
import {
  pgTable,
  text,
  timestamp,
  boolean,
  pgEnum,
  index,
  uniqueIndex,
} from 'drizzle-orm/pg-core';
import { relations } from 'drizzle-orm';
import { createId } from '@paralleldrive/cuid2';

// Enums
export const roleEnum = pgEnum('role', ['USER', 'MODERATOR', 'ADMIN']);

// Users table
export const users = pgTable('users', {
  id: text('id').primaryKey().$defaultFn(() => createId()),
  email: text('email').notNull().unique(),
  name: text('name').notNull(),
  password: text('password').notNull(),
  role: roleEnum('role').default('USER').notNull(),
  createdAt: timestamp('created_at').defaultNow().notNull(),
  updatedAt: timestamp('updated_at').defaultNow().notNull(),
}, (table) => ({
  emailIdx: uniqueIndex('users_email_idx').on(table.email),
  roleIdx: index('users_role_idx').on(table.role),
}));

// Profiles table
export const profiles = pgTable('profiles', {
  id: text('id').primaryKey().$defaultFn(() => createId()),
  bio: text('bio'),
  avatar: text('avatar'),
  userId: text('user_id').notNull().references(() => users.id, { onDelete: 'cascade' }).unique(),
});

// Posts table
export const posts = pgTable('posts', {
  id: text('id').primaryKey().$defaultFn(() => createId()),
  title: text('title').notNull(),
  slug: text('slug').notNull().unique(),
  content: text('content'),
  published: boolean('published').default(false).notNull(),
  authorId: text('author_id').notNull().references(() => users.id, { onDelete: 'cascade' }),
  createdAt: timestamp('created_at').defaultNow().notNull(),
  updatedAt: timestamp('updated_at').defaultNow().notNull(),
}, (table) => ({
  slugIdx: uniqueIndex('posts_slug_idx').on(table.slug),
  authorIdx: index('posts_author_idx').on(table.authorId),
  publishedIdx: index('posts_published_idx').on(table.published, table.createdAt),
}));

// Tags table
export const tags = pgTable('tags', {
  id: text('id').primaryKey().$defaultFn(() => createId()),
  name: text('name').notNull().unique(),
});

// Posts to Tags junction table
export const postsToTags = pgTable('posts_to_tags', {
  postId: text('post_id').notNull().references(() => posts.id, { onDelete: 'cascade' }),
  tagId: text('tag_id').notNull().references(() => tags.id, { onDelete: 'cascade' }),
}, (table) => ({
  pk: index('posts_to_tags_pk').on(table.postId, table.tagId),
}));

// Relations
export const usersRelations = relations(users, ({ one, many }) => ({
  profile: one(profiles, {
    fields: [users.id],
    references: [profiles.userId],
  }),
  posts: many(posts),
}));

export const profilesRelations = relations(profiles, ({ one }) => ({
  user: one(users, {
    fields: [profiles.userId],
    references: [users.id],
  }),
}));

export const postsRelations = relations(posts, ({ one, many }) => ({
  author: one(users, {
    fields: [posts.authorId],
    references: [users.id],
  }),
  tags: many(postsToTags),
}));

export const tagsRelations = relations(tags, ({ many }) => ({
  posts: many(postsToTags),
}));

export const postsToTagsRelations = relations(postsToTags, ({ one }) => ({
  post: one(posts, {
    fields: [postsToTags.postId],
    references: [posts.id],
  }),
  tag: one(tags, {
    fields: [postsToTags.tagId],
    references: [tags.id],
  }),
}));
```

## Client Setup

```typescript
// src/db/index.ts
import { drizzle } from 'drizzle-orm/postgres-js';
import postgres from 'postgres';
import * as schema from './schema';

const connectionString = process.env.DATABASE_URL!;

// For query purposes
const queryClient = postgres(connectionString);
export const db = drizzle(queryClient, { schema });

// For migrations
export const migrationClient = postgres(connectionString, { max: 1 });
```

### Fastify Plugin

```typescript
// src/plugins/database.ts
import { FastifyPluginAsync } from 'fastify';
import fp from 'fastify-plugin';
import { drizzle } from 'drizzle-orm/postgres-js';
import postgres from 'postgres';
import * as schema from '../db/schema';

type DB = ReturnType<typeof drizzle<typeof schema>>;

declare module 'fastify' {
  interface FastifyInstance {
    db: DB;
  }
}

const databasePlugin: FastifyPluginAsync = async (fastify) => {
  const client = postgres(process.env.DATABASE_URL!);
  const db = drizzle(client, { schema });

  fastify.decorate('db', db);

  fastify.addHook('onClose', async () => {
    await client.end();
  });
};

export default fp(databasePlugin, { name: 'database' });
```

## Query Patterns

### Basic CRUD

```typescript
import { eq, desc, and, or, like, sql } from 'drizzle-orm';
import { db } from './db';
import { users, posts, tags } from './db/schema';

// Create
const [user] = await db.insert(users).values({
  email: 'user@example.com',
  name: 'User',
  password: hashedPassword,
}).returning();

// Read single
const user = await db.query.users.findFirst({
  where: eq(users.id, userId),
});

// Read many
const allUsers = await db.query.users.findMany({
  where: eq(users.role, 'USER'),
  orderBy: desc(users.createdAt),
  limit: 10,
});

// Update
const [updated] = await db.update(users)
  .set({ name: 'New Name', updatedAt: new Date() })
  .where(eq(users.id, userId))
  .returning();

// Delete
await db.delete(users).where(eq(users.id, userId));
```

### Relations

```typescript
// Query with relations
const userWithPosts = await db.query.users.findFirst({
  where: eq(users.id, userId),
  with: {
    profile: true,
    posts: {
      where: eq(posts.published, true),
      limit: 10,
      orderBy: desc(posts.createdAt),
      with: {
        tags: {
          with: {
            tag: true,
          },
        },
      },
    },
  },
});

// Select specific columns
const userNames = await db.select({
  id: users.id,
  name: users.name,
}).from(users);
```

### Complex Queries

```typescript
// Joins
const postsWithAuthors = await db
  .select({
    post: posts,
    author: {
      id: users.id,
      name: users.name,
    },
  })
  .from(posts)
  .innerJoin(users, eq(posts.authorId, users.id))
  .where(eq(posts.published, true))
  .orderBy(desc(posts.createdAt));

// Aggregations
const postCounts = await db
  .select({
    authorId: posts.authorId,
    count: sql<number>`count(*)::int`,
  })
  .from(posts)
  .groupBy(posts.authorId);

// Subqueries
const usersWithPostCount = await db
  .select({
    user: users,
    postCount: sql<number>`(
      SELECT count(*) FROM ${posts}
      WHERE ${posts.authorId} = ${users.id}
    )::int`,
  })
  .from(users);
```

### Transactions

```typescript
const result = await db.transaction(async (tx) => {
  const [user] = await tx.insert(users).values({
    email: 'user@example.com',
    name: 'User',
    password: hashedPassword,
  }).returning();

  const [profile] = await tx.insert(profiles).values({
    userId: user.id,
    bio: 'New user',
  }).returning();

  return { user, profile };
});
```

## Drizzle Config

```typescript
// drizzle.config.ts
import type { Config } from 'drizzle-kit';

export default {
  schema: './src/db/schema.ts',
  out: './drizzle',
  driver: 'pg',
  dbCredentials: {
    connectionString: process.env.DATABASE_URL!,
  },
} satisfies Config;
```

## Migration Commands

```bash
# Generate migration
npx drizzle-kit generate:pg

# Apply migrations
npx drizzle-kit push:pg

# View migrations
npx drizzle-kit studio
```

### Migration Script

```typescript
// src/db/migrate.ts
import { migrate } from 'drizzle-orm/postgres-js/migrator';
import { drizzle } from 'drizzle-orm/postgres-js';
import postgres from 'postgres';

const connectionString = process.env.DATABASE_URL!;
const sql = postgres(connectionString, { max: 1 });
const db = drizzle(sql);

async function main(): Promise<void> {
  console.log('Running migrations...');
  await migrate(db, { migrationsFolder: './drizzle' });
  console.log('Migrations complete');
  await sql.end();
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
```

## Type Inference

```typescript
// Infer types from schema
import { InferSelectModel, InferInsertModel } from 'drizzle-orm';
import { users, posts } from './db/schema';

export type User = InferSelectModel<typeof users>;
export type NewUser = InferInsertModel<typeof users>;

export type Post = InferSelectModel<typeof posts>;
export type NewPost = InferInsertModel<typeof posts>;
```

## Package.json Scripts

```json
{
  "scripts": {
    "db:generate": "drizzle-kit generate:pg",
    "db:migrate": "tsx src/db/migrate.ts",
    "db:push": "drizzle-kit push:pg",
    "db:studio": "drizzle-kit studio"
  }
}
```

## Best Practices

1. **Use relations** - Define relations for type-safe joins
2. **Type inference** - Use InferSelectModel/InferInsertModel
3. **Prepared statements** - Use db.query for better performance
4. **Transactions** - Use for related operations
5. **Indexes** - Define indexes in schema

## Notes

- Drizzle is SQL-first - full control over queries
- Smaller bundle size than Prisma
- No code generation step required
- Excellent TypeScript inference
