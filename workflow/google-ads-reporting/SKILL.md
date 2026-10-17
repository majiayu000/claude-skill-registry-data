---
name: google-ads-reporting
description: Pull the right Google Ads report and read the numbers correctly. Use when the user asks about Google Ads reporting, the report editor, predefined reports, custom columns, segments, dimensions, impression share, search lost IS (budget vs rank), absolute top or top impression share, which metrics to use in Google Ads, ROAS or cost per conversion, scheduling reports, Looker Studio, Google Ads scripts, or GAQL and API reporting.
---

# Google Ads reporting

Pick the report surface that answers the question, add only the columns and segments that question needs, then read each metric against the campaign goal. This skill covers the report editor, predefined reports, custom columns, segments, dimensions, the metric catalog (including impression share), and the three ways to report at scale (scripts, Looker Studio, the API with GAQL).

Google Ads is a separate platform from Display & Video 360. Do not apply DV360 report types, column names, or surfaces here, and do not carry these into DV360. For shared KPI math and definitions (CTR, CPA, ROAS, eCPM), see the `programmatic-foundations` skill. For choosing the metric set by objective (awareness, consideration, action, retention), see the `reporting-by-campaign-goal` skill. For multi-touch and assisted-conversion reads, see the `path-to-conversion-analysis` skill. When the pull is scripted against the API, hand the auth, batching, and mutate workflow to the `google-ads-api-and-bulk-operations` skill.

## When to use this skill

- "Pull a Google Ads report on [campaign / ad group / keyword / asset]."
- "How do I use the report editor?" or "build a custom table."
- "What are predefined reports?" or "where did the Dimensions tab go?"
- "Create a custom column for [profit / blended ROAS / mobile share]."
- "Segment this by device / network / click type / time / conversions."
- "What is my impression share?" or "explain search lost IS (budget) vs (rank)."
- "Which metrics should I report for this campaign?"
- "Schedule this report" or "email it weekly."
- "Connect Google Ads to Looker Studio" or "report with a script."
- "Pull this with GAQL" or "report via the Google Ads API."

Boundary: if the question is what a metric means or how the math works, that is `programmatic-foundations`. If it is which metrics belong to a given objective, that is `reporting-by-campaign-goal`. If it is how a conversion is credited across touchpoints, that is `path-to-conversion-analysis`. If the work is API auth, bulk mutates, or running GAQL in code, that is `google-ads-api-and-bulk-operations`.

## Quick reference

Pick the surface from the question, not from the metrics you think you want.

| Need | Surface | Notes |
| --- | --- | --- |
| Quick answer, slice while you think | Statistics table with segments | Fastest. Segment the live table by time, device, network, click type, or conversions. |
| A ready-made cut by a non-default dimension (geo, time, paid and organic) | Predefined reports (formerly Dimensions) | Starting point you can save, edit, and schedule. |
| A custom table or chart, saved and shared | Report editor (Custom) | Drag dimensions to rows, metrics to columns. Table, Line, Column, Bar, Scatter, or Pie. |
| A metric Google does not ship as a column | Custom column | Build from existing metrics, filters, functions, and other custom columns. |
| Recurring stakeholder deliverable | Saved report on a schedule | Email at a set interval. Export CSV or other formats. |
| A live dashboard or a blend with other data | Looker Studio | Use the Google Ads connector as a data source. |
| Programmatic pull or automation | Scripts or the API with GAQL | Scripts for in-product automation, the API for a managed integration. |

Default to segmenting the statistics table for a one-off answer. Reach for the report editor when you need a saved, shaped artifact, and for custom columns when the metric you need does not exist as a stock column.

## Core process

1. **Define the question in one sentence.** "Did the non-brand search ad groups hit a 4x ROAS last week?" forces a single goal, a date range, and a grain (ad group). A vague pull produces a wide table no one reads.
2. **Pick the surface from the question.** A one-off slice goes to the live table with a segment. A reusable, shaped artifact goes to the report editor. A metric Google does not ship goes to a custom column. A blend or a live dashboard goes to Looker Studio. An automated feed goes to a script or the API.
3. **Add only the metrics the question needs.** Start with the smallest set that answers it. Every extra column is noise, and conversion-based segments blank out non-conversion columns (Clicks, Impr., Cost show "--" when a conversion segment is applied), so do not mix them carelessly.
4. **Segment or split only to explain a number.** Each segment or dimension multiplies rows. Add Device only when you suspect device is the story. Read at the coarsest grain that could answer the question first.
5. **Set the date range and scope filters.** Match the range to the question. Filter to the account, campaign, or ad group in scope so totals are not diluted by everything else.
6. **Read each metric against its plan target, not against itself.** A 3 percent CTR or a 35 dollar CPA is good or bad only relative to the benchmark for that channel and goal. Pull the goal from `reporting-by-campaign-goal` if you are unsure which metrics matter.

## Surfaces in detail

- **Statistics table with segments.** The campaigns, ad groups, ads, and keywords tables each accept segments. Segment splits one row into several so you can isolate, for example, mobile vs desktop without leaving the table. This is the fast path for a single question.
- **Predefined reports (formerly the Dimensions tab).** Ready-made reports that answer common questions (geographic, time, paid and organic, and more). Open one, then save it as the starting point for a report you can edit, schedule, and share.
- **Report editor.** Build a custom table or chart from scratch. Drag a dimension (Campaign, Ad group, Day) into Row, X-Axis, Series, or Segment, and drag metrics (Clicks, Conversions, Cost) into Columns, Y-Axis, or Value. Chart types are Table, Line, Column, Bar, Scatter, and Pie. Filter on data that is not in your rows or columns, apply conditional formatting, save, share, and add to a dashboard.
- **Custom columns.** Build a metric Google does not ship: combine existing metrics, apply a filter (for example Clicks where Device is Mobile), reference other custom columns, and use spreadsheet-style functions. Custom columns can be filtered, sorted, downloaded, and charted like stock columns. Use them for profit, margin, blended ROAS, mobile share, and any account-specific ratio.

## Segments

Segment to split a table row by an attribute. The choices depend on which table you are viewing, but the ones that matter most:

- **Time.** Day, week, month, quarter, year, day of week, and hour of day. Use to find day-parting and trend.
- **Device.** Computers, mobile phones, tablets, and TV screens. The most common first split when performance looks flat in aggregate.
- **Network (with search partners).** Google Search, search partners, and the Display Network. Always check this before judging search performance, because partner and Display traffic behave differently.
- **Click type.** Which element drove the visit (headline, sitelink, call, and so on). Use to see whether assets, not the core ad, are carrying clicks.
- **Conversions.** Conversion action, conversion category, and days to conversion. These segments only populate conversion columns. Non-conversion columns blank to "--" when a conversion segment is applied, so segment a conversion-only view rather than mixing.
- **Top vs Other.** Whether the ad showed in the top positions or elsewhere on the page.

Add one segment at a time. Stacking segments multiplies rows fast and buries the answer.

## Dimensions

In the report editor, dimensions become rows or splits: Campaign, Ad group, Ad, Keyword, Search term, Day, Device, Network, Geographic (country, region, city), Landing page, Conversion action, and more. Each dimension multiplies rows and can change how a metric aggregates. Add a dimension only to explain a number you already see at a coarser grain.

## Metrics that matter

Add the smallest set that answers the question. Formulas live in `programmatic-foundations`; this is what to pull in Google Ads and what to watch.

- **Impressions, Clicks, CTR.** Delivery and engagement. CTR is clicks over impressions. Read CTR by network, because search partners and Display drag a blended CTR.
- **Avg. CPC, Cost.** Average cost per click and total spend. Avg. CPC moving up with flat conversions points at competition or a bidding change.
- **Conversions, Conv. value (Conversion value).** Outcomes and their booked value. Confirm which conversion actions are counted in the Conversions column before you trust it.
- **Cost / conv. (cost per conversion), Conv. rate (conversion rate).** Efficiency and funnel quality. Cost per conversion is the headline efficiency metric for an action goal. Conversion rate is conversions over interactions; a falling rate with steady cost per click is usually a landing-page or audience-quality issue.
- **Conv. value / cost (ROAS).** Return on ad spend, revenue over cost. Use when the goal is value, not volume. A volume goal optimized to cost per conversion can still lose money if value per conversion varies, so report ROAS whenever revenue differs by product.
- **Search impression share (Search IS).** Impressions received on the Search Network divided by impressions you were eligible to receive. The single best read on how much of the available demand you are capturing.
- **Search lost IS (budget).** Share of eligible impressions missed because the budget ran out. This is the budget-limited signal. Available at the campaign level.
- **Search lost IS (rank).** Share of eligible impressions missed because of low Ad Rank (bid and quality). This is the rank-limited signal. Budget-limited and rank-limited call for different fixes, so always read both lost-IS columns together.
- **Search top IS and Search absolute top IS.** Share of your impressions that showed among the top ads, and in the very first position above the organic results. Use to judge prominence, not just presence.
- **Search lost top IS and Search lost absolute top IS (budget and rank variants).** Why you are not reaching the top or absolute top: a budget variant and a rank variant for each. Use them to decide whether more budget or a higher bid and better quality would lift you into top positions.

When the question is "which metrics should I report for this campaign," route the objective-to-metric mapping through `reporting-by-campaign-goal` and pull only that set.

## Reporting at scale

- **Saved reports on a schedule.** Save a report editor report, then schedule it to email account users at a set interval. Export formats include CSV. Use for recurring stakeholder deliverables. The schedule shares the file, so confirm someone actually consumes it.
- **Looker Studio.** Connect Google Ads as a data source with the Google Ads connector, then build live dashboards or blend Google Ads with other sources. A single data source connects to one account, and a manager (MCC) data source can report across multiple sub-accounts. Note that Auction Insights fields are not available through the connector, so impression-share competitive views still live in the product.
- **Google Ads scripts.** JavaScript in a browser-based environment that can fetch entities, run report queries, and schedule itself to run without an active session. Use for in-product automation: recurring exports, alerting, and bulk checks across accounts. Scripts query with GAQL under the hood.
- **The API with GAQL.** For a managed integration, query the Google Ads API with the Google Ads Query Language. A query is `SELECT fields FROM resource WHERE conditions ORDER BY field LIMIT n`, returning rows of resources, attributes, segments, and metrics. Build and validate queries with the interactive query builder before you ship them. For auth, batching, and mutates, hand off to `google-ads-api-and-bulk-operations`.

## Common pitfalls

- **Reading a blended CTR or CPA across networks.** Search partners and the Display Network behave differently from Google Search. Segment by network before you judge search performance.
- **Mixing conversion segments with delivery columns.** A conversion segment blanks Clicks, Impr., and Cost to "--". Pull a conversion-only view when you segment by conversion action or category.
- **Stacking segments.** Each segment multiplies rows. One at a time, or the answer disappears into a grid.
- **Confusing the two lost-IS signals.** Search lost IS (budget) and Search lost IS (rank) demand opposite fixes (raise budget vs raise bid and quality). Never quote one without the other.
- **Optimizing to cost per conversion when value varies.** If conversions are worth different amounts, a great cost per conversion can still be a poor ROAS. Report value when revenue differs by product or lead type.
- **Trusting fresh conversion numbers.** Conversions lag (often hours, longer for some actions). Do not declare "no conversions" or re-optimize on data that is only a few hours old.
- **Expecting Auction Insights in Looker Studio.** Those fields are not in the connector. Read impression-share competitive data in the product.
- **Treating Google Ads columns like DV360 columns.** The platforms name and compute metrics differently. Do not port DV360 report logic into Google Ads.

## Sources

- Create and manage reports, Google Ads Help: https://support.google.com/google-ads/answer/6201327 (as of June 2026)
- Create custom reports in Report Editor, Google Ads Help: https://support.google.com/google-ads/answer/7489070 (as of June 2026)
- Use segments in your tables, Google Ads Help: https://support.google.com/google-ads/answer/2454072 (as of June 2026)
- About custom columns, Google Ads Help: https://support.google.com/google-ads/answer/3073556 (as of June 2026)
- About impression share, Google Ads Help: https://support.google.com/google-ads/answer/2497703 (as of June 2026)
- Get impression share data, Google Ads Help: https://support.google.com/google-ads/answer/7103314 (as of June 2026)
- About top and absolute top metrics, Google Ads Help: https://support.google.com/google-ads/answer/7501826 (as of June 2026)
- Google Ads Query Language overview, Google Ads API: https://developers.google.com/google-ads/api/docs/query/overview (as of June 2026)
- Google Ads scripts product overview, Google for Developers: https://developers.google.com/google-ads/scripts/docs/start (as of June 2026)
