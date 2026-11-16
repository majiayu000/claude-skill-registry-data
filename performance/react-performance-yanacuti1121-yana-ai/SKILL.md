---
name: react-performance
description: React and Next.js performance optimization — eliminate waterfalls, reduce bundle size, optimize renders, server-side patterns. 70+ rules by impact priority. Profile first, optimize second.
license: MIT
source: https://github.com/affaan-m/ECC
---

# React Performance

Ordered by impact. Fix P1 before P2. Profile before adding memo.

**Trigger phrases:** "slow React", "performance", "bundle size", "waterfall", "re-render", "optimize Next.js", "LCP", "FCP"

---

## P1 — Waterfall Elimination

```tsx
// ❌ Sequential
const user = await getUser(id)
const posts = await getPosts(user.id)

// ✅ Parallel
const [user, posts] = await Promise.all([getUser(id), getPosts(id)])
```

---

## P2 — Bundle Size

```tsx
// ✅ Dynamic imports
const HeavyChart = dynamic(() => import('./Chart'), { loading: () => <Skeleton />, ssr: false })

// ✅ Tree-shake
import { debounce } from 'lodash/debounce'   // ✅ not import from 'lodash'
```

Target: JS bundle < 200KB gzipped per route.

---

## P3 — Server-Side Patterns

```tsx
// Server Component — zero client JS
async function ProductList() {
  const products = await db.products.findMany({ take: 20 })
  return <ul>{products.map(p => <ProductCard key={p.id} {...p} />)}</ul>
}

// Cache expensive computations
import { cache } from 'react'
const getUser = cache(async (id: string) => db.users.findUnique({ where: { id } }))
```

---

## P4 — Client Data Fetching

```tsx
const { data } = useQuery({ queryKey: ['users'], queryFn: getUsers, staleTime: 1000 * 60 * 5 })
```

---

## P5 — Re-render Prevention

```tsx
const ExpensiveList = memo(({ items }) => <ul>{items.map(i => <Item key={i.id} {...i} />)}</ul>)
const handleClick = useCallback((id: string) => setSelected(id), [])
const sorted = useMemo(() => items.sort(compareFn), [items])
```

**Only add memo after React DevTools Profiler confirms the cost.**

---

## P6 — Virtualize Long Lists

```tsx
import { useVirtualizer } from '@tanstack/react-virtual'
// For lists > 100 items
```

---

## Anti-Fake-Pass

```
❌ Adding memo everywhere without profiling — adds overhead
❌ Parallel fetches split across separate useEffect → still sequential
❌ No staleTime in TanStack Query → refetches on every focus
❌ Large images without next/image
```
