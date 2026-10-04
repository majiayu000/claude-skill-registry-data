---
name: data-fetching
description: |
  Data fetching patterns for Next.js App Router — Server Components, Server Actions,
  React Query, and streaming. Use when implementing or reviewing data fetching logic,
  choosing between RSC and client-side fetching, or designing API routes.
trigger: 需要实现数据获取逻辑
input: 数据需求
output: 数据获取代码
next: 无
dependencies: 无
---

# Data Fetching (Next.js)

Canonical patterns for fetching data in Next.js App Router.

## Fetch Strategy Decision

```
Need data for a page / route?
├─ Data is public / user-agnostic?
│   ├─ Static (rarely changes) → Server Component + fetch() with { cache: 'force-cache' }
│   ├─ Dynamic (per-request)   → Server Component + fetch() (default dynamic)
│   └─ Revalidating            → Server Component + fetch() with { next: { revalidate: N } }
├─ Data is user-specific?
│   └─ Server Component + cookies()/headers() (auto-deduped, secure)
├─ Need real-time / polling?
│   └─ Client Component + React Query / SWR
└─ Need user-initiated mutation?
    └─ Server Action (form action / event handler)
```

## Patterns

### 1. Server Component Data Fetching (Preferred)

```tsx
// app/posts/page.tsx — Server Component, fetch runs on server, zero client JS
export default async function PostsPage() {
  const posts = await fetch('https://api.example.com/posts', {
    next: { revalidate: 60 }  // ISR: revalidate every 60s
  }).then(r => r.json())

  return <PostList posts={posts} />
}
```

### 2. Parallel Data Fetching

```tsx
export default async function Dashboard() {
  // Parallel — both fetches start at the same time
  const [user, analytics] = await Promise.all([
    getUser(),
    getAnalytics()
  ])

  return <DashboardView user={user} analytics={analytics} />
}
```

### 3. Streaming with Suspense

```tsx
import { Suspense } from 'react'

export default function Page() {
  return (
    <div>
      <Header />              {/* Shown instantly */}
      <Suspense fallback={<Skeleton />}>
        <SlowDataComponent />  {/* Streamed in when ready */}
      </Suspense>
    </div>
  )
}
```

### 4. Server Actions (Mutations)

```tsx
'use server'

export async function createPost(formData: FormData) {
  const title = formData.get('title')
  await db.post.create({ title })
  revalidatePath('/posts')  // Revalidate the cache
}
```

### 5. Client-Side React Query (Real-time / Polling)

When Server Components aren't enough (polling, real-time, window-focus refetch):
- Use React Query / TanStack Query
- Keep the fetch logic in a custom hook
- Use `initialData` from Server Components to hydrate

## Anti-Patterns

| Anti-Pattern | Why | Fix |
|-------------|-----|-----|
| Fetching in `useEffect` for initial page data | Wastes server capability, hurts UX | Use Server Component fetching |
| Sequential fetches in Server Components | Doubles load time | Use `Promise.all()` |
| Mixing server/client fetch for the same data | Redundant network calls | Fetch once in Server, pass down |
| Over-fetching in RSC | Large bundle from serialized data | Only pass what the client needs |
| `useEffect` + fetch for mutations | No built-in loading/error states | Use Server Actions + `useActionState` |

## Checklist

- [ ] Could this fetch happen in a Server Component? (prefer it)
- [ ] Are parallel fetches batched with `Promise.all`?
- [ ] Is the revalidation strategy correct? (time-based / on-demand / no cache)
- [ ] Are loading states handled via `loading.tsx` or Suspense?
- [ ] Are error states handled via `error.tsx`?
- [ ] Are Server Actions used for mutations (not API routes)?
- [ ] Is sensitive data only fetched server-side, never exposed to client JS?