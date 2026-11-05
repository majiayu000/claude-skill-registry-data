---
name: gsc-opportunity-report
description: Analyze Google Search Console performance for SEO growth, local-demand capture, ranking opportunities, CTR gaps, query/page trends, cannibalization, and emerging demand. Use when the user asks for a GSC/Search Console report, uploads a GSC CSV/Sheet/export/screenshot, wants period-over-period SEO analysis, asks what pages or queries to improve, or wants a search-demand audit for Nick's Tire & Auto or another site.
triggers: search console, gsc report, seo, ranking opportunities, ctr gaps, queries, pages, cannibalization, emerging demand, gsc export, last 28 days, local demand
---

# GSC Opportunity Report

Produce an evidence-first Search Console report that converts search data into prioritized actions.

## Workflow

1. Establish the dataset before interpreting it.
   - Identify property, exact date range, timezone if known, search type, filters, dimensions, and whether the data is complete or sampled/limited.
   - Accept connected data, CSV/XLSX/Sheets, JSON, screenshots, PDFs, or pasted tables.
   - If multiple exports exist, reconcile them before drawing conclusions.
2. Normalize metrics without assuming a fixed current GSC schema.
   - Use clicks, impressions, CTR, average position, query, page, country, device, date, and search appearance when present.
   - Preserve exact source values; calculate derived metrics separately.
3. Compare the current period with the immediately preceding equal-length period by default. Add year-over-year only when comparable data exists.
4. Segment before concluding.
   - Brand vs non-brand when identifiable.
   - Service intent vs informational intent.
   - Local/commercial intent vs broad traffic.
   - Page, query, device, geography, and search appearance where useful.
5. Find opportunities, not just winners and losers.
   - High impressions + weak CTR at competitive positions.
   - Queries/pages sitting near page-one or top-three thresholds.
   - Rising demand with insufficient landing-page coverage.
   - Pages losing clicks despite stable demand.
   - Cannibalization or multiple URLs competing for the same intent.
   - Query-to-page mismatches and thin local/service coverage.
   - New queries with business intent.
6. Separate signal from noise.
   - Do not overreact to tiny volumes, average-position movement caused by query-mix changes, or one-day spikes.
   - State materiality thresholds used when possible.
7. Tie findings to business outcomes. For Nick's, prioritize likely impact on calls, directions, tire inquiries/orders, appointments, vehicle arrivals, repeat customers, reviews, and revenue rather than traffic for its own sake.
8. Read `references/report-contract.md` and follow its output structure.

## Analysis rules

- Never infer conversions or revenue from clicks alone.
- Never call an SEO change successful because impressions rose if qualified clicks, local intent, or downstream outcomes did not improve.
- Distinguish observed facts, derived calculations, and hypotheses.
- Flag data gaps that could materially change the conclusion.
- Prefer exact dates and raw deltas plus percentage changes.
- When current Google behavior or documentation materially affects the interpretation, verify it with an authoritative current source before relying on it.

## Useful triggers

Examples: "run my GSC report", "analyze this Search Console export", "what SEO opportunities are hiding here?", "compare the last 28 days", "which queries should Nick's attack next?"
