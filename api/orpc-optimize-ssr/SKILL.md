---
name: oRPC Optimize SSR
description: Optimize SSR for fullstack frameworks by avoiding unnecessary HTTP self-calls.
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# Optimize Server-Side Rendering (SSR) for Fullstack Frameworks

Optimize SSR with oRPC to eliminate redundant network calls during server rendering.

## The Problem

Standard SSR involves the server making HTTP requests back to its own API endpoints, adding latency.

## Conceptual approach

```ts
// Use this for server-side calls
const orpc = createRouterClient(router)

// Fallback to this for client-side calls
const orpc: RouterClient<typeof router> = createORPCClient(someLink)
```

A naive `typeof window === 'undefined'` check exposes your router logic to the client. Use `globalThis` to share the server client without bundling into client code.

## Implementation

```ts
// lib/orpc.ts
import type { RouterClient } from '@orpc/server'
import { RPCLink } from '@orpc/client/fetch'
import { createORPCClient } from '@orpc/client'

declare global {
  var $client: RouterClient<typeof router> | undefined
}

const link = new RPCLink({
  url: () => {
    if (typeof window === 'undefined') {
      throw new Error('RPCLink is not allowed on the server side.')
    }
    return `${window.location.origin}/rpc`
  },
})

export const client: RouterClient<typeof router> = globalThis.$client ?? createORPCClient(link)
```

```ts
// lib/orpc.server.ts
import 'server-only'
import { createRouterClient } from '@orpc/server'

globalThis.$client = createRouterClient(router, {
  context: async () => ({
    headers: await headers(),
  }),
})
```

## OpenAPILink support

```ts
// lib/orpc.server.ts
import { createJsonifiedRouterClient } from '@orpc/openapi'

globalThis.$client = createJsonifiedRouterClient(router, {
  context: async () => ({ headers: await headers() }),
})
```

## Ensure `orpc.server.ts` is imported first

```ts
// instrumentation.ts (Next.js)
export async function register() {
  await import('./lib/orpc.server')
}
```

```ts
// app/layout.tsx
import '../lib/orpc.server'
```

## Alternative Approach (Fetch-based)

```ts
// lib/orpc.server.ts
import 'server-only'
import { createORPCClient } from '@orpc/client'
import { RPCLink } from '@orpc/client/fetch'
import { handler } from '@/app/rpc/[[...rest]]/route'

const link = new RPCLink({
  url: 'http://placeholder',
  method: inferRPCMethodFromRouter(router),
  plugins: [
    new DedupeRequestsPlugin({
      groups: [{ condition: () => true, context: {} }],
    }),
  ],
  fetch: async (request) => {
    const { response } = await handler.handle(request, {
      context: { headers: await headers() },
    })
    return response ?? new Response('Not Found', { status: 404 })
  },
})

globalThis.$client = createORPCClient<RouterClient<typeof router>>(link)
```

## Using the Client

```tsx
export default async function PlanetListPage() {
  const planets = await client.planet.list({ limit: 10 })

  return (
    <div>
      {planets.map(planet => (
        <div key={planet.id}>{planet.name}</div>
      ))}
    </div>
  )
}
```

## TanStack Query

```tsx
export default function PlanetListPage() {
  const { data: planets } = useSuspenseQuery(
    orpc.planet.list.queryOptions({
      input: { limit: 10 },
    }),
  )

  return (
    <div>
      {planets.map(planet => <div key={planet.id}>{planet.name}</div>)}
    </div>
  )
}
```
