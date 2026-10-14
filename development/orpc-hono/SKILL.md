---
name: oRPC Hono Adapter
description: Use oRPC inside a Hono project.
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# Hono Adapter

[Hono](https://honojs.dev/) is a high-performance web framework built on Fetch API.

## Basic

```ts
import { Hono } from 'hono'
import { RPCHandler } from '@orpc/server/fetch'
import { onError } from '@orpc/server'

const app = new Hono()

const handler = new RPCHandler(router, {
  interceptors: [onError(e => console.error(e))],
})

app.use('/rpc/*', async (c, next) => {
  const { matched, response } = await handler.handle(c.req.raw, {
    prefix: '/rpc',
    context: {}
  })

  if (matched) {
    return c.newResponse(response.body, response)
  }

  await next()
})

export default app
```

## Body Already Used Error?

If Hono middleware reads the body before oRPC, use a proxy:

```ts
const BODY_PARSER_METHODS = new Set(['arrayBuffer', 'blob', 'formData', 'json', 'text'] as const)

app.use('/rpc/*', async (c, next) => {
  const request = new Proxy(c.req.raw, {
    get(target, prop) {
      if (BODY_PARSER_METHODS.has(prop as any)) {
        return () => c.req[prop as any]()
      }
      return Reflect.get(target, prop, target)
    }
  })

  const { matched, response } = await handler.handle(request, {
    prefix: '/rpc',
    context: {}
  })

  if (matched) return c.newResponse(response.body, response)
  await next()
})
```

> The `handler` can be any supported oRPC handler.
