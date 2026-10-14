---
name: oRPC Astro Adapter
description: Use oRPC inside an Astro project.
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# Astro Adapter

[Astro](https://astro.build/) is a JavaScript web framework optimized for fast, content-driven websites. For HTTP context, see the [HTTP Adapter](/docs/adapters/http) guide.

## Basic

```ts
// pages/rpc/[...rest].ts
import { RPCHandler } from '@orpc/server/fetch'
import { onError } from '@orpc/server'

const handler = new RPCHandler(router, {
  interceptors: [
    onError((error) => {
      console.error(error)
    }),
  ],
})

export const prerender = false

export const ALL: APIRoute = async ({ request }) => {
  const { response } = await handler.handle(request, {
    prefix: '/rpc',
    context: {},
  })

  return response ?? new Response('Not found', { status: 404 })
}
```

> The `handler` can be any supported oRPC handler — `RPCHandler`, `OpenAPIHandler`, or a custom handler.
