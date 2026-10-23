---
name: web-vitals-inp-deep
description: "Deep INP (Interaction to Next Paint) testing: decomposes input delay, processing duration, and presentation delay via the web-vitals/attribution build, asserts per-interaction INP budgets in Playwright using PerformanceObserver plus the web-vitals visibilitychange flush, and identifies long tasks blocking the main thread. Use when a page feels unresponsive while LCP and CLS are green, or to gate key interactions (form submit, modal open, route change) under an INP budget in CI. Covers interactions only - for page-load Web Vitals gating use lighthouse-perf; for service-worker cache-strategy latency use the qa-pwa plugin's service-worker skills."
metadata:
  keywords: "web-vitals, inp, core-web-vitals, responsiveness, performance"
  version: "1.1.11"
---

# web-vitals-inp-deep

INP is *"the time from the start of the interaction to the moment the
next frame is fully presented"* per the [INP web.dev article].
Thresholds at the 75th percentile of page loads:

- **Good:** ≤ 200 ms
- **Needs Improvement:** 201 - 500 ms
- **Poor:** > 500 ms

## When to use

- A page reports "feels slow" but LCP and CLS are green - INP is
  the missing dimension.
- Pre-merge gate: assert key user interactions (form submit, modal
  open, route transition) stay under budget.
- Field debugging: correlate field INP outliers with specific
  interaction types.

## Step 1 - Install the web-vitals library

```bash
npm install web-vitals
```

Per the [INP web.dev article].

## Step 2 - Measure INP in lab (per interaction)

```ts
import { onINP } from 'web-vitals';

onINP((metric) => {
  console.log('INP:', metric.value, metric);
  // metric.attribution gives interaction details (target, eventType, etc.)
});
```

Per the [INP web.dev article]: the `web-vitals` library handles
edge cases (BFCache restoration, visibility changes) that raw
`PerformanceObserver` does not.

## Step 3 - Decompose INP

INP encompasses three components per the [INP web.dev article]:

1. **Input Delay** - time before event handlers begin (often long
   tasks blocking main thread)
2. **Processing Duration** - time for all event handler callbacks
   to run
3. **Presentation Delay** - time until browser paints the next frame

Use `metric.attribution` (provided by web-vitals INP attribution
build) to identify which component dominates:

```ts
import { onINP } from 'web-vitals/attribution';

onINP((metric) => {
  console.log('Total INP:', metric.value);
  console.log('Input delay:', metric.attribution.inputDelay);
  console.log('Processing duration:', metric.attribution.processingDuration);
  console.log('Presentation delay:', metric.attribution.presentationDelay);
  console.log('Long animation frame:', metric.attribution.longAnimationFrameEntries);
});
```

## Step 4 - Playwright assertion per interaction

```ts
import { test, expect } from '@playwright/test';

test('modal open INP under 200ms', async ({ page }) => {
  await page.addInitScript({ path: 'node_modules/web-vitals/dist/web-vitals.iife.js' });
  await page.goto('https://localhost:3000');

  await page.evaluate(() => {
    (window as any).__inpValues = [];
    (window as any).webVitals.onINP((m: any) => {
      (window as any).__inpValues.push(m.value);
    });
  });

  // The interaction under test
  await page.click('[data-testid="open-modal"]');
  await page.waitForSelector('[role="dialog"]');

  // Force INP to flush. web-vitals finalizes INP inside its own
  // visibilitychange handler, which reads document.visibilityState
  // synchronously (per the [web-vitals README]). Redefine the property to
  // 'hidden' FIRST, THEN dispatch the event: if you dispatch first, the
  // handler still sees 'visible' and never reports.
  await page.evaluate(() => {
    Object.defineProperty(document, 'visibilityState', {
      configurable: true,
      get: () => 'hidden',
    });
    document.dispatchEvent(new Event('visibilitychange'));
  });

  const inps = await page.evaluate(() => (window as any).__inpValues);
  const max = Math.max(...inps);
  expect(max).toBeLessThan(200);
});
```

## Step 5 - Identify long tasks blocking main thread

```ts
test('no long tasks > 50ms during route change', async ({ page }) => {
  // Install the observer BEFORE navigation and push entries onto a
  // window-scoped array. A closure-local array would never reach
  // window.__longTasks, so the later read returns [] and the assertion
  // passes vacuously regardless of real long tasks.
  await page.addInitScript(() => {
    (window as any).__longTasks = [];
    const obs = new PerformanceObserver((list) => {
      for (const e of list.getEntries()) {
        (window as any).__longTasks.push({
          name: e.name, duration: e.duration, startTime: e.startTime,
        });
      }
    });
    // 'longtask' is the Long Tasks API entry type; buffered:true replays
    // tasks recorded before the observer attached (per [MDN longtask]).
    obs.observe({ type: 'longtask', buffered: true });
  });

  await page.goto('https://localhost:3000');
  await page.click('[data-testid="route-link"]');
  await page.waitForLoadState('networkidle');

  const blocking = (await page.evaluate(() => (window as any).__longTasks ?? []))
    .filter((t: any) => t.duration > 50);
  expect(blocking).toEqual([]);
});
```

The richer successor to Long Tasks is the Long Animation Frames (LoAF) API
(`type: 'long-animation-frame'`), but it is not yet Baseline across browsers
per [MDN LoAF], so attach it as a separate, guarded observer rather than
relying on it alone.

## Step 6 - CrUX field data correlation

Lab + field don't always match. Pair lab tests with CrUX queries:

```bash
# CrUX REST API - key from the environment, sent as a header
curl -X POST 'https://chromeuxreport.googleapis.com/v1/records:queryRecord' \
  -H "x-goog-api-key: $CRUX_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"url":"https://yoursite.com/","metrics":["interaction_to_next_paint"]}'
```

Send the key in the `x-goog-api-key` header rather than a `?key=` query
parameter: per [Google API keys], a key in the URL is exposed to theft through
URL scans.

Field 75th percentile INP ≤ 200 ms = "Good" per the [INP web.dev
article]. Lab passing + field failing = sample population mismatch
(real devices slower, real interactions less predictable).

## Anti-patterns

| Anti-pattern | Why it fails | Fix |
|---|---|---|
| Use raw `PerformanceObserver` for INP | Misses BFCache, visibility-change reporting | Use `web-vitals` library (Step 2) |
| Test INP only on `click` events | INP measures all interactions; tap, keypress also count | Test representative interactions per type |
| Use desktop CPU 4× speed | Hides regressions; field is mobile + slower CPU | Throttle CPU 4 - 6× in Playwright config |
| Assert single sample | INP is jittery; one bad sample fails CI | Run interaction N times; assert P75 ≤ budget |
| Fix INP by fragmenting handlers with `setTimeout(0)` | Hides yield, doesn't reduce work | Actually reduce processing duration via deferral patterns |

## Limitations

- INP became the official Core Web Vital in March 2024 (replacing
  FID). Some older audit tools still report FID - verify the tool
  uses INP.
- Service worker interception adds presentation-delay variance
  (cache miss vs hit). Pin to a known cache state in tests. Testing the
  cache strategy itself is out of scope here: use the qa-pwa plugin's
  service-worker skills.
- `attribution` API requires the `web-vitals/attribution` build
  bundle, not the default.

## References

- [INP web.dev article] - definition, thresholds, decomposition,
  measurement via `web-vitals` library
- [web-vitals README] - attribution build, `onINP`, and the
  visibilitychange flush behavior
- [MDN longtask] - Long Tasks API entry type and buffered observe
- [MDN LoAF] - Long Animation Frames API (richer, not yet Baseline)
- [Google API keys] - "Using an API key with REST": the `x-goog-api-key`
  header, and why a key in the URL is exposed

[INP web.dev article]: https://web.dev/articles/inp
[web-vitals README]: https://github.com/GoogleChrome/web-vitals#readme
[MDN longtask]: https://developer.mozilla.org/en-US/docs/Web/API/PerformanceLongTaskTiming
[MDN LoAF]: https://developer.mozilla.org/en-US/docs/Web/API/PerformanceLongAnimationFrameTiming
[Google API keys]: https://docs.cloud.google.com/docs/authentication/api-keys-use
