---
name: google-ads-search-execution
description: "Use when making changes to Google Ads Search campaigns: tool parameters for bid adjustments, budget changes, negation, query isolation."
metadata:
  source: "prompts/skills/google_ads/search-execution"
---

# Google Ads Search — Execution Rules

Tool parameters and processes for implementing search campaign changes. Load this after completing analysis with `google-ads-search-analysis`.

## Bid Adjustments

**When to increase bids (5–10%)**:
- ALL must be true: majority Q1 queries, CPA ≤ target, Rank Pressure = HIGH

**Keyword-level bid change**: `google_ads_propose_update_adgroups` on the keyword's ad group, with a `keyword_changes` entry for the keyword and its new `cpc_bid_micros` = current bid × 1.05–1.10, **in account currency** (divide the GAQL micros value by 1,000,000; e.g. 1.5 for $1.50).

**Ad group-level bid change**: `google_ads_propose_update_adgroups` with the new `cpc_bid_micros` = current bid × 1.05–1.10, in account currency.

Dry-run first; apply only after the user approves.

## Budget Adjustments

**When to increase budget (10–20%)**:
- ALL must be true: CPA stable, Q1–Q3 spend share ≥ 60%, Budget Pressure = HIGH

Tool: `google_ads_propose_update_campaigns` with the new daily `budget_micros` = current budget × 1.10–1.20, **in account currency** (e.g. 50 for $50; divide the GAQL `amount_micros` by 1,000,000). Dry-run first; apply only after the user approves.

## Query Negation

**Immediate negation (Q5)**: free, cheap, diy, how to, job, salary, course, pdf, meaning, used, repair.

**Conditional negation (Q4)**: Cost ≥ 1× target CPA AND conversions = 0, OR CPA ≥ 1.5× target.

Action: Add terms to shared negative keyword list at campaign or account level.

## Query Isolation (Q1)

When Q1 queries are mixed with Q2–Q5 and CPA on Q1 is below target but overall CPA is above target:

1. Identify top Q1 queries sorted by conversions
2. Create new campaign or ad group for isolated Q1 terms
3. Add Q1 queries as **Exact match** keywords in the new structure
4. Add the same terms as **negatives** in the original campaigns to prevent overlap
5. Set budget independently for the isolated campaign
