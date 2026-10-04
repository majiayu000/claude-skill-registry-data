---
name: perf-checklist
description: Performance quick reference — Core Web Vitals, bundle size, rendering, DB queries, caching. Use during implementation or review when perf matters.
---

# Performance checklist

Measure first. Opinion second.

## Frontend — Core Web Vitals

### LCP (Largest Contentful Paint) — ≤ 2.5s
- [ ] Hero image preloaded, sized, `fetchpriority="high"`.
- [ ] Critical CSS inlined or loaded before render-blocking resources.
- [ ] Fonts: `font-display: swap`, preloaded if above the fold.
- [ ] No render-blocking JS on the critical path. `defer` or `async`.

### CLS (Cumulative Layout Shift) — ≤ 0.1
- [ ] `width`/`height` on images and iframes.
- [ ] Reserved space for async content (skeletons, aspect-ratio boxes).
- [ ] No ads / embeds inserted above existing content without reservation.
- [ ] No web-font swap without matching metrics.

### INP (Interaction to Next Paint) — ≤ 200ms
- [ ] No long tasks (>50ms) on interaction paths.
- [ ] Break up work: `scheduler.yield()`, idle callbacks, debounced expensive calcs.
- [ ] Virtualize long lists.
- [ ] Event handlers don't do layout thrash — batch reads then writes.

## Frontend — bundle

- [ ] Tree-shake-friendly imports. `import { x } from 'lib'` — not `import lib from 'lib'` unless required.
- [ ] No `moment` — use `date-fns` or `Temporal` polyfill.
- [ ] No full `lodash` — use `lodash-es` named imports or dropping to native.
- [ ] Code-split routes. Lazy-load heavy components that aren't above the fold.
- [ ] Images: modern formats (WebP/AVIF), responsive `srcset`, served from a CDN.

## Backend — query layer

- [ ] No query inside a loop over a result set (N+1). Batch with `IN`/`JOIN`/dataloader.
- [ ] Every `WHERE` / `ORDER BY` / `JOIN` column used on large tables is indexed.
- [ ] `SELECT *` replaced with specific columns on hot paths.
- [ ] Pagination uses cursors, not offset, on tables that grow.
- [ ] Queries have statement timeouts.

## Backend — request

- [ ] Timeouts on every outbound call.
- [ ] Retries capped with backoff. Never infinite.
- [ ] Circuit breakers for dependencies you can't trust.
- [ ] Response compression enabled (gzip/brotli).
- [ ] Static assets behind a CDN with long `Cache-Control`.

## Cache
- [ ] Layers have clear ownership: browser, CDN, app memory, database.
- [ ] TTLs tied to staleness tolerance, not wish.
- [ ] Invalidation path is obvious. If you can't invalidate it, you can't cache it.
- [ ] `Cache-Control: stale-while-revalidate` for content that tolerates it.

## Instrumentation
- [ ] Real User Monitoring (RUM) for Web Vitals on production.
- [ ] Server: p50/p95/p99 latency per endpoint.
- [ ] Flame graphs available in production (sampled) for hot paths.
- [ ] Alerts on regression — not just absolute thresholds.

## Common mistakes
- "Add caching" to mask a slow query — fix the query.
- Memoizing in React before measuring — often makes things worse.
- Index everything — indexes have a write cost; pick with intention.
- Serve Gzip but forget to compress API JSON — biggest gzip wins are often in the API.
