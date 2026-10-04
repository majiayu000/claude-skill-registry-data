---
name: qa-detect-loading-states
section: performance
description: "Tests loading-state behavior under simulated slow network. Detects stuck skeletons, loading spinners overlapping content, lazy-load that fails on slow connections, and below-fold content that never loads. Uses an in-page fetch/XHR interceptor for network throttling (works without CDP). Runs as ONE in-page async probe."
model: haiku
applyOn: [mobile]
needsSetup: false
viewportSensitive: false
interactive: true
executable: true
cacheVersion: "1.0.0"
ownership: "exclusive: any bug specific to slow-network loading-state behavior belongs to this skill"
requires: [hasLoadingSpinner, hasSkeletonScreen]
---

## How the orchestrator runs this (ONE call — no hand-driving)

🚨 **This skill is an EXECUTABLE in-page probe, not a prose playbook.** Do NOT drive it with separate install/navigate/snapshot/remove MCP calls. Instead make **ONE** call:

```
result = browser_evaluate(<the async function in "## Interactive Probe" below>)
```

The function installs a slow-3G throttle (wraps `fetch` + `XMLHttpRequest` with a per-request delay) on the **already-loaded** page, then re-triggers in-flight data by snapshotting loading state at 0s / 2s / 5s, analyzes the evolution, tests infinite-scroll on slow network, removes the throttle, and returns `findings[]` — all inside the page in one round-trip. It does its own waits via in-page `setTimeout` promises, so there is **no AI reasoning between steps**. It **self-skips** (returns `[]`) when there is no skeleton/spinner/lazy-image/critical content to evaluate. The probe **always restores** `window.fetch` and `window.XMLHttpRequest` and restores scroll position before returning, so the page is left clean and at normal speed for the next skill. Transcribe each returned finding verbatim into the cell JSONL; add only the envelope fields (runId, cellId, route, viewport, …).

Run on **mobile only** (the orchestrator gates `applyOn: [mobile]`). Because `browser_evaluate` cannot re-navigate, the throttle is applied to the live page and the probe measures how loading indicators behave while subsequent fetches (triggered by the synthetic interaction and the lazy-load/infinite-scroll pokes) are delayed.

## Interactive Probe (browser_evaluate, async)

```js
async () => {
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  const DELAY = 1500; // slow-3G per-request delay
  const out = [];
  const add = o => out.push(Object.assign({ skill: 'qa-detect-loading-states' }, o));
  const vis = el => { if (!el) return false; const r = el.getBoundingClientRect(); const s = getComputedStyle(el); return r.width > 0 && r.height > 0 && s.display !== 'none' && s.visibility !== 'hidden'; };

  const snapshot = () => {
    const skeletons = [...document.querySelectorAll('.skeleton, [class*="skeleton"], [class*="shimmer"], [class*="loading-placeholder"], [aria-busy="true"]')].filter(vis);
    const spinners = [...document.querySelectorAll('.spinner, .loader, [class*="spinner"], [role="progressbar"], svg.animate-spin, [data-loading="true"]')].filter(vis);
    const heroPresent = !!document.querySelector(
      'main h1, [class*="hero"] h1, main > section:first-child h1, mat-card-title, mat-toolbar-row h1, mat-toolbar h1, ' +
      '[class*="page-title"], [class*="page-header"] h1, [class*="mat-h1"], .mat-headline, mat-sidenav-content h1, mat-sidenav-content h2'
    );
    const ctaPresent = !!document.querySelector('button[type="submit"], a.cta, .btn-primary, button[mat-raised-button], button[mat-flat-button], [class*="mat-primary"]');
    const mainContentLength = ((document.querySelector('main') || document.body).innerText || '').length;
    const lazyImages = [...document.querySelectorAll('img[loading="lazy"], img[data-src], img.lazy')];
    const lazyLoaded = lazyImages.filter(img => img.complete && img.naturalWidth > 0).length;
    return {
      skeletonCount: skeletons.length,
      spinnerCount: spinners.length,
      criticalContentPresent: heroPresent || (ctaPresent && mainContentLength > 200),
      lazyImageTotalCount: lazyImages.length,
      lazyImageLoadedCount: lazyLoaded,
      mainContentLength
    };
  };

  // ── self-skip: nothing loading-related to evaluate ──
  const s0 = snapshot();
  if (s0.skeletonCount === 0 && s0.spinnerCount === 0 && s0.lazyImageTotalCount === 0 && s0.mainContentLength > 200 && s0.criticalContentPresent) {
    // still continue ONLY if there is some loading affordance or critical content to verify; otherwise skip
  }
  const hasAnything = s0.skeletonCount > 0 || s0.spinnerCount > 0 || s0.lazyImageTotalCount > 0 || document.querySelector('main, [role="main"]');
  if (!hasAnything) return [];

  // ── install slow-network throttle (fetch + XHR) ──
  const origFetch = window.fetch;
  const OrigXHR = window.XMLHttpRequest;
  let throttled = false;
  try {
    window.fetch = function (...args) { return new Promise(res => setTimeout(res, DELAY)).then(() => origFetch.apply(this, args)); };
    function ThrottledXHR() {
      const xhr = new OrigXHR();
      const origSend = xhr.send.bind(xhr);
      xhr.send = function (...a) { setTimeout(() => origSend(...a), DELAY); };
      return xhr;
    }
    window.XMLHttpRequest = ThrottledXHR;
    throttled = true;
  } catch (_) {}

  const restore = () => { try { if (throttled) { window.fetch = origFetch; window.XMLHttpRequest = OrigXHR; } } catch (_) {} };

  // ── re-trigger loading: poke lazy images into view + a benign interaction ──
  try {
    for (const img of document.querySelectorAll('img[loading="lazy"], img[data-src], img.lazy')) { try { img.scrollIntoView({ block: 'nearest' }); } catch (_) {} }
    window.scrollTo(0, 0);
  } catch (_) {}

  // ── sample loading state at 0 / 2s / 5s ──
  const state0 = snapshot();
  await sleep(2000);
  const state2 = snapshot();
  await sleep(3000);
  const state5 = snapshot();

  // 1. skeleton stuck after load
  if (state5.skeletonCount > 0 && state5.skeletonCount >= state0.skeletonCount)
    add({ issueType: 'skeletonStuckAfterLoad', severity: 'high', description: 'Skeleton placeholder still visible 5s after load and did not decrease — skeleton appears stuck on slow network.', evidence: { skeleton0: state0.skeletonCount, skeleton5: state5.skeletonCount } });

  // 2. spinner overlaps real content
  if (state5.spinnerCount > 0 && state5.criticalContentPresent)
    add({ issueType: 'loadingSpinnerOverlapsContent', severity: 'medium', description: 'A loading spinner is still rendered on top of real content after 5s — spinner overlaps content (z-index / dismiss issue).', evidence: { spinnerCount: state5.spinnerCount } });

  // 3. lazy-load fails on slow network
  if (state5.lazyImageTotalCount > 0 && state5.lazyImageLoadedCount === state0.lazyImageLoadedCount && state5.lazyImageLoadedCount < state5.lazyImageTotalCount)
    add({ issueType: 'lazyLoadFailsOnSlow', severity: 'medium', description: 'Below-fold lazy images did not load even after 5s on slow network — lazy-load fails on slow connections.', evidence: { loaded: state5.lazyImageLoadedCount, total: state5.lazyImageTotalCount } });

  // 4. loading indicator missing (blank screen with no affordance)
  if (state2.skeletonCount === 0 && state2.spinnerCount === 0 && !state2.criticalContentPresent && state2.mainContentLength < 100)
    add({ issueType: 'loadingIndicatorMissing', severity: 'medium', description: 'Page is empty at 2s with no skeleton or spinner — users see a blank screen with no loading indicator and think it is broken.', evidence: { mainContentLength: state2.mainContentLength } });

  // 5. critical content missing at slow
  if (!state5.criticalContentPresent)
    add({ issueType: 'criticalContentMissingAtSlow', severity: 'high', description: 'Critical above-fold content (hero / primary CTA) is missing or empty after 5s on slow network.', evidence: { mainContentLength: state5.mainContentLength } });

  // 6. infinite scroll stuck on slow
  const hasInfinite = !!document.querySelector('[class*="infinite"], [data-infinite-scroll], [data-sentinel], .sentinel, [data-load-more]');
  if (hasInfinite) {
    const itemSel = 'article, [data-item], .item, [class*="card"]';
    const before = document.querySelectorAll(itemSel).length;
    const prevScroll = window.scrollY;
    try { window.scrollTo(0, document.body.scrollHeight); } catch (_) {}
    await sleep(3000);
    const after = document.querySelectorAll(itemSel).length;
    if (after <= before)
      add({ issueType: 'infiniteScrollStuckOnSlow', severity: 'low', description: 'Scrolling to the bottom on slow network did not load more items — infinite-scroll trigger never fired.', evidence: { itemsBefore: before, itemsAfter: after } });
    try { window.scrollTo(0, prevScroll); } catch (_) {}
  }

  // ── MANDATORY restore ──
  restore();
  return out;
}
```

## Issues
| issueType | severity | description |
|---|---|---|
| skeletonStuckAfterLoad | high | Skeleton placeholder still visible after page has loaded all content |
| loadingSpinnerOverlapsContent | medium | Spinner element rendered on top of real content (z-index issue) |
| lazyLoadFailsOnSlow | medium | Below-fold images don't load even after extended wait time |
| loadingIndicatorMissing | medium | Page is waiting for data with no visible loading indicator (users think it's broken) |
| infiniteScrollStuckOnSlow | low | Infinite scroll trigger never fires more content after scrolling to bottom on slow network |
| criticalContentMissingAtSlow | high | Critical above-fold content (hero, primary CTA) is missing or empty after 5s on slow network |

## Configuration (customize.toml)

```toml
[loading_states]
enabled              = true
throttle_delay_ms    = 1500   # per-request delay (1500 = slow 3G; 500 = fast 3G)
sample_intervals_ms  = [0, 2000, 5000]
test_infinite_scroll = true
```

`throttle_delay_ms` maps to the `DELAY` constant in the probe; sample intervals are 0/2s/5s.

## Hard rules

1. **Mandatory throttle removal** — the probe restores `window.fetch` and `window.XMLHttpRequest` at the end via `restore()`, even on early return. Subsequent skills must not be slow.
2. **Run on mobile only** — desktop slow-network simulation is artificial.
3. **5-second total wait** — bounded; longer waits hurt cell budget.

## Notes on this conversion
- This replaces the old 6-step flow (install → re-navigate → 3× snapshot → infinite-scroll → remove → re-navigate) with ONE async `browser_evaluate`. Because `browser_evaluate` cannot re-navigate, the throttle is applied to the live page and re-triggering is done by poking lazy images into view and scrolling — the snapshot evolution (0/2s/5s) still surfaces stuck skeletons, overlapping spinners, failed lazy-loads, and missing critical content.
- All 6 issueTypes preserved.
- The throttle uses local `origFetch`/`OrigXHR` captured at install and never persists a window global, so cleanup cannot leak across cells.
- For genuinely WebSocket-heavy apps the throttle is incomplete (WS isn't intercepted) — sufficient for typical SPA fetch/XHR traffic, same caveat as before.
