---
name: orphex-budget-pacing-forecast
description: "Compare actual spend with a supplied period budget and forecast transparent remaining-spend scenarios; use reallocation to move fixed campaign caps."
license: MIT
metadata:
  version: "2.0.1"
---

# Orphex Budget Pacing & Forecast

Assess whether observed spend is aligned with the supplied period plan and produce transparent remaining-spend scenarios. A budget cap, actual spend, and a forecast are distinct quantities.

## With an Orphex connection

If an Orphex connector is available, check it before asking for exports. Run `capability_search` with platform `orphex` and limit 100; use a read only if that search returns its id, and ask which workspace to use when several are bound. Read `scorecards.read` for actual, pace and forecast against targets, `workflow.weekly_digest_read`, and `controller.catalog` then `controller.fetch` at level `campaign` for daily spend and budget. If `playbook.catalog` lists the campaign pacing health playbook, run it with `playbook.run`. Then list guides with `skill_catalog` (kind `guide`, topic `pacing`) and follow a matching one through `skill_read`; choose by title, never by a stored id.

If a read is not returned, this connection cannot reach that Orphex data for the workspace: say so, then use the live platform reads it offers or the supplied exports. An absent, refused or empty read is not evidence of zero, none or healthy. Describe each read with `capability_describe` before `run_read`, keep `date_end` no later than yesterday, disclose request adjustments, and name each number's source, workspace and window. This skill's evidence rules still govern any guide, insight or playbook label, and no read authorizes account changes. Ask the user only for what is still missing.

## Reconcile the interval

Record period start/end, timezone, completed-day cutoff, data refresh, currency, spend source, flight/off days, authorized period budget, and unique budget ownership. Exclude partial current days unless modeled explicitly. Reconcile delayed reports before treating the gap as underdelivery. Count shared owners once; never add a parent budget and its children's governed caps. Keep currencies separate without a supplied exchange rate and date.

Calculate remaining budget = period budget − spend. For completed calendar days, linear reference spend = period budget × elapsed days / total days, and required future daily spend = remaining budget / remaining days. If the campaign has an uneven schedule, promotions, or specified daily weights, use that supplied planned curve instead and name it. At the final day, report actual variance; do not divide by zero remaining days. A negative remainder means the supplied budget is exceeded, not negative required delivery.

## Forecast bounded scenarios

Show a constant observed run-rate scenario only when its assumption is useful. Prefer supplied future spend bounds or a documented forecast model with dated input. Never describe scenario bounds as statistical confidence intervals. Do not extrapolate conversions from historical average CPA as guaranteed marginal output. Note cap/billing semantics, eligibility, conversion lag for outcome claims, and the absence of flight changes. Google average daily budgets can deliver unevenly; verify the account's actual budget type before translating pacing into caps.

Report period/refresh, spend and planned reference, remaining amount, scenario arithmetic, assumptions, and a next completed-day check. Propose a change only with unambiguous entity, unit, scope, dates, and authorization; do not silently reduce budgets or move funds.

## Official reference

- [Google average daily budget semantics](https://support.google.com/google-ads/answer/6385083?hl=en)

## Portable inputs and examples

- Read [the input contract](references/input-contract.md) when mapping a new export or checking the example's scope and definitions. Copy [the header-only CSV template](assets/input-template.csv) when preparing data; equivalent supplied exports remain acceptable.
- Read [the reusable business context](references/business-context.md) only for business facts or constraints this task needs. Reuse user-supplied facts with their source/date; the template contains no default targets.
- Inspect [the complete fictional input](assets/example-input.csv) with [its example output](references/example-output.md) when learning the output and calculation boundaries. Never use fictional values for a real account.

State whether the result is complete, partial, or blocked for the requested decision. Link material findings to actual supplied rows/sources and separate observed metrics, hypotheses, and estimates. Lead with a short business conclusion, then evidence, uncertainty, and the next measurable check. A data export or installed skill does not authorize account changes.

For the supported arithmetic only, optionally run [the bundled calculator](scripts/marketing_math.py) with Python 3: `python3 scripts/marketing_math.py pacing < calculation.json`. Read its input mapping in the input contract before preparing JSON. It reads JSON, not CSV directly. If Python or the requested method is unavailable, show a reproducible alternative calculation or mark it unsupported; do not report an uncomputed result as verified.
