---
name: start-patterns
description: Implements TanStack Start full-stack React framework features including server functions (createServerFn), SSR streaming, middleware, client-server data synchronization, and edge deployment presets.
version: 1.0.0
---

# TanStack Start Full-Stack Patterns

Patterns for building full-stack SSR and streaming React applications using **TanStack Start** (powered by TanStack Router).

## 1. Architecture Overview

TanStack Start turns TanStack Router into a full-stack framework with:
- **Server Functions (`createServerFn`)**: Type-safe RPC between client and server without manual fetch endpoints.
- **SSR & Streaming**: Instant HTML shells with streamed data loaders.
- **Nitro Engine Deployment**: Deploy to Cloudflare Workers, Vercel, Node, Bun, or Netlify with zero code changes.

```
app/
├── routes/
│   ├── __root.tsx         # HTML document shell (Head, Scripts, Outlet)
│   ├── index.tsx          # Home page
│   └── posts.$id.tsx      # Loader with server function
├── router.tsx             # Router factory for SSR hydration
├── client.tsx             # Client hydration entrypoint
└── ssr.tsx                # Server rendering entrypoint
```

---

## 2. Server Functions (`createServerFn`)

Server functions run purely on the server and are callable directly from loaders, mutations, or React components:

```typescript
// app/features/users/server.ts
import { createServerFn } from '@tanstack/start'
import { z } from 'zod'
import { db } from '@/server/db'

export const getUserServerFn = createServerFn({ method: 'GET' })
  .validator((id: string) => z.string().uuid().parse(id))
  .handler(async ({ data: id }) => {
    const user = await db.user.findUnique({ where: { id } })
    if (!user) throw new Error('User not found')
    return user
  })

export const updateUserNameServerFn = createServerFn({ method: 'POST' })
  .validator((payload: { id: string; name: string }) =>
    z.object({ id: z.string(), name: z.string().min(2) }).parse(payload)
  )
  .handler(async ({ data }) => {
    return await db.user.update({
      where: { id: data.id },
      data: { name: data.name },
    })
  })
```

---

## 3. Route Loader Integration

Call server functions seamlessly inside route loaders:

```typescript
// app/routes/users.$userId.tsx
import { createFileRoute } from '@tanstack/react-router'
import { getUserServerFn } from '@/features/users/server'

export const Route = createFileRoute('/users/$userId')({
  loader: async ({ params }) => {
    return await getUserServerFn({ data: params.userId })
  },
  component: UserProfilePage,
})

function UserProfilePage() {
  const user = Route.useLoaderData()
  return <div><h1>{user.name}</h1></div>
}
```

---

## 4. Middleware & Context (Auth, Session)

```typescript
import { createMiddleware } from '@tanstack/start'
import { getSession } from '@/server/auth'

export const authMiddleware = createMiddleware().server(async ({ next }) => {
  const session = await getSession()
  if (!session) throw new Error('Unauthorized')
  return next({ context: { session } })
})

export const getProtectedData = createServerFn({ method: 'GET' })
  .middleware([authMiddleware])
  .handler(async ({ context }) => {
    return { userId: context.session.user.id }
  })
```
