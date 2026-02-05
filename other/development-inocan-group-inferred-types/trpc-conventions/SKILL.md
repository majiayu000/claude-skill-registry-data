---
name: trpc-conventions
description: tRPC router patterns for Otaku Odyssey. Use when creating or modifying tRPC routers, procedures, or API endpoints.
allowed-tools: Read, Write, Edit, Bash
---

# tRPC Conventions for Otaku Odyssey

## Router Structure

Every router follows this structure:

```typescript
import { createTRPCRouter, protectedProcedure, publicProcedure } from "../trpc";
import { z } from "zod";
import { eq, and, desc } from "drizzle-orm";
import { features } from "@/db/schema";
import { createFeatureSchema, updateFeatureSchema } from "@/lib/validations/feature";
import { TRPCError } from "@trpc/server";

export const featureRouter = createTRPCRouter({
  // LIST - with pagination
  list: protectedProcedure
    .input(z.object({
      page: z.number().min(1).default(1),
      limit: z.number().min(1).max(100).default(20),
      conventionId: z.string().optional(),
    }))
    .query(async ({ ctx, input }) => {
      const { page, limit, conventionId } = input;
      const offset = (page - 1) * limit;

      const where = conventionId 
        ? eq(features.conventionId, conventionId)
        : undefined;

      const [items, countResult] = await Promise.all([
        ctx.db.query.features.findMany({
          where,
          limit,
          offset,
          orderBy: desc(features.createdAt),
          with: {
            convention: true, // Include relations as needed
          },
        }),
        ctx.db.select({ count: sql<number>`count(*)` })
          .from(features)
          .where(where),
      ]);

      return {
        items,
        pagination: {
          page,
          limit,
          total: countResult[0]?.count ?? 0,
          totalPages: Math.ceil((countResult[0]?.count ?? 0) / limit),
        },
      };
    }),

  // GET BY ID
  getById: protectedProcedure
    .input(z.object({ id: z.string() }))
    .query(async ({ ctx, input }) => {
      const item = await ctx.db.query.features.findFirst({
        where: eq(features.id, input.id),
        with: {
          convention: true,
        },
      });

      if (!item) {
        throw new TRPCError({
          code: "NOT_FOUND",
          message: "Feature not found",
        });
      }

      return item;
    }),

  // CREATE
  create: protectedProcedure
    .input(createFeatureSchema)
    .mutation(async ({ ctx, input }) => {
      const [created] = await ctx.db
        .insert(features)
        .values({
          ...input,
          createdBy: ctx.session.user.id,
        })
        .returning();

      return created;
    }),

  // UPDATE
  update: protectedProcedure
    .input(z.object({
      id: z.string(),
      data: updateFeatureSchema,
    }))
    .mutation(async ({ ctx, input }) => {
      const existing = await ctx.db.query.features.findFirst({
        where: eq(features.id, input.id),
      });

      if (!existing) {
        throw new TRPCError({
          code: "NOT_FOUND",
          message: "Feature not found",
        });
      }

      const [updated] = await ctx.db
        .update(features)
        .set({
          ...input.data,
          updatedAt: new Date(),
        })
        .where(eq(features.id, input.id))
        .returning();

      return updated;
    }),

  // DELETE
  delete: protectedProcedure
    .input(z.object({ id: z.string() }))
    .mutation(async ({ ctx, input }) => {
      const existing = await ctx.db.query.features.findFirst({
        where: eq(features.id, input.id),
      });

      if (!existing) {
        throw new TRPCError({
          code: "NOT_FOUND",
          message: "Feature not found",
        });
      }

      await ctx.db.delete(features).where(eq(features.id, input.id));

      return { success: true };
    }),
});
```

## Exporting from Root Router

Always add new routers to `src/server/api/root.ts`:

```typescript
import { featureRouter } from "./routers/feature";

export const appRouter = createTRPCRouter({
  // ... existing routers
  feature: featureRouter,
});
```

## Error Handling

Use TRPCError with appropriate codes:

```typescript
import { TRPCError } from "@trpc/server";

// Not found
throw new TRPCError({ code: "NOT_FOUND", message: "Item not found" });

// Unauthorized
throw new TRPCError({ code: "UNAUTHORIZED", message: "Must be logged in" });

// Forbidden (authed but no permission)
throw new TRPCError({ code: "FORBIDDEN", message: "No permission" });

// Bad input
throw new TRPCError({ code: "BAD_REQUEST", message: "Invalid input" });

// Conflict (duplicate)
throw new TRPCError({ code: "CONFLICT", message: "Already exists" });
```

## Procedure Types

- `publicProcedure` - No auth required
- `protectedProcedure` - Requires authenticated session
- Custom procedures for role-based access (when RBAC is implemented)

## Client Usage Pattern

```typescript
// In React components
import { api } from "@/trpc/react";

function FeatureList() {
  const { data, isLoading } = api.feature.list.useQuery({
    page: 1,
    limit: 20,
  });

  const createMutation = api.feature.create.useMutation({
    onSuccess: () => {
      // Invalidate and refetch
      utils.feature.list.invalidate();
    },
  });
}
```

## Checklist for New Routers

- [ ] Import from "../trpc"
- [ ] Use Zod for all inputs
- [ ] Include pagination for list queries
- [ ] Handle NOT_FOUND for single-item queries
- [ ] Use protectedProcedure for mutations
- [ ] Return created/updated entity from mutations
- [ ] Export from root.ts
- [ ] Add corresponding validation schemas
