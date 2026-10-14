---
name: oRPC Body Limit Plugin
description: A plugin for oRPC to limit the request body size.
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# Body Limit Plugin

The **Body Limit Plugin** restricts the size of the request body.

## Import

```ts
import { BodyLimitPlugin } from '@orpc/server/fetch'
import { BodyLimitPlugin } from '@orpc/server/node'
```

## Setup

```ts
const handler = new RPCHandler(router, {
  plugins: [
    new BodyLimitPlugin({
      maxBodySize: 1024 * 1024, // 1MB
    }),
  ],
})
```

> The `handler` can be any supported oRPC handler — `RPCHandler`, `OpenAPIHandler`, or a custom handler.
