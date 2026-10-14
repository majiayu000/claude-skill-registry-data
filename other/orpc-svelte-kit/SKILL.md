---
name: oRPC Svelte Kit Adapter
description: Use oRPC inside a Svelte Kit project.
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# Svelte Kit Adapter

[Svelte Kit](https://svelte.dev/docs/kit/introduction) integration.

## Server

```ts
// src/routes/rpc/[...rest]/+server.ts
import { RPCHandler } from '@orpc/server/fetch'
import { onError } from '@orpc/server'

const handler = new RPCHandler(router, {
  interceptors: [onError(e => console.error(e))],
})

const handle: RequestHandler = async ({ request }) => {
  const { response } = await handler.handle(request, {
    prefix: '/rpc',
    context: {}
  })
  return response ?? new Response('Not Found', { status: 404 })
}

export const GET = handle
export const POST = handle
export const PUT = handle
export const PATCH = handle
export const DELETE = handle
```

## Optimize SSR

```ts
// src/lib/orpc.ts
import type { RouterClient } from '@orpc/server'
import { RPCLink } from '@orpc/client/fetch'
import { createORPCClient } from '@orpc/client'

declare global {
  var $client: RouterClient<typeof router> | undefined
}

const link = new RPCLink({
  url: () => {
    if (typeof window === 'undefined') {
      throw new Error('This link is not allowed on the server side.')
    }
    return `${window.location.origin}/rpc`
  },
})

export const client: RouterClient<typeof router> = globalThis.$client ?? createORPCClient(link)
```

```ts
// src/lib/orpc.server.ts
import type { RouterClient } from '@orpc/server'
import { createORPCClient } from '@orpc/client'
import { RPCLink } from '@orpc/client/fetch'
import { getRequestEvent } from '$app/server'

const link = new RPCLink({
  url: async () => `${getRequestEvent().url.origin}/rpc`,
  async fetch(request, init) {
    return getRequestEvent().fetch(request, init)
  },
})

const serverClient: RouterClient<typeof router> = createORPCClient(link)
globalThis.$client = serverClient
```

```ts
// src/hooks.server.ts
import './lib/orpc.server'
```
