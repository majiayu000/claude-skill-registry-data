---
name: oRPC Response Headers Plugin
description: Set response headers in oRPC.
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# Response Headers Plugin

Injects a `resHeaders` instance into the `context`, enabling you to modify response headers.

## Context Setup

```ts
import { setCookie } from '@orpc/server/helpers'
import { ResponseHeadersPluginContext } from '@orpc/server/plugins'

interface ORPCContext extends ResponseHeadersPluginContext {}

const base = os.$context<ORPCContext>()

const example = base
  .use(({ context, next }) => {
    context.resHeaders?.set('x-custom-header', 'value')
    return next()
  })
  .handler(({ context }) => {
    setCookie(context.resHeaders, 'session_id', 'abc123', {
      secure: true,
      maxAge: 3600
    })
  })
```

> `resHeaders` can be `undefined` to allow procedures to run safely without the plugin (e.g., direct calls).

> Combine with [Cookie Helpers](/docs/helpers/cookie) for streamlined cookie management.

## Handler Setup

```ts
import { ResponseHeadersPlugin } from '@orpc/server/plugins'

const handler = new RPCHandler(router, {
  plugins: [new ResponseHeadersPlugin()],
})
```
