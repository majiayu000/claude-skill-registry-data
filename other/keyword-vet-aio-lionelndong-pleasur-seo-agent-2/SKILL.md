---
name: keyword-vet-aio
description: Layer 3 of the keyword research pipeline. For every BID-passing keyword, detects AI Overview **presence** by default (via the Ahrefs keywords-explorer-overview `serp_features` array — NOT serp-overview, which has no serp_features column) — non-exempt AIO-present rows are flagged RISKY so the writer differentiates. An OPT-IN heavier path (Brand Radar body-fetch + per-keyword AIO completeness scoring) can reject fully "AIO-cannibalized" keywords, but that is behind a flag, not the default.
allowed-tools: Read, Write, Edit, Bash, WebFetch, mcp__ahrefs__*, Task
---

# Keyword Vet — AI Overview Cannibalization Check

> **Data layer: Ahrefs MCP** (`mcp__ahrefs__*`). Read [`../research/references/ahrefs-mcp-cheatsheet.md`](../research/references/ahrefs-mcp-cheatsheet.md) first — string params (not arrays), `select`+`country` required, `doc {tool:"..."}` any unfamiliar tool. The logic below (filters, thresholds, scoring, schema) is binding.

For every keyword that passed BID (Layer 2), check:
1. Does the SERP show an AI Overview?
2. If yes, how completely does it answer the query?
3. Is the keyword cannibalized (AIO is so thorough nobody clicks)?

The keyword-research transcript's most counter-intuitive finding: even keywords that pass classic Business / Intent / Difficulty checks can be **traffic-dead** if Google answers them at the top of the SERP. Definitional queries lose 35-77% of clicks when AIOs appear; comparison and tool queries lose much less. This layer surfaces which is which.

## Input

`/keyword-vet-aio`

Reads:
- `content-pipeline/0-keywords/keyword-ideas.csv` (after Layer 2 — must have `bid_verdict`)
- `.claude/skills/keyword-research-pipeline/references/aio-cannibalization-rubric.md` (the 0-10 scoring rubric)
- `content-pipeline/0-keywords/cache/aio-fetch/` (per-keyword AIO body cache)

## Process

1. **Filter to BID-PASS rows only.** Layer 3 doesn't run on FAIL rows — they're already excluded.

2. **For each candidate, detect AIO presence.** Call `keywords-explorer-overview` (`{keywords:"<kw>", country:"US", select:"keyword,volume,serp_features"}`) for the keyword. Look at the `serp_features` array in the response — AI Overview shows up under the **literal key `ai_overview`** (underscore, not hyphen). Other features in the array (`featured_snippet`, `question` = People Also Ask, etc.) are useful as secondary evidence but only `ai_overview` triggers the cannibalization check.

   > ⚠️ **Do NOT call `serp-overview` for this** — `serp-overview` has **no `serp_features` column** (selecting it hard-errors: `column 'serp_features' not found`). SERP features (incl. `ai_overview`) live ONLY on `keywords-explorer-overview`. Verified 2026-06-29 (PLE-3063); see the cheatsheet section 4 callout. `keywords-explorer-overview` takes `keywords:` (plural) and you can batch several comma-separated keywords per call — cheaper than one `serp-overview` per keyword.

   - If `ai_overview` not in `serp_features`: `has_aio=false`, `aio_verdict=PASS` (no cannibalization risk), continue.
   - If `ai_overview` in `serp_features`: `has_aio=true`, proceed to step 3.

3. **Source-of-truth exemptions.** These keyword classes are AIO-immune by transcript principle and skip the cannibalization check:
   - `serp_intent=tool-led` — already routed to tool-opportunities, but if any tool-led keyword reaches here, mark `aio_verdict=PASS` reason `tool_led_immune`.
   - `serp_intent=commercial-investigation` AND has affiliate/comparison intent — AIOs rarely satisfy "best X for Y" because users want options, not summary.

   **Default stop here.** In the default presence-only mode, any non-exempt row with `has_aio=true` is marked `aio_verdict=RISKY` (reason `aio_present`) and the layer moves on — no body fetch, no scoring. Steps 4-6 below run **only when the opt-in completeness-scoring path is enabled** (`BLOG_AGENT_AIO_DEEP=1`); otherwise skip straight to step 7 (persist) with the presence-derived verdict.

4. **(OPT-IN — `BLOG_AGENT_AIO_DEEP=1` only) For non-exempt AIO-present keywords, fetch the AIO body.** Try in this order (Ahrefs Brand Radar AI-responses → SERP-feature snippet → WebFetch — the migration retired the old Semrush AI Toolkit path):

   1. **`brand-radar-ai-responses`** for the keyword (Ahrefs's Brand Radar AI-citation toolkit — cheatsheet "Bonus capabilities"). It returns the actual AI-engine response body Ahrefs captured during its most recent crawl, the engine (filter to the Google AI Overview engine), the cited sources, and a freshness timestamp. This is the highest-fidelity source — use it first. (`brand-radar-cited-pages` gives the cited URLs if you need them for Layer 4's mentions signal.)
   2. **`WebFetch`** the SERP URL `https://www.google.com/search?q={url-encoded-keyword}` and extract the AIO block (parse for `<div data-ai-overview>` or similar — heuristic; will sometimes miss but Brand Radar is the stronger source). This is the second-line source when Brand Radar doesn't have a recent crawl.

   > Note: there is **no** Ahrefs serp_features *body* source. `keywords-explorer-overview`'s `serp_features` only flags AIO **presence** (the `ai_overview` key) — it does NOT carry the AIO text. For the body you need Brand Radar (best) or WebFetch (fallback). The old "serp-overview snippet" source was a migration artifact and never existed on Ahrefs.

   Cache successful fetches under `content-pipeline/0-keywords/cache/aio-fetch/{keyword-slug}.json` with timestamp and a `_meta.source` field set to one of `brand_radar_ai_responses` or `webfetch`. Refresh weekly. (Pre-migration cache files have Semrush `ai_toolkit_*` source shapes — treat them as stale on first read and re-fetch.)

   Optionally also use `brand-radar-cited-pages` / `brand-radar-sov-overview` for the keyword to check whether the brand or any competitor is currently cited inside the AIO body — informational only; not required for the cannibalization score.

   If all three sources fail: mark `aio_verdict=UNKNOWN` reason `fetch_failed`, treat as `RISKY` for queue purposes, log to calibration file.

5. **(OPT-IN) Score AIO completeness via adversarial sub-agent.** Spawn a Task sub-agent with `model="sonnet"` and this brief:

   > You are a reader who just searched **{keyword}** on Google.
   >
   > The AI Overview at the top of the SERP says:
   >
   > """
   > {aio_body}
   > """
   >
   > Your job: rate from **0 to 10** how completely this AI Overview answers the query.
   >
   > - **10** = the AIO fully answers what I needed; clicking any link would be redundant.
   > - **7-9** = the AIO answers most of what I needed; I might click for one specific thing but not deep reading.
   > - **4-6** = the AIO gives a partial answer; I'd still click 1-2 results to get the full picture.
   > - **1-3** = the AIO is shallow / wrong / generic; I'd ignore it and click the regular results.
   > - **0** = the AIO is useless or doesn't address the query.
   >
   > Apply the rubric in {project-root}/.claude/skills/keyword-research-pipeline/references/aio-cannibalization-rubric.md as your scoring guide.
   >
   > Reply in this exact format (one line each, nothing else):
   > ```
   > SCORE: <0-10>
   > CLICK_INTENT: <yes-deep | yes-shallow | no>
   > REASONING: <one sentence — what the AIO does well or fails at, specifically>
   > ```
   >
   > Be honest. If the AIO is genuinely good, score it high — saying everything is shallow when it isn't burns the brand's writing budget on traffic-dead keywords.

6. **(OPT-IN) Apply the completeness verdict** based on the score + intent (replaces the presence-derived `RISKY` for rows that went through scoring):
   - **Score >= 8 AND `serp_intent=informational`** → `aio_verdict=FAIL_CANNIBALIZED`. The AIO is comprehensive on a query type where users won't click past it.
   - **Score 5-7** → `aio_verdict=RISKY`. The AIO partially answers; the article must offer something the AIO can't (depth, examples, opinion, walkthroughs). Stays in queue with the flag so the writer knows to differentiate.
   - **Score 0-4** → `aio_verdict=PASS`. AIO is weak; classic SERP traffic intact.
   - **Score >= 8 AND `serp_intent=commercial-investigation`** → `aio_verdict=PASS`. Commercial intent is AIO-resistant per transcript principle (users want options, not summary).

7. **Persist columns** to `keyword-ideas.csv`:
   - `has_aio` (true/false — derived from the `ai_overview` literal in `keywords-explorer-overview`'s `serp_features`)
   - `aio_completeness_score` (0-10 or null)
   - `aio_click_intent` (yes-deep / yes-shallow / no / null)
   - `aio_verdict` (PASS / RISKY / FAIL_CANNIBALIZED / UNKNOWN)
   - `aio_reasoning` (one-sentence agent rationale)
   - `aio_body_source` (brand_radar_ai_responses / webfetch — informs Layer 4's confidence in the score; presence is always from `keywords-explorer-overview` serp_features, which is not a body source)

8. **Print summary**:
   ```
   AIO check on N BID-PASS candidates:
     No AIO present (no ai_overview):         X
     AIO present, exempt (tool/CI):           X
     AIO present, non-exempt (RISKY):         X    # presence-only default
     # the buckets below populate ONLY under BLOG_AGENT_AIO_DEEP=1:
     AIO scored 0-4 (PASS):                   X
     AIO scored 5-7 (RISKY):                  X
     AIO scored 8-10 (FAIL_CANNIBALIZED):     X
     Fetch failed (UNKNOWN, treated RISKY):   X
     Body sources: brand_radar=X webfetch=Y
   Top 3 cannibalized rejections (deep mode only):
     - <keyword> — score <n>: <reasoning>
   Top 3 risky survivors:
     - <keyword> — score <n>: <reasoning>
   ```

## Output

Updated `content-pipeline/0-keywords/keyword-ideas.csv` with AIO columns.

Cached AIO bodies under `content-pipeline/0-keywords/cache/aio-fetch/`. Each file carries `_meta.source` so the orchestrator can audit fetch-mix drift.

Calibration log at `content-pipeline/0-keywords/cache/aio-calibration.log`.

## Quality checklist

- [ ] Every BID-PASS row has `aio_verdict` populated
- [ ] AIO presence detection used the `ai_overview` literal in `keywords-explorer-overview`'s `serp_features` (NOT `serp-overview` — it has no serp_features column)
- [ ] Presence-only default: every non-exempt `has_aio=true` row is `RISKY` (reason `aio_present`); no `FAIL_CANNIBALIZED` is emitted unless deep mode ran
- [ ] **Deep mode (`BLOG_AGENT_AIO_DEEP=1`) only:** at least 1 row got each of {PASS, RISKY, FAIL_CANNIBALIZED} (scorer doing real work — if all PASS too lenient, if all FAIL hallucinating); no row scored 8+ was kept as PASS unless exempt; `aio_reasoning` is specific (e.g. "fully covers the definition + 3 examples"), not generic; cache files written with `_meta.source`

## Why this is the most important new layer

The keyword-research transcript: top-ranking pages with AIOs lost 35% of clicks; some pages lost 77% from peak to trough. Existing keyword research methodology (volume + difficulty + brand fit) doesn't see this — a keyword can have great metrics on paper and produce zero traffic in practice. Layer 3 is the only check that sees AIO cannibalization, and it's the difference between an autonomous pipeline that produces dead content and one that produces traffic-relevant content.

## When AIO appears mid-pipeline (vs static at write-time)

AIO presence drifts. A query without an AIO today may have one in 6 months. The orchestrator runs Layer 3 weekly via the keyword-research-pipeline cadence, so the queue gets re-vetted regularly. Articles already published don't get re-vetted (they're in `8-publish/`); the update pipeline runs its own AIO check via `/update-topic-gaps`.

## Calibration

The 0-10 scoring is the most subjective layer in the pipeline. Initial calibration:

1. Run on 20 known queries (see `aio-cannibalization-rubric.md` for canonical examples).
2. Spot-check the verdicts against your own judgment as the editor.
3. If the scorer is over-rating (everything 8+) → strengthen the contrarian language in the brief and re-run.
4. If under-rating (everything 4-) → relax (rare; AIOs are getting better not worse).

After calibration, the discipline check (Layer 4 redteam questioning AIO classifications) is the ongoing safety net.

## Adversarial sub-agent: why Sonnet not Opus

Per project memory ("Claude-in-Chrome work always runs on Sonnet 4.6") and the model-routing principle: scoring an AIO body is high-throughput, low-reasoning judgment. Sonnet is fast and accurate enough; Opus is wasted spend across 50-100 keyword scorings per pipeline run. The brief is structured (rubric + format), which Sonnet handles cleanly.

## Ahrefs API units notes

- `keywords-explorer-overview` is the most-called tool here for presence detection — but you can batch several keywords per call (`keywords:` is plural, comma-separated), so it's cheaper than the old one-`serp-overview`-per-keyword pattern. With ~50-100 candidates per run, batch them in groups to cut unit spend.
- `brand-radar-ai-responses` is the fidelity-leading source for AIO bodies — its call frequency is bounded by the non-exempt-AIO subset (typically ~30-60 keywords per run after exemptions).
- `brand-radar-cited-pages` / `brand-radar-sov-overview` are optional; only call when Layer 4 will use the mentions signal.
- WebFetch fallback bypasses Ahrefs units but is slower and parses inconsistently. Last resort.

If the orchestrator detects units pressure (Ahrefs returns 429), pause Layer 3 mid-run, persist progress to `keyword-ideas.csv`, exit with code 75 (signal: rate-limited, retry after cool-down). The orchestrator handles the retry on next cron cycle.

> **Note on presence-only posture (the default).** Layer 3's default is *presence-only* AIO detection via `keywords-explorer-overview`'s `serp_features`: any non-exempt row with `has_aio=true` is flagged `RISKY` (reason `aio_present`) and the writer differentiates — no body fetch, no scoring. The Brand Radar body-fetch + adversarial-scoring path (steps 4-6) is the **opt-in** full cannibalization check, gated behind `BLOG_AGENT_AIO_DEEP=1`; it is preserved from the pre-migration design and is now genuinely sourceable on Ahrefs (Brand Radar exists where Semrush AI Toolkit / DataForSEO did not). Enable it deliberately when Brand Radar coverage is available and you want FAIL_CANNIBALIZED rejections; otherwise the presence-only default stands rather than blocking.

**Ahrefs MCP only** — no other data providers. Presence from `keywords-explorer-overview` serp_features; AIO body (deep mode) from Brand Radar → WebFetch in that order.
