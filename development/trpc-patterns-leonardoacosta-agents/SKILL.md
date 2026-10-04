---
name: trpc-patterns
description: tRPC v11 patterns for T3 Turbo App Router — queryOptions/mutationOptions, type inference with RouterOutputs/RouterInputs, middleware composition, and error handling. Use when building tRPC routers, typing procedures, or integrating tRPC with React Query.
user-invocable: false
category: API
level: library
engineer: api-engineer
gate: "pnpm tsc --noEmit"
bundles: []
allowed-tools: Read, Glob, Grep
paths: ["packages/api/**"]
---


# tRPC Patterns — T3 Turbo / v11 / App Router

Expert reference for tRPC v11 with Next.js App Router, React Query, TypeScript, and Drizzle.
API lives in `packages/api/src/`. Canonical pattern: `queryOptions()` / `mutationOptions()`, never direct hooks.

## Router Composition

```typescript
// packages/api/src/router/user.ts
export const userRouter = createTRPCRouter({
  getById: protectedProcedure
    .input(z.object({ id: z.string() }))
    // illustrative only; ctx.db is BLOCKED here — see § DB Import — ctx.db is BLOCKED
    .query(({ ctx, input }) => ctx.db.query.user.findFirst({ where: eq(users.id, input.id) })),
});

// packages/api/src/root.ts
export const appRouter = createTRPCRouter({
  user: userRouter,
  post: postRouter,
});

// Must export for client inference — without this, RouterOutputs breaks
export type AppRouter = typeof appRouter;
```

`protectedProcedure` vs `publicProcedure` is enforced in middleware, not repeated per-procedure.
`ctx.session` and `ctx.db` are injected by the context factory in `packages/api/src/trpc.ts`.

---

## Type Inference (Non-Obvious)

```typescript
import type { RouterOutputs, RouterInputs } from "~/trpc/react";

// Extract return types — no manual interface duplication
type User = RouterOutputs["user"]["getById"];
type UserList = RouterOutputs["user"]["list"][number];

// Extract input types — useful for form prop typing
type GetByIdInput = RouterInputs["user"]["getById"];

// Pass procedure options as props without coupling to hooks
import type { inferReactQueryProcedureOptions } from "@trpc/react-query";
type UserQueryOptions = inferReactQueryProcedureOptions<AppRouter>["user"]["getById"];
```

Using `any` on tRPC outputs defeats the type inference chain — the error surfaces downstream as an
untyped `data` in React Query, losing autocomplete and null safety.

---

## Query / Mutation Patterns — Canonical

```typescript
// ✅ queryOptions() — respects staleTime config, cache key stable, composable
const opts = api.user.getById.queryOptions({ id })
const { data } = useQuery(opts)

// ✅ With staleTime override
const { data } = useQuery({ ...api.user.list.queryOptions(), staleTime: 60_000 })

// ✅ mutationOptions() for forms
const opts = api.user.update.mutationOptions()
const mutation = useMutation(opts)

// ❌ Direct hook — bypasses centralized cache config, harder to compose
const { data } = api.user.getById.useQuery({ id })
```

`queryOptions()` returns a plain object (`{ queryKey, queryFn, ... }`). This enables:
- Passing options to `useQuery` / `useSuspenseQuery` / `prefetchQuery` with the same call
- Spreading overrides without losing the query key

---

## Server Components: createCaller

For RSC data fetching, use `createCaller` — it runs procedures in-process (no HTTP round-trip):

```typescript
// app/users/page.tsx
import { createCaller } from "~/server/api/root";
import { createTRPCContext } from "~/server/api/trpc";

export default async function UsersPage() {
  const ctx = await createTRPCContext({ headers: new Headers() });
  const caller = createCaller(ctx);
  const users = await caller.user.list();  // direct call, full type safety
  return <UserList users={users} />;
}
```

Never use client-side `api.*` hooks in Server Components — they require the React Query provider
which is client-only.

---

## Middleware Patterns

```typescript
// Auth middleware — throw early, never rely on procedure-level null checks
const enforceAuth = t.middleware(({ ctx, next }) => {
  if (!ctx.session?.user) throw new TRPCError({ code: "UNAUTHORIZED" });
  return next({ ctx: { ...ctx, session: ctx.session } });  // narrows session to non-null
});

export const protectedProcedure = t.procedure.use(enforceAuth);

// Logging middleware — chain before auth so all requests are logged
const loggerMiddleware = t.middleware(async ({ path, type, next }) => {
  const start = Date.now();
  const result = await next();
  console.log(`[tRPC] ${type} ${path} — ${Date.now() - start}ms`);
  return result;
});

// Rate limiting — attach to publicProcedure or a specific sub-procedure, not per-handler
const rateLimitedProcedure = t.procedure.use(rateLimitMiddleware).use(enforceAuth);
```

`opts.next({ ctx })` merges with the existing context — only override the fields you're narrowing.

---

## Error Handling

```typescript
// Server: throw TRPCError with semantic code
throw new TRPCError({ code: "NOT_FOUND", message: "User not found" });
throw new TRPCError({ code: "FORBIDDEN", message: "Cannot modify another user's data" });
throw new TRPCError({ code: "BAD_REQUEST", message: "Invalid state transition" });

// Zod validation errors surface automatically as BAD_REQUEST — don't catch them
// ❌ Wrong: try/catch around input parsing is noise

// Client: handle by code
if (error?.data?.code === "UNAUTHORIZED") router.push("/login");
if (error?.data?.code === "NOT_FOUND") setNotFound(true);
```

Code reference: `UNAUTHORIZED` (no session), `FORBIDDEN` (session exists, wrong permissions),
`NOT_FOUND` (resource missing), `BAD_REQUEST` (invalid input beyond Zod), `INTERNAL_SERVER_ERROR`
(unexpected failures — never expose internal details in message).

---

## Performance

**staleTime defaults:**

| Query type | Recommended staleTime |
|---|---|
| User profile, session data | `Infinity` (changes only on mutation) |
| List views | `30_000` – `60_000` ms |
| Real-time / polling | `0` (always refetch) |
| Reference data (enums, config) | `Infinity` |

Set globally in `TRPCReactProvider` via `queryClient` config. Override per-query only when the
data freshness requirement genuinely differs.

**Batching gotcha:** tRPC batches concurrent requests by default. This is good for page load but
creates a waterfall when requests are intentionally sequential (e.g., fetch user → fetch user's
data). Use `httpBatchLink` with `maxURLLength` or split into separate fetch calls if batching
causes observable latency.

---

## Never List

- NEVER call `useQuery` / `useMutation` directly on tRPC procedures — use `queryOptions()` / `mutationOptions()` wrappers
- NEVER put business logic in Zod input validators — validation shape only, not authorization
- NEVER return the full Drizzle model from a procedure — select specific fields to avoid leaking columns
- NEVER ignore `UNAUTHORIZED` errors on the client — always redirect or surface to user
- NEVER use `createCaller` from client components — it bypasses HTTP and auth headers

---

## Project-Specific Patterns (T3 Turbo Monorepo)

### DB Import — ctx.db is BLOCKED

The skill's `Router Composition` example uses `ctx.db` for illustration, but in this monorepo it
causes a TypeScript recursion error (full rationale: `t3-code-patterns` § Database > Import
Pattern). Always import `db` directly — worked example (tenant-scoped CRUD router):

```typescript
// ✅ Correct — import db directly
import { db } from "@{workspace}/db/client";

export const entityRouter = createTRPCRouter({
  getAll: protectedProcedure
    .input(z.object({ limit: z.number().optional() }))
    .query(async ({ ctx, input }) => {
      return await db.query.entities.findMany({
        where: eq(entities.organizationId, ctx.organizationId),
        limit: input.limit ?? 50,
      });
    }),

  getById: protectedProcedure
    .input(z.object({ id: z.string().uuid() }))
    .query(async ({ ctx, input }) => {
      const entity = await db.query.entities.findFirst({
        where: and(
          eq(entities.id, input.id),
          eq(entities.organizationId, ctx.organizationId),
        ),
      });
      if (!entity) throw new TRPCError({ code: "NOT_FOUND" });
      return entity;
    }),

  create: protectedProcedure
    .input(createEntitySchema)
    .mutation(async ({ ctx, input }) => {
      const [entity] = await db
        .insert(entities)
        .values({ ...input, organizationId: ctx.organizationId })
        .returning();
      return entity;
    }),
});

// ❌ BLOCKED — ctx.db causes TypeScript recursion in this monorepo
.query(async ({ ctx }) => {
  return await ctx.db.query.entities.findMany({...}); // Never use
});
```

### Client-Side Prefetching

```typescript
// Server component or loader
await queryClient.prefetchQuery(trpc.entity.getById.queryOptions({ id }));

// Client component — hover prefetch
const prefetch = () => {
  queryClient.prefetchQuery(trpc.entity.getById.queryOptions({ id }));
};
```

### Quick Reference

| Pattern                    | Use                  |
| -------------------------- | -------------------- |
| `trpc.x.queryOptions()`    | Wrap all queries     |
| `trpc.x.mutationOptions()` | Wrap all mutations   |
| `trpc.x.queryKey()`        | For invalidation     |
| Direct `useQuery`          | With queryOptions    |
| Direct `useMutation`       | With mutationOptions |
| `trpc.x.useQuery()`        | BLOCKED              |
| `ctx.db`                   | BLOCKED (TS recursion) |

---

## Advanced / Less-Frequent Topics

The patterns above cover day-to-day router work. These three are distinct, lower-frequency
concerns — load the matching reference when the situation applies:

| Situation | Reference |
| --- | --- |
| A router cluster is growing past ~300 lines or spans multiple sub-domains (CRUD + scheduling + assignment + reporting) and needs splitting | [`references/sub-router-structure.md`](references/sub-router-structure.md) — the `_shared.ts` barrel pattern |
| Typecheck fails with `RangeError: Maximum call stack size exceeded` as router/schema count grows | [`references/ts-serialization-limits.md`](references/ts-serialization-limits.md) — the documented three-site workaround |
| Onboarding a new contributor, or the valid procedure surface needs to be auditable in one place | [`references/procedure-inventory.md`](references/procedure-inventory.md) — the `.claude/trpc-patterns.md` inventory convention |

## Cross-Reference: Domain Errors

See `t3-code-patterns` § Domain Errors for the canonical error-handling shape. tRPC routers should throw via `DomainError` factory calls, NOT bare `throw new TRPCError(...)`.
