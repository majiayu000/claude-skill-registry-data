---
name: create-model
description: Create Prisma model layer functions. Use when adding database operations. Never call Prisma directly in routes.
---

# Create Model

Creates model layer functions for database operations. All database access MUST go through the model layer.

## When to Use

- Adding any database operations
- Creating, reading, updating, or deleting data
- User asks to "add database functions" or "create model"

## Critical Rules

### 1. Never Call Prisma Directly in Routes

```typescript
// ❌ NEVER do this in routes
const user = await prisma.user.findUnique({ where: { id } });

// ✅ ALWAYS do this
import { getUserById } from '~/models/user.server';
const user = await getUserById(id);
```

### 2. Use Correct Import Paths

```typescript
// ✅ CORRECT
import { prisma } from '~/db.server';
import type { User, Role } from '~/generated/prisma/client';

// ❌ NEVER
import { PrismaClient } from '@prisma/client';
```

### 3. File Naming

```
app/models/[feature].server.ts
```

The `.server.ts` suffix ensures the code only runs on the server.

## Model Layer Template

**Location:** `app/models/[feature].server.ts`

```typescript
import { prisma } from '~/db.server';
import type { Item } from '~/generated/prisma/client';

// ============================================
// READ Operations
// ============================================

/**
 * Get a single item by ID
 */
export function getItem(id: string) {
    return prisma.item.findUnique({
        where: { id },
        select: {
            id: true,
            name: true,
            description: true,
            userId: true,
            createdAt: true,
            updatedAt: true,
        },
    });
}

/**
 * Get all items for a user
 */
export function getItemsByUser(userId: string) {
    return prisma.item.findMany({
        where: { userId },
        orderBy: { createdAt: 'desc' },
    });
}

/**
 * Get items with pagination
 */
export async function getItemsPaginated(
    userId: string,
    page: number = 1,
    pageSize: number = 10
) {
    const [items, total] = await Promise.all([
        prisma.item.findMany({
            where: { userId },
            skip: (page - 1) * pageSize,
            take: pageSize,
            orderBy: { createdAt: 'desc' },
        }),
        prisma.item.count({ where: { userId } }),
    ]);

    return {
        items,
        pagination: {
            page,
            pageSize,
            total,
            totalPages: Math.ceil(total / pageSize),
        },
    };
}

// ============================================
// CREATE Operations
// ============================================

/**
 * Create a new item
 */
export function createItem(
    userId: string,
    data: { name: string; description?: string }
) {
    return prisma.item.create({
        data: {
            ...data,
            userId,
        },
    });
}

// ============================================
// UPDATE Operations
// ============================================

/**
 * Update an existing item
 */
export function updateItem(
    id: string,
    data: Partial<{ name: string; description: string }>
) {
    return prisma.item.update({
        where: { id },
        data,
    });
}

// ============================================
// DELETE Operations
// ============================================

/**
 * Delete an item
 */
export function deleteItem(id: string) {
    return prisma.item.delete({
        where: { id },
    });
}

/**
 * Delete all items for a user
 */
export function deleteItemsByUser(userId: string) {
    return prisma.item.deleteMany({
        where: { userId },
    });
}
```

## Common Patterns

### Use `select` for Type Safety

```typescript
export function getUser(id: string) {
    return prisma.user.findUnique({
        where: { id },
        select: {
            id: true,
            email: true,
            name: true,
            // Exclude sensitive fields like password
        },
    });
}
```

### Include Related Data

```typescript
export function getPostWithComments(id: string) {
    return prisma.post.findUnique({
        where: { id },
        include: {
            author: true,
            comments: {
                include: { author: true },
                orderBy: { createdAt: 'desc' },
            },
        },
    });
}
```

### Transactions

```typescript
export async function transferCredits(fromId: string, toId: string, amount: number) {
    return prisma.$transaction(async (tx) => {
        await tx.user.update({
            where: { id: fromId },
            data: { credits: { decrement: amount } },
        });

        await tx.user.update({
            where: { id: toId },
            data: { credits: { increment: amount } },
        });
    });
}
```

### Upsert

```typescript
export function upsertSettings(userId: string, data: SettingsData) {
    return prisma.settings.upsert({
        where: { userId },
        update: data,
        create: { ...data, userId },
    });
}
```

## After Schema Changes

1. Run `npx prisma migrate dev --name description`
2. Run `npx prisma generate`
3. Restart dev server

## Anti-Patterns

- ❌ Calling Prisma directly in routes
- ❌ Importing from `@prisma/client`
- ❌ Creating new PrismaClient instances
- ❌ N+1 queries (fetching in loops)
- ❌ Exposing sensitive data
- ❌ Missing `.server.ts` suffix

## Templates

- [Model Template](./templates/model.server.ts)

## Full Reference

See `.github/instructions/prisma.instructions.md` for comprehensive documentation.
