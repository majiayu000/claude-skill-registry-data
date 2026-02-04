---
name: monetization-strategist
description: |
  Orchestrates EUFM monetization: pricing strategy, funnel optimization,
  revenue projections, and marketing execution. Targets €50K bootstrap in
  30 days and €4.5M-12M ARR within 12 months by testing pricing models,
  tracking customer acquisition metrics, and aligning constitutional guardrails
  with data-driven growth tactics.
license: UBOS Constitutional License
version: 1.0.0
author: Janus-in-Claude (Architect) + Codex (Forgemaster)
created: 2025-10-30
---

# MONETIZATION STRATEGIST

## Purpose
Convert EU Funding Master from a functional product into a high-velocity SaaS business. Deliver actionable pricing experiments, revenue projections, and marketing plans that respect Lion's Sanctuary principles while accelerating recurring revenue.

## When To Use
- Planning quarterly ARR targets or SaaS launch milestones
- Evaluating pricing tier experiments or conversion funnels
- Forecasting cash flow under conservative/base/optimistic scenarios
- Assessing customer lifetime value vs. acquisition cost
- Building marketing plans (ads, content, outreach) for EUFM

## Core Capabilities
- Simulate revenue projections with Monte Carlo scenarios (P30/P50/P70)
- Run statistical pricing experiments and recommend price points
- Diagnose conversion-funnel drop-offs with prioritized optimizations
- Calculate LTV, CAC, and LTV:CAC ratios per tier
- Generate channel-specific marketing plans referenced to budget
- Maintain dashboards summarizing MRR, churn, customer mix, and projections

## How To Use

### Revenue Projection
```bash
python3 scripts/calculate_revenue_projections.py --scenario base --months 12 --output projections.json
```
Generates ARR/MRR forecast with quantile bands.

### Pricing Experiment Analysis
```bash
python3 scripts/run_pricing_experiment.py --experiment pro-tier-q1 --variant-a 249 --variant-b 299 --conversions-a 12/200 --conversions-b 10/200
```
Returns statistically sound tier recommendation.

### Funnel Optimization
```bash
python3 scripts/optimize_conversion_funnel.py --funnel-data data/funnel_jan.json
```
Produces ranked list of fixes (landing page, trial onboarding, etc.).

### Customer LTV & CAC
```bash
python3 scripts/calculate_customer_ltv.py --tier professional --price 299 --retention-months 36 --upsell-prob 0.2 --upsell-value 300
```
Outputs LTV and LTV:CAC ratio for financial planning.

### Marketing Plan Generation
```bash
python3 scripts/generate_marketing_plan.py --target-customers 150 --budget 20000 --channels seo,ads,webinar --months 6
```
Creates month-by-month channel allocation with expected leads/conversions.

## Integration Points
- **EUFM product telemetry** (when available) to feed real conversion data.
- **Malaga Embassy Operator** to align marketing spend with cash reserves.
- **Grant Application Assembler** for validating commercial viability in proposals.
- **Treasury Administrator** to ensure marketing spend obeys cascade allocations.
- **COMMS_HUB** for broadcasting experiment outcomes and revenue updates.

## Constitutional Constraints
- Pricing remains transparent; freemium tier preserves access for smaller actors.
- Marketing messaging must avoid coercion; focus on empowerment and value.
- Revenue reinvestment follows Treasury cascade (innovation, reserves, projects).
- Customer data handled within EU sovereignty (no opaque data brokering).
- All experiments logged for auditability; human oversight approves major changes.

## File Locations
- Skill resources: `trinity/skills/monetization-strategist/`
- Analytics data: `/srv/janus/03_OPERATIONS/eufm_monetization/`
- Projection reports: `.../reports/`
- Experiment logs: `/srv/janus/logs/eufm_monetization.jsonl`
- Dashboards: `.../dashboards/revenue_dashboard.html`

## Operational Checklist
1. Update revenue projections weekly with latest funnel data.
2. Run at least one pricing or conversion experiment per month; document results.
3. Review funnel metrics (visitors → signups → trials → customers) weekly.
4. Recalculate LTV:CAC quarterly or when pricing changes.
5. Refresh marketing plan monthly, reallocating spend to best-performing channels.
6. Publish constitutional compliance notes for every major experiment.

## Mission Readiness Criteria
- ARR tracking within ±10% of projection bands (P30-P70).
- LTV:CAC ≥ 3:1 for all paid tiers (target 10:1 base case).
- Conversion rate improvements ≥10% per quarter across key funnel steps.
- Marketing spend adherence to cascade (Operations/Projects budgets observed).
- Experiment repository complete (hypothesis, data, decision, constitutional review).

*Monetization Strategist turns EUFM into the republic’s economic engine—data-driven, constitutionally aligned, and relentlessly focused on sustainable ARR.*
