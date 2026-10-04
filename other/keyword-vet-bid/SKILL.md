---
name: keyword-vet-bid
description: Layer 2 of the keyword research pipeline. Runs the BID method (Business potential / Intent / Difficulty) on every candidate keyword. Rejects keywords that don't pass all three tests, with reason logged. The mechanical filter that drops obvious bad fits before downstream layers spend tokens on them.
allowed-tools: Read, Write, Edit, Bash, mcp__semrush__*
---

# Keyword Vet — BID Method

> **DATA LAYER RULING (2026-06-12).** Every `mcp__semrush__<kebab-name>` tool named below is FICTIONAL (never existed on the live server), and DataForSEO is retired. Before making any data call, read [`../keyword-research-pipeline/references/semrush-data-layer.md`](./../keyword-research-pipeline/references/semrush-data-layer.md) — it maps this layer's old calls to the real Semrush MCP pattern (`get_report_schema` -> `execute_report`). The logic below (filters, thresholds, output schema) remains binding; only the data calls changed.

For every candidate in `keyword-ideas.csv`, run three tests:
1. **B**usiness potential — would ranking #1 actually move the needle for this brand?
2. **I**ntent — does the keyword's intent match what we'd publish (a blog post)?
3. **D**ifficulty — can the brand realistically rank against the current top 10?

If a keyword fails any test, mark `bid_verdict=FAIL` with reason. Failures stay in the CSV (transparency, future re-vet) but are excluded from the queue downstream.

This is the mechanical filter — heuristics + Semrush metrics, no LLM judgment yet. Layer 4 (`/keyword-redteam`) is where the LLM challenges Layer 2's verdicts.

> **Threshold reminder.** Every threshold in this skill is recalibrated for Semrush per `.claude/skills/keyword-research-pipeline/references/semrush-metric-translation.md`. **Never transplant Ahrefs thresholds.** AS tends ~5-10 points lower than DR for the same site; KD% is materially stricter than KD. The full BID method including the recalibration math lives in `.claude/skills/keyword-research-pipeline/references/bid-method.md`. Read both before tuning.

## Input

`/keyword-vet-bid`

Reads:
- `content-pipeline/0-keywords/keyword-ideas.csv` (must exist; from Layer 1)
- `brand-config.md` (audience, products, brand domain for AS comparison)
- `content-pipeline/0-keywords/cache/brand-as.json` — cached brand Authority Score (refresh weekly)

## Process

1. **Resolve brand AS.** Read `cache/brand-as.json` if < 7 days old. Otherwise call `mcp__semrush__domain-overview` for the brand domain — read the `authority_score` field — and write `cache/brand-as.json` with `{ "domain": "...", "authority_score": N, "fetched_at": "ISO-8601" }`. Brand AS is the reference point for the difficulty test. (The legacy file `brand-dr.json` is retired; if it lingers, delete it — its DR-shaped payload will silently mis-calibrate the gate.)

2. **Read brand context** for the Business potential test:
   - Audience persona + pain points
   - Live products + their use cases
   - Monetization model (informs which keywords actually produce revenue)

3. **For each row in `keyword-ideas.csv`:**

   ### B — Business potential

   - Compute `brand_fit` (0-10): does this keyword address a known audience pain point?
     - 10 = directly addresses a stated pain point in brand-config
     - 7 = relevant topic the audience cares about
     - 4 = adjacent, audience might find it useful
     - 0 = wrong audience entirely
   - Compute `product_fit` (0-10): how naturally can a brand product be the demonstration?
     - 10 = the article is impossible to write well without mentioning a brand product
     - 7 = product strongly helps demonstrate the topic
     - 4 = product can be mentioned in passing
     - 0 = no relevant product
   - **Reject** if `brand_fit < 4` OR `product_fit < 3`. (When the brand has no products, set `product_fit_weight=0` and skip the product check — same logic as `keyword-prioritization` for personal-blog cases.)
   - **Reject** if the keyword is a "vanity rank" — high traffic but no path to revenue/users (e.g. brand keyword for a competitor, or pure curiosity terms with no commercial relevance).

   ### I — Intent (Semrush classifier primary, SERP-grounded fallback)

   #### Phase 4e — Semrush `intents` array as the primary BID-Intent signal

   The Semrush `intents` array on `mcp__semrush__keyword-overview` is the per-keyword intent classification (informational / navigational / commercial / transactional). It is **higher quality than re-deriving intent from URL patterns on the SERP** — Semrush trains the classifier on click data, not heuristics. Use it as the primary signal:

   - Pull `intents` from `mcp__semrush__keyword-overview` (already in the row from Layer 1 if present; re-fetch if missing).
   - Apply the policy:
     - `informational` ∈ intents (alone or with `commercial`) → `intent_match=PASS`
     - `commercial` ∈ intents (alone or with `informational`) → `intent_match=PASS`
     - `transactional` is the dominant intent → `intent_match=FAIL` reason `serp_is_transactional`
     - `navigational` is the only intent → `intent_match=FAIL` reason `serp_is_navigational`
     - `intents` is empty / mixed-without-clear-dominant → fall through to the SERP-grounded fallback below

   #### Fallback — URL/title heuristic on the SERP top-10 (demoted to tie-breaker)

   When `intents` is empty, equally split, or disagrees with brand fit, classify the SERP top-10 by URL pattern + title heuristics. Same code as the legacy Ahrefs pipeline used; demoted to fallback. Call `mcp__semrush__serp-results` (or `mcp__semrush__serp-overview` for the SERP feature list when results are not needed) for the keyword and look at the top 10 URLs:

   - `informational` — blog posts, how-to articles, knowledge-base entries (paths like `/blog/`, `/learn/`, `/how-to/`, `/guides/`; titles starting with how/what/why/guide)
   - `commercial-investigation` — best-of lists, comparison articles, reviews (paths like `/best/`, `/vs/`, `/review/`; titles like "best X for Y" or "X vs Y")
   - `transactional` — e-commerce category, product detail, pricing pages (paths like `/products/`, `/shop/`, `/pricing/`; e-commerce platform domains; price in title or snippet)
   - `hybrid` — mixed top 10 (e.g. 4 blog + 4 product + 2 tool)

   Match policy on the fallback:
   - Accept `informational`, `commercial-investigation`, `hybrid` → `intent_match=PASS`
   - Reject `transactional` → `intent_match=FAIL` reason `serp_is_transactional`

   #### Independent gate — tool-led detection (NOT a Semrush `intents` value)

   `tool-led` is **not** a label in Semrush's `intents` array. Run the URL/title heuristic separately as a routing gate, regardless of what `intents` says:

   - If the SERP top 5 contains ≥ 3 results with `/tools/`, `/calculator/`, `/generator/` paths or "free X tool" titles → mark for `tool-opportunities.csv` (separate output, not for the writing queue) and set `intent_match=FAIL` reason `serp_is_tool_led_route_to_tools`. Layer 5 handles the routing.

   Persist the classification to `serp_intent` column (use `intents`-array-derived label when available; fallback label otherwise).

   ### D — Difficulty (KD% + AS + weak-link check)

   - Pull `kd_percent` and `volume` from cache or `mcp__semrush__keyword-overview` (already in the row from Layer 1, but re-fetch if missing).
   - Pull AS for the top 10 ranking domains via `mcp__semrush__serp-overview` (returns the SERP results enriched with per-URL Page AS / domain AS) or `mcp__semrush__domain-overview` per domain when the SERP-overview payload doesn't include it. Batch where the MCP supports it; otherwise iterate.
   - Compute:
     - `as_top10_median` — median Authority Score of the top 10 domains
     - `referring_domains_top10_median` — median referring-domain count of top 10 pages (if exposed in `serp-overview`; otherwise leave null)
     - `weak_link_count` — number of top-10 results with `AS < (brand_AS + 4)` (these are "displaceable" pages — note the +4 vs the legacy +5 to compensate for AS scaling)
   - Apply the rule (recalibrated for Semrush AS — see `semrush-metric-translation.md`):
     - **Accept** if `as_top10_median ≤ brand_AS + 12` (within striking distance — was `+15` for Ahrefs DR; tightened by 3 to compensate)
     - **Accept** if `weak_link_count ≥ 2` (at least two pages we can displace by being better)
     - **Reject** otherwise → `difficulty_match=FAIL` reason `as_gap_too_wide`

4. **Compute `bid_verdict`** per row:
   - `PASS` if all three tests pass
   - `FAIL` otherwise; record `bid_reason` as the first failed test

5. **Write enriched columns back to `keyword-ideas.csv`.** Add columns if missing:
   - `brand_fit`, `product_fit`, `serp_intent`, `as_top10_median`, `referring_domains_top10_median`, `weak_link_count`, `bid_verdict`, `bid_reason`
   - Existing rows get updated; no duplication.

6. **Print a summary**:
   ```
   Vetted N candidates:
     B (business potential): X PASS, Y FAIL
     I (intent):             X PASS, Y FAIL (Z routed to tool-opportunities)
                             primary signal source: A intents-array, B URL-fallback
     D (difficulty):         X PASS, Y FAIL
     Overall:                X PASS, Y FAIL
   Top 5 PASS by traffic_potential:
     1. <keyword> — TP <n>, KD% <n>, intents=<>, AS-gap=<>
     ...
   Top 5 FAIL with reasons:
     1. <keyword> — <reason>
     ...
   ```

## Output

Updated `content-pipeline/0-keywords/keyword-ideas.csv` with BID columns + verdict.

## Quality checklist

- [ ] Every row has `bid_verdict` populated (no nulls)
- [ ] At least 1 keyword failed each of the three reasons (sanity check that the gates aren't too lenient — if everything passes, the heuristics need tightening)
- [ ] `cache/brand-as.json` freshness logged; no leftover `brand-dr.json` on disk
- [ ] ≥ 70% of rows used `intents`-array as the primary intent signal (if the share is much lower, Layer 1 isn't pulling `intents` properly — fix upstream)
- [ ] SERP intent looks correct on a manual spot-check of 3-5 keywords (e.g. "best X" should be commercial-investigation, not informational)
- [ ] `weak_link_count` is plausible (zero on highly competitive queries, multiple on niche queries)

## Why mechanical, not LLM-judged

LLMs are fine for judgment calls — that's Layer 4's job. But running 200+ keywords through a token-heavy adversarial vetting at this stage burns budget on candidates that fail mechanical tests anyway. BID is heuristic-driven by design: cheap, fast, deterministic, auditable. Layer 4 then takes the survivors and challenges them on judgment-heavy questions (where mechanical heuristics blind-spot — e.g. "the SERP intent looks informational but the brand intent really matters here").

## Calibration

> Recalibration math reference: `.claude/skills/keyword-research-pipeline/references/semrush-metric-translation.md`. Don't tune thresholds without reading it first.

- **If everything passes:** thresholds are too loose. First-line tighten:
  - `brand_fit` floor 5 (was 4)
  - `product_fit` floor 4 (was 3)
  - AS gap to `brand_AS + 8` (was `+12`)
  - KD% ≤ 60 (was 70)
- **If nothing passes:** thresholds are too tight, OR the candidate pool is genuinely poor (Layer 1 issue). Look at the top FAIL reasons:
  - `as_gap_too_wide` dominates → brand AS may be too low for current ambition. Relax the gap to `brand_AS + 20` once and re-run.
  - `serp_is_transactional` dominates → Layer 1's seed/modifier mix is wrong (commerce-leaning candidates leaked through). Adjust modifiers — drop "buy", "shop"; keep "best", "vs", "review".
  - `brand_fit < 4` dominates → seeds are too generic. Tighten Layer 1a's prompt to require seeds tied to specific audience pain points.

Calibration logs go to `content-pipeline/0-keywords/cache/bid-calibration.log` so the orchestrator can see threshold drift over time.

## When the brand has no live products

`product_fit` is computed but its weight in the gate is zeroed out. The brand_fit floor stays at 4. This handles personal blogs, agency sites, and brands in pre-product mode.

## When the SERP can't be fetched

If `mcp__semrush__serp-results` / `mcp__semrush__serp-overview` errors (rate-limit, query has no SERP data) AND the keyword's `intents` array is empty (no primary-signal fallback available), mark `serp_intent=unknown` and treat as a soft FAIL with reason `serp_unavailable`. These are revisited on the next pipeline run when quota resets — they don't block the queue, they just don't make it into this run's queue.

If `intents` is populated but the SERP fetch fails, the difficulty test loses `as_top10_median` / `weak_link_count`. Mark `difficulty_match=FAIL` reason `serp_unavailable_for_difficulty` rather than passing on partial data.

## No Ahrefs fallbacks

`mcp__ahrefs__*` is retired. If you find one in this skill or in cached artifacts, it's a leftover from migration — remove it, don't try to fall back. Quota errors from Semrush surface as exit 75 (orchestrator handles retry on next cron cycle).
