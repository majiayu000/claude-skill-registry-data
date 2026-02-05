---
name: nextjs-performance
description: Next.js performance optimizations including next/image, next/font, dynamic imports, caching strategies, and bundle optimization. Use when optimizing Next.js apps for speed or Core Web Vitals.
---

# Next.js Performance

Expert guidance for optimizing Next.js applications.

## Quick Reference

| Concern | Solution | Impact |
|---------|----------|--------|
| Images | next/image with sizing | CLS prevention, auto-optimization |
| Fonts | next/font | No layout shift, self-hosted |
| Heavy components | next/dynamic | Reduced initial bundle |
| Data caching | fetch options (revalidate) | Reduced server load |
| Client navigation | Link component | Instant transitions |
| Bundle size | Tree shaking, no unused deps | Faster JS loading |

## What Do You Need?

1. **Image optimization** - next/image usage, sizing, formats
2. **Font loading** - next/font, preloading
3. **Code splitting** - Dynamic imports, route splitting
4. **Caching** - ISR, revalidation, cache strategies
5. **Navigation** - Link usage, prefetching

Specify a number or describe your performance concern.

## Routing

| Response | Reference to Read |
|----------|-------------------|
| 1, "image", "img", "optimization", "cls" | [images.md](./references/images.md) |
| 2, "font", "layout shift", "typography" | [fonts.md](./references/fonts.md) |
| 3, "dynamic", "import", "lazy", "split" | [code-splitting.md](./references/code-splitting.md) |
| 4, "cache", "revalidate", "isr", "fetch" | [caching.md](./references/caching.md) |
| 5, "navigation", "link", "prefetch" | [navigation.md](./references/navigation.md) |

## Essential Principles

**Optimize images**: Use next/image with width/height for all images. Prevents CLS and enables automatic optimization.

**Self-host fonts**: Use next/font to eliminate requests to external font services and prevent layout shift.

**Dynamic import heavy code**: Use next/dynamic for components that are heavy or not immediately visible.

**Client-side navigation**: Use Link component for all internal links. Enables instant page transitions.

**Cache strategically**: Use appropriate fetch caching (force-cache, no-store, revalidate) based on data freshness needs.

## Common Performance Issues

| Issue | Severity | Impact | Fix |
|-------|----------|--------|-----|
| Using `<img>` instead of next/image | High | CLS, no optimization | Use next/image |
| External fonts | Medium | Layout shift, extra request | Use next/font |
| Large initial bundle | High | Slow initial load | Dynamic imports |
| No caching on static data | Medium | Unnecessary server load | Add revalidate |
| Using `<a>` instead of Link | High | Full page reload | Use Link |
| No priority hints | Low | Delayed LCP | Use priority prop |

## Code Patterns

### Images
```typescript
// Good: next/image with sizing
import Image from 'next/image'

<Image
  src="/avatar.jpg"
  width={100}
  height={100}
  alt="Avatar"
  priority // For above-fold images
/>
```

### Fonts
```typescript
// Good: next/font
import { Inter } from 'next/font/google'

const inter = Inter({ subsets: ['latin'] })

export default function RootLayout({ children }: { children: ReactNode }) {
  return <html className={inter.className}>{children}</html>
}
```

### Dynamic Imports
```typescript
// Good: Dynamic import for heavy component
import dynamic from 'next/dynamic'

const HeavyChart = dynamic(() => import('./HeavyChart'), {
  loading: () => <div>Loading...</div>,
  ssr: false, // If client-only
})
```

### Caching
```typescript
// Good: Appropriate caching
export const revalidate = 3600 // Revalidate every hour

async function getData() {
  const res = await fetch('https://api.example.com/data', {
    next: { revalidate: 3600 } // or { revalidate: 0 } for no cache
  })
  return res.json()
}
```

## Reference Index

| File | Topics |
|------|--------|
| [images.md](./references/images.md) | next/image, sizing, priority, formats |
| [fonts.md](./references/fonts.md) | next/font, Google fonts, local fonts |
| [code-splitting.md](./references/code-splitting.md) | Dynamic imports, route splitting |
| [caching.md](./references/caching.md) | fetch options, ISR, revalidatePath |
| [navigation.md](./references/navigation.md) | Link component, prefetching, scroll |

## Success Criteria

Performance is good when:
- All images use next/image with proper sizing
- Fonts loaded with next/font (no layout shift)
- Heavy components dynamically imported
- Static data cached appropriately (revalidate set)
- All internal links use Link component
- LCP < 2.5s, FID < 100ms, CLS < 0.1
