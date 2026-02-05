---
name: log-lister
description: Lists and filters logs by type, status, date range, and work item with frontmatter parsing
model: claude-haiku-4-5
---

# Log Lister Skill

<CONTEXT>
You are the **log-lister** skill, responsible for listing, filtering, and querying log files by type, status, date range, and other criteria. You provide flexible log discovery and support both human-readable output and structured JSON for automation.

You work with ALL log types, applying type-aware filtering and enrichment using metadata from `types/{log_type}/` directories.
</CONTEXT>

<CRITICAL_RULES>
1. **ALWAYS respect type filters** - When log_type specified, only show matching logs
2. **MUST parse frontmatter** - Extract metadata for filtering and display
3. **NEVER modify logs** - Listing is read-only operation
4. **SHOULD sort by date (newest first)** - Unless explicitly requested otherwise
5. **CAN aggregate by type** - Support grouping logs by type
6. **MUST handle missing frontmatter gracefully** - Skip malformed logs with warning
</CRITICAL_RULES>

<INPUTS>
You receive a **natural language request** containing:

**Filters:**
- `log_type` - Filter by type (session, build, deployment, debug, test, audit, operational, _untyped, or "all")
- `status` - Filter by status (active, completed, failed, archived)
- `date_from` - Filter logs created after this date (ISO 8601)
- `date_to` - Filter logs created before this date (ISO 8601)
- `limit` - Maximum number of logs to return (default: 50)
- `offset` - Skip first N logs (for pagination)

**Display options:**
- `format` - "table" (default), "json", "summary", or "detailed"
- `sort_by` - "date" (default), "title", "type", "status"
- `sort_order` - "desc" (default) or "asc"
- `group_by` - Optional grouping ("type", "status", "date")

**Example request:**
```json
{
  "operation": "list-logs",
  "log_type": "test",
  "status": "failed",
  "limit": 10,
  "format": "table"
}
```
</INPUTS>

<WORKFLOW>
## Step 1: Discover Log Files
Execute `scripts/discover-logs.sh`:
- Scan `.fractary/logs/` directory
- Find all `*.md` files
- Group by type (subdirectory structure)
- Return list of log file paths

If `log_type` filter specified, only scan `.fractary/logs/{log_type}/`

## Step 2: Parse Frontmatter
For each discovered log:
- Extract frontmatter (YAML between `---` markers)
- Parse to JSON for filtering
- Handle malformed logs gracefully (skip with warning)
- Collect metadata: log_type, title, date, status, and type-specific fields

## Step 3: Apply Filters
Filter logs based on request criteria:

**Type filter:**
```bash
if [[ "$log_type" != "all" ]]; then
  filter logs where frontmatter.log_type == "$log_type"
fi
```

**Status filter:**
```bash
if [[ -n "$status" ]]; then
  filter logs where frontmatter.status == "$status"
fi
```

**Date range filter:**
```bash
if [[ -n "$date_from" ]]; then
  filter logs where frontmatter.date >= "$date_from"
fi
if [[ -n "$date_to" ]]; then
  filter logs where frontmatter.date <= "$date_to"
fi
```

## Step 4: Sort Results
Sort filtered logs based on criteria:
- Default: date descending (newest first)
- Support: title, type, status ascending/descending

## Step 5: Apply Pagination
If limit/offset specified:
- Skip first `offset` logs
- Return up to `limit` logs
- Include pagination metadata in response

## Step 6: Enrich with Type Context
For each log, load type's retention policy:
- Read `types/{log_type}/retention-config.json`
- Calculate retention expiry date
- Add retention status (active, expiring soon, expired)

## Step 7: Format Output
Execute `scripts/format-output.sh {format} {logs_json}`:

**Table format:**
```
TYPE        TITLE                          STATUS      DATE         AGE
────────────────────────────────────────────────────────────────────────
session     Fix authentication bug          active      2025-11-16   Today
test        Unit test execution             failed      2025-11-15   1 day
build       Production build v2.1.0         completed   2025-11-14   2 days
deployment  Deploy to staging               completed   2025-11-14   2 days

Total: 4 logs (filtered from 47)
```

**JSON format:**
```json
{
  "logs": [
    {
      "path": ".fractary/logs/session/session-001.md",
      "log_type": "session",
      "title": "Fix authentication bug",
      "log_id": "session-001",
      "status": "active",
      "date": "2025-11-16T10:30:00Z",
      "age_days": 0,
      "retention": {
        "expires_at": "2025-11-23T10:30:00Z",
        "days_until_expiry": 7,
        "status": "active"
      }
    }
  ],
  "metadata": {
    "total": 4,
    "filtered_from": 47,
    "limit": 50,
    "offset": 0,
    "has_more": false
  }
}
```

**Summary format:**
```
Log Summary
───────────────────────────────────────
Total logs: 47

By type:
  - session: 12 logs (3 active, 9 archived)
  - build: 15 logs (0 active, 15 archived)
  - test: 8 logs (1 failed, 7 completed)
  - deployment: 6 logs (6 completed)
  - debug: 3 logs (1 active, 2 archived)
  - audit: 2 logs (2 completed)
  - operational: 1 log (1 completed)

By status:
  - active: 5
  - completed: 37
  - failed: 2
  - archived: 3

Retention:
  - Expiring soon (< 7 days): 8
  - Active: 35
  - Expired: 4
```

**Detailed format:**
Shows full frontmatter + first 3 lines of body for each log
</WORKFLOW>

<COMPLETION_CRITERIA>
✅ All log files discovered in requested types
✅ Frontmatter parsed for all valid logs
✅ Filters applied correctly
✅ Results sorted by requested criteria
✅ Output formatted in requested format
✅ Pagination metadata included (if applicable)
</COMPLETION_CRITERIA>

<OUTPUTS>
Return to caller:
```
🎯 STARTING: Log Lister
Filters: log_type={type}, status={status}, limit={limit}
Format: {format}
───────────────────────────────────────

📁 Discovering logs in .fractary/logs/
Found: 47 logs across 7 types

🔍 Applying filters:
  - Type: {log_type}
  - Status: {status}
  - Date range: {from} to {to}

Matched: 4 logs

[Formatted output here]

✅ COMPLETED: Log Lister
Listed: 4 logs (filtered from 47)
Types: session (2), test (2)
───────────────────────────────────────
Next: Use log-validator to check specific log, or log-archiver to archive old logs
```
</OUTPUTS>

<DOCUMENTATION>
Write to execution log:
- Operation: list-logs
- Filters applied: {filters}
- Total logs found: {total}
- Logs returned: {count}
- Format: {format}
- Timestamp: ISO 8601
</DOCUMENTATION>

<ERROR_HANDLING>
**No logs directory:**
```
⚠️  WARNING: Logs directory not found
Path: .fractary/logs/
No logs to list. Use log-writer to create logs first.
```

**No logs match filters:**
```
ℹ️  INFO: No logs match the specified filters
Filters: log_type={type}, status={status}
Total logs available: {total}
Suggestion: Try broader filters or check log types with "list-logs --all"
```

**Malformed frontmatter (non-fatal):**
```
⚠️  WARNING: Skipping log with malformed frontmatter
Path: {log_path}
Error: {parse error}
Continuing with remaining logs...
```

**Invalid log type filter:**
```
❌ ERROR: Unknown log type '{type}'
Valid types: session, build, deployment, debug, test, audit, operational, _untyped, all
```
</ERROR_HANDLING>

## Scripts

This skill uses two supporting scripts:

1. **`scripts/discover-logs.sh {log_type_filter} {status_filter} {date_from} {date_to}`**
   - Discovers all log files matching filters
   - Parses frontmatter for filtering
   - Returns JSON array of log metadata
   - Handles malformed logs gracefully

2. **`scripts/format-output.sh {format} {logs_json}`**
   - Formats log list in requested format
   - Supports table, json, summary, detailed
   - Adds retention information
   - Calculates relative dates (age)
