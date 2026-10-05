---
name: session-start
description: Run the start-of-session checklist — Calendar + Inbox + Chat Logs + bypass question. Use at the very beginning of a chat, or after context reset, or when Priscila says "morning" / "let's start" / "what do I have today". Do not use mid-task.
---

# Session Start Checklist

## When to use
- First message of a new chat
- User says "morning", "let's start", "what's on today", "where did we leave off"
- After a context compression / fresh session

## When NOT to use
- Mid-task
- User already gave a specific task
- Same-session repeat

## Steps (run in order — all routes have fallbacks, never give up)

### 1. Calendar — today's tasks
- Route A: `mcp__claude_ai_Google_Calendar__gcal_list_events` (load via ToolSearch first — deferred tool)
- Route B: Composio `GOOGLECALENDAR_FIND_EVENT`
- Route C: Python OAuth — `build('calendar','v3',credentials=creds).events().list(calendarId='primary', timeMin=today, timeMax=tomorrow).execute()` using `~/ClaudeWorkspace/Credentials/sheets_token.json`
- Filter: events NOT starting with "DONE"
- Count: X pending tasks

### 2. Inspiration Library — pending captures
- Spreadsheet ID: `1IrFrCNGVIF7cvAr9cIuAXvCtUR_-eQN1mdCpHXpfbcU`
- Tab: `Inspiration Library`
- Route A: Google Sheets API via OAuth (SHEETS_TOKEN)
- Route B: Composio `GOOGLESHEETS_BATCH_GET`
- Count rows with Status = `NEEDS_REVIEW` or blank

### 3. Chat Logs — yesterday's log
- Folder ID: `1qitnbz5_8tfZI2rnTogV1zLLLLOwFVCw`
- Route: Drive MCP `mcp__claude_ai_Google_Drive__search_files` (q: parents has folder + name contains yesterday's date)
- Read summary if found

### 4. Report in this format
```
✅ Session ready
- X calendar tasks pending (top 3: …)
- Y inbox items need /capture
- Last session: [date] — [one-line summary from log]
```

### 5. Ask bypass question (exact text — see CLAUDE.md SESSION PERMISSIONS)

## Reference scripts (reuse, do not rewrite)
- Calendar logic pattern: `~/.claude/scripts/eod_checker.py` (reads Calendar via OAuth)
- Sheets read pattern: `~/.claude/scripts/add_inbox_task.py`
- Full routing rules: `~/.claude/projects/-Users-priscilahigashi/memory/reference_active_connections.md`

## Notes
- If a route fails, immediately try next route — never report "blocked" until all 3 tried
- Calendar MCP and Drive MCP are DEFERRED tools — load schemas via ToolSearch before calling
