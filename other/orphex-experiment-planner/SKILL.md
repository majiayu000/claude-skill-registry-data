---
name: orphex-experiment-planner
description: "Design a bounded marketing or conversion experiment with a supplied meaningful effect, feasible traffic, guardrails, and a predeclared decision rule."
license: MIT
metadata:
  version: "2.0.1"
---

# Orphex Experiment Planner

Turn a specific business uncertainty into a feasible experiment brief. Preserve the user's chosen scope and meaningful effect; do not add unrelated variants or guarantee a winner.

## With an Orphex connection

If an Orphex connector is available, check it before asking for exports. Run `capability_search` with platform `orphex` and limit 100; use a read only if that search returns its id, and ask which workspace to use when several are bound. Read `controller.catalog` then `controller.fetch` at the planned unit's level for baseline volume, conversion rate and day-to-day variation over a comparable recent window.

If a read is not returned, this connection cannot reach that Orphex data for the workspace: say so, then use the live platform reads it offers or the supplied exports. An absent, refused or empty read is not evidence of zero, none or healthy. Describe each read with `capability_describe` before `run_read`, keep `date_end` no later than yesterday, disclose request adjustments, and name each number's source, workspace and window. This skill's evidence rules still govern any guide, insight or playbook label, and no read authorizes account changes. Ask the user only for what is still missing.

## Define the estimand and design

State the one change, hypothesis, eligible population, unit of randomization, control/treatment, primary outcome numerator and denominator, attribution/follow-up, and the smallest effect worth acting on. Separate a relative lift from percentage points. Specify consistent assignment, contamination risk, excluded units, instrumentation checks, guardrails, and the analysis horizon before launch. An optimized creative delivery comparison is not randomized assignment; platform experiment types and supported campaign/goal combinations must be verified for the actual account.

Keep outcome follow-up, conversion maturation, reporting/import delay, and attribution model/lookback as separately named definitions. A supplied seven-day outcome or reporting lag does not establish a seven-day attribution window. Preserve the supplied label and leave an unsupplied attribution rule unknown; do not fill it with a platform default when writing the brief.

For a simple independent binary outcome with two equal arms, use the optional calculator for an approximate fixed-horizon sample estimate from baseline rate, target rate, alpha, and power supplied by the user. State assumptions and round enrollment upward. Do not use that calculation for revenue/CPA means, clustered geographies, repeated users, sequential monitoring, multiple variants, or heavy-tailed outcomes; use an appropriate documented method or report that feasibility remains unquantified. Baseline zero/one or missing traffic requires different evidence, not fabricated defaults.

For a baseline-sensitivity scenario, explicitly state whether the absolute effect, relative effect, or target rate is held fixed and recompute the sample requirement under that convention. A lower baseline does not universally increase required sample: both outcome variance and the distance to the specified target matter. Do not make a directional sample or power claim from a changed baseline alone, or silently switch effect conventions. Alternative meaningful-effect criteria require the user's approval before they replace the supplied decision question.

Compare required sample with actual eligible traffic after allocation and add outcome/reporting maturation. A business deadline is not evidence of sufficient power. If infeasible, present the tradeoff: more traffic/time, a different user-approved effect criterion, or a descriptive pilot. Do not weaken the criterion silently. Predeclare what happens for inconclusive, guardrail-failing, or invalid results, including stop conditions for operational faults and a rollback reference.

Distinguish an enrollment deadline from a fully mature result deadline. For a result deadline, subtract required outcome follow-up and reporting lag from the available calendar horizon before calculating traffic needed for enrollment. Derive a traffic requirement only when that remaining enrollment window is positive. If the result horizon is no longer than the required lag, increasing traffic cannot create a positive enrollment window for a new fully mature trial. Extend the result deadline, clarify that the deadline concerns enrollment only, or offer a clearly descriptive pilot; sample sufficiency alone does not establish deadline feasibility.

## Deliver a reviewable brief

Include hypothesis, assigned units, metric, guardrails, sample assumptions, dates/lag, exclusions, and the decision rule. Keep creation, edits, and rollout proposal-only without specific authorization. Check platform auto-apply settings rather than assuming a scheduled test cannot mutate campaigns.

## Official reference

- [Google custom experiment setup and split types](https://support.google.com/google-ads/answer/6261395?hl=en)

## Portable inputs and examples

- Read [the input contract](references/input-contract.md) when mapping a new export or checking the example's scope and definitions. Copy [the header-only CSV template](assets/input-template.csv) when preparing data; equivalent supplied exports remain acceptable.
- Read [the reusable business context](references/business-context.md) only for business facts or constraints this task needs. Reuse user-supplied facts with their source/date; the template contains no default targets.
- Inspect [the complete fictional input](assets/example-input.csv) with [its example output](references/example-output.md) when learning the output and calculation boundaries. Never use fictional values for a real account.

State whether the result is complete, partial, or blocked for the requested decision. Link material findings to actual supplied rows/sources and separate observed metrics, hypotheses, and estimates. Lead with a short business conclusion, then evidence, uncertainty, and the next measurable check. A data export or installed skill does not authorize account changes.

For the supported arithmetic only, optionally run [the bundled calculator](scripts/marketing_math.py) with Python 3: `python3 scripts/marketing_math.py experiment < calculation.json`. Read its input mapping in the input contract before preparing JSON. It reads JSON, not CSV directly. If Python or the requested method is unavailable, show a reproducible alternative calculation or mark it unsupported; do not report an uncomputed result as verified.
