---
description: Project revenue, expenses, and cash flow over the planning horizon
---

# Forecast

Project the financial forecast for "$ARGUMENTS". Build a driver-based model that translates planning assumptions into monthly revenue, expense, and cash flow projections.

## Prerequisites

Read `.metapowers/finance/$ARGUMENTS/02-plan.md`. If this file does not exist, tell the user:

> Phase 2 (Plan) has not been completed for "$ARGUMENTS". Run `/finance:plan $ARGUMENTS` first, or use `--skip-checks` to bypass.

If `--skip-checks` is present in $ARGUMENTS, skip this check and log to `.metapowers/finance/$ARGUMENTS/skip-log.md`.

## Process

1. **Read context:**
   - Read `.metapowers/finance/$ARGUMENTS/01-assess.md` for baseline data
   - Read `.metapowers/finance/$ARGUMENTS/02-plan.md` for assumptions and KPI targets

2. **Build revenue forecast:**
   - Model each revenue stream separately
   - Apply growth assumptions (new customers, churn, expansion, pricing changes)
   - Account for seasonality and ramp periods
   - Calculate monthly and annual totals
   - Reference `financial-model-template.md` for revenue model structure

3. **Build expense forecast:**
   - Project fixed costs (rent, salaries, subscriptions)
   - Project variable costs tied to revenue drivers
   - Include planned headcount additions and timing
   - Account for one-time costs (equipment, setup, legal)

4. **Build cash flow forecast:**
   - Map revenue to cash collections (considering payment terms)
   - Map expenses to cash payments
   - Include capital expenditures and financing
   - Calculate monthly net cash flow and ending balance
   - Determine runway and break-even timing

5. **Validate against KPIs:**
   - Check if the forecast achieves the KPI targets from the plan
   - Identify gaps and what would need to change
   - Note dependencies and risks

6. **Write the artifact** to `.metapowers/finance/$ARGUMENTS/03-forecast.md` with sections:
   - **Revenue Forecast** — monthly projections by stream
   - **Expense Forecast** — monthly projections by category
   - **Cash Flow Forecast** — monthly cash in, cash out, net, balance
   - **Key Metrics Over Time** — MRR, gross margin, burn rate, runway
   - **KPI Achievement** — projected vs target values
   - **Forecast Risks** — key sensitivities and downside scenarios

## Output

The forecast written to `.metapowers/finance/$ARGUMENTS/03-forecast.md`. Present a summary highlighting:
- Revenue trajectory and growth rate
- Burn rate and runway
- Whether KPI targets are achievable
- Top forecast risks
