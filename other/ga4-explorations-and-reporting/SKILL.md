---
name: ga4-explorations-and-reporting
description: Build ad-hoc analyses in the GA4 Explore workspace and read standard reports correctly within sampling limits. Use when the user asks how to build a free-form, funnel, path, cohort, segment overlap, or user-lifetime exploration, why numbers differ between Explore and standard reports, why a report shows "(other)", whether data is sampled, which attribution model GA4 uses now, or how to pull the same analysis through the Data API.
---

# GA4 explorations and reporting

Pick the analysis surface that answers the question, build it so the numbers are trustworthy, and read them knowing where sampling, cardinality, and the attribution model bend the result. This skill covers the Explore workspace (free-form, funnel, path, cohort, segment overlap, user exploration, user lifetime), standard reports, the sampling and cardinality limits that change what you see, and pulling the same analysis through the Data API v1.

This skill assumes you know sessions, users, engagement rate, and conversion-rate math. For KPI definitions and blended-metric math, see the `programmatic-foundations` skill. GA4 uses key events, not "conversions"; for marking and managing them, see the `ga4-events-and-key-events` skill. For building and exporting audiences, see the `ga4-conversions-and-audiences` skill. When you need unsampled, event-level truth, hand off to the `ga4-bigquery-export-and-sql` skill.

## When to use this skill

- "Build a funnel / path / cohort / free-form / segment overlap exploration."
- "Why do Explore and the standard report show different numbers?"
- "Is this report sampled?" / "What does the sampling triangle mean?"
- "Why is there an (other) row and where did my values go?"
- "Which attribution model does GA4 use now?" / "Where did first-click and linear go?"
- "What is the difference between the default reporting identity and event/device?"
- "Pull this same analysis through the Data API."

Boundaries with sibling skills:
- What counts as a key event and how to mark one: `ga4-events-and-key-events`.
- Building audiences, predictive audiences, and exporting them to ad platforms: `ga4-conversions-and-audiences`.
- Configuring the BigQuery export and writing SQL against the event schema: `ga4-bigquery-export-and-sql`.
- Property, data stream, retention, and reporting-identity setup: `ga4-property-and-data-stream-setup`.

## Quick reference

Pick the technique from the question, not from habit.

| Question | Technique | Why |
| --- | --- | --- |
| How do users move from step A to step B, where do they drop | Funnel exploration | Ordered or open-funnel step conversion and drop-off |
| What paths do users take before or after an event | Path exploration | Tree of preceding/following events or pages |
| How does a weekly acquisition cohort retain or spend over time | Cohort exploration | Retention and per-cohort metric decay |
| How much do two segments overlap | Segment overlap | Venn of up to three segments |
| Custom pivot table or crosstab of any dimensions and metrics | Free-form exploration | Table, bar, line, scatter, geo, crosstab |
| Per-user event stream for debugging or QA | User exploration | Drill into individual anonymized users |
| Lifetime value and lifetime metrics by acquisition | User lifetime | LTV, lifetime engagement, predicted revenue |
| A fixed, board-ready number that must match billing | Standard report or BigQuery | Aggregated tables, less sampling and cardinality risk |

Default rule: use standard reports for headline numbers because they read from pre-aggregated tables and rarely sample. Use Explore when you need to slice, segment, or sequence in ways standard reports cannot. When the number has to be exact and unsampled, go to BigQuery (`ga4-bigquery-export-and-sql`).

## Core process

1. State the question as a shape, not a metric. "Drop-off between add-to-cart and purchase" is a funnel; "what did users do right before churning" is a path; "how does the January cohort retain" is a cohort. The shape picks the technique, so naming it wrong wastes a rebuild.
2. Open the Explore workspace and start the matching technique from the gallery. Every technique shares three panels: Variables (the dimensions, metrics, and segments you make available), Tab Settings (how the current tab uses them), and the canvas (the visualization). You drag from Variables into Tab Settings; nothing renders until it is placed.
3. Set the date range first, then the segments, then the breakdown. Order matters because a wide date range plus a high-cardinality breakdown is what triggers sampling and the "(other)" bucket. Start narrow and widen only if the response stays unsampled.
4. Add only the dimensions and metrics the question needs. Extra rows inflate cardinality and push low-count values into "(other)". A four-column crosstab that answers the question beats a twelve-column one that samples.
5. Check the sampling indicator before you trust the number. A green shield or "100%" means unsampled; a yellow/amber indicator means the response is based on a sample of sessions. If sampled, narrow the range, cut the breakdown, or move the analysis to BigQuery.
6. Read the result against the attribution model and reporting identity in effect. Key-event credit follows the property's attribution model (data-driven by default), and user counts follow the reporting identity (Blended, Observed, or Device-based). Two "correct" reports disagree when these differ, so state both when you report a number.
7. To operationalize a one-off Explore into a recurring pull, rebuild it through the Data API v1 (`runReport`, `runPivotReport`, `runFunnelReport`) or, for unsampled event-level output, in BigQuery. Explore is for exploration; scheduled truth belongs in the API or the warehouse.

## Decision rules and thresholds

### Explore vs standard report vs BigQuery

- Standard report when the number is a headline (users, sessions, key events, revenue) that must be stable and match other GA4 surfaces. Standard reports use aggregate tables, so they sample far less and bucket into "(other)" far less than Explore.
- Explore when you need a funnel, a path, a cohort, a segment overlap, or a custom crosstab that standard reports cannot express, and a small amount of sampling is acceptable.
- BigQuery when the number must be exact and unsampled, when you need event-level detail below what the UI exposes, or when cardinality would bury the values you care about under "(other)". Hand off to `ga4-bigquery-export-and-sql`.

### Sampling thresholds

GA4 applies sampling when an Explore query spans more events than the query threshold:

- Standard properties: sampling begins above 10 million events in the query's date range.
- Analytics 360 properties: sampling begins above 1 billion events per query, and 360 offers unsampled explorations (a daily unsampled-token budget) to force a full pass.

Standard reports read from aggregated tables and generally are not sampled. If a headline number must be unsampled and you are on a standard property near the 10M ceiling, use a standard report or BigQuery instead of Explore.

### Cardinality and the "(other)" row

A dimension with more than 500 distinct values is high-cardinality. When a report or exploration exceeds the row limit, GA4 groups the lowest-count values into a single "(other)" row, so per-value numbers become unreliable even though the total is right. Rules:

- Prefer standard reports for high-cardinality dimensions; their aggregate tables reduce "(other)" bucketing.
- Reduce the date range or the breadth of the breakdown to pull values out of "(other)".
- For genuinely high-cardinality data (item IDs, page paths, transaction IDs), analyze in BigQuery, where there is no "(other)" bucket. Send such data as event parameters rather than registering it as a custom dimension so it stays available in BigQuery without consuming custom-dimension limits.

### Attribution models available in 2026

GA4 credits key events using cross-channel models. As of November 2023 the rules-based first click, linear, time decay, and position-based models were removed. What remains:

| Model | What it does |
| --- | --- |
| Data-driven attribution (default) | Machine learning distributes credit across clicks by measured contribution |
| Paid and organic last click | 100% credit to the last non-direct channel clicked |
| Google paid channels last click | 100% credit to the last Google Ads click, else falls back to paid and organic last click |

Data-driven attribution can reattribute a key event for up to 7 days after it occurs, so very recent conversion credit can shift. Attribution applies to key events, not to traffic or engagement metrics, so a "users by channel" report is unaffected by the model while a "key events by channel" report is not.

### Reporting identity

User and key-event counts depend on the reporting identity: Blended (uses User-ID, then Google signals, then device, then modeling), Observed (User-ID then device, no modeling), or Device-based (device signal only). Changing the identity re-counts users retroactively across the UI, so before comparing two reports confirm they use the same identity. This is set at the property level; see `ga4-property-and-data-stream-setup`.

## Reference material

- `references/exploration-techniques.md`: each of the seven Explore techniques with what it answers, the Tab Settings fields it uses (rows, columns, values, breakdown, steps, node types), segment and filter behavior, and a worked configuration. Read this when building or debugging a specific exploration.
- `references/sampling-and-cardinality.md`: the sampling thresholds by property tier, how to read the sampling indicator, the 500-value cardinality rule and the "(other)" row, quota tokens, and the escalation ladder to BigQuery. Read this when a number looks wrong, is sampled, or shows "(other)".
- `references/attribution-models-2026.md`: the three surviving GA4 attribution models, the November 2023 removals, lookback windows, the data-driven reattribution window, conversion vs key-event terminology, and how attribution differs from BigQuery event-level joins. Read this when a channel report disagrees with a platform or another GA4 surface.

## Templates and examples

- Checkout funnel drop-off: Funnel exploration, open funnel off, steps `view_item` then `add_to_cart` then `begin_checkout` then `purchase`, breakdown by `device category`, 28-day range. Read the step-to-step completion rate; the biggest drop names the fix.
- Path before churn: Path exploration, ending node set to the last session event, expand backward two to three nodes, segment to users with no session in the prior 30 days. Read the most common preceding page or event.
- New-user retention: Cohort exploration, inclusion `first_visit`, return criterion any event, cohort granularity weekly, metric active users, 6-week window. Read the retention curve's week-1 and week-4 cliffs.
- Segment overlap for a campaign: Segment overlap of "Paid social users", "Purchasers", and "Mobile users". Read the three-way intersection to size a retargeting audience before building it in `ga4-conversions-and-audiences`.
- Free-form channel-to-key-event crosstab: rows `session default channel group`, values `sessions` and `key events` and `session key event rate`, 30-day range, no extra breakdown. Read which channel converts, and state the attribution model in the caption.
- Same analysis via API: `runReport` with `dateRanges` 30 days, `dimensions` `sessionDefaultChannelGroup`, `metrics` `sessions` and `keyEvents`, then check `metadata.samplingMetadatas` in the response for the sampled flag. For funnels use `runFunnelReport` (early preview). See `references/exploration-techniques.md` for the field map.

## Common pitfalls

- Trusting a sampled Explore as a headline number. The amber indicator means the number is an estimate from a session sample. Narrow the range, cut the breakdown, or pull it from a standard report or BigQuery before you report it.
- Reading per-value numbers inside an "(other)" row. Once values collapse into "(other)", the individual counts are gone; the total is fine but the breakdown is not. Reduce cardinality or move to BigQuery.
- Comparing Explore to a standard report and calling the difference a bug. They can legitimately differ on sampling, cardinality bucketing, reporting identity, and how estimated/modeled data is included. Match those settings before concluding anything is broken.
- Expecting first-click, linear, time-decay, or position-based models. They were removed in November 2023. Only data-driven, paid and organic last click, and Google paid channels last click remain.
- Saying "conversions" when you mean key events. GA4 renamed conversions to key events; the Google Ads-side counterpart is still called a conversion. Use the right word for the surface, and see `ga4-events-and-key-events` for the mapping.
- Comparing two user counts pulled under different reporting identities. Blended, Observed, and Device-based counts differ by design. Confirm the identity is the same on both before comparing.
- Rebuilding a fragile Explore by hand every week. If it recurs, move it to the Data API or BigQuery so it is reproducible and unsampled, per `ga4-bigquery-export-and-sql`.

## Sources

- [Get started with Explorations](https://support.google.com/analytics/answer/7579450?hl=en) (as of July 2026)
- [Google Analytics 360 (Google Analytics 4 properties), feature and sampling limits](https://support.google.com/analytics/answer/11202874?hl=en) (as of July 2026)
- [About attribution and attribution models](https://support.google.com/analytics/answer/10596866?hl=en) (as of July 2026)
- [High-cardinality dimensions](https://support.google.com/analytics/answer/9309767?hl=en) (as of July 2026)
- [Google Analytics Data API v1 overview](https://developers.google.com/analytics/devguides/reporting/data/v1) (as of July 2026)
