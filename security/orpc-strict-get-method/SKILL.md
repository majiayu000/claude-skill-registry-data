---
name: oRPC Strict GET Method Plugin
description: Only procedures explicitly accepting GET can be called via HTTP GET (CSRF protection).
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# Strict GET Method Plugin

Enhances security by ensuring only procedures explicitly marked to accept `GET` requests can be called using HTTP `GET` for [RPC Protocol](/docs/advanced/rpc-protocol). Helps prevent certain CSRF attacks.

## When to Use

Beneficial if your application stores sensitive data (session/auth tokens) in cookies with `SameSite=Lax` or `SameSite=None`.

> Enabled by default for HTTP Adapter. You may switch to [Simple CSRF Protection](/docs/plugins/simple-csrf-protection) or disable entirely.

## How it works

Only procedures configured with `method: 'GET'` can be invoked via GET requests:

```ts
import { os } from '@orpc/server'

const ping = os
  .route({ method: 'GET' })
  .handler(() => 'pong')
```

## Setup

```ts
import { StrictGetMethodPlugin } from '@orpc/server/plugins'

const handler = new RPCHandler(router, {
  plugins: [
    new StrictGetMethodPlugin()
  ],
})
```
