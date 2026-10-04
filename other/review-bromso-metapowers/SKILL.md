---
description: Monitor performance against budget, analyze variances, and reforecast
---

# Review

Review financial performance for "$ARGUMENTS". Compare actuals to budget, analyze variances, identify trends, and update the forecast based on new information.

## Prerequisites

Read `.metapowers/finance/$ARGUMENTS/05-model.md`. If this file does not exist, tell the user:

> Phase 5 (Model) has not been completed for "$ARGUMENTS". Run `/finance:model $ARGUMENTS` first, or use `--skip-checks` to bypass.

If `--skip-checks` is present in $ARGUMENTS, skip this check and log to `.metapowers/finance/$ARGUMENTS/skip-log.md`.

## Process

1. **Read context:**
   - Read `.metapowers/finance/$ARGUMENTS/02-plan.md` for KPI targets
   - Read `.metapowers/finance/$ARGUMENTS/03-forecast.md` for original projections
   - Read `.metapowers/finance/$ARGUMENTS/04-budget.md` for departmental budgets
   - Read `.metapowers/finance/$ARGUMENTS/05-model.md` for scenario benchmarks

2. **Collect actuals:**
   - Ask the user for actual financial results for the review period
   - Revenue actuals by stream
   - Expense actuals by department and category
   - Cash position and cash flow actuals
   - Headcount actuals

3. **Variance analysis:**
   - Calculate budget vs actual for each line item
   - Classify variances: favorable/unfavorable, timing/permanent, volume/price/mix
   - Identify the top 5 variances by dollar amount
   - Determine root causes for significant variances

4. **KPI scorecard:**
   - Update each KPI with actual values
   - Show trend (improving, stable, declining)
   - Flag any KPIs at risk of missing annual target

5. **Reforecast:**
   - Based on actuals and trends, update the remaining forecast
   - Adjust assumptions that have proven incorrect
   - Recalculate runway and break-even timing
   - Recommend budget reallocations if needed

6. **Write the artifact** to `.metapowers/finance/$ARGUMENTS/06-review.md` with sections:
   - **Period Summary** — review period and key headlines
   - **Variance Analysis** — budget vs actual with explanations
   - **KPI Scorecard** — target vs actual vs trend
   - **Reforecast** — updated projections for remaining periods
   - **Recommendations** — actions to take based on findings
   - **Risks and Watch Items** — emerging issues to monitor

## Output

The review written to `.metapowers/finance/$ARGUMENTS/06-review.md`. Present a summary highlighting:
- Performance vs budget (on track, ahead, behind)
- Largest variances and root causes
- Updated runway and key metric trajectory
- Recommended actions
