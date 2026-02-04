---
name: add-trpc-endpoint
description: Scaffold new tRPC API endpoints for the dealflow-network project with proper Zod validation, middleware, database functions, and client hooks. Use when adding new API routes, creating CRUD operations, or extending existing routers.
---

# Add tRPC Endpoint

Scaffold complete tRPC endpoints following project patterns.

## Quick Start

When adding a new endpoint, I will:
1. Add Zod input schema to `server/routers.ts`
2. Create database function in `server/db.ts` (if needed)
3. Add procedure with appropriate middleware
4. Show client usage pattern

## Procedure Types

Choose based on auth requirements:

```typescript
// No authentication required
publicProcedure

// Requires logged-in user (ctx.user available)
protectedProcedure

// Requires admin role (ctx.user.role === 'admin')
adminProcedure
```

## Template: Query Endpoint

```typescript
// In server/routers.ts - add to appropriate router

const getItem = protectedProcedure
  .input(z.object({
    id: z.number(),
  }))
  .query(async ({ ctx, input }) => {
    const db = await getDb();
    if (!db) throw new TRPCError({ code: "INTERNAL_SERVER_ERROR" });

    const [item] = await db
      .select()
      .from(items)
      .where(eq(items.id, input.id));

    if (!item) {
      throw new TRPCError({ code: "NOT_FOUND", message: "Item not found" });
    }

    return item;
  });
```

## Template: Mutation Endpoint

```typescript
const createItem = protectedProcedure
  .input(z.object({
    name: z.string().min(1, "Name is required"),
    description: z.string().optional(),
    categoryId: z.number().optional(),
  }))
  .mutation(async ({ ctx, input }) => {
    const db = await getDb();
    if (!db) throw new TRPCError({ code: "INTERNAL_SERVER_ERROR" });

    const [result] = await db.insert(items).values({
      ...input,
      createdBy: ctx.user.id,
      createdAt: new Date(),
    });

    return { id: result.insertId, ...input };
  });
```

## Template: List with Pagination

```typescript
const listItems = protectedProcedure
  .input(z.object({
    page: z.number().default(1),
    limit: z.number().default(20),
    search: z.string().optional(),
  }))
  .query(async ({ ctx, input }) => {
    const db = await getDb();
    if (!db) throw new TRPCError({ code: "INTERNAL_SERVER_ERROR" });

    const offset = (input.page - 1) * input.limit;

    let query = db.select().from(items);

    if (input.search) {
      query = query.where(like(items.name, `%${input.search}%`));
    }

    const results = await query.limit(input.limit).offset(offset);

    return results;
  });
```

## Adding to Router

```typescript
// In server/routers.ts
export const appRouter = router({
  // ... existing routers
  items: router({
    list: listItems,
    get: getItem,
    create: createItem,
    update: updateItem,
    delete: deleteItem,
  }),
});
```

## Client Usage

```typescript
// Query hook
const { data, isLoading, error } = trpc.items.list.useQuery({ page: 1 });

// Mutation hook
const createMutation = trpc.items.create.useMutation({
  onSuccess: () => {
    // Invalidate cache to refetch list
    utils.items.list.invalidate();
    toast.success("Item created");
  },
  onError: (error) => {
    toast.error(`Failed: ${error.message}`);
  },
});

// Call mutation
createMutation.mutate({ name: "New Item" });
```

## Common Zod Patterns

```typescript
// Required string with min length
name: z.string().min(1, "Required")

// Optional email
email: z.string().email().optional().or(z.literal(""))

// URL validation
linkedinUrl: z.string().url().optional().or(z.literal(""))

// Enum
status: z.enum(["pending", "active", "completed"])

// Array of IDs
tagIds: z.array(z.number())

// Nested object
metadata: z.object({
  source: z.string(),
  confidence: z.number(),
}).optional()
```

## Error Handling

```typescript
import { TRPCError } from "@trpc/server";

// Common error codes
throw new TRPCError({ code: "NOT_FOUND", message: "Item not found" });
throw new TRPCError({ code: "UNAUTHORIZED" });
throw new TRPCError({ code: "FORBIDDEN", message: "Admin only" });
throw new TRPCError({ code: "BAD_REQUEST", message: "Invalid input" });
throw new TRPCError({ code: "INTERNAL_SERVER_ERROR" });
```

## Checklist

- [ ] Input validation with Zod schema
- [ ] Appropriate procedure type (public/protected/admin)
- [ ] Database null check
- [ ] Error handling with TRPCError
- [ ] Add to router export
- [ ] Client cache invalidation strategy
