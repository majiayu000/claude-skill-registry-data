---
name: prisma
description: Prisma ORM patterns, schema design, migrations, relations, transactions, raw queries, and production optimization
layer: domain
category: database
triggers:
  - "prisma"
  - "prisma client"
  - "prisma schema"
  - "prisma migrate"
  - "prisma relations"
inputs:
  - "Data model requirements"
  - "Query patterns"
  - "Migration needs"
outputs:
  - "Prisma schema definitions"
  - "Type-safe query patterns"
  - "Migration strategies"
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
  - drizzle
  - supabase
riskLevel: low
memoryReadPolicy: selective
memoryWritePolicy: none
sideEffects: []
---

# Prisma Domain Skill

## Purpose

Provide expert-level guidance on Prisma ORM, including schema design, relations, migrations, transactions, advanced querying, performance optimization, and production deployment patterns.

## Key Patterns

### 1. Schema Design

```prisma
// schema.prisma
generator client {
  provider        = "prisma-client-js"
  previewFeatures = ["fullTextSearchPostgres", "relationJoins"]
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

// Base mixin pattern (use @@map for snake_case table names)
model User {
  id        String   @id @default(cuid())
  email     String   @unique
  name      String
  role      Role     @default(MEMBER)
  isActive  Boolean  @default(true) @map("is_active")

  // Relations
  posts     Post[]
  profile   Profile?
  sessions  Session[]

  // Audit fields
  createdAt DateTime @default(now()) @map("created_at")
  updatedAt DateTime @updatedAt @map("updated_at")
  deletedAt DateTime? @map("deleted_at")

  // Indexes
  @@index([email, isActive])
  @@index([role, createdAt(sort: Desc)])
  @@map("users")
}

enum Role {
  ADMIN
  MEMBER
  VIEWER
}

model Post {
  id          String   @id @default(cuid())
  title       String
  slug        String   @unique
  content     String
  published   Boolean  @default(false)
  publishedAt DateTime? @map("published_at")

  // Relations
  author      User     @relation(fields: [authorId], references: [id], onDelete: Cascade)
  authorId    String   @map("author_id")
  categories  CategoriesOnPosts[]
  tags        String[]

  createdAt   DateTime @default(now()) @map("created_at")
  updatedAt   DateTime @updatedAt @map("updated_at")

  // Compound index for common queries
  @@index([authorId, published, createdAt(sort: Desc)])
  @@index([published, publishedAt(sort: Desc)])
  @@map("posts")
}

model Category {
  id    String @id @default(cuid())
  name  String @unique
  slug  String @unique
  posts CategoriesOnPosts[]

  @@map("categories")
}

// Explicit many-to-many for extra fields
model CategoriesOnPosts {
  post       Post     @relation(fields: [postId], references: [id], onDelete: Cascade)
  postId     String   @map("post_id")
  category   Category @relation(fields: [categoryId], references: [id], onDelete: Cascade)
  categoryId String   @map("category_id")
  assignedAt DateTime @default(now()) @map("assigned_at")

  @@id([postId, categoryId])
  @@map("categories_on_posts")
}

model Profile {
  id     String  @id @default(cuid())
  bio    String?
  avatar String?
  user   User    @relation(fields: [userId], references: [id], onDelete: Cascade)
  userId String  @unique @map("user_id")

  @@map("profiles")
}
```

### 2. Client Initialization and Extensions

```typescript
import { PrismaClient, Prisma } from '@prisma/client';

// Singleton pattern
const globalForPrisma = globalThis as unknown as { prisma: PrismaClient };

export const prisma =
  globalForPrisma.prisma ??
  new PrismaClient({
    log: process.env.NODE_ENV === 'development'
      ? ['query', 'error', 'warn']
      : ['error'],
  });

if (process.env.NODE_ENV !== 'production') globalForPrisma.prisma = prisma;

// Soft delete extension
const prismaWithSoftDelete = prisma.$extends({
  query: {
    $allModels: {
      async findMany({ model, operation, args, query }) {
        args.where = { ...args.where, deletedAt: null };
        return query(args);
      },
      async findFirst({ model, operation, args, query }) {
        args.where = { ...args.where, deletedAt: null };
        return query(args);
      },
      async delete({ model, operation, args, query }) {
        // Convert delete to soft delete
        return prisma[model as string].update({
          where: args.where,
          data: { deletedAt: new Date() },
        });
      },
    },
  },
});

// Logging extension for slow queries
const prismaWithLogging = prisma.$extends({
  query: {
    $allModels: {
      async $allOperations({ operation, model, args, query }) {
        const start = performance.now();
        const result = await query(args);
        const duration = performance.now() - start;

        if (duration > 100) {
          console.warn(`Slow query: ${model}.${operation} took ${duration.toFixed(0)}ms`);
        }

        return result;
      },
    },
  },
});
```

### 3. Query Patterns

```typescript
// Avoid N+1: Use include/select
const usersWithPosts = await prisma.user.findMany({
  where: { isActive: true },
  include: {
    posts: {
      where: { published: true },
      orderBy: { createdAt: 'desc' },
      take: 5,
      select: {
        id: true,
        title: true,
        slug: true,
        createdAt: true,
      },
    },
    _count: {
      select: { posts: { where: { published: true } } },
    },
  },
  orderBy: { createdAt: 'desc' },
  take: 20,
});

// Cursor-based pagination (efficient for large datasets)
async function paginatePosts(cursor?: string, take: number = 20) {
  const posts = await prisma.post.findMany({
    where: { published: true },
    take: take + 1, // Fetch one extra to check hasMore
    ...(cursor && {
      cursor: { id: cursor },
      skip: 1, // Skip the cursor itself
    }),
    orderBy: { createdAt: 'desc' },
    select: {
      id: true,
      title: true,
      slug: true,
      author: { select: { name: true } },
      createdAt: true,
    },
  });

  const hasMore = posts.length > take;
  const items = hasMore ? posts.slice(0, take) : posts;

  return {
    items,
    nextCursor: hasMore ? items[items.length - 1].id : null,
    hasMore,
  };
}

// Complex filtering with type safety
function buildPostFilter(params: {
  search?: string;
  categoryId?: string;
  authorId?: string;
  publishedAfter?: Date;
}): Prisma.PostWhereInput {
  const where: Prisma.PostWhereInput = { published: true };

  if (params.search) {
    where.OR = [
      { title: { contains: params.search, mode: 'insensitive' } },
      { content: { contains: params.search, mode: 'insensitive' } },
    ];
  }

  if (params.categoryId) {
    where.categories = {
      some: { categoryId: params.categoryId },
    };
  }

  if (params.authorId) {
    where.authorId = params.authorId;
  }

  if (params.publishedAfter) {
    where.publishedAt = { gte: params.publishedAfter };
  }

  return where;
}

// Upsert
const user = await prisma.user.upsert({
  where: { email: 'jane@example.com' },
  update: { name: 'Jane Updated' },
  create: { email: 'jane@example.com', name: 'Jane Doe' },
});

// Aggregate queries
const stats = await prisma.post.aggregate({
  where: { published: true },
  _count: true,
  _avg: { viewCount: true },
  _max: { viewCount: true },
});

// Group by
const postsByMonth = await prisma.post.groupBy({
  by: ['authorId'],
  where: { published: true },
  _count: { id: true },
  _sum: { viewCount: true },
  orderBy: { _count: { id: 'desc' } },
  take: 10,
});
```

### 4. Transactions

```typescript
// Interactive transaction (recommended for complex operations)
async function transferCredits(fromId: string, toId: string, amount: number) {
  return prisma.$transaction(async (tx) => {
    const sender = await tx.user.findUnique({
      where: { id: fromId },
      select: { credits: true },
    });

    if (!sender || sender.credits < amount) {
      throw new Error('Insufficient credits');
    }

    await tx.user.update({
      where: { id: fromId },
      data: { credits: { decrement: amount } },
    });

    await tx.user.update({
      where: { id: toId },
      data: { credits: { increment: amount } },
    });

    return tx.transaction.create({
      data: {
        fromUserId: fromId,
        toUserId: toId,
        amount,
        type: 'TRANSFER',
      },
    });
  }, {
    maxWait: 5000,    // Max time to wait for transaction slot
    timeout: 10000,   // Max transaction execution time
    isolationLevel: Prisma.TransactionIsolationLevel.Serializable,
  });
}

// Batch transaction (atomic batch of operations)
const [updatedUser, newPost] = await prisma.$transaction([
  prisma.user.update({ where: { id: userId }, data: { postCount: { increment: 1 } } }),
  prisma.post.create({ data: { title: 'New Post', authorId: userId } }),
]);
```

### 5. Raw Queries (Escape Hatch)

```typescript
// Type-safe raw queries
const result = await prisma.$queryRaw<Array<{ id: string; rank: number }>>`
  SELECT id, RANK() OVER (ORDER BY view_count DESC) as rank
  FROM posts
  WHERE published = true
  AND created_at > ${thirtyDaysAgo}
  LIMIT ${limit}
`;

// For complex queries not supported by Prisma Client
const searchResults = await prisma.$queryRaw`
  SELECT p.id, p.title, p.slug,
    ts_rank(to_tsvector('english', p.title || ' ' || p.content), query) AS rank
  FROM posts p, to_tsquery('english', ${searchQuery}) query
  WHERE p.published = true
    AND to_tsvector('english', p.title || ' ' || p.content) @@ query
  ORDER BY rank DESC
  LIMIT 20
`;
```

## Best Practices

1. **Use `select` over `include`** when you don't need all fields -- reduces data transfer
2. **Use cursor-based pagination** for production -- offset pagination degrades on large tables
3. **Add `@@index` for every `where` + `orderBy` combination** you frequently query
4. **Use interactive transactions** (`$transaction(async (tx) => {})`) for complex business logic
5. **Set `maxWait` and `timeout`** on transactions to prevent deadlocks
6. **Use Prisma extensions** for cross-cutting concerns (soft delete, logging, audit)
7. **Map to snake_case** with `@@map` and `@map` for database-conventional naming
8. **Use `cuid()` or `uuid()`** for primary keys, not auto-increment integers
9. **Run `prisma migrate deploy`** in CI/CD, not `prisma migrate dev`
10. **Monitor query performance** with the logging extension pattern

## Common Pitfalls

| Pitfall | Impact | Fix |
|---------|--------|-----|
| N+1 queries from missing `include` | Excessive DB round trips | Use `include` or `select` with nested relations |
| Using `findMany` without `take` | Loading entire tables | Always paginate with `take` + cursor/offset |
| Not adding indexes for query patterns | Full table scans | `@@index` on every filtered/sorted field combination |
| `prisma migrate dev` in production | Data loss risk | Use `prisma migrate deploy` in production |
| Not handling `PrismaClientKnownRequestError` | Untyped error responses | Check `error.code` (P2002 = unique, P2025 = not found) |
| Singleton not used (Next.js hot reload) | Connection exhaustion | Use the global singleton pattern |
| Missing `onDelete` on relations | Orphaned records or FK errors | Set `Cascade`, `SetNull`, or `Restrict` explicitly |
