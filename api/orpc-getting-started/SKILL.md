---
name: oRPC Getting Started
description: Quick guide to oRPC — define procedures, handle errors, integrate with popular frameworks.
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# Getting Started

oRPC (OpenAPI Remote Procedure Call) combines RPC with OpenAPI, allowing type-safe API definition and consumption.

## Prerequisites

* Node.js 18+ (20+ recommended) | Bun | Deno | Cloudflare Workers
* A package manager (npm/pnpm/yarn/bun/deno)
* A TypeScript project (strict mode recommended)

## Installation

```sh
npm install @orpc/server@latest @orpc/client@latest
```

## Define App Router

```ts
import type { IncomingHttpHeaders } from 'node:http'
import { ORPCError, os } from '@orpc/server'
import * as z from 'zod'

const PlanetSchema = z.object({
  id: z.number().int().min(1),
  name: z.string(),
  description: z.string().optional(),
})

export const listPlanet = os
  .input(z.object({
    limit: z.number().int().min(1).max(100).optional(),
    cursor: z.number().int().min(0).default(0),
  }))
  .handler(async ({ input }) => {
    return [{ id: 1, name: 'name' }]
  })

export const findPlanet = os
  .input(PlanetSchema.pick({ id: true }))
  .handler(async ({ input }) => {
    return { id: 1, name: 'name' }
  })

export const createPlanet = os
  .$context<{ headers: IncomingHttpHeaders }>()
  .use(({ context, next }) => {
    const user = parseJWT(context.headers.authorization?.split(' ')[1])
    if (user) return next({ context: { user } })
    throw new ORPCError('UNAUTHORIZED')
  })
  .input(PlanetSchema.omit({ id: true }))
  .handler(async ({ input, context }) => {
    return { id: 1, name: 'name' }
  })

export const router = {
  planet: {
    list: listPlanet,
    find: findPlanet,
    create: createPlanet
  }
}
```

## Create Server (Node.js)

```ts
import { createServer } from 'node:http'
import { RPCHandler } from '@orpc/server/node'
import { CORSPlugin } from '@orpc/server/plugins'
import { onError } from '@orpc/server'

const handler = new RPCHandler(router, {
  plugins: [new CORSPlugin()],
  interceptors: [onError(e => console.error(e))],
})

const server = createServer(async (req, res) => {
  const result = await handler.handle(req, res, {
    context: { headers: req.headers }
  })

  if (!result.matched) {
    res.statusCode = 404
    res.end('No procedure matched')
  }
})

server.listen(3000, '127.0.0.1', () => console.log('Listening'))
```

## Create Client

```ts
import type { RouterClient } from '@orpc/server'
import { createORPCClient } from '@orpc/client'
import { RPCLink } from '@orpc/client/fetch'

const link = new RPCLink({
  url: 'http://127.0.0.1:3000',
  headers: { Authorization: 'Bearer token' },
})

export const orpc: RouterClient<typeof router> = createORPCClient(link)
```

## Call Procedure

```ts
const planet = await orpc.planet.find({ id: 1 })
```

## Next Steps

For OpenAPI integration, see [OpenAPI Getting Started](/docs/openapi/getting-started).
