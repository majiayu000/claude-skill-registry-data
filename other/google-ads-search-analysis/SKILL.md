---
name: google-ads-search-analysis
description: "Use when analyzing Google Ads Search campaigns: Q1–Q5 query classification, CPC inflation diagnosis, rank/budget pressure, decision matrix, scaling prerequisites."
metadata:
  source: "prompts/skills/google_ads/search-analysis"
---

# Google Ads Search — Analysis & Optimization

> Metric definitions (CPA, ROAS, CVR, CPC, micros conversion, CPC trend formulas, Smart Bidding minimums, scaling cap) live in `google_ads/tool-fundamentals` and auto-load with this skill. Do NOT redefine them here. This skill is the workflow: classify queries → diagnose auction pressure → decide action.

## Data Requirements

Pull these using `google_ads_run_gaql`:

1. **Campaign auction metrics**: `metrics.search_impression_share`, `metrics.search_rank_lost_impression_share`, `metrics.search_budget_lost_impression_share`, `metrics.search_top_impression_percentage`, `metrics.search_absolute_top_impression_percentage`, `metrics.average_cpc`, `metrics.cost_micros`, `metrics.conversions`, `metrics.conversions_value`, `metrics.clicks`, `metrics.impressions`. Filter: `campaign.advertising_channel_type = 'SEARCH'`, `LAST_30_DAYS`, `campaign.status = 'ENABLED'`.
2. **Search terms**: `search_term_view.search_term`, impressions, clicks, cost, conversions, conversion_value. Sort by cost DESC, limit 200.
3. **Keyword-level auction**: keyword text, match type, keyword IS, IS Lost (Rank), avg CPC, conversions, cost from `keyword_view`. Sort by cost DESC, limit 200.
4. **CPC trend**: avg CPC for current 7 days vs prior 7 days (two queries with different `DURING` clauses; compute WoW delta locally per `tool-fundamentals → CPC trend WoW`).

Ask user for **target CPA** (or target ROAS for ecommerce). Default: use historical 30-day average.

---

## Step 1: Query Classification (Q1–Q5)

Classify each search term by performance:

| Tier | Name | Condition |
|------|------|-----------|
| **Q1** | Profitable | Conversions ≥ 2, OR CPA ≤ target, OR ROAS ≥ target |
| **Q2** | Promising | Conversions = 0 AND cost < 0.5× target CPA AND no Q5 signals |
| **Q3** | Unproven | Conversions = 0 AND cost between 0.5×–1× target CPA |
| **Q4** | Losing | Cost ≥ 1× target CPA with 0 conversions, OR CPA ≥ 1.5× target, OR ROAS ≤ 0.7× target |
| **Q5** | Invalid | Query contains: free, cheap, diy, how to, job, salary, course, pdf, meaning, used, repair |

**Q5 terms are eliminated regardless of cost.** Calculate spend share per tier.

---

## Step 2: Auction Pressure Classification

### Rank Pressure

| Rank Pressure = HIGH | if ANY true |
|---------------------|-------------|
| IS Lost (Rank) ≥ 30% | |
| Search IS ≤ 50% AND IS Lost (Rank) > IS Lost (Budget) | |
| Top of Page Rate ≤ 60% on Q1 queries | |
| Absolute Top ≤ 20% on Q1 queries | |

| Rank Pressure = LOW | if ALL true |
|--------------------|-------------|
| IS Lost (Rank) ≤ 20% | |
| Top of Page Rate ≥ 70% | |
| Absolute Top ≥ 30% on Q1 queries | |

### Budget Pressure

| Budget Pressure = HIGH | if ALL true |
|-----------------------|-------------|
| IS Lost (Budget) ≥ 20% | |
| IS Lost (Budget) > IS Lost (Rank) | |
| CPA ≤ target CPA | |
| ≥ 60% of spend from Q1–Q3 | |

| Budget Pressure = LOW | if ANY true |
|----------------------|-------------|
| IS Lost (Budget) < 10% | |
| CPA > target CPA | |
| Q4 + Q5 spend ≥ 25% | |

---

## Step 3: Decision Matrix

### Primary Action Table

| Query Mix | Rank Pressure | Budget Pressure | Action |
|-----------|--------------|-----------------|--------|
| Q1-heavy | Low | High | Increase budget 10–20% |
| Q1-heavy | High | Low | Increase bids 5–10% OR improve ad relevance |
| Q1-heavy | High | High | Fix rank first, then budget |
| Q1-heavy | Low | Low | Hold — no changes needed |
| Q2–Q3 heavy | Low | High | Limited budget test |
| Q4+ present | High | Any | Cap or cut spend |
| Q5 present | Any | Any | Negate immediately |

### Metric-Specific Logic

**Search IS**: Low IS alone means nothing. Only act if Q1 share ≥ 50% AND IS Lost (Rank or Budget) explains it.

**IS Lost (Rank)**: If majority Q1, CPA ≤ target, Rank Pressure HIGH → increase bids 5–10% or improve ad relevance. If CPA > target → do NOT raise bids, instead tighten queries (promote Q1 to Exact, kill Q3/Q4 leakage).

**IS Lost (Budget)**: If CPA stable, Q1–Q3 share ≥ 60%, Budget Pressure HIGH → increase budget 10–20%. Otherwise fix queries first.

**Top/Absolute Top**: Use only on Q1 queries. If CVR at Top ≥ 1.15× rest → defend position. No CVR delta = ego tax, ignore.

---

## Step 4: CPC Inflation Diagnosis

When CPC is increasing (compare WoW per `tool-fundamentals → CPC trend WoW`), identify which case applies:

| Symptom | Root Cause | Action |
|---------|-----------|--------|
| CPC ↑ AND IS Lost (Rank) ↑ | Competition increased | Bid increase allowed ONLY if CPA ≤ target |
| CPC ↑ AND new Q4/Q5 terms appearing | Match type leakage | Add negatives, tighten match types |
| CPC ↑ AND CTR ↓ | Ad relevance degraded | Improve ad copy, NOT bids |

**Only Case 1 (competition) justifies bid increases.** Cases 2 and 3 require query or creative fixes.

---

## Step 5: Scaling Prerequisites

Scale ONLY if ALL true:
- Q1 queries isolated (Exact or tight Phrase match)
- CPA stable or improving over 14+ days
- IS Lost (Budget) ≥ 20%
- CPC WoW% increase < CVR WoW% increase (efficiency improving faster than costs)

If CPC rising faster than CVR → false scale signal. Do not increase budget.

Scaling step caps come from `tool-fundamentals → Scaling step cap` and `google-ads-guardrails`.

---

## Step 6: Competitor & Brand Logic

**Brand defense** (when brand CPC ↑, Absolute Top ↓, competitor overlap ↑):
- Raise bids only on exact-match brand terms
- Tighten match types on brand campaigns
- Add competitor terms as negatives in non-brand campaigns

**Competitor campaigns**: Default state is OFF. Enable only if CPA ≤ 1.2× target AND Rank Pressure = LOW. Otherwise pause.

---

## Prohibitions

- Never increase budget to fix low IS without classifying queries first
- Never increase bids with Q4/Q5 terms present
- Never chase Absolute Top without CVR proof
- Never let Broad match dominate auction signals
- Never increase bids AND budget simultaneously

## Weekly Execution Order (immutable)

1. Prune Q4/Q5 queries
2. Reclassify remaining queries
3. Recompute auction pressure
4. Make bid/budget moves
5. Fix ad relevance

---

## Next Steps

If changes need to be executed, read the `google-ads-search-execution` skill for tool parameters and implementation details.

Output must include: query mix breakdown with spend shares, pressure diagnosis with IS metrics, CPC trend analysis with root cause, recommended actions in execution order, expected 7-day impact.
