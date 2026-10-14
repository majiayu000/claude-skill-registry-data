---
name: oRPC Nuxt.js Adapter
description: Use oRPC inside a Nuxt.js project.
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# Nuxt.js Adapter

[Nuxt.js](https://nuxt.com/) integration.

## Server

```ts
// server/routes/rpc/[...].ts
import { RPCHandler } from '@orpc/server/fetch'
import { onError } from '@orpc/server'

const handler = new RPCHandler(router, {
  interceptors: [onError(e => console.error(e))],
})

export default defineEventHandler(async (event) => {
  const request = toWebRequest(event)
  const { response } = await handler.handle(request, {
    prefix: '/rpc',
    context: {},
  })

  if (response) return response

  setResponseStatus(event, 404, 'Not Found')
  return 'Not found'
})
```

```ts
// server/routes/rpc/index.ts
export { default } from './[...]'
```

## Client

Set up in a [Nuxt Plugin](https://nuxt.com/docs/guide/directory-structure/plugins) for SSR compatibility:

```ts
// app/plugins/orpc.ts
export default defineNuxtPlugin(() => {
  const event = useRequestEvent()

  const link = new RPCLink({
    url: `${typeof window !== 'undefined' ? window.location.origin : 'http://localhost:3000'}/rpc`,
    headers: event?.headers,
  })

  const client: RouterClient<typeof router> = createORPCClient(link)

  return { provide: { client } }
})
```

## Optimize SSR

```ts
// app/plugins/orpc.client.ts
export default defineNuxtPlugin(() => {
  const link = new RPCLink({
    url: `${window.location.origin}/rpc`,
    headers: () => ({}),
  })

  const client: RouterClient<typeof router> = createORPCClient(link)

  return { provide: { client } }
})
```

```ts
// app/plugins/orpc.server.ts
export default defineNuxtPlugin((nuxt) => {
  const event = useRequestEvent()

  const client = createRouterClient(router, {
    context: { headers: event?.headers },
  })

  return { provide: { client } }
})
```
