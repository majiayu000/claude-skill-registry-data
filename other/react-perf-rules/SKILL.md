---
name: react-perf-rules
description: Provides prioritized P0/P1/P2 criteria for auditing React and Next.js branch diffs across waterfalls, bundle bloat, server execution, and client re-renders.
version: 1.0.0
---

# React & Next.js Performance Review Rules

Prioritized review rules to audit branches for performance regressions.

## Severity Classification

### P0 (Critical — Must Fix Before Merge)
- **Sequential Waterfalls**: Unnecessary chained `await` statements in server components or route handlers that could be parallelized with `Promise.all()`.
- **Accidental De-opt of Server Components**: Adding `'use client'` to layout roots or high-level containers instead of leaf nodes.
- **Unbounded Client-Side Lists**: Rendering dynamic lists with 100+ items without virtualization or pagination.
- **Missing Memoization on Expensive Render Trees**: Passing new inline functions/objects as props to expensive or memoized child subtrees.

### P1 (High Impact — Strong Recommendation)
- **Massive Barrel Imports**: Importing icons or utilities from index barrel files that bypass bundler tree-shaking.
- **Synchronous Heavy Operations in Route Handlers**: Missing `after()` for non-critical side effects (audit logging, telemetry) in Next.js 15.
- **Uncached Cacheable Fetches in Next.js 15**: Relying on legacy Next.js 14 caching assumptions without explicit `revalidate` or `cache: 'force-cache'`.
- **Derived State Synced via `useEffect`**: Storing computed values in `useState` and setting them in `useEffect` instead of calculating inline during render.

### P2 (Medium / Polish)
- **Missing `next/image` dimensions / priority**: Hero images missing `priority` causing LCP delay.
- **Unoptimized Third-Party Scripts**: Analytics or chat widgets loaded eagerly rather than `lazyOnload`.
