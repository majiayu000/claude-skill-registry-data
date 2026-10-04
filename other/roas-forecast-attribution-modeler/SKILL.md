---
name: roas-forecast-attribution-modeler
description: Build ROAS forecasting and attribution-model assumptions for Meta (Facebook/Instagram), Google Ads, TikTok Ads, YouTube Ads, Amazon Ads, Shopify Ads, and DSP/programmatic planning.
---

# Ads ROAS Forecast

## Purpose
Core mission:
- forecast scenario modeling, attribution sensitivity, budget recommendation

This skill is specialized for advertising workflows and should output actionable plans rather than generic advice.

## When To Trigger
Use this skill when the user asks for:
- ad execution guidance tied to business outcomes
- growth decisions involving revenue, roas, cpa, or budget efficiency
- platform-level actions for: Meta (Facebook/Instagram), Google Ads, TikTok Ads, YouTube Ads, Amazon Ads, Shopify Ads, DSP/programmatic
- this specific capability: forecast scenario modeling, attribution sensitivity, budget recommendation

High-signal keywords:
- ads, advertising, campaign, growth, revenue, profit
- roas, cpa, roi, budget, bidding, traffic, conversion, funnel
- meta, googleads, tiktokads, youtubeads, amazonads, shopifyads, dsp

## Input Contract
Required:
- forecast_target: roas, cpa, or revenue
- planning_horizon
- base_assumptions

Optional:
- attribution_window_options
- budget_scenarios
- seasonality_factors
- risk_tolerance

## Output Contract
1. Model Inputs
2. Scenario Outputs
3. Sensitivity Analysis
4. Attribution Impact Notes
5. Budget Recommendation

## Workflow
1. Normalize baseline metrics and assumptions.
2. Build base, upside, and downside scenarios.
3. Run sensitivity on conversion rate and CPC assumptions.
4. Compare attribution windows and expected deltas.
5. Recommend budget path with confidence bounds.

## Decision Rules
- If assumptions are uncertain, widen forecast intervals and reduce aggressiveness.
- If scenario spread is large, recommend phased budget release.
- If attribution window drives major variance, present dual-plan decisions.

## Platform Notes
Primary scope:
- Meta (Facebook/Instagram), Google Ads, TikTok Ads, YouTube Ads, Amazon Ads, Shopify Ads, DSP/programmatic

Platform behavior guidance:
- Keep recommendations channel-aware; do not collapse all channels into one generic plan.
- For Meta and TikTok Ads, prioritize creative testing cadence.
- For Google Ads and Amazon Ads, prioritize demand-capture and query/listing intent.
- For DSP/programmatic, prioritize audience control and frequency governance.

## Constraints And Guardrails
- Never fabricate metrics or policy outcomes.
- Separate observed facts from assumptions.
- Use measurable language for each proposed action.
- Include at least one rollback or stop-loss condition when spend risk exists.

## Failure Handling And Escalation
- If critical inputs are missing, ask for only the minimum required fields.
- If platform constraints conflict, show trade-offs and a safe default.
- If confidence is low, mark it explicitly and provide a validation checklist.
- If high-risk issues appear (policy, billing, tracking breakage), escalate with a structured handoff payload.

## Code Examples
### Forecast Input

    spend: 50000
    cpc: 1.2
    cvr: 0.035
    aov: 68

### Scenario Output

    base_roas: 2.6
    upside_roas: 3.1
    downside_roas: 2.1

## Examples
### Example 1: Budget planning with uncertainty
Input:
- Next month spend doubled
- Baseline CVR unstable

Output focus:
- base/upside/downside scenarios
- sensitivity drivers
- safe budget release plan

### Example 2: Attribution sensitivity
Input:
- 1d and 7d attribution produce different ROAS
- Need allocation decision

Output focus:
- attribution delta model
- decision thresholds
- channel-level impact

### Example 3: Seasonal forecast
Input:
- Holiday promotion planned
- Historical CPC volatility high

Output focus:
- seasonality adjustment assumptions
- risk-adjusted forecast range
- final recommendation

## Quality Checklist
- [ ] Required sections are complete and non-empty
- [ ] Trigger keywords include at least 3 registry terms
- [ ] Input and output contracts are operationally testable
- [ ] Workflow and decision rules are capability-specific
- [ ] Platform references are explicit and concrete
- [ ] At least 3 practical examples are included
