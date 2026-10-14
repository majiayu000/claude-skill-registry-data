---
name: trpc-pro
description: tRPC guidance — end-to-end typesafe APIs, routers, procedures, auth, and React Query integration.
category: development
---

## Overview

tRPC gives you end-to-end type safety for TypeScript APIs without codegen or schemas: define procedures on the server, call them from the client like functions, and types flow automatically. It's the fastest path to a typesafe full-stack TypeScript app — and it's deliberately not a public-API technology. This skill covers structuring tRPC routers, procedure patterns (query/mutation/subscription), auth via context, and the React Query integration that powers the client.

## When to use

- Building a full-stack TypeScript app (Next.js, Vite + Express, etc.).
- Choosing between tRPC, REST, and GraphQL for internal APIs.
- Structuring routers, procedures, and middleware in tRPC.
- Adding auth, validation (Zod), and error handling to tRPC.
- Using subscriptions (WebSockets/SSE) with tRPC.
- Migrating an existing REST API to tRPC incrementally.

## Core concepts

- **Procedures are the API.** `publicProcedure`, `protectedProcedure` (via middleware), `query`/`mutation`/`subscription` — each procedure is one endpoint with inferred input/output types. No schema files, no codegen step.
- **Routers compose.** Nest routers by domain (`appRouter` → `userRouter`, `orderRouter`) with `mergeRouters` or nested `.router()` calls. Router structure is your API structure — organize by domain, not by technical layer.
- **Context is the request scope.** Created per request (user, DB client, request ID); middleware enriches or rejects it. Auth checks belong in middleware producing `protectedProcedure` — not repeated inside every procedure.
- **Validation with Zod.** `.input(z.object({...}))` validates at runtime and infers TypeScript types. Validate every input; tRPC's type safety is compile-time only without it.
- **Middleware pipeline.** Reusable wrappers for auth, logging, rate limiting: `.use()` chains that run before the procedure. Compose small middlewares rather than one god-middleware.
- **Error shaping.** `TRPCError` with codes (`UNAUTHORIZED`, `NOT_FOUND`, `BAD_REQUEST`...) maps to HTTP statuses; unexpected errors masked in production. Keep error codes consistent — clients switch on them.
- **React Query integration.** The client is a thin wrapper over TanStack Query: `trpc.order.get.useQuery()`, mutations with optimistic updates, automatic cache invalidation via `utils`. Learn invalidation patterns — stale UI is the common complaint.
- **Batching.** `httpBatchLink` combines calls into one HTTP request — fewer round trips, but one slow procedure delays the batch; split latency-sensitive calls onto a separate link.
- **Subscriptions.** WebSocket or SSE links for realtime; like all subscriptions, design for reconnect and resume. tRPC subscriptions are convenient but carry the same operational weight as raw WebSockets.
- **It's not for public APIs.** tRPC assumes a TypeScript client and couples client/server deploys. For third-party consumers, put a REST (or GraphQL) facade in front — don't expose tRPC directly.
- **Versioning.** tRPC has no built-in versioning; evolve procedures additively, deprecate with naming or comments, and coordinate client/server deploys since types are shared.
- **Server-component caller.** `createCaller` invokes procedures directly inside React Server Components without HTTP — same validation and auth, zero round trip.
- **Output validation.** `.output(zodSchema)` validates procedure results at runtime — catches service-layer shape drift before it reaches clients.

## Practical workflow

1. **Set up the foundation.** `initTRPC` with context creation (auth session, DB), a `publicProcedure` base, and middleware for logging; choose links (`httpBatchLink` default, `wsLink` if subscriptions).
   ```ts
   export const t = initTRPC.context<Context>().create();
   export const publicProcedure = t.procedure;
   export const protectedProcedure = t.procedure.use(isAuthed);
   ```
2. **Build domain routers.** One router per domain with queries/mutations; Zod schemas for inputs; thin procedures calling services.
   ```ts
   export const orderRouter = t.router({
     get: protectedProcedure
       .input(z.object({ id: z.string().uuid() }))
       .query(({ ctx, input }) => orderService.get(ctx, input.id)),
     cancel: protectedProcedure
       .input(z.object({ id: z.string().uuid() }))
       .mutation(({ ctx, input }) => orderService.cancel(ctx, input.id)),
   });
   ```
3. **Enforce auth in middleware.** `isAuthed` throws `UNAUTHORIZED` when `ctx.user` is missing; resource-level checks (ownership) inside services, not routers.
4. **Handle errors consistently.** Throw `TRPCError` with the right code; global error formatter for logging + masking; clients map codes to UI states.
5. **Wire the client.** React Query provider + tRPC client; use `useQuery`/`useMutation` with `onSuccess` invalidation (`utils.order.get.invalidate()`); optimistic updates for snappy mutations with rollback on error.
   ```ts
   const utils = trpc.useUtils();
   const cancel = trpc.order.cancel.useMutation({
     onMutate: async (input) => {
       await utils.order.get.cancel();
       const prev = utils.order.get.getData({ id: input.id });
       utils.order.get.setData({ id: input.id }, (o) => o && { ...o, status: "cancelled" });
       return { prev };
     },
     onError: (_e, input, ctx) => utils.order.get.setData({ id: input.id }, ctx?.prev),
     onSettled: (_d, _e, input) => utils.order.get.invalidate({ id: input.id }),
   });
   ```
6. **Paginate inputs.** Cursor-based input schemas (`{ cursor, limit }`) for lists; never return unbounded arrays from a query.
7. **Add subscriptions where needed.** `wsLink` + subscription procedures for live data; client reconnect logic; server-side cleanup on disconnect.
8. **Deploy coordinated.** Since types are shared, deploy server and client together (monorepo) or version the router contract; monitor procedure-level error rates and latencies.

## Common pitfalls

- **No input validation** — trusting TypeScript types at runtime; every procedure needs a Zod schema.
- **Auth inside procedures** — repeated, inconsistent checks; centralize in middleware → `protectedProcedure`.
- **Fat procedures** — business logic in routers becomes untestable; push to services.
- **Unbounded queries** — returning full tables; paginate every list procedure.
- **Over-batching latency** — one slow procedure in a batch delays everything; split links by latency class.
- **Exposing tRPC publicly** — third parties can't consume it without TypeScript; add a REST facade for external consumers.
- **Ignoring invalidation** — mutations that don't invalidate queries leave stale UI; define invalidation per mutation.
- **Leaking internal errors** — raw DB/validation errors to clients; format and mask in production.
- **No rate limiting** — procedures are cheap to call in loops; add middleware-based limits on expensive ones.
- **Breaking changes without coordination** — renaming a procedure breaks the client build; treat router changes as contract changes in CI.
- **Skipping output validation** — service refactors silently changing response shapes; `.output()` schemas catch the drift in tests.
- **Server-component waterfalls** — awaiting procedures sequentially in RSCs; parallelize with `Promise.all` or prefetch instead.
