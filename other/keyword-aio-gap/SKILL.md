---
name: keyword-aio-gap
description: Layer 1c of the keyword research pipeline — SKIPPED on the current Semrush MCP (it exposes no AI-visibility / AI-toolkit reports, so there is no multi-engine citation-gap source). Retained as a logged no-op pass-through; never fabricate aio_gap rows. Revisit only if Semrush ships AI-toolkit reports on MCP.
allowed-tools: Read, Write, Bash
---

# Keyword AI-Overview Gap Skill (Semrush AI Toolkit)

> **DATA LAYER RULING (2026-06-12).** Every `mcp__semrush__<kebab-name>` tool named below is FICTIONAL (never existed on the live server), and DataForSEO is retired. Before making any data call, read [`../keyword-research-pipeline/references/semrush-data-layer.md`](./../keyword-research-pipeline/references/semrush-data-layer.md) — it maps this layer's old calls to the real Semrush MCP pattern (`get_report_schema` -> `execute_report`). The logic below (filters, thresholds, output schema) remains binding; only the data calls changed.

Find prompts where competitors appear in AI search (Google AI Overview, ChatGPT, Gemini, Perplexity, Copilot) but the brand doesn't. These are "AI-search citation gaps" — queries where the goal isn't traditional ranking, it's getting cited by the AI when someone asks about the topic.

This is the fifth piece of Ryan Law's keyword-research strategy: instead of asking "what keywords should I rank for?", ask "what queries do I want my brand associated with in AI search?" Then work backwards.

## What's different on Semrush vs the prior Ahrefs Brand Radar version

Ahrefs Brand Radar was **keyword-centric**: for each competitor, fetch the queries where their pages were cited in AI responses, then set-difference against brand-cited queries.

Semrush AI Toolkit is **prompt-centric**: it tracks a configurable set of *prompts* (questions / comparisons / "best X" queries) against a panel of AI engines. For each prompt, it reports which brands / domains / URLs each engine cited and the share-of-voice per domain. The signal is richer (multi-engine, prompt-level, SoV) but the data model differs — this skill is rewritten around the new model.

> **Read [`../keyword-research-pipeline/references/semrush-metric-translation.md`](../keyword-research-pipeline/references/semrush-metric-translation.md)** before applying any threshold. The "Brand Radar mentions (keyword-centric) → AI Toolkit AI Mentions (prompt-centric)" row in the translation table is the call-out for this skill.

## Input

`/keyword-aio-gap`

Reads:
- `brand-config.md` — brand domain + brand name
- `content-pipeline/0-keywords/cache/competitors.json` — produced by `/content-gap-analysis` Layer 1b. Falls back to `mcp__semrush__organic-competitors` (top-3 by organic intersection) when missing.
- `content-pipeline/0-keywords/keyword-ideas.csv` — current candidate pool. Each surviving candidate seeds 1–3 prompt phrasings.

Optional:
- `--competitors competitor1.com,competitor2.com` — override auto-discovered competitors
- `--max-prompts 200` — cap on prompts registered per run (default 200; respects AI Toolkit quota)
- `--engines aio,chatgpt,gemini,perplexity,copilot` — restrict the engine panel (default: all that the user's plan exposes)
- `--regen` — bust the prompt-panel hash cache and re-register from scratch

## Process

### Step 1 — Resolve brand + competitors

1. Read brand domain + name from `brand-config.md`.
2. Load competitors:
   - First: `cache/competitors.json` (Layer 1b output).
   - Else: `--competitors` override.
   - Else: call `mcp__semrush__organic-competitors` with the brand domain; take top 3 by organic-intersection score.
3. Persist the resolved set to `cache/aio-gap-competitors.json` so the rest of the run is deterministic.

### Step 2 — Generate the prompt panel from the candidate pool

Read `content-pipeline/0-keywords/keyword-ideas.csv`. For each candidate keyword (skip `source=question_mining` rows already covered by Layer 1d), generate **1–3 prompt phrasings**:

| Phrasing | Pattern | When to emit |
|---|---|---|
| Informational | `what is {keyword}?` / `how does {keyword} work?` | Always (1 prompt per candidate) |
| Comparison | `{keyword} vs {competitor-product}` / `best {keyword} alternatives` | Emit only if `gap_mode=missing` or `gap_mode=weak` |
| "Best for X" | `best {keyword} for {audience-persona-from-brand-config}` | Emit only if the candidate has `intents` containing `commercial` |

**Cap**: `--max-prompts` (default 200) per run. If the candidate pool would generate more, prioritize by current `priority_score` (or `volume` if Layer 5 hasn't run yet).

Persist the generated panel to `cache/aio-prompt-panel.json` with `{prompts: [{id, text, source_keyword, source_phrasing}], generated_at, hash}`. The `hash` is `sha256(sorted-prompt-texts)` — used for idempotency in Step 3.

### Step 3 — Register the prompt panel (idempotent, hash-keyed)

Call `mcp__semrush__ai-toolkit-prompts` to register the panel. Two paths:

- **First run, or hash changed since last run:** call the management endpoint with the full panel; persist the returned `panel_id` to `cache/aio-panel-registry.json`.
- **Hash unchanged AND `--regen` not passed:** reuse the existing `panel_id`. Skip re-registration. Log "panel reused (hash match)" to the run summary.

Idempotency matters because AI Toolkit quotas are real and prompt registration may itself be metered. Re-registering an unchanged panel wastes quota.

### Step 4 — Pull mentions per engine

Call `mcp__semrush__ai-toolkit-mentions` for the registered `panel_id`, filtered to `--engines` (default: full panel). The response shape we expect (verify against `semrush-mcp-tool-inventory.md`):

```json
{
  "results": [
    {
      "prompt_id": "...",
      "prompt_text": "...",
      "engine": "aio" | "chatgpt" | "gemini" | "perplexity" | "copilot",
      "responded": true,
      "mentions": [
        {"domain": "candy.ai", "url": "https://candy.ai/...", "rank": 1, "share_of_voice": 0.42},
        ...
      ]
    }
  ]
}
```

Cache the response at `cache/aio-toolkit-mentions-{panel_id}.json`. TTL **7 days** (matches the legacy Brand Radar TTL — AI Toolkit data refreshes daily on Semrush's side, but we don't need daily granularity for content planning).

### Step 5 — Compute the gap

For each `prompt_id`, group mentions by domain. A prompt qualifies as a **gap** if:

- At least one competitor domain appears in `mentions` for at least one engine, AND
- The brand domain does NOT appear in `mentions` for ANY engine

For each gap prompt, derive the row payload:

| Field | Computation |
|---|---|
| `keyword` | `prompts[i].source_keyword` (the original candidate the prompt was generated from) |
| `aio_prompt_text` | `prompts[i].text` (the prompt phrasing — useful for the writer, doesn't go in the CSV but lands in the summary) |
| `aio_engines` | comma-list of engines that cited a competitor for this prompt (e.g. `aio,chatgpt,perplexity`) — multi-engine citation = stronger signal |
| `competitor_aio_mention` | comma-list of competitor domains cited |
| `competitor_cited_url` | the most-prominent (highest `rank` / lowest number) competitor URL across the engine panel |
| `aio_sov_competitor_top` | top competitor's share-of-voice for this prompt (max of competitor SoVs across engines) — `priority_score` tie-breaker in Layer 5 |
| `source` | `aio_gap` (or `both` if a prior layer already added the row — see Step 6) |

### Step 6 — Enrich + append to keyword-ideas.csv

For each gap row, call `mcp__semrush__keyword-overview` to add `volume`, `kd_pct`, `traffic_potential`, `cluster_id` (KSB), `intents`. Skip rows with `volume < 20` (signal too thin).

Append to `content-pipeline/0-keywords/keyword-ideas.csv`. Column contract for `aio_gap` source rows:

```
keyword, volume, kd_pct, traffic_potential, cluster_id, intents,
source, competitor_aio_mention, aio_engines, competitor_cited_url,
aio_sov_competitor_top, gap_mode, question_subtype,
priority_score, brand_fit, product_fit, notes, rank
```

The `aio_engines`, `competitor_cited_url`, and `aio_sov_competitor_top` columns are **new** vs the Brand Radar era. The first run after migration will widen the CSV — that's expected.

If a row already exists for the same `keyword` (e.g. content-gap-analysis surfaced it as `gap_mode=missing`), **merge in place**: set `source=both`, append competitors to `competitor_aio_mention`, write `aio_engines` / `aio_sov_competitor_top` / `competitor_cited_url` as new columns. Don't duplicate the row.

If `keyword-ideas.csv` doesn't exist yet, create it with the standard header (above) — Layer 5 prioritization tolerates absent columns by treating them as default.

### Step 7 — Print the run summary

```
Layer 1c — AI Toolkit gap analysis
  Brand domain: pleasur.ai
  Competitors: candy.ai, ourdream.ai, createporn.com
  Prompt panel: 187 prompts (hash 1f3a..., cache HIT — reused panel_id 8721)
  Engines queried: aio, chatgpt, gemini, perplexity, copilot
  Prompts with competitor citations: 84
  Prompts with brand AND competitor citations: 12
  Gap prompts (competitor cited, brand not): 72

Top 5 gap prompts by aio_sov_competitor_top:
  1. "best ai girlfriend app 2026"             SoV 0.61   engines: aio,chatgpt,perplexity   competitor: candy.ai
  2. "candy.ai vs ourdream comparison"          SoV 0.55   engines: chatgpt,gemini           competitor: candy.ai
  3. "ai companion app with voice chat"         SoV 0.48   engines: aio,perplexity           competitor: ourdream.ai
  ...
```

Save the summary to `cache/aio-gap-summary.md` for the orchestrator + auto-blog-loop's redteam read.

## Output

- Rows appended to `content-pipeline/0-keywords/keyword-ideas.csv` with `source=aio_gap` (or `both`)
- `cache/aio-prompt-panel.json` — the generated prompt panel + hash
- `cache/aio-panel-registry.json` — `{hash: panel_id}` mapping for idempotency
- `cache/aio-toolkit-mentions-{panel_id}.json` — raw API response (TTL 7 days)
- `cache/aio-gap-competitors.json` — resolved competitor list for this run
- `cache/aio-gap-summary.md` — human-readable run summary

## Quota handling — 429 → exit 75

AI Toolkit has its own quota. If `mcp__semrush__ai-toolkit-mentions` or `mcp__semrush__ai-toolkit-prompts` returns HTTP 429:

1. Persist whatever progress was made (panel registration succeeded? mentions fetch partial?) to the cache files above.
2. Append a quota event to `cache/aio-toolkit-quota.log`.
3. **Exit code 75** — same convention `auto-blog-loop` and the keyword-research-pipeline orchestrator already understand. The orchestrator retries on the next cron cycle; quota windows reset on Semrush's side.

Don't fall back to Ahrefs Brand Radar — Ahrefs is retired. Don't fall back to WebFetch — manual scraping won't reproduce Semrush's panel methodology.

## Quality checklist

- [ ] At least 1 competitor's mentions were successfully fetched (otherwise AI Toolkit may be unauthenticated — surface clearly)
- [ ] Each gap row has a non-empty `aio_engines` and `aio_sov_competitor_top`
- [ ] No duplicate rows by keyword (existing rows get merged with `source=both`, not duplicated)
- [ ] Cache files are under `content-pipeline/0-keywords/cache/` (gitignored)
- [ ] Summary lists top 5 gap prompts with the citing competitors and engine breakdown
- [ ] Prompt panel hash matches the `cache/aio-panel-registry.json` entry (idempotency working)
- [ ] CSV header includes the three new columns (`aio_engines`, `competitor_cited_url`, `aio_sov_competitor_top`) when this skill writes for the first time

## Why this exists

AI search is increasingly where queries get answered. If competitors are getting cited in Google AI Overview / ChatGPT for "best electric bike under $2000" and the brand isn't, ranking #1 in classic SERP doesn't fix that — the user may never click through. The fix is to **become the source AI cites**. That requires: (a) finding which prompts the AI cites competitors for; (b) writing content that earns those citations.

Layer 5 (`/keyword-prioritization`) gives `aio_gap` keywords a `+1.5` priority boost. The new `aio_sov_competitor_top` column adds a tie-breaker — when two keywords tie on `priority_score`, the one with higher competitor SoV-to-displace ranks higher (more headroom to claim).

## When the brand has zero AI-search presence

That's normal for newer brands or brands that haven't optimized for AI search. The skill still runs — every competitor-cited prompt is a gap. The summary calls this out so the orchestrator can prioritize content that earns the brand's first AI citations.

## When competitors aren't in AI search either

If neither brand nor competitors get AI citations for any of the registered prompts, the gap set is empty. That's still useful information. Write a stub row to `cache/aio-gap-summary.md` documenting which prompts were checked and the absence of citations. Layer 5 will see no `aio_gap` source and skip the boost.

## When the prompt panel hashes mismatch

If `cache/aio-panel-registry.json` has a `panel_id` for a hash you don't recognize, the candidate pool changed (Layer 1a/1b/1d ran since the last AIO sweep). Generate a fresh panel; register it; persist the new `(hash, panel_id)` entry. The old `panel_id` stays in the registry for audit but isn't reused.

## When AI Toolkit returns multi-engine SoV but no `share_of_voice` field

Some Semrush plans expose mentions but not domain SoV. In that case, fall back to **citation count rank** as the SoV proxy:

```
sov_proxy = 1 / rank if rank else 0
aio_sov_competitor_top = max(sov_proxy across engines)
```

Note this in the summary so the editor knows the SoV column is approximate, not raw SoV.

## Caching policy

- **Mentions cache (`aio-toolkit-mentions-{panel_id}.json`):** 7-day TTL. The orchestrator's weekly keyword-research cadence lines up with the cache TTL — re-fetches happen automatically without manual invalidation.
- **Panel registry (`aio-panel-registry.json`):** persistent. Hashes don't expire; `panel_id`s only get retired when Semrush deletes them upstream.
- **Quota log (`aio-toolkit-quota.log`):** persistent. The auto-blog-loop reads it to throttle subsequent runs after a 429.
- **`--regen`** invalidates the panel registry for the current hash and forces re-registration. Use sparingly — wastes quota.
