---
name: ga4-apis-and-measurement-protocol
description: Automate GA4 reporting and configuration and send server-side events with code. Use when the user asks how to pull GA4 data through the Data API v1 (runReport, runPivotReport, runRealtimeReport, batchRunReports, getMetadata, checkCompatibility, funnel or audience exports), manage a property through the Admin API v1 (create key events, custom dimensions, data streams, Measurement Protocol secrets, Google Ads links), send server-side or offline events with the Measurement Protocol, validate events on the debug endpoint, hits a Data API quota or a 25-event Measurement Protocol limit, or asks why UI numbers do not match an API pull.
---

# GA4 APIs and Measurement Protocol

Drive GA4 with code instead of the UI: pull reports at scale through the Data API v1, read and write property configuration through the Admin API v1, and send server-to-server or offline events through the Measurement Protocol. This is the automation layer under GA4. When a task means "do this a thousand times", "on a schedule", "in a pipeline", or "from a server", it lives here.

This skill assumes you know sessions, events, key events, and CPA/ROAS math. For those, see the `programmatic-foundations` skill. GA4 uses key events, not "conversions", and this skill uses that term throughout.

## When to use this skill

- "Pull GA4 data through the Data API." / "runReport / runPivotReport / runRealtimeReport / batchRunReports."
- "List available dimensions and metrics." / "getMetadata / checkCompatibility before I build a report."
- "Build a funnel report or an audience export through the API."
- "Create a key event / custom dimension / data stream / Google Ads link through the Admin API."
- "Generate a Measurement Protocol secret." / "Send a server-side or offline event to GA4."
- "Validate my Measurement Protocol payload." / "Why did my event not show up?"
- "I hit a Data API quota (RESOURCE_EXHAUSTED)." / "How many tokens does a report cost?"
- "Why does my API pull not match the GA4 UI number?"

Boundaries with sibling skills:
- Standing up the property, data streams, retention, reporting identity in the UI: `ga4-property-and-data-stream-setup`.
- Designing the event model and defining which events are key events (the concept): `ga4-events-and-key-events`.
- Building audiences and exporting them and key events to ad platforms, plus the June 2026 consent change: `ga4-conversions-and-audiences`.
- Explore workspace analyses, sampling, and the attribution model in the UI: `ga4-explorations-and-reporting`.
- The BigQuery export and SQL against the raw nested event schema (a different, unsampled path to the same data): `ga4-bigquery-export-and-sql`.
- Consent Mode v2 signals and default-vs-update ordering that decide whether events even collect: `gtm-consent-mode-v2`.
- Reconciling API-derived counts against CM360 and the DSPs: `cross-platform-conversion-reconciliation`.

## Quick reference

Pick the surface from the job, not from habit.

| Job | Surface | Method or endpoint | Why |
| --- | --- | --- | --- |
| Read aggregated report data on a schedule | Data API v1 | `runReport`, `batchRunReports` | Server-side, quota-metered, unattended |
| Pivot table with column groupings | Data API v1 | `runPivotReport` | Only method that returns pivots |
| Last 30 minutes of activity | Data API v1 | `runRealtimeReport` | Realtime is a separate quota category |
| Discover valid dimensions and metrics | Data API v1 | `getMetadata` | Names change per property (custom dims) |
| Check a dimension and metric combine | Data API v1 | `checkCompatibility` | Avoids INVALID_ARGUMENT before you run |
| Funnel completion through steps | Data API v1 | `runFunnelReport` (alpha) | UI-parity funnel from code |
| Snapshot audience membership | Data API v1 | `properties.audienceExports` (alpha) | Get user list for a saved audience |
| Create a key event or custom dimension | Admin API v1 | `properties.keyEvents.create`, `properties.customDimensions.create` | Write config at scale |
| Generate a server-side event secret | Admin API v1 | `...measurementProtocolSecrets.create` | Required to authorize MP events |
| Send an offline or server event | Measurement Protocol | POST `/mp/collect` | Only path for server-to-server hits |
| Test an event before sending live | Measurement Protocol | POST `/debug/mp/collect` | Production `/mp/collect` never validates |

Three distinct systems, three auth models:
- Data API and Admin API: OAuth 2.0 or a service account with the Analytics scope. Read (Data API) and read/write (Admin API) property configuration and data.
- Measurement Protocol: an `api_secret` bound to a data stream, passed as a query parameter. Write-only event ingestion. No OAuth.

## Core process

### Reporting through the Data API v1

1. Resolve the numeric property ID (the digits, not `G-XXXXXXXXXX`). Every Data API call targets `properties/{propertyId}`, so an alphanumeric Measurement ID here fails.
2. Call `getMetadata` first when a property has custom dimensions or metrics, because their API names (`customEvent:promo_id`, `customUser:loyalty_tier`) are property-specific and you cannot guess them.
3. Call `checkCompatibility` for any non-obvious dimension and metric pairing before building the full request, so you catch an incompatible combination as a fast, cheap call instead of a failed `runReport`.
4. Build the request: `dateRanges`, `dimensions`, `metrics`, and optional `dimensionFilter`, `metricFilter`, `orderBys`, `limit`, `offset`. Use `batchRunReports` when you need several reports for one property, because batching shares one HTTP round trip and is quota-friendlier than serial calls.
5. Page through results with `limit` and `offset` when `rowCount` exceeds what one response returns (the API caps rows per response). Loop until you have all rows.
6. Read the response defensively: check `metadata.dataLossFromOtherRow` (an `(other)` row absorbed high-cardinality values) and any sampling metadata before trusting totals. If either flags, the raw truth is in the BigQuery export (`ga4-bigquery-export-and-sql`).

### Configuration through the Admin API v1

1. Read before you write. `properties.get`, `dataStreams.list`, `keyEvents.list`, `customDimensions.list` show current state, so a create call does not collide with an existing resource.
2. Use the current resource names. The `keyEvents` resource replaced `conversionEvents`; write against `keyEvents`. Custom dimensions and metrics are separate resources with hard per-property caps (see Decision rules).
3. Create Measurement Protocol secrets under the data stream, not the property: `properties/{p}/dataStreams/{s}/measurementProtocolSecrets`. The returned `secretValue` is the `api_secret` your event sender uses.
4. Gate every write. Creating a key event changes what Google Ads can import and bid on; creating a Google Ads link changes data flow. Treat Admin API writes as production changes and confirm with a human before running them.

### Server-side events through the Measurement Protocol

1. Get two credentials: the stream's Measurement ID (`G-XXXXXXXXXX`) for web or the `firebase_app_id` for app, and an `api_secret` from an Admin API Measurement Protocol secret.
2. Build the payload: a `client_id` (web) or `app_instance_id` (app) that matches the on-device gtag/SDK identifier, and an `events` array where each event has a `name` and a `params` object. Add `user_id` and `consent` where you have them.
3. Validate on the debug endpoint first. POST to `https://www.google-analytics.com/debug/mp/collect` and read `validationMessages`. This is the only place GA4 tells you a payload is wrong, because production `/mp/collect` returns a 2xx for a broken payload and silently drops it.
4. Send to production only after the debug response returns an empty `validationMessages`. POST to `https://www.google-analytics.com/mp/collect` (or `https://region1.google-analytics.com/mp/collect` for EU-region collection).
5. Reconcile in Realtime and DebugView. A correctly sent event appears in `runRealtimeReport` and, if you added `debug_mode`, in DebugView. If it never appears, the payload was silently dropped and you missed it in step 3.

## Decision rules and thresholds

### Data API quotas (get these right before you build a pipeline)

Quotas are per property and split into three independent categories: Core, Realtime, and Funnel. A `runReport` charges Core; a `runRealtimeReport` charges Realtime. Standard vs 360 limits:

| Quota | Standard | 360 |
| --- | --- | --- |
| Tokens per property per day | 200,000 | 2,000,000 |
| Tokens per property per hour | 40,000 | 400,000 |
| Tokens per project per property per hour | 14,000 | 140,000 |
| Concurrent requests per property | 10 | 50 |
| Server errors per project per property per hour | 10 | 50 |

Token cost per request is not fixed. It scales with date range, number of dimensions, filter complexity, and data cardinality, so a 90-day, high-cardinality report can cost many multiples of a 1-day summary. Read `propertyQuota` in every response to see remaining tokens and back off before you hit `RESOURCE_EXHAUSTED`. Daily quotas reset at midnight Pacific. Rule of thumb: widen date ranges and reduce request count with `batchRunReports` rather than firing many small serial reports, and cache metadata rather than calling `getMetadata` on every run.

### Measurement Protocol hard limits

| Limit | Value |
| --- | --- |
| Events per request | 25 |
| Parameters per event | 25 |
| User properties per request | 25 |
| Event name length | 40 characters |
| Parameter name length | 40 characters |
| Parameter value length | 100 (Standard), 500 (360) |
| User property name length | 24 characters |
| User property value length | 36 characters |
| POST body size | Under 130 kB |
| Backdating window (`timestamp_micros`) | 72 hours |

`timestamp_micros` is Unix epoch in microseconds, not milliseconds. An event older than 72 hours is dropped. Event names must start with a letter and use only letters, numbers, and underscores, and the prefixes `firebase_`, `ga_`, and `google_` are reserved. Reserved event and parameter names (`session_start`, `first_visit`, `user_engagement`, and others) are rejected. The full reserved list and the field map are in `references/measurement-protocol-limits.md`.

### Admin API configuration caps

Per-property caps are enforced by the API, so plan the taxonomy before you create resources: event-scoped and user-scoped custom dimensions and custom metrics each have a fixed maximum, and key events have their own cap. Hitting a cap returns an error on create, not a silent truncation. Design the dimension set once (in `ga4-events-and-key-events`) rather than creating dimensions ad hoc through the API and running out.

### When API totals will not match the UI

- Sampling: high-complexity Explore queries sample; most Data API core reports do not, so an API number can legitimately exceed a sampled UI number.
- `(other)` row: when a dimension exceeds its cardinality limit, low-frequency values collapse into `(other)`. Check `dataLossFromOtherRow` in the response.
- Attribution and identity: the API respects the property's reporting identity and attribution model, so a mismatch often traces to a different identity space, not a bug.
- Freshness: the Data API can lag the UI by hours for the current day. Compare closed days, not today.
- For byte-exact, unsampled truth, leave the reporting APIs and query the BigQuery export (`ga4-bigquery-export-and-sql`).

### Consent and legal posture

The Measurement Protocol lets a server send events GA4 would otherwise never see, which makes consent your responsibility, not the browser's. Set the `consent` object (`ad_user_data`, `ad_personalization`) on MP payloads and only send events for users whose consent you have recorded. Consent Mode v2 requires `ad_storage`, `analytics_storage`, `ad_user_data`, and `ad_personalization`, and a June 2026 change gates ads-data flow on consent, so a server bypass that ignores consent is both a data-quality and a legal problem. For the consent framework and signal wiring, see `gtm-consent-mode-v2` and `privacy-and-consent`.

## Reference material

- `references/data-api-methods-and-quotas.md`: every Data API v1 method with its request and response shape, the dimension/metric filter grammar, pagination and `batchRunReports` patterns, the full quota table with token-cost drivers, and the common error codes (`INVALID_ARGUMENT`, `PERMISSION_DENIED`, `RESOURCE_EXHAUSTED`). Read this when building or debugging a report pull.
- `references/admin-api-resources.md`: the Admin API v1 resource tree, the create/list/patch/delete method map per resource, the `keyEvents`-replaced-`conversionEvents` change, required fields for key events, custom dimensions and metrics, data streams, Measurement Protocol secrets, and Google Ads links, plus the per-property caps. Read this when reading or writing property configuration.
- `references/measurement-protocol-limits.md`: the exact endpoint URLs, required query params and body fields for web vs app, the full limits table, the reserved event and parameter names and prefixes, the `consent` object fields, the debug-endpoint `validationMessages` codes, and a worked payload. Read this when building or validating a server-side event sender.

## Templates and examples

Data API `runReport` request body (sessions and key events by channel, last 28 days):

```json
{
  "dateRanges": [{ "startDate": "28daysAgo", "endDate": "yesterday" }],
  "dimensions": [{ "name": "sessionDefaultChannelGroup" }],
  "metrics": [{ "name": "sessions" }, { "name": "keyEvents" }],
  "orderBys": [{ "metric": { "metricName": "sessions" }, "desc": true }],
  "limit": 100
}
```

Admin API create a key event (mark `generate_lead` as a key event):

```
POST https://analyticsadmin.googleapis.com/v1beta/properties/123456789/keyEvents
{ "eventName": "generate_lead", "countingMethod": "ONCE_PER_EVENT" }
```

Measurement Protocol offline `purchase` event (validate first, then send):

```
POST https://www.google-analytics.com/debug/mp/collect?measurement_id=G-XXXXXXXXXX&api_secret=YOUR_SECRET
{
  "client_id": "1993.1735689600",
  "timestamp_micros": 1751414400000000,
  "consent": { "ad_user_data": "GRANTED", "ad_personalization": "DENIED" },
  "events": [{
    "name": "purchase",
    "params": {
      "transaction_id": "T-10492",
      "currency": "USD",
      "value": 129.00,
      "items": [{ "item_id": "SKU-88", "item_name": "Trail Shoe", "price": 129.00, "quantity": 1 }]
    }
  }]
}
```

Read `validationMessages` in the debug response. Empty array means the payload is valid; then repost to `/mp/collect` (no `/debug`) to record it.

## Common pitfalls

- Using the Measurement ID as the property ID. Data API calls need the numeric property ID (`123456789`); `G-XXXXXXXXXX` is the stream Measurement ID for the Measurement Protocol. Swapping them is the most common first failure.
- Trusting `/mp/collect` because it returned 200. Production never validates and returns 2xx for garbage. Validate on `/debug/mp/collect` and only trust an empty `validationMessages`.
- Backdating past 72 hours. Offline events with a `timestamp_micros` older than three days are dropped with no error. Send within the window or accept the loss.
- Silent quota exhaustion. Firing many small serial `runReport` calls burns hourly tokens fast. Batch reports, cache `getMetadata`, read `propertyQuota`, and back off before `RESOURCE_EXHAUSTED`.
- Writing to `conversionEvents`. That resource is replaced; write key events against the `keyEvents` resource or the call fails or targets a deprecated path.
- Sending MP events without consent signals. A server can push events the browser suppressed, which breaks Consent Mode and creates legal exposure. Set the `consent` object and only send for consented users.
- Comparing today's API pull to the UI. The Data API lags for the current day. Reconcile on closed days, and for exact figures use the BigQuery export.
- Guessing custom dimension API names. `customEvent:` and `customUser:` names are property-specific. Pull them from `getMetadata`, do not hardcode from memory.

## Sources

- [Analytics Data API v1 overview](https://developers.google.com/analytics/devguides/reporting/data/v1) (as of July 2026)
- [Data API v1 quotas](https://developers.google.com/analytics/devguides/reporting/data/v1/quotas) (as of July 2026)
- [Analytics Admin API v1 overview](https://developers.google.com/analytics/devguides/config/admin/v1) (as of July 2026)
- [Measurement Protocol for GA4 overview](https://developers.google.com/analytics/devguides/collection/protocol/ga4) (as of July 2026)
- [Sending Measurement Protocol events](https://developers.google.com/analytics/devguides/collection/protocol/ga4/sending-events) (as of July 2026)
- [Measurement Protocol reference and limitations](https://developers.google.com/analytics/devguides/collection/protocol/ga4/reference) (as of July 2026)
- [Validating Measurement Protocol events](https://developers.google.com/analytics/devguides/collection/protocol/ga4/validating-events) (as of July 2026)
- [BigQuery export schema](https://support.google.com/analytics/answer/9358801?hl=en) (as of July 2026)
- [About key events](https://support.google.com/analytics/answer/9267568?hl=en) (as of July 2026)
