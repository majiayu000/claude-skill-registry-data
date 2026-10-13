---
name: orphex-campaign-budget-reallocator
description: "Prepare a balanced transfer between supplied campaign budgets while preserving a fixed total and all protected bounds; use budget pacing to forecast period spend."
license: MIT
metadata:
  version: "2.0.1"
---

# Orphex Campaign Budget Reallocator

Use this skill to reallocate a fixed marketing budget across campaigns while keeping the total unchanged. Every valid result must reconcile to the stated total and respect floors, ceilings, and protected allocations. Unlike a general budget-change proposal, this workflow explicitly balances transfers across the included campaigns.

## With an Orphex connection

If an Orphex connector is available, check it before asking for exports. Run `capability_search` with platform `orphex` and limit 100; use a read only if that search returns its id, and ask which workspace to use when several are bound. Read `controller.catalog` then `controller.fetch` at level `campaign` for spend, budget and outcomes, `scorecards.read`, and `causal.latest_summary` for any measured lift. If `playbook.catalog` lists the budget reallocation efficiency playbook, run it with `playbook.run`. Then list guides with `skill_catalog` (kind `guide`, topic `budget`) and follow a matching one through `skill_read`; choose by title, never by a stored id.

If a read is not returned, this connection cannot reach that Orphex data for the workspace: say so, then use the live platform reads it offers or the supplied exports. An absent, refused or empty read is not evidence of zero, none or healthy. Describe each read with `capability_describe` before `run_read`, keep `date_end` no later than yesterday, disclose request adjustments, and name each number's source, workspace and window. This skill's evidence rules still govern any guide, insight or playbook label, and no read authorizes account changes. Ask the user only for what is still missing.

## Confirm the budget and constraints

Record account/campaign scope, total, currency, budget unit and horizon, timezone, effective dates, and whether rows repeat a shared budget. Count each budget entity once; do not add a portfolio cap to the campaigns it governs. Keep currencies separate without a supplied exchange rate and date.

Minimum input is the fixed total, current allocation, and floors, ceilings, frozen amounts, or protected outcomes. Ranking also needs comparable spend, defined outcomes, attribution window, conversion lag, delivery status, and objective. Without marginal evidence, label a transfer a hypothesis and omit an impact forecast.

Use a common unit throughout. Check that the current allocations sum to the fixed total. If not, show the discrepancy and ask whether the total or source rows are authoritative. Compute movable capacity as current allocation minus floor; compute headroom as ceiling minus current allocation. A plan is infeasible if the floors sum above the total, the ceilings sum below it, any floor exceeds its ceiling, or frozen allocations leave insufficient movable capacity. Do not relax constraints silently.

## Build a balanced proposal

Use the allocation unit for every delta. Show current, delta, proposed value, bounds, and evidence per unique budget-owning entity, listing its affected campaigns. Never allocate independently to campaigns whose cap is the same shared budget. Require `proposed = current + delta`, `sum(deltas) = 0`, and proposed total equal to fixed total. Keep protected campaigns unchanged. Prefer observed marginal efficiency or a supplied response curve; average CPA/ROAS describes past spend, not the next dollar.

Treat supplied allocation weights, target shares, and requested transfers as planning preferences. They may determine a feasible allocation under the stated constraints, but they do not establish relative efficiency, marginal returns, or expected improvement. Report arithmetic feasibility separately from evidence supporting the transfer direction. A preference can justify a planning choice; it cannot substitute for performance or marginal-response evidence. Do not request allocation weights as a way to upgrade an optimization hypothesis into an evidence-supported performance recommendation.

For currency budgets, calculate in minor units and show rounding reconciliation. Assign any remainder only within an eligible campaign’s bounds and name the rule. A cap is not a spend forecast. Check the platform’s budget type, pacing, and campaign eligibility; these rules differ by platform. Google Ads average daily budgets may pace unevenly, and shared budgets have campaign-type constraints.

Estimate outcomes only from explicit marginal data or a user scenario. If using `incremental spend / marginal CPA`, label it an estimate and include event, lag, and range when assumptions vary. Do not infer incremental conversions from average CPA. Include a review point after lag, a stop condition, and the prior allocation for rollback when supplied.

## Approval boundary and output

Do not mutate budgets as an unrequested extension of analysis. Apply a reallocation only if a current or prior instruction authorizes the resulting changes for the specified account and campaigns, and the write path permits them. Confirm that values, unit, currency, effective time, and scope are unambiguous; ask only about missing details that affect the action. Without an authorized write path, deliver the proposal and state it was not applied.

Start with feasibility and the reconciled total. Then show the allocation table, evidence and uncertainty, expected-impact limits, review condition, and whether the output is proposal-only. Confidence reflects the quality of the marginal evidence, not a promise of delivery.

Fictional example: fixed daily cap is $1,000. Campaign A has a $650 floor, B a $250 floor, and C a $200 floor. Floors total $1,100, so no valid reallocation exists; stop and ask which constraint may change. In a separate feasible case, current caps of $600/$300/$100 become $650/$250/$100. Deltas are +$50/−$50/$0, the total remains $1,000, and all stated bounds hold. This arithmetic does not claim that actual spend or results will follow the caps; the plan remains a proposal.

## Official references

- [Google Ads average daily budgets](https://support.google.com/google-ads/answer/6385083)
- [Google Ads shared budgets](https://support.google.com/google-ads/answer/10487241?hl=en)
- [Google Ads campaign total budgets](https://support.google.com/google-ads/answer/15137812?hl=en)

## Portable inputs and examples

- Read [the input contract](references/input-contract.md) when mapping a new export or checking the example's scope and definitions. Copy [the header-only CSV template](assets/input-template.csv) when preparing data; equivalent supplied exports remain acceptable.
- Read [the reusable business context](references/business-context.md) only for business facts or constraints this task needs. Reuse user-supplied facts with their source/date; the template contains no default targets.
- Inspect [the complete fictional input](assets/example-input.csv) with [its example output](references/example-output.md) when learning the output and calculation boundaries. Never use fictional values for a real account.

State whether the result is complete, partial, or blocked for the requested decision. Link material findings to actual supplied rows/sources and separate observed metrics, hypotheses, and estimates. Lead with a short business conclusion, then evidence, uncertainty, and the next measurable check. A data export or installed skill does not authorize account changes.

For the supported arithmetic only, optionally run [the bundled calculator](scripts/marketing_math.py) with Python 3: `python3 scripts/marketing_math.py reallocate < calculation.json`. Read its input mapping in the input contract before preparing JSON. It reads JSON, not CSV directly. If Python or the requested method is unavailable, show a reproducible alternative calculation or mark it unsupported; do not report an uncomputed result as verified.
