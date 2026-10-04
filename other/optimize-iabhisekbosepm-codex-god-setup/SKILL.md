---
name: optimize
description: "Profile and optimize performance: bundle size, rendering, algorithms, queries, memory leaks, Web Vitals."
argument-hint: "[area-to-optimize]"
allowed-tools: Read Write Edit Bash Grep Glob
model: gpt-5.3-codex
---

# /optimize — Performance Optimization

Optimize: **$ARGUMENTS**. See `agents/performance-optimizer.md`.

1. **Profile** — Bundle (`webpack-bundle-analyzer`), build time, runtime (O(n^2) patterns, re-renders)
2. **Analyze** — Check against targets: bundle <200KB gzip, LCP <2.5s, CLS <0.1, TBT <200ms
3. **Optimize** — Algorithmic, React, bundle, network, database, memory fixes
4. **Verify** — Re-measure with before/after metrics
