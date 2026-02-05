---
name: core-web-vitals
description: Measure and optimize Core Web Vitals (LCP, INP, CLS). Use when implementing CWV tracking or debugging performance.
triggers:
  - "core web vitals"
  - "LCP optimization"
  - "INP tracking"
  - "CLS issues"
priority: 1
---

# Core Web Vitals

Measure the three metrics Google uses to assess user experience.

## The Three Metrics

| Metric | Measures | Good | Poor |
|--------|----------|------|------|
| **LCP** | Loading - Largest Contentful Paint | ≤2.5s | >4.0s |
| **INP** | Interactivity - Interaction to Next Paint | ≤200ms | >500ms |
| **CLS** | Visual Stability - Cumulative Layout Shift | ≤0.1 | >0.25 |

## Key Principles

1. **Always include attribution** - Without it, you can't debug
2. **Track all three** - INP replaced FID, don't skip it
3. **Track by route** - Aggregate data hides problems
4. **Alert on poor vitals** - Don't just log, enable alerts

## Attribution = Actionable

| Without | With |
|---------|------|
| "LCP is 3.2s" | "LCP is 3.2s, caused by hero-image.jpg" |
| Can't fix | Actionable |

## Common Causes

### LCP
- Large hero images → Optimize, preload
- Slow TTFB → CDN, improve server
- Render-blocking resources → Defer non-critical

### INP
- Long JS tasks → Break into chunks
- Heavy event handlers → Debounce
- Third-party scripts → Defer, lazy load

### CLS
- Images without dimensions → Set width/height
- Dynamic content → Reserve space
- Web fonts → font-display: optional

## Implementation

See `templates/web-vitals.ts` for production-ready code.

Use Read tool to load template when generating implementation.

## Anti-Patterns

See `references/anti-patterns.md` for:
- CWV without attribution
- Missing INP tracking
- Blocking main thread with telemetry

## Related

- `skills/hydration-performance` - SSR impact on LCP
- `skills/bundle-performance` - JS impact on INP
- `references/core-web-vitals.md` - Deep dive
