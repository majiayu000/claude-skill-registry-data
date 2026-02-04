---
name: standards-backend
description: Backend standards for modern TypeScript applications covering Convex, Supabase, Drizzle ORM, Stripe, tRPC, and API design patterns. Load when implementing server-side code, database schemas, or API endpoints.
---

# Backend Standards

Comprehensive backend development standards for modern TypeScript applications.

## When to Use

- Setting up a new backend or database
- Implementing API endpoints
- Adding authentication or payments
- Choosing between database technologies
- Implementing real-time features

## Resources

| Resource | Use When |
|----------|----------|
| [convex.md](resources/convex.md) | Real-time apps, automatic sync |
| [supabase.md](resources/supabase.md) | PostgreSQL + Auth + Storage + RLS |
| [drizzle.md](resources/drizzle.md) | Type-safe ORM, serverless/edge |
| [stripe.md](resources/stripe.md) | Payments, subscriptions, webhooks |
| [trpc.md](resources/trpc.md) | End-to-end type-safe APIs |
| [api-design.md](resources/api-design.md) | REST conventions, error handling |

## Database Selection Guide

| Use Case | Recommended Stack | Why |
|----------|------------------|-----|
| Real-time collaborative apps | **Convex** | Built-in subscriptions, automatic sync |
| Full-stack with auth + storage | **Supabase** | PostgreSQL + Auth + Storage + Realtime |
| Serverless/Edge functions | **Neon + Drizzle** | HTTP connections, no connection pooling |
| Traditional server apps | **Prisma** | Excellent DX, type safety, migrations |
| High-performance queries | **Neon + Drizzle** | Prepared statements, edge-optimized |

## Quick Reference

### Convex Schema

```typescript
import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export default defineSchema({
  users: defineTable({
    email: v.string(),
    name: v.string(),
  }).index("by_email", ["email"]),
});
```

### Drizzle Schema

```typescript
import { pgTable, uuid, varchar, timestamp } from "drizzle-orm/pg-core";

export const users = pgTable("users", {
  id: uuid("id").primaryKey().defaultRandom(),
  email: varchar("email", { length: 320 }).notNull().unique(),
  name: varchar("name", { length: 100 }).notNull(),
  createdAt: timestamp("created_at").defaultNow().notNull(),
});

export type User = typeof users.$inferSelect;
```

### Supabase RLS Policy

```sql
-- Users can only view their own data
CREATE POLICY "Users can view own data"
  ON users FOR SELECT
  USING (auth.uid() = id);
```

### Stripe Webhook Handler

```typescript
// app/api/webhooks/stripe/route.ts
export async function POST(req: Request) {
  const body = await req.text();
  const signature = headers().get("stripe-signature")!;
  
  const event = stripe.webhooks.constructEvent(
    body,
    signature,
    process.env.STRIPE_WEBHOOK_SECRET!
  );
  
  switch (event.type) {
    case "checkout.session.completed":
      // Handle checkout
      break;
    case "customer.subscription.updated":
      // Handle subscription change
      break;
  }
  
  return new Response(null, { status: 200 });
}
```

### tRPC Router

```typescript
import { router, protectedProcedure } from "./init";
import { z } from "zod";

export const postRouter = router({
  create: protectedProcedure
    .input(z.object({
      title: z.string().min(1),
      content: z.string(),
    }))
    .mutation(async ({ ctx, input }) => {
      return await ctx.db.insert(posts).values({
        ...input,
        authorId: ctx.userId,
      });
    }),
});
```

## Amp Tools to Use

- `finder` - Find existing backend patterns
- `Read` - Check API conventions
- `oracle` - Complex architecture decisions
- `mcp__exa__get_code_context_exa` - Research latest backend patterns

## Related Skills

- `standards-global` - TypeScript conventions
- `standards-frontend` - Client-side data fetching
- `standards-testing` - API testing patterns
