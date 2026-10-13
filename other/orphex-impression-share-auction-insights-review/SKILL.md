---
name: orphex-impression-share-auction-insights-review
description: "Review Google Ads impression-share losses and Auction Insights overlap without conflating denominators or forecasting competitor spend and profit."
license: MIT
metadata:
  version: "2.0.1"
---

# Orphex Impression Share & Auction Insights Review

Use this skill when asked whether campaigns are missing eligible impressions, whether loss appears budget- or rank-related, or how visible competitors overlap in auctions. Analyze supplied Google Ads exports and documents; an already-authorized read-only source is optional. Treat these metrics as diagnostics of eligible auction participation, not a forecast of profitable demand or a reason to raise budget automatically.

## With an Orphex connection

If an Orphex connector is available, check it before asking for exports. Run `capability_search` with platform `orphex` and limit 100; use a read only if that search returns its id, and ask which workspace to use when several are bound. Read `controller.catalog` then `controller.fetch` at level `campaign` for search impression share and budget- and rank-lost share; Auction Insights is a live platform read. If `playbook.catalog` lists the lost-impression-share budget playbook, run it with `playbook.run`.

If a read is not returned, this connection cannot reach that Orphex data for the workspace: say so, then use the live platform reads it offers or the supplied exports. An absent, refused or empty read is not evidence of zero, none or healthy. Describe each read with `capability_describe` before `run_read`, keep `date_end` no later than yesterday, disclose request adjustments, and name each number's source, workspace and window. This skill's evidence rules still govern any guide, insight or playbook label, and no read authorizes account changes. Ask the user only for what is still missing.

## Confirm the comparison frame

Request campaign IDs/types, network, reporting dates/timezone, currency, campaign status and targeting, impressions, cost, clicks, conversions/value, impression share (IS), Search lost IS (budget), Search lost IS (rank), and Auction Insights rows. Preserve the report's entity level, device/time segments, and metric availability. Ask for campaign objective, conversion action/window, attribution lag, and any planned changes during the period. Compare only like campaign types and scopes; keep Search, Shopping, and PMax segments separate. The [Google IS guide](https://support.google.com/google-ads/answer/2497703?hl=en) and [Auction Insights definitions](https://support.google.com/google-ads/answer/2579754?hl=en) should be checked for current availability and denominator details.

## Read share and loss metrics precisely

IS is observed impressions divided by estimated eligible impressions. Eligibility depends on settings, approval, and quality, and the denominator is estimated. A share change can reflect changed eligibility as well as changed serving. Lost IS due to budget and due to rank are separate diagnostics; they are not interchangeable. Use only fields reported for the campaign type and grain. In particular, do not fill a missing “lost” percentage with zero, or calculate a residual from rounded shares when inputs have different availability or definitions. Google notes Auction Insights may be unavailable below its activity threshold, including Search impressions share below 10%; “unavailable” means censored or insufficient evidence, not no competitors. Preserve bounded values such as `<10%` as intervals, never as exact 10%. If a same-scope below-threshold share is paired with positive Auction Insights rows, reconcile entity, dates, filters, segment, and freshness before interpreting the overlap; withhold the contradictory value until resolved.

Auction Insights has its own eligible-auction population. Overlap rate describes how often another advertiser showed when your ad showed; position-above applies when both ads showed; outranking share covers occasions your ad ranked higher or showed when theirs did not. Do not compare those rates as if they share a denominator, cover the whole market, or represent competitor budget, bids, or total impression share. Google also reports PMax auction insights in Search/Shopping segments; preserve that split.

## Diagnose business implications

Separate delivery constraints from economics. If lost IS budget is reported, check budget pacing, day/time, geography, campaign objective, and performance over the same period. If rank loss is reported, inspect quality, bids or bid strategy, eligibility, and approval evidence only when supplied. Then compare the observed economics of existing spend—such as cost per named conversion or value/cost—to the stated goal, with counts and lag status. Existing average performance does not establish the marginal result of buying missed impressions. Competitor overlap may explain a competitive context but does not reveal their spend or prove that they took profitable sales.

Do not invent missing impression estimates, bid levels, spend, conversion rates, or forecasts. If goals, eligibility, or campaign changes are missing, give a descriptive reading and list the evidence needed before a budget or bid proposal. Distinguish observed changes from hypotheses; a rise in competitor overlap or rank loss is not causal proof of a competitor action.

## Output and authorization

Lead with scope, date, network, campaign type, data refresh/lag, and missing fields. Use a table with campaign/entity; eligible-scope IS and loss fields; reported Auction Insights metrics with their definitions; spend and business outcomes; source rows; interpretation; candidate checks; confidence; and what remains unavailable. Show denominators or the platform's documented denominator where provided. Do not combine across currencies, campaign types, or incompatible segments.

Fictional example: a 30-day Search campaign report shows IS 42%, lost IS budget 18%, and lost IS rank 40%, with $8,000 spend and 80 mature leads in USD. The shares describe estimated eligible opportunity, not the number of profitable leads missed. Review pacing and marginal lead economics before proposing any budget test; Auction Insights rows, if censored, cannot fill the gap.

Any account mutation requires explicit user authorization naming the account, campaigns, exact budget/bid/settings change, amount, and timing. This analysis and an installed skill authorize no changes.

## Portable inputs and examples

- Read [the input contract](references/input-contract.md) when mapping a new export or checking the example's scope and definitions. Copy [the header-only CSV template](assets/input-template.csv) when preparing data; equivalent supplied exports remain acceptable.
- Read [the reusable business context](references/business-context.md) only for business facts or constraints this task needs. Reuse user-supplied facts with their source/date; the template contains no default targets.
- Inspect [the complete fictional input](assets/example-input.csv) with [its example output](references/example-output.md) when learning the output and calculation boundaries. Never use fictional values for a real account.

State whether the result is complete, partial, or blocked for the requested decision. Link material findings to actual supplied rows/sources and separate observed metrics, hypotheses, and estimates. Lead with a short business conclusion, then evidence, uncertainty, and the next measurable check. A data export or installed skill does not authorize account changes.
