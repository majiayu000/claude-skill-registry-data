---
name: dv360-advanced-analytics-adh
description: Run privacy-safe, event-level analysis of Display & Video 360 data in BigQuery with Ads Data Hub, and decide when to use raw BigQuery exports instead. Use when the user mentions Ads Data Hub, ADH, privacy-safe analysis, BigQuery export, cross-device or cross-campaign reach, de-duplicated reach, incrementality, joining first-party data, audience overlap, reach curves, frequency optimization, custom attribution, segment-level ROAS, or connected TV analysis that standard reporting cannot do.
---

# DV360 advanced analytics with Ads Data Hub

Answer questions that aggregated reports cannot: de-duplicated reach across devices and campaigns, custom attribution, incrementality, audience overlap, and segment-level ROAS that needs your own first-party data joined to event-level ad logs. Ads Data Hub (ADH) does this in BigQuery without exposing a single user-level row. This skill decides whether a question even needs ADH, frames the query, and gets a result past the privacy checks.

For what each metric means and how the math works, see the `programmatic-foundations` skill. For standard reports and the BigQuery export path, see the `dv360-reporting` skill. For Floodlight, attribution models, and reach methodology, see the `dv360-measurement-and-attribution` skill. For scoring impressions to drive bids (the analyst-to-trader bridge), see the `dv360-custom-bidding` skill.

## When to use this skill

- "Analyze this in Ads Data Hub" or "write an ADH query."
- "De-duplicated reach across devices / across campaigns / cross-media."
- "Build a reach curve" or "find the optimal frequency."
- "Run an incrementality / lift analysis" or "what was the incremental reach of campaign B over A."
- "Join our first-party data (CRM, loyalty, LTV) to DV360 impressions."
- "Segment-level ROAS," "audience overlap between two segments," "connected TV co-viewing analysis."
- "Should I use ADH or a raw BigQuery export?" or "why can I not see user-level rows."

Boundary with sibling skills: if a standard report answers it (delivery, pacing, viewability, a supported Reach report), stay in `dv360-reporting`. ADH is for analysis that needs event-level joins, custom logic, or de-duplication that aggregated reports cannot express. If the question is which attribution model to pick or how Floodlight counts, that is `dv360-measurement-and-attribution`. ADH is where you build a custom attribution model from the events themselves.

## Quick reference

First decide whether you need event-level analysis at all, then pick the surface.

| Need | Surface | Why |
| --- | --- | --- |
| Delivery, pacing, viewability, supported Reach report | Standard reporting (`dv360-reporting`) | The report already answers it. Do not reach for ADH. |
| De-duplicated reach across devices, campaigns, or media; reach curves; frequency optimization | Ads Data Hub | Reach must be computed from event-level logs joined on a user key, not summed from rows. |
| Custom attribution, incrementality, audience overlap, segment-level ROAS with your first-party data | Ads Data Hub | Needs event-level joins and custom logic, with privacy enforced on output. |
| Row-level log files for your own warehouse modeling, where you own the privacy obligations | Raw BigQuery export (Data Transfer Service) | Gives raw rows, but you take on all privacy responsibility. |

Default position: try a standard report first, use ADH when the question needs event-level joins or de-duplication, and reserve a raw export for when you genuinely need the rows in your own pipeline and accept the privacy duty that comes with them.

## What Ads Data Hub is

ADH lets you query event-level Google advertising data (impressions, clicks, conversions across Display & Video 360, Google Ads, Campaign Manager 360, and YouTube) joined to your own first-party data, with all of it living in BigQuery inside your Google Cloud project. The defining constraint: you never get user-level rows out. Google operates on the event-level data inside its own project, you bring your first-party tables into yours, ADH sits between them and runs your SQL, and only aggregated, privacy-checked output is written back to your BigQuery dataset.

Two facts shape every ADH design decision:

- **Joins are keyed to a user identifier you choose, and the output is aggregated.** You can join impressions to a CRM table on a user key to compute, say, ROAS by loyalty tier, but you receive the tier-level aggregate, never the per-user rows.
- **The privacy checks decide whether your query returns anything at all.** A query that is logically correct still returns nothing if a group is too small to pass the aggregation threshold. Designing for the checks is part of writing the query, not an afterthought.

## Use cases that standard reporting cannot do

These are the questions to route to ADH, because each one needs event-level data or a join that aggregated reports cannot produce:

- **Cross-device and cross-campaign de-duplicated reach.** Count distinct people across devices and across multiple campaigns or line items, computed from the event log on a user key. Summing reach rows from a report overcounts; ADH de-duplicates at the user level and returns the aggregate.
- **Custom attribution.** Build your own attribution model (position-based, time-decay, or a bespoke rule) directly from the impression, click, and conversion events, rather than accepting a packaged model.
- **Incrementality.** Compare exposed and unexposed (or control) groups to estimate the incremental conversions or reach a campaign drove, beyond what a last-touch report credits.
- **Segment-level ROAS with first-party data.** Join revenue or lifetime-value data from your CRM to ad exposure and report ROAS or value by your own segments (loyalty tier, predicted LTV band, product affinity).
- **Audience overlap.** Measure how much two audiences or two campaigns overlap in the people they reached, to find redundant targeting or net-new reach.
- **Reach curves and frequency optimization.** Model reach as a function of impressions or budget, find where the curve flattens, and pick the frequency cap that maximizes net reach for the spend. See `dv360-frequency-and-brand-safety` for setting the cap once you have the answer.
- **Connected TV analysis.** Analyze CTV exposure, co-viewing, and incremental reach of CTV over other channels, which the standard surfaces only partially expose.

If a request is none of these and a supported report covers it, do not pay the ADH tax in latency and complexity. Use the report.

## Privacy checks

ADH enforces privacy on the output, not the input. Design every query expecting these gates:

- **Aggregation requirement (minimum users per row).** Each output row must aggregate over at least a minimum number of distinct users, or the row is dropped. The threshold depends on the mode and data: roughly 50 unique users per row under difference checks, roughly 20 per row under noise injection, and roughly 10 per row for queries restricted to click and conversion data. Treat these as moving targets to design around, not exact contracts; confirm the current values against the privacy-checks documentation before relying on a number.
- **Difference checks.** ADH compares result sets across queries to stop someone from isolating an individual by differencing two nearly identical aggregates (for example running the same query twice with one user added). This is why re-running a query with a slightly narrower filter can suddenly return nothing.
- **Noise injection.** In the noise-injection mode, ADH adds calibrated random noise to results so that no single user materially changes an output value, while keeping aggregates accurate enough to read. Expect small results to be noisier than large ones.
- **Static checks.** ADH inspects the query text itself for patterns that would leak user-level data (for example selecting a user id into the output) and blocks them before the query runs.
- **Data access budget.** Repeated querying of the same underlying data spends a data access budget. Heavy iteration, or many slightly different cuts of the same slice, can exhaust it, after which further queries on that data are blocked until the budget recovers. Plan the analysis so you are not burning the budget on trial and error.

The practical consequence: write the query to produce coarse-enough groups to clear the aggregation threshold, avoid tiny segments, and do your iteration on logic before you start spending budget on the real data.

## BigQuery: ADH versus raw export

Both paths put DV360 data in BigQuery, but they differ on privacy and on who carries the obligation.

- **Ads Data Hub.** Event-level analysis with privacy enforced on the output. You get aggregated, checked results and never user-level rows. Use it whenever the question needs joins to first-party data or de-duplication and you want Google to enforce the privacy floor.
- **BigQuery Data Transfer Service for DV360.** A managed connector that loads DV360 reporting data into BigQuery on a scheduled, recurring basis, landing in date-partitioned tables. This is report-level data on a schedule, useful when you want DV360 reporting alongside other warehouse data without enforcing ADH-style aggregation. For the reporting-side view of this export, see the `dv360-reporting` skill.
- **DV360 Data Transfer (event-level log files).** Delivers raw, row-level log files. This gives you the events themselves to model in your own pipeline, but you then own every privacy obligation that ADH would otherwise enforce. Choose it only when row-level modeling in your environment is genuinely required and you have the governance to handle user-level data responsibly. The mechanics of this transfer live in the `dv360-reporting` skill.

Rule of thumb: if the analysis needs first-party joins or de-duplication and you want the privacy floor enforced for you, use ADH. If you need scheduled report-level data next to other warehouse tables, use the BigQuery Data Transfer Service. Only take raw event-level log files when you must model the events yourself and can carry the privacy duty.

## Core process

1. **Define the question as one measurable statement.** "What was the de-duplicated reach of campaigns A and B combined, by device, last month?" names the metric, the grain, and the window. A vague question produces a query that either fails the privacy checks or answers nothing useful.
2. **Confirm it actually needs ADH.** If a supported report answers it, stop and use `dv360-reporting`. Only continue when the question needs event-level joins, custom logic, or de-duplication.
3. **Identify the tables and the join key.** Decide which event-level ad tables you need and which first-party table you are joining, and on what user identifier. The join key determines what de-duplication and segmentation are even possible.
4. **Write the SQL to aggregate above the privacy floor.** Group to a grain coarse enough to clear the minimum-users-per-row threshold. Avoid tiny segments, single-day slices on thin data, or splits that fragment users into sub-threshold groups.
5. **Run it and read the privacy result, not just the numbers.** If rows are missing, the cause is usually the aggregation threshold or a difference check, not a logic bug. Widen the grouping or the window rather than re-running the same narrow cut, which also spends data access budget.
6. **Get the aggregated output and visualize.** The result is an aggregate table in your BigQuery dataset. Chart the reach curve, the overlap, or the segment ROAS from there. Tie the answer back to the decision it serves (a frequency cap, a budget reallocation, a targeting change).

## Caveats and prerequisites

- **Access and setup.** ADH runs on Google Cloud and requires an ADH account linked to the DV360 advertiser or partner, plus a BigQuery project to hold your first-party tables and receive output. Some features and data require allowlisting or account approval before they are available. Confirm access before promising an analysis.
- **Latency.** ADH data is not instant. Event-level data lands with a lag, so same-day questions belong in instant reporting, not ADH. Build in the lag when scoping a deadline.
- **Query budget.** The data access budget caps how much you can iterate on the same data. Heavy trial-and-error exhausts it. Settle the query logic on test runs before spending budget on the real cut.
- **Privacy floor is non-negotiable.** Small segments will not return. If the business needs a cut finer than the threshold allows, the answer is to coarsen the segment or the window, not to fight the check.
- **SQL dialect and templates.** ADH uses BigQuery SQL with ADH-specific tables and functions. Use the documented query templates as a starting point rather than writing reach or overlap logic from scratch.

## Common pitfalls

- **Reaching for ADH when a report would do.** ADH adds latency, cost, and privacy constraints. If a supported Reach or Standard report answers the question, use it. Save ADH for genuine event-level work.
- **Designing a query that cannot pass the privacy checks.** Slicing to tiny segments or single users returns nothing. Aggregate above the minimum-users-per-row floor from the start.
- **Burning the data access budget on iteration.** Running many near-identical queries on the real data to "see what comes back" exhausts the budget. Iterate on logic with test runs, then run the final cut once.
- **Summing reach instead of de-duplicating.** The whole point of ADH reach work is de-duplication on a user key. Adding reach across rows or segments overcounts people, the same error called out in `dv360-reporting`.
- **Confusing the raw export with ADH.** A raw event-level export gives you rows and hands you the privacy obligation; ADH gives you checked aggregates. Picking the export for convenience and then mishandling user-level data is a governance failure, not a shortcut.
- **Ignoring latency on a time-sensitive read.** ADH lags. A question that needs today's numbers belongs in instant reporting.

## Sources

- Introduction to Ads Data Hub: https://developers.google.com/ads-data-hub/guides/intro (as of June 2026)
- Privacy checks in Ads Data Hub: https://developers.google.com/ads-data-hub/guides/privacy-checks (as of June 2026)
- Ads Data Hub for Google for Developers (overview and access): https://developers.google.com/ads-data-hub (as of June 2026)
- What is the BigQuery Data Transfer Service: https://docs.cloud.google.com/bigquery/docs/dts-introduction (as of June 2026)
- Load Display & Video 360 data into BigQuery (Data Transfer Service connector): https://docs.cloud.google.com/bigquery/docs/display-video-transfer (as of June 2026)
- Data Transfer v2, Display & Video 360 Help (event-level log files): https://support.google.com/displayvideo/answer/7315192 (as of June 2026)
- Link to an Ads Data Hub account, Display & Video 360 Help: https://support.google.com/displayvideo/answer/9002720 (as of June 2026)
