---
name: ya-direct-statistics
description: Build, audit, explain, export, and safely operate Yandex Direct statistics reports, including Report Wizard, report library, saved reports, search queries, placements, regions, audiences, devices, ad assets, products, reach, apps, DOOH, conversion payments, invalid traffic, acts, and call logs. Use for Яндекс Директ reporting, filters, groupings, metrics, goals, attribution, VAT, comparisons, charts, downloads, and report troubleshooting; use a broader Yandex Direct skill for campaign creation or optimization outside statistics.
---

# Yandex Direct statistics

Use current official Yandex documentation and observable account state as the
technical truth. Product labels, report templates, available fields and
attribution options can change.

## Establish the report contract

Before building or interpreting a report, identify:

- advertiser, client login or agency/organization context;
- requested period, timezone and whether today is included;
- currency and VAT treatment;
- attribution model;
- goals and whether goal metrics are summed, separated or both;
- required groupings, metrics, filters and time detail;
- business question and source of truth for sales or revenue;
- whether the user wants inspection, a proposed report, a download or a saved
  report.

Do not infer unspecified revenue semantics. A configured goal value is not
proof of payment, and reports based on click date, conversion date, order date
or payment date are not interchangeable.

## Choose the reporting surface

- For a custom report or field-level analysis, read
  [report-builder.md](references/report-builder.md).
- For presets and special reports, read
  [report-library.md](references/report-library.md).
- For complex filters or field selection, read
  [filters-and-fields.md](references/filters-and-fields.md).
- For browser operation, saved reports, downloads or row actions, read
  [browser-safety.md](references/browser-safety.md).
- For current product behavior, consult
  [official-sources.md](references/official-sources.md).

Open only the references needed for the current request.

## Work read-only by default

Read-only work includes opening reports, choosing settings, reading tables and
explaining empty results. Treat authenticated access as access, not authority
to change advertising objects.

Require explicit authorization immediately before:

- saving, overwriting, renaming, duplicating, sharing or deleting a report;
- downloading advertiser data;
- adding search queries as negative keywords or keywords;
- blocking placements;
- navigating from a report into campaign edits and changing objects;
- invoking an external generative summary when data leaves the report context.

For an authorized mutation, show the exact target rows, destination object and
expected effect first. Re-read current state, apply the smallest approved
batch, record per-object results and stop on scope drift or partial failure.

## Build and validate

1. Open the correct account and confirm the report title.
2. Select the period and inclusion of today.
3. Select attribution, goals, goal display and VAT.
4. Add groupings, metrics and filters; preserve template-required fields.
5. Set time detail, table shape and comparison only when needed.
6. Wait for the current report state to load.
7. Verify every requested setting from the rendered report before reading
   values or downloading.
8. Distinguish a valid empty result from a loading or authorization error.

Prefer accessible roles and labels for browser selectors. Use stable test IDs
only when available. Do not rely solely on generated CSS classes, element
position, advertiser-specific values or temporary report-state IDs.

## Analyze without overclaiming

Keep dimensions distinct: campaign, group, ad, targeting condition, search
query, placement, device, geography, audience and time. Include numerator,
denominator, sample size, period, attribution and VAT basis in comparisons.

Separate:

- observed report data;
- calculated values;
- interpretation;
- unavailable data;
- proposed changes;
- actions actually executed.

When a template has hidden filters, report them. If a result is surprising,
inspect filters, goals, attribution, VAT, time basis, archived-object handling
and row granularity before concluding that the data is wrong.

## Handle sensitive data

Never place OAuth tokens, cookies, account exports, client logins, internal
IDs, personal data or production report payloads in prompts, commits, logs or
public artifacts. Let the user complete passwords and one-time codes through
the normal authentication UI.

## Report the outcome

State the report contract, exact settings, evidence, findings, limitations,
files downloaded or saved, and changes explicitly not made. If an operation
was authorized, include object-level results and rollback or recovery status.
