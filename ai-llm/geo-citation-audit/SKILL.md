---
name: geo-citation-audit
description: Measure pleasur.ai's AI-citation share across ChatGPT / Perplexity / Gemini / Google AI Overviews for the tracked query list, using SemRush (data API for AIO-presence screening + AI Toolkit via browser for share-of-voice / mention + citation gaps) and direct engine queries. Scores each query into the GEO ledger and surfaces the highest-leverage gaps to fix. The GEO Lead's core measurement loop.
allowed-tools: Read, Write, Edit, Bash, WebFetch, Task, mcp__semrush__*
---

# GEO Citation Audit

The measurement half of the GEO loop. Turns the tracked query list into a scored citation ledger and
a ranked list of "competitor cited, we're not" gaps to prescribe fixes for. **SemRush is the
mandated instrument** — see `GEO-PLAYBOOK.md` (instructions bundle) for the full method; this skill
is the repeatable procedure.

## Input
- `life/resources/geo-queries.md` — tracked queries by cluster + competitor list. If absent, build it
  first (category + competitor + "best AI girlfriend / companion / NSFW chat" intent prompts; align
  clusters with EO's keyword clusters).
- `life/resources/geo-ledger.csv` — prior scores (for week-over-week deltas).
- `SEMRUSH_API_KEY`, `SEMRUSH_USERNAME`, `SEMRUSH_PASSWORD`, `FIRECRAWL_API_KEY`, `POSTHOG_*` via Doppler.

## Process

1. **Screen AIO presence (cheap, SemRush data API).** For the due queries, batch
   `phrase_these` / `phrase_this` with `export_columns=Ph,Nq,Fk` and read the SERP-features list;
   the AI-Overview feature code flags which queries even trigger a Google AI Overview. Confirm the
   current AIO code once against a query you know shows one. Drop queries that never trigger AIO from
   the Google-AIO column (don't optimize a surface that isn't there). Cost: ~10 units/line.

2. **Pull SemRush AI Toolkit (browser — the high-value surface).** Drive the always-on VPS Chrome
   (claude-in-chrome), logged into semrush.com with the Doppler creds, to the AI Toolkit. Capture,
   filtered to our topics ("ai girlfriend", "ai companion", "nsfw ai chat"):
   - AI Share of Voice (us vs tracked competitors), by engine.
   - Mentions + impressions + trend.
   - **AI mention gap** (competitors mentioned, not us) and **AI citation gap** (pages cite
     competitors, not us) → the Cited-pages target list.
   If the AI Toolkit is gated behind an add-on not on the plan, record the exact entitlement + price
   and escalate in the report (don't fake the numbers); proceed with steps 1, 3, 4.

3. **Direct-query the priority queries (ground truth).** For the top ~10 due queries, ask the engines
   directly — VPS Chrome for ChatGPT / Gemini / Google AI Overview; Perplexity via its API or browser.
   Record verbatim: cited? (y/n), position/prominence, sentiment, and which competitor is cited if we
   aren't. Save evidence snippets.

4. **Score into the ledger.** For each query × platform write `cited?, position, sentiment,
   last_checked, fix_filed, wow_delta` to `life/resources/geo-ledger.csv`. Compute the GEO score
   (visibility + position + sentiment) and the citation-share total + WoW trend.

5. **Surface the gaps.** Emit a ranked list of the highest-leverage gaps (intent × answerable ×
   right-to-win) where competitors are cited and we're absent — this feeds the GEO loop's 2 daily
   fixes (prescribe → hand to EO / CTO / Affiliates / Community Lead per `GEO-PLAYBOOK.md`).

## Output
- Updated `life/resources/geo-ledger.csv` (scored, with WoW deltas).
- A ranked gap list (query, platform, competitor-cited, suggested fix-type + owner) for the fix loop.
- AI-driven traffic note from PostHog (AI/LLM referrers → sessions/signups) for the trend.

## Quality bar
- Every "cited" verdict backed by a captured snippet (no guessing).
- AIO-presence screen done before scoring the Google-AIO column.
- AI Toolkit numbers are real pulls or an explicit "gated — escalated" note, never fabricated.
- Adult-reality honesty: mark hard-blocked surfaces and stop scoring them.

## When to run
Every GEO measurement cycle (per HEARTBEAT.md), and on demand before a monthly GEO report.
