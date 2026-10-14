---
name: oRPC Dedupe Requests Plugin
description: Prevents duplicate requests by deduplicating similar ones to reduce server load.
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# Dedupe Requests Plugin

Prevents redundant requests by deduplicating similar ones.

## Usage

```ts
import { DedupeRequestsPlugin } from '@orpc/client/plugins'

const link = new RPCLink({
  plugins: [
    new DedupeRequestsPlugin({
      filter: ({ request }) => request.method === 'GET',
      groups: [
        { condition: () => true, context: {} },
      ],
    }),
  ],
})
```

> By default, only `GET` requests are deduplicated.

## Groups

A request must match at least one group. Requests in the same group are deduplicated together.

Example: dedupe based on cache control:

```ts
interface ClientContext { cache?: RequestCache }

const link = new RPCLink<ClientContext>({
  url: 'http://localhost:3000/rpc',
  method: ({ context }) => context?.cache ? 'GET' : 'POST',
  plugins: [
    new DedupeRequestsPlugin({
      filter: ({ request }) => request.method === 'GET',
      groups: [
        {
          condition: ({ context }) => context?.cache === 'force-cache',
          context: { cache: 'force-cache' },
        },
        { condition: () => true, context: {} },
      ],
    }),
  ],
  fetch: (request, init, { context }) => globalThis.fetch(request, {
    ...init,
    cache: context?.cache,
  }),
})
```
