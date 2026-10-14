---
name: oRPC Fastify Adapter
description: Use oRPC inside a Fastify project.
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# Fastify Adapter

[Fastify](https://fastify.dev/) integration.

> Fastify parses common request content types by default. oRPC will use the parsed body when available.

## Basic

```ts
import Fastify from 'fastify'
import { RPCHandler } from '@orpc/server/fastify'
import { onError } from '@orpc/server'

const rpcHandler = new RPCHandler(router, {
  interceptors: [onError(e => console.error(e))],
})

const fastify = Fastify()

fastify.addContentTypeParser('*', (request, payload, done) => {
  // Allow any content type, let oRPC parse manually
  done(null, undefined)
})

fastify.all('/rpc/*', async (req, reply) => {
  const { matched } = await rpcHandler.handle(req, reply, {
    prefix: '/rpc',
    context: {}
  })

  if (!matched) {
    reply.status(404).send('Not found')
  }
})

fastify.listen({ port: 3000 }).then(() => console.log('Server running on http://localhost:3000'))
```

> The `handler` can be any supported oRPC handler — `RPCHandler`, `OpenAPIHandler`, or a custom handler.
