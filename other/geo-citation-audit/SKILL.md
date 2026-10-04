---
name: geo-citation-audit
description: Measure pleasur.ai's AI-citation share across ChatGPT / Perplexity / Gemini / Google AI Overviews for the tracked query list, using the Ahrefs MCP Brand Radar (AI share-of-voice / mentions + cited-pages gaps) plus keywords-explorer-overview serp_features for AIO-presence screening, backed by direct engine queries for ground truth. Scores each query into the GEO ledger and surfaces the highest-leverage gaps to fix. The GEO Lead's core measurement loop.
allowed-tools: Read, Write, Edit, Bash, WebFetch, Agent, mcp__ahrefs__*
---

# GEO Citation Audit

The measurement half of the GEO loop. Turns the tracked query list into a scored citation ledger and
a ranked list of "competitor cited, we're not" gaps to prescribe fixes for. **Ahrefs Brand Radar is the
mandated instrument** — it is the AI-citation surface the prior Semrush layer never had (Semrush is
retired). See `GEO-PLAYBOOK.md` (instructions bundle) for the full method; this skill is the
repeatable procedure.

> Read [`../research/references/ahrefs-mcp-cheatsheet.md`](../research/references/ahrefs-mcp-cheatsheet.md) first — the "GEO / AI-citation tracking" block maps this loop to `brand-radar-ai-responses`, `brand-radar-cited-pages`, `brand-radar-sov-overview`, and `site-explorer-ai-responses-count`. Param rules bite: comma-separated **strings** not JSON arrays, and `select` + `country` are required on most endpoints. Call `doc {tool:"brand-radar-sov-overview"}` (etc.) for any Brand Radar tool you haven't used this run to confirm its exact schema; never invent tool names.

## Input
- `life/resources/geo-queries.md` — tracked queries by cluster + competitor list. If absent, build it
  first (category + competitor + "best AI girlfriend / companion / NSFW chat" intent prompts; align
  clusters with EO's keyword clusters).
- `life/resources/geo-ledger.csv` — prior scores (for week-over-week deltas).
- `AHREFS_MCP_KEY` (Brand Radar via MCP), `FIRECRAWL_API_KEY`, `POSTHOG_*` via Doppler.

## Process

1. **Screen AIO presence (cheap, Ahrefs `keywords-explorer-overview`).** For the due queries, call
   `mcp__ahrefs__keywords-explorer-overview` (`keywords` plural, comma-separated and batchable, `country:"US"`, `select:"keyword,serp_features"`)
   and read the `serp_features` list; the `ai_overview` feature flags which queries even trigger a
   Google AI Overview. (⚠️ NOT `serp-overview` — it has no `serp_features` column; verified PLE-3063.)
   Confirm the `ai_overview` key once against a query you know shows one. Drop
   queries that never trigger AIO from the Google-AIO column (don't optimize a surface that isn't there).
   Keep `limit` tight — units cost ≈ 50 base + per-row.

2. **Pull Ahrefs Brand Radar (the high-value AI-citation surface).** Via the MCP, capture for our
   tracked topics ("ai girlfriend", "ai companion", "nsfw ai chat") and the competitor list:
   - `mcp__ahrefs__brand-radar-sov-overview` → AI Share of Voice (us vs tracked competitors), by engine.
   - `mcp__ahrefs__brand-radar-ai-responses` → mentions + impressions + trend across ChatGPT / Perplexity / Gemini / AI Overviews.
   - `mcp__ahrefs__brand-radar-cited-pages` → which pages the engines cite → the **AI citation gap** (pages cite competitors, not us) and **AI mention gap** (competitors mentioned, not us) → the Cited-pages target list.
   - `mcp__ahrefs__site-explorer-ai-responses-count` for `pleasur.ai` (and each competitor) → how often AI engines cite the target overall, as a single trendable number for the ledger header.
   Pass `country:"US"` and an explicit `select`; call `doc` first on each Brand Radar tool. If a Brand
   Radar surface is gated behind an entitlement not on the plan, record the exact entitlement + price
   and escalate in the report (don't fake the numbers); proceed with steps 1, 3, 4.

3. **Direct-query the priority queries (ground truth).** For the top ~10 due queries, ask the engines
   directly — VPS Chrome for ChatGPT / Gemini / Google AI Overview; Perplexity via its API or browser.
   Record verbatim: cited? (y/n), position/prominence, sentiment, and which competitor is cited if we
   aren't. Save evidence snippets. (Direct queries remain the ground-truth check on Brand Radar's
   aggregate numbers — Brand Radar tells you the trend; the direct read confirms the current state.)

4. **Score into the ledger.** For each query × platform write `cited?, position, sentiment,
   last_checked, fix_filed, wow_delta` to `life/resources/geo-ledger.csv`. Compute the GEO score
   (visibility + position + sentiment) and the citation-share total + WoW trend, anchored to the Brand
   Radar SoV + `site-explorer-ai-responses-count` figures.

5. **Surface the gaps.** Emit a ranked list of the highest-leverage gaps (intent × answerable ×
   right-to-win) where competitors are cited and we're absent (from `brand-radar-cited-pages`) — this
   feeds the GEO loop's 2 daily fixes (prescribe → hand to EO / CTO / Affiliates / Community Lead per
   `GEO-PLAYBOOK.md`).

## Output
- Updated `life/resources/geo-ledger.csv` (scored, with WoW deltas).
- A ranked gap list (query, platform, competitor-cited, suggested fix-type + owner) for the fix loop.
- AI-driven traffic note from PostHog (AI/LLM referrers → sessions/signups) for the trend.

## Quality bar
- Every "cited" verdict backed by a captured snippet (no guessing).
- AIO-presence screen (`keywords-explorer-overview` `serp_features.ai_overview`) done before scoring the Google-AIO column.
- Brand Radar numbers are real MCP pulls or an explicit "gated — escalated" note, never fabricated.
- Adult-reality honesty: mark hard-blocked surfaces and stop scoring them.

## When to run
Every GEO measurement cycle (per HEARTBEAT.md), and on demand before a monthly GEO report.
