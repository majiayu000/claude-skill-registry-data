---
name: orphex-customer-cohort-ltv-review
description: "Compare acquired-customer cohorts at a common observed horizon using defined revenue, retention, and CAC; separate observed value from lifetime forecasts."
license: MIT
metadata:
  version: "2.0.1"
---

# Orphex Customer Cohort & LTV Review

Review customer cohort value, repeat behavior and acquisition economics at a common observed horizon. A skill title containing LTV does not make a finite observation a lifetime estimate.

## With an Orphex connection

If an Orphex connector is available, check it before asking for exports. Run `capability_search` with platform `orphex` and limit 100; use a read only if that search returns its id, and ask which workspace to use when several are bound. Read `business_outcomes.mmp_cohort_campaign_read` for install-cohort revenue, purchases and events at d0, w0 and m0, and `controller.catalog` then `controller.fetch` at level `campaign` for matching cost. Then list guides with `skill_catalog` (kind `guide`, topic `subscription`) and follow a matching one through `skill_read`; choose by title, never by a stored id.

If a read is not returned, this connection cannot reach that Orphex data for the workspace: say so, then use the live platform reads it offers or the supplied exports. An absent, refused or empty read is not evidence of zero, none or healthy. Describe each read with `capability_describe` before `run_read`, keep `date_end` no later than yesterday, disclose request adjustments, and name each number's source, workspace and window. This skill's evidence rules still govern any guide, insight or playbook label, and no read authorizes account changes. Ask the user only for what is still missing.

## Align cohorts before comparing

Define new/acquired customer membership, acquisition date, attribution and cost allocation, unique identity rules, product/business model, currency, revenue/cost basis, snapshot, and per-customer follow-up. Use the same elapsed horizon from acquisition for every eligible customer; a monthly cohort's average age or earliest member age cannot certify maturity for the whole cohort. Exclude right-censored periods from an equal-horizon comparison or disclose a valid censoring-adjusted method rather than extrapolating automatically.

Net/gross revenue, collected cash, recognized revenue, ARR and contribution are different numerators. For SaaS, a booked annual contract or ARR is not observed recognized cash over 60 days. Define repeat purchasers, active/subscription retention, renewals or churn against the original eligible denominator; do not mix transaction count with unique repeat customers. For repeat metrics, preserve customers with zero subsequent activity when still observable. Consent/deletion or identity gaps are missingness limits, not churn evidence.

## Calculate supported value

Observed horizon value per acquired customer = matching cohort value / unique acquired customers. CAC = scoped acquisition cost / those customers. Aggregate from sums, preserve currencies, and avoid zero-denominator ratios. Label revenue-to-CAC separately from contribution-to-CAC; neither is company ROI without the full cost definition. Payback requires cumulative contribution/cash by elapsed time; it cannot be inferred from a revenue multiple alone.

A lifetime forecast needs an explicitly supplied/validated retention or survival model, horizon, cost path, discounting assumptions when applicable, calibration and uncertainty. Do not invent a retention multiplier, claim a younger cohort's ultimate value, or bid to a forecast from these aggregates. Use the optional calculator only for common-horizon arithmetic, not survival modeling.

Deliver observed horizon coverage, weighted value/CAC/repeat metrics, economic definition, uncertainty and a next cohort check. Acquisition attribution is not causal lift; budget or bidding changes remain bounded proposals.

## Portable inputs and examples

- Read [the input contract](references/input-contract.md) when mapping a new export or checking the example's scope and definitions. Copy [the header-only CSV template](assets/input-template.csv) when preparing data; equivalent supplied exports remain acceptable.
- Read [the reusable business context](references/business-context.md) only for business facts or constraints this task needs. Reuse user-supplied facts with their source/date; the template contains no default targets.
- Inspect [the complete fictional input](assets/example-input.csv) with [its example output](references/example-output.md) when learning the output and calculation boundaries. Never use fictional values for a real account.

State whether the result is complete, partial, or blocked for the requested decision. Link material findings to actual supplied rows/sources and separate observed metrics, hypotheses, and estimates. Lead with a short business conclusion, then evidence, uncertainty, and the next measurable check. A data export or installed skill does not authorize account changes.

For the supported arithmetic only, optionally run [the bundled calculator](scripts/marketing_math.py) with Python 3: `python3 scripts/marketing_math.py cohort < calculation.json`. Read its input mapping in the input contract before preparing JSON. It reads JSON, not CSV directly. If Python or the requested method is unavailable, show a reproducible alternative calculation or mark it unsupported; do not report an uncomputed result as verified.
