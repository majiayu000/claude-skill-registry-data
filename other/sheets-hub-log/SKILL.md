---
name: sheets-hub-log
description: Append a row to the Spreadsheet Hub whenever a new spreadsheet is created OR a new tab is added to an existing spreadsheet. This is an automatic rule — never skip it. Do not use for logging flow docs (use /flow-plans-log).
---

# Spreadsheet Hub Logger

## When to use (MANDATORY — never skip)
- A new Google Sheet is created (by any skill or script)
- A new tab is added to an existing Google Sheet
- Priscila says "I added a tab" or "I made a new sheet"

## When NOT to use
- Flow docs / master plans / process docs → use `/flow-plans-log` (different spreadsheet)
- Reading the Hub → call Sheets API directly

## Target
- Spreadsheet: **Spreadsheet Hub**
- ID: `1qDbO6JQX0cKbZ9rHjiM7a4U_p7OOddZ3k3Sp30JJoqo`
- Location: Marketing > Resource Hub
- Link: https://docs.google.com/spreadsheets/d/1qDbO6JQX0cKbZ9rHjiM7a4U_p7OOddZ3k3Sp30JJoqo

## Columns (in this order — one row per tab)
| SPREADSHEET | TAB | PURPOSE | LINK | SPREADSHEET ID |

## Execute
Route A (preferred) — Sheets API via OAuth (SHEETS_TOKEN):
```
POST https://sheets.googleapis.com/v4/spreadsheets/1qDbO6JQX0cKbZ9rHjiM7a4U_p7OOddZ3k3Sp30JJoqo/values/Sheet1!A:E:append?valueInputOption=USER_ENTERED
Body: {"values": [["<sheet name>", "<tab name>", "<purpose>", "<link>", "<sheet id>"]]}
```
Working Python pattern: `~/.claude/scripts/add_inbox_task.py` (same OAuth + append idiom — swap sheet/range).

Route B — Composio `GOOGLESHEETS_APPEND_ROW`.

## Service account
If writing from a GitHub Action or server-side context, use: `oak-park-sheets@gen-lang-client-0364933181.iam.gserviceaccount.com` — already shared on the Hub.

## After appending
Confirm: `✅ Logged to Spreadsheet Hub: <sheet> / <tab>`

## Why this matters
The Hub is the source of truth for every tab that exists. Skipping a log means future sessions can't find a tab they need to reference.
