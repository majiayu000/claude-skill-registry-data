---
name: factory-api
description: API conventions for both server actions and tRPC builds. Covers the decision between them, per-mutation Zod input schemas, central router composition, pagination shape, multi-field search via Drizzle `ilike` + `or()`, mutation lifecycle hooks, conditional query enabling, stale-time defaults, error response shape and custom error class taxonomy, mutation-boundary audit logging, fetch adapter for tRPC routes. Read when designing or implementing any data-mutation endpoint.
---

# Factory api

Each section leads with **Principle** (one sentence, stack-agnostic), then **Why** (constraint → option → tradeoff), then **Recipe** (the Next.js / Drizzle / tRPC shape we use), and **Failure mode** when there's one to name. Sections that are pure style with no deeper truth are marked `Recipe only`. Editors: if the Principle could appear unchanged in *Clean Code*, sharpen the Why with a Factory-specific observation or drop the section to Recipe only — honesty over inflation.

## API style — pick one

**Principle.** Pick one transport style per project; don't mix server actions and tRPC.

**Why.** Two transport styles in one codebase means two error-handling conventions, two cache-invalidation patterns, two surfaces to audit. The cost compounds linearly with every new endpoint; the cleanup is almost never worth the disruption. The decision is cheap at project start and expensive six months in.

**Recipe.**

| Style | Pick when |
|---|---|
| **Server actions** | Default. Feature-folder colocation matters. One frontend consumer. App-internal API only. Pairs with TanStack Query `useMutation`. |
| **tRPC** | ≥3 entities with cross-feature queries. Multiple frontend consumers. Need typed RPC across a real network boundary. |
| **REST / OpenAPI** | Only when an external system needs to call you. Don't use for internal app traffic. |

**Failure mode.** Encode imported tRPC at project start and built the rest in server actions; the unused tRPC surface created confusion at every call site for months before being deleted.

## Server actions — canonical shape

**Principle.** Every mutation: parse input first, then wrap with org context, then fire-and-forget the audit log.

**Why.** Three contracts in tension. Validation is the boundary guarantee — past `safeParse`, downstream code assumes the shape. Org context is the tenant guarantee — without it, a cross-tenant write is one missing filter away. Audit is the reconstructability guarantee — but it's after-the-fact, so it never blocks the response. The order matters: validation can refuse; org context can refuse; audit can fail silently.

**Recipe.**

```ts
// features/customers/actions.ts
'use server';

import { customerInputSchema } from './schema';
import { requireAuth, withOrgContext } from '@/lib/auth';
import { db } from '@/db';
import { customers } from '@/db/schema';
import { logAdminAction } from '@/lib/admin/activity';

export async function createCustomer(input: unknown): Promise<ActionResult<Customer>> {
  const parsed = customerInputSchema.safeParse(input);
  if (!parsed.success) {
    return { error: parsed.error.issues[0].message };
  }

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

type ActionResult<T> = { data: T; error?: never } | { error: string; data?: never };
```

Result type is a discriminated union — client checks `if ('error' in result)`.

## TanStack Query hook wrapping the action

**Principle.** Invalidate at the 2-segment query-key prefix, not the individual key.

**Why.** A list query and a detail query for the same entity share the same invalidation trigger — a mutation invalidates both. Per-key invalidation means writing the prefix twice and forgetting one. Prefix invalidation hits both with one call and stays correct as the entity grows new views.

**Recipe.**

```ts
// features/customers/hooks.ts
'use client';

import { useMutation, useQueryClient } from '@tanstack/react-query';
import { createCustomer } from './actions';

export function useCreateCustomer() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: createCustomer,
    onSuccess: () => qc.invalidateQueries({ queryKey: ['customers'] }),
  });
}
```

## tRPC — central router composition

**Principle.** Manual registration over automagic discovery.

**Why.** A grep-able surface area beats an auto-discovery convention. Every new domain is one diff line that names itself. "Where are all the routers?" answered by reading one file. The cost of one explicit line per domain is trivial; the cost of an implicit auto-discovery scheme is one debugging session per onboarding.

**Recipe.**

```ts
// src/server/api/root.ts
export const appRouter = createTRPCRouter({
  customers: customersRouter,
  vehicles: vehiclesRouter,
  invoices: invoicesRouter,
  // explicit naming, manual registration — no automagic
});

export type AppRouter = typeof appRouter;
```

## Procedure tiers — stacked

**Principle.** Stack permission tiers by extension, not by independent definition.

**Why.** Procedure tiers are an additive permission graph: every authenticated procedure also passes the public middleware; every org-scoped procedure also passes the auth middleware. Building each tier by extending the prior one makes the chain visible at the definition site and impossible to drift. Building each tier independently means duplicated middleware that diverges silently.

**Recipe.**

```ts
export const publicProcedure = t.procedure;
export const protectedProcedure = publicProcedure.use(requireAuthMiddleware);
export const orgProcedure = protectedProcedure.use(requireOrgMiddleware);
```

See `factory-auth.md` for the middleware shapes.

**Failure mode.** Ford-analysis: every procedure defined as `publicProcedure`. Auth checks lived inside each handler and drifted. Three procedures shipped without auth before someone noticed.

## Per-mutation Zod input

**Principle.** One Zod schema per mutation; colocate with the router.

**Why.** Mutations diverge in shape long before they look like they will — `create` needs fields `update` doesn't, `update` allows partial input `create` can't. A shared schema with `.optional()` everywhere becomes a parse layer that enforces nothing. Per-mutation schemas keep each contract sharp. Colocation means refactoring the mutation refactors the schema in the same diff.

**Recipe.**

```ts
const createCustomerInput = z.object({
  name: z.string().min(1),
  email: z.string().email(),
  // ...
});

export const customersRouter = createTRPCRouter({
  create: orgProcedure
    .input(createCustomerInput)
    .mutation(async ({ ctx, input }) => {
      // ctx.orgId is set by middleware
      const [customer] = await ctx.db.insert(customers).values({
        ...input,
        orgId: ctx.orgId,
      }).returning();
      return customer;
    }),
});
```

Schemas live next to the router, not in a separate file — unless shared with the client form, in which case see `factory-forms.md` on the three-variant pattern.

## Pagination — limit/offset/orderBy

**Principle.** Offset pagination by default; cursor only when offset actually breaks.

**Why.** Offset gives jump-to-page-N at no additional state cost and keeps client state to a single integer. Cursor breaks that affordance, requires more client state, and only pays off past ~100K rows or on append-only feeds. Defaulting to cursor is paying the complexity tax without ever needing the scale.

**Recipe.**

```ts
const listInput = z.object({
  limit: z.number().int().min(1).max(100).default(50),
  offset: z.number().int().min(0).default(0),
  orderBy: z.enum(['createdAt', 'updatedAt', 'name']).default('createdAt'),
  orderDir: z.enum(['asc', 'desc']).default('desc'),
});

list: orgProcedure.input(listInput).query(async ({ ctx, input }) => {
  return ctx.db.select().from(customers)
    .where(eq(customers.orgId, ctx.orgId))
    .limit(input.limit)
    .offset(input.offset)
    .orderBy(input.orderDir === 'desc' ? desc(customers[input.orderBy]) : asc(customers[input.orderBy]));
});
```

Cothon uses cursor for chat messages — append-only, never-jump-to-page. That's the right case for cursor.

## Multi-field search — `ilike` + `or()`

**Principle.** Start with `ilike` over the obvious fields; promote to full-text search only when search becomes the bottleneck.

**Why.** Full-text search is real infrastructure — `tsvector` indexes, query parsers, ranking. At 10K rows `ilike` works fine. At 1M rows the upgrade is forced and you'll have the row count to justify it. Reaching for `tsvector` at 1K rows is engineering against a workload that doesn't exist yet.

**Recipe.**

```ts
import { ilike, or, and, eq } from 'drizzle-orm';

const searchTerm = `%${input.q}%`;
const results = await ctx.db.select().from(customers).where(
  and(
    eq(customers.orgId, ctx.orgId),
    or(
      ilike(customers.name, searchTerm),
      ilike(customers.email, searchTerm),
      ilike(customers.phone, searchTerm),
    ),
  ),
);
```

## Aggregated stats in list queries

**Principle.** If the list view shows a count, the list query returns the count.

**Why.** A list page that issues one row-level "fetch count" per visible row is N+1 in slow motion — works fine at 10 rows, falls over at 100. A single aggregated query with `leftJoin + groupBy` returns the same data in one round trip. The cost is one slightly-longer SQL statement; the savings are linear in row count.

**Recipe.**

```ts
list: orgProcedure.input(listInput).query(async ({ ctx, input }) => {
  return ctx.db
    .select({
      ...getTableColumns(customers),
      vehicleCount: count(vehicles.id),
      chargerCount: count(chargers.id),
    })
    .from(customers)
    .leftJoin(vehicles, eq(vehicles.customerId, customers.id))
    .leftJoin(chargers, eq(chargers.customerId, customers.id))
    .where(eq(customers.orgId, ctx.orgId))
    .groupBy(customers.id);
});
```

For N+1-prone aggregations on detail views, use a subquery (see `factory-data-layer.md`).

## Mutation lifecycle hooks

**Principle.** Specify `onSuccess`; let errors propagate to the boundary.

**Why.** Per-call-site error handling is duplication that ages badly — every new mutation adds another copy of the toast-on-error pattern. A global error boundary catches what falls through; `onSuccess` carries the per-mutation specifics (which key to invalidate, which drawer to close). The boundary handles the policy; the hook handles the local action.

**Recipe.**

```tsx
const createMutation = useMutation({
  mutationFn: createCustomer,
  onSuccess: (result) => {
    if ('error' in result) {
      toast.error(result.error);
      return;
    }
    toast.success('Customer created');
    setMode({ kind: 'closed' });
    qc.invalidateQueries({ queryKey: ['customers'] });
  },
});
```

For server actions with `ActionResult<T>` shape, error-handling lives in `onSuccess` (the discriminated-union check). For tRPC mutations, errors throw — handle via `onError` or React Error Boundary.

## Conditional query enabling

**Principle.** Gate a dependent query with `enabled`; never let it fire with `undefined` arguments.

**Why.** A query that fires with `undefined` arguments either errors at the server, returns garbage, or — worst — returns a successful response for "all rows" because the filter silently dropped. `enabled` makes the dependency declarative and removes the failure mode.

**Recipe.**

```ts
const { data } = useQuery({
  queryKey: ['vehicle', 'list', { fleetId }],
  queryFn: () => listVehicles({ fleetId }),
  enabled: !!fleetId,
});
```

## Stale time defaults

**Principle.** Pick a baseline `staleTime` at the QueryClient; bump per-query for stable reference data.

**Why.** Per-query `staleTime` decisions in every hook is friction that compounds — every new query is another stale-time call. A 60s baseline catches most cases; opt into longer only when the data genuinely doesn't change. `staleTime: Infinity` is a different design — invalidation becomes the only refresh path, so one missed invalidation is permanent stale state.

**Recipe.**

```ts
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 60_000,          // 1 minute default — covers most cases
      gcTime: 5 * 60_000,         // 5 minute default
      retry: 1,
    },
  },
});
```

For stable reference data (states, vehicle types, country list), bump to 3-5 minutes per-query.

**Failure mode.** Setting `staleTime: Infinity` globally because "data is mostly cached anyway" — a missed invalidation now needs a hard refresh to recover.

## Error response shape

**Principle.** One error shape across all transports; convert at the boundary.

**Why.** A client display layer that handles "the error shape from server actions" and "the error shape from tRPC" separately is two display layers. One `ApiError` shape at the boundary is one display layer that doesn't drift when a new transport joins (mobile native client, webhook handler).

**Recipe.**

```ts
type ApiError = {
  code: 'unauthenticated' | 'forbidden' | 'not_found' | 'validation_failed' | 'conflict' | 'internal';
  message: string;
  details?: unknown;
};
```

For server actions, return `{ error: 'message' }`. For tRPC, throw `TRPCError({ code, message })`. Client converts both to the same `ApiError` shape for display.

## Custom error class taxonomy

**Principle.** Errors carry a type, not a string.

**Why.** A `catch (err)` block branching on `err.message` ages worse than any other catch idiom — error messages get reworded for clarity, and the branch silently breaks. Class taxonomy gives `instanceof` checks that don't drift, plus the constructor is the contract for what context the error needs.

**Recipe.**

```ts
// src/lib/errors.ts
export class AuthError extends Error {
  constructor(public reason: 'unauthenticated' | 'forbidden') {
    super(reason);
  }
}

export class NotFoundError extends Error {
  constructor(public resource: string) {
    super(`${resource} not found`);
  }
}

export class ValidationError extends Error {
  constructor(public issues: { field: string; message: string }[]) {
    super('validation_failed');
  }
}
```

Throw these from server-side code. Catch at the route handler / server action boundary; convert to `ApiError` shape for the client.

## Audit logging at mutation boundary

**Principle.** Fire-and-forget audit logs; never on the critical path.

**Why.** An audit log is for after-the-fact reconstruction. If logging fails, the mutation still succeeded — that's the right answer. If logging blocks, every mutation is gated by the logging service's availability. Awaiting the audit log makes one slow logging call into one slow mutation; fire-and-forget makes it into one missed log line. Log lines are recoverable; user-visible slowness is not.

**Recipe.**

```ts
// fire-and-forget — never block the mutation
logAdminAction({
  action: 'customer.update',
  subject_id: customerId,
  actor_id: userId,
  metadata: { fields_changed: Object.keys(input) },
}).catch((err) => console.error('audit log failed', err));
```

Log actions and IDs. Never log raw payloads — see `factory-security.md` on data minimization.

**Failure mode.** Awaiting the audit insert in the mutation path — one slow logging call became one slow mutation; p95 mutations went from 80ms to 400ms when the logging service degraded.

## Fetch adapter for tRPC routes (App Router)

**Principle.** One handler for all tRPC routes; don't write per-route HTTP handlers.

**Why.** Per-route handlers duplicate the tRPC invocation, the context creation, the auth check. The fetch adapter is the integration point — anything past it is rewriting it. The cost of the adapter is one file; the cost of per-route handlers is one debugging session per new route.

**Recipe.**

```ts
// app/api/trpc/[trpc]/route.ts
import { fetchRequestHandler } from '@trpc/server/adapters/fetch';
import { appRouter } from '@/server/api/root';
import { createTRPCContext } from '@/server/api/trpc';

const handler = (req: Request) => fetchRequestHandler({
  endpoint: '/api/trpc',
  req,
  router: appRouter,
  createContext: () => createTRPCContext({ req }),
});

export { handler as GET, handler as POST };
```

Same handler for GET and POST.

## Source patterns

Fleet-advisor (procedure tier stacking, central router composition, per-mutation Zod, aggregated stats in list queries, conditional query enabling, stale-time configuration, fetch adapter), kairos (server-action shape with discriminated-union result, useTransition wrapper, query-key naming, fire-and-forget audit logging, custom error classes), duezy (tRPC with org context, batch link with superjson, 60s default stale), encode/monorepo (custom error class taxonomy: DatabaseError, AuthError, NotFoundError, UnauthorizedError), cothon (COUNT subquery to avoid N+1, cursor pagination for chat messages).
