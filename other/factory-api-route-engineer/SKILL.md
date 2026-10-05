---
name: factory-api-route-engineer
description: Use when designing or implementing API endpoints — server actions, tRPC procedures, REST routes for external consumers. Carries the factory's API conventions — the server actions vs tRPC decision, procedure tier stacking, per-mutation Zod schemas, central router composition with manual registration, pagination (limit/offset/orderBy default; cursor only when needed), multi-field search via `ilike` + `or()`, aggregated stats in list queries, mutation lifecycle hooks, stale-time defaults, custom error class taxonomy, fetch adapter for tRPC in App Router. Outputs endpoints that fit the house style — not bespoke per-route handlers.
---

Apply the **api-route-engineer** specialist workflow. Build endpoints grounded in the factory's API conventions, not bespoke per-route handlers. Load the canonical `factory-api` and `factory-auth` skills through the host's skill capability when needed.

## How to think (in order)

1. **API style?** Apply the decision matrix from `factory-api.md`:
   - **Server actions** — default. One frontend consumer. Feature-folder colocation matters.
   - **tRPC** — ≥3 entities with cross-feature queries. Multiple consumers. Typed RPC.
   - **REST / OpenAPI** — only for external system callers.

   If the project already commits to one, use it. Don't mix.

2. **What's the surface?**
   - **Mutation** — create, update, delete, custom action
   - **Query** — list (paginated), detail (by ID), search, aggregation
   - **Webhook** — external system → your service

3. **Auth tier?**
   - **publicProcedure** — only for genuinely public endpoints (signup, public docs)
   - **protectedProcedure** — authed user, no org context
   - **orgProcedure** — authed user + org context (default for app endpoints)

4. **Input shape?** Per-endpoint Zod schema. For paginated lists:
   - `limit: number().int().min(1).max(100).default(50)`
   - `offset: number().int().min(0).default(0)`
   - `orderBy: enum([...]).default('createdAt')`
   - `orderDir: enum(['asc','desc']).default('desc')`
   - Plus per-feature filter object

5. **Output shape?** Three options:
   - **List**: `{ items: T[], total?: number }` — include `total` if pagination needs it
   - **Detail**: `T | null` — return null on not-found, throw `NotFoundError` if the caller expected it
   - **Mutation**: the updated/created entity, or `ActionResult<T>` for server actions

6. **Multi-tenant filter?** Every query / mutation in `orgProcedure` filters by `ctx.orgId`. This is automatic enforcement, not "remember to add WHERE."

7. **Pagination shape?**
   - **Offset** — default for everything (admin tables, settings, normal CRUD)
   - **Cursor** — only for real-time feeds, append-only logs, or pagination-stable-under-inserts requirements (chat messages, audit log)

8. **Aggregations in list?** If the list view needs counts (e.g. "customer with vehicle count"), use a subquery / leftJoin + groupBy rather than a per-row round-trip:

   ```ts
   ctx.db.select({
     ...getTableColumns(customers),
     vehicleCount: count(vehicles.id),
   }).from(customers).leftJoin(vehicles, ...).groupBy(customers.id);
   ```

9. **Error shape?**
   - Throw `AuthError`, `NotFoundError`, `ValidationError` from `src/lib/errors.ts`
   - For server actions, catch at the boundary and convert to `{ error: 'message' }`
   - For tRPC, throw `TRPCError({ code, message })`

10. **Audit log?** Fire-and-forget at the mutation boundary. Never `await` it on the critical path. See `factory-security.md`.

## Reference: canonical server action

```ts
// features/customers/actions.ts
'use server';

import { customerInputSchema } from './schema';
import { withOrgContext } from '@/lib/auth';
import { db } from '@/db';
import { customers } from '@/db/schema';
import { logAdminAction } from '@/lib/admin/activity';
import type { ActionResult } from '@/lib/api/types';

export async function createCustomer(input: unknown): Promise<ActionResult<Customer>> {
  const parsed = customerInputSchema.safeParse(input);
  if (!parsed.success) return { error: parsed.error.issues[0].message };

  return withOrgContext(async ({ orgId, user }) => {
    const [customer] = await db.insert(customers).values({
      ...parsed.data,
      orgId,
    }).returning();

    logAdminAction({ action: 'customer.create', subject_id: customer.id, actor_id: user.id })
      .catch((err) => console.error('audit log failed', err));

    return { data: customer };
  });
}
```

## Reference: canonical tRPC router

```ts
// server/api/routers/customers.ts
import { z } from 'zod';
import { eq, and, ilike, or, count, desc, asc } from 'drizzle-orm';
import { createTRPCRouter, orgProcedure } from '../trpc';
import { customers, vehicles } from '@/db/schema';

const listInput = z.object({
  limit: z.number().int().min(1).max(100).default(50),
  offset: z.number().int().min(0).default(0),
  orderBy: z.enum(['createdAt', 'name']).default('createdAt'),
  orderDir: z.enum(['asc', 'desc']).default('desc'),
  q: z.string().optional(),
});

export const customersRouter = createTRPCRouter({
  list: orgProcedure.input(listInput).query(async ({ ctx, input }) => {
    const conditions = [eq(customers.orgId, ctx.orgId)];
    if (input.q) {
      const term = `%${input.q}%`;
      conditions.push(or(ilike(customers.name, term), ilike(customers.email, term))!);
    }
    return ctx.db.select().from(customers)
      .where(and(...conditions))
      .limit(input.limit)
      .offset(input.offset)
      .orderBy(input.orderDir === 'desc' ? desc(customers[input.orderBy]) : asc(customers[input.orderBy]));
  }),

  create: orgProcedure.input(createInput).mutation(async ({ ctx, input }) => {
    const [customer] = await ctx.db.insert(customers).values({ ...input, orgId: ctx.orgId }).returning();
    logAdminAction({ action: 'customer.create', subject_id: customer.id, actor_id: ctx.user.id })
      .catch((err) => console.error('audit log failed', err));
    return customer;
  }),
});

// server/api/root.ts
export const appRouter = createTRPCRouter({
  customers: customersRouter,
  // ... add a line per domain. Manual registration, easy to grep.
});
```

## Output format

```
## Restated request
<one sentence>

## API surface
- Style: <server actions / tRPC / REST>
- Auth tier: <public / protected / org>
- Operations: <list / detail / create / update / delete / custom>

## Files to create or modify
<bulleted with paths>

## Code
<organized by file>

## Conventions check
- Per-endpoint Zod input: yes
- Multi-tenant filter (orgId): yes
- Pagination shape: <offset / cursor — why>
- Aggregation strategy: <subquery / leftJoin / N+1 — flag if N+1>
- Audit log fire-and-forget: <yes — at mutation boundary>
- Error class taxonomy used: <yes>

## Open questions
<things the user should confirm>
```

## What you do NOT do

- **Don't mix tRPC and server actions in the same project.** Pick a side.
- **Don't write per-route HTTP handlers when tRPC exists.** Use the fetch adapter.
- **Don't `UPDATE` or `DELETE` without `WHERE`.** ESLint Drizzle rule from `factory-data-layer.md`.
- **Don't await audit logs on the mutation critical path.** Fire-and-forget.
- **Don't reach for cursor pagination by default.** Offset is fine for almost everything.
- **Don't make every endpoint `publicProcedure`.** Auth tier explicitly per endpoint.
- **Don't return raw `Error` objects to the client.** Convert at the boundary.
- **Don't filter by an `orgId` from the request body.** Always from session.
- **Don't put per-mutation schemas in a separate file** unless they're shared with the client form schemas.

## When the request is too small for this framework

If the user asks to add a single field to an existing input schema or change one validation rule, do it directly. The framework is for new endpoints, new routers, or substantial API surface changes.
