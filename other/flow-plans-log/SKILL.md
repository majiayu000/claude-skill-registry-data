---
name: flow-plans-log
description: Append a row to the Flow Plans Tracker whenever a new flow doc / master plan / process doc / how-to / niche strategy doc is created. Auto-rule, never skip. Do not use for new spreadsheets or tabs (use /sheets-hub-log).
---

# Flow Plans Tracker Logger

## When to use (MANDATORY)
- New flow doc (video flow, capture flow, content pipeline, carousel lessons, website plan)
- New master plan or process doc
- New niche strategy doc (Brazil, OPC, McFolling, etc.)
- New how-to doc

## When NOT to use
- New spreadsheet or new tab → use `/sheets-hub-log` (different target)
- New captured content ideas → those go to Inspiration Library, not here

## Target
- Spreadsheet: **Flow Plans Tracker — Master Index**
- ID: `1fggy918FgPfnMQ-dzGQk2zx9uhi2_-uWXMKGW4MA47k`
- Location: Marketing > Claude Code Workspace
- Link: https://docs.google.com/spreadsheets/d/1fggy918FgPfnMQ-dzGQk2zx9uhi2_-uWXMKGW4MA47k

## Tab to update (pick based on doc type + ALSO always add to All Docs)
- `Flow Plans` — process / how-to docs
- `Niche Plans` — niche-specific strategy docs
- `All Docs` — EVERY doc (master index) — ALWAYS add here too

## Columns for All Docs tab (in this exact order)
| NAME | TYPE | NICHE | STATUS | DESCRIPTION | OPEN | DOC_ID | TABS | LAST UPDATED |

## Execute
Route A (preferred) — Sheets API via OAuth (SHEETS_TOKEN):
```
POST https://sheets.googleapis.com/v4/spreadsheets/1fggy918FgPfnMQ-dzGQk2zx9uhi2_-uWXMKGW4MA47k/values/All Docs!A:I:append?valueInputOption=USER_ENTERED
Body: {"values": [[name, type, niche, status, description, open_url, doc_id, tabs, last_updated]]}
```
Working Python pattern: `~/.claude/scripts/add_inbox_task.py`.

Route B — Composio `GOOGLESHEETS_APPEND_ROW`.

## Service account note
The 4AM agent reads this tab. For the agent to read the doc's content, share the doc with `oak-park-sheets@gen-lang-client-0364933181.iam.gserviceaccount.com`.

## After appending
Confirm: `✅ Logged to Flow Plans Tracker: <doc name> (<tab>)`

## Why this matters
This is the 4AM agent's manifest. The agent reads this tab nightly to detect plan changes and propagate rules. Skipping a log means the agent never sees the doc.
