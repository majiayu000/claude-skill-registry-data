---
name: oRPC Next.js Adapter
description: Use oRPC inside a Next.js project (App Router and Pages Router).
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# Next.js Adapter

[Next.js](https://nextjs.org/) integration. Works with App Router and Pages Router.

> oRPC also supports [Server Action](/docs/server-action) out of the box.

## Server

```ts
// app/rpc/[[...rest]]/route.ts
import { RPCHandler } from '@orpc/server/fetch'
import { onError } from '@orpc/server'

const handler = new RPCHandler(router, {
  interceptors: [onError(e => console.error(e))],
})

async function handleRequest(request: Request) {
  const { response } = await handler.handle(request, {
    prefix: '/rpc',
    context: {},
  })
  return response ?? new Response('Not found', { status: 404 })
}

export const HEAD = handleRequest
export const GET = handleRequest
export const POST = handleRequest
export const PUT = handleRequest
export const PATCH = handleRequest
export const DELETE = handleRequest
```

## Pages Router Support

```ts
// pages/api/rpc/[[...rest]].ts
import { RPCHandler } from '@orpc/server/node'

const handler = new RPCHandler(router)

export const config = {
  api: { bodyParser: false },
}

export default async (req, res) => {
  const { matched } = await handler.handle(req, res, {
    prefix: '/api/rpc',
    context: {},
  })

  if (matched) return

  res.statusCode = 404
  res.end('Not found')
}
```

> Disable the body parser to fully utilize oRPC features like [Bracket Notation](/docs/openapi/bracket-notation).

## Client

```ts
// lib/orpc.ts
import { RPCLink } from '@orpc/client/fetch'

const link = new RPCLink({
  url: `${typeof window !== 'undefined' ? window.location.origin : 'http://localhost:3000'}/rpc`,
  headers: async () => {
    if (typeof window !== 'undefined') return {}
    const { headers } = await import('next/headers')
    return await headers()
  },
})
```

## Optimize SSR

```ts
// lib/orpc.ts
import type { RouterClient } from '@orpc/server'
import { RPCLink } from '@orpc/client/fetch'
import { createORPCClient } from '@orpc/client'

declare global {
  var $client: RouterClient<typeof router> | undefined
}

const link = new RPCLink({
  url: () => {
    if (typeof window === 'undefined') {
      throw new Error('RPCLink is not allowed on server')
    }
    return `${window.location.origin}/rpc`
  },
})

export const client: RouterClient<typeof router> = globalThis.$client ?? createORPCClient(link)
```

```ts
// lib/orpc.server.ts
import 'server-only'
import { headers } from 'next/headers'
import { createRouterClient } from '@orpc/server'

globalThis.$client = createRouterClient(router, {
  context: async () => ({ headers: await headers() }),
})
```

```ts
// instrumentation.ts
export async function register() {
  await import('./lib/orpc.server')
}
```
