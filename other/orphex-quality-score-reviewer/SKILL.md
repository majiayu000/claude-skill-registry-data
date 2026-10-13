---
name: orphex-quality-score-reviewer
description: "Prioritize Search Quality Score component checks by business exposure; treat the score as a keyword diagnostic."
license: MIT
metadata:
  version: "2.0.1"
---

# Orphex Quality Score Reviewer

Use this skill when asked to diagnose Search keyword Quality Score (QS), explain component patterns, or prioritize ad-group follow-up. QS is a keyword-level diagnostic, not a campaign outcome. Work from supplied exports and documents; an already-authorized read-only source is optional. Do not treat the review as permission to edit ads, keywords, or landing pages.

## With an Orphex connection

If an Orphex connector is available, check it before asking for exports. Run `capability_search` with platform `orphex` and limit 100; use a read only if that search returns its id, and ask which workspace to use when several are bound. Read `controller.catalog` then `controller.fetch` at level `keyword` for Quality Score, its components, cost and outcomes. If `playbook.catalog` lists the quality score repair playbook, run it with `playbook.run`.

If a read is not returned, this connection cannot reach that Orphex data for the workspace: say so, then use the live platform reads it offers or the supplied exports. An absent, refused or empty read is not evidence of zero, none or healthy. Describe each read with `capability_describe` before `run_read`, keep `date_end` no later than yesterday, disclose request adjustments, and name each number's source, workspace and window. This skill's evidence rules still govern any guide, insight or playbook label, and no read authorizes account changes. Ask the user only for what is still missing.

## Gather comparable evidence

Request keyword ID/text, campaign and ad-group IDs, match type, current and historical QS, the three component statuses, date or segment, impressions, clicks, cost, conversions/value, status, final URL, and relevant query or ad evidence. Ask for account timezone, currency, conversion action and attribution window. Include the current and historical period separately because the score and its statuses are benchmark diagnostics, while performance rows may cover a different date range. Historical QS components are evaluated against other advertisers whose ads showed for the exact same search over the preceding 90 days; do not imply that a 7-day performance export measures the same window. See [Google's Quality Score guide](https://support.google.com/google-ads/answer/6167118?hl=en).

If QS is shown as a dash, missing, or absent, record it as “not available / insufficient evidence,” never zero or poor. Do not fill missing component status from the numerical score. If keyword-level data or the period is absent, explain the limit and request it rather than inferring ad-group QS.

## Read components without turning them into a KPI

Keep expected CTR, ad relevance, and landing-page experience as separate status fields. The score runs from 1–10 at the keyword level; Google describes it as diagnostic, says it is not a KPI to aggregate, and says it is not an input in the ad auction. Do not average QS across keywords, add it to performance, set a target score, or promise that raising it will lower CPC or improve rank.

Group rows only when a shared cause is plausible from supplied evidence: same ad group and query theme for ad relevance, shared final URL or page template for landing-page experience, or a coherent set of queries for expected CTR. Prioritize clusters by actual spend, eligible impressions, conversions/value, and the business goal, not by lowest score alone. Report raw counts beside rates and keep zero, missing, and lagged outcomes distinct. Low volume and unavailable components reduce confidence.

## Turn a status into a testable hypothesis

For below-average expected CTR, inspect the actual queries, audience/location/time segments, ad message and observed click-through rate; suggest checking message fit before changing bids. For below-average ad relevance, compare search intent with keyword grouping and the ads that could serve; propose a tighter theme or more relevant copy only when the rows support it. For below-average landing-page experience, compare the final URL and page evidence with the query and promised offer; request page speed, mobile, navigation, or content evidence when those facts are not in the export. A component status alone does not identify the cause.

For “Average” or “Above average,” do not claim the rest of the experience is strong: QS does not capture every quality factor. Avoid treating device, location, time, or creative changes as causes without a controlled test or a documented before/after that addresses confounders. Separate observed facts, likely diagnostic explanations, and untested hypotheses.

## Recommended output

State scope, period, source, currency, outcome definition, and mismatched QS/performance windows. Provide an action-cluster table: component/status; affected keywords and IDs; representative queries/ad/page; spend, eligible impressions, clicks, conversions/value; evidence; hypothesis; proposed review or test; confidence; and what evidence would confirm it. Include unavailable rows explicitly. Link each statement to the source file and row or segment.

Fictional example: three keywords on one landing page show below-average landing-page experience; together they have $900 spend and four leads in a complete 30-day USD export. Their QS values differ, so do not report an average score. Recommend reviewing the shared page against the three query intents; the pattern supports a page-relevance hypothesis, not proof that the page caused lead cost.

Any later account edit requires explicit authorization for the account, exact keywords, and change. This skill authorizes analysis only.

## Portable inputs and examples

- Read [the input contract](references/input-contract.md) when mapping a new export or checking the example's scope and definitions. Copy [the header-only CSV template](assets/input-template.csv) when preparing data; equivalent supplied exports remain acceptable.
- Read [the reusable business context](references/business-context.md) only for business facts or constraints this task needs. Reuse user-supplied facts with their source/date; the template contains no default targets.
- Inspect [the complete fictional input](assets/example-input.csv) with [its example output](references/example-output.md) when learning the output and calculation boundaries. Never use fictional values for a real account.

State whether the result is complete, partial, or blocked for the requested decision. Link material findings to actual supplied rows/sources and separate observed metrics, hypotheses, and estimates. Lead with a short business conclusion, then evidence, uncertainty, and the next measurable check. A data export or installed skill does not authorize account changes.

For the supported arithmetic only, optionally run [the bundled calculator](scripts/marketing_math.py) with Python 3: `python3 scripts/marketing_math.py weighted-ratio < calculation.json`. Read its input mapping in the input contract before preparing JSON. It reads JSON, not CSV directly. If Python or the requested method is unavailable, show a reproducible alternative calculation or mark it unsupported; do not report an uncomputed result as verified.
