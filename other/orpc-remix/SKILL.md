---
name: oRPC Remix Adapter
description: Use oRPC inside a Remix project.
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# Remix Adapter

[Remix](https://remix.run/) is a full stack JavaScript framework.

## Basic

```ts
// app/routes/rpc.$.ts
import { RPCHandler } from '@orpc/server/fetch'
import { onError } from '@orpc/server'

const handler = new RPCHandler(router, {
  interceptors: [onError(e => console.error(e))],
})

export async function loader({ request }: LoaderFunctionArgs) {
  const { response } = await handler.handle(request, {
    prefix: '/rpc',
    context: {}
  })

  return response ?? new Response('Not Found', { status: 404 })
}
```

> The `handler` can be any supported oRPC handler.
