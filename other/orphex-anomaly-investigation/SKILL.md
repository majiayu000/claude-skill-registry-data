---
name: orphex-anomaly-investigation
description: "Investigate an unexpected spend, outcome, CPA, or ROAS shift; rank falsifiable causes without treating coincident changes as proof."
license: MIT
metadata:
  version: "2.0.1"
---

# Orphex Anomaly Investigation

Use this skill when someone asks why a marketing metric changed suddenly, whether it is an incident, or what to check first. Work from Orphex data when the connection below reaches it, and from supplied exports, diagnostics, change records, and documents. A change log shows timing, not causation or authority to change settings.

## With an Orphex connection

If an Orphex connector is available, check it before asking for exports. Run `capability_search` with platform `orphex` and limit 100; use a read only if that search returns its id, and ask which workspace to use when several are bound. Read `anomaly.read` (about one week retained; segment names carry the channel), `insights.read`, `alerts.read`, `workspace.brief` for data freshness, and `controller.catalog` then `controller.fetch` for the metric's numerator and denominator over the shift and a comparable prior window. Then list guides with `skill_catalog` (kind `guide`, topic `anomaly`) and follow a matching one through `skill_read`; choose by title, never by a stored id.

If a read is not returned, this connection cannot reach that Orphex data for the workspace: say so, then use the live platform reads it offers or the supplied exports. An absent, refused or empty read is not evidence of zero, none or healthy. Describe each read with `capability_describe` before `run_read`, keep `date_end` no later than yesterday, disclose request adjustments, and name each number's source, workspace and window. This skill's evidence rules still govern any guide, insight or playbook label, and no read authorizes account changes. Ask the user only for what is still missing.

## Establish whether the shift is comparable

Record metric and scope, timezone, dates, refresh time, currency, event and denominator, attribution model/window, and whether dates refer to interaction or conversion. Prefer equal-length periods with the same weekdays. Mark partial periods, unsettled conversions, holidays, promotions, or scope changes. Call immature results provisional and name a recheck point. Without a defensible baseline, describe the value without labeling it an anomaly.

Minimum evidence is the metric numerator and denominator, a named comparison period, and the source definition. Daily or campaign rows, delivery status, creative changes, and timestamped changes improve diagnosis. If evidence is still missing after the Orphex check, ask or leave the question unresolved; do not invent account facts.

A reporting date, previous/current labels, equal-length periods, or asserted maturity do not specify exact interval endpoints. Do not reconstruct dates or days exposed to a change from those facts. Without supplied dated rows, do not distribute aggregate outcomes uniformly across days, project a prior daily average onto pre-change days, or use such hypothetical counts to bound a change's possible effect. Keep timing unresolved and request actual period boundaries, the change timestamp, date basis, and daily rows.

Use the supplied values to calculate an absolute difference as current minus reference. Calculate relative change only when the reference is numeric and nonzero. If a baseline is zero, report the movement as “from 0 to N”; do not invent a percentage. Compute CPA as spend divided by the named conversions and ROAS as the consistently attributed revenue divided by spend. A zero or missing denominator makes the ratio unavailable. Recompute portfolio ratios from summed numerators and denominators; never average campaign CPA or ROAS. Component changes add only for the same additive metric and mutually exclusive components. Ratio movements do not have additive campaign contributions.

## Rank causes and test them

Check the metric and data path early; this is a verification sequence, not a causal prior. Missing tracking logs or import diagnostics mean measurement health is unknown, not that tracking is the leading cause. Neither an abrupt nor a gradual decline, nor a short zero-conversion period, identifies a tracking, bidding, or delivery cause by itself. Flat spend describes the CPA numerator only; it does not establish a budget cap, unchanged CPC or traffic, or a weak bid response. Request event diagnostics and reconciliation alongside dated delivery and change records. Prioritize tracking or delivery remediation when actual diagnostics support a concrete failure; otherwise keep explanations as hypotheses with checks that could falsify them.

Compare delivery, pacing, campaign mix, creative, audience/placement, landing or offer changes, seasonality, and conversion lag. Rank causal hypotheses only when supplied evidence supports their relative ranking; otherwise report unresolved alternatives with low confidence. Prioritize next checks separately by impact, diagnostic value, and test speed, and state whether the order is a checking sequence or an evidence-supported likelihood ranking. State the fact, possible explanation, contrary evidence, falsifiable check, and high/medium/low confidence. Avoid universal alert thresholds. Use a median and dispersion only with sufficient stable matched history, and name the sample size; otherwise keep the comparison descriptive.

Align change-log times to account timezone and event-time basis. A nearby change is a test lead, not causal proof. State what would disconfirm each hypothesis. Experiments or documented holdouts can support causal claims; observational exports support association only.

## Report

Lead with the shift and period maturity. Show current and reference values, absolute and valid relative change, denominator, period, and source. Then list ranked hypotheses, confidence, supporting/contrary evidence, and next checks. Name unresolved currency, timezone, attribution, freshness, or denominator issues. Execute a change only when a current or prior instruction explicitly authorizes the exact account scope and action, and an available write path permits it; otherwise provide a proposal.

Fictional boundary case: a dashboard shows 0 purchases for a partial Tuesday versus 2 the prior Tuesday, while conversions can arrive after the report refresh. Mark CPA unavailable for the current day and keep the finding provisional. A budget edit recorded Monday raises a testable hypothesis but does not establish the cause. Request a mature same-weekday export and the event diagnostic before escalating it as an outage.

## Official references

- [Google Ads conversion tracking status and troubleshooting](https://support.google.com/google-ads/answer/12674892?hl=en)
- [Google Analytics cross-channel conversion reporting](https://support.google.com/analytics/answer/16638051?hl=en)

## Portable inputs and examples

- Read [the input contract](references/input-contract.md) when mapping a new export or checking the example's scope and definitions. Copy [the header-only CSV template](assets/input-template.csv) when preparing data; equivalent supplied exports remain acceptable.
- Read [the reusable business context](references/business-context.md) only for business facts or constraints this task needs. Reuse user-supplied facts with their source/date; the template contains no default targets.
- Inspect [the complete fictional input](assets/example-input.csv) with [its example output](references/example-output.md) when learning the output and calculation boundaries. Never use fictional values for a real account.

State whether the result is complete, partial, or blocked for the requested decision. Link material findings to actual supplied rows/sources and separate observed metrics, hypotheses, and estimates. Lead with a short business conclusion, then evidence, uncertainty, and the next measurable check. A data export or installed skill does not authorize account changes.

For the supported arithmetic only, optionally run [the bundled calculator](scripts/marketing_math.py) with Python 3: `python3 scripts/marketing_math.py weighted-ratio < calculation.json`. Read its input mapping in the input contract before preparing JSON. It reads JSON, not CSV directly. If Python or the requested method is unavailable, show a reproducible alternative calculation or mark it unsupported; do not report an uncomputed result as verified.
