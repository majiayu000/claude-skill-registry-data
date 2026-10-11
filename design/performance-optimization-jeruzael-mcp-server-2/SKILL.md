---
name: performance-optimization
description: Identify, analyze, and improve slow application behavior without breaking correctness. Use when Codex needs to investigate or optimize slow pages, heavy dashboards, slow APIs, inefficient database queries, slow reports, laggy mobile screens, frozen forms, slow tables, delayed search/filter behavior, repeated API calls, large response payloads, poor caching, stale cache rules, large bundles, heavy dependencies, slow assets/images, timeout logs, hosting cost concerns, slow background jobs, frontend rendering, backend endpoint logic, database indexes, pagination, server-side filtering, virtualization, build performance, and deployment/runtime bottlenecks.
---

# Performance Optimization

Use this skill when the task is to understand and improve slowness, resource waste, or scalability risk.

## Core Rule

Find evidence before optimizing. Preserve correctness, validation, authorization, data integrity, and user behavior while improving speed or resource usage.

## Workflow

1. Understand the performance problem:
   - affected page/screen/endpoint/query/job/build, user role, expected speed, actual speed, environment, data size, affected users, and likely layer
2. Classify the issue:
   - frontend rendering, backend endpoint, database query, network/API payload, mobile interaction, build/dependency, asset, cache, background job, or deployment/runtime bottleneck
3. Inspect existing performance patterns:
   - pagination, lazy loading, query caching, response shaping, indexes, optimized queries, background jobs, image optimization, code splitting, memoization, virtualization, server caching, CDN/static caching, metrics, and logs
4. Establish baseline evidence:
   - timings, query duration, payload size, API call count, DB query count, record count, render count, bundle size, memory, build/test time, logs, profiling, or code evidence
5. Inspect frontend rendering when relevant:
   - large components, re-renders, expensive render calculations, repeated filtering/sorting, global state overuse, heavy props, large lists, tables, images, animation, form input lag, and frequent state updates
6. Inspect API calls:
   - duplicate mount calls, calls in loops, keystroke calls without debounce, excessive refetching, weak cache keys, unused fetched data, large records for small UI needs, no pagination, and client-side filtering
7. Inspect backend endpoint logic:
   - route/controller/service/repository code, loops over large data, serialization, external APIs, file processing, transaction length, permission checks, report calculations, and response shaping
8. Inspect database queries:
   - missing filters, full scans, missing indexes, N+1 queries, joins, sorts, offsets, aggregations, unused columns/relationships, late tenant/shop scoping, and client-side filtering after fetching all rows
9. Inspect payload size and response shape:
   - nested data, unused fields, large arrays, repeated objects, debug fields, embedded base64/images, sensitive fields, and pagination metadata
10. Inspect caching strategy:
   - cacheable data, private data risks, key correctness, invalidation, user/shop/tenant scoping, stale data risk, and sensitive data risk
11. Inspect pagination, filtering, search, bundle size, dependencies, images/assets, mobile performance, background jobs, and long-running tasks where relevant.
12. Recommend fixes by impact and risk:
   - prioritize high-impact, low-risk changes before larger architectural changes
13. Implement focused improvements only when requested or clearly implied:
   - avoid unrelated optimization, new dependencies without approval, unsafe caching, and behavior-changing API contract edits unless required and documented
14. Verify improvements where possible:
   - tests/build, timing comparison, query plan, call count, payload size, bundle size, manual check, logs, or profiling result
15. Identify remaining bottlenecks and follow-up recommendations separately.
16. Summarize issue, evidence, bottlenecks, fixes, behavior preserved, verification, unmeasured areas, remaining bottlenecks, risks, and next steps.

Read `references/performance-checklist.md` for baseline ideas, inspection categories, fix prioritization, verification methods, and the final report format.

## Non-Negotiable Rules

- Do not guess the bottleneck without inspecting evidence.
- Do not optimize unrelated code.
- Do not sacrifice correctness for speed.
- Do not remove validation or permission checks for performance.
- Do not cache private data unsafely.
- Do not introduce stale data without invalidation rules.
- Do not add indexes without considering migration safety.
- Do not fetch all records when pagination or filtering is needed.
- Do not render huge lists without considering virtualization or pagination.
- Do not add new dependencies without clear benefit.
- Do not claim performance improved without measurement or clear before/after reasoning.
- Do not ignore mobile users and slow networks.
- Do not over-optimize code that is not actually slow.
- Keep performance changes focused and reviewable.

## Output Contract

When using this skill, provide:

1. Performance issue and affected area.
2. Evidence or baseline, clearly separating measured facts from assumptions.
3. Bottlenecks found.
4. Recommended fixes prioritized by impact and risk.
5. Improvements implemented, if any.
6. Behavior preserved.
7. Tests/checks run.
8. Performance verification: before, after, and unmeasured areas.
9. Remaining bottlenecks.
10. Risks and follow-up recommendations.
