---
name: keyword-prioritization
description: Deterministically score, route, rank, and select at most one fully vetted Pleasur.ai Stage 01 blog-keyword candidate using product-fit-dominant business value, traffic opportunity, brand fit, DR-relative winnability, and a free-seeker penalty. Use only after BID and AIO evaluation are complete.
---

# Keyword Prioritization

Rank only fully evidenced candidates that passed BID. Read [references/scoring-policy.md](references/scoring-policy.md) before calculating scores.

## Required inputs

Require for every candidate:

- keyword, target country, discovery source, volume, KD, traffic potential, parent topic, and current content-gap status;
- BID verdict, brand fit, product fit, product applicability, business value, free-seeker flag, observed intent, tool-led flag, current brand DR, median top-ten DR, weak-link evidence, and BID provenance;
- AIO mode, presence, verdict, reasoning, and AIO evidence provenance;
- an approved, versioned brand/product snapshot, current Pleasur.ai content inventory, and current evidence-backed `max_targetable_kd`;
- the Stage 01 formula/policy version and evidence-freshness decisions.

Use `needs_data` when a required input is missing, stale, contradictory, or country-mismatched. Do not rank incomplete candidates.

## Eligibility and routing

Evaluate every candidate, then route before ranking:

1. BID `FAIL` → `rejected` with the BID reason.
2. BID `needs_data` or AIO `needs_data` → `needs_data`.
3. `aio_verdict=FAIL_CANNIBALIZED` → `rejected`.
4. `aio_verdict=RISKY` → eligible only when the Stage 01 packet explicitly accepts the named information-gain/click requirement; otherwise `needs_data` for human decision.
5. `serp_intent=tool-led` → `routed_tool_opportunity`, never the blog candidate set.
6. Existing strong Pleasur.ai coverage → `track_existing_strength`, never selected for a new article.
7. Remaining BID-PASS and AIO-eligible candidates → scoring pool.

Do not describe routed or unselected candidates as rejected unless a gate actually failed.

## Scoring process

### 1. Traffic score

Calculate a 0–10 opportunity score from current traffic potential and KD:

`traffic_raw = min(10, 2 × log10(traffic_potential + 1) - kd / 20)`

Clamp the result to `[0, 10]`. If traffic potential is unavailable, do not silently substitute volume; return `needs_data` unless the approved run policy defines and versions an alternative normalization.

Record raw inputs, calculation, clamping, and formula version.

### 2. Brand and product fit

Reuse the evidence-backed BID scores; do not rescore them during prioritization.

- `brand_fit` remains 0–10.
- `product_fit` remains 0–10 and is the dominant factor when products exist.
- Preserve the named product and fit rationale.

If the approved brand snapshot has no products, use the no-products formula below and record `product_fit_applicable=false`.

### 3. Winnability

Score 0–10 relative to current Pleasur.ai authority, never KD alone. Require current `brand_dr`, current evidence-backed `max_targetable_kd`, median top-ten DR, and named weak links. Require `max_targetable_kd > brand_dr`; otherwise return `needs_data`.

Calculate `base_winnability` exactly:

- `kd <= brand_dr` → `10`;
- `brand_dr < kd <= max_targetable_kd` → `5 + 3 × (max_targetable_kd - kd) / (max_targetable_kd - brand_dr)`;
- `max_targetable_kd < kd <= max_targetable_kd + 15` → `3`;
- `kd > max_targetable_kd + 15` → `1` and `above_ceiling=true`.

If `weak_link_count >= 3`, set `winnability = min(10, base_winnability + 2.0)` and name the three or more URLs supporting the override. Otherwise set `winnability = base_winnability`. Keep full precision through final ranking.

If current `max_targetable_kd` is unavailable, return `needs_data`. Do not derive an alternative from qualitative bands or revive a legacy cache value.

### 4. Free-seeker penalty

Set `free_seeker_penalty=0.4` when BID flagged the query as free-seeking; otherwise use `1.0`. Keep the candidate eligible unless another gate fails. Add `top-of-funnel / low-business-value` to its rationale.

### 5. Priority score

When products exist, calculate:

`priority_score = (0.2 × traffic + 0.2 × brand_fit + 0.4 × product_fit + 0.2 × winnability) × free_seeker_penalty`

When the approved snapshot has no products, calculate:

`priority_score = (0.3 × traffic + 0.4 × brand_fit + 0.3 × winnability) × free_seeker_penalty`

Keep full precision for sorting and display a consistent rounded value separately. Apply no boost for commercial wording, source, subjective enthusiasm, or preferred outcome.

## Ranking and selection

Sort eligible candidates by:

1. full-precision `priority_score`, descending;
2. traffic potential, descending;
3. KD, ascending;
4. normalized keyword, lexical ascending.

Assign deterministic rank after routing. Approve at most the rank-1 eligible blog candidate. Mark other eligible candidates `evaluated_not_selected`; they remain available for a future run.

If the scoring pool is empty:

- return `needs_data` when any candidate could become eligible after required evidence or human acceptance;
- otherwise return terminal Stage 01 status `rejected` and preserve every gate reason.

Never start Stage 02, draft an article, publish, install a skill, trigger another workflow, or write external systems.

## Output schema

Persist the following in the immutable Stage 01 packet:

- every candidate and its route/status;
- traffic inputs, calculation, score, brand fit, product fit, product applicability, winnability inputs, named weak links, winnability score, business value, free-seeker flag, penalty, and final priority score;
- the exact formula and policy versions;
- tie-break values, deterministic rank, selection reason, and non-selection reason;
- AIO acceptance requirement for every selected RISKY candidate;
- all source provenance, freshness, nulls, conflicts, uncertainty, and human decisions.

Summarize the ranked eligible set, tool opportunities, existing-strength routes, rejected candidates, and `needs_data` candidates. Clearly name the single selected candidate or state that none was selected.

## Quality checks

- Only BID-PASS, AIO-eligible, fully evidenced blog candidates were ranked.
- Tool-led and existing-strength candidates were routed out before ranking.
- Product fit is the dominant weight when products exist.
- Winnability varies with current Pleasur.ai authority and observed SERP evidence.
- The exact interpolation and `+2.0` weak-link adjustment reproduce the same winnability from identical evidence.
- No above-ceiling candidate received high winnability without a named, evidence-backed weak-link override.
- Free-seeker penalty was applied exactly once.
- Full-precision values, tie-breaks, and lexical normalization make the result reproducible.
- At most one candidate is selected; all other survivors are `evaluated_not_selected`.
- No local cache, CSV, repository, CMS, workflow, or production system was mutated.
