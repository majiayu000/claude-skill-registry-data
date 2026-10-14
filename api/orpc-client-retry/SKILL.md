---
name: oRPC Client Retry Plugin
description: A plugin for oRPC that enables retrying client calls when errors occur.
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# Client Retry Plugin

The `Client Retry Plugin` enables retrying client calls when errors occur.

## Setup

```ts
import { RPCLink } from '@orpc/client/fetch'
import { ClientRetryPlugin, ClientRetryPluginContext } from '@orpc/client/plugins'

interface ORPCClientContext extends ClientRetryPluginContext {}

const link = new RPCLink<ORPCClientContext>({
  url: 'http://localhost:3000/rpc',
  plugins: [
    new ClientRetryPlugin({
      default: {
        retry: ({ path }) => {
          if (path.join('.') === 'planet.list') return 2
          return 0
        }
      },
    }),
  ],
})

const client: RouterClient<typeof router, ORPCClientContext> = createORPCClient(link)
```

> The `link` can be any oRPC link — `RPCLink`, `OpenAPILink`, or custom implementations.

## Usage

```ts
const planets = await client.planet.list({ limit: 10 }, {
  context: {
    retry: 3, // Maximum retry attempts
    retryDelay: 2000, // Delay between retries in ms
    shouldRetry: options => true, // Decide whether to retry
    onRetry: (options) => {
      // Hook executed on each retry
      return (isSuccess) => {
        // Execute after the retry is complete
      }
    },
  }
})
```

Defaults:
- `retry`: `0` (disabled unless explicitly set)
- `retryDelay`: `(o) => o.lastEventRetry ?? 2000`
- `shouldRetry`: `true`

## Event Iterator (SSE)

Replicate [EventSource](https://developer.mozilla.org/en-US/docs/Web/API/EventSource) behavior:

```ts
const streaming = await client.streaming('the input', {
  context: { retry: Number.POSITIVE_INFINITY }
})

for await (const message of streaming) {
  console.log(message)
}
```
