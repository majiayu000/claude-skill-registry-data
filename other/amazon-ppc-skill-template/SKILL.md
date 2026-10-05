---
name: amazon-example-ppc-skill
description: Replace this with a precise trigger description. State the Amazon PPC workflow, user intent, required data, and when Codex or Claude should use this skill.
---

# Amazon Example PPC Skill

## Purpose

Replace this with the operator job. A good purpose explains the decision the skill supports, the Amazon entities it reasons about, and the business outcome it protects or improves.

Examples:

- Find search terms ready for exact-match harvesting.
- Diagnose wasted spend without cutting strategic defense traffic.
- Build an inventory-aware PPC scaling plan.

## Required Inputs

Gather, derive, or mark unavailable:

- Marketplace, profile/account, currency, timezone, ASIN and campaign scope.
- Exact analysis window and comparison period.
- Relevant Amazon Ads reports and metrics.
- Retail readiness: inventory, Featured Offer / Buy Box, price, reviews, rating, delivery promise, listing status, and conversion.
- Unit economics or target thresholds when profitability matters.
- BSR, organic rank, total sales, and competitor context when rank or incrementality matters.
- Known changes: bids, budgets, placements, negatives, launches, pauses, listings, pricing, promotions, and inventory events.

## Data Schema

Document the minimum useful fields for this skill. Replace this placeholder with a concise schema, for example:

- Entity fields: ASIN, campaign ID, ad group ID, keyword ID, target ID, search term, match type, placement, state.
- Performance fields: spend, sales, orders, impressions, clicks, CTR, CPC, CVR, ACoS, ROAS.
- Retail fields: inventory, Featured Offer / Buy Box, price, reviews, rating, margin, BSR, total sales.
- Context fields: date window, comparison window, marketplace, currency, timezone, recent changes.

## Safety Gates

Before recommending execution, classify the case as `Actionable`, `Directional`, or `Non-actionable`.

Do not recommend bid, budget, placement, negative, pause, relaunch, or campaign-creation actions unless:

- The data is fresh enough for the decision.
- The entity has enough volume for the claim.
- The action is specific and reversible or clearly risk-assessed.
- Missing margin, inventory, Featured Offer / Buy Box, retail readiness, total sales, or BSR data does not materially change the recommendation.
- The recommendation includes monitoring or rollback criteria.

If connected to Rocketcart MCP or any live Amazon Ads execution layer, require explicit approval, preflight against live state, and readback after execution.

## Common Failure Modes

Replace or extend these with skill-specific blockers:

- Missing entity IDs but live write is requested.
- Same-day or stale data is treated as complete.
- Margin, inventory, Featured Offer / Buy Box, total sales, or BSR is missing but the output makes firm profitability or causality claims.
- A negative, pause, or budget cut would harm brand defense, own-ASIN defense, launch/rank support, or low-sample discovery.
- Action rows are vague and omit entity, evidence, current state, proposed state, risk, approval status, or monitoring.
- Rocketcart or other live-write tooling is available but no explicit approval, preflight, readback, or monitoring plan exists.

## Workflow

1. Establish scope, data coverage, freshness, and attribution caveats.
2. Segment the data by the relevant Amazon entities.
3. Apply evidence thresholds and retail-readiness gates.
4. Separate confirmed facts from hypotheses and missing data.
5. Produce action rows with confidence, risk, and approval status.
6. Define monitoring windows and success/failure criteria.

## Output Format

Return these sections unless the user asks for a shorter version:

1. **Data Coverage And Trust**: available data, missing data, date ranges, scope, attribution caveats, and confidence.
2. **Executive Summary**: the main decision, top opportunity or risk, and what to do first.
3. **Findings**: evidence grouped by ASIN, campaign, keyword, search term, target, placement, or other relevant entity.
4. **Recommended Actions**: action table with entity, action, reason, expected impact, risk, confidence, timing, and approval requirement.
5. **Watchlist**: items with promising or concerning signals that are not action-ready.
6. **Monitoring Plan**: metrics, windows, success criteria, failure criteria, and next response.

## Optional References

Move detailed formulas, examples, schemas, and long workflow variants into `references/` and link them here only when needed.

## Minimum Example And Eval

When turning this template into a production skill, add:

- `examples/<skill-name>/prompt.md`: realistic synthetic or anonymized prompt.
- `examples/<skill-name>/input-summary.md`: available fields, missing fields, assumptions, and scope.
- `examples/<skill-name>/expected-output-outline.md`: required sections and safety behavior.
- At least one relevant `evals/` or `stress-tests/` addition when the skill introduces a new safety, causality, or actionability risk.
