---
name: oRPC Solid Start Adapter
description: Use oRPC inside a Solid Start project.
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# Solid Start Adapter

[Solid Start](https://start.solidjs.com/) is a full stack JavaScript framework for building web applications with SolidJS.

## Server

```ts
// src/routes/rpc/[...rest].ts
import type { APIEvent } from '@solidjs/start/server'
import { RPCHandler } from '@orpc/server/fetch'
import { onError } from '@orpc/server'

const handler = new RPCHandler(router, {
  interceptors: [onError(e => console.error(e))],
})

async function handle({ request }: APIEvent) {
  const { response } = await handler.handle(request, {
    prefix: '/rpc',
    context: {}
  })
  return response ?? new Response('Not Found', { status: 404 })
}

export const HEAD = handle
export const GET = handle
export const POST = handle
export const PUT = handle
export const PATCH = handle
export const DELETE = handle
```

## Client

```ts
import { RPCLink } from '@orpc/client/fetch'
import { getRequestEvent } from 'solid-js/web'

const link = new RPCLink({
  url: `${typeof window !== 'undefined' ? window.location.origin : 'http://localhost:3000'}/rpc`,
  headers: () => getRequestEvent()?.request.headers ?? {},
})
```

## Optimize SSR

```ts
// src/lib/orpc.ts
if (typeof window === 'undefined') {
  await import('./orpc.server')
}

import type { RouterClient } from '@orpc/server'
import { RPCLink } from '@orpc/client/fetch'
import { createORPCClient } from '@orpc/client'

declare global {
  var $client: RouterClient<typeof router> | undefined
}

const link = new RPCLink({
  url: () => {
    if (typeof window === 'undefined') {
      throw new Error('RPCLink is not allowed on the server side.')
    }
    return `${window.location.origin}/rpc`
  },
})

export const client: RouterClient<typeof router> = globalThis.$client ?? createORPCClient(link)
```

```ts
// src/lib/orpc.server.ts
import { createRouterClient } from '@orpc/server'
import { getRequestEvent } from 'solid-js/web'

globalThis.$client = createRouterClient(router, {
  context: async () => {
    const headers = getRequestEvent()?.request.headers
    return { headers }
  },
})
```
