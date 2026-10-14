---
name: oRPC Rethrow Handler Plugin
description: Catch and rethrow specific errors during request handling.
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# Rethrow Handler Plugin

The `RethrowHandlerPlugin` lets you catch and rethrow specific errors during request handling. Useful when your framework has its own error handling mechanism (e.g., global exception filters in NestJS, error middleware in Express).

## Usage

```ts
import { ORPCError } from '@orpc/server'
import { RPCHandler } from '@orpc/server/fetch'
import {
  experimental_RethrowHandlerPlugin as RethrowHandlerPlugin,
} from '@orpc/server/plugins'

const handler = new RPCHandler(router, {
  plugins: [
    new RethrowHandlerPlugin({
      filter: (error) => {
        // Rethrow all non-ORPCError errors
        return !(error instanceof ORPCError)
      },
    }),
  ],
})
```

> The `handler` can be any supported oRPC handler.
