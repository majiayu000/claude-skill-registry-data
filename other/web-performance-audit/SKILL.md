---
name: web-performance-audit
description: Use when a website or web app is slow, Lighthouse or PageSpeed scores are low, Core Web Vitals (LCP, INP, CLS) fail, the bundle is too large, pages load or scroll with jank, or React/Next.js/Vue renders feel sluggish.
---

# Web Performance Audit

## Overview

Tie every fix to the metric it moves. Find the few causes that dominate load time and interaction delay, show where they are in the code, and estimate the gain.

## Method

1. **Measure if possible.** With a URL: run `npx lighthouse <url> --only-categories=performance --output=json --quiet` or use PageSpeed Insights. Record LCP, INP (or TBT), CLS and total JS. Without a URL, audit the code and say that numbers are estimates.
2. **Find the LCP element** (usually the hero image or heading) and trace what delays it: server time, render-blocking CSS/fonts/scripts, image size and priority.
3. **Sweep the code** with [checklist.md](checklist.md): images, fonts, JavaScript weight, third parties, rendering, data fetching, caching.
4. **Rank** by impact on the failing metric, then by effort.
5. **Report** using the contract below.

## Targets (75th percentile, mobile)

| Metric | Good | Usual causes when poor |
|---|---|---|
| LCP | ≤ 2.5 s | Large or lazy-loaded hero image, render-blocking CSS/fonts, slow TTFB, client-side data fetch before render |
| INP | ≤ 200 ms | Long tasks, heavy hydration, expensive re-renders, synchronous work in event handlers |
| CLS | ≤ 0.1 | Images or embeds without size, late-loading fonts, injected banners above content |
| JS (compressed) | < 170 KB on first load | Whole-library imports, no code splitting, duplicated packages |

## Output contract

Start with the metric summary (measured or estimated). Then, highest impact first:

```
### [High | Medium | Low] Title
- Metric: LCP | INP | CLS | TTFB | bundle size
- Where: file:line or resource URL
- Evidence: the code or measurement that shows the problem
- Fix: the exact change (code snippet or config)
- Expected gain: e.g. "LCP −0.8 s", "−120 KB JS"
```

End with **Quick wins** (under an hour each) and **Already good** (what you checked that is fine).

## Common mistakes

- Lazy-loading the LCP image. It must load eagerly with high priority.
- Recommending generic tips ("minify CSS") that the build already does.
- Memoizing everything instead of fixing the one component that re-renders a large list.
- Ignoring third-party scripts, which often cost more than the app itself.
- Claiming exact gains without measurement; label estimates.

---

Made by **Wageesha Tripathi** · [LinkedIn](https://www.linkedin.com/in/wst2002/) · [Email](mailto:tripathiwageesha2002@gmail.com) · [More skills](https://github.com/WST2002/claude-code-skills)
