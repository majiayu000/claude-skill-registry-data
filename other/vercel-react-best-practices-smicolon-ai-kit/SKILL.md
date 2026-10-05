---
name: vercel-react-best-practices
description: Official React and Next.js performance optimization guidelines from Vercel Engineering. Auto-activates when writing, reviewing, or refactoring React components, Next.js pages, data fetching, bundle optimization, or performance-critical frontend code.
version: 1.0.0
---

# Vercel React Best Practices

Comprehensive performance optimization guide for React and Next.js applications, maintained by Vercel Engineering. Contains rules across 8 categories, prioritized by impact to guide automated refactoring and code generation.

## Rule Categories by Priority

| Priority | Category | Impact | Prefix | Focus |
|:---|:---|:---|:---|:---|
| 1 | Eliminating Waterfalls | CRITICAL | `async-` | Parallel fetches, deferred awaits, Suspense streaming |
| 2 | Bundle Size Optimization | CRITICAL | `bundle-` | Direct imports over barrel files, dynamic imports, conditional loading |
| 3 | Server-Side Performance | HIGH | `server-` | React.cache(), non-blocking after(), data minimization |
| 4 | Client-Side Data Fetching | MEDIUM-HIGH | `client-` | SWR / TanStack Query, optimistic UI, caching |
| 5 | Re-render Optimization | MEDIUM | `rerender-` | Reference stability, context splitting, derived state |
| 6 | Rendering Performance | MEDIUM | `rendering-` | Virtualization, content-visibility, memoization |
| 7 | JavaScript Performance | LOW-MEDIUM | `js-` | Algorithmic efficiency, avoiding work in render |
| 8 | Advanced Patterns | LOW | `advanced-` | Islands, partial hydration, micro-optimizations |

---

## 1. Eliminating Waterfalls (CRITICAL)

### `async-defer-await`
Move `await` into the exact branches where the value is needed, not at the top of functions:
```typescript
// ❌ WRONG: Blocks execution even if user branch is never hit
async function handleRequest(userId?: string) {
  const user = userId ? await fetchUser(userId) : null
  if (!user) return redirect('/login')
  return renderProfile(user)
}

// ✅ CORRECT: Start early or await inside condition
async function handleRequest(userId?: string) {
  if (!userId) return redirect('/login')
  const user = await fetchUser(userId)
  return renderProfile(user)
}
```

### `async-parallel`
Use `Promise.all()` for independent asynchronous operations:
```typescript
// ❌ WRONG: Sequential waterfall (takes T1 + T2)
const user = await fetchUser(id)
const posts = await fetchPosts(id)

// ✅ CORRECT: Concurrent fetches (takes max(T1, T2))
const [user, posts] = await Promise.all([
  fetchUser(id),
  fetchPosts(id),
])
```

### `async-suspense-boundaries`
Stream slow components independently using React Suspense rather than awaiting data in parent layouts:
```tsx
// ✅ Stream heavy content without blocking the main shell
export default function Page() {
  return (
    <div>
      <Header />
      <Suspense fallback={<AnalyticsSkeleton />}>
        <SlowAnalyticsDashboard />
      </Suspense>
    </div>
  )
}
```

---

## 2. Bundle Size Optimization (CRITICAL)

### `bundle-barrel-imports`
Import directly from the module source; **avoid large barrel files** (`index.ts` re-exporting hundreds of icons or utilities), as barrel files defeat compiler tree-shaking and bloat JS bundles:
```typescript
// ❌ WRONG: Imports entire icon library barrel file
import { ChevronRight, Settings } from 'lucide-react'

// ✅ PREFERRED in large bundles: Direct or optimized path
import ChevronRight from 'lucide-react/dist/esm/icons/chevron-right'
```

### `bundle-dynamic-imports`
Dynamically import heavy components (charts, rich-text editors, maps) with `next/dynamic` so they are not included in the initial page chunk:
```tsx
import dynamic from 'next/dynamic'

const HeavyChart = dynamic(() => import('@/components/AnalyticsChart'), {
  loading: () => <ChartSkeleton />,
  ssr: false, // only if chart requires window / client canvas
})
```

### `bundle-defer-third-party`
Load non-critical analytics, customer support widgets, and logging scripts only after hydration using `next/script` with `strategy="afterInteractive"` or `strategy="lazyOnload"`.

---

## 3. Server-Side Performance & Next.js 15 (HIGH)

### Next.js 15 Default Caching Behavior
> [!IMPORTANT]
> In **Next.js 15**, `fetch` requests and GET Route Handlers are **uncached by default** (`cache: 'no-store'`).
> If you want data to be cached, you must explicitly declare `cache: 'force-cache'` or `next: { revalidate: 3600 }`.

```typescript
// ✅ Explicit caching when data is cacheable
const res = await fetch('https://api.example.com/products', {
  next: { revalidate: 60 }, // ISR: cached for 60s
})
```

### `server-cache-react`
Use `React.cache()` for per-request function deduplication across Server Components:
```typescript
import { cache } from 'react'

export const getOrganization = cache(async (orgId: string) => {
  return await db.organization.findUnique({ where: { id: orgId } })
})
```

### `server-after-nonblocking`
In Next.js 15+, use `after()` from `next/server` to run non-critical side effects (analytics logging, cache warming, notifications) without delaying the HTTP response:
```typescript
import { after } from 'next/server'

export async function POST(request: Request) {
  const data = await request.json()
  const result = await processOrder(data)

  // Runs in background after response is sent to client
  after(async () => {
    await sendAuditLog(result.id)
    await notifySlack(result)
  })

  return Response.json({ success: true, id: result.id })
}
```

---

## 4. Client-Side & React 19 Patterns

### `useActionState` & `useOptimistic` (React 19)
Replace legacy `useTransition` + manual error states with React 19 Server Action hooks:
```tsx
'use client'
import { useActionState, useOptimistic } from 'react'
import { updateNameAction } from '@/actions/profile'

export function ProfileForm({ initialName }: { initialName: string }) {
  const [state, formAction, isPending] = useActionState(updateNameAction, null)
  const [optimisticName, setOptimisticName] = useOptimistic(
    initialName,
    (_current, update: string) => update
  )

  return (
    <form action={async (formData) => {
      setOptimisticName(formData.get('name') as string)
      await formAction(formData)
    }}>
      <input name="name" defaultValue={optimisticName} />
      <button disabled={isPending}>Save</button>
    </form>
  )
}
```

### No `forwardRef` in React 19
React 19 allows passing `ref` directly as a component prop. Do not wrap modern components in `forwardRef()`.
