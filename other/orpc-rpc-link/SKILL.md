---
name: oRPC RPCLink
description: Use RPCLink in oRPC clients to communicate with RPCHandler.
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# RPCLink

Enables communication with [RPCHandler](/docs/rpc-handler) or any API following the [RPC Protocol](/docs/advanced/rpc-protocol) using HTTP/Fetch.

## Overview

```ts
import { onError } from '@orpc/client'
import { RPCLink } from '@orpc/client/fetch'

const link = new RPCLink({
  url: 'http://localhost:3000/rpc',
  headers: () => ({ 'x-api-key': 'my-api-key' }),
  fetch: (request, init) => {
    return globalThis.fetch(request, {
      ...init,
      credentials: 'include',
    })
  },
  interceptors: [onError(e => console.error(e))],
})

export const client: RouterClient<typeof router> = createORPCClient(link)
```

## Using Client Context

```ts
interface ClientContext { something?: string }

const link = new RPCLink<ClientContext>({
  url: 'http://localhost:3000/rpc',
  headers: async ({ context }) => ({
    'x-api-key': context?.something ?? ''
  })
})

const client: RouterClient<typeof router, ClientContext> = createORPCClient(link)

const result = await client.planet.list(
  { limit: 10 },
  { context: { something: 'value' } }
)
```

## Custom Request Method

```ts
interface ClientContext { cache?: RequestCache }

const link = new RPCLink<ClientContext>({
  url: 'http://localhost:3000/rpc',
  method: ({ context }, path) => {
    if (context?.cache) return 'GET'
    if (typeof window === 'undefined') return 'GET'
    if (path.at(-1)?.match(/^(?:get|find|list|search)(?:[A-Z].*)?$/)) return 'GET'
    return 'POST'
  },
  fetch: (request, init, { context }) => globalThis.fetch(request, {
    ...init,
    cache: context?.cache,
  }),
})
```

Use the contract method automatically:

```ts
import { inferRPCMethodFromContractRouter } from '@orpc/contract'

const link = new RPCLink({
  url: 'http://localhost:3000/rpc',
  method: inferRPCMethodFromContractRouter(contract),
})
```

## Lazy URL

```ts
const link = new RPCLink({
  url: () => {
    if (typeof window === 'undefined') {
      throw new Error('Not allowed on server')
    }
    return `${window.location.origin}/rpc`
  },
})
```

## Lifecycle

```mermaid
sequenceDiagram
  actor A1 as Client
  participant P1 as Input/Output/Error Encoder
  participant P2 as Client Sender
  participant P3 as Adapter

  A1 ->> P1: input, signal, lastEventId
  P1 ->> P1: encode request
  P1 ->> P2: standard request
  P2 ->> P3: adapter request
  P3 ->> P3: send
  P3 ->> P2: adapter response
  P2 ->> P1: standard response
  P1 ->> P1: decode response
  P1 ->> A1: error/output
```
