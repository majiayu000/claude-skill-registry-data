---
name: orbit-lighthouse
description: Lighthouse Core Web Vitals scoring for a WordPress plugin's frontend output and admin pages. Reports Performance, Accessibility, Best Practices, SEO scores with detailed breakdowns of LCP / FCP / TBT / CLS / TTI. Use when the user says "Lighthouse", "Core Web Vitals", "performance score", "LCP / CLS / TBT", "PageSpeed", or wants frontend perf metrics.
---

# 🪐 orbit-lighthouse — Core Web Vitals scoring

Google's quality bar for the modern web. Lighthouse measures what real users feel.

---

## Quick start

```bash
# Full report (opens in browser)
lighthouse http://localhost:8881 \
  --output=html --output-path=reports/lighthouse/report.html \
  --chrome-flags="--headless" --quiet
open reports/lighthouse/report.html

# Just the scores
lighthouse http://localhost:8881 --output=json --quiet \
  | python3 -c "import json,sys; d=json.load(sys.stdin); \
    print('Perf:', int(d['categories']['performance']['score']*100), \
    '| A11y:', int(d['categories']['accessibility']['score']*100), \
    '| BP:', int(d['categories']['best-practices']['score']*100), \
    '| SEO:', int(d['categories']['seo']['score']*100))"
```

Or via gauntlet (Step 7):
```bash
bash scripts/gauntlet.sh --plugin . --mode full
```

---

## Targets

| Metric | Min | Target | What it means |
|---|---|---|---|
| Performance | 75 | 85+ | Overall weighted score |
| **LCP** | < 2.5s | < 2.0s | Largest Contentful Paint |
| **FCP** | < 1.8s | < 1.5s | First Contentful Paint |
| **TBT** | < 200ms | < 100ms | Total Blocking Time |
| **CLS** | < 0.1 | 0 | Cumulative Layout Shift |
| **TTI** | < 3.8s | < 3.0s | Time to Interactive |
| Accessibility | 95 | 100 | WCAG 2.2 AA |
| Best Practices | 95 | 100 | HTTPS, no console errors, modern APIs |
| SEO | 95 | 100 | Meta tags, indexable |

Performance < 75 → block release.

---

## Run on every visual URL

```bash
URLS=$(jq -r '.visualUrls | join(" ")' qa.config.json)
for url in $URLS; do
  lighthouse "http://localhost:8881$url" \
    --output=json \
    --output-path=reports/lighthouse/$(basename "$url").json \
    --quiet --chrome-flags="--headless"
done
```

---

## Multi-config (mobile + desktop + admin)

```bash
# Mobile (default for Lighthouse)
lighthouse http://localhost:8881 --preset=desktop --output=json

# Slow 3G + 4× CPU throttle (worst case)
lighthouse http://localhost:8881 \
  --throttling-method=devtools \
  --throttling.cpuSlowdownMultiplier=4 \
  --throttling.requestLatencyMs=150 \
  --throttling.downloadThroughputKbps=1638 \
  --throttling.uploadThroughputKbps=750
```

---

## Lighthouse CI (LHCI) — track scores over time

```bash
# Already in install-power-tools.sh
npm i -g @lhci/cli

# Run + assert thresholds
lhci autorun \
  --collect.url=http://localhost:8881 \
  --collect.url=http://localhost:8881/sample-page \
  --assert.preset=lighthouse:recommended

# Fail CI if any URL drops below threshold
```

Config: `config/lighthouserc.json` — already shipped with Orbit thresholds.

---

## What this skill catches

### Frontend
- Slow LCP from oversized images (use `loading="lazy"`, modern formats)
- High TBT from long JS tasks (split bundles, defer)
- CLS from images / ads / late-loaded fonts (set width/height attrs)
- Render-blocking resources (move CSS to async, defer JS)
- Unused JavaScript (tree-shake, route-split)

### Admin (less common, but real)
- Settings page > 4s load → users abandon
- Admin LCP > 2.5s → editor / settings UI feels janky
- 100+ console errors on admin pages

---

## Common findings + fixes

### "Reduce unused JavaScript — 250 KiB savings"
```bash
npx source-map-explorer assets/js/main.js
# → see exactly what's bloating the bundle
# → tree-shake with webpack/rollup, or split routes
```
Pair with `/orbit-bundle-analysis`.

### "Eliminate render-blocking resources — 350ms savings"
```php
// BAD — blocks render
wp_enqueue_script( 'my-script', '...', [], '1.0', false );  // false = in <head>

// GOOD — load in footer (or use defer)
wp_enqueue_script( 'my-script', '...', [], '1.0', true );  // true = footer
// Or with defer attribute (WP 6.3+):
wp_script_add_data( 'my-script', 'strategy', 'defer' );
```

### "Image format and size — 1.2MB savings"
```html
<!-- BAD -->
<img src="/wp-content/uploads/hero.png">

<!-- GOOD -->
<img src="/wp-content/uploads/hero.webp" loading="lazy" width="1200" height="600">
```

### "Largest Contentful Paint — 3.2s"
LCP element is usually a hero image or H1. Inline its CSS, preload the font, set its image as `fetchpriority="high"`.

```html
<link rel="preload" as="image" href="/hero.webp" fetchpriority="high">
```

### "Cumulative Layout Shift — 0.34"
- Set `width` + `height` on every `<img>`
- Reserve space for ads / embeds
- Avoid fonts that swap drastically (use `font-display: optional` or self-host)

---

## Output

`reports/lighthouse/lh-<timestamp>.json` (full data) + `report.html` (visual). The HTML is what you share with PMs.

The gauntlet's master report includes the score in the summary table:
```
✓ Lighthouse: 87 / 100 (LCP: 2.1s, CLS: 0.02, TBT: 95ms)
```

---

## When this misses real perf issues

Lighthouse measures the **rendered page**. It does NOT see:
- Slow PHP hooks (`/orbit-wp-performance`)
- Heavy DB queries (`/orbit-db-profile`)
- Editor performance — Elementor, Gutenberg (`/orbit-editor-perf`)
- Bundle bloat in actual production (`/orbit-bundle-analysis`)

Run all five for complete perf coverage.

---

## CI

```yaml
- run: lighthouse http://localhost:8881 --output=json --output-path=lh.json --quiet --chrome-flags="--headless"
- run: |
    SCORE=$(jq '.categories.performance.score * 100' lh.json | cut -d. -f1)
    if [ "$SCORE" -lt 75 ]; then echo "Lighthouse $SCORE < 75"; exit 1; fi
```

Or use LHCI's built-in assertions (cleaner).
