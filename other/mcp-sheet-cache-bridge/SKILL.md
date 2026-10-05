---
name: mcp-sheet-cache-bridge
description: Keep Zapier Tables or another MCP-connected record store as the source of truth while Google Sheets-based tools read an event-driven cache tab.
---

# MCP Sheet Cache Bridge

Use this skill when a team wants Zapier Tables to be the source of truth but still needs Google Sheets-based tools, scripts, dashboards, or exports to read a simple tab.

## What This Skill Does

1. Designs a cache tab schema that mirrors only the fields downstream tools need.
2. Builds an event-driven sync pattern from the source record store to Google Sheets.
3. Uses create, update, and delete logic keyed by a stable record ID.
4. Points legacy consumers at the cache instead of direct API reads.
5. Documents the field map and cutover plan so the sync stays maintainable.

## When You Need This Pattern

- A team replaced a multi-tab spreadsheet with Zapier Tables but still has Apps Script, Looker Studio, formulas, or exports reading Google Sheets.
- A Slack pinned digest or daily report needs fresh rows without running a scheduled full refresh.
- Scheduled syncs would create too many unnecessary tasks.
- Existing tools can read Google Sheets easily but do not have direct access to the source record store.
- The team wants one source of truth with a cheap, stable read path.

## Architecture

```text
Zapier Tables source of truth
  -> event-driven cache sync on record change
  -> Google Sheet cache tab
  -> Apps Script, Looker Studio, exports, or digests
```

## Required Connections Through Zapier MCP

- Zapier Tables or another approved record store: read record changes.
- Google Sheets: create, update, and delete cache rows.
- Optional Slack: post digest or sync-health summaries.

## Cache Sync Rules

| Source event | Cache action |
| --- | --- |
| Record matches active cache filter | Create or update matching row |
| Record no longer matches filter | Delete or clear matching row |
| Record deleted in source | Delete matching cache row |
| Cache schema changes | Pause sync until the field map is reviewed |

## Cache Tab Columns

| Column | Purpose |
| --- | --- |
| record_id | Source row ID or external join key |
| display_title | Subject, name, or primary label |
| status | Filter or workflow state |
| priority | Sort order for digest or dashboard |
| assignee | Owner or responsible team |
| link | Source record, ticket, or Slack permalink |
| updated_at | Last sync timestamp |

## Task Budget Pattern

| Pattern | Approximate task impact |
| --- | --- |
| Cache sync on record change | One sync run per relevant source change |
| Scheduled full-table sync every 5 minutes | Hundreds of unnecessary runs per day |
| Apps Script read of cache tab | No Zapier task usage for the read path |

## Zapier MCP And SDK Role

- Use Zapier MCP to read source record changes and update Google Sheets cache rows.
- Use Zapier SDK when the pattern becomes repeatable: schema map validation, idempotent upsert handling, sync logging, retry handling, and health alerts.
- Keep destructive sync actions behind approval until the team trusts the mapping.

## Guardrails

- Do not run scheduled full-table syncs unless the team explicitly accepts the task cost.
- Do not store private API tokens in Apps Script if the cache solves the read path.
- Do not delete production cache tabs without explicit approval.
- Do not disable legacy read paths until cutover is verified.
- Keep schema changes documented in both the source table and cache map.

## Inspired By

Generalized from a public workflow by Kenny Taber. The public writeup names Kenny and does not name the company.
