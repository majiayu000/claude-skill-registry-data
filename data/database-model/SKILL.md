---
name: database-model
description: Create Prisma schema models with relations and indexes. Use when designing database schemas, adding models, or defining entity relationships.
---

## ⚠️ CRITICAL - DO NOT MODIFY

```prisma
// prisma/schema.prisma - NEVER change these blocks
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}
```

Import: `import { prisma } from '@/lib/prisma'` (already exists)

## Model Conventions

```prisma
model Product {
  id        String   @id @default(uuid())
  name      String
  price     Float    // Use Float for UI (returns number directly)
  isActive  Boolean  @default(true)
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  category   Category @relation(fields: [categoryId], references: [id], onDelete: Cascade)
  categoryId String

  @@index([categoryId])
  @@index([name])
}
```

**Rules:**
- Model names: PascalCase
- Field names: camelCase
- IDs: `@id @default(uuid())`
- Always: `createdAt`, `updatedAt`
- Always: `@@index` on foreign keys

## Number Types

| Type | Returns | Use Case |
|------|---------|----------|
| `Int` | number | Counts, whole numbers |
| `Float` | number | Prices (recommended) |
| `Decimal` | Prisma.Decimal | Financial (needs conversion) |

## Relations

### One-to-Many
```prisma
model Category {
  id       String    @id @default(uuid())
  name     String    @unique
  products Product[]
}

model Product {
  id         String   @id @default(uuid())
  category   Category @relation(fields: [categoryId], references: [id], onDelete: Cascade)
  categoryId String
  @@index([categoryId])
}
```

### One-to-One
```prisma
model User {
  id      String   @id @default(uuid())
  profile Profile?
}

model Profile {
  id     String @id @default(uuid())
  user   User   @relation(fields: [userId], references: [id], onDelete: Cascade)
  userId String @unique  // @unique = one-to-one
}
```

### Many-to-Many
```prisma
model Post {
  id   String @id @default(uuid())
  tags Tag[]  // Prisma handles junction table
}

model Tag {
  id    String @id @default(uuid())
  name  String @unique
  posts Post[]
}
```

## NextAuth Models

User, Account, Session already exist in boilerplate. Just add relations:
```prisma
model User {
  // ... existing fields
  posts Post[]  // Add your relations
}
```

## After Schema Changes

DO NOT run db push manually. Runs automatically in validation phase.

## NEVER
- Modify datasource/generator blocks
- Recreate lib/prisma.ts
- Recreate User/Account/Session
- Forget @@index on foreign keys
- Skip onDelete: Cascade on children
- Run db push during implementation
