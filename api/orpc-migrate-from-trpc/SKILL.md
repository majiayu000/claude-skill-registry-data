---
name: oRPC Migrate from tRPC
description: A comprehensive guide to migrate your tRPC application to oRPC.
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# Migrating from tRPC

oRPC draws significant inspiration from tRPC, making migration straightforward.

> For quick enhancement without full migration, see [tRPC Integration](/docs/openapi/integrations/trpc).

## Core Concepts Comparison

| Concept                 | tRPC                         | oRPC                |
| ----------------------- | ---------------------------- | ------------------- |
| Router                  | `t.router()`                 | an object           |
| Procedure               | `t.procedure`                | `os`                |
| Context                 | `t.context()`                | `os.$context()`     |
| Create Middleware       | `t.middleware()`             | `os.middleware()`   |
| Use Middleware          | `t.procedure.use()`          | `os.use()`          |
| Input Validation        | `t.procedure.input(schema)`  | `os.input(schema)`  |
| Output Validation       | `t.procedure.output(schema)` | `os.output(schema)` |
| Error Handling          | `TRPCError`                  | `ORPCError`         |
| Serializer              | `superjson`                  | built-in            |

## Step-by-Step Migration

### 1. Installation

```sh
npm uninstall @trpc/server @trpc/client @trpc/tanstack-react-query
npm install @orpc/server@latest @orpc/client@latest @orpc/tanstack-query@latest
```

### 2. Initialize

```ts
import { ORPCError, os } from '@orpc/server'

export async function createRPCContext(opts: { headers: Headers }) {
  const session = await auth()
  return { headers: opts.headers, session }
}

const o = os.$context<Awaited<ReturnType<typeof createRPCContext>>>()

const timingMiddleware = o.middleware(async ({ next, path }) => {
  const start = Date.now()
  try {
    return await next()
  } finally {
    console.log(`[oRPC] ${path} took ${Date.now() - start}ms`)
  }
})

export const publicProcedure = o.use(timingMiddleware)

export const protectedProcedure = publicProcedure.use(({ context, next }) => {
  if (!context.session?.user) {
    throw new ORPCError('UNAUTHORIZED')
  }
  return next({
    context: { session: { ...context.session, user: context.session.user } }
  })
})
```

### 3. Procedures

In oRPC there are no separate `.query`/`.mutation`/`.subscription` methods. Use `.handler` for all procedure types.

```ts
export const planetRouter = {
  list: publicProcedure
    .input(z.object({ cursor: z.number().int().default(0) }))
    .handler(({ input }) => {
      return { planets: [], nextCursor: input.cursor + 1 }
    }),

  create: protectedProcedure
    .input(z.object({
      name: z.string().min(1),
      distanceFromSun: z.number().positive()
    }))
    .handler(async ({ context, input }) => {}),
}
```

### 4. App Router

In oRPC you don't need to wrap routers — plain objects are enough:

```ts
export const appRouter = {
  planet: planetRouter,
}
```

### 5. Error Handling

```ts
throw new ORPCError('BAD_REQUEST', {
  message: 'Invalid input',
  data: 'some data',
  cause: validationError
})
```

### 6. Server Setup (Next.js)

```ts
// app/api/orpc/[[...rest]]/route.ts
import { RPCHandler } from '@orpc/server/fetch'

const handler = new RPCHandler(appRouter, {
  interceptors: [
    async ({ next }) => {
      try { return await next() }
      catch (error) { console.error(error); throw error }
    }
  ]
})

async function handleRequest(request: Request) {
  const { response } = await handler.handle(request, {
    prefix: '/api/orpc',
    context: await createORPCContext(request)
  })
  return response ?? new Response('Not found', { status: 404 })
}

export const GET = handleRequest
export const POST = handleRequest
```

### 7. Client Setup

```ts
import { createORPCClient, onError } from '@orpc/client'
import { RPCLink } from '@orpc/client/fetch'

const link = new RPCLink({
  url: 'http://localhost:3000/api/orpc',
  interceptors: [onError(e => console.error(e))],
})

export const client: RouterClient<typeof appRouter> = createORPCClient(link)

// Usage:
const { planets } = await client.planet.list({ cursor: 0 })
```

### 8. TanStack Query Integration

```ts
import { createTanstackQueryUtils } from '@orpc/tanstack-query'

export const orpc = createTanstackQueryUtils(client)

// Usage:
const query = useQuery(orpc.planet.list.queryOptions({ input: { cursor: 0 } }))
const mutation = useMutation(orpc.planet.create.mutationOptions())
```
