---
name: oRPC OpenAPILink
description: Use OpenAPILink in oRPC clients to communicate with OpenAPI-compliant APIs.
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# OpenAPILink

Enables communication with an [OpenAPIHandler](/docs/openapi/openapi-handler) or any API following the [OpenAPI Specification](https://swagger.io/specification/) using HTTP/Fetch.

## Installation

```sh
npm install @orpc/openapi-client@latest
```

## Setup

```ts
import type { JsonifiedClient } from '@orpc/openapi-client'
import type { ContractRouterClient } from '@orpc/contract'
import { createORPCClient, onError } from '@orpc/client'
import { OpenAPILink } from '@orpc/openapi-client/fetch'

const link = new OpenAPILink(contract, {
  url: 'http://localhost:3000/api',
  headers: () => ({ 'x-api-key': 'my-api-key' }),
  fetch: (request, init) => {
    return globalThis.fetch(request, {
      ...init,
      credentials: 'include',
    })
  },
  interceptors: [onError(e => console.error(e))],
})

const client: JsonifiedClient<ContractRouterClient<typeof contract>> = createORPCClient(link)
```

> Due to JSON limitations, wrap your client with `JsonifiedClient`. Alternatively, see [Expanding Type Support for OpenAPI Link](/docs/openapi/advanced/expanding-type-support-for-openapi-link).

## Limitations

* Payloads with `Blob`/`File` outside root use `multipart/form-data` and [Bracket Notation](/docs/openapi/bracket-notation).
* For `GET` requests, payload sent as `URLSearchParams` with [Bracket Notation](/docs/openapi/bracket-notation).

## CORS policy

Needs `Content-Disposition` header to distinguish file responses:

```ts
const handler = new OpenAPIHandler(router, {
  plugins: [
    new CORSPlugin({
      exposeHeaders: ['Content-Disposition'],
    }),
  ],
})
```

## Using Client Context

```ts
interface ClientContext { something?: string }

const link = new OpenAPILink<ClientContext>(contract, {
  url: 'http://localhost:3000/api',
  headers: async ({ context }) => ({
    'x-api-key': context?.something ?? ''
  })
})

const client: JsonifiedClient<ContractRouterClient<typeof contract, ClientContext>> = createORPCClient(link)

const result = await client.planet.list(
  { limit: 10 },
  { context: { something: 'value' } }
)
```

## Lazy URL

```ts
const link = new OpenAPILink({
  url: () => {
    if (typeof window === 'undefined') {
      throw new Error('Not allowed on server')
    }
    return `${window.location.origin}/api`
  },
})
```

## Lifecycle

Follows the same lifecycle as [RPCLink Lifecycle](/docs/client/rpc-link#lifecycle).
