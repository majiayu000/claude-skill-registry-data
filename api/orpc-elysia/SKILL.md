---
name: oRPC Elysia Adapter
description: Use oRPC inside an Elysia project.
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# Elysia Adapter

[Elysia](https://elysiajs.com/) is a high-performance Bun web framework following the Fetch API.

## Basic

```ts
import { Elysia } from 'elysia'
import { RPCHandler } from '@orpc/server/fetch'
import { onError } from '@orpc/server'

const handler = new RPCHandler(router, {
  interceptors: [onError(e => console.error(e))],
})

const app = new Elysia()
  .all('/rpc*', async ({ request }: { request: Request }) => {
    const { response } = await handler.handle(request, { prefix: '/rpc' })
    return response ?? new Response('Not Found', { status: 404 })
  }, {
    parse: 'none' // Disable Elysia body parser to prevent "body already used" error
  })
  .listen(3000)
```

> The `handler` can be any supported oRPC handler — `RPCHandler`, `OpenAPIHandler`, or a custom handler.
