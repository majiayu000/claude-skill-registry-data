---
name: react-performance
model: standard
description:
  React and Next.js performance optimization patterns. Use when writing,
  reviewing, or refactoring React/Next.js code to ensure optimal performance.
  Triggers on tasks involving components, data fetching, bundle optimization,
  re-render reduction, or server component architecture.
version: "1.0"
---

# React Performance Patterns

Performance optimization guide for React and Next.js applications. Patterns
across 7 categories, prioritized by impact. Detailed examples in `references/`.

## When to Apply

- Writing new React components or Next.js pages
- Implementing data fetching (client or server-side)
- Reviewing or refactoring for performance
- Optimizing bundle size or load times

## Categories by Priority

| # | Category             | Impact     |
|---|----------------------|------------|
| 1 | Async / Waterfalls   | CRITICAL   |
| 2 | Bundle Size          | CRITICAL   |
| 3 | Server Components    | HIGH       |
| 4 | Re-renders           | MEDIUM     |
| 5 | Rendering            | MEDIUM     |
| 6 | Client-Side Data     | MEDIUM     |
| 7 | JS Performance       | LOW-MEDIUM |


## Installation

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install react-performance
```


---

## 1. Async — Eliminating Waterfalls (CRITICAL)

### Parallelize independent operations

Sequential awaits are the single biggest performance mistake in React apps.

```typescript
// BAD — sequential, 3 round trips
const user = await fetchUser()
const posts = await fetchPosts()
const comments = await fetchComments()

// GOOD — parallel, 1 round trip
const [user, posts, comments] = await Promise.all([
  fetchUser(), fetchPosts(), fetchComments(),
])
```

### Defer await until needed

Move `await` into branches where the value is actually used.

```typescript
// BAD — blocks both branches
async function handle(userId: string, skip: boolean) {
  const data = await fetchUserData(userId)
  if (skip) return { skipped: true }    // Still waited
  return process(data)
}

// GOOD — only blocks when needed
async function handle(userId: string, skip: boolean) {
  if (skip) return { skipped: true }    // Returns immediately
  return process(await fetchUserData(userId))
}
```

### Strategic Suspense boundaries

Show layout immediately while data-dependent sections load independently.

```tsx
// BAD — entire page blocked
async function Page() {
  const data = await fetchData()
  return <div><Sidebar /><Header /><DataDisplay data={data} /><Footer /></div>
}

// GOOD — layout renders immediately, data streams in
function Page() {
  return (
    <div>
      <Sidebar /><Header />
      <Suspense fallback={<Skeleton />}><DataDisplay /></Suspense>
      <Footer />
    </div>
  )
}
async function DataDisplay() {
  const data = await fetchData()
  return <div>{data.content}</div>
}
```

Share a promise across components with `use()` to avoid duplicate fetches.

---

## 2. Bundle Size (CRITICAL)

### Avoid barrel file imports

Barrel files load thousands of unused modules. Direct imports save 200-800ms.

```tsx
// BAD — loads 1,583 modules
import { Check, X, Menu } from 'lucide-react'

// GOOD — loads only 3 modules
import Check from 'lucide-react/dist/esm/icons/check'
import X from 'lucide-react/dist/esm/icons/x'
import Menu from 'lucide-react/dist/esm/icons/menu'
```

Next.js 13.5+: use `experimental.optimizePackageImports` in config.
Commonly affected: `lucide-react`, `@mui/material`, `react-icons`, `@radix-ui`,
`lodash`, `date-fns`.

### Dynamic imports for heavy components

```tsx
import dynamic from 'next/dynamic'
const MonacoEditor = dynamic(
  () => import('./monaco-editor').then((m) => m.MonacoEditor),
  { ssr: false }
)
```

### Defer non-critical third-party libraries

Analytics, logging, error tracking — load after hydration with `dynamic()` and
`{ ssr: false }`.

### Preload on user intent

```tsx
const preload = () => { void import('./monaco-editor') }
<button onMouseEnter={preload} onFocus={preload} onClick={onClick}>Open Editor</button>
```

---

## 3. Server Components (HIGH)

### Minimize serialization at RSC boundaries

Only pass fields the client actually uses across the server/client boundary.

```tsx
// BAD — serializes all 50 user fields
return <Profile user={user} />

// GOOD — serializes 1 field
return <Profile name={user.name} />
```

### Parallel data fetching with composition

RSC execute sequentially within a tree. Restructure to parallelize.

```tsx
// BAD — Sidebar waits for header fetch
export default async function Page() {
  const header = await fetchHeader()
  return <div><div>{header}</div><Sidebar /></div>
}

// GOOD — sibling async components fetch simultaneously
async function Header() { return <div>{await fetchHeader()}</div> }
async function Sidebar() { return <nav>{(await fetchSidebarItems()).map(renderItem)}</nav> }
export default function Page() { return <div><Header /><Sidebar /></div> }
```

### React.cache() for per-request deduplication

```typescript
import { cache } from 'react'
export const getCurrentUser = cache(async () => {
  const session = await auth()
  if (!session?.user?.id) return null
  return await db.user.findUnique({ where: { id: session.user.id } })
})
```

Use primitive args (not inline objects) — `React.cache()` uses `Object.is`.
Next.js auto-deduplicates `fetch`, but `React.cache()` is needed for DB queries,
auth checks, and computations.

### after() for non-blocking operations

```tsx
import { after } from 'next/server'
export async function POST(request: Request) {
  await updateDatabase(request)
  after(async () => { logUserAction({ userAgent: request.headers.get('user-agent') }) })
  return Response.json({ status: 'success' })
}
```

---

## 4. Re-render Optimization (MEDIUM)

### Derive state during render — not in effects

```tsx
// BAD — redundant state + effect
const [fullName, setFullName] = useState('')
useEffect(() => { setFullName(first + ' ' + last) }, [first, last])

// GOOD — derive inline
const fullName = first + ' ' + last
```

### Functional setState for stable callbacks

```tsx
// BAD — recreated on every items change
const addItem = useCallback((item: Item) => {
  setItems([...items, item])
}, [items])

// GOOD — stable, always latest state
const addItem = useCallback((item: Item) => {
  setItems((curr) => [...curr, item])
}, [])
```

### Defer state reads to usage point

Don't subscribe to dynamic state if you only read it in callbacks.

```tsx
// BAD — re-renders on every searchParams change
const searchParams = useSearchParams()
const handleShare = () => shareChat(chatId, { ref: searchParams.get('ref') })

// GOOD — reads on demand
const handleShare = () => {
  const ref = new URLSearchParams(window.location.search).get('ref')
  shareChat(chatId, { ref })
}
```

### Lazy state initialization

```tsx
// BAD — JSON.parse runs every render
const [settings] = useState(JSON.parse(localStorage.getItem('s') || '{}'))

// GOOD — runs only once
const [settings] = useState(() => JSON.parse(localStorage.getItem('s') || '{}'))
```

### Subscribe to derived booleans

```tsx
// BAD — re-renders on every pixel
const width = useWindowWidth(); const isMobile = width < 768

// GOOD — re-renders only when boolean flips
const isMobile = useMediaQuery('(max-width: 767px)')
```

### Transitions for non-urgent updates

```tsx
// BAD — blocks UI on scroll
const handler = () => setScrollY(window.scrollY)

// GOOD — non-blocking
const handler = () => startTransition(() => setScrollY(window.scrollY))
```

### Extract expensive work into memoized components

```tsx
const UserAvatar = memo(function UserAvatar({ user }: { user: User }) {
  const id = useMemo(() => computeAvatarId(user), [user])
  return <Avatar id={id} />
})
function Profile({ user, loading }: Props) {
  if (loading) return <Skeleton />
  return <div><UserAvatar user={user} /></div>
}
```

Note: React Compiler makes manual `memo()`/`useMemo()` unnecessary.

---

## 5. Rendering Performance (MEDIUM)

### CSS content-visibility for long lists

For 1000 items, browser skips ~990 off-screen (10x faster initial render).

```css
.list-item { content-visibility: auto; contain-intrinsic-size: 0 80px; }
```

### Hoist static JSX outside components

Avoids re-creation, especially for large SVG nodes. React Compiler does this
automatically.

```tsx
const skeleton = <div className="skeleton" />
function Container() { return <div>{loading && skeleton}</div> }
```

---

## 6. Client-Side Data (MEDIUM)

### SWR for deduplication and caching

```tsx
// BAD — each instance fetches independently
useEffect(() => { fetch('/api/users').then(r => r.json()).then(setUsers) }, [])

// GOOD — multiple instances share one request
const { data: users } = useSWR('/api/users', fetcher)
```

---

## 7. JS Performance (LOW-MEDIUM)

### Set/Map for O(1) lookups

```typescript
// BAD — O(n)
items.filter(i => allowed.includes(i.id))
// GOOD — O(1)
const allowedSet = new Set(allowed)
items.filter(i => allowedSet.has(i.id))
```

### Combine array iterations

```typescript
// BAD — 3 passes
const a = users.filter(u => u.isAdmin)
const t = users.filter(u => u.isTester)
// GOOD — 1 pass
const a: User[] = [], t: User[] = []
for (const u of users) { if (u.isAdmin) a.push(u); if (u.isTester) t.push(u) }
```

**Also:** early returns, cache property access in loops, hoist RegExp outside
loops, prefer `for...of` for hot paths.

---

## Quick Decision Guide

1. **Slow page load?** → Bundle size (2), then async waterfalls (1)
2. **Sluggish interactions?** → Re-renders (4), then JS perf (7)
3. **Server page slow?** → RSC serialization & parallel fetching (3)
4. **Client data stale/slow?** → SWR (6)
5. **Long lists janky?** → content-visibility (5)
