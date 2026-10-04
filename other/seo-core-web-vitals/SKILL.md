---
name: seo-core-web-vitals
description: >
  Dedicated Core Web Vitals deep-dive: pull field data (CrUX / PageSpeed
  Insights), fall back to Lighthouse lab data, score LCP, INP, and CLS against
  Google's thresholds at the 75th percentile, and run per-metric diagnosis
  playbooks with concrete fixes. Use when user says "core web vitals", "CWV",
  "LCP", "INP", "CLS", "page speed metrics", or "field data".
allowed-tools:
  - Read
  - Bash
  - WebFetch
---

# Core Web Vitals Deep-Dive
<!-- Updated: 2026-06-10 -->

Core Web Vitals (CWV) measure real-world loading performance, responsiveness,
and visual stability. Google's position, per
https://developers.google.com/search/docs/appearance/core-web-vitals: CWV are
used by Google's core ranking systems and good CWV is recommended for success
with Search — but good scores alone do **not** guarantee top rankings; there
is more to page experience than CWV, and chasing a perfect score purely for
SEO is not the best use of time.

**INP replaced FID on March 12, 2024.** FID is gone from all Chrome tooling.
Never reference FID as a current metric.

## Thresholds

Each metric is evaluated at the **75th percentile** of real page loads,
segmented by mobile and desktop. A page "passes" CWV when all three metrics
are Good at p75.

| Metric | Measures | Good | Needs Improvement | Poor |
|--------|----------|------|-------------------|------|
| **LCP** (Largest Contentful Paint) | Loading | ≤ 2.5s | 2.5s – 4.0s | > 4.0s |
| **INP** (Interaction to Next Paint) | Responsiveness | ≤ 200ms | 200ms – 500ms | > 500ms |
| **CLS** (Cumulative Layout Shift) | Visual stability | ≤ 0.1 | 0.1 – 0.25 | > 0.25 |

References: https://web.dev/articles/lcp · https://web.dev/articles/inp · https://web.dev/articles/cls · https://web.dev/articles/vitals

## Inputs

| Input | Required | Notes |
|-------|----------|-------|
| URL or origin | Yes | URL-level data preferred; origin-level as fallback |
| Form factor | No | Default: report both mobile (PHONE) and desktop |
| CrUX API key | No | Degrade to PSI API if absent |

## Execution

1. **Field data — CrUX API (preferred, needs an API key):**
   ```bash
   curl -s -X POST "https://chromeuxreport.googleapis.com/v1/records:queryRecord?key=$CRUX_API_KEY" \
     -H 'Content-Type: application/json' \
     -d '{"url": "<url>", "formFactor": "PHONE", "metrics": ["largest_contentful_paint","interaction_to_next_paint","cumulative_layout_shift"]}'
   ```
   Docs: https://developer.chrome.com/docs/crux/api
   - If the URL has insufficient traffic (404 response), retry with `"origin"` instead of `"url"` and note that results are origin-level.
   - **No API key? Degrade gracefully** to step 2 — do not fail.

2. **Field data — PageSpeed Insights API (no key needed for light use):**
   ```bash
   curl -s "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=<url>&category=performance&strategy=mobile"
   ```
   CrUX field data is embedded in `loadingExperience` (URL-level) and
   `originLoadingExperience` (origin-level): p75 percentiles and Good/NI/Poor
   distributions per metric. Docs: https://developers.google.com/speed/docs/insights/v5/get-started

3. **Lab fallback / diagnostics — Lighthouse.** If no field data exists
   (low-traffic page), use the `lighthouseResult` from step 2 or the
   `seo-lighthouse-audit` skill. Label it clearly as **lab data**: lab LCP/CLS
   approximate field values; lab has no INP — use TBT (Total Blocking Time)
   as a rough proxy for interactivity problems, never as a substitute score.

4. **Score each metric** against the thresholds table (Good / Needs
   Improvement / Poor at p75, mobile and desktop separately). Mobile is
   usually worse — lead with it.

5. **Diagnose failing metrics** using the playbooks below, fetching the page
   HTML (`curl -s <url>`) to check for concrete causes (missing
   `fetchpriority`, unsized images, render-blocking tags, heavy third-party
   scripts).

## Diagnosis Playbooks

### LCP — break into the four subparts

| Subpart | Typical share | Fixes |
|---------|---------------|-------|
| **TTFB** (server time to first byte) | ~40% | CDN, edge caching, faster origin, `Server-Timing` header to locate backend cost, avoid redirect chains |
| **Resource load delay** (gap before LCP resource starts downloading) | should be ~0 | `<link rel="preload">` the LCP image/font, `fetchpriority="high"` on the LCP `<img>`, never `loading="lazy"` on the LCP element, avoid CSS background-image for hero |
| **Resource load time** (download duration) | varies | Compress/resize image, modern formats (WebP/AVIF), CDN, `preconnect` to the resource origin |
| **Element render delay** (downloaded but not painted) | should be small | Eliminate render-blocking CSS/JS, inline critical CSS, avoid client-side rendering of the hero |

Full guide: https://web.dev/articles/optimize-lcp ·
[Lighthouse LCP audit](https://developer.chrome.com/docs/lighthouse/performance/lighthouse-largest-contentful-paint)

### INP — find the slow interaction

Common causes and fixes:
- **Long tasks on the main thread** — break work into <50ms chunks, yield with `scheduler.yield()` / `setTimeout`; see [Lighthouse TBT audit](https://developer.chrome.com/docs/lighthouse/performance/lighthouse-total-blocking-time)
- **Heavy event handlers** — debounce, move computation to Web Workers, defer non-visual work until after the next paint
- **Large DOM** — keep under ~1,500 nodes; big DOMs make style/layout recalc slow on every interaction ([dom-size audit](https://developer.chrome.com/docs/lighthouse/performance/dom-size))
- **Third-party JS** — tag managers, ads, chat widgets competing for the main thread; lazy-load or facade them ([third-party-summary](https://developer.chrome.com/docs/lighthouse/performance/third-party-summary))
- **Excessive hydration** (SPA frameworks) — partial/progressive hydration, server components

Full guide: https://web.dev/articles/optimize-inp

### CLS — find what moved

Common causes and fixes:
- **Unsized images/embeds/iframes** — always set `width`/`height` or CSS `aspect-ratio` so the browser reserves space
- **Injected content** (ads, banners, late-loading UI) — reserve slots with fixed min-height; never insert above existing content except on user interaction
- **Web fonts (FOIT/FOUT swaps)** — `font-display: swap` plus `size-adjust`/fallback font metric matching; preload critical fonts ([font-display audit](https://developer.chrome.com/docs/lighthouse/performance/font-display))
- **Animations using layout properties** — animate `transform` instead of `top/left/width/height`

Full guide: https://web.dev/articles/optimize-cls

## Output

```
# Core Web Vitals Report: <url>

## Field Data (CrUX, 75th percentile, last 28 days)
| Metric | Mobile p75 | Desktop p75 | Rating (mobile) |
|--------|-----------|-------------|-----------------|
| LCP | X.Xs | X.Xs | ✅ Good / ⚠️ NI / ❌ Poor |
| INP | XXXms | XXXms | ✅/⚠️/❌ |
| CLS | 0.XX | 0.XX | ✅/⚠️/❌ |

CWV Assessment: PASS / FAIL (all three Good at p75 → pass)
Data level: URL / Origin (note if origin-level fallback was used)

## Distribution (per metric)
Good XX% | Needs Improvement XX% | Poor XX%

## Lab Data (Lighthouse — diagnostics only)
LCP X.Xs · TBT XXXms (INP proxy, not a substitute) · CLS 0.XX

## Diagnosis & Fixes (per failing metric)
### LCP (if failing): subpart breakdown + top 3 fixes
### INP (if failing): suspected cause + top 3 fixes
### CLS (if failing): shifting elements + top 3 fixes

## Context
- CWV is used by Google's ranking systems, but good CWV alone does not
  guarantee rankings — see
  https://developers.google.com/search/docs/appearance/core-web-vitals
- For the broader experience checklist (HTTPS, interstitials, mobile),
  see the seo-page-experience skill.
```
