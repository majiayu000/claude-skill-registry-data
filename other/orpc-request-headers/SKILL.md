---
name: oRPC Request Headers Plugin
description: Access request headers in oRPC.
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# Request Headers Plugin

Injects a `reqHeaders` instance into the `context`, enabling you to read incoming request headers.

## Context Setup

```ts
import { getCookie } from '@orpc/server/helpers'
import { RequestHeadersPluginContext } from '@orpc/server/plugins'

interface ORPCContext extends RequestHeadersPluginContext {}

const base = os.$context<ORPCContext>()

const example = base
  .use(({ context, next }) => {
    const sessionId = getCookie(context.reqHeaders, 'session_id')
    return next()
  })
  .handler(({ context }) => {
    const userAgent = context.reqHeaders?.get('user-agent')
    return { userAgent }
  })
```

> `reqHeaders` can be `undefined` to allow procedures to run safely without `RequestHeadersPlugin`, such as in direct calls.

> Combine with [Cookie Helpers](/docs/helpers/cookie) for streamlined cookie management.

## Handler Setup

```ts
import { RequestHeadersPlugin } from '@orpc/server/plugins'

const handler = new RPCHandler(router, {
  plugins: [new RequestHeadersPlugin()],
})
```

> The `handler` can be any supported oRPC handler.
