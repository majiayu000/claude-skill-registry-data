---
name: performance
description: Next.js performance optimization — Core Web Vitals, ISR/SSG strategy, bundle analysis, image optimization, and runtime performance patterns. Use when diagnosing slow pages, optimizing Core Web Vitals, or reviewing production performance.
trigger: 需要优化网站性能
input: 性能问题
output: 性能优化建议
next: 无
dependencies: 无
---

# Next.js Performance

Systematic approach to optimizing Next.js applications.

## Performance Dimensions

### 1. Rendering Strategy

Pick the right strategy per route:

| Strategy | Use Case | Trade-off |
|----------|----------|-----------|
| **Static (SSG)** | Public content, blog, docs | Fastest, no server load, stale on update |
| **ISR** | Content that changes periodically | Revalidate on demand or by time |
| **Dynamic (SSR)** | User-specific, auth-gated | Always fresh, server cost per request |
| **Streaming** | Routes with slow data dependencies | Faster TTFB, progressive rendering |

Rule of thumb: **Static by default, dynamic by necessity.**

### 2. Bundle Optimization

```bash
# Analyze bundle
ANALYZE=true npm run build

# Check individual package size
npx cost-of-modules
```

Key areas:
- Dynamic imports for heavy components (`next/dynamic`)
- Tree-shake unused imports
- Avoid barrel exports (`index.ts` re-exports hurt tree-shaking)
- Use `react-compiler` where possible

```tsx
import dynamic from 'next/dynamic'
const HeavyChart = dynamic(() => import('./heavy-chart'), {
  loading: () => <ChartSkeleton />
})
```

### 3. Image Optimization

Use `next/image` everywhere:

```tsx
import Image from 'next/image'

// ✅ Good: automatic optimization, lazy loading, correct sizing
<Image
  src="/hero.jpg"
  alt="Hero"
  width={1200}
  height={600}
  priority          // Use for above-the-fold images
  sizes="100vw"     // Responsive: fills viewport width
/>
```

Rules:
- Always provide `width` and `height` (prevents layout shift)
- Use `priority` for LCP images (hero, main banner)
- Use `sizes` for responsive images
- Host images on a CDN (or use remote patterns)

### 4. Font Optimization

```tsx
// app/layout.tsx
import { Inter } from 'next/font/google'

const inter = Inter({
  subsets: ['latin'],
  display: 'swap',  // Prevent FOIT
})
```

- Always use `next/font` (self-hosts, eliminates external requests)
- Use `display: 'swap'` for better perceived performance

### 5. Core Web Vitals Checklist

| Metric | Target | Common Fixes |
|--------|--------|-------------|
| **LCP** | ≤ 2.5s | Optimize hero image (`priority`), reduce TTFB, preload key resources |
| **FID / INP** | ≤ 200ms | Break up long tasks, lazy load below-fold, avoid heavy JS on main thread |
| **CLS** | ≤ 0.1 | Set dimensions on images/videos, avoid layout shifts from dynamic content |

### 6. Route Segment Optimization

```tsx
// Good: colocate data fetching with the segment that needs it
app/
  blog/
    page.tsx              // fetch blog list
    [slug]/
      page.tsx            // fetch single post
      loading.tsx         // segment-level loading state
```

- Each segment can have its own `loading.tsx` (streaming boundary)
- Long page + slow section → extract into `page.tsx` with `<Suspense>`

## Measurement

```bash
# Local Lighthouse
npx @next/codemod@latest optimize

# Production monitoring
# Vercel Analytics / Speed Insights — enable in dashboard
```

## Checklist

- [ ] Correct rendering strategy per route (static > ISR > dynamic > streaming)
- [ ] Hero image has `priority` and explicit dimensions
- [ ] No layout shift from dynamic content (set height/width placeholders)
- [ ] Heavy components lazy-loaded with `next/dynamic`
- [ ] Font uses `next/font` with `display: 'swap'`
- [ ] No barrel exports in component directories
- [ ] Loading states with `loading.tsx` or Suspense boundaries
- [ ] Vercel Speed Insights enabled for production monitoring