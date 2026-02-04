---
name: backend-trpc
description: Type-safe API layer for TypeScript full-stack applications. Use when building APIs that need end-to-end type safety between client and server WITHOUT code generation. Ideal for Next.js, React, and Express apps where both frontend and backend are TypeScript. Choose tRPC over REST/GraphQL when you control both ends and want zero runtime overhead for type checking.
allowed-tools: Read, Edit, Write, Bash (*)
---

# tRPC (Type-Safe API Layer)

## Overview

tRPC enables end-to-end typesafe APIs by sharing TypeScript types between client and server. No code generation, no schema files—just TypeScript.

**Version**: v11.7+ (2024-2025)  
**Requirements**: TypeScript ≥5.7.2 with strict mode

**Key Benefit**: Change a procedure's input/output → TypeScript errors appear immediately on client.

## When to Use This Skill

✅ **Use tRPC when:**
- Building full-stack TypeScript apps (Next.js, React + Express)
- You control both client and server code
- Need type-safe API without GraphQL complexity
- Want automatic request batching and caching
- Building internal APIs, dashboards, admin panels

❌ **Don't use tRPC when:**
- External clients need REST/OpenAPI (use tRPC + OpenAPI adapter)
- Non-TypeScript clients (mobile apps, third-party integrations)
- Microservices with different languages

---

## Quick Start

### Installation

```bash
npm install @trpc/server @trpc/client zod

# For React/Next.js:
npm install @trpc/react-query @tanstack/react-query@^5
```

### Core Setup

**Always create tRPC instance in a dedicated file:**

```typescript
// src/server/trpc.ts
import { initTRPC, TRPCError } from '@trpc/server';
import { z } from 'zod';

interface Context {
  user?: { id: string; role: string };
  db: PrismaClient;
}

const t = initTRPC.context<Context>().create({
  errorFormatter({ shape, error }) {
    return {
      ...shape,
      data: {
        ...shape.data,
        zodError: error.cause instanceof z.ZodError 
          ? error.cause.flatten() 
          : null,
      },
    };
  },
});

export const router = t.router;
export const publicProcedure = t.procedure;
export const middleware = t.middleware;
export const createCallerFactory = t.createCallerFactory;
```

---

## Procedure Patterns

### Query vs Mutation

```typescript
// src/server/routers/user.ts
import { z } from 'zod';
import { router, publicProcedure, protectedProcedure } from '../trpc';
import { TRPCError } from '@trpc/server';

export const userRouter = router({
  // Query - GET semantics (reads)
  getById: publicProcedure
    .input(z.object({ id: z.string().uuid() }))
    .query(async ({ input, ctx }) => {
      const user = await ctx.db.user.findUnique({ where: { id: input.id } });
      if (!user) throw new TRPCError({ code: 'NOT_FOUND' });
      return user;
    }),

  // Mutation - POST/PUT/DELETE semantics (writes)
  create: protectedProcedure
    .input(z.object({
      name: z.string().min(2).max(100),
      email: z.string().email(),
    }))
    .mutation(async ({ input, ctx }) => {
      return ctx.db.user.create({ data: input });
    }),
});
```

### Cursor-Based Pagination

```typescript
list: publicProcedure
  .input(z.object({
    limit: z.number().min(1).max(100).default(10),
    cursor: z.string().uuid().optional(),
  }))
  .query(async ({ input, ctx }) => {
    const items = await ctx.db.user.findMany({
      take: input.limit + 1,
      cursor: input.cursor ? { id: input.cursor } : undefined,
      orderBy: { createdAt: 'desc' },
    });
    
    let nextCursor: string | undefined;
    if (items.length > input.limit) {
      nextCursor = items.pop()?.id;
    }
    return { items, nextCursor };
  }),
```

---

## Middleware Patterns

### Authentication Middleware

```typescript
const isAuthed = middleware(async ({ ctx, next }) => {
  if (!ctx.user) {
    throw new TRPCError({ code: 'UNAUTHORIZED' });
  }
  return next({ ctx: { user: ctx.user } });
});

export const protectedProcedure = publicProcedure.use(isAuthed);
```

### Role-Based Authorization

```typescript
const hasRole = (role: string) => middleware(async ({ ctx, next }) => {
  if (ctx.user?.role !== role) {
    throw new TRPCError({ code: 'FORBIDDEN' });
  }
  return next();
});

export const adminProcedure = protectedProcedure.use(hasRole('admin'));
```

### Logging Middleware

```typescript
const loggerMiddleware = middleware(async ({ path, type, next }) => {
  const start = Date.now();
  const result = await next();
  console.log(`[${type}] ${path} - ${Date.now() - start}ms`);
  return result;
});
```

---

## Context Creation

### Express Adapter

```typescript
// src/server/context.ts
import { CreateExpressContextOptions } from '@trpc/server/adapters/express';
import { prisma } from '../lib/prisma';

export async function createContext({ req }: CreateExpressContextOptions) {
  const token = req.headers.authorization?.split(' ')[1];
  const user = token ? await verifyToken(token) : null;
  
  return { user, db: prisma };
}

export type Context = Awaited<ReturnType<typeof createContext>>;
```

### Express Server Setup

```typescript
// src/server/index.ts
import express from 'express';
import cors from 'cors';
import { createExpressMiddleware } from '@trpc/server/adapters/express';
import { appRouter } from './routers/_app';
import { createContext } from './context';

const app = express();
app.use(cors());
app.use('/trpc', createExpressMiddleware({
  router: appRouter,
  createContext,
}));

app.listen(3000);
```

---

## Router Merging

```typescript
// src/server/routers/_app.ts
import { router } from '../trpc';
import { userRouter } from './user';
import { postRouter } from './post';

export const appRouter = router({
  user: userRouter,
  post: postRouter,
});

export type AppRouter = typeof appRouter;
```

---

## Rules

### Do ✅

- Use Zod for all input validation
- Create separate routers per domain and merge them
- Use `TRPCError` with appropriate codes
- Enable strict mode in TypeScript
- Use `httpBatchLink` on client for request batching
- Export `AppRouter` type for client

### Avoid ❌

- Mixing v10 and v11 patterns (breaking changes)
- Skipping input validation
- Throwing non-TRPCError exceptions (wrap them)
- Creating multiple tRPC instances
- Using `any` for context types

---

## Error Codes Reference

| Code | HTTP | Use Case |
|------|------|----------|
| `BAD_REQUEST` | 400 | Invalid input |
| `UNAUTHORIZED` | 401 | No/invalid auth |
| `FORBIDDEN` | 403 | No permission |
| `NOT_FOUND` | 404 | Resource missing |
| `CONFLICT` | 409 | Already exists |
| `INTERNAL_SERVER_ERROR` | 500 | Unexpected error |

---

## Troubleshooting

```yaml
"Types not updating on client":
  → Run TypeScript server in watch mode
  → Check AppRouter is exported and imported correctly
  → Verify tsconfig paths match

"Input validation errors not showing":
  → Add zodError to errorFormatter
  → Use .safeParse() on client for detailed errors

"CORS errors":
  → Configure cors() before tRPC middleware
  → Check origin whitelist

"Procedures not batching":
  → Ensure using httpBatchLink on client
  → Check all requests go to same endpoint
```

---

## File Structure

```
src/server/
├── trpc.ts              # tRPC instance, base procedures
├── context.ts           # Context creation
└── routers/
    ├── _app.ts          # Root router (merges all)
    ├── user.ts          # User procedures
    └── post.ts          # Post procedures
```

## References

- https://trpc.io/docs — Official documentation
- https://trpc.io/docs/client/react — React Query integration
- https://trpc.io/docs/server/adapters — Server adapters
