---
name: dv360-reporting
description: Pull the right Display & Video 360 report and read it correctly. Use when the user asks to pull a report, asks what report to use, asks about offline vs instant reporting, wants to schedule a report, asks which metrics and dimensions to add, asks for a reach report, or asks how to export reporting to BigQuery or the API.
---

# DV360 reporting

Pick the report type that answers the question, add only the metrics and dimensions that question needs, then read the numbers against the campaign goal. This skill covers report types, the metric and dimension catalog, scheduling, and programmatic pulls. For what each metric means and how the math works, see the `programmatic-foundations` skill. For attribution, Floodlight setup, Brand Lift, and reach methodology, see the `dv360-measurement-and-attribution` skill.

## When to use this skill

- "Pull a report on [campaign / line item / creative]."
- "What report do I use for [reach / conversions / viewability / video]?"
- "Offline vs instant reporting, which one?"
- "Schedule this report to run weekly."
- "Which metrics and dimensions should I add?"
- "Build me a reach report" or "unique reach by audience."
- "Export reporting to BigQuery" or "pull reports via the API."

Boundary: if the question is what a metric means or how to compute a KPI by hand, that is `programmatic-foundations`. If it is whether a conversion should count or how attribution credits it, that is `dv360-measurement-and-attribution`. If the pull is part of a scripted automation (Reports API auth, SDF), see the `dv360-api-and-sdf-automation` skill. For event-level log analysis in BigQuery, see the `dv360-advanced-analytics-adh` skill.

## Quick reference

Pick the surface first, then the report type.

| Need | Surface | Report or query type |
| --- | --- | --- |
| Fast, interactive, slice while you think | Instant reporting (Reports, Explore) | Standard |
| Large data set, recurring delivery, raw to a warehouse | Offline reporting | Standard, scheduled |
| Unique people reached and frequency | Either | Reach |
| Audience segment performance and composition | Either | Audience |
| YouTube and Partners line items | Either | YouTube |
| Conversions by Floodlight activity | Either | Floodlight |
| Deduplicated reach across digital and linear TV | Offline reporting | Cross-Media Reach |
| Where can I buy this audience or inventory | Offline reporting | Inventory availability |
| Viewability and measurability | Either | Standard with Active View metrics |

Default to instant reporting. The platform is moving toward instant reporting as the primary surface, and offline reporting deactivates scheduled reports that go undownloaded for 60 days or that keep failing for 30 days. Reserve offline reporting for jobs that are too large for the interactive view, that must land on a fixed schedule, or that feed BigQuery.

## Core process

1. **Define the question in one sentence.** "Did line item X hit its CPA target last week?" forces a single goal, a date range, and the grain (line item). A vague pull produces a wide table no one reads.
2. **Pick the report type from the question, not the metrics.** Reach questions need a Reach report because de-duplicated unique users are not a sum of daily rows. Conversion questions need Floodlight columns. Viewability questions need Active View columns. Choosing type first prevents building a Standard report that cannot answer the question.
3. **Pick the surface.** Interactive exploration and anything you will iterate on goes to instant reporting. A recurring stakeholder deliverable or a warehouse feed goes to an offline scheduled report.
4. **Add only the metrics and dimensions the question needs.** Every extra dimension splits the data into more rows and can change how metrics aggregate (a unique-reach number does not add up across an extra split). Start narrow, add a dimension only when you need to explain a number.
5. **Set the date range and filters.** Match the range to the question and to the metric's constraints (reach metrics run on blocks of 92 to 93 days or less and lag about 3 days). Filter to the advertiser, campaign, or line item in scope so totals are not diluted.
6. **Run and read against the goal.** Compare each metric to its target from the media plan, not to itself. A 0.40 percent CTR is good or bad only relative to the benchmark for that format and goal.

## Report and query types

- **Standard.** The workhorse. Impressions, clicks, cost, conversions, video, and Active View, sliced by any standard dimension. Use for delivery, pacing, and performance reads.
- **Reach.** Unique users reached, viewable unique reach, average frequency, click reach, and incremental reach, with co-viewing variants for connected TV. Unique reach is modeled and deduplicated across devices, so it is not the sum of daily impressions. Requires Country, Gender, and Age dimensions and is supported only in certain countries.
- **Audience.** Performance and composition by audience list, demographic, affinity, or in-market segment. Use to compare segments and find who converts.
- **YouTube.** TrueView and YouTube and Partners metrics (views, view rate, earned actions, earned subscribers) for YouTube line items. Standard reports do not carry the full YouTube metric set.
- **Floodlight.** Conversions attributed to Floodlight activities, post-click and post-view, with revenue. Use to tie media to outcomes. Definitions and attribution live in `dv360-measurement-and-attribution`.
- **Cross-Media Reach.** Incremental and deduplicated reach across digital (including CTV) and linear TV in one view, using third-party TV data. Set up under Reports, Cross-media reach: pick a location, add up to 50 insertion orders, add the TV campaigns, then set dates and demographics. Reporting window is 92 days or less and data covers the past 24 months. Geographic availability is limited.
- **Inventory availability.** Forecasts addressable inventory and audience scale for planning. An offline report type, useful before launch to size a buy.
- **Active View.** Viewability and measurability. In practice you add Active View metrics to a Standard report rather than building a separate type.

## Key metrics

Add the smallest set that answers the question. Formulas and definitions live in `programmatic-foundations`; this is the DV360 column mapping and what to watch.

- **Impressions, Clicks, Click Rate (CTR).** Delivery and engagement. CTR is clicks over impressions.
- **Total Media Cost, Media Cost, Revenue.** Spend and booked revenue. Media Cost is the raw inventory cost; Total Media Cost adds platform and data fees. Know which one your plan is measured on.
- **Media Cost eCPM, CPM.** Cost per thousand impressions. CPM is the rate you bought; eCPM is the realized rate after delivery. Diverging eCPM and CPM signals waste or under-delivery.
- **Post-Click Conversions, Post-View Conversions.** Conversions credited after a click versus after a view. Report them separately; collapsing them hides how much credit is view-through.
- **CPA (cost per acquisition), Revenue eCPA.** Cost per conversion. Compare to the plan target, not across line items with different goals.
- **ROAS.** Revenue over cost. Use when the goal is value, not volume.
- **Active View: % Viewable Impressions, Measurable Impressions, % Audible and Visible.** Viewable rate is viewable over measurable, not over total. A high viewable rate on a low measurable base is not a clean signal; read both.
- **Complete Views, Completion Rate (VCR), Midpoint and quartile views.** Video pacing and retention. VCR is completes over starts (or over impressions, depending on the column); confirm the denominator before you report it.
- **CPCV (cost per completed view).** Cost efficiency for video and CTV goals.
- **Unique Reach: Impression Reach, Average Impression Frequency.** Deduplicated people and how often each saw the ad. Use to manage saturation, not to sum.
- **Win rate.** Auctions won over auctions bid. Low win rate with healthy budget points at bid or eligibility problems; hand off to the `dv360-troubleshooting` skill.

## Key dimensions

Date, Advertiser, Campaign, Insertion Order, Line Item, Creative, Audience List, Demographic, Country and Region (geo), Device Type, App or URL, Exchange, and Deal ID. Each dimension multiplies rows and can change aggregation. Add a dimension only to explain a number you already see at a coarser grain. For reach metrics, the required Country, Gender, and Age dimensions are mandatory and cannot be dropped.

## Scheduling and automation

- **Scheduled offline reports.** Set a frequency (daily, weekly, monthly) and a start and end date. Output is CSV, zipped automatically when over 200 kB, delivered by email attachment or download link. Only the report files are shared, not the report definition. Undownloaded reports deactivate after 60 days and failing reports after 30, so do not rely on a schedule no one collects.
- **BigQuery export.** Link the DV360 partner or advertiser to a BigQuery project and dataset (Linked Accounts, BigQuery Exporter), grant the generated service account BigQuery Job User on the project and BigQuery Data Editor on the dataset, then the dataset appears as a BigQuery destination in offline reporting. Use this when reporting must join other data or exceed CSV practicality.
- **Bid Manager Reports API.** The DV360 reporting API (v2) exposes queries (create, get, list, run, delete) and the reports each query generates (get, list). Use it to create and run report queries programmatically and to retrieve the generated CSV from Cloud Storage. For full auth, scopes, and the SDF workflow, see the `dv360-api-and-sdf-automation` skill.
- **Data Transfer.** For raw, event-level log files rather than aggregated reports, DV360 Data Transfer delivers files to Cloud Storage or BigQuery. Use it when row-level analysis is the goal; analysis patterns live in the `dv360-advanced-analytics-adh` skill.

## Common pitfalls

- **Summing unique reach.** Reach is modeled and deduplicated. Adding daily or per-segment reach rows overcounts people. Read reach at the grain you need it; do not aggregate it yourself.
- **Reading viewable rate without measurable rate.** % Viewable is over measurable impressions. A great viewable percentage on a small measurable base is noise.
- **Collapsing post-click and post-view.** They answer different questions. Keep them as separate columns or you will over-credit view-through.
- **Media Cost vs Total Media Cost mismatch.** Plans measured on one and reports built on the other will not reconcile. Match the column to the plan.
- **A schedule nobody downloads.** Offline scheduled reports deactivate after 60 days undownloaded. For anything that must persist, prefer BigQuery export or an API pull.
- **Too many dimensions.** Each split changes aggregation and buries the answer. Start at the coarsest grain that could answer the question and add dimensions only to explain an anomaly.
- **Date range outside metric limits.** Reach and Cross-Media Reach run on windows of about 92 to 93 days or less and lag a few days. A 6-month reach pull will not return.

## Sources

- Offline reporting, Display & Video 360 Help: https://support.google.com/displayvideo/answer/6375151 (as of June 2026)
- Instant reporting, Display & Video 360 Help: https://support.google.com/displayvideo/answer/7674615 (as of June 2026)
- Reach reports, Display & Video 360 Help: https://support.google.com/displayvideo/answer/6170584 (as of June 2026)
- Cross-Media Reach reporting, Display & Video 360 Help: https://support.google.com/displayvideo/answer/13955444 (as of June 2026)
- Metrics in reports, Display & Video 360 Help: https://support.google.com/displayvideo/table/3187025 (as of June 2026)
- Data Transfer v2, Display & Video 360 Help: https://support.google.com/displayvideo/answer/7315192 (as of June 2026)
- Bid Manager API REST reference (v2): https://developers.google.com/bid-manager/reference/rest (as of June 2026)
- Create and access scheduled reports, Bid Manager API: https://developers.google.com/bid-manager/guides/scheduled-reports/overview (as of June 2026)
