---
description: Allocate expenses by department and set spending guardrails
---

# Budget

Allocate the budget for "$ARGUMENTS". Break down the forecast into departmental budgets with spending limits, approval thresholds, and accountability.

## Prerequisites

Read `.metapowers/finance/$ARGUMENTS/03-forecast.md`. If this file does not exist, tell the user:

> Phase 3 (Forecast) has not been completed for "$ARGUMENTS". Run `/finance:forecast $ARGUMENTS` first, or use `--skip-checks` to bypass.

If `--skip-checks` is present in $ARGUMENTS, skip this check and log to `.metapowers/finance/$ARGUMENTS/skip-log.md`.

## Process

1. **Read context:**
   - Read `.metapowers/finance/$ARGUMENTS/02-plan.md` for strategic objectives
   - Read `.metapowers/finance/$ARGUMENTS/03-forecast.md` for expense projections

2. **Define budget structure:**
   - List all departments or cost centers
   - Categorize expenses: personnel, tools/software, marketing, infrastructure, professional services, other
   - Determine budget period (monthly, quarterly, annual)

3. **Allocate by department:**
   - For each department:
     - Personnel costs (headcount x compensation)
     - Non-personnel costs (tools, travel, contractors, etc.)
     - Growth investments vs maintenance spend
   - Ensure allocations sum to the forecast total
   - Identify which departments have the most budget flexibility

4. **Set guardrails:**
   - Define spending authority levels (who can approve what amounts)
   - Set variance thresholds that trigger review (e.g., >10% over budget)
   - Identify protected vs discretionary line items
   - Define the reallocation process

5. **Create accountability framework:**
   - Assign a budget owner to each department
   - Define reporting cadence (monthly actuals vs budget)
   - Set up variance explanation requirements

6. **Write the artifact** to `.metapowers/finance/$ARGUMENTS/04-budget.md` with sections:
   - **Budget Summary** — total budget by period, split by department
   - **Department Budgets** — detailed allocation per department
   - **Headcount Budget** — planned hires, timing, and cost
   - **Spending Guardrails** — authority levels, thresholds, protected items
   - **Accountability** — owners, reporting cadence, variance rules

## Output

The budget written to `.metapowers/finance/$ARGUMENTS/04-budget.md`. Present a summary highlighting:
- Total budget and department breakdown
- Largest budget categories
- Key guardrails and approval thresholds
- Headcount plan
