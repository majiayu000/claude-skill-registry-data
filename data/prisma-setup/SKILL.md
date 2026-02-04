---
name: prisma-setup
description: Prisma ORM configuration and patterns. Use when setting up database access with Prisma.
---

# Prisma Setup Skill

This skill covers Prisma ORM setup and patterns for Node.js applications.

## When to Use

Use this skill when:
- Setting up database access
- Defining data models
- Managing migrations
- Optimizing database queries

## Core Principle

**TYPE-SAFE DATABASE ACCESS** - Prisma generates TypeScript types from your schema. Use them everywhere.

## Installation

```bash
npm install @prisma/client
npm install -D prisma
npx prisma init
```

## Schema Definition

```prisma
// prisma/schema.prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model User {
  id        String   @id @default(cuid())
  email     String   @unique
  name      String
  password  String
  role      Role     @default(USER)
  posts     Post[]
  profile   Profile?
  sessions  Session[]
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  @@index([email])
  @@index([role])
}

model Profile {
  id     String  @id @default(cuid())
  bio    String? @db.Text
  avatar String?
  userId String  @unique
  user   User    @relation(fields: [userId], references: [id], onDelete: Cascade)
}

model Post {
  id        String     @id @default(cuid())
  title     String
  slug      String     @unique
  content   String?    @db.Text
  published Boolean    @default(false)
  authorId  String
  author    User       @relation(fields: [authorId], references: [id], onDelete: Cascade)
  tags      Tag[]
  comments  Comment[]
  createdAt DateTime   @default(now())
  updatedAt DateTime   @updatedAt

  @@index([authorId])
  @@index([slug])
  @@index([published, createdAt])
}

model Tag {
  id    String @id @default(cuid())
  name  String @unique
  posts Post[]
}

model Comment {
  id        String   @id @default(cuid())
  content   String   @db.Text
  postId    String
  post      Post     @relation(fields: [postId], references: [id], onDelete: Cascade)
  authorId  String
  createdAt DateTime @default(now())

  @@index([postId])
}

model Session {
  id        String   @id @default(cuid())
  token     String   @unique
  userId    String
  user      User     @relation(fields: [userId], references: [id], onDelete: Cascade)
  expiresAt DateTime
  createdAt DateTime @default(now())

  @@index([userId])
  @@index([expiresAt])
}

enum Role {
  USER
  MODERATOR
  ADMIN
}
```

## Client Setup

```typescript
// src/db/client.ts
import { PrismaClient } from '@prisma/client';

declare global {
  // eslint-disable-next-line no-var
  var prisma: PrismaClient | undefined;
}

export const prisma = globalThis.prisma ?? new PrismaClient({
  log: process.env.NODE_ENV === 'development'
    ? ['query', 'info', 'warn', 'error']
    : ['error'],
});

if (process.env.NODE_ENV !== 'production') {
  globalThis.prisma = prisma;
}
```

### Fastify Plugin

```typescript
// src/plugins/database.ts
import { FastifyPluginAsync } from 'fastify';
import fp from 'fastify-plugin';
import { PrismaClient } from '@prisma/client';

declare module 'fastify' {
  interface FastifyInstance {
    db: PrismaClient;
  }
}

const databasePlugin: FastifyPluginAsync = async (fastify) => {
  const prisma = new PrismaClient({
    log: [
      { emit: 'event', level: 'query' },
      { emit: 'event', level: 'error' },
    ],
  });

  prisma.$on('query', (e) => {
    fastify.log.debug({ query: e.query, duration: e.duration }, 'database query');
  });

  await prisma.$connect();
  fastify.decorate('db', prisma);

  fastify.addHook('onClose', async () => {
    await prisma.$disconnect();
  });
};

export default fp(databasePlugin, { name: 'database' });
```

## Query Patterns

### Basic CRUD

```typescript
// Create
const user = await prisma.user.create({
  data: {
    email: 'user@example.com',
    name: 'User',
    password: hashedPassword,
  },
});

// Read
const user = await prisma.user.findUnique({
  where: { id: userId },
});

const users = await prisma.user.findMany({
  where: { role: 'USER' },
  orderBy: { createdAt: 'desc' },
  take: 10,
});

// Update
const updated = await prisma.user.update({
  where: { id: userId },
  data: { name: 'New Name' },
});

// Delete
await prisma.user.delete({
  where: { id: userId },
});
```

### Relations

```typescript
// Create with relations
const post = await prisma.post.create({
  data: {
    title: 'My Post',
    slug: 'my-post',
    content: 'Content here',
    author: {
      connect: { id: userId },
    },
    tags: {
      connectOrCreate: [
        {
          where: { name: 'typescript' },
          create: { name: 'typescript' },
        },
      ],
    },
  },
});

// Include relations
const postWithAuthor = await prisma.post.findUnique({
  where: { id: postId },
  include: {
    author: {
      select: { id: true, name: true, email: true },
    },
    tags: true,
    _count: {
      select: { comments: true },
    },
  },
});
```

### Pagination

```typescript
interface PaginationParams {
  page: number;
  perPage: number;
}

interface PaginatedResult<T> {
  data: T[];
  meta: {
    total: number;
    page: number;
    perPage: number;
    totalPages: number;
  };
}

async function paginateUsers(
  params: PaginationParams
): Promise<PaginatedResult<User>> {
  const { page, perPage } = params;
  const skip = (page - 1) * perPage;

  const [users, total] = await prisma.$transaction([
    prisma.user.findMany({
      skip,
      take: perPage,
      orderBy: { createdAt: 'desc' },
    }),
    prisma.user.count(),
  ]);

  return {
    data: users,
    meta: {
      total,
      page,
      perPage,
      totalPages: Math.ceil(total / perPage),
    },
  };
}
```

### Transactions

```typescript
// Sequential transaction
const [user, post] = await prisma.$transaction([
  prisma.user.create({ data: userData }),
  prisma.post.create({ data: postData }),
]);

// Interactive transaction
const result = await prisma.$transaction(async (tx) => {
  const user = await tx.user.findUnique({
    where: { id: userId },
  });

  if (!user) {
    throw new Error('User not found');
  }

  const post = await tx.post.create({
    data: {
      title: 'New Post',
      slug: 'new-post',
      authorId: user.id,
    },
  });

  return { user, post };
});
```

## Migration Commands

```bash
# Create migration
npx prisma migrate dev --name add_users

# Apply migrations (production)
npx prisma migrate deploy

# Reset database (development only)
npx prisma migrate reset

# Generate client
npx prisma generate

# Push schema (no migration)
npx prisma db push

# View database
npx prisma studio
```

## Seed Script

```typescript
// prisma/seed.ts
import { PrismaClient } from '@prisma/client';
import bcrypt from 'bcrypt';

const prisma = new PrismaClient();

async function main(): Promise<void> {
  console.log('Seeding database...');

  // Clear existing data
  await prisma.comment.deleteMany();
  await prisma.post.deleteMany();
  await prisma.session.deleteMany();
  await prisma.profile.deleteMany();
  await prisma.user.deleteMany();
  await prisma.tag.deleteMany();

  // Create admin user
  const adminPassword = await bcrypt.hash('admin123', 12);
  const admin = await prisma.user.create({
    data: {
      email: 'admin@example.com',
      name: 'Admin User',
      password: adminPassword,
      role: 'ADMIN',
      profile: {
        create: {
          bio: 'System administrator',
        },
      },
    },
  });

  // Create tags
  const tags = await Promise.all([
    prisma.tag.create({ data: { name: 'typescript' } }),
    prisma.tag.create({ data: { name: 'nodejs' } }),
    prisma.tag.create({ data: { name: 'prisma' } }),
  ]);

  // Create posts
  await prisma.post.create({
    data: {
      title: 'Getting Started with Prisma',
      slug: 'getting-started-with-prisma',
      content: 'Prisma is a modern database toolkit...',
      published: true,
      authorId: admin.id,
      tags: {
        connect: tags.map((t) => ({ id: t.id })),
      },
    },
  });

  console.log('Database seeded successfully');
}

main()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
```

## Package.json Config

```json
{
  "prisma": {
    "seed": "tsx prisma/seed.ts"
  }
}
```

## Best Practices

1. **Use transactions** - For related operations
2. **Index foreign keys** - Always add @@index
3. **Select only needed fields** - Use select for performance
4. **Avoid N+1** - Use include for relations
5. **Soft deletes** - Add deletedAt for audit trails
6. **Connection pooling** - Use pgbouncer in production

## Notes

- Run `prisma generate` after schema changes
- Use `prisma studio` for database exploration
- Migrations are production-safe
- Use environment variables for database URL
