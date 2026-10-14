---
name: oRPC TanStack Start Adapter
description: Use oRPC inside a TanStack Start project with server routes, isomorphic links, and SSR optimization.
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# TanStack Start Adapter

[TanStack Start](https://tanstack.com/start) is a full-stack React framework built on [Vite](https://vitejs.dev/) and the [Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API). For additional context, see the [HTTP Adapter](/docs/adapters/http) guide.

## Server

Set up an oRPC server inside TanStack Start using its [Server Routes](https://tanstack.com/start/latest/docs/framework/react/guide/server-routes).

```ts
// src/routes/api/rpc.$.ts
import { RPCHandler } from '@orpc/server/fetch'
import { createFileRoute } from '@tanstack/react-router'
import { onError } from '@orpc/server'

const handler = new RPCHandler(router, {
  interceptors: [
    onError((error) => {
      console.error(error)
    }),
  ],
})

export const Route = createFileRoute('/api/rpc/$')({
  server: {
    handlers: {
      ANY: async ({ request }) => {
        const { response } = await handler.handle(request, {
          prefix: '/api/rpc',
          context: {},
        })

        return response ?? new Response('Not Found', { status: 404 })
      },
    },
  },
})
```

> The `handler` can be any supported oRPC handler (`RPCHandler`, `OpenAPIHandler`, or custom).

## Client

Use `createIsomorphicFn` to configure the RPC link for both browser and SSR environments:

```ts
import { RPCLink } from '@orpc/client/fetch'
import { createIsomorphicFn } from '@tanstack/react-start'
import { getRequestHeaders } from '@tanstack/react-start/server'

const getClientLink = createIsomorphicFn()
  .client(() => new RPCLink({
    url: `${window.location.origin}/api/rpc`,
  }))
  .server(() => new RPCLink({
    url: 'http://localhost:3000/api/rpc',
    headers: () => getRequestHeaders(),
  }))
```

## Optimize SSR

Use a [Server-Side Client](/docs/client/server-side) during SSR to reduce HTTP requests:

```ts
// src/lib/orpc.ts
import { createRouterClient } from '@orpc/server'
import type { RouterClient } from '@orpc/server'
import { createORPCClient } from '@orpc/client'
import { RPCLink } from '@orpc/client/fetch'
import { getRequestHeaders } from '@tanstack/react-start/server'
import { createIsomorphicFn } from '@tanstack/react-start'

const getORPCClient = createIsomorphicFn()
  .server(() => createRouterClient(router, {
    context: async () => ({
      headers: getRequestHeaders(),
    }),
  }))
  .client((): RouterClient<typeof router> => {
    const link = new RPCLink({
      url: `${window.location.origin}/api/rpc`,
    })
    return createORPCClient(link)
  })

export const client: RouterClient<typeof router> = getORPCClient()
```
