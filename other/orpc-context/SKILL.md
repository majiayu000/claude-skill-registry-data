---
name: oRPC Context
description: Type-safe dependency injection pattern in oRPC.
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# Context in oRPC

oRPC's context mechanism provides a type-safe dependency injection pattern. Two types:

* **Initial Context:** Provided explicitly when invoking a procedure.
* **Execution Context:** Generated during procedure execution, typically by middleware.

## Initial Context

```ts
const base = os.$context<{ headers: Headers, env: { DB_URL: string } }>()

const getting = base.handler(async ({ context }) => {
  console.log(context.env)
})

export const router = { getting }
```

Pass initial context explicitly:

```ts
import { RPCHandler } from '@orpc/server/fetch'

const handler = new RPCHandler(router)

export default function fetch(request: Request) {
  handler.handle(request, {
    context: {
      headers: request.headers,
      env: { DB_URL: '***' }
    }
  })
}
```

## Execution Context

Provided dynamically through middleware:

```ts
import { cookies, headers } from 'next/headers'

const base = os.use(async ({ next }) => next({
  context: {
    headers: await headers(),
    cookies: await cookies(),
  },
}))

const getting = base.handler(async ({ context }) => {
  context.cookies.set('key', 'value')
})
```

## Combining Initial and Execution Context

```ts
const base = os.$context<{ headers: Headers, env: { DB_URL: string } }>()

const requireAuth = base.middleware(async ({ context, next }) => {
  const user = parseJWT(context.headers.get('authorization')?.split(' ')[1])
  if (user) return next({ context: { user } })
  throw new ORPCError('UNAUTHORIZED')
})

const dbProvider = base.middleware(async ({ context, next }) => {
  const client = new Client(context.env.DB_URL)
  try {
    await client.connect()
    return next({ context: { db: client } })
  } finally {
    await client.disconnect()
  }
})

const getting = base
  .use(dbProvider)
  .use(requireAuth)
  .handler(async ({ context }) => {
    console.log(context.db)
    console.log(context.user)
  })
```

> When you pass additional context to `next`, it merges with the existing context.
