---
name: oRPC OpenAPI Handler
description: Comprehensive Guide to the OpenAPIHandler in oRPC.
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# OpenAPI Handler

`OpenAPIHandler` enables communication with clients over RESTful APIs adhering to the OpenAPI specification.

## Supported Data Types

* **string**, **number** (`NaN` → `null`), **boolean**, **null**
* **undefined** (`undefined` in arrays → `null`)
* **Date** (`Invalid Date` → `null`)
* **BigInt** → `string`, **RegExp** → `string`, **URL** → `string`
* **Record (object)**, **Array**
* **Set** → `array`, **Map** → `array`
* **Blob**, **File** (unsupported in `AsyncIteratorObject`)
* **AsyncIteratorObject** (only at root; powers [Event Iterator](/docs/event-iterator))
* **ReadableStream\<Uint8Array>** (root level only)

> If payload contains `Blob` or `File` outside root, it must use `multipart/form-data` and apply [Bracket Notation](/docs/openapi/bracket-notation).

## Installation

```sh
npm install @orpc/openapi@latest
```

## Setup

```ts
import { OpenAPIHandler } from '@orpc/openapi/fetch'
import { CORSPlugin } from '@orpc/server/plugins'
import { onError } from '@orpc/server'

const handler = new OpenAPIHandler(router, {
  plugins: [new CORSPlugin()],
  interceptors: [onError(e => console.error(e))],
})

export default async function fetch(request: Request) {
  const { matched, response } = await handler.handle(request, {
    prefix: '/api',
    context: {}
  })

  if (matched) return response
  return new Response('Not Found', { status: 404 })
}
```

## Filtering Procedures

```ts
const handler = new OpenAPIHandler(router, {
  filter: ({ contract, path }) => !contract['~orpc'].route.tags?.includes('internal'),
})
```

## Lifecycle

Follows the same lifecycle as [RPCHandler Lifecycle](/docs/rpc-handler#lifecycle).
