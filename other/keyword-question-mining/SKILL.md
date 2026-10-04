---
name: keyword-question-mining
description: Layer 1d of the keyword research pipeline. Mines question-shaped keywords from Semrush phrase_questions (per surviving seed) plus People-Also-Ask strings from the SERP. Appends rows to keyword-ideas.csv with source=question_mining (or merges to source=both when the keyword already exists) and a question_subtype column. Cap of 100 rows per run.
allowed-tools: Read, Write, Edit, Bash, mcp__semrush__*
---

# Keyword Question Mining Skill (Layer 1d)

> **DATA LAYER RULING (2026-06-12).** Every `mcp__semrush__<kebab-name>` tool named below is FICTIONAL (never existed on the live server), and DataForSEO is retired. Before making any data call, read [`../keyword-research-pipeline/references/semrush-data-layer.md`](./../keyword-research-pipeline/references/semrush-data-layer.md) — it maps this layer's old calls to the real Semrush MCP pattern (`get_report_schema` -> `execute_report`). The logic below (filters, thresholds, output schema) remains binding; only the data calls changed.

Extract question-form keywords from the brand's category and the existing candidate pool. Question-form keywords have less competition, higher informational intent, and map cleanly to PAA-driven SERP real estate. Ryan Law explicitly flags the under-delivery of question keywords as a gap in the legacy method — Layer 1d closes it.

This is a **first-class source**, not a bolt-on. The rows it appends become regular candidates that flow through Layer 2 (BID), Layer 3 (AIO), Layer 4 (redteam), and Layer 5 (prioritization) like any other.

## Input

`/keyword-question-mining`

Reads:
- `content-pipeline/0-keywords/seeds.json` — surviving seeds from Layer 1a
- `content-pipeline/0-keywords/keyword-ideas.csv` — current candidate pool (Layers 1b + 1c output)
- `brand-config.md` — used only to read the country code for SERP results (defaults to US)

No CLI flags. The skill is deterministic given its inputs and the global cap.

## Process

1. **Load inputs.**
   - Parse `seeds.json` — extract the `seeds` array. If the file is missing, skip Source A (Keyword Magic Questions) and proceed with Source B alone, logging the absence.
   - Read `keyword-ideas.csv`. If the file doesn't exist, write a stub header (matching the contract in `content-gap-analysis/SKILL.md` step 9) plus the new `question_subtype` column, then proceed — Source B will run on an empty top-30 pool and produce zero rows; Source A still adds value.

2. **Ensure the `question_subtype` column exists.** If `keyword-ideas.csv` already has rows but no `question_subtype` header, add the column to the header row and backfill empty values for every existing row. Use atomic write (write to `.tmp` then move) to avoid corruption mid-edit.

3. **Source A — Keyword Magic Questions per seed.**
   For each seed in `seeds.json`:
   - Call `mcp__semrush__keyword-magic-questions` with the seed as the keyword. Request question-form variants with volume + KD% + `intents` array.
   - Drop rows with `volume < 10` (the cheatsheet's filtering rule for Keyword Magic; matches the volume floor in `semrush-mcp-cheatsheet.md` "Keyword filtering rules"). Keep rows with no volume only if they look like strong question themes (recognizable "how to / what is / why does / can I" prefixes); these often have under-counted long-tail volume.
   - Drop branded-competitor terms (e.g. for Pleasur.AI, drop questions containing `candy.ai`, `ourdream.ai`, `createporn.com` etc. — pull this list from `cache/competitors.json` if present, otherwise skip the filter).
   - Cap per-seed expansion at **20 results** so a 10-seed brand yields ≤ 200 raw Source A candidates before the global cap kicks in.
   - Tag each surviving row with `question_subtype = km_question`.

4. **Source B — PAA mining from top 30 candidates.**
   - Sort the existing rows in `keyword-ideas.csv` by `priority_score` descending, falling back to `traffic_potential` descending when `priority_score` is empty (which is normal pre-Layer-2 — the column is filled by Layer 5).
   - Take the top **30** rows.
   - For each, call `mcp__semrush__serp-results` and parse `serp_features.people_also_ask` for the literal PAA strings.
   - Each PAA string becomes a candidate. Drop strings shorter than 4 words (PAA boilerplate), longer than 20 words (long-form questions that don't survive in Google), or containing brand-name placeholders (`{`, `}`, etc.).
   - Tag each surviving row with `question_subtype = paa`.

5. **Cap to 100 rows per run.** After collecting Source A + Source B, deduplicate-then-cap:
   - First, dedupe within the new-rows pool (case-insensitive, trim whitespace) so two seeds producing the same question collapse to one row.
   - Sort the deduped pool by an internal tier order: `paa > km_question`, then by `volume` descending. PAA wins the tie because PAA presence is a direct SERP-feature signal of search intent, whereas Keyword Magic Questions can include long-tail noise.
   - Keep the top 100. Drop the rest. Log the drop count to `cache/question-mining-skipped.log` for visibility.

6. **Merge with existing rows in `keyword-ideas.csv`.** For each capped new row:
   - **If the keyword already exists** (case-insensitive match on the `keyword` column): set the existing row's `source` to `both`, set `question_subtype` to `both` if the existing subtype was already populated (from a prior Layer 1d run with a different subtype), otherwise set to the new subtype. Don't overwrite metric columns (`volume`, `kd`, `traffic_potential`, etc.) — the existing row's values were already enriched by Layer 1b/1c.
   - **If the keyword is new**: append a fresh row with:
     - `keyword`, `volume`, `kd`, `traffic_potential` (from Source A; for Source B, traffic_potential may be missing — write empty string)
     - `parent_topic` (from Source A's `first_keyword_group` / KSB cluster id; for Source B, run `mcp__semrush__keyword-magic-questions` with the PAA string as the keyword to enrich, OR write empty string and let Layer 2 enrich during BID — the latter saves quota)
     - `intent` (from Source A's `intents` array, joined as comma-list)
     - `source = question_mining`
     - `question_subtype = km_question` or `paa`
     - `serp_features` = empty (Layer 2 fills this)
     - All BID/AIO/redteam columns and `priority_score`, `notes` left empty (Layers 2-5 fill them)

7. **Write `keyword-ideas.csv`** atomically (write to `.tmp` then move). Preserve the original column order; the new `question_subtype` column lives between `source` and `serp_features` (i.e. just after the existing `source` column, so it's logically grouped with the other source-related metadata).

8. **Print a one-line summary**: rows from Source A, rows from Source B, merges into existing rows, new rows added, skipped (over the 100 cap), top 5 new question keywords by volume.

## Output

Rows appended (or merged) to `content-pipeline/0-keywords/keyword-ideas.csv`. New column: `question_subtype`.

## Column contract

After Layer 1d, the row contract for `keyword-ideas.csv` is:

| Column | Source layer | Notes |
|---|---|---|
| `keyword` | 1a/1b/1c/1d | unique key |
| `volume` | 1b/1c/1d | int; ≥ 10 for question_mining rows (or empty for strong-theme PAA) |
| `kd` | 1b/1c/1d | KD% per Semrush; ≤ 70 default Layer 1 filter |
| `traffic_potential` | 1b/1c/1d | may be empty for PAA-only rows |
| `competitor_top_position` | 1b | empty for question_mining-only rows |
| `competitor_domains` | 1b | empty for question_mining-only rows |
| `parent_topic` | 1b/1c/1d | KSB cluster id (preferred) / `first_keyword_group` (fallback) |
| `intent` | 1b/1c/1d | comma-list from Semrush `intents` array |
| `source` | 1a/1b/1c/1d | `competitor_gap` / `seed_modifier` / `aio_gap` / `question_mining` / `both` |
| **`question_subtype`** (NEW) | 1d | `km_question` / `paa` / `both` / empty (for non-question rows) |
| `serp_features` | 2 | filled by Layer 2 |
| `brand_fit`, `product_fit`, `serp_intent`, `dr_top10_median`, `weak_link_count`, `bid_verdict`, `bid_reason` | 2 | |
| `has_aio`, `aio_completeness_score`, `aio_click_intent`, `aio_verdict`, `aio_reasoning` | 3 | |
| `redteam_verdict`, `redteam_priority_delta`, `redteam_critique_summary` | 4 | |
| `priority_score`, `notes` | 5 | |

The `question_subtype` field stays empty for rows that didn't come from Layer 1d (competitor_gap, seed_modifier, aio_gap-only sources). Layer 5 (`/keyword-prioritization`) doesn't apply a boost on `question_subtype` directly — question keywords flow through the same scoring, with their lower KD% and higher informational intent already lifting `priority_score` naturally.

## Why the cap is 100

Two reasons:
1. **Quota discipline.** A 10-seed brand could in theory produce 10 × 20 = 200 Source A rows + 30 Source B rows = 230 candidates. Half of those would be near-duplicates of existing rows or low-volume long-tail noise. 100 is the empirically-supported "where the signal stops mattering" line — past the 100th row, downstream BID rejection rates approach 80%, so the marginal API cost stops paying for itself.
2. **Layer 2 throughput.** Layer 2 (BID) does ~3 SERP/Domain calls per row. An extra 100 rows is ~300 additional Semrush calls — material but not catastrophic. 200+ would push Layer 2 past the per-run quota window for budget-tier Semrush plans.

If the cap bites repeatedly (logged > 5 times per week to `cache/question-mining-skipped.log`), revisit the per-seed cap (currently 20) before raising the global cap — the per-seed cap is the right knob for noise-vs-signal trade-off.

## Quality checklist

- [ ] `question_subtype` column exists in `keyword-ideas.csv` after the run
- [ ] All Layer 1d new rows have `source = question_mining` (and `question_subtype` ∈ {`km_question`, `paa`})
- [ ] Existing rows that received a Layer 1d match have `source = both` and `question_subtype` populated
- [ ] No more than 100 new+merged rows added by this run
- [ ] PAA strings are 4–20 words; below/above is dropped
- [ ] No competitor-branded questions in km_question rows (when `cache/competitors.json` exists)
- [ ] Atomic CSV write — no half-written file on crash

## Failure handling

- **`mcp__semrush__keyword-magic-questions` errors for a single seed**: log the seed + reason to `cache/question-mining-failed.log` and skip that seed; continue with the rest. A single seed failing isn't fatal; some seeds reliably produce no question-form variants.
- **`mcp__semrush__serp-results` rate-limit (429) during Source B**: persist whatever rows were collected in Source A, write them to `keyword-ideas.csv`, then exit code 75. The orchestrator handles retry on the next cron cycle (matches the convention in `keyword-research-pipeline/SKILL.md`).
- **`seeds.json` missing**: log to `cache/question-mining-failed.log`, skip Source A, run Source B alone, exit 0. Layer 1d still adds value from PAA mining even without seed expansion.
- **`keyword-ideas.csv` empty / missing top-30**: write the new column header, run Source A only, exit 0. Source B contributes nothing without an existing pool, which is fine — Layer 1d isn't the candidate-pool generator (Layers 1b/1c are).

Layer 1d is **not blocking** in the same way Layer 0 isn't blocking — the orchestrator continues to Layer 2 even if Layer 1d added zero rows. But unlike Layer 0, an outright crash here propagates because it indicates an MCP/connectivity problem the operator should see.

## When question keywords overlap heavily with existing rows

That's fine. The merge logic preserves the richer metadata from Layer 1b/1c (which had `competitor_top_position` / `aio_engines` etc.) and just upgrades the `source` field to `both`. The `question_subtype` field gets set so Layer 2's intent classification and Layer 5's prioritization can still see "this keyword is question-shaped" as a signal.

When the merge rate exceeds 70% (logged in the run summary), it usually means either: (a) the brand's category is already well-mined and Layer 1d isn't surfacing fresh territory — fine, the layer is essentially a no-op week; or (b) the seed list is too narrow — escalate to revisiting `seeds.json` via `/seed-modifier-prompt --regen`.

## Invocation from the master orchestrator

`/keyword-research-pipeline` calls Layer 1d **after** Layer 1c (`/keyword-aio-gap`) and **before** Layer 2 (`/keyword-vet-bid`). The orchestrator's brief for this layer is:

```
You are running Layer 1d at {ROOT}.

Your job: append question-shaped keywords to content-pipeline/0-keywords/keyword-ideas.csv per .claude/skills/keyword-question-mining/SKILL.md. Read the SKILL.md first.

Source A: for each seed in seeds.json, call mcp__semrush__keyword-magic-questions; cap 20 results per seed; tag question_subtype=km_question.
Source B: for top-30 by priority_score (or traffic_potential pre-Layer-2), call mcp__semrush__serp-results, parse serp_features.people_also_ask; tag question_subtype=paa.

Cap 100 new+merged rows total. Existing rows get source=both on overlap.

If serp-results returns 429, persist Source A rows and exit 75.

Return: Source A count, Source B count, merges into existing rows, new rows, skipped (cap), top 5 new question keywords by volume. Under 250 words.
```

## References

- `.claude/skills/research/references/semrush-mcp-cheatsheet.md` — Keyword Magic filtering rules (volume floor ≥ 10, intent classification, KSB clustering)
- `.claude/skills/keyword-research-pipeline/references/semrush-mcp-tool-inventory.md` — verify `mcp__semrush__keyword-magic-questions` and `mcp__semrush__serp-results` resolve to live tool names
- `.claude/skills/keyword-research-pipeline/references/semrush-metric-translation.md` — KD% thresholds (Layer 1 floor: ≤ 70), intent-array primacy
- `.claude/skills/content-gap-analysis/SKILL.md` — column contract for `keyword-ideas.csv` (Layer 1d preserves and extends it)
