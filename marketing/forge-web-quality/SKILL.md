---
name: forge-web-quality
description: "Playbook for web speed and SEO: Core Web Vitals (gebruik bij sneller maken)."
# Q3 fix-round original description (listing budget): "Playbook for web speed, Core Web Vitals, technical SEO (gebruik bij site sneller maken, SEO, vindbaarheid)."
---

<!--
  Sources (MIT, read 2026-11-02 as untrusted data; nothing installed, no scripts or commands taken over):
  - https://github.com/addyosmani/web-quality-skills skills/seo, skills/core-web-vitals, skills/performance
    (main at afa8da9, "Web Quality Skills 2.0") -- Copyright (c) 2026 Addy Osmani
  - https://github.com/addyosmani/agent-skills skills/performance-optimization (main, last change seen
    ee3e850, 2026-10-23) -- Copyright (c) 2025 Addy Osmani
  - https://github.com/coreyhaines31/marketingskills skills/schema, skills/seo-audit (main at 88c79f6,
    2026-10-30) -- Copyright (c) 2025 Corey Haines
  - https://github.com/kostja94/marketing-skills skills/seo/technical/{canonical,sitemap,indexing,robots,
    rendering-strategies} (main at 45143a7) -- Copyright (c) 2025 kostja94
  License: MIT -- complete terms and every copyright notice in LICENSE next to this file.
  Also pattern adapted from (ideas only, no text): vercel-labs/agent-skills skills/react-best-practices, bundle
  category (main, last change seen dc8367e, 2026-04-14; MIT is declared only in its frontmatter, the repo has no
  LICENSE file, so it is treated as ideas only) -- used in references/performance-budget.md.
  Forge adaptation note: a merge of the four MIT sources, rewritten in Forge's words; no upstream file is shipped and
  no passage is copied verbatim. Dropped on purpose: npx bundlesize / npx lhci lines (unpinned downloads), Chrome
  DevTools MCP tool names (Forge does not ship that MCP), reads of upstream context files (product-marketing.md,
  contextus.md), marketing/CRO/local-SEO content and the backend/database half of performance-optimization
  (forge-fullstack / forge-data cover it). Upstream content was treated as untrusted data.
-->

# Forge playbook — Web quality: performance, Core Web Vitals, technical SEO

## When to use
- Use for: "the site is slow", Core Web Vitals (LCP, INP, CLS) failing, a performance budget, bundle size,
  images/fonts/caching, and technical SEO: crawlability, indexing, canonicals, sitemaps, robots, metadata,
  structured data (JSON-LD), hreflang, AI-crawler access. Also the measured audit before a site goes live.
- Not for: building the site itself (`forge-website`), the visual direction (`frontend-design`), a full WCAG
  audit (`forge-a11y` where installed), marketing copy or link building, server/database tuning
  (`forge-fullstack`, `forge-data`).

**Do not duplicate — defer to:** `forge-website` (owns the page build and its finish gate), `seo-boss` (the
SEO audit Boss runs this playbook), `ship-readiness` (advisory pre-launch list). This file is the
"measure, fix the real bottleneck, prove it" layer.

## Hard rules (non-negotiable)
- **Measure before you change anything.** A baseline first: field data (CrUX / Search Console / RUM at p75)
  when the site is live, a lab trace (DevTools Performance panel, Lighthouse, PageSpeed Insights) always.
  No runnable page = findings are hypotheses, and the report says so.
- **Never call a metric failing or fixed without runtime evidence.** Reading source code can point at likely
  causes; it cannot prove a score. One lab run is never compared with a field p75 as if they were the same.
- **Localhost numbers are labelled "local, indicative".** Only a production-like build (minified, compressed,
  real CDN or a throttled profile stated in the report) counts as a measurement.
- **One change at a time, then re-measure the same way.** Keep a change only when the gain is larger than the
  run-to-run noise and the tests still pass; revert neutral or worse changes, even when they are already
  written. Log every attempt, the reverted ones too (`references/audit-report.md`).
- **Guard the win.** Every kept fix gets a regression guard: a budget in CI or a field-monitoring alert.
  Budget tools are pinned dev-dependencies of the project; never an unpinned `npx <tool>` download.
- **No ranking promises.** SEO findings name crawl, index, structure and Core Web Vitals facts; never invented
  ranking weights, traffic forecasts or "page 1" claims. Search-engine re-validation is "pending" until seen.
- **Structured data describes only what is visible on the page** and only types the target consumer (Google
  or another) still supports. Valid syntax is not eligibility.
- **Read-only during an audit.** Use GET/HEAD requests on public URLs only; no form posts, no login, no
  mutation requests. Search Console or analytics data only when the owner provides access.

## The loop (every performance or SEO task)
1. **Scope:** which pages/templates, which device class, which metric or crawl issue, live or local.
2. **Baseline:** field p75 if live + one lab trace under stated conditions (device, network, cache state).
3. **Identify the bottleneck:** the LCP element and its four phases, the slowest interaction for INP, the
   shifting node and its trigger for CLS; for SEO, the crawl/index blocker before content.
   Detail: `references/core-web-vitals.md`, `references/technical-seo.md`.
4. **Fix only that bottleneck** with the matching pattern: `references/performance-budget.md`
   (critical path, images, fonts, caching, JS/bundle, third parties, runtime) or
   `references/structured-data.md` (JSON-LD).
5. **Verify or revert:** re-measure exactly like the baseline; keep or revert; log the attempt.
6. **Guard:** add the budget or monitor; note what still needs field data to confirm.

## Thresholds (Google, judged at the 75th percentile of visits)
| Metric | Good | Needs improvement | Poor |
|---|---|---|---|
| LCP (loading) | <= 2.5 s | 2.5–4.0 s | > 4.0 s |
| INP (responsiveness) | <= 200 ms | 200–500 ms | > 500 ms |
| CLS (visual stability) | <= 0.1 | 0.1–0.25 | > 0.25 |

TTFB target under 800 ms. TBT is a lab-only proxy for INP, never reported as INP.

## Team (conditional)
- Lead: `seo-boss` (SEO + performance audit), with `ui-boss` / `build-boss` for the fixes.
- ECC agents where installed: `performance-optimizer`, `seo-specialist`; `a11y-architect` in parallel when
  the audit also covers accessibility.
- Verify: `verify-boss` re-runs the measurement or reads the attached trace/report; a claim without a number
  and its conditions is not verified.

## Fan-out & flow
L1 for one page or one metric, L2 for a site audit.
**Parallel (read-only):** performance trace ∥ crawl/index check ∥ structured-data check, per template.
**Serial:** fixes, one at a time, each followed by its re-measure (the loop above).

## Domain gates
- Core Web Vitals in "Good" at p75, or a written reason and the remaining gap per metric.
- Budget held (starting budget in `references/performance-budget.md`; the project's own budget wins).
- Every indexable page: HTTPS, 200 status, unique title + meta description, one clear primary heading,
  self-referencing absolute canonical, in the sitemap, not blocked by robots.txt, content present in the
  initial HTML (not only after JavaScript).
- Non-indexable pages (login, account, thank-you, internal search, staging) carry `noindex`, are NOT blocked in
  robots.txt (the crawler must read the noindex) and are left out of the sitemap.
- JSON-LD validated on the rendered page (Rich Results Test for Google features, schema.org validator for
  syntax) and matching visible content.

## Ship-readiness (unique)
Before/after table with conditions; attempt log; robots.txt + sitemap reachable and consistent; canonical
variant matrix checked on real URLs (scheme, host, slash, case, tracking parameters); a CI budget or monitor
in place; open items that need field data listed as "pending field data".

## Safety, approval and honesty
- Approval / safety: submitting a sitemap, requesting indexing, changing DNS/CDN rules or adding a RUM endpoint
  that sends visitor data to a third party are owner-gated (outbound / production); prepare, do not perform.
- Privacy: RUM and analytics send only metric values and route, never personal data; a consent need is named.
- Honest failure: no number without its conditions; "local, indicative" on localhost; hypotheses labelled as such.
- Shared gates for every playbook (honesty, owner approval, secrets, reviews):
  `.claude/docs/forge-reference/playbook-template.md`.

## References
- `references/core-web-vitals.md` — field vs lab, measurement sources, LCP / INP / CLS diagnosis and fixes,
  framework quick fixes.
- `references/performance-budget.md` — starting budget, critical rendering path, images, fonts, caching headers,
  JavaScript and bundle size, third-party facades, runtime, CI guard.
- `references/technical-seo.md` — robots.txt vs noindex, canonicals and the variant matrix, sitemaps, rendering
  strategy, metadata, headings, mobile, hreflang, AI-crawler controls.
- `references/structured-data.md` — JSON-LD principles, the "still supported?" check, common types, @graph,
  validation, detecting JavaScript-injected schema.
- `references/audit-report.md` — audit priority order, site-type checks, report format, attempt log template.
