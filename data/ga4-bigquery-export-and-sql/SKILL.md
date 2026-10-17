---
name: ga4-bigquery-export-and-sql
description: Configure the GA4 BigQuery export and query its nested event schema for unsampled, event-level analysis. Use when the user asks how to link GA4 to BigQuery, daily vs streaming vs fresh daily export, the events_YYYYMMDD table, UNNEST event_params, rebuild sessions or key events in SQL, why BigQuery totals do not match the GA4 UI, the 1M events per day Standard limit, or how to attribute conversions from raw GA4 export data.
---

# GA4 BigQuery export and SQL

Get GA4 event data out of the reporting UI and into BigQuery, where it is raw, unsampled, and joinable, then query the nested event schema to answer questions the standard reports cannot. The export is the only way to see every event with no sampling and no cardinality collapse, which is why serious attribution, sessionization, and cross-source joins live here and not in Explore.

This skill assumes you know what an event, a key event, a session, and CPA/ROAS are. For the event data model and how key events are defined and marked, see the `ga4-events-and-key-events` skill. For sampling and cardinality limits inside the GA4 UI, see `ga4-explorations-and-reporting`. For reconciling the numbers you compute here against CM360, DV360, or a DSP, hand off to `cross-platform-conversion-reconciliation`.

## When to use this skill

- "How do I link GA4 to BigQuery?" / "Set up the BigQuery export."
- "Daily vs streaming vs fresh daily export, which do I pick?"
- "Query the events_YYYYMMDD table" / "how do I UNNEST event_params?"
- "Get the value of a specific event parameter (page_location, ga_session_id, transaction value)."
- "Rebuild sessions / count key events / attribute conversions from the raw export."
- "Why does BigQuery not match the GA4 UI?" / "why are my numbers off by a few percent?"
- "I hit the 1M events per day export limit on a Standard property."
- "Deduplicate events / handle the intraday table / dedupe streaming rows."

Boundaries with sibling skills:
- Standing up the property and data streams that feed the export: `ga4-property-and-data-stream-setup`.
- Defining, marking, and managing key events and recommended ecommerce events: `ga4-events-and-key-events`.
- Building audiences and exporting conversions to ad platforms: `ga4-conversions-and-audiences`.
- Explore reports, sampling, and attribution models inside the UI: `ga4-explorations-and-reporting`.
- Reconciling BigQuery-derived conversions against ad platforms and the billed number: `cross-platform-conversion-reconciliation`.

## Quick reference

| Situation | Do this | Why |
| --- | --- | --- |
| Need every event, no sampling | Query `events_YYYYMMDD` daily tables | Daily export is complete and unsampled |
| Standard property over 1M events/day | Expect truncation, plan a fix | Standard daily export caps at 1M events/day |
| Need data within minutes | Enable streaming export | Streaming lands rows continuously (extra cost) |
| Streaming rows look duplicated | Dedupe on the batch keys | Streaming can deliver a row more than once |
| Reading today before daily runs | Query `events_intraday_YYYYMMDD` | Intraday table holds streaming rows until daily completes |
| Pull an event parameter value | `UNNEST(event_params)` and filter on `key` | Params are a repeated record, not columns |
| Rebuild a session | Read `ga_session_id` from `event_params` | GA4 stores the session id as a param, not a top-level field |
| Count a key event | Filter `event_name`, apply your consent and validity rules | The export has no "key event" flag; you define it in SQL |
| 360 property, very high volume | Consider fresh daily export | 360 supports up to 20B events/day and faster batches |

## Core process

1. Confirm you actually need the export. If the question is answerable in a standard report without sampling, stay in the UI; the export adds BigQuery cost and query engineering. Reach for it when you need unsampled event-level data, joins to non-GA data, or logic the UI cannot express (custom sessionization, custom attribution, dedup against another source).
2. Link the property to a BigQuery project, because the link is what provisions the dataset and starts the daily flow. Do it in the property's Admin under Product links, BigQuery links, or through the Admin API `properties.bigQueryLinks` resource. This spends BigQuery money, so gate it: name the target project, set the region, and get sign-off before you enable it.
3. Choose the export types. Turn on daily export for the complete unsampled tables. Add streaming only if you need near-real-time data, since it bills per gigabyte and needs dedup. On a 360 property, consider fresh daily export for faster, more complete batches.
4. Set the export controls at link time. Pick the dataset location (region) deliberately because it is fixed for the dataset and affects where you can join data. Decide whether to include advertising identifiers, and list any events to exclude from export so you do not pay to store data you will never query.
5. Verify the first tables land. Daily export writes `events_YYYYMMDD` (usually mid-afternoon in the property timezone, one table per day). Streaming writes `events_intraday_YYYYMMDD`, which is deleted once that day's daily export completes. Confirm a table exists and row counts look sane before building anything on top.
6. Query the nested schema. Every event parameter and user property is a repeated record, so you `UNNEST` and filter on `key` to read a value. Cross-join the unnested array back to the base row. Patterns are in `references/unnest-event-params-patterns.md`.
7. Rebuild the metric you actually care about in SQL. Sessions, key event counts, and attribution are not pre-aggregated in the export; you compute them from `ga_session_id`, `event_name`, and the traffic-source records. Sessionization and attribution templates are in `references/sessionization-and-attribution-sql.md`.
8. Expect the export and the UI to differ, and know why before you explain it. Different processing, sampling in the UI, consent modeling in the UI but not the raw export, and (Not set) handling all move the numbers. The reconciliation checklist is in the pitfalls section and expanded in `references/daily-vs-streaming-schema.md`.

## Decision rules and thresholds

### Which export type

- Daily export: always turn this on. It is the source of truth for unsampled, complete data and is what nearly every downstream query reads.
- Streaming export: enable only when the use case needs data within minutes (operational dashboards, fast anomaly checks). It costs about 0.05 USD per gigabyte of exported data and can deliver the same event more than once, so you must dedupe. Do not use raw streaming rows for billing-grade counts without dedup.
- Fresh daily export (360 only): use when you want daily-quality completeness faster than the standard daily table, with batches typically arriving within about 60 minutes and available by roughly 5am property time. It is a 360 feature; do not promise it on a Standard property.

### Volume limits that change the plan

- Standard property daily export caps at up to 1M events per day. If the property is over that, the daily table is truncated and your counts silently undercount. Options: upgrade to 360 (20B events/day), reduce event volume, exclude high-volume low-value events from the export, or move the heavy analysis upstream. Never present a truncated Standard export as a complete count.
- 360 property daily export supports up to 20B events per day, and streaming has no stated volume cap (you still pay per gigabyte).

### Table selection

- Read `events_YYYYMMDD` for any finalized day. Use a wildcard with `_TABLE_SUFFIX` to scan a date range, and always bound the range so you do not scan the whole history and blow up the bill.
- Read `events_intraday_YYYYMMDD` only for the current, not-yet-finalized day, and know it is incomplete and will be replaced. Do not union intraday into historical reporting without deduping and without accepting it is provisional.
- If both daily and intraday exist for the same date during the handoff window, prefer the daily table; the intraday one is about to be deleted.

### Dedup rules

- Streaming and intraday rows can repeat. Deduplicate on the batch keys the export provides for this purpose: `batch_event_index`, `batch_page_id`, and `batch_ordering_id`, together with `event_timestamp`, `user_pseudo_id`, and `event_name`. The exact dedup pattern is in `references/unnest-event-params-patterns.md`.
- Daily tables are already finalized; you do not need batch dedup there, but you still de-dupe at the logical level (for example, one purchase per `transaction_id`).

### When BigQuery will not match the GA4 UI (expected, not a bug)

- The UI can sample large or complex queries; the daily export never samples. Expect the export to be higher and more stable.
- The UI applies consent modeling and thresholding; the raw export contains only observed hits, no modeled conversions. This gap widened after the June 2026 consent change gated ads-data flow on consent, so modeled UI conversions and raw export events can legitimately diverge. See `ga4-conversions-and-audiences` for the consent-gating detail.
- Cardinality collapse to (other) happens in the UI, not in the export, so high-cardinality dimensions look different.
- Timezone and late-arriving hits: the export is bucketed by the property timezone and can receive events up to about 72 hours late, so a day's table can still change slightly right after it lands.

## Reference material

- `references/daily-vs-streaming-schema.md`: the full field map of the GA4 export schema (top-level columns, the `event_params` / `user_properties` / `items` repeated records, and the `device` / `geo` / `traffic_source` / `session_traffic_source_last_click` / `ecommerce` / `privacy_info` records), plus a daily vs streaming vs fresh-daily comparison and the value-type sub-fields. Read this when you need to know a field name, whether it is repeated, or which export type has it.
- `references/unnest-event-params-patterns.md`: copy-ready SQL for pulling a single param, pulling many params in one pass, reading user properties and item arrays, deduping streaming rows on the batch keys, and safely scanning a date range with `_TABLE_SUFFIX`. Read this when you are writing the actual query.
- `references/sessionization-and-attribution-sql.md`: SQL to rebuild sessions from `ga_session_id`, count sessions and engaged sessions, count key events with consent and validity filters, and run last-non-direct and first-click attribution from `session_traffic_source_last_click` and `collected_traffic_source`. Read this when you need session, key-event, or attribution numbers from the raw export.

## Templates and examples

Pull a single event parameter (`page_location`) for one day, unsampled:

```sql
SELECT
  event_timestamp,
  user_pseudo_id,
  (SELECT value.string_value FROM UNNEST(event_params) WHERE key = 'page_location') AS page_location
FROM `my-project.analytics_123456789.events_20260615`
WHERE event_name = 'page_view';
```

Count a key event (`purchase`) across a bounded date range, one row per transaction:

```sql
SELECT
  COUNT(DISTINCT (SELECT value.string_value FROM UNNEST(event_params) WHERE key = 'transaction_id')) AS purchases,
  SUM(ecommerce.purchase_revenue) AS revenue
FROM `my-project.analytics_123456789.events_*`
WHERE _TABLE_SUFFIX BETWEEN '20260601' AND '20260615'
  AND event_name = 'purchase';
```

Rebuild session count for a day from the session id param:

```sql
SELECT
  COUNT(DISTINCT CONCAT(
    user_pseudo_id, '.',
    CAST((SELECT value.int_value FROM UNNEST(event_params) WHERE key = 'ga_session_id') AS STRING)
  )) AS sessions
FROM `my-project.analytics_123456789.events_20260615`;
```

The `analytics_<propertyId>` dataset name and the numeric property id are real placeholders you replace with your own; the property id is the same number shown in GA4 Admin.

## Common pitfalls

- Reading `event_params` as if they were columns. There is no `page_location` column; it is a key inside the repeated `event_params` record. Forgetting to `UNNEST` returns nothing or an error. Use the subquery-over-UNNEST pattern.
- Scanning `events_*` with no `_TABLE_SUFFIX` bound. This reads the entire history on every run and is the fastest way to burn the BigQuery bill. Always bound the date range.
- Treating streaming or intraday rows as final. They can duplicate and the intraday table is deleted after the daily export lands. Dedupe on the batch keys and prefer the daily table for finalized days.
- Assuming BigQuery equals the GA4 UI. It will not, and that is usually correct behavior (UI sampling, consent modeling, cardinality collapse, timezone and late hits). Explain the gap; do not "fix" it by mangling the SQL.
- Silent truncation on Standard over 1M events/day. The export just stops at the cap with no error in your query. Check property volume before you trust a Standard daily count.
- Counting `purchase` events instead of distinct `transaction_id`. Retries and re-fires double-count revenue. Dedupe on `transaction_id`.
- Wrong dataset region chosen at link time. The location is fixed for the dataset and constrains which tables you can join in one query. Decide the region before enabling the link, not after.
- Enabling the link without sign-off. It provisions a dataset and starts billable storage and (if streaming) per-gigabyte export cost. Treat enabling the export as a spend decision and get approval first.

## Sources

- [BigQuery Export (daily, streaming, fresh daily, limits)](https://support.google.com/analytics/answer/9358801?hl=en) (as of July 2026)
- [BigQuery Export schema](https://support.google.com/analytics/answer/7029846?hl=en) (as of July 2026)
- [GA4 Admin API v1 (properties.bigQueryLinks)](https://developers.google.com/analytics/devguides/config/admin/v1) (as of July 2026)
- [Data collection limits (event and parameter limits)](https://support.google.com/analytics/answer/9267744?hl=en) (as of July 2026)
