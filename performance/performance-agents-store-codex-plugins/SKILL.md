---
name: performance
description: Core Web Vitals optimization and page speed for Next.js. This skill should be used when the user asks about "Core Web Vitals", "page speed", "PageSpeed", "LCP", "INP", "CLS", "Lighthouse score", "performance optimization", "next/image optimization", "next/font", "lazy loading", "code splitting", "bundle size", or needs to improve their site's loading speed and interaction responsiveness.
---

# Performance & Core Web Vitals

Core Web Vitals are Google's ranking signals measuring real user experience. Optimize for these three metrics.

## Current Thresholds (2026)

| Metric | Good | Needs Improvement | Poor | What It Measures |
|--------|------|-------------------|------|------------------|
| **LCP** | < 2.5s | 2.5s - 4.0s | > 4.0s | Largest visible content painted |
| **INP** | < 200ms | 200ms - 500ms | > 500ms | Responsiveness to all interactions |
| **CLS** | < 0.1 | 0.1 - 0.25 | > 0.25 | Visual stability (layout shifts) |

**INP replaced FID** in March 2024. INP measures ALL interactions (clicks, taps, keyboard), not just the first one.

## LCP Optimization (Largest Contentful Paint)

LCP measures how quickly the largest above-the-fold element renders.

### Prioritize the LCP Image

```tsx
import Image from 'next/image'

// The hero/banner image is the LCP element: load it eagerly at high fetch priority
<Image
  src="/hero.jpg"
  alt="Hero banner"
  width={1200}
  height={630}
  loading="eager"             // Critical: never lazy-load the LCP image
  fetchPriority="high"        // Critical: tell the browser to fetch it first
  sizes="100vw"               // Full-width image
/>
```

Mark only the LCP element this way — one image per page. If different images are the LCP element at different viewport sizes (a mobile hero and a desktop hero), do **not** use `loading="eager"` or `preload` on them: both images would download on every device. Keep the default lazy loading and set `fetchPriority="high"` only — the Next.js docs' recommendation for that case. Prioritizing everything prioritizes nothing.

**`priority` was replaced in Next.js 16.** The `priority` prop of `next/image` is deprecated since 16.0 in favor of `preload`, which inserts a `<link rel="preload">` for the image in `<head>`. The Next.js docs recommend `loading="eager"` or `fetchPriority="high"` in most cases; use `preload={true}` only when one image is the LCP element at every viewport size and you do not also set `loading` or `fetchPriority`. Do not use `preload` or `loading="eager"` when different images win LCP on different screens (both would download); use `fetchPriority="high"` alone. On Next.js 15 and earlier the prop is still `priority`, and `fetchPriority="high"` works there too.

### Optimize Image Formats

Configure AVIF (best compression) with WebP fallback:

```ts
// next.config.ts
const nextConfig = {
  images: {
    formats: ['image/avif', 'image/webp'],
    remotePatterns: [
      { protocol: 'https', hostname: 'your-cms.com', pathname: '/assets/**' },
    ],
  },
}
```

### Responsive Images with sizes

Always provide `sizes` — without it, the browser downloads the largest image:

```tsx
// Full-width hero
<Image src="/hero.jpg" alt="Hero" width={1920} height={1080}
  loading="eager" fetchPriority="high" sizes="100vw" />

// Grid of 3 columns on desktop, full-width on mobile
<Image src="/card.jpg" alt="Card" width={400} height={300}
  sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw" />

// Sidebar image
<Image src="/sidebar.jpg" alt="Sidebar" width={300} height={200}
  sizes="(max-width: 768px) 100vw, 300px" />
```

### Server-Side Render Above the Fold

Use Server Components for LCP content — no hydration delay:

```tsx
// app/page.tsx — Server Component by default
export default async function Home() {
  const hero = await getHeroContent() // Fetched on server, rendered in HTML

  return (
    <section>
      <h1>{hero.title}</h1>
      <Image src={hero.image} alt={hero.title} loading="eager" fetchPriority="high"
        sizes="100vw" width={1200} height={630} />
    </section>
  )
}
```

## INP Optimization (Interaction to Next Paint)

INP measures responsiveness across ALL user interactions. Three phases: input delay + processing time + presentation delay.

### Break Long Tasks

Any task >50ms blocks the main thread. Split heavy work:

```tsx
'use client'
import { startTransition } from 'react'

function handleSearch(query: string) {
  // Non-urgent: use startTransition to avoid blocking input
  startTransition(() => {
    setFilteredResults(filterLargeDataset(query))
  })
}
```

### Code Split Heavy Components

```tsx
'use client'
import dynamic from 'next/dynamic'

// Load chart library only when needed — not in initial bundle
const Chart = dynamic(() => import('@/components/chart'), {
  loading: () => <div className="h-64 animate-pulse bg-muted rounded" />,
  ssr: false,  // Chart needs browser APIs
})
```

### Debounce Event Handlers

```tsx
'use client'
import { useDeferredValue, useState } from 'react'

function SearchInput() {
  const [query, setQuery] = useState('')
  const deferredQuery = useDeferredValue(query)

  return (
    <>
      <input value={query} onChange={(e) => setQuery(e.target.value)} />
      <SearchResults query={deferredQuery} />
    </>
  )
}
```

### Reduce DOM Size

Target: < 1,500 nodes, depth < 32, < 60 children per parent. For long lists, use virtual scrolling:

```tsx
'use client'
import { useVirtualizer } from '@tanstack/react-virtual'

function VirtualList({ items }: { items: string[] }) {
  const parentRef = useRef<HTMLDivElement>(null)
  const virtualizer = useVirtualizer({
    count: items.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 50,
  })

  return (
    <div ref={parentRef} style={{ height: '400px', overflow: 'auto' }}>
      <div style={{ height: `${virtualizer.getTotalSize()}px`, position: 'relative' }}>
        {virtualizer.getVirtualItems().map((virtualItem) => (
          <div key={virtualItem.key} style={{
            position: 'absolute', top: 0, left: 0, width: '100%',
            height: `${virtualItem.size}px`,
            transform: `translateY(${virtualItem.start}px)`,
          }}>
            {items[virtualItem.index]}
          </div>
        ))}
      </div>
    </div>
  )
}
```

## CLS Optimization (Cumulative Layout Shift)

CLS measures visual stability — elements jumping around as the page loads.

### Always Set Dimensions on Images

```tsx
// Good — dimensions prevent layout shift
<Image src="/photo.jpg" alt="Photo" width={800} height={600} />

// Good — fill with sized parent
<div className="relative aspect-video">
  <Image src="/photo.jpg" alt="Photo" fill sizes="100vw" />
</div>

// Bad — no dimensions → layout shift
<img src="/photo.jpg" alt="Photo" />
```

### Use next/font to Prevent Font Shift

```tsx
// app/layout.tsx
import { Inter } from 'next/font/google'

const inter = Inter({
  subsets: ['latin'],
  display: 'swap',        // Show fallback immediately, swap when loaded
  variable: '--font-sans',
})

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={`${inter.variable} antialiased`}>
      <body>{children}</body>
    </html>
  )
}
```

Tailwind CSS integration:
```css
/* globals.css */
@import 'tailwindcss';

@theme inline {
  --font-sans: var(--font-sans);
}
```

`next/font` downloads fonts at build time and self-hosts them — zero external requests, zero FOUT (Flash of Unstyled Text).

### Avoid Content Injection Above Fold

Never insert banners, cookie notices, or ads above existing content. Reserve space with CSS:

```tsx
// Reserve space for a dynamic banner
<div className="min-h-12">
  <Suspense fallback={<div className="h-12" />}>
    <DynamicBanner />
  </Suspense>
</div>
```

## Caching & ISR

### Incremental Static Regeneration

Serve static pages, revalidate in the background. Check `next.config.ts` for `cacheComponents` first — the two caching models use different APIs.

Previous model (`cacheComponents` off, still the default):

```tsx
// app/blog/[slug]/page.tsx — works only without cacheComponents
export const revalidate = 3600 // Revalidate every hour

export default async function BlogPost({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params
  const post = await getPost(slug)
  return <article>{/* content */}</article>
}
```

With `cacheComponents: true`, the segment config `revalidate` is removed. Cache the data function instead and set its lifetime with `cacheLife`:

```tsx
// lib/posts.ts — Cache Components (cacheComponents: true)
import { cacheLife, cacheTag } from 'next/cache'

export async function getPost(slug: string) {
  'use cache'
  cacheLife('hours')      // replaces export const revalidate = 3600
  cacheTag(`post:${slug}`) // lets a webhook invalidate this post on demand
  return fetchPostFromCms(slug)
}
```

### On-Demand Revalidation

Revalidate when content changes (via webhook from CMS):

```tsx
// app/api/revalidate/route.ts
import { revalidatePath, revalidateTag } from 'next/cache'

export async function POST(request: Request) {
  const { path, tag } = await request.json()
  if (path) revalidatePath(path)
  // The one-argument revalidateTag(tag) is deprecated: pass a profile.
  // 'max' = stale-while-revalidate (recommended). For a webhook that must expire
  // the data immediately, use revalidateTag(tag, { expire: 0 }).
  if (tag) revalidateTag(tag, 'max')
  return Response.json({ revalidated: true })
}
```

In a Server Action, prefer `updateTag(tag)` when the user must see their own change immediately (read-your-own-writes). Protect the route with a shared secret before exposing it.

## Measurement Tools

| Tool | Data Type | Use For |
|------|-----------|---------|
| **PageSpeed Insights** | Field + Lab | Quick check of any URL |
| **Google Search Console** | Field | Real user data over time |
| **Lighthouse** (DevTools) | Lab | Detailed development audit |
| **Web Vitals Extension** | Field | Real-time monitoring during dev |
| **`next build --profile`** | Lab | Identify slow build/render paths |

## Quick Wins Checklist

| Action | Metric Impact | Effort |
|--------|---------------|--------|
| `fetchPriority="high"` + `loading="eager"` on the LCP image (`fetchPriority` alone if the LCP image differs per viewport) | LCP -500ms+ | Low |
| Add `sizes` to all images | LCP, bandwidth | Low |
| Use `next/font` | CLS elimination | Low |
| Set image width/height | CLS elimination | Low |
| `dynamic()` for heavy components | INP, bundle size | Medium |
| Enable AVIF format | LCP, bandwidth | Low |
| Use `startTransition` for non-urgent updates | INP | Medium |
| ISR (`revalidate`, or `'use cache'` + `cacheLife` with Cache Components) | TTFB | Medium |