---
description: Define strategic financial objectives, KPIs, and planning assumptions
---

# Plan

Define the strategic financial plan for "$ARGUMENTS". Set objectives, choose KPIs, and document the assumptions that will drive the forecast and budget.

## Prerequisites

Read `.metapowers/finance/$ARGUMENTS/01-assess.md`. If this file does not exist, tell the user:

> Phase 1 (Assess) has not been completed for "$ARGUMENTS". Run `/finance:assess $ARGUMENTS` first, or use `--skip-checks` to bypass.

If `--skip-checks` is present in $ARGUMENTS, skip this check and log to `.metapowers/finance/$ARGUMENTS/skip-log.md`.

## Process

1. **Read context:**
   - Read `.metapowers/finance/$ARGUMENTS/01-assess.md` for baseline metrics and business profile

2. **Define strategic objectives:**
   - What is the planning horizon? (quarterly, annual, 3-year)
   - What are the top 3-5 financial goals? (growth rate, profitability, fundraise, break-even)
   - What business milestones are tied to these goals?
   - Are there external deadlines? (fundraise timeline, board commitments)

3. **Select KPIs:**
   - Choose 5-10 KPIs aligned with objectives
   - For each KPI: define the metric, target, current value, and measurement frequency
   - Categorize: growth, profitability, efficiency, liquidity
   - Identify leading vs lagging indicators

4. **Document planning assumptions:**
   - Revenue assumptions (growth rates, pricing, churn, expansion)
   - Cost assumptions (hiring plan, vendor costs, inflation)
   - Market assumptions (TAM, competitive dynamics, seasonality)
   - Capital assumptions (funding, debt, payment terms)
   - Flag which assumptions carry the most risk

5. **Write the artifact** to `.metapowers/finance/$ARGUMENTS/02-plan.md` with sections:
   - **Planning Horizon** — timeframe and context
   - **Strategic Objectives** — prioritized financial goals
   - **KPI Dashboard** — metrics, targets, current values
   - **Planning Assumptions** — all assumptions with risk ratings
   - **Milestones** — key dates and financial triggers

## Output

The plan written to `.metapowers/finance/$ARGUMENTS/02-plan.md`. Present a summary highlighting:
- Planning horizon and objectives
- Key KPIs and targets
- Highest-risk assumptions
