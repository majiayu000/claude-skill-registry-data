---
name: frontend-performance
description: This skill should be used when a frontend feels slow, fails Core Web Vitals, has a large bundle, or needs performance optimization. Trigger phrases include "make it faster", "improve performance", "Core Web Vitals", "LCP", "INP", "CLS", "reduce bundle size", "code splitting", "lazy load", "it's slow to load", "optimize images", "bundle too big", "Lighthouse score". It targets the real Core Web Vitals thresholds with stack-specific fixes for React + Vite + Vercel.
---

# Frontend Performance

This skill makes a React + Vite app hit the Core Web Vitals bar — the same metrics Google uses for ranking and that users feel as "fast." It optimizes against real thresholds, not vibes.

Analogy: shipping a fast app is like packing for a flight. You don't drag every possession to the gate — you pack the carry-on with what's needed now (above-the-fold) and check the rest (lazy-load below-the-fold). Overpacking the initial bundle is what makes the page heavy.

## The targets (field data, 75th percentile)

- **LCP < 2.5s** — largest content paint.
- **INP < 200ms** — interaction to next paint (replaced FID in March 2024).
- **CLS < 0.1** — cumulative layout shift.

## Discovery (max 3 questions, only if unknown)

1. What's slow — first load (LCP/bundle) or interactions (INP)?
2. Do you have field data (real users) or only a Lighthouse lab score?
3. What's the biggest payload — JS bundle, images, or fonts?

## Step 1 — Measure real users first

Install `web-vitals` (attribution build) and report `onLCP/onINP/onCLS` to your analytics. **Lab tools (Lighthouse) miss field INP** — optimize against real-user data, not just a local score. The Vercel Speed Insights package gives this with no backend.

## Step 2 — Cut the bundle

- **Route-level code splitting** with `React.lazy` + `<Suspense>`. Lazy-load below-the-fold and modal/dialog components so the initial bundle ships only above-the-fold code.
- **Split vendors** in `vite.config.ts` via `build.rollupOptions.output.manualChunks` (separate `react`/`react-dom`, charts, icons) for long-term cache hits.
- **Keep the largest initial chunk under ~200KB gzipped.** Treat Vite's "chunks larger than 500KB" warning as a **budget failure**, not a suggestion.
- **Enforce the budget in CI** with `size-limit`; fail the build on regression. Inspect with `vite-bundle-visualizer`.
- **Tree-shake** via named imports; prefer `lucide-react` over monolithic icon packs.

## Step 3 — Fix LCP

- Preload the LCP image: `<link rel="preload" fetchpriority="high">`. **Never lazy-load the hero.**
- Serve images as **AVIF/WebP** through Vercel image optimization; always set explicit `width`/`height` (or `aspect-ratio`) to prevent CLS.
- Self-host or `preconnect` fonts; use `font-display: swap`.

## Step 4 — Fix INP

- Break up long tasks; defer non-critical JS.
- Use `useTransition` / `startTransition` for non-urgent React updates so input handlers stay responsive.
- Avoid synchronous work inside input/click handlers.

## Step 5 — Fix CLS

- Reserve space for images, ads, and embeds (explicit dimensions / `aspect-ratio`).
- Don't inject content above existing content after load.
- Animate only `transform`/`opacity` (GPU-composited) — never `width`/`height`/`top`/`left`, which trigger layout and hurt both CLS and INP.

## Output

Deliver: a before/after of the three vitals (or the targets if no baseline), the concrete `vite.config.ts` chunk config, the `React.lazy` split points, the image/font fixes, and the CI bundle-budget step.

## Reference

GoogleChrome/web-vitals (~8.5k⭐), web.dev Core Web Vitals, Vite build docs (manualChunks), Vercel image optimization, `size-limit`.
