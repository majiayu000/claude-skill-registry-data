---
name: content-gap-analysis
description: Layer 1b of the keyword research pipeline. Finds keyword opportunities by comparing the brand's blog against competitors AND by expanding seeds + modifiers via Semrush (phrase_fullsearch / phrase_related). Auto-discovers competitors via domain_organic_organic when none are provided, derives the keyword gap via domain_domains, tags every row with `gap_mode`, and outputs a candidate-keyword CSV ready for downstream BID/AIO vetting.
allowed-tools: Read, Write, Bash, mcp__semrush__*
---

# Content Gap Analysis Skill

> **DATA LAYER RULING (2026-06-12).** Every `mcp__semrush__<kebab-name>` tool named below is FICTIONAL (never existed on the live server), and DataForSEO is retired. Before making any data call, read [`../keyword-research-pipeline/references/semrush-data-layer.md`](./../keyword-research-pipeline/references/semrush-data-layer.md) — it maps this layer's old calls to the real Semrush MCP pattern (`get_report_schema` -> `execute_report`). The logic below (filters, thresholds, output schema) remains binding; only the data calls changed.

Use Semrush's multi-mode Keyword Gap and Keyword Magic Tool to surface keywords competitors rank for that the brand doesn't, plus seed-modifier expansion of the brand's own keyword universe. The output feeds `/keyword-prioritization`, which then feeds `/blog-pipeline` for the chosen keywords.

> **Threshold reminder.** All KD% thresholds in this skill are recalibrated for Semrush per `.claude/skills/keyword-research-pipeline/references/semrush-metric-translation.md`. Semrush KD% is materially stricter than Ahrefs KD — do not transplant Ahrefs thresholds. Read the metric-translation doc before tuning any number here.

## Input

`/content-gap-analysis <competitor-domain> [<competitor-domain> ...] [--our-domain <domain>]`

Examples:
- `/content-gap-analysis competitor1.com competitor2.com`
- `/content-gap-analysis competitor1.com --our-domain mybrand.com`

If `--our-domain` isn't provided, read it from `brand-config.md`.

## Process

1. **Parse input.** Extract competitor domains (CLI args or auto-discover) and read the brand domain from `brand-config.md`.

2. **Resolve competitors.** In order of preference:
   - CLI args (e.g. `/content-gap-analysis competitor1.com competitor2.com`)
   - `brand-config.md` competitor list
   - **Autonomous fallback**: call `mcp__semrush__organic-competitors` for the brand domain, take top 3 by organic-keyword intersection
   - Cache the resolved competitors to `content-pipeline/0-keywords/cache/competitors.json` so Layer 1c (`/keyword-aio-gap`) reuses the same set without re-querying

3. **Read brand context.** Audience, products — used downstream to filter the gap list to relevant intent (Layer 2's BID).

4. **Run multi-mode Keyword Gap analysis via `mcp__semrush__keyword-gap`.** Semrush's Keyword Gap exposes five modes; Layer 1b uses **all five** and tags every returned row with the originating `gap_mode` column. Pass to each call:
   - `our_domain` = brand domain
   - `competitors` = 1–3 competitor domains (Semrush accepts up to 4 in addition to the seed)
   - `country` = US (or read from `brand-config.md` if specified)
   - `min_volume` = 20 (default)
   - `max_kd_percent` = 70 (Semrush KD% — equivalent to legacy Ahrefs KD ≤ 60 per the metric-translation doc)
   - Exclude branded terms for competitors (use the negative-keyword filter on competitor brand strings)

   ### Phase 4b — multi-mode Keyword Gap

   Run the gap report once per mode and concatenate the rows. Tag the originating mode on each row:

   | `gap_mode` | What it means | What to do with it |
   |---|---|---|
   | `missing` | Competitors rank, brand doesn't (the classic content gap) | Default candidates — feed straight into the merged pool |
   | `weak` | Brand ranks 11+, competitors top-10 | Small-effort wins — feed into the pool, prioritization will boost |
   | `unique` | Only one competitor ranks (single point of failure to displace) | High-leverage — feed into the pool, prioritization will boost |
   | `common` | Everyone ranks (saturated SERPs) | Feed into the pool with a penalty applied at Layer 5 — keep for completeness, deprioritize |
   | `strong` | Brand ranks top-3, competitors don't (already won) | **Do NOT feed into the writing queue.** Route to `content-pipeline/0-keywords/cache/strong-positions.csv` for tracking only |

   Run order: `missing` → `weak` → `unique` → `common`. Skip `strong` mode for the writing pool; run it separately and write its rows to `cache/strong-positions.csv` with the same column shape so downstream tooling can read them. Cap each mode at 200 rows sorted by traffic_potential descending.

5. **Pull the gap keyword list.** Aim for ~400–800 raw rows across the four pool-eligible modes (missing/weak/unique/common). Tag each with `source=competitor_gap` and the corresponding `gap_mode`.

6. **Auto-relax filters if pool is small.** If fewer than 50 candidates come back at the default filters, automatically re-run once with relaxed thresholds: volume ≥ 5, KD% ≤ 85 (Semrush — equivalent to legacy Ahrefs KD ≤ 80). Log the relaxation. If still under 50, continue with what we have — Layer 1c (AIO gap) and Layer 1a-driven seed expansion will widen the pool.

7. **Seed-modifier expansion (Layer 1a integration).** If `content-pipeline/0-keywords/seeds.json` exists:
   - For each seed, call `mcp__semrush__keyword-magic-broad` with the seed as the keyword and the modifiers list as an `include` filter (terms include any of the listed strings). Use `mcp__semrush__keyword-magic-phrase` and `mcp__semrush__keyword-magic-related` for breadth where the broad search is thin; use `mcp__semrush__keyword-magic-exact` only when a modifier is a multi-word phrase that needs exact-match expansion.
   - Pull volume, KD%, traffic_potential, `first_keyword_group` (or KSB cluster id when available), and the `intents` array from `mcp__semrush__keyword-overview` for each result that lacks an intent label.
   - Tag each row with `source=seed_modifier` and `gap_mode=seed_modifier` (sentinel value — not one of the five Semrush gap modes).
   - Cap per-seed expansion at 100 results to keep the merged pool manageable.

8. **Merge and dedupe.** Combine competitor-gap rows with seed-modifier rows. Keep one row per unique keyword:
   - If a keyword appears in both a competitor-gap mode and seed-modifier expansion, set `source=both` and retain BOTH `gap_mode` (from the competitor-gap row) and `competitor_top_position` from the gap row, plus the seed_modifier metadata.
   - If a keyword appears in multiple competitor-gap modes (e.g. it shows up in both `missing` and `weak` because two different competitors are scored differently), keep the row with the higher-priority `gap_mode`. Priority order: `unique` > `weak` > `missing` > `common`.
   - Otherwise keep the source-specific row as-is.

9. **Add columns the downstream layers need:**
   - `keyword` (from Semrush)
   - `volume` (monthly searches)
   - `kd_percent` (Semrush Keyword Difficulty %)
   - `traffic_potential` (estimated traffic of the #1-ranking page from `mcp__semrush__keyword-overview` or domain-organic-pages of the top result)
   - `competitor_top_position` (the best position any competitor holds; null for seed_modifier-only rows)
   - `cluster_id` (Keyword Strategy Builder cluster id when available; otherwise empty — Layer 5 uses this for `cluster_authority_gap` boost)
   - `first_keyword_group` (Semrush Keyword Magic group; fallback when `cluster_id` is empty)
   - `intents` (array — Semrush's per-keyword intent classification: informational / navigational / commercial / transactional. Layer 2 uses this as the primary BID-Intent signal)
   - `source` (competitor_gap / seed_modifier / both / aio_gap — Layer 1c will append aio_gap rows)
   - `gap_mode` (missing / weak / unique / common / seed_modifier — populated for every row; `strong`-mode rows go to `cache/strong-positions.csv`, not this CSV)
   - Empty columns for `priority_score`, `brand_fit`, `product_fit`, `notes`, plus the BID/AIO/redteam columns Layers 2-4 will fill

10. **Save as CSV** to `content-pipeline/0-keywords/keyword-ideas.csv`. Use UTF-8, headers in row 1.

11. **Print a one-line summary** (autonomous mode) or suggest running `/keyword-prioritization` next (interactive mode). The summary breaks out row counts per `gap_mode` so the orchestrator can see whether the pool leans `missing` vs `weak` vs `unique`.

## Output

`content-pipeline/0-keywords/keyword-ideas.csv`

A CSV with one row per gap keyword, every row tagged with a `gap_mode`, plus the columns listed above.

`content-pipeline/0-keywords/cache/strong-positions.csv` (parallel — `gap_mode=strong` rows; tracking only, not the writing queue).

## Quality checklist

- [ ] CSV has at least 50 rows (the gap is real)
- [ ] Every row has a `gap_mode` populated (no nulls)
- [ ] No competitor branded terms in the list (e.g. competitor product names)
- [ ] All keywords have volume ≥ 20 (or ≥ 5 if auto-relaxed)
- [ ] All keywords have `kd_percent ≤ 70` (or ≤ 85 if auto-relaxed)
- [ ] `cluster_id` or `first_keyword_group` populated (used by prioritization for cluster_authority_gap)
- [ ] `intents` array populated for ≥ 90% of rows (Layer 2 needs it as the primary BID-Intent signal)
- [ ] File is valid UTF-8 CSV (opens in Excel / Sheets without garbage)
- [ ] `cache/strong-positions.csv` exists when `gap_mode=strong` rows were returned

## When the gap is small

If fewer than 20 results come back, either:
- The brand and competitors are too similar in coverage (good problem) — try different competitors
- The filters were too tight — relax volume to ≥ 5 and KD% to ≤ 85
- Semrush returned a partial result — re-run

## Autonomous behavior

When invoked from `/keyword-research-pipeline` (or with `BLOG_AGENT_AUTONOMOUS=1` set):

- **Auto-discover competitors** via `mcp__semrush__organic-competitors` if neither CLI args nor `brand-config.md` provide any. Take top 3 by organic-keyword intersection. Cache to `cache/competitors.json` so Layer 1c reuses the same set.
- **Run all five gap modes** and tag rows with `gap_mode`. Route `strong` to `cache/strong-positions.csv`; the rest go to the writing pool.
- **Auto-relax filters** if pool is < 50 (volume ≥ 5, KD% ≤ 85; once only).
- **Auto-merge seed-modifier expansion** if `seeds.json` exists.
- **No human prompt** — never ask "which competitors?" or "is this enough?"; the orchestrator can't answer.

## When competitors can't be auto-discovered

If `mcp__semrush__organic-competitors` returns empty (very rare — usually means the brand domain isn't indexed by Semrush, or it's brand-new):

- Log to `cache/competitor-discovery-failed.log`
- Fall through to seed-modifier expansion alone (which doesn't need competitors). Every row will have `source=seed_modifier` and `gap_mode=seed_modifier`.
- Downstream layers handle the empty `competitor_top_position` column gracefully

## Interactive mode (legacy / dev-only)

If neither CLI args nor brand-config nor auto-discovery yields competitors AND `BLOG_AGENT_AUTONOMOUS` is not set, fall back to asking the user. This branch only fires when a human is at the keyboard.

## Tool naming

Tool names follow the placeholder convention from `.claude/skills/keyword-research-pipeline/references/semrush-mcp-tool-inventory.md`. After running the discovery prompt described in that file, replace any name in this skill that doesn't match the verified inventory. **No `mcp__ahrefs__*` calls** — Ahrefs is retired; an Ahrefs call from this skill is a bug, not a fallback.
