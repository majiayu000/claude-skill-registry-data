---
name: keyword-vet-bid
description: Layer 2 of the keyword research pipeline. Runs the BID method (Business potential / Intent / Difficulty) on every candidate keyword. Rejects keywords that don't pass all three tests, with reason logged. The mechanical filter that drops obvious bad fits before downstream layers spend tokens on them.
allowed-tools: Read, Write, Edit, Bash, mcp__ahrefs__*
---

# Keyword Vet — BID Method

> **Data layer: Ahrefs MCP** (`mcp__ahrefs__*`). Read [`../research/references/ahrefs-mcp-cheatsheet.md`](../research/references/ahrefs-mcp-cheatsheet.md) first — string params not JSON arrays, `select`+`country` required, `doc {tool:"..."}` any unfamiliar tool. The logic below (filters, thresholds, schema) is binding.

For every candidate in `keyword-ideas.csv`, run three tests:
1. **B**usiness potential — would ranking #1 actually move the needle for this brand?
2. **I**ntent — does the keyword's intent match what we'd publish (a blog post)?
3. **D**ifficulty — can the brand realistically rank against the current top 10?

If a keyword fails any test, mark `bid_verdict=FAIL` with reason. Failures stay in the CSV (transparency, future re-vet) but are excluded from the queue downstream.

This is the mechanical filter — heuristics + Ahrefs metrics, no LLM judgment yet. Layer 4 (`/keyword-redteam`) is where the LLM challenges Layer 2's verdicts.

> **Threshold reminder.** Every threshold in this skill is the Ahrefs-edition gate documented in `.claude/skills/keyword-research-pipeline/references/bid-method.md` (which now carries the recalibration math inline — the old `*-metric-translation.md` doc is retired). The full BID method including the gate math lives there. Read it before tuning any number; don't let an Agent invent a threshold from training data.

## Input

`/keyword-vet-bid`

Reads:
- `content-pipeline/0-keywords/keyword-ideas.csv` (must exist; from Layer 1)
- `brand-config.md` (audience, products, brand domain for DR comparison)
- `content-pipeline/0-keywords/cache/brand-dr.json` — cached brand Domain Rating (refresh weekly)

## Process

1. **Resolve brand authority.** Read `cache/brand-dr.json` if < 7 days old. Otherwise **run `scripts/refresh_brand_authority.py`** (under doppler) — it fetches our live DR + referring-domain data and writes the FULL `cache/brand-dr.json` (`domain_rating` + **`max_targetable_kd`** + RD figures). **Do NOT hand-write a DR-only brand-dr.json** — that clobbers `max_targetable_kd`, which Layer 5 winnability needs. Brand DR is the reference point for the difficulty test; `max_targetable_kd` (the hardest KD we can realistically rank for at this DR) is the reach ceiling for winnability — both move as our authority grows. (Any legacy `brand-as.json` is retired; if it lingers, delete it — its AS-shaped payload will silently mis-calibrate the gate.)

   **MANDATORY — fail loud, never fall back to a bare KD cutoff.** Brand DR is the reference point for *every* difficulty decision in this run. If `cache/brand-dr.json` is absent AND the live `site-explorer-domain-rating` call fails (Ahrefs MCP/REST down), **HALT the keyword-research run** with a clear error (`brand_dr_unavailable — Ahrefs is the sole SEO source and is down; cannot calibrate difficulty`). Do **NOT** proceed by gating on KD alone (e.g. "KD ≤ 70") — KD is absolute and ignores OUR domain; a DR-21 site that "passes" a KD-50 term that way is publish-and-pray. A blind gate is worse than no gate. (As of 2026-06-29, pleasur.ai DR ≈ **21** — a young domain; the cache is pre-seeded with this value.)

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
   - Set `business_value` (0-3) from `product_fit` gated by audience (see `bid-method.md` B#4): 3 = product is the natural answer for a paying-prospect topic; 2 = helps/mentionable; 1 = weak path; 0 = no product fit. **Do NOT reward salesy "best/review/pricing" phrasing** — `product_fit` already scores genuine fits high, and the Ahrefs model favors useful *informational* product-adjacent posts over thirsty listicles.
   - Set the `free_seeker` flag when the keyword signals a non-paying reader ("free", "no-filter", "uncensored", "unfiltered", "unlimited", "without paying/account"). **Do NOT reject** — persist `business_value` + `free_seeker` for Layer 5, which weights product-fit over traffic and penalizes free-seekers (the fix for the "high traffic, 0 paid" leak the scorecard surfaced).

   ### I — Intent (Ahrefs classifier primary, SERP-grounded fallback)

   #### Phase 4e — Ahrefs `intents` array as the primary BID-Intent signal

   The Ahrefs `intents` array on `keywords-explorer-overview` is the per-keyword intent classification (informational / navigational / commercial / transactional). It is **higher quality than re-deriving intent from URL patterns on the SERP** — the classifier is trained on click data, not heuristics. Use it as the primary signal:

   - Pull `intents` from `keywords-explorer-overview` (already in the row from Layer 1 if present; re-fetch if missing).
   - Apply the policy:
     - `informational` ∈ intents (alone or with `commercial`) → `intent_match=PASS`
     - `commercial` ∈ intents (alone or with `informational`) → `intent_match=PASS`
     - `transactional` is the dominant intent → `intent_match=FAIL` reason `serp_is_transactional`
     - `navigational` is the only intent → `intent_match=FAIL` reason `serp_is_navigational`
     - `intents` is empty / mixed-without-clear-dominant → fall through to the SERP-grounded fallback below

   #### Fallback — URL/title heuristic on the SERP top-10 (demoted to tie-breaker)

   When `intents` is empty, equally split, or disagrees with brand fit, classify the SERP top-10 by URL pattern + title heuristics. Call `serp-overview` (`{keyword:"<kw>", country:"US", select:"url,title,position,domain_rating,url_rating"}`) for the keyword and look at the top 10 URLs. (⚠️ Do NOT select `serp_features` here — `serp-overview` has no such column and the call hard-errors; SERP-feature signals live on `keywords-explorer-overview`. Verified PLE-3063.)

   - `informational` — blog posts, how-to articles, knowledge-base entries (paths like `/blog/`, `/learn/`, `/how-to/`, `/guides/`; titles starting with how/what/why/guide)
   - `commercial-investigation` — best-of lists, comparison articles, reviews (paths like `/best/`, `/vs/`, `/review/`; titles like "best X for Y" or "X vs Y")
   - `transactional` — e-commerce category, product detail, pricing pages (paths like `/products/`, `/shop/`, `/pricing/`; e-commerce platform domains; price in title or snippet)
   - `hybrid` — mixed top 10 (e.g. 4 blog + 4 product + 2 tool)

   Match policy on the fallback:
   - Accept `informational`, `commercial-investigation`, `hybrid` → `intent_match=PASS`
   - Reject `transactional` → `intent_match=FAIL` reason `serp_is_transactional`

   #### Independent gate — tool-led detection (NOT an Ahrefs `intents` value)

   `tool-led` is **not** a label in Ahrefs's `intents` array. Run the URL/title heuristic separately as a routing gate, regardless of what `intents` says:

   - If the SERP top 5 contains ≥ 3 results with `/tools/`, `/calculator/`, `/generator/` paths or "free X tool" titles → mark for `tool-opportunities.csv` (separate output, not for the writing queue) and set `intent_match=FAIL` reason `serp_is_tool_led_route_to_tools`. Layer 5 handles the routing.

   Persist the classification to `serp_intent` column (use `intents`-array-derived label when available; fallback label otherwise).

   ### D — Difficulty (difficulty (KD) + DR + weak-link check)

   - Pull `difficulty` (KD) and `volume` from cache or `keywords-explorer-overview` (already in the row from Layer 1, but re-fetch if missing).
   - Pull DR for the top 10 ranking domains. `serp-overview` returns the SERP results with per-URL DR/UR where available; when the SERP-overview payload doesn't include it, fall back to `site-explorer-domain-rating` per domain or `batch-analysis` for many domains at once (cheatsheet section 5). Batch where the MCP supports it; otherwise iterate.
   - Compute:
     - `dr_top10_median` — median Domain Rating of the top 10 domains
     - `referring_domains_top10_median` — median referring-domain count of top 10 pages (from `serp-overview` / `site-explorer-backlinks-stats`; otherwise leave null)
     - `weak_link_count` — number of top-10 results with `DR < (brand_DR + 4)` (these are "displaceable" pages)
   - Apply the rule (the Ahrefs-edition gate — see `bid-method.md`):
     - **Accept** if `dr_top10_median ≤ brand_DR + 12` (within striking distance)
     - **Accept** if `weak_link_count ≥ 2` (at least two pages we can displace by being better)
     - **Reject** otherwise → `difficulty_match=FAIL` reason `dr_gap_too_wide`

   **This DR-relative rule IS the difficulty test — a bare `KD ≤ N` threshold is not a substitute.** KD ignores our domain; on a DR-21 site a KD-50 term is unrankable no matter that `50 < 70`. Persist `dr_top10_median`, `referring_domains_top10_median`, and `weak_link_count` on every row even when it PASSES — Layer 5 (`keyword-prioritization`) turns `kd` + `weak_link_count` (relative to brand DR) into the `winnability` score, which is what cherry-picks the easy, rankable wins to the top of the queue (course Lesson 3.4–3.5). A keyword that squeaks past this binary gate but has a wide DR gap will still rank low on winnability — that's intended.

4. **Compute `bid_verdict`** per row:
   - `PASS` if all three tests pass
   - `FAIL` otherwise; record `bid_reason` as the first failed test

5. **Write enriched columns back to `keyword-ideas.csv`.** Add columns if missing:
   - `brand_fit`, `product_fit`, `business_value`, `free_seeker`, `serp_intent`, `dr_top10_median`, `referring_domains_top10_median`, `weak_link_count`, `bid_verdict`, `bid_reason`
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
     1. <keyword> — TP <n>, KD <n>, intents=<>, DR-gap=<>
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
- [ ] `cache/brand-dr.json` freshness logged; no leftover `brand-as.json` on disk
- [ ] ≥ 70% of rows used `intents`-array as the primary intent signal (if the share is much lower, Layer 1 isn't pulling `intents` properly — fix upstream)
- [ ] SERP intent looks correct on a manual spot-check of 3-5 keywords (e.g. "best X" should be commercial-investigation, not informational)
- [ ] `weak_link_count` is plausible (zero on highly competitive queries, multiple on niche queries)

## Why mechanical, not LLM-judged

LLMs are fine for judgment calls — that's Layer 4's job. But running 200+ keywords through a token-heavy adversarial vetting at this stage burns budget on candidates that fail mechanical tests anyway. BID is heuristic-driven by design: cheap, fast, deterministic, auditable. Layer 4 then takes the survivors and challenges them on judgment-heavy questions (where mechanical heuristics blind-spot — e.g. "the SERP intent looks informational but the brand intent really matters here").

## Calibration

> Recalibration math reference: `.claude/skills/keyword-research-pipeline/references/bid-method.md` (Ahrefs edition, math inline). Don't tune thresholds without reading it first.

- **If everything passes:** thresholds are too loose. First-line tighten:
  - `brand_fit` floor 5 (was 4)
  - `product_fit` floor 4 (was 3)
  - DR gap to `brand_DR + 8` (was `+12`)
  - KD ≤ 60 (was 70)
- **If nothing passes:** thresholds are too tight, OR the candidate pool is genuinely poor (Layer 1 issue). Look at the top FAIL reasons:
  - `dr_gap_too_wide` dominates → brand DR may be too low for current ambition. Relax the gap to `brand_DR + 20` once and re-run.
  - `serp_is_transactional` dominates → Layer 1's seed/modifier mix is wrong (commerce-leaning candidates leaked through). Adjust modifiers — drop "buy", "shop"; keep "best", "vs", "review".
  - `brand_fit < 4` dominates → seeds are too generic. Tighten Layer 1a's prompt to require seeds tied to specific audience pain points.

Calibration logs go to `content-pipeline/0-keywords/cache/bid-calibration.log` so the orchestrator can see threshold drift over time.

## When the brand has no live products

`product_fit` is computed but its weight in the gate is zeroed out. The brand_fit floor stays at 4. This handles personal blogs, agency sites, and brands in pre-product mode.

## When the SERP can't be fetched

If `serp-overview` errors (rate-limit, query has no SERP data) AND the keyword's `intents` array is empty (no primary-signal fallback available), mark `serp_intent=unknown` and treat as a soft FAIL with reason `serp_unavailable`. These are revisited on the next pipeline run when units reset — they don't block the queue, they just don't make it into this run's queue.

If `intents` is populated but the SERP fetch fails, the difficulty test loses `dr_top10_median` / `weak_link_count`. Mark `difficulty_match=FAIL` reason `serp_unavailable_for_difficulty` rather than passing on partial data.

## Ahrefs MCP only

All data comes from `mcp__ahrefs__*`. Quota/units errors surface as exit 75 (orchestrator handles retry on the next cron cycle).
