---
name: performance-engineering
description: Bundle budgets, Lighthouse thresholds, Core Web Vitals, code splitting, image optimization, animation frame budgets, and lazy loading. Use when enforcing the "60fps" performance target.
version: "1.0.0"
verified_date: 2026-06-01
category: frontend
---

# Performance Engineering

## Purpose
Make performance claims enforceable with concrete budgets, measurement tools, and optimization patterns. "60fps" is meaningless without measurement. This skill provides the measurement framework.

## When to Use This Skill
Use when:
- Auditing page performance before shipping
- Optimizing a sluggish page
- Setting up performance monitoring
- Code-splitting heavy dependencies (Three.js, GSAP)
- Image and font optimization

Do NOT use when:
- The task is a simple textual change or mock with no runtime or load impact.

## Phase 1: Performance Analysis

## 1. Performance Budgets

### Bundle Size Budgets
| Metric | Budget | Measurement |
|--------|--------|-------------|
| Initial JS (gzipped) | < 200KB | `next build` output or `bundleanalyzer` |
| Total JS (gzipped) | < 500KB | All chunks combined |
| CSS (gzipped) | < 50KB | Tailwind purge should achieve this |
| Largest single chunk | < 100KB | Split if exceeded |
| First-party JS | < 100KB | Your code only, excluding node_modules |

### Core Web Vitals Targets
| Metric | Good | Needs Improvement | Poor |
|--------|------|-------------------|------|
| **LCP** (Largest Contentful Paint) | < 2.5s | 2.5s – 4.0s | > 4.0s |
| **FID** (First Input Delay) | < 100ms | 100ms – 300ms | > 300ms |
| **CLS** (Cumulative Layout Shift) | < 0.1 | 0.1 – 0.25 | > 0.25 |
| **INP** (Interaction to Next Paint) | < 200ms | 200ms – 500ms | > 500ms |
| **TTFB** (Time to First Byte) | < 800ms | 800ms – 1800ms | > 1800ms |

### Lighthouse Thresholds
| Category | Minimum Score |
|----------|---------------|
| Performance | > 90 |
| Accessibility | > 95 |
| Best Practices | > 95 |
| SEO | > 95 |

### Animation Frame Budgets
| Context | Frame Budget | Target FPS |
|---------|-------------|------------|
| Standard UI animations | 16.6ms per frame | 60fps |
| Heavy pages (3D + scroll) | 33.3ms per frame | 30fps acceptable on mobile |
| Composition-only (transform/opacity) | 8ms per frame | 120fps capable |

---

## 2. Code Splitting

### Dynamic Import for Heavy Libraries
```tsx
// Split Three.js / R3F out of the main bundle
import dynamic from "next/dynamic";

const Scene3D = dynamic(() => import("@/components/Scene3D"), {
  ssr: false,
  loading: () => <div className="h-screen bg-zinc-950 animate-pulse" />,
});

// The Scene3D component (and Three.js) only loads when this component renders
```

### Route-Based Splitting (Automatic)
Next.js App Router automatically code-splits per route. Each `page.tsx` is a separate chunk.

### Component-Level Splitting
```tsx
import dynamic from "next/dynamic";

// Split heavy components that aren't needed immediately
const PricingCalculator = dynamic(() => import("@/components/PricingCalculator"));
const TestimonialCarousel = dynamic(() => import("@/components/TestimonialCarousel"));

// These load only when rendered, reducing initial bundle
```

### Conditional Splitting
```tsx
// Load heavy features only when needed
const [showEditor, setShowEditor] = useState(false);

const CodeEditor = dynamic(() => import("@/components/CodeEditor"), {
  loading: () => <div className="h-64 bg-zinc-900 animate-pulse rounded-lg" />,
});

return (
  <>
    <button onClick={() => setShowEditor(true)}>Open Editor</button>
    {showEditor && <CodeEditor />}
  </>
);
```

---

## 3. Image & Font Optimization

> See [`nextjs-app-router-patterns`](../nextjs-app-router-patterns/SKILL.md) §6 for `next/image` and `next/font` implementation patterns.
> See [`ecc-hydration-performance`](../frontend/ecc-hydration-performance.md) for CLS-safe font fallback overrides and preloading strategy.

---

## 4. Lazy Loading Patterns

### Intersection Observer for Heavy Sections
```tsx
"use client";
import { useRef, useState, useEffect } from "react";

function useLazyLoad() {
  const ref = useRef<HTMLDivElement>(null);
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsVisible(true);
          observer.disconnect(); // Stop observing after first intersection
        }
      },
      { rootMargin: "200px" } // Start loading 200px before it's visible
    );

    if (ref.current) observer.observe(ref.current);
    return () => observer.disconnect();
  }, []);

  return { ref, isVisible };
}

// Usage:
export function HeavySection() {
  const { ref, isVisible } = useLazyLoad();

  return (
    <div ref={ref} className="min-h-[400px]">
      {isVisible ? <ActualContent /> : <Skeleton />}
    </div>
  );
}
```

### CSS content-visibility
```css
/* Sections below the fold — browser skips rendering until near viewport */
.lazy-section {
  content-visibility: auto;
  contain-intrinsic-size: 0 600px; /* Estimated height — prevents layout shift */
}
```

---

## 5. Measuring Performance

### Browser DevTools Audit
```
Chrome DevTools → Performance tab → Record → Scroll through page → Stop

Key metrics to check:
- Long tasks (> 50ms) — these block the main thread
- Layout shifts — yellow markers in the timeline
- Paint events — green markers (should be minimal)
- JS execution time — blue markers (should be < 16ms per frame)
```

### Lighthouse CLI
```bash
npx lighthouse https://localhost:3000 --output=json --output-path=./lighthouse.json
# Or in Chrome DevTools: Lighthouse tab → Generate report
```

### Performance API (Runtime Measurement)
```tsx
// Measure a specific operation
performance.mark("animation-start");
// ... animation code ...
performance.mark("animation-end");
performance.measure("animation", "animation-start", "animation-end");

const measure = performance.getEntriesByName("animation")[0];
console.log(`Animation took ${measure.duration.toFixed(2)}ms`);
// If > 16ms, you're dropping frames
```

### Web Vitals Reporting
```tsx
// app/layout.tsx
import { Analytics } from "@vercel/analytics/react";
import { SpeedInsights } from "@vercel/speed-insights/next";

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        {children}
        <Analytics />
        <SpeedInsights />
      </body>
    </html>
  );
}
```

---

## 6. Optimization Checklist

### Pre-Ship Audit
- [ ] `next build` output shows no chunks > 100KB
- [ ] Lighthouse Performance score > 90
- [ ] LCP < 2.5s on mobile (throttled 3G in DevTools)
- [ ] CLS < 0.1 (no layout shifts after load)
- [ ] No long tasks > 50ms in Performance timeline
- [ ] All below-fold images lazy loaded
- [ ] All heavy components (3D, editors, charts) dynamically imported
- [ ] Font files ≤ 3, total weight < 150KB
- [ ] `content-visibility: auto` on below-fold sections
- [ ] Animation frame time < 16ms (check in Performance tab)

### Three.js / WebGL Specific
- [ ] Canvas loaded with `dynamic(..., { ssr: false })`
- [ ] DPR capped at `[1, 1.5]`
- [ ] Mobile fallback renders static image instead of 3D
- [ ] Post-processing disabled on mobile
- [ ] Model files Draco-compressed, < 5MB

### GSAP / Framer Motion Specific
- [ ] Only `transform` and `opacity` animated (no layout properties)
- [ ] `will-change: transform` on animated elements (sparingly — max 5 per page)
- [ ] No competing animation libraries in the same component tree

## Output Format / Delivery
- Performance report with Lighthouse scores, Core Web Vitals target verification, and bundle budgets.

## Behavior Rules
- Enforce strict size budgets for JS/CSS and Draco-compression for 3D files.
- Always use Dynamic Imports for heavy libraries like R3F/GSAP/Three.js.

## Maintenance Notes
- Updated to match structural guidelines in June 2026.
