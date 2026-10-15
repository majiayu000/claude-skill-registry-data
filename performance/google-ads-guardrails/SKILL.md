---
name: google-ads-guardrails
description: "Guardrails for Google Ads recommendations and mutations. Hard rules on what NOT to recommend, prohibited phrasing, data-quality requirements. Used internally for any Google Ads optimization or change recommendation."
metadata:
  source: "prompts/skills/google_ads/guardrails"
---

# Google Ads Guardrails

**READ BEFORE GENERATING ANY RECOMMENDATION.**

## Budget Reallocation Prohibition

You CANNOT allocate, shift, increase, reduce, or "optimize" budget for: keywords, search terms, match types, devices (unless bid adjustments in Search), locations (unless bid adjustments or exclusions), audiences (unless bid modifiers), asset groups (PMax has no asset-group budgets).

**Before writing ANY recommendation, ask:** Does this imply moving money between keywords, queries, products, devices, audiences, or asset groups? If YES → rewrite using valid controls below.

## Valid Budget Controls

| Campaign Type | Valid Controls |
|--------------|---------------|
| Search / Shopping | Campaign daily budget, bid strategy targets (tCPA/tROAS/max CPC), pause/enable campaigns or ad groups |
| Performance Max | Campaign daily budget, bid strategy targets (tCPA/tROAS), pause asset groups or campaign |

If a recommendation does not map to one of these controls, it is not actionable.

## Mandatory Rewrites

❌ "Shift budget from keyword A to keyword B"
✅ "Pause keyword A. Increase campaign daily budget by 10–20% to allow keyword B more eligible demand."

❌ "Allocate more to [breakdown: placement/device/demographic/product/asset group]"
✅ "Create a new campaign targeting [dimension] with its own budget, OR use bid adjustments/exclusions."

**Rule**: Any recommendation implying budget movement between sub-campaign entities must be rewritten to use campaign budget, bid targets, pause/enable, or structural separation.

## Metric Selection

First infer conversion type:
- **Ecommerce**: Use ROAS, conversion value, cost per purchase. Never use CPA alone for revenue decisions.
- **Lead gen**: Use CPA, cost per lead. Never use ROAS unless offline revenue is imported.
- **Unclear**: ASK the user. Do not assume.

## Scaling Limits

- Max budget increase: **20% at a time**
- Never scale if: CPA > target, ROAS < target, or query/search term hygiene not done
- Never scale based on: Impression Share alone, CPC alone, or early data (< 7 days)
- Frame scaling as: "Incremental test with downside risk"

## Learning & Stability

- Do not stack changes (budget + bids + structure simultaneously)
- Do not judge performance on: < 30 conversions (Search), < 50 conversions (PMax/Shopping)
- Avoid changes that reset learning unless absolutely required

## Immediate STOP Triggers

Halt any recommendation that attempts:
- "Scale keywords / products / asset groups"
- "Reallocate spend between queries"
- "Optimize placements in PMax"
- "Increase bids and budget at the same time"
- "Scale > 20% in one step"
- "Fix low IS by increasing budget blindly"

## Required Diagnostics Before Any Action

Before any scale/pause/restructure suggestion, check:
1. Search term quality (Q4/Q5 presence)
2. CPA/ROAS vs target
3. IS Lost (Rank vs Budget breakdown)
4. CPC trend direction
5. Conversion volume sufficiency
6. Bidding strategy compatibility

If diagnostics are incomplete → say **insufficient data**, do not recommend.
