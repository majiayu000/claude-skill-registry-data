---
name: nextjs-performance-optimization
description: Advanced Next.js performance optimization toolkit for improving Core Web Vitals, reducing bundle sizes, implementing optimal caching strategies, and maximizing runtime performance. Use when building high-performance Next.js applications, conducting performance audits, optimizing existing applications, implementing caching strategies, reducing bundle sizes, improving loading times, solving performance bottlenecks, or optimizing Core Web Vitals in Next.js 16+ projects using App Router. Automatically triggers when users mention 'performance', 'slow', 'optimize', 'Core Web Vitals', 'LCP', 'CLS', 'INP', 'bundle size', 'caching', or request performance improvements.
---

# Next.js Performance Optimization

Expert system for optimizing Next.js 16+ applications across all performance dimensions: rendering strategies, caching, bundle sizes, Core Web Vitals, and runtime performance.

## Overview

This skill provides comprehensive performance optimization guidance for Next.js applications, covering:

- **Performance Auditing**: Automated analysis of build output, bundle sizes, and Core Web Vitals patterns
- **Caching Strategies**: Implementation of Cache Components, Data Cache, and granular invalidation
- **Bundle Optimization**: Reducing JavaScript bundle sizes through code splitting and tree shaking
- **Core Web Vitals**: Achieving excellent LCP, INP, and CLS scores
- **Image Optimization**: Maximizing image performance with Next.js Image component
- **Runtime Performance**: Streaming, prefetching, and rendering optimizations

## When to Use This Skill

Trigger this skill when:
- User requests performance optimization or mentions app is "slow"
- User asks about Core Web Vitals (LCP, CLS, INP, TTFB, FCP)
- User wants to reduce bundle size or improve loading times
- User needs to implement caching strategies
- User mentions performance audit or optimization
- User asks about image optimization
- User requests help with Next.js 16 Cache Components
- Application performance needs improvement
- Conducting pre-production performance review

## Performance Optimization Workflow

### 1. Initial Performance Audit

Start every performance optimization task with a comprehensive audit to identify issues.

#### Run Automated Audit

```bash
# Build the application first
npm run build

# Run performance audit script
python scripts/performance_audit.py .next

# Run Core Web Vitals checker
python scripts/web_vitals_checker.py app

# Run cache strategy analyzer
python scripts/cache_analyzer.py app
```

#### Interpret Audit Results

The scripts identify:
- **Critical Issues**: Large bundles (> 244KB), missing cache configurations, Core Web Vitals violations
- **Optimization Opportunities**: Missing cache tags, non-optimized imports, missing image priorities
- **Current Performance**: Bundle sizes, cache hit potential, performance patterns

#### Manual Checks

In addition to automated audits, perform:

```bash
# Bundle analysis with treemap
ANALYZE=true npm run build

# Lighthouse audit
npx lighthouse http://localhost:3000 --view

# Check Turbopack performance
NEXT_TURBOPACK_TRACING=1 npm run dev
```

### 2. Prioritize Optimizations

Based on audit results, prioritize in this order:

**Priority 1 - Critical (Immediate Impact)**
- LCP > 2.5s → Fix hero image loading
- Bundle size > 244KB → Implement code splitting
- Missing cache on data fetches → Add cache configuration
- CLS > 0.1 → Add image dimensions and font fallbacks
- Server Actions without revalidation → Add cache invalidation

**Priority 2 - High (Significant Impact)**
- INP > 200ms → Optimize event handlers, use memoization
- Missing Cache Components → Add 'use cache' to expensive components
- Non-optimized imports → Fix tree-shaking issues
- TTFB > 600ms → Implement caching strategies
- Images without priority → Add priority to LCP images

**Priority 3 - Medium (Incremental Gains)**
- Missing cache tags → Add granular invalidation
- Opportunities for prefetching → Implement route prefetching
- Missing blur placeholders → Add image placeholders
- Font optimization → Configure font loading strategies

### 3. Implement Optimizations by Category

#### A. Caching Optimizations

Implement multi-layer caching for maximum performance.

**Cache Components (Next.js 16+)**

For expensive Server Components with complex logic:

```tsx
import { cacheLife, cacheTag } from 'next/cache'

async function ProductList({ category }: { category: string }) {
  'use cache'

  // Choose appropriate cache profile
  cacheLife('hours')  // Built-in: 15m stale, 1h revalidate, 1w expire

  // Add tags for granular invalidation
  cacheTag(`products-${category}`)

  const products = await db.products.findMany({
    where: { category }
  })

  return <div>{/* render products */}</div>
}
```

**Cache Profiles Selection**

Choose based on data freshness requirements:

```tsx
cacheLife('seconds')  // Very dynamic (stock prices, live data)
cacheLife('minutes')  // Frequently updated (user dashboards)
cacheLife('hours')    // Moderately dynamic (product listings)
cacheLife('days')     // Mostly static (blog posts)
cacheLife('weeks')    // Rarely changes (documentation)
cacheLife('max')      // Static content (marketing pages)
```

**Data Cache (Fetch)**

For individual API/database requests:

```tsx
// Time-based revalidation (ISR)
const res = await fetch('https://api.example.com/products', {
  next: {
    revalidate: 3600,  // 1 hour
    tags: ['products', `category-${categoryId}`]
  }
})

// Static caching
const res = await fetch('https://api.example.com/static', {
  cache: 'force-cache'
})

// Dynamic (no cache)
const res = await fetch('https://api.example.com/user', {
  cache: 'no-store'
})
```

**Cache Invalidation**

After mutations, invalidate affected caches:

```tsx
'use server'
import { revalidateTag, revalidatePath } from 'next/cache'

export async function updateProduct(id: string, data: any) {
  await db.products.update({ where: { id }, data })

  // Granular invalidation (preferred)
  revalidateTag(`product-${id}`)
  revalidateTag('products')

  // Or path-based invalidation
  revalidatePath('/products')
}
```

**Reference**: See `references/caching-strategies.md` for advanced patterns, troubleshooting, and custom cache profiles.

#### B. Bundle Size Optimization

Reduce JavaScript bundle sizes through strategic code splitting and import optimization.

**Enable Package Import Optimization**

```js
// next.config.js
module.exports = {
  experimental: {
    optimizePackageImports: [
      '@mui/material',
      '@mui/icons-material',
      'lodash',
      'react-icons',
      'lucide-react',
      'date-fns'
    ]
  }
}
```

**Fix Non-Optimized Imports**

```tsx
// ❌ Bad - imports entire library
import { Button, TextField } from '@mui/material'
import _ from 'lodash'

// ✅ Good - tree-shakeable imports
import Button from '@mui/material/Button'
import TextField from '@mui/material/TextField'
import { debounce } from 'lodash-es'
```

**Dynamic Imports for Heavy Components**

```tsx
import dynamic from 'next/dynamic'

// Load heavy components on-demand
const HeavyChart = dynamic(() => import('@/components/HeavyChart'), {
  loading: () => <ChartSkeleton />,
  ssr: false  // Disable SSR if not needed
})

const PDFViewer = dynamic(() => import('@/components/PDFViewer'), {
  ssr: false
})

const MarkdownEditor = dynamic(() => import('@/components/MarkdownEditor'), {
  loading: () => <EditorSkeleton />
})
```

**Replace Heavy Packages**

```tsx
// Common replacements for bundle savings
moment (329KB)     → dayjs (7KB) or date-fns (13KB)
lodash (72KB)      → lodash-es + specific imports
axios (33KB)       → fetch API (built-in)
react-icons (all)  → lucide-react (specific icons)
chart.js (400KB)   → recharts (100KB)
```

**Turbopack Configuration**

```js
// next.config.js
module.exports = {
  turbopack: {
    resolveAlias: {
      'lodash': 'lodash-es',  // Use ES modules for tree-shaking
      'date-fns': 'date-fns/esm'
    }
  },

  compiler: {
    removeConsole: process.env.NODE_ENV === 'production' ? {
      exclude: ['error', 'warn']
    } : false
  }
}
```

**Reference**: See `references/bundle-optimization.md` for advanced code splitting, chunk configuration, and bundle analysis techniques.

#### C. Core Web Vitals Optimization

Optimize for Google's Core Web Vitals metrics.

**LCP (Largest Contentful Paint) - Target < 2.5s**

Fix hero image loading:

```tsx
import Image from 'next/image'

export default function Hero() {
  return (
    <Image
      src="/hero.jpg"
      alt="Hero"
      width={1920}
      height={1080}
      priority        // ← Preloads the image
      quality={90}    // Higher quality for hero
      placeholder="blur"
      blurDataURL={blurDataUrl}
    />
  )
}
```

Implement streaming for faster FCP:

```tsx
import { Suspense } from 'react'

export default function Page() {
  return (
    <>
      <Header />  {/* Shell loads immediately */}

      <Suspense fallback={<HeroSkeleton />}>
        <HeroSection />  {/* LCP content streams in */}
      </Suspense>

      <Suspense fallback={<ContentSkeleton />}>
        <ContentSection />
      </Suspense>
    </>
  )
}
```

**INP (Interaction to Next Paint) - Target < 200ms**

Optimize expensive computations:

```tsx
'use client'

import { useMemo, useCallback } from 'react'

export default function SearchResults({ data }) {
  // Memoize expensive computations
  const filtered = useMemo(
    () => data.filter(item => expensiveCheck(item)),
    [data]
  )

  // Memoize callbacks
  const handleClick = useCallback((id) => {
    processItem(id)
  }, [])

  return <ResultsList items={filtered} onClick={handleClick} />
}
```

Debounce user inputs:

```tsx
'use client'

import { useState, useCallback } from 'react'

export default function SearchBar() {
  const [query, setQuery] = useState('')

  const debouncedSearch = useCallback(
    debounce(async (value: string) => {
      const results = await searchAPI(value)
      setResults(results)
    }, 300),
    []
  )

  return <input onChange={(e) => debouncedSearch(e.target.value)} />
}
```

**CLS (Cumulative Layout Shift) - Target < 0.1**

Add image dimensions:

```tsx
// ❌ Causes layout shift
<img src="/product.jpg" />

// ✅ Prevents layout shift
<Image
  src="/product.jpg"
  width={400}
  height={300}
/>
```

Configure font loading:

```tsx
// app/layout.tsx
import { Inter } from 'next/font/google'

const inter = Inter({
  subsets: ['latin'],
  display: 'swap',
  preload: true,
  adjustFontFallback: true,  // ← Reduces CLS
  variable: '--font-inter'
})
```

Use skeletons for loading states:

```tsx
export default function Page() {
  return (
    <Suspense fallback={<UserProfileSkeleton />}>
      <UserProfile />
    </Suspense>
  )
}
```

**Reference**: See `references/core-web-vitals.md` for comprehensive guides on each metric, measurement strategies, and troubleshooting.

#### D. Image Optimization

Maximize image performance with Next.js Image component.

**Hero/LCP Images**

```tsx
<Image
  src="/hero.jpg"
  alt="Hero"
  width={1920}
  height={1080}
  priority          // Preload for LCP
  quality={90}      // High quality
  placeholder="blur"
  blurDataURL={blurDataUrl}
  sizes="100vw"
/>
```

**Content Images**

```tsx
<Image
  src="/product.jpg"
  alt="Product"
  width={800}
  height={600}
  quality={85}      // Balanced quality
  loading="lazy"    // Default lazy loading
  sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
/>
```

**Global Configuration**

```js
// next.config.js
module.exports = {
  images: {
    formats: ['image/avif', 'image/webp'],
    deviceSizes: [640, 750, 828, 1080, 1200, 1920, 2048, 3840],
    minimumCacheTTL: 31536000,  // 1 year

    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'cdn.example.com'
      }
    ]
  }
}
```

**Reference**: See `references/image-optimization.md` for responsive images, blur placeholders, remote images, and advanced patterns.

#### E. Runtime Performance

Optimize rendering and data fetching strategies.

**Rendering Strategy Selection**

```tsx
// Static Generation (fastest) - for content that doesn't change
export default async function StaticPage() {
  const data = await fetch('https://api.example.com/data', {
    cache: 'force-cache'
  })
  return <div>{/* render */}</div>
}

// ISR - for content that updates periodically
export default async function ISRPage() {
  const data = await fetch('https://api.example.com/data', {
    next: { revalidate: 3600 }
  })
  return <div>{/* render */}</div>
}

// Dynamic - for personalized content
import { cookies } from 'next/headers'

export default async function DynamicPage() {
  const cookieStore = await cookies()
  const theme = cookieStore.get('theme')
  return <div>{/* personalized content */}</div>
}
```

**Parallel Data Fetching**

```tsx
async function ProductPage({ id }: { id: string }) {
  // Initiate requests in parallel
  const productPromise = getProduct(id)
  const reviewsPromise = getReviews(id)
  const relatedPromise = getRelated(id)

  // Await all together
  const [product, reviews, related] = await Promise.all([
    productPromise,
    reviewsPromise,
    relatedPromise
  ])

  return <ProductDetail product={product} reviews={reviews} related={related} />
}
```

**Prefetching Strategies**

```tsx
import Link from 'next/link'
import { prefetch } from 'next/navigation'

// Automatic prefetching (viewport-based)
<Link href="/products" prefetch={true}>
  Products
</Link>

// Manual prefetching on hover
export function PrefetchButton() {
  return (
    <button
      onMouseEnter={() => prefetch('/dashboard')}
      onClick={() => router.push('/dashboard')}
    >
      Dashboard
    </button>
  )
}
```

### 4. Verification and Monitoring

After implementing optimizations, verify improvements:

**Build Analysis**

```bash
# Re-run performance audit
npm run build
python scripts/performance_audit.py .next

# Verify bundle sizes reduced
ANALYZE=true npm run build

# Check cache implementation
python scripts/cache_analyzer.py app
```

**Core Web Vitals Measurement**

```bash
# Lighthouse audit
lighthouse http://localhost:3000 --view

# Check specific metrics
lighthouse http://localhost:3000 --only-categories=performance
```

**Production Monitoring**

```tsx
// app/layout.tsx - Track Core Web Vitals
export function reportWebVitals(metric: any) {
  const thresholds = {
    FCP: 1800,
    LCP: 2500,
    INP: 200,
    CLS: 0.1,
    TTFB: 600
  }

  if (metric.value > thresholds[metric.name]) {
    // Send to analytics
    analytics.track('web_vital_issue', {
      metric: metric.name,
      value: metric.value,
      threshold: thresholds[metric.name],
      path: window.location.pathname
    })
  }
}
```

### 5. Performance Checklist

Before deploying optimized application:

**Build Optimization**
- [ ] Using Turbopack for dev and build
- [ ] Bundle analyzer shows no unexpected large dependencies
- [ ] Initial JS bundle < 200KB (gzipped)
- [ ] Configured `optimizePackageImports`
- [ ] Tree-shaking working correctly
- [ ] No duplicate dependencies

**Caching Strategy**
- [ ] Implemented appropriate `revalidate` times
- [ ] Using Cache Components for expensive logic
- [ ] Cache tags configured for granular invalidation
- [ ] Server Actions call revalidateTag/revalidatePath
- [ ] CDN cache headers configured

**Images & Assets**
- [ ] All images use Next.js Image component
- [ ] Hero images have `priority={true}`
- [ ] Implemented blur placeholders
- [ ] WebP/AVIF formats configured
- [ ] Responsive sizes specified

**Core Web Vitals**
- [ ] LCP < 2.5s
- [ ] INP < 200ms
- [ ] CLS < 0.1
- [ ] TTFB < 600ms
- [ ] FCP < 1.8s

**Runtime Performance**
- [ ] Using streaming where appropriate
- [ ] Parallel data fetching implemented
- [ ] Prefetching configured
- [ ] Memoization for expensive computations
- [ ] Error boundaries implemented

## Common Performance Patterns

### Pattern: Progressive Enhancement with Streaming

```tsx
import { Suspense } from 'react'

export default function DashboardPage() {
  return (
    <>
      {/* Instant shell */}
      <DashboardHeader />

      {/* Critical content streams first */}
      <Suspense fallback={<StatsSkeleton />}>
        <DashboardStats />
      </Suspense>

      {/* Non-critical content streams later */}
      <Suspense fallback={<ActivitySkeleton />}>
        <RecentActivity />
      </Suspense>

      <Suspense fallback={<ChartSkeleton />}>
        <AnalyticsChart />
      </Suspense>
    </>
  )
}
```

### Pattern: Optimistic UI with Cache Invalidation

```tsx
'use server'

import { revalidateTag } from 'next/cache'

export async function likePost(postId: string) {
  // Optimistic update happens on client
  await db.likes.create({
    data: { postId, userId: getCurrentUserId() }
  })

  // Invalidate relevant caches
  revalidateTag(`post-${postId}`)
  revalidateTag('posts')
}
```

### Pattern: Code Splitting by Route and Component

```tsx
// app/dashboard/page.tsx
import dynamic from 'next/dynamic'

// Heavy components loaded dynamically
const AnalyticsChart = dynamic(() => import('@/components/AnalyticsChart'), {
  loading: () => <ChartSkeleton />,
  ssr: false
})

const DataTable = dynamic(() => import('@/components/DataTable'))

export default function Dashboard() {
  return (
    <>
      <DashboardHeader />
      <AnalyticsChart />
      <DataTable />
    </>
  )
}
```

## Troubleshooting Performance Issues

### Issue: Slow Page Load

**Diagnose:**
```bash
python scripts/performance_audit.py .next
lighthouse http://localhost:3000
```

**Common Causes:**
- Large bundle sizes → Implement dynamic imports
- Missing caching → Add Cache Components and Data Cache
- Unoptimized images → Use Image component with priority
- Blocking resources → Implement streaming

### Issue: Poor Core Web Vitals

**Diagnose:**
```bash
python scripts/web_vitals_checker.py app
lighthouse http://localhost:3000 --only-categories=performance
```

**Common Causes:**
- High LCP → Add priority to hero images, implement caching
- High INP → Debounce inputs, use memoization
- High CLS → Add image dimensions, configure fonts

### Issue: Large Bundle Size

**Diagnose:**
```bash
ANALYZE=true npm run build
```

**Common Causes:**
- Non-optimized imports → Enable optimizePackageImports
- Heavy libraries → Use dynamic imports or lighter alternatives
- Unused code → Verify tree-shaking is working

## Resources

This skill includes comprehensive reference documentation:

### Scripts (`scripts/`)

- **`performance_audit.py`**: Analyzes build output, bundle sizes, and provides recommendations
- **`web_vitals_checker.py`**: Checks code patterns that impact Core Web Vitals scores
- **`cache_analyzer.py`**: Analyzes caching patterns and identifies missing configurations

### References (`references/`)

- **`caching-strategies.md`**: Deep dive into Cache Components, Data Cache, and invalidation strategies
- **`bundle-optimization.md`**: Comprehensive guide to reducing bundle sizes and code splitting
- **`core-web-vitals.md`**: Complete guide to optimizing LCP, INP, and CLS
- **`image-optimization.md`**: Advanced image optimization techniques and patterns

## Best Practices

1. **Always Audit First**: Run automated audits before making changes
2. **Prioritize Critical Issues**: Focus on high-impact optimizations first
3. **Measure Impact**: Verify improvements with metrics after each optimization
4. **Use Cache Layers**: Combine Cache Components, Data Cache, and Route Cache
5. **Optimize Images**: Always use Image component with appropriate configurations
6. **Monitor Production**: Track Core Web Vitals in production with analytics
7. **Test in Production Mode**: Performance characteristics differ from development
8. **Set Performance Budgets**: Enforce bundle size and metric thresholds in CI/CD

## Performance Targets

| Metric | Target | Maximum |
|--------|--------|---------|
| LCP | < 2.5s | < 4.0s |
| INP | < 200ms | < 500ms |
| CLS | < 0.1 | < 0.25 |
| TTFB | < 600ms | < 800ms |
| FCP | < 1.8s | < 3.0s |
| Initial JS | < 130KB | < 170KB |
| Total JS | < 200KB | < 350KB |

*All bundle sizes are gzipped*
