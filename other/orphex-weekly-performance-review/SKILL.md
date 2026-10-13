---
name: orphex-weekly-performance-review
description: "Review marketing period changes and diagnose evidence-backed drivers from supplied comparable exports; use the summarizer for a short stakeholder update."
license: MIT
metadata:
  version: "2.0.1"
---

# Orphex Weekly Performance Review

Turn marketing exports and documents supplied by the user into a concise, decision-ready period review. Orphex MCP may be used when available and authorized, but is optional. Never imply that data was fetched or verified when the user supplied no source for it.

## With an Orphex connection

If an Orphex connector is available, check it before asking for exports. Run `capability_search` with platform `orphex` and limit 100; use a read only if that search returns its id, and ask which workspace to use when several are bound. Read `workflow.weekly_digest_read`, `scorecards.read`, `insights.read`, `anomaly.read`, and `controller.catalog` then `controller.fetch` with a comparison window for each numerator and denominator. Then list guides with `skill_catalog` (kind `guide`, topic `account_health`, then `cross_platform`) and follow a matching one through `skill_read`; choose by title, never by a stored id.

If a read is not returned, this connection cannot reach that Orphex data for the workspace: say so, then use the live platform reads it offers or the supplied exports. An absent, refused or empty read is not evidence of zero, none or healthy. Describe each read with `capability_describe` before `run_read`, keep `date_end` no later than yesterday, disclose request adjustments, and name each number's source, workspace and window. This skill's evidence rules still govern any guide, insight or playbook label, and no read authorizes account changes. Ask the user only for what is still missing.

## Make the comparison valid

Confirm the business question, reporting timezone, exact current and comparison dates, campaign scope, currency, conversion event, attribution model and window, and data refresh time. Prefer equal-length periods with the same weekday mix. For a week-over-week comparison, check for incomplete current days, holidays, promotion changes, and conversion lag. If the periods or definitions differ, explain the mismatch and qualify or withhold the comparison.

Keep the source and definitions attached to every metric. Distinguish spend from budget cap, clicks from landing visits, platform-attributed outcomes from CRM outcomes, and gross revenue from net revenue. Convert currencies only when an explicit rate and date are supplied; otherwise report currencies separately. Do not combine unlike account currencies into a single total.

Calculate only metrics whose inputs and definitions are present:

- CTR = clicks / impressions
- CPC = spend / clicks
- conversion rate = named conversions / a named denominator
- CPA = spend / named conversions
- ROAS = named revenue / spend

Show counts with rates and specify the denominator. Mark a ratio unavailable when its denominator is zero, missing, or ambiguous. Report both absolute and relative movement where valid; do not express percentage change from a zero or missing baseline. Reconcile totals against the supplied source before explaining trends.

## Separate evidence from explanation

Explain the aggregate ratio using actual rows from the same named period. An unweighted row mean can coincide numerically with a total ratio in some data; that coincidence does not validate it for another period. Do not invent a zero-conversion-row example when none is needed to answer the supplied comparison. If zero rows are present, their CPA is undefined; retain their spend in total spend / total conversions instead of claiming that every row mean inherently drops it.

Describe campaign metric movements without claiming additive contributions to a portfolio CPA or ROAS change. Do not introduce an unrequested counterfactual or say that one campaign accounts for the entire ratio change while other rates or conversion/spend shares also move. If a decomposition is explicitly requested, label its constructed reference and assumptions, show every rate and mix component, and reconcile them to the actual prior-to-current change. A comparison against a synthetic reference is not the observed total change or a causal effect.

Describe the largest movements first, ranked by business impact and confidence. Tie each observation to its period, scope, and source. A change in CPA or ROAS is not proof that a campaign edit caused the change. Separate observed movement, plausible drivers, and tested causal evidence. Use experiments or documented holdouts for causal claims; if none are supplied, say what the data cannot establish.

Consider delivery, budget pacing, audience or channel mix, creative rotation, landing-page changes, offer, seasonality, attribution lag, and measurement changes only when the supplied evidence supports them. Treat unexplained movement as a question to investigate, not a finding. Distinguish the average performance of existing spend from the likely marginal result of additional spend.

End with a small set of prioritized actions. Each action should name an owner or decision when supplied, the evidence behind it, a next measurement, and a check-in period that accounts for conversion lag. Do not invent thresholds or make platform changes.

## Recommended output

Start with the decision or headline. State the scope and comparability limits, then use a table for period values, absolute and relative movement, and source. Follow with observed campaign movements, uncertainties, and prioritized next actions. Use a causal explanation only when supported by the supplied evidence.

Before emitting any answer, audit the headline, every explanatory paragraph and the structured output together. Remove phrases such as "the whole deterioration", "the entire ratio change" or "would have produced" when no explicit, fully reconciled decomposition was requested. Report the actual campaign spend, conversion and CPA movements instead. A correct aggregate calculation or a caveat elsewhere does not repair a contradictory attribution in the headline or body.
## Portable inputs and examples

Describe portfolio CPA as total spend divided by total matching conversions, not as a spend-weighted mean of campaign CPAs. When every individual CPA is defined, a CPA mean weighted by matching conversion counts can be equivalent; spending weights are not that method. Use the direct summed ratio so spend from zero-conversion rows is retained rather than silently dropped. Name the numerator and denominator in the output instead of prescribing an ambiguous weighting label.

When explaining a weighting error with source figures, use counts from the same named period; do not pair a current-period count with a prior-period count as though they described one comparison. A row with no defined CPA makes a row-CPA mean undefined unless a handling rule is specified. Dropping that row is one invalid workaround, not an inherent property of every mean; retain its spend in the direct aggregate ratio.

Use observed spend terminology for spend rows. Neither unchanged spend nor a spend increase establishes a flat configured budget or a budget increase; do not promote an observed metric into a setting or change-history fact. A budget log can establish whether an edit occurred and its scope and timestamp, but it does not by itself establish its causal contribution to the performance movement. Keep that effect unresolved without justified causal evidence.

A reporting date, previous/current labels, equal-duration periods, or asserted maturity do not establish exact period endpoints. Do not turn the report date into a week-ending date or reconstruct an interval unless the source explicitly supplies it. Before presenting the review, check every date, budget-setting statement, and causal assertion against an actual supplied field or diagnostic; remove unsupported details or leave them unknown while preserving the available arithmetic.

- Read [the input contract](references/input-contract.md) when mapping a new export or checking the example's scope and definitions. Copy [the header-only CSV template](assets/input-template.csv) when preparing data; equivalent supplied exports remain acceptable.
- Read [the reusable business context](references/business-context.md) only for business facts or constraints this task needs. Reuse user-supplied facts with their source/date; the template contains no default targets.
- Inspect [the complete fictional input](assets/example-input.csv) with [its example output](references/example-output.md) when learning the output and calculation boundaries. Never use fictional values for a real account.

State whether the result is complete, partial, or blocked for the requested decision. Link material findings to actual supplied rows/sources and separate observed metrics, hypotheses, and estimates. Lead with a short business conclusion, then evidence, uncertainty, and the next measurable check. A data export or installed skill does not authorize account changes.

For the supported arithmetic only, optionally run [the bundled calculator](scripts/marketing_math.py) with Python 3: `python3 scripts/marketing_math.py weighted-ratio < calculation.json`. Read its input mapping in the input contract before preparing JSON. It reads JSON, not CSV directly. If Python or the requested method is unavailable, show a reproducible alternative calculation or mark it unsupported; do not report an uncomputed result as verified.
