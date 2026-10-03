---
name: perf-audit
description: Ranked web performance audit — bundle size, asset weight, loading strategy, render thrash, 3D extras. Trigger on performance, slowness, bundle size, Lighthouse, page weight, or pre-release.
---

# Perf Audit — Measure, Rank, Fix the Top Item

Performance work fails two ways: optimizing without measuring (fixing the wrong thing) and reporting a wall of findings nobody acts on. This pass produces a ranked shortlist with numbers.

## Self-improvement (do this first and last)
1. **At start:** read `learnings.md` in this skill's folder if it exists. Apply relevant lessons.
2. **At end of every use:** append one dated bullet — the biggest win found and its measured impact, or a check that produced noise. Merge instead of duplicating; delete disproven bullets.

## Step 1 — Weigh the payload (static, no server needed)
- Production build → sizes: total JS, total CSS, largest chunks. Flag any single JS chunk > ~150KB gzip and note what's in it (build analyzer if the project has one; otherwise inspect the dist folder).
- **Assets are usually the real weight:** list images/textures/video by size, sorted. Flag: images > ~200KB, anything uncompressed (PNG where WebP/AVIF works), assets larger than their largest displayed size, missing responsive variants.
- Fonts: count families × weights; flag > 4 font files or missing `font-display: swap`.
- Dead weight: grep for imports of libraries used once trivially (a 30KB dep for one function).

## Step 2 — Loading strategy
- What blocks first paint? Render-blocking CSS/JS in `<head>`, synchronous third-party scripts.
- Are below-fold images/sections lazy (`loading="lazy"`, `client:visible` in Astro)?
- Is the largest above-fold image preloaded and prioritized (`fetchpriority="high"`)? That's usually LCP.
- Caching/immutability: hashed filenames on static assets.

## Step 3 — Runtime behavior (needs the app running)
- Long tasks on load and on scroll (DevTools performance trace or judgement from code: heavy work in scroll handlers?).
- Layout thrash: reads (`getBoundingClientRect`, `offsetHeight`) interleaved with writes in the same frame — batch reads then writes, or use IntersectionObserver/rAF.
- Listeners: scroll/resize handlers doing real work directly instead of flagging for rAF; missing `passive: true` on scroll/touch.
- Animations: compositor-friendly (`transform`/`opacity`) vs layout properties (`top/left/width`); `will-change` used sparingly, not sprayed.

## 3D/animation-heavy extras (when applicable)
- Texture memory is the mobile killer: total decoded texture MB (width×height×4 per texture, mipmaps +33%); flag > ~100MB.
- Draw calls per frame (`renderer.info.render.calls`); flag hundreds — merge/instance.
- Pixel ratio capped ≤ 2; render-on-demand for static scenes; zombie render loops after navigation.
- GC hitches: allocation inside the rAF tick.

## Step 4 — Report
Ranked table, max ~7 rows: finding · measured size/impact · fix · effort (S/M/L). Lead with the single highest-impact item and offer to fix it. Don't fix unprompted — the audit is the deliverable unless asked to apply. Gate behavior across session modes: see `mode-kernel`.
