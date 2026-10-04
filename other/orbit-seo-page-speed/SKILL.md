---
name: orbit-seo-page-speed
description: Google PageSpeed Insights API integration — fetch Core Web Vitals (LCP, INP, CLS) for the live site URL from Google's CrUX dataset, compare your local Lighthouse score to real-user Field Data. Use when the user says "PageSpeed Insights", "PSI", "field data", "CrUX", "real-user metrics".
---

# 🪐 orbit-seo-page-speed — Google PSI integration

Lighthouse measures lab data on YOUR machine. CrUX (Chrome User Experience Report) measures REAL users in the field. They often disagree.

---

## Quick start

```bash
GOOGLE_PSI_API_KEY=your-key \
  bash ~/Claude/orbit/scripts/psi-pull.sh https://my-site.com
```

(API key free at https://console.cloud.google.com — enable PSI API)

---

## What it does

### 1. Fetches PSI data for a URL
```
GET https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=...&key=...
```

Returns:
- Lab data (Lighthouse run server-side)
- Field data (CrUX — real-user metrics from last 28 days)

### 2. Compares lab vs field
**Whitepaper intent:** Lab fast, field slow = real users on slow connections / older devices. Lab and field agree = you're measuring the right thing. Lab slow, field fast = you're testing on a slow box (rare).

```
URL: https://my-site.com/products/

Lab (your Lighthouse):
  Performance: 87 / 100
  LCP: 1.8s
  CLS: 0.05

Field (CrUX, last 28 days, real users):
  LCP p75: 4.2s ❌ (failing Core Web Vitals threshold of 2.5s)
  INP p75: 280ms ⚠ (target < 200ms)
  CLS p75: 0.08 ✓

→ Your lab is misleading. Real users see 4.2s LCP. Investigate slow-network experience.
```

### 3. Origin-level CrUX
Beyond per-URL, get site-wide stats:
```bash
PSI on origin: https://my-site.com (entire origin)
```

Useful when individual pages don't have enough traffic for CrUX (URL needs ~hundreds of visits / 28 days to show in CrUX).

### 4. Mobile + desktop
PSI gives you both. Mobile is usually the worse number — Google ranks mobile-first.

### 5. CWV pass / fail
```
Core Web Vitals pass = ALL of:
- LCP p75 < 2.5s
- INP p75 < 200ms
- CLS p75 < 0.1

If any fails → whole URL "not assessed as good" → may impact ranking.
```

### 6. Historical trend
PSI provides 28-day rolling. To track over time, schedule a weekly run + log to a CSV.

```bash
0 9 * * MON psi-pull.sh https://my-site.com >> psi-history.csv
```

---

## Output

```markdown
# PSI Audit — https://my-site.com/products/ (mobile)

## Lab data (Lighthouse server-side)
- Performance: 87
- LCP: 1.8s
- CLS: 0.05

## Field data (real users, last 28 days)
- LCP p75: 4.2s ❌
- INP p75: 280ms ⚠
- CLS p75: 0.08 ✓

## Verdict
❌ Core Web Vitals NOT passing (LCP fails)

## Causes (top of Lighthouse opportunities)
- Eliminate render-blocking resources (1.2s estimated savings)
- Reduce unused JavaScript (650 KB)
- Properly size images (320 KB)

## Suggested fixes (cross-referenced with Orbit skills)
- Run /orbit-bundle-analysis — find which JS to drop
- Run /orbit-lighthouse — get the full waterfall
- Move plugin's enqueue to footer with `strategy => defer`
```

---

## Pair with

- `/orbit-lighthouse` — local lab Lighthouse
- `/orbit-bundle-analysis` — what's bloating bundle
- `/orbit-perf-cdn` — edge cache for LCP improvement

---

## Sources & Evergreen References

### Canonical docs
- [PageSpeed Insights API](https://developers.google.com/speed/docs/insights/v5/get-started) — how to call
- [Core Web Vitals](https://web.dev/vitals/) — current metrics + thresholds (Google updates yearly)
- [CrUX Report](https://developer.chrome.com/docs/crux/) — field data
- [Web Vitals JS library](https://github.com/GoogleChrome/web-vitals) — collect your own RUM

### Rule lineage
- LCP / FID → INP transition (March 2024) — INP replaced FID as a CWV
- Thresholds 2.5s / 200ms / 0.1 — current as of 2026-04; Google may tighten

### Last reviewed
- 2026-04-29 — re-fetch CWV thresholds quarterly (Google evolves the bar)
