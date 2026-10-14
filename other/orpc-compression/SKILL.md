---
name: oRPC Compression Plugin
description: A plugin for oRPC that compresses response bodies to reduce bandwidth usage.
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# Compression Plugin

The **Compression Plugin** compresses response bodies to reduce bandwidth usage and improve performance.

## Import

```ts
import { CompressionPlugin } from '@orpc/server/node'
import { CompressionPlugin } from '@orpc/server/fetch'
```

## Setup

```ts
const handler = new RPCHandler(router, {
  plugins: [new CompressionPlugin()],
})
```

> The `handler` can be any supported oRPC handler — `RPCHandler`, `OpenAPIHandler`, or a custom handler.
