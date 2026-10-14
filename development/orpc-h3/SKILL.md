---
name: oRPC H3 Adapter
description: Use oRPC inside an H3 project.
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# H3 Adapter

[H3](https://h3.dev/) is a universal, tiny, and fast web framework built on top of web standards.

## Basic

```ts
import { H3, serve } from 'h3'
import { RPCHandler } from '@orpc/server/fetch'
import { onError } from '@orpc/server'

const app = new H3()

const handler = new RPCHandler(router, {
  interceptors: [onError(e => console.error(e))],
})

app.use('/rpc/**', async (event) => {
  const { matched, response } = await handler.handle(event.req, {
    prefix: '/rpc',
    context: {}
  })

  if (matched) return response
})

serve(app, { port: 3000 })
```

> The `handler` can be any supported oRPC handler.
