---
name: trpc
description: tRPC — end-to-end type-safe APIs with routers, procedures, middleware, context, React Query.
---

## trpc

### Routers & Procedures
- `t.router({ user: t.procedure.query(...) })` — define API surface.
- Procedures: `.query()` for reads, `.mutation()` for writes, `.subscription()` for real-time events.
- Input validation: `t.procedure.input(z.string()).query(...)` — auto-inferred types.
- `.output(z.object({...}))` — validate and type response shape.

### Middleware & Context
- `t.middleware(async ({ ctx, next }) => { ... return next({ ctx: enriched }) })` — pipeline.
- Context: `router.createContext()` — per-request initialization (auth, DB, session).
- Per-procedure middleware via `.use(middleware)` chaining.

### Error Handling
- `TRPCError` — `new TRPCError({ code: 'NOT_FOUND', message: '...' })` with typed codes.
- Error formatting: `router.formatError(({ shape, error }) => ...)` — customize error shape.
- Error filtering by code in client `onError` callbacks.

### React Query Integration
- Auto-generated hooks: `trpc.user.useQuery(args)`, `.useMutation()`, `.useUtils().invalidate()`.
- SSR: `trpcNext.createSSGHelpers()` or `trpcNext.withTRPC()` HOC for Next.js.
- Server-side calls: `caller = router.createCaller(ctx)` — invoke without HTTP.

### Adapters
- HTTP: `@trpc/server/adapters/express`, `@trpc/server/adapters/next`, `@trpc/server/adapters/fastify`.
- Standalone: `@trpc/server/adapters/standalone` for Node http server.
- AWS Lambda: `@trpc/server/adapters/aws-lambda`.
