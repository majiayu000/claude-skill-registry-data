---
name: orphex-weekly-performance-summarizer
description: "Write a brief stakeholder update from supplied weekly results, preserving weighted totals and caveats; use the performance review for deeper diagnosis."
license: MIT
metadata:
  version: "2.0.1"
---

# Orphex Weekly Performance Summarizer

Separate diagnostic priority from causal likelihood. Aggregate weekly totals without discriminating campaign, delivery, or event diagnostics do not establish a most likely explanation, including a campaign-mix shift. Keep unsupported alternatives unranked and causal confidence unresolved. You may prioritize a next check by diagnostic value and feasibility, but label that as a checking order rather than a probability ranking throughout the native answer, including the headline and explanatory text.

Use this skill when someone needs a short weekly or period update for a stakeholder, team meeting, or decision brief. It turns supplied reports into a clear narrative, not a full diagnostic review. Optional Orphex MCP reads may be used within the user's authorized scope. Never imply that the account was checked when the only evidence is user-provided.

## With an Orphex connection

If an Orphex connector is available, check it before asking for exports. Run `capability_search` with platform `orphex` and limit 100; use a read only if that search returns its id, and ask which workspace to use when several are bound. Read `workflow.weekly_digest_read`, `scorecards.read`, and `controller.catalog` then `controller.fetch` with a comparison window for the totals the update quotes. Then list guides with `skill_catalog` (kind `guide`, topic `account_health`) and follow a matching one through `skill_read`; choose by title, never by a stored id.

If a read is not returned, this connection cannot reach that Orphex data for the workspace: say so, then use the live platform reads it offers or the supplied exports. An absent, refused or empty read is not evidence of zero, none or healthy. Describe each read with `capability_describe` before `run_read`, keep `date_end` no later than yesterday, disclose request adjustments, and name each number's source, workspace and window. This skill's evidence rules still govern any guide, insight or playbook label, and no read authorizes account changes. Ask the user only for what is still missing.

## Confirm scope and maturity

Record the business objective, included accounts and channels, current and comparison dates, timezone, refresh time, currency, conversion event and denominator, attribution model/window, and whether dates mean ad interaction or conversion. Prefer equal-length periods with the same weekday mix. If the current week is partial, label it partial and compare equal elapsed days only when their weekday mix is comparable. If conversion lag or reporting delay is material, call results preliminary and name the recheck date. With no sound comparison period, write a current-state update rather than inventing a trend.

Minimum input is a named reporting period, a source, and at least one objective-linked metric with its numerator and denominator. Campaign or channel detail, budget constraints, major promotion dates, and change records help explain movement. If reports mix currencies, show separate currency rows; convert only with a supplied exchange rate and date. If an input is missing, name it in one caveat and keep the summary useful with the evidence that exists.

## Calculate the story accurately

For additive measures such as spend, impressions, clicks, or distinct event counts, sum only non-overlapping rows with aligned scope. Do not sum the same attributed conversion claimed by multiple platforms into a cross-channel total. Recompute aggregate CTR, conversion rate, CPA, or ROAS from aligned total numerators and denominators; never average campaign rates. Label every conversion-rate denominator. Calculate absolute change as current minus prior. Relative change is `(current − prior) / prior` only when prior is numeric and nonzero. For a zero baseline, state “from 0 to N” and omit the percentage. Distinguish percentage points in a rate from percent change in the rate.

Explain only what the evidence supports. A spend increase alongside more conversions is a movement, not proof that spend caused the increase. Attribute additive contributions only across comparable, disjoint components and only for the same metric. Treat budget-change timestamps as context rather than causal proof. Use plain language for likely drivers and mark them as hypotheses when no experiment, holdout, or direct diagnostic establishes cause. Do not add an arbitrary alert threshold.

## Write the update

Lead with the business result in one sentence. Add a compact table with the few metrics that answer the stated question: current, previous, absolute or valid relative change, unit/denominator, period, and source. Include one to three prioritized next actions when evidence supports them; if evidence is thin, recommend one best next check instead of manufacturing a list. Each action should name an owner if supplied, the condition to monitor, and when to revisit after data matures. Label confidence as high, medium, or low based on source quality, comparability, and maturity. Adapt length to the user; a 300–500 word update is a useful default, not a fixed requirement.

Fictional boundary case: Monday–Wednesday is incomplete. Search spend is USD and Social spend is EUR; both platforms claim the same fictional purchases under different attribution windows. Do not publish a combined spend or conversion total, and do not claim a cross-channel cause. Report separate currency rows, label the period partial, and make one next action: rerun the same-scope comparison after the conversion window settles, with event definitions aligned.

## Official references

- [Google Analytics cross-channel conversion reporting](https://support.google.com/analytics/answer/16638051?hl=en)
- [Google Ads conversion tracking status, reporting latency, and attribution date](https://support.google.com/google-ads/answer/12674892?hl=en)

## Portable inputs and examples

Observed spend is not a configured budget. Rising or falling spend and unchanged outcome totals neither establish nor rule out a budget cut, another settings change, or its causal effect. Establish changes from the budget entity, type, effective timestamps, and change history; assess their effects with comparable delivery evidence and a justified counterfactual. Distinguish rejecting an unsupported causal claim from proving that the proposed cause was absent. When settings, history, or causal evidence are missing, keep the budget explanation unresolved rather than refuting it from spend direction.

A change log can resolve whether a configured edit occurred, not by itself whether that edit caused the outcome movement. Describe that as an occurrence check; causal attribution still requires supported delivery evidence and a justified comparison or counterfactual. Do not promise that obtaining a log alone will resolve the causal question.

A reporting date, previous/current labels, equal-duration periods, or asserted maturity do not establish exact period endpoints. Do not turn the report date into a week-ending date or reconstruct an interval unless the source explicitly supplies it. Before presenting the update, check every date, budget-setting statement, and causal assertion against an actual supplied field or diagnostic; remove unsupported details or leave them unknown while preserving the available arithmetic.

Period-to-period spend and outcome differences do not measure marginal or incremental contribution. Higher spend with flat outcomes does not establish that the added spend produced no purchases, was avoidable, or should be removed. Do not recommend a spending ceiling or a return to prior-period spend solely from those aggregate differences. Historical spend is not an authorized budget limit or a demonstrated performance-safe allocation. A numerical spending guardrail needs a supplied business constraint, applicable budget semantics and period, and clear proposal scope; otherwise recommend the next diagnostic check and leave the ceiling unresolved.

- Read [the input contract](references/input-contract.md) when mapping a new export or checking the example's scope and definitions. Copy [the header-only CSV template](assets/input-template.csv) when preparing data; equivalent supplied exports remain acceptable.
- Read [the reusable business context](references/business-context.md) only for business facts or constraints this task needs. Reuse user-supplied facts with their source/date; the template contains no default targets.
- Inspect [the complete fictional input](assets/example-input.csv) with [its example output](references/example-output.md) when learning the output and calculation boundaries. Never use fictional values for a real account.

State whether the result is complete, partial, or blocked for the requested decision. Link material findings to actual supplied rows/sources and separate observed metrics, hypotheses, and estimates. Lead with a short business conclusion, then evidence, uncertainty, and the next measurable check. A data export or installed skill does not authorize account changes.

For the supported arithmetic only, optionally run [the bundled calculator](scripts/marketing_math.py) with Python 3: `python3 scripts/marketing_math.py weighted-ratio < calculation.json`. Read its input mapping in the input contract before preparing JSON. It reads JSON, not CSV directly. If Python or the requested method is unavailable, show a reproducible alternative calculation or mark it unsupported; do not report an uncomputed result as verified.
