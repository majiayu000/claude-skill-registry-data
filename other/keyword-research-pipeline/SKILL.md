---
name: keyword-research-pipeline
description: Master orchestrator for the keyword research pipeline. Chains topic-discovery → seed/modifier ideation → competitor + AI-search gap analysis → question mining → BID method → AIO cannibalization check → adversarial redteam → final ranked queue. Same anti-context-bloat pattern as /blog-pipeline (every layer is an Agent dispatch, never a Skill fork).
allowed-tools: Read, Write, Bash, Agent, Glob
---

# Keyword Research Pipeline (Master Orchestrator)

## Provider ruling (2026-06-12 — supersedes the 2026-06-10 DataForSEO note)

**Semrush MCP is the data layer.** The paid plan has full MCP data access (verified live).
DataForSEO is retired; `scripts/dataforseo_keyword_pipeline.py` is archived and must not run.

Every layer's real data calls are pinned in
[`references/semrush-data-layer.md`](./references/semrush-data-layer.md) — read it before
dispatching any layer. The server has 13 tools and exactly one call pattern
(`get_report_schema` → `execute_report`); any `mcp__semrush__<kebab-name>` mention in the
layer briefs below is a historical fiction that the data-layer file overrides. Metric
thresholds still go through `references/semrush-metric-translation.md`.

Layer 1c (`keyword-aio-gap`) remains **SKIPPED** — this MCP server exposes no AI-visibility
toolkit. Do not fake `aio_gap` rows or `aio_sov_competitor_top`. Layer 3's AIO check is
presence-only via the `Fk` SERP-features column (see the data-layer file). Keep the
deterministic quality, judgment rewrite, and voice-drift rollback gates.

Take a brand and produce a *vetted* keyword queue (`keyword-queue.csv`) ready for the autonomous blog loop. Layered chain (0 → 1a → 1b → 1c → 1d → 2 → 3 → 4 → 5), each rejecting candidates with reasons logged, each dispatched as a fresh Agent.

This is the upstream of `auto-blog-loop`. The blog loop reads the queue this orchestrator emits — never the raw `keyword-ideas.csv`.

> **Threshold reminder.** Every layer in this chain is recalibrated against `.claude/skills/keyword-research-pipeline/references/dataforseo-metric-translation.md`. If a brief tells a layer to apply a numeric threshold, the underlying skill's gate should already match the metric-translation doc — do not let an Agent invent its own threshold from training data. **`mcp__semrush__*` and `mcp__ahrefs__*` are retired for keyword research**; if any sub-agent reaches for either provider, that's a migration leftover bug, not a fallback.

## Invocation

```
/keyword-research-pipeline [--regen] [--max-redteam 30]
```

`--regen` forces fresh runs of idempotent layers (topic-discovery re-runs even if brand-config hash unchanged, seed-modifier-prompt re-runs, redteam re-evaluates already-judged rows, BID/AIO refetch cached SERP data).

`--max-redteam` overrides the Layer 4 batch size (default 30).

## Why agent dispatch, not skill fork

Same constraint as `/blog-pipeline` (line 22-24 of `blog-pipeline/SKILL.md`): the Skill tool forks with the parent's context. After any compaction or accumulated history, that fork hits `Prompt is too long`. The Agent tool starts each layer with a clean window. This is non-negotiable — every layer MUST be an Agent dispatch.

## Process

1. **Resolve project root** (`C:\Users\ndong\Downloads\blog-agent-2` or wherever the host runs). Set `{ROOT}`.

2. **Layer 0 — `/topic-discovery`** (Agent dispatch). Build a topic-graph + market-trends snapshot for the brand's category before any seed work happens. Self-contained brief:

   ```
   You are running Layer 0 of the keyword research pipeline at {ROOT}.

   Your job: produce content-pipeline/0-keywords/topic-graph.json plus content-pipeline/0-keywords/trends.md per .claude/skills/topic-discovery/SKILL.md. Read the SKILL.md first.

   Read brand-config.md. Pull mcp__semrush__topic-research for the brand's category-level seeds and mcp__semrush__trends-overview for the brand domain (or category URL). Synthesize the top 5 KSB clusters per category and the trending vs. declining queries. Save the JSON + markdown atomically.

   Idempotent: if topic-graph.json exists and the brand-config hash is unchanged AND --regen was not passed, exit without re-generating. Never block the pipeline — if Topic Research / .Trends both error, log to cache/topic-discovery-failed.log and exit cleanly with topic-graph.json containing only the brand-config seeds.

   Return: top 5 cluster names, count of trending-up / trending-down queries, idempotency status (regenerated vs. skipped). Under 250 words.
   ```

   On failure: log and continue. Layer 0 is enrichment, not a gate — Layer 1a will still run with brand-config seeds alone if topic-graph.json is empty.

3. **Layer 1a — `/seed-modifier-prompt`** (Agent dispatch). Self-contained brief:

   ```
   You are running Layer 1a of the keyword research pipeline at {ROOT}.

   Your job: produce content-pipeline/0-keywords/seeds.json per .claude/skills/seed-modifier-prompt/SKILL.md. Read the SKILL.md first.

   Read brand-config.md AND content-pipeline/0-keywords/topic-graph.json (from Layer 0). Pre-feed the top 5 KSB clusters from topic-graph.json into the seed-generation prompt so seeds anchor in real Semrush clusters, not just brand-config alone. Generate 10 seeds + 10+ modifiers (with at least 3 AI-resistant: calculator/checker/generator/tool/template/examples). No word overlap between seeds and modifiers.

   Idempotent: if seeds.json exists and brand-config hash unchanged, exit without re-generating. Force re-gen only if --regen passed.

   Return: seeds count, modifiers count, tool-modifier count, first 3 seeds, whether re-generated or skipped. Under 200 words.
   ```

   On failure: stop the pipeline. Layer 1a is the cheapest layer; if it fails, something is structurally wrong.

4. **Layer 1b — `/content-gap-analysis`** (Agent dispatch). Brief:

   ```
   You are running Layer 1b at {ROOT}.

   Your job: produce content-pipeline/0-keywords/keyword-ideas.csv per .claude/skills/content-gap-analysis/SKILL.md. Read the SKILL.md first.

   Auto-discover competitors via mcp__semrush__organic-competitors if brand-config doesn't list any; cache to cache/competitors.json so Layer 1c reuses the same set. Read seeds.json from Layer 1a — for each seed, expand via mcp__semrush__keyword-magic-broad (and -phrase / -related where breadth is thin) with modifiers as `include` filter. Pull intents array via mcp__semrush__keyword-overview for each row.

   Run multi-mode Keyword Gap via mcp__semrush__keyword-gap — all five modes (missing / weak / unique / common / strong). Tag every row with `gap_mode`. Route `strong`-mode rows to cache/strong-positions.csv (NOT the writing pool). Merge competitor-gap + seed-modifier sources, dedupe on keyword. Add `source` and `gap_mode` columns.

   Apply Semrush KD% threshold ≤ 70 (default) — DO NOT transplant Ahrefs KD ≤ 60. The metric-translation doc has the recalibration math.

   Return: total candidates, breakdown by source (competitor_gap / seed_modifier / both), breakdown by gap_mode (missing / weak / unique / common), strong-positions count, top 5 candidates by traffic_potential. Under 300 words.
   ```

   On failure: stop. Layer 1b failures usually mean a Semrush auth issue (401/OAuth) or quota exhaustion (429).

5. **Layer 1c — `/keyword-aio-gap`** (Agent dispatch). Brief:

   ```
   You are running Layer 1c at {ROOT}.

   Your job: append AI-search gap candidates to content-pipeline/0-keywords/keyword-ideas.csv per .claude/skills/keyword-aio-gap/SKILL.md. Read the SKILL.md first.

   Use the Semrush AI Toolkit's prompt-centric model (NOT the legacy Ahrefs Brand Radar keyword-centric model). For each brand + competitor, register the relevant prompts via mcp__semrush__ai-toolkit-prompts and call mcp__semrush__ai-toolkit-mentions across the multi-engine panel (AIO, ChatGPT, Gemini, Perplexity, Copilot). Compute the gap (competitor-cited prompts where brand isn't). Enrich with mcp__semrush__keyword-overview metrics. Append rows with source=aio_gap (or merge to existing rows as source=both). Add aio_engines and aio_sov_competitor_top columns for Layer 5 prioritization.

   If AI Toolkit returns 429, exit code 75 — orchestrator retries on next cron cycle. Don't crash.

   Return: brand mentions, total competitor mentions across the engine panel, gap-prompt count, top 5 gap keywords with their dominant engine. Under 300 words.
   ```

   On Layer 1c rate-limit: don't fail the pipeline — Layer 1b already produced a candidate pool, downstream layers can vet it. Note the 1c skip in the run summary.

6. **Layer 1d — `/keyword-question-mining`** (Agent dispatch). Brief:

   ```
   You are running Layer 1d at {ROOT}.

   Your job: append question-shaped keyword candidates to content-pipeline/0-keywords/keyword-ideas.csv per .claude/skills/keyword-question-mining/SKILL.md. Read the SKILL.md first.

   For every primary seed in seeds.json, call mcp__semrush__keyword-magic-questions to pull the question-form variants Semrush exposes. Then call mcp__semrush__serp-results per top seed and parse the People Also Ask block for additional questions Keyword Magic missed. Cap the merged pool at 100 rows per pipeline run; dedupe against existing keyword-ideas.csv. Tag every appended row with source=question_mining and a question_subtype field (`paa` / `km_question` / `both`). Pull intents via mcp__semrush__keyword-overview for each new row.

   On 429: persist progress, exit 75. The orchestrator handles retry.

   Return: km_questions count, paa-only count, deduped-against-existing count, top 5 questions by volume, subtype breakdown. Under 250 words.
   ```

   On failure (other than 429): continue. Layer 1d is enrichment; missing question-mining rows don't break the queue.

7. **Layer 2 — `/keyword-vet-bid`** (Agent dispatch). Brief:

   ```
   You are running Layer 2 at {ROOT}.

   Your job: enrich content-pipeline/0-keywords/keyword-ideas.csv with BID verdicts per .claude/skills/keyword-vet-bid/SKILL.md. Read the SKILL.md first.

   Resolve brand AS via mcp__semrush__domain-overview, cache to cache/brand-as.json (7-day TTL). Delete any leftover cache/brand-dr.json — its DR-shaped payload is incompatible.

   For each row: compute brand_fit + product_fit; classify intent — PRIMARY signal is the Semrush `intents` array from mcp__semrush__keyword-overview (informational/commercial = PASS; transactional/navigational = FAIL); fall back to URL-pattern heuristic on mcp__semrush__serp-results only when `intents` is empty/mixed. Pull per-URL Authority Score for the SERP top-10 via mcp__semrush__serp-overview / mcp__semrush__domain-overview. Apply the BID gate (recalibrated for Semrush — as_top10_median ≤ brand_AS + 12; weak_link_count of pages with AS < brand_AS + 4; KD% ≤ 70 baseline).

   Persist columns: brand_fit, product_fit, serp_intent, as_top10_median, weak_link_count, bid_verdict, bid_reason.

   Calibration check: if all rows pass OR all fail, log to cache/bid-calibration.log and adjust thresholds per the SKILL's "Calibration" section.

   Return: total vetted, B/I/D pass rates, share of intent decisions made via `intents` array vs URL fallback, overall PASS count, top 5 PASS by traffic_potential, top 5 FAIL with reasons. Under 350 words.
   ```

   On failure: stop. BID failures usually mean Semrush quota or auth issues — not recoverable mid-run.

8. **Layer 3 — `/keyword-vet-aio`** (Agent dispatch). Brief:

   ```
   You are running Layer 3 at {ROOT}.

   Your job: enrich BID-PASS rows in keyword-ideas.csv with AIO cannibalization verdicts per .claude/skills/keyword-vet-aio/SKILL.md. Read the SKILL.md and the rubric at .claude/skills/keyword-research-pipeline/references/aio-cannibalization-rubric.md first.

   For each BID-PASS row: detect AIO presence via mcp__semrush__serp-overview — Semrush's literal SERP-feature key is `ai_overview` (underscore — NOT the legacy Ahrefs `ai-overview`). Apply exemptions (tool-led, commercial-investigation, aio_gap source). For non-exempt AIO-present rows fetch the AIO body in this order: mcp__semrush__ai-toolkit-response → mcp__semrush__serp-overview's serp-features summary → WebFetch on https://www.google.com/search?q=…  Spawn the adversarial Sonnet sub-agent with the 0-10 completeness brief; persist has_aio, aio_completeness_score, aio_click_intent, aio_verdict, aio_reasoning, aio_body_source.

   Cache AIO bodies under cache/aio-fetch/ with _meta.source. Refresh weekly. Pre-migration cache files (brand_radar_*) are stale — re-fetch.

   Calibration check: if every score is 8+ OR every score is 4-, the scorer is mis-calibrated — log and re-run with strengthened brief per the SKILL's "Calibration" section.

   Return: total checked, breakdown (no AIO / exempt / PASS / RISKY / FAIL_CANNIBALIZED / UNKNOWN), body-source mix (ai_toolkit / serp_features / webfetch), top 3 cannibalized rejections, top 3 risky survivors. Under 400 words.
   ```

   On rate-limit (exit 75): persist progress, surface to orchestrator. Layer 3 is the most quota-heavy layer (one serp-overview + one ai-toolkit-response per non-exempt BID-PASS row).

9. **Layer 4 — `/keyword-redteam`** (Agent dispatch — judgment-heavy, stays on parent model). Brief:

   ```
   You are running Layer 4 at {ROOT}.

   Your job: redteam top-{max_redteam} survivors per .claude/skills/keyword-redteam/SKILL.md. Read the SKILL.md first.

   Filter to bid_verdict=PASS AND aio_verdict ∈ {PASS, RISKY, UNKNOWN} AND no existing redteam_verdict (idempotent). Take top 30 by current priority_score. Spawn the skeptical-SEO sub-agent with the (a)-(d) challenge brief. The agent reasons over Semrush metrics (intents array, AS gap, KD%, KSB cluster id, AI Toolkit SoV) — not Ahrefs DR/KD heuristics.

   Apply discipline check: if KEEP rate > 80% with weak per-candidate critique (avg < 60 words), re-run with the contrarian addendum from the SKILL.

   Persist redteam_verdict, redteam_priority_delta, redteam_critique_summary to keyword-ideas.csv. Save full critique to redteam-notes.md.

   Return: KEEP/DROP/REVISE counts, sum of priority deltas, top 3 DROPs with one-line reasons, top 3 REVISE-down with reasons. Under 400 words.
   ```

   On failure: stop. Don't ship a queue without the redteam check.

10. **Layer 5 — `/keyword-prioritization`** (Agent dispatch). Brief:

    ```
    You are running Layer 5 at {ROOT}.

    Your job: emit content-pipeline/0-keywords/keyword-queue.csv per the updated .claude/skills/keyword-prioritization/SKILL.md. Read the SKILL.md first.

    Filter pool: only rows where bid_verdict=PASS AND aio_verdict ∈ {PASS, RISKY} AND redteam_verdict ∈ {KEEP, REVISE_PRIORITY}.

    Apply the existing 0.4/0.3/0.3 scoring weights. Apply boosts:
      +1.5 if source=aio_gap
      +0.5 if gap_mode=weak
      +0.7 if gap_mode=unique
      -0.3 if gap_mode=common
      +0.5 if cluster_authority_gap=true (KSB cluster the brand has zero authority in but is low-difficulty)
      +1.0 if serp_intent=tool-led (but ROUTE those to tool-opportunities.csv, not the writing queue)
    Tie-breaker on equal priority_score: row with higher aio_sov_competitor_top wins.

    Apply redteam_priority_delta (capped ±2.0).

    Re-rank, write top-50 to keyword-queue.csv. Tool-opportunity rows go to tool-opportunities.csv (not the writing queue). gap_mode=strong rows are already in cache/strong-positions.csv and are ignored here.

    Return: queue size, top 10 with rank/keyword/priority_score/source/intent/gap_mode/verdicts, tool-opportunities count. Under 350 words.
    ```

11. **Verify each layer's output file exists** before advancing. Layer 0: topic-graph.json + trends.md (or topic-discovery-failed.log). Layer 1a: seeds.json. Layer 1b/1c/1d: keyword-ideas.csv with relevant `source` rows; cache/strong-positions.csv when applicable. Layer 2/3: required columns present. Layer 4: redteam-notes.md exists, keyword-ideas.csv has redteam columns. Layer 5: keyword-queue.csv exists.

12. **Reporting.** When complete, output:

    ```
    ✓ Keyword research pipeline complete

    Layers:
      ✓ 0 topic-discovery     → topic-graph.json (12 clusters, 8 trending-up) / trends.md
      ✓ 1a seed-modifier      → seeds.json (10 seeds, 12 modifiers, 4 tool-modifiers)
      ✓ 1b content-gap        → keyword-ideas.csv (124 candidates: 78 missing, 22 weak, 14 unique, 10 common; 6 strong → cache)
      ✓ 1c keyword-aio-gap    → +37 rows from aio_gap (engines: AIO=18 ChatGPT=11 Perplexity=8) (or SKIPPED: rate-limit)
      ✓ 1d question-mining    → +42 rows (28 km_questions, 19 paa, dedup-overlap=5)
      ✓ 2 keyword-vet-bid     → 203 vetted, 91 PASS / 112 FAIL  (intents-array signal: 78%, URL-fallback: 22%)
      ✓ 3 keyword-vet-aio     → 91 checked, 71 PASS / 14 RISKY / 4 FAIL_CANNIBALIZED  (body source: ai_toolkit=58 serp=7 webfetch=2)
      ✓ 4 keyword-redteam     → 30 redteamed, 22 KEEP / 5 DROP / 3 REVISE
      ✓ 5 prioritization      → keyword-queue.csv (top 50 ranked, 8 aio_gap-boosted, 4 cluster-authority-boosted)
                               → tool-opportunities.csv (12 entries)

    Queue ready for /auto-blog-loop.
    ```

## Failure handling

Per the plan, **bad keyword research is worse than empty queue**. Layer failures stop the chain rather than auto-retrying. Specifically:

- Layer 0 fails → continue. Topic-discovery is enrichment, not a gate.
- Layer 1a fails → stop. Brand-config hash issue or agent malfunction.
- Layer 1b fails → stop. Likely Semrush auth issue (401) or unauthorized OAuth.
- Layer 1c fails (rate-limit) → continue without 1c rows; log skip.
- Layer 1c fails (other) → continue with a warning; 1b alone is a viable candidate pool.
- Layer 1d fails (rate-limit, exit 75) → persist progress; orchestrator retries on next cron.
- Layer 1d fails (other) → continue. Question mining is enrichment.
- Layer 2 fails → stop. The mechanical filter is required.
- Layer 3 rate-limit (exit 75) → persist progress, exit cleanly with code 75. The auto-blog-loop reads this and retries on the next cron cycle.
- Layer 3 fails (other) → stop. AIO check is required.
- Layer 4 fails → stop. Redteam is required.
- Layer 5 fails → stop. Queue emission is the whole point.

The orchestrator never auto-retries — bad keyword research compounds. It logs the failure to `content-pipeline/0-keywords/cache/pipeline-failures.log` and exits.

## When `/auto-blog-loop` invokes this orchestrator

The blog loop calls this when `keyword-queue.csv` is empty (selector exit 2). The keyword-research-pipeline runs to completion (or fails cleanly), then control returns to the blog loop. If it fails:
- The previous `keyword-queue.csv` (if any) stays in place — blog loop falls back to the stale queue.
- If no previous queue, blog loop exits cleanly with a "no work" log entry.

## Calibration cadence

The mechanical layers (BID, AIO) need calibration on first run after Semrush migration AND after major brand-config changes. Calibration logs are in `cache/`:
- `cache/bid-calibration.log` — threshold drift, pass-rate trends
- `cache/aio-calibration.log` — score distribution, rubber-stamp detection

The runbook (`.claude/skills/auto-blog-loop/references/runbook.md`) has a section on reading these logs and tuning thresholds. **Always recalibrate against `references/semrush-metric-translation.md` — Ahrefs thresholds will silently mis-fire on Semrush data.**

## Cost per run

Approximate, for a 200-candidate pool, on Semrush quota:

- Layer 0: ~3-5 Semrush MCP calls (Topic Research + .Trends overview); idempotent — most runs skip
- Layer 1a: ~1K LLM tokens (one Agent call)
- Layer 1b: ~10-15 Semrush MCP calls (organic-competitors + 5 keyword-gap modes + ~6 keyword-magic expansions per seed)
- Layer 1c: ~10-30 AI Toolkit calls (mentions across the engine panel; weighted heavier than the legacy Brand Radar count because of multi-engine fan-out)
- Layer 1d: ~10-20 keyword-magic-questions + serp-results PAA-extraction calls
- Layer 2: ~200 keyword-overview + 200 serp-overview + ~200-2000 domain-overview calls (batched for the per-domain AS lookups)
- Layer 3: ~100 serp-overview + ~50-70 ai-toolkit-response + ~50 Sonnet sub-agent invocations
- Layer 4: ~1 Opus call (30K-50K tokens)
- Layer 5: ~1 Agent call

Total: ~$0.50-1.50 in Semrush MCP quota + ~$0.50 in LLM tokens per run. Weekly cadence keeps annual cost < $80. The blog loop's article cost is much higher; keyword research is cheap insurance. Layer 0 + Layer 1d add ~$0.05-0.10 per run on top of the legacy chain — small price for the upstream uplift.
