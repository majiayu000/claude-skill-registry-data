---
name: performance
description: "Performance measure-first: profile CPU/mem/IO/network/DB/bundle/render. Core Web Vitals targets; fix N+1, waterfalls, rerenders."
---

# performance

Measure first, optimize second, prove third. Intuition-only optimization is a defect source.
## Inspection

Profile first: lab (Lighthouse) + field data; identify the bottleneck layer (network, JS, render, images, fonts, backend).

## Decision rules

Fix the measured bottleneck only; budgets per route (JS KB, image weight, LCP/INP/CLS targets); regressions block like test failures.


## Activate when

- Perf requirements exist, regressions suspected, or bundle/render/DB costs questioned.

## Do NOT activate for

- Backend profiling specifics (see backend/*); SEO plumbing (see technical-seo).

## Procedure

1. Baseline: profile the actual bottleneck (CPU, memory, I/O, network, DB, bundle, render) with lab + field data; set Core Web Vitals targets (LCP/INP/CLS).
2. Fix the measured cause: N+1/waterfalls, rerender storms (memoization boundaries), bundle bloat (splitting, treeshaking), image weight (see media-assets), font/render blocking.
3. Re-measure on the same workload; record before/after numbers in the PR.
4. Guard: budgets + regression tests so the win survives; no speculative micro-optimizations.
5. Verify: targets met on representative devices/networks, no functional regression, numbers quoted.

## Failure modes

Optimizing unmeasured code; image weight ignored while JS is micro-tuned; third-party scripts unexamined; lab-green but field-red.

## Escalation

Backend slowness → backend/* + databases/*; asset weight → frontend/media-assets.
