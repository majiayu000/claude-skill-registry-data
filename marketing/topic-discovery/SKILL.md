---
name: topic-discovery
description: Layer 0 of the keyword research pipeline. Builds a topic-graph snapshot for the brand's category before any seed work, approximated from Semrush phrase_related + phrase_questions on the category seeds plus the brand's own ranking footprint (domain_organic_unique). Idempotent on brand-config hash; never blocks the pipeline; cheap.
allowed-tools: Read, Write, Bash, mcp__semrush__*
---

# Topic Discovery Skill (Layer 0)

> **DATA LAYER RULING (2026-06-12).** Every `mcp__semrush__<kebab-name>` tool named below is FICTIONAL (never existed on the live server), and DataForSEO is retired. Before making any data call, read [`../keyword-research-pipeline/references/semrush-data-layer.md`](./../keyword-research-pipeline/references/semrush-data-layer.md) — it maps this layer's old calls to the real Semrush MCP pattern (`get_report_schema` -> `execute_report`). The logic below (filters, thresholds, output schema) remains binding; only the data calls changed.

Take `brand-config.md` and produce two artefacts that downstream layers consume as enrichment:

1. **`content-pipeline/0-keywords/topic-graph.json`** — the Semrush Topic Research idea-cluster tree rooted at the brand's category. Layer 1a (`/seed-modifier-prompt`) reads the top 5 cluster names so the seed agent grounds its output in Semrush's actual topic graph rather than brand-config alone. Layer 5 (`/keyword-prioritization`) reads cluster-level metrics to compute the `cluster_authority_gap` boost.
2. **`content-pipeline/0-keywords/trends.md`** — a short markdown summary of category-level trending queries, momentum direction, and competitor traffic shifts pulled from Semrush .Trends. Layer 4 (`/keyword-redteam`) reads this to ground its "is this keyword trending up or down today?" critique.

This layer is **enrichment, not a gate.** If Semrush returns nothing useful, downstream layers fall through to brand-config-only behavior. Layer 0 must never block the pipeline.

## Input

`/topic-discovery [--regen]`

Reads:
- `brand-config.md` — brand category positioning, brand domain
- `content-pipeline/0-keywords/topic-graph.json` — previous output (for change detection)

`--regen` forces a fresh run even if the brand-config hash hasn't changed.

## Process

1. **Compute brand-config hash.** SHA-256 of `brand-config.md` content. Compare against `topic-graph.json`'s `brand_snapshot` field if it exists. If unchanged AND `--regen` not passed, exit cleanly with a one-line message saying "topic graph is current, skipping" — Layer 0 stays idempotent (mirrors the pattern in `seed-modifier-prompt/SKILL.md` step 1).

2. **Read brand-config.** Extract:
   - **Brand category root** — the noun-phrase that defines the brand's category for SEO purposes. Derived from `brand-config.md`'s "Category positioning" line. If the line is verbose, condense to 1–3 words (e.g. for Pleasur.AI: "ai adult companions" → root seed `ai companion`). When in doubt, prefer the broader of two candidates — Topic Research returns richer trees from broader roots.
   - **Brand domain** — used as the .Trends root URL. Strip protocol and trailing slash.

3. **Call `mcp__semrush__topic-research`** with the brand category as the root keyword. Request the full idea-cluster tree: each cluster includes a name, headlines, questions, related searches, aggregated volume, and aggregated difficulty (KD%). Cache the raw response under `content-pipeline/0-keywords/cache/topic-research-raw.json` so re-runs without `--regen` don't refetch when only writing the structured tree.

4. **Call `mcp__semrush__trends-overview`** with the brand domain as the root URL. Pull:
   - Trending queries within the category (volume momentum up vs. down)
   - Competitor traffic shifts (domains gaining or losing share)
   - Audience overlap (which competitor audiences also visit which sites)
   Cache the raw response under `content-pipeline/0-keywords/cache/trends-raw.json`.

5. **Assemble `topic-graph.json`** as a structured tree:
   ```json
   {
     "root_seed": "ai companion",
     "brand_domain": "pleasur.ai",
     "clusters": [
       {
         "id": "ksb-cluster-id-from-semrush",
         "name": "ai girlfriend",
         "volume": 246000,
         "kd_percent": 64,
         "headlines": ["...", "..."],
         "questions": ["what is an ai girlfriend?", "..."],
         "related_searches": ["...", "..."]
       }
     ],
     "generated_at": "ISO8601 UTC",
     "brand_snapshot": "sha256-hex-of-brand-config-md",
     "_meta": {
       "source": "Semrush Topic Research + .Trends",
       "tool_inventory_ref": ".claude/skills/keyword-research-pipeline/references/semrush-mcp-tool-inventory.md"
     }
   }
   ```
   Sort clusters by `volume` descending. Cap headlines / questions / related_searches at 10 entries each per cluster — Layer 1a only consumes the top 5 clusters anyway, but downstream tooling stays bounded.

6. **Assemble `trends.md`** as readable markdown for the redteam agent:
   ```markdown
   # Category trends — {brand_domain} ({YYYY-MM-DD})

   ## Trending up (volume momentum +)
   - keyword (vol_now → vol_prev, change %)

   ## Trending down (volume momentum −)
   - keyword (vol_now → vol_prev, change %)

   ## Competitor traffic shifts
   - competitor.com — gaining/losing X% organic share over the last 90 days

   ## Audience overlap
   - competitor.com ↔ othercompetitor.com — Y% audience overlap

   _Source: Semrush .Trends, generated {ISO timestamp}_
   ```
   Keep it tight — under 60 lines. The redteam agent reads this as ambient context, not a primary input.

7. **Write both files** atomically (write to `.tmp` then move). Print a one-line summary: cluster count, top 3 cluster names with volumes, trending-up count, trending-down count, top 3 competitors by traffic shift.

## Output

- `content-pipeline/0-keywords/topic-graph.json` — structured idea-cluster tree
- `content-pipeline/0-keywords/trends.md` — markdown trends summary
- `content-pipeline/0-keywords/cache/topic-research-raw.json` — raw MCP response (gitignored)
- `content-pipeline/0-keywords/cache/trends-raw.json` — raw MCP response (gitignored)

## Idempotency

Same contract as `seed-modifier-prompt`: re-runs without `--regen` exit cleanly when the brand-config SHA-256 hasn't changed. Two MCP calls per actual run; zero on the no-op path. Safe for the orchestrator to call on every keyword-research-pipeline invocation without worrying about cost.

## Failure handling

**Layer 0 never blocks the pipeline.** It's enrichment, not a gate. Specific failure modes:

- **`mcp__semrush__topic-research` returns empty** (root seed too narrow / not indexed): write a stub `topic-graph.json` with `clusters: []`, `_meta.degraded: true`, and the root_seed used. Append a one-line entry to `content-pipeline/0-keywords/cache/topic-discovery-failed.log` with the timestamp and reason. Exit code 0. Layer 1a reads the empty `clusters` array and falls through to brand-config-only seed generation (current behavior preserved).
- **`mcp__semrush__topic-research` errors** (auth, network, server): write the same stub graph with `_meta.degraded: true` and `_meta.error: "<reason>"`. Log to `cache/topic-discovery-failed.log`. Exit 0.
- **`mcp__semrush__trends-overview` returns empty / errors**: write a `trends.md` containing only the heading and a single line `_Source: Semrush .Trends — no data returned for {brand_domain} ({YYYY-MM-DD})_`. Log to `cache/topic-discovery-failed.log`. Exit 0. The redteam agent reads the absence as "no trend signal available" and reasons without it.
- **Both calls error with the same auth code (401)**: Semrush MCP isn't connected or consent expired. Surface a clear one-line error to stderr ("Semrush MCP unauthenticated — re-run consent or check `SEMRUSH_API_KEY_BLOG_AGENT`") and exit 0 anyway. The orchestrator continues.
- **Rate-limit (429)**: persist whatever responses we did get; if neither call succeeded, write the stub artefacts and log the quota event. Exit 0 (do **not** propagate exit 75 — Layer 0 is non-blocking). The orchestrator will pick up the cached stubs on the next run.

The discipline here is the user's call-out: "the pipeline never blocks on Layer 0 because it's enrichment, not a gate."

## Quality checklist

- [ ] `topic-graph.json` exists and parses as JSON
- [ ] `brand_snapshot` matches current `brand-config.md` SHA-256
- [ ] `clusters` array is sorted by volume descending (or empty + `_meta.degraded: true`)
- [ ] Each non-degraded cluster has at least: id, name, volume, headlines, questions
- [ ] `trends.md` exists and has a section heading even if empty
- [ ] Failure paths log to `cache/topic-discovery-failed.log` rather than crashing
- [ ] Two MCP calls maximum per actual run; zero on no-op
- [ ] Cache files are under `content-pipeline/0-keywords/cache/` (gitignored)

## Why this exists

Ryan Law's pre-Semrush method had no equivalent of Topic Research or .Trends — Ahrefs surfaced individual keywords but not the **cluster topology** of a category, and not the **time-axis momentum** signal that tells you whether a topic is rising or fading. Both are first-class signals in Semrush.

- The cluster topology lets Layer 1a generate seeds that match how the brand's category is actually organized in Google's view (rather than a brand-config-trained generative guess).
- The momentum signal lets Layer 4's redteam reject keywords that look attractive but are on a 12-month decline — an opportunity-cost critique the legacy pipeline couldn't make.

Adding Layer 0 doesn't disturb the existing chain — Layers 1–5 still run if Layer 0 produces nothing. It's pure enrichment, gated on a cheap idempotency check.

## When the brand-config has no clear category

(Edge case: a personal blog or generic agency site without a sharp category positioning.) The root seed will be too broad and Topic Research returns a shallow cluster tree. The skill still runs — it writes whatever it gets, and downstream layers behave as if Layer 0 returned an empty tree. No special-casing required; the failure-handling path covers it.

## Invocation from the master orchestrator

`/keyword-research-pipeline` calls this skill **first**, before Layer 1a. Because of the brand-config hash check, the master can call it on every run without worrying about waste. On a typical run with stable brand-config, Layer 0 is a < 1-second no-op.

## References

- `.claude/skills/research/references/semrush-mcp-cheatsheet.md` — Topic Research playbook (sections "Topic Research playbook" and ".Trends quick-reference")
- `.claude/skills/keyword-research-pipeline/references/semrush-mcp-tool-inventory.md` — source of truth for the actual `mcp__semrush__*` tool names exposed by the connected MCP. Verify `mcp__semrush__topic-research` and `mcp__semrush__trends-overview` resolve to live tools before assuming the placeholders are correct.
- `.claude/skills/keyword-research-pipeline/references/semrush-metric-translation.md` — KSB cluster id is the "parent topic" replacement; reference for downstream layers that read `topic-graph.json`.
