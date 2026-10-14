---
name: oRPC Batch Requests Plugin
description: A plugin for oRPC to batch requests and responses to reduce overhead.
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# Batch Requests Plugin

The **Batch Requests Plugin** combines multiple requests and responses into a single batch, reducing overhead.

> HTTP/2, HTTP/3, and later versions support multiplexing natively, so this plugin may be less beneficial in modern setups.

## Server

```ts
import { BatchHandlerPlugin } from '@orpc/server/plugins'

const handler = new RPCHandler(router, {
  plugins: [new BatchHandlerPlugin()],
})
```

## Client

Requests within the same group will be considered for batching together.

```ts
import { BatchLinkPlugin } from '@orpc/client/plugins'

const link = new RPCLink({
  url: 'https://api.example.com/rpc',
  plugins: [
    new BatchLinkPlugin({
      groups: [
        { condition: () => true, context: {} }
      ]
    }),
  ],
})
```

## Batch Mode

Default `streaming` mode sends responses asynchronously. Switch to `buffered` mode for environments without streaming support:

```ts
new BatchLinkPlugin({
  mode: typeof window === 'undefined' ? 'buffered' : 'streaming',
  groups: [{ condition: () => true, context: {} }]
})
```

## Limitations

Does not support `AsyncIteratorObject` or `File`/`Blob` in responses. Use `exclude` to skip unsupported procedures:

```ts
new BatchLinkPlugin({
  groups: [{ condition: () => true, context: {} }],
  exclude: ({ path }) => ['planets/getImage', 'planets/subscribe'].includes(path.join('/'))
})
```

## Custom Headers

```ts
new BatchLinkPlugin({
  groups: [{ condition: () => true, context: {} }],
  headers: () => ({ authorization: 'Bearer 1234567890' })
})
```

## Groups by Cache Control Example

```ts
const link = new RPCLink<ClientContext>({
  url: 'http://localhost:3000/rpc',
  method: ({ context }) => context?.cache ? 'GET' : 'POST',
  plugins: [
    new BatchLinkPlugin({
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
