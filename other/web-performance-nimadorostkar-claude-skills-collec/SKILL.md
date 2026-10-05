---
name: web-performance
description: Use when improving page load or runtime performance. Covers Core Web Vitals, bundle and asset optimization, rendering strategy, caching headers, and measuring on real hardware rather than a fast laptop.
metadata:
  category: frontend
  version: 1.0.0
  tags: [performance, core-web-vitals, lcp, inp, bundle]
---

# Web Performance

## Purpose

Make pages fast on the devices people actually use. Performance work without measurement on representative hardware is guesswork, and it is usually spent on the wrong thing.

## When to Use

- Core Web Vitals failing in field data.
- A page that feels slow, or a bundle that has quietly grown.
- Before launching anything that matters commercially.
- Diagnosing jank, layout shift, or slow interactions.

## Capabilities

- Core Web Vitals: LCP, INP, CLS — diagnosis and remediation.
- Bundle analysis and code splitting.
- Image, font, and asset optimization.
- Caching and CDN header configuration.
- Runtime profiling: long tasks, layout thrashing, memory growth.

## Inputs

- Field data (Chrome UX Report, RUM), not just a lab score.
- The bundle, the network waterfall, and a CPU profile.
- The device and network profile of the actual audience.

## Outputs

- A ranked list of fixes with expected impact.
- Before/after measurements on throttled hardware.
- Budgets in CI so the improvement holds.

## Workflow

1. **Measure the field, not the lab** — Lighthouse on a developer laptop tells you nothing about a mid-range Android on 4G. Start with real-user data and reproduce it with 4x CPU throttling and a Slow 4G profile.
2. **Find the LCP element** — It is nearly always a hero image or a heading blocked by a font or a script. Preload it; do not lazy-load it.
3. **Fix INP by breaking up long tasks** — Interaction latency comes from the main thread being busy. Find tasks over 50ms in the profile and yield, defer, or move them off-thread.
4. **Fix CLS by reserving space** — Every image needs `width` and `height` or an `aspect-ratio`. Every ad slot, embed, and late-loading banner needs a reserved box.
5. **Cut the bundle** — Analyze it. One date library, one icon set, or one un-tree-shaken utility library is usually a third of the payload.
6. **Set the cache headers** — Immutable, fingerprinted assets get a one-year `max-age`. HTML gets `no-cache` and revalidates.
7. **Budget it in CI** — Otherwise it regresses within two sprints.

## Best Practices

- Lazy-loading the LCP image makes LCP worse. `loading="lazy"` belongs below the fold, never above it.
- `font-display: swap` prevents invisible text but causes a shift; `size-adjust` with a matched fallback metric prevents both.
- Third-party scripts are the largest performance cost in most real applications, and the least examined. Audit them; load them with `async`, in a worker, or not at all.
- A 200 KB JavaScript bundle costs far more than a 200 KB image: the image decodes off-thread, the JavaScript must be parsed and executed on the main thread.
- Preconnect to critical third-party origins, but only two or three — each one costs a connection.
- Do not optimize what the profile does not show. The bottleneck is rarely where intuition says it is.

## Examples

**Preloading the LCP image and the font that blocks it:**

```html
<link rel="preload" as="image"
      href="/hero-960.avif"
      imagesrcset="/hero-640.avif 640w, /hero-960.avif 960w, /hero-1440.avif 1440w"
      imagesizes="(max-width: 768px) 100vw, 960px"
      fetchpriority="high" />

<link rel="preload" as="font" type="font/woff2"
      href="/fonts/inter-var.woff2" crossorigin />

<img src="/hero-960.avif" width="1440" height="810"
     alt="" fetchpriority="high" />   <!-- dimensions reserve space: no CLS -->
```

**Breaking a long task to fix INP:**

```javascript
// Before: 400ms of blocking work on click. INP is terrible.
button.addEventListener("click", () => {
  const results = items.map(expensiveTransform);   // blocks the main thread
  render(results);
});

// After: yield to the browser between chunks so input stays responsive.
async function processInChunks(items, chunkSize = 50) {
  const out = [];
  for (let i = 0; i < items.length; i += chunkSize) {
    out.push(...items.slice(i, i + chunkSize).map(expensiveTransform));
    await scheduler.yield();   // hand control back; the browser can paint and respond
  }
  return out;
}
```

## Notes

- INP replaced FID as a Core Web Vital in March 2024. It measures every interaction, not just the first, and it is a far harder bar — most sites that passed FID comfortably do not pass INP.
- Compression matters more than minification: Brotli at level 11 on a 300 KB bundle typically beats aggressive minification by a wider margin than the minifier does.
- `content-visibility: auto` skips rendering work for off-screen content and is close to free on long pages. It is one of the highest-value single-property changes available.
