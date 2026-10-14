---
name: oRPC Retry After Plugin
description: Automatically retries requests based on server Retry-After headers.
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# Retry After Plugin

Automatically retries requests based on server `Retry-After` headers. Useful for handling rate limiting and temporary server unavailability.

## Usage

```ts
import { RetryAfterPlugin } from '@orpc/client/plugins'

const link = new RPCLink({
  url: 'http://localhost:3000/rpc',
  plugins: [
    new RetryAfterPlugin({
      condition: (response, options) => {
        return response.status === 429 || response.status === 503
      },
      maxAttempts: 5,
      timeout: 5 * 60 * 1000,
    }),
  ],
})
```

## Options

* `condition`: Whether a request should be retried. Defaults to `429` and `503` status codes.
* `maxAttempts`: Maximum retry attempts (default `3`).
* `timeout`: Maximum retry duration in ms (default `5 * 60 * 1000`).
