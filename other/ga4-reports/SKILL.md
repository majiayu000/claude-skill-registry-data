---
name: ga4-reports
description: >-
  Pull and explain Google Analytics 4 reports — traffic by source and channel, period comparisons, daily breakdowns, conversion events, signup and purchase funnels — through the GA4 MCP server, with a REST fallback when the MCP hangs. Knows the GA4 reporting traps (cross-day attribution, users vs events, Ads vs GA date mismatch). Use when someone asks about website traffic, GA4, sessions, conversions, funnel drop-off or channel performance. Triggers: "pull GA4", "traffic last month", "conversions by source", "funnel report", "Google Analytics".
---

# GA4 reports

Reports from Google Analytics 4 through the official GA4 MCP server (`mcp__google-analytics__*` or similar tools), or through `scripts/ga4.py` when the MCP is broken. Both use the same Google login and the same query JSON.

Setup (one time): `connections/ga4-mcp.md`, or run the `connect` skill.

## Before the first report: know the funnel

GA4 data is only as useful as your event map. Read `references/funnel-map.md`. If the user's copy is still the template, ask them for their key events (or list the events from the last 30 days by `eventName` and ask which ones matter), then fill it in and save it. Do this once; every later report uses it.

## Auth

The MCP and the script both use Google Application Default Credentials.

1. If a call fails with `Reauthentication is needed`, `401` or `invalid_grant`, the login expired. Run the login from `connections/ga4-mcp.md` **in the background** (it opens a browser) and tell the user: "A browser window opened — sign in with the Google account that has GA4 access."
2. Wait for the command to finish, then retry. Check with the account-summaries tool or `python3 ${CLAUDE_SKILL_DIR}/scripts/ga4.py --list-properties`.

If Google says **"This app is blocked"**, the default gcloud client is blocked for these scopes on the user's Workspace — the fix (your own OAuth client) is in `connections/ga4-mcp.md`.

## Running reports

### The rules the API enforces

- `dimensions` is always required — the API errors without it. `date_range` is not a dimension.
- For people counts use `totalUsers` (unique users), not `eventCount` (raw events), unless the user asks for events.

### Period comparison

```json
{
  "dimensions": ["month"],
  "date_ranges": [
    {"start_date": "2026-03-01", "end_date": "2026-03-31", "name": "march"},
    {"start_date": "2026-02-01", "end_date": "2026-02-28", "name": "february"}
  ],
  "metrics": ["sessions", "totalUsers", "newUsers", "engagedSessions", "averageSessionDuration", "conversions"]
}
```

GA returns rows for both ranges — drop zero-value rows for a clean table.

### Daily breakdown

```json
{
  "dimensions": ["date"],
  "date_ranges": [{"start_date": "28daysAgo", "end_date": "yesterday"}],
  "metrics": ["sessions", "totalUsers"],
  "order_bys": [{"dimension": {"dimension_name": "date"}, "desc": false}]
}
```

### One source or channel

```json
{"dimension_filter": {"filter": {"field_name": "sessionSource",
  "string_filter": {"match_type": "CONTAINS", "value": "linkedin", "case_sensitive": false}}}}
```

```json
{"dimension_filter": {"filter": {"field_name": "sessionDefaultChannelGroup",
  "string_filter": {"match_type": "EXACT", "value": "Paid Search"}}}}
```

### Funnel steps

Query `eventName` with `totalUsers`, filtered to the events in your funnel map (`in_list_filter`), then compute step-to-step conversion yourself.

## REST fallback

If the MCP's `run_report` times out (`504 Deadline Exceeded`) while lighter tools work, or the server isn't connected: **don't debug the MCP — switch to the script.** It's usually 1–2 seconds per query.

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/ga4.py --property <PROPERTY_ID> query.json --out raw/ga4/<name>.json
```

It accepts the same snake_case JSON as the MCP, prints a table and saves the raw response. Property id from `--property` or the env var `GA4_PROPERTY_ID`. Several queries → run them sequentially in one Bash call.

## Reporting rules

- **Lead with the configured conversion events** (form submitted, meeting booked, purchase), not raw step-view events. A funnel built from page views and CTA clicks looks alarming ("87 opened the form, 11 passed step one — the form is broken") when the real conversions are fine. Curiosity clicks are not failures.
- **Reconcile with the ad platform** when the user has it. Google Ads and GA4 mostly agree, with ±1–2 a day of difference: **Ads attributes a conversion to the click date, GA4 logs it on the event date.** Say this before anyone calls it a tracking bug.
- **Cross-day steps can exceed 100%.** A user can open a page on Monday and convert on Tuesday, so within a date range step B / step A can be over 100%. Mark it with an asterisk; don't "fix" the number.
- **Don't compute lagging conversions inside one period** (trial → first payment, lead → deal). The numerator and the denominator are different people. That needs a cohort view — say so instead.
- **Today and yesterday are incomplete.** If the last days dip, note it in one line under the table, not as a finding.
- **Combine split sources.** LinkedIn arrives as `linkedin` and `linkedin.com`; Facebook as several sources. Sum them and say you did.
- `averageSessionDuration` is in seconds. Money metrics follow the property currency.
- Answer exactly what was asked. No "insights", "next steps" or extra channel overviews unless requested.

## Adapt it

- Fill in `references/funnel-map.md` — it turns this skill from generic into yours.
- If you need the same report every week, ask the agent to write it as a script once and run the script on a schedule. A stable report doesn't need an agent every time.
