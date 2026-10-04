---
name: senternet-site-lighthouse
description: Apply performance and Lighthouse optimization decisions to a marketing site.
---

# Lighthouse / PageSpeed Optimization

Achieve Lighthouse scores of Performance ≥94, Accessibility ≥98, Best Practices ≥96, SEO 100 on mobile.

## How to measure

Use the PageSpeed Insights API directly (avoids browser caching noise).

If the site already has a Firebase project, use that project ID for the PSI key work so the `gcloud` commands stay scoped to the current site. All project-specific `gcloud` commands here should include `--project "$PROJECT_ID"`.

### Step 1 — Get a PSI API key

**Auto-create with gcloud (preferred):** Run this to enable the API and create a key restricted to PageSpeed Insights:
```bash
gcloud services enable pagespeedonline.googleapis.com --project "$PROJECT_ID" && \
PSI_KEY=$(gcloud alpha services api-keys create \
  --project "$PROJECT_ID" \
  --display-name="PageSpeed Insights" \
  --api-target=service=pagespeedonline.googleapis.com \
  --format="value(keyString)" 2>/dev/null) && \
echo "PSI_API_KEY=$PSI_KEY"
```
Save the printed key — you'll use it in Step 2. If the `alpha` component isn't installed, gcloud will prompt you to install it.

**No gcloud / manual fallback:**
1. Go to [console.cloud.google.com/apis/credentials](https://console.cloud.google.com/apis/credentials)
2. Click **Create Credentials → API key**
3. Click **Edit key → Restrict key → API restrictions → PageSpeed Insights API**
4. Save the key

### Step 2 — Run the audit

```bash
curl -s "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=https://www.DOMAIN.com/&strategy=mobile&key=YOUR_PSI_API_KEY" | python3 -c "
import json,sys; d=json.load(sys.stdin); lh=d['lighthouseResult']
cats=lh['categories']; audits=lh['audits']
print('Scores:', {k:round(v['score']*100) for k,v in cats.items()})
for m in ['first-contentful-paint','largest-contentful-paint','total-blocking-time','cumulative-layout-shift','speed-index']:
    print(f'  {m}: {audits[m][\"displayValue\"]}')
"
```

After a fresh deploy, wait 10–15 min before measuring — Firebase CDN edge nodes take time to warm up new asset hashes.

## Critical decisions — do not undo without retesting

| Decision | Why | Risk if undone |
|---|---|---|
| `hydrateRoot` in `main.tsx` | Attaches React to prerendered DOM instead of replacing it | LCP jumps to React render time (~3.5s) |
| `will-change: transform` on hero image wrapper | Pre-promotes compositing layer, keeps LCP visible on first frame | LCP regresses ~1s under CPU throttle |
| Hero image in `public/` with stable URL | Allows `<link rel="preload">` in `index.html` to match actual `src` | Preload hint stops matching, LCP worsens |
| GA loaded after `window.load` | Doesn't block FCP/LCP | GA inline → ~1s FCP regression |
| `manualChunks: { 'vendor-react': [...] }` in Rollup | Splits React into parallel-downloadable chunk | Larger single bundle, slower parse |
| `modulepreload` links injected by `htmlPlugin` | Browser fetches JS from `<head>` not end of `<body>` | ~200ms extra JS load latency |
| Animations disabled on mobile via media query | Repaints from opacity animations tank mobile CPU | LCP/Speed Index regressions |

## Performance checklist

### LCP (Largest Contentful Paint — target <2.5s)

- [ ] Hero image placed in `public/` with a stable (unhashed) filename
- [ ] `<link rel="preload" as="image" href="/hero.webp" fetchpriority="high">` in `<head>`
- [ ] Hero `<img>` has `fetchpriority="high"` attribute
- [ ] Hero image is WebP, not PNG or JPG
- [ ] Mobile and desktop hero images preloaded separately with `media` attribute
- [ ] `hydrateRoot` used in `main.tsx` (not `createRoot`)
- [ ] `will-change: transform` on hero image wrapper element

### FCP (First Contentful Paint — target <1.8s)

- [ ] No render-blocking scripts (GA loads after `window.load`)
- [ ] No render-blocking CSS from third-party fonts (use `@fontsource` npm packages instead of Google Fonts CDN, or `font-display: swap`)
- [ ] `<link rel="modulepreload">` for JS chunks injected by `htmlPlugin`
- [ ] `<link rel="preconnect">` for any third-party domains your site contacts on load (API, analytics)

### CLS (Cumulative Layout Shift — target <0.1)

- [ ] All images have explicit `width` and `height` attributes (or CSS `aspect-ratio`)
- [ ] No layout shift from web font loading (`font-display: optional` or FOUT prevention)
- [ ] No content inserted above the fold after load (e.g., cookie banners, header ads)
- [ ] `<meta name="viewport" content="width=device-width, initial-scale=1.0">` is set

### TBT (Total Blocking Time — target <200ms)

- [ ] No heavy synchronous JS on the main thread during startup
- [ ] Third-party scripts (GA, Reddit pixel, Clarity) loaded lazily — not `<script>` in `<head>`
- [ ] Long animation loops or scroll handlers are passive and off main thread
- [ ] `manualChunks` in Rollup splits vendor code into parallel-loadable chunk

### Speed Index

- [ ] No CSS animations with `opacity` or `background-color` on above-the-fold elements during initial load (these force repaints and inflate Speed Index)
- [ ] `border-glow`, `neon-pulse`, and similar animated effects replaced with static styles for the first paint, then enabled after load

## Accessibility checklist (target ≥98)

- [ ] All text uses sufficient contrast ratio (≥4.5:1 for normal text, ≥3:1 for large text)
- [ ] All `<img>` elements have descriptive `alt` text (empty `alt=""` for decorative images)
- [ ] No `<button>` nested inside `<a>` — use styled `<a>` for navigation
- [ ] Interactive elements have `aria-label` when their text content doesn't describe the action
- [ ] FAQ toggles have `aria-expanded` on the controlling button
- [ ] `<nav>` elements have `aria-label="Main navigation"` (or similar)
- [ ] Heading hierarchy: h1 → h2 → h3, no skipped levels
- [ ] Form inputs have associated `<label>` elements

## Best Practices checklist (target ≥96)

- [ ] Security headers set in `firebase.json`: `X-Content-Type-Options`, `X-Frame-Options`, `X-XSS-Protection`, `Referrer-Policy`
- [ ] No mixed content (all resources loaded over HTTPS)
- [ ] Console is clean — no errors or warnings in DevTools
- [ ] Images have correct `width`/`height` to avoid layout shifts

## SEO checklist (target 100)

- [ ] `<meta name="description">` on every page
- [ ] `<link rel="canonical">` on every page
- [ ] `robots.txt` exists and is valid
- [ ] `sitemap.xml` is submitted to Google Search Console
- [ ] All links have descriptive text (no "click here")
- [ ] `<html lang="en">` (or appropriate language code)

## PSI vs local Lighthouse discrepancy

PSI results frequently differ from local runs — this is expected:
1. CDN cold cache after deploy: wait 10–15 min and re-run
2. Geographic variance: PSI hits different CDN PoPs than local
3. Third-party scripts: Lighthouse never fires user events, so lazy-loaded scripts never load

Rule of thumb: if local shows ≥94 and PSI shows <90, it's almost always CDN cache. Wait and re-run.

## Framework: Next.js track

Same score targets, different levers and a different local target.

**Test against `npm run build && npm start`**, not a served `build/` directory. There is no static output directory to serve.

Skip the Vite-specific work — `manualChunks`, `modulepreload` injection, and the `htmlPlugin` do not exist here; code splitting and preloading are the framework's job. The fixes that actually move the numbers on this track:

- **Shrink the client boundary.** The single largest performance lever is how much of the tree is under `'use client'`. Check the build output's First Load JS per route; a marketing page well above ~100 kB usually has a client directive too high up.
- **Check the route table.** Pages marked `ƒ` (dynamic) pay a cold start on first visit and will not hit the LCP target from a scale-to-zero backend. Make them static, or accept `minInstances: 1` in `apphosting.yaml` and say so.
- **`priority` on the LCP image only**, via `next/image`. Multiple priority images compete for bandwidth and delay the one that counts.
- **`next/font` instead of a font CDN `<link>`.** Self-hosting removes a render-blocking third-party request and the flash that comes with it.
- **Third-party scripts on `strategy="lazyOnload"`.** Anything on `beforeInteractive` blocks hydration.
- **Cold starts are a real Lighthouse variable.** A scale-to-zero backend can show a first-request TTFB of a second or more that has nothing to do with the page. Run the audit twice and use the warm number, but do not pretend the cold number is not what a first visitor gets.

Headers and caching fixes go in `next.config.ts` `headers()`, not `firebase.json`.

See `/senternet-site-framework` for the full convention map.
