---
name: nextjs-optimisation-skill
description: Audit or improve any Next.js site for technical SEO, AI-search visibility, crawlability, metadata, structured data, indexing, rendering, Core Web Vitals, bundles, prefetching, images, fonts, animation, accessibility, analytics, build cost, serverless compute, caching, and release discovery. Use for route reviews, new pages, performance regressions, schema/entity work, sitemap or robots changes, IndexNow publishing, client-boundary reductions, deployment-compute reductions, and repository-wide optimisation audits across App Router or Pages Router projects.
---

# Next.js Optimisation

Use evidence, preserve truthful semantics, and make the smallest change that fixes a demonstrated problem. Treat discovery, rendering, performance, accessibility, and measurement as one system rather than independent score-chasing exercises.

## Start here

1. Read repository instructions such as `AGENTS.md`.
2. Determine the installed Next.js version from `package.json`.
3. Before changing framework APIs, detect the installed version and use its bundled documentation when available, such as `node_modules/next/dist/docs/`. Do not assume the latest Next.js behavior applies to the target project.
4. Inspect the route, its shared layout/components/data, metadata, generated output, tests, and the current git diff. Preserve unrelated user changes.
5. Classify the task: discovery, structured data, rendering, performance, media, animation, analytics, indexing, publishing, or a combination.
6. Open [index.md](index.md), then load only the references and checklist needed for the task.

## Operating workflow

### 1. Establish intent and evidence

- Identify the visible purpose, audience, canonical URL, conversion action, and whether the route deserves independent indexing.
- Separate objective defects from strategic choices. A missing canonical or invalid JSON-LD is objective; whether a route should be indexed or an animation retained is strategic.
- For performance work, record a baseline or identify a concrete payload/runtime cause. Do not claim a score without comparable lab or field data.
- Check history when current code reflects a deliberate reversal. Newer verified decisions override older audit documents.

### 2. Choose the least dynamic architecture

- Prefer Server Components and prerendered HTML for meaningful content.
- Add a Client Component only around the interaction that needs browser state, effects, or event handlers.
- Keep semantic content present without JavaScript; animation and enhancement may sit on top.
- Use static generation for stable public content. Use dynamic rendering only when request-time data, authentication, or per-user state requires it.
- Defer heavy, below-fold, or conditional interactions with dynamic import, `React.lazy`, `Suspense`, intent, or viewport proximity when the loading experience remains accessible.

### 3. Implement coherent discovery signals

- Align visible H1/copy, title, description, canonical, robots directive, sitemap inclusion, internal links, and JSON-LD.
- Use stable absolute `@id` values and reference shared entities by `{"@id": ...}`.
- Describe visible, verifiable facts. Never invent reviews, ratings, prices, outcomes, people, dates, or FAQ content for eligibility.
- Put an indexable URL in the sitemap only when its metadata also permits indexing and its content is independently useful.
- Treat AI-search optimisation as accessible, attributable, well-structured web publishing—not a special hidden-text layer.

### 4. Control loading work

- Give LCP media explicit responsive `sizes` and deliberate preload/priority behavior; lazy-load below-fold media.
- Avoid broad barrel imports and global client wrappers. Enforce narrow imports when recurring regressions justify lint rules.
- Prefetch high-intent paths; disable automatic prefetch on large low-intent link collections and enable it on hover, focus, or touch when useful.
- Load animation libraries only on routes and devices that use them. Respect reduced motion and clean up observers, media queries, timelines, and triggers.
- Audit third-party scripts separately from application code. Load once, at the latest strategy compatible with correctness and consent.

### 5. Validate in layers

Run the narrowest useful checks first, then expand in proportion to risk:

1. focused tests for changed behavior;
2. type checking and linting;
3. production build;
4. rendered-output SEO/schema validation;
5. representative browser, accessibility, responsive, and performance checks;
6. live canonical, redirects, robots, sitemap, verification file, analytics, or IndexNow checks after deployment.

If a validator disagrees with intentional architecture, inspect both. Update stale expectations only after confirming the rendered result is correct.

### 6. Minimise build and deployment compute

- Treat build work, request work, transformations, cache churn, and observability as separate budgets. Reducing browser JavaScript does not prove that server-side compute fell.
- Inspect route cardinality and the production build table. Do not prerender an entire database merely because records can have URLs; publish static detail pages for intentionally indexed or high-demand records and keep the remaining records discoverable in a directory, or generate them on demand when that trade-off is supported.
- Keep stable pages, metadata, feeds, and public data endpoints static or cacheable. Prevent request-only APIs, uncached reads, or broad middleware from making unrelated routes dynamic.
- Apply expensive platform services selectively. Optimise high-value responsive/LCP images, but consider direct delivery for already-sized editorial media, tiny files, vectors, and animations when transformation and cache-write cost exceeds transfer savings.
- Keep function bundles narrow, place compute near its stateful data source, reuse concurrency-safe clients where the runtime permits it, and avoid per-request fan-out that could have been batched, queued, cached, or moved to publishing time.
- Every compute reduction needs a failure mode: staleness, larger transfers, cold first requests, cache invalidation complexity, regional consistency, reduced preview fidelity, or operational burden may outweigh the saving.

For a build-cost, serverless, ISR, caching, function, middleware, image-transformation, or deployment-efficiency task, read [references/server-build-deployment.md](references/server-build-deployment.md). Use its decision table instead of applying every tactic globally.

## Repository adaptation

Infer conventions from the repository instead of assuming a company, route tree, schema vocabulary, analytics vendor, animation library, or deployment platform. Locate central metadata/data registries, indexing allowlists, sitemap/robots generators, tests, release scripts, and historical decisions. Preserve deliberate architecture unless current evidence justifies a change.

Convert useful local patterns into general rules: centralize stable IDs, keep commercial claims truthful, avoid thin route generation, curate indexability, preserve semantic HTML beneath enhancement, notify discovery services after deployment, and use substantive freshness dates. Do not copy example identities, URLs, dates, crawler lists, script names, or content policies into another repository.

## Non-negotiable anti-patterns

- Do not add schema solely to pursue a rich result.
- Do not mass-index generated, repetitive, or discovery-only routes.
- Do not make a route dynamic to solve a problem static data can solve.
- Do not put the whole page behind `"use client"` for one interaction.
- Do not preload every image, font, script, or route.
- Do not add smooth-scroll or animation runtimes site-wide by default.
- Do not submit IndexNow before changed canonicals are deployed.
- Do not duplicate GA page views, consent state, third-party libraries, or enhanced-measurement events.
- Do not report Core Web Vitals improvements without measurement.

## Navigation

Use [index.md](index.md) as the reference map. For a new route, follow [checklists/new-page.md](checklists/new-page.md). For an existing route, follow [checklists/audit-page.md](checklists/audit-page.md). Use the performance and release checklists before claiming completion.

## Creator

Created for and maintained by [Brownsmith Dynamics](https://brownsmithdynamics.com).
