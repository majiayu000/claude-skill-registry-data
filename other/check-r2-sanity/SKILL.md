---
name: check-r2-sanity
description: Run a deterministic, read-only quality audit of Apple Health and Health Auto Export JSON archived in the project's private Cloudflare R2 bucket. Use when the user invokes /check-r2-sanity or $check-r2-sanity, asks whether an R2 health export is complete or suitable for backfilling, compares export settings/providers, or wants metric coverage, workout-detail, duplicate, timestamp, parse, and temporal-consistency checks without exposing private health values.
---

# Check Health R2 Sanity

Audit `health-raw-data` without modifying Cloudflare state. This exact bucket name is hardcoded in the script and cannot be supplied through arguments or environment variables:

```sh
node .codex/skills/check-r2-sanity/scripts/check-r2-sanity.mjs
```

When the intended backfill interval is known, make completeness testable:

```sh
node .codex/skills/check-r2-sanity/scripts/check-r2-sanity.mjs --expected-start YYYY-MM-DD --expected-end YYYY-MM-DD
```

The script freezes a timestamped R2 inventory, downloads each exact object with Wrangler into a mode-`0700` temporary directory, emits aggregate-only JSON, and removes all temporary bodies. It never prints health values, payload fragments, workout names, GPS coordinates, or object keys.

Use the report to assess:

- inventory and JSON/envelope integrity;
- observed payload-date coverage rather than receipt timestamps;
- metric breadth, units, metric-aware numeric rows (including summarized sleep fields), row/source/timestamp coverage, and core-metric presence;
- workout IDs, duplicate deliveries, summary-only versus actual nested series;
- workout-series and route timestamps outside declared workout intervals;
- duplicate raw payload digests.

Interpret `fail` as unsuitable for replacement/backfill until resolved. Interpret `warn` in context: summary-only workout deliveries and sparse metrics are valid evidence, but may not meet the current experiment's detail goal. Compare the complete report with the prior candidate or baseline; do not decide from bytes, receipt times, or export labels alone.

Observed sample dates prove payload coverage, not that an exporter attempted every calendar day. Use the expected interval as a strict experiment gate only when the chosen export should contain daily metric observations. Per-metric gaps, duplicate rows, unit drift, and missing workout IDs are warnings because their acceptability depends on metric cadence and the backfill transform's deduplication rules.

For local parser verification only:

```sh
node .codex/skills/check-r2-sanity/scripts/check-r2-sanity.mjs --input-dir workers/health-ingest/test/fixtures
```

Do not upload, delete, transform, deploy, or write D1 as part of this skill.
