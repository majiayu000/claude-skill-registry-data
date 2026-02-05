---
name: cdp-lite-adapter
description: Adapt the User Explorer (CDP-lite) prototype to new data sources by mapping input exports to the build pipeline, updating adapters/enrichments, and preserving output JSON schemas for the UI. Use when asked to connect real data, replace inputs, or modify the build outputs/UI contracts.
---

# CDP-lite Adapter

## Overview

Map new data sources into the existing CDP-lite build pipeline while keeping output schemas stable for the UI.

## Workflow

1. Identify input formats and field names for activity + profiles.
2. Update adapters to normalize into the expected fields.
3. Adjust enrichments (score/segments) only if business rules change.
4. Run `make build` and validate `data/` outputs against the UI contract.

## Adapter Targets

- `scripts/adapters/activity.js`
  - Normalize to: email, date, login, total_views, unique_views, dashboard_name (optional)
- `scripts/adapters/profiles.js`
  - Normalize to: email, name, department, geo, title, manager_email, skip_level_email

## Output Contract

Preserve the output schemas in:
- `data/users/u_<sha1>.json`
- `data/index.json`
- `data/facets.json`
- `data/dashboards.json`

For field-level details, read `references/data-contract.md`.

## Notes

- Weekly activity must include every week from 2025-06-01 to today, Monday week start.
- Email is the primary key; always normalize to lowercase + trim.
- Keep `activity_score_bucket` in the index for filtering.
