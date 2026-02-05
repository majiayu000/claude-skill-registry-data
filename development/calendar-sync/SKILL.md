---
name: calendar-sync
description: |
  This skill should be used when the user asks to "sync to Google Calendar", "import activities to calendar", "add GitHub/Linear events to calendar", or "convert activity report to calendar". Transforms structured activity data into gcalcli commands for Google Calendar import.
context: fork
---

# Calendar Sync

Convert structured activity data from GitHub, Linear, and other sources into executable gcalcli commands for Google Calendar import.

## Workflow

### 1. Collect Configuration

Use `AskUserQuestion` to gather required information interactively:

**Calendar selection:**
```bash
# List available calendars
calendars=$(gcalcli list)
```

Prompt user with `AskUserQuestion`:
- **Question**: "Which calendar should events be added to?"
- **Options**: List from `gcalcli list` output (primary calendar, work calendar, etc.)
- **Header**: "Calendar"

**Timezone detection** (optional):
```bash
# Auto-detect system timezone
TZ_ABBR=$(date +%Z)  # e.g., "KST", "PST"
```

If user request specifies different timezone or auto-detection fails, use `AskUserQuestion` to confirm.

**Duplicate check preference:**
- **Question**: "Check for duplicate events before importing?"
- **Options**: "Yes (recommended)" | "No (faster import)"
- **Header**: "Duplicates"
- **Default**: Yes

### 2. Parse Input

Accept input in three formats:

**Markdown table** (from github-activity skill):
```markdown
| Time  | Activity |
|-------|----------|
| 09:00 | 🔨 **Commits**: 3 commits in `org/repo` |
| 17:00 | 🔀 **PR Created**: [#234](url) "title" in `org/repo` |
```

**JSON file** (GitHub/Linear activity output):
```json
{
  "activities": [
    {
      "type": "commit|pr_created|pr_merged|issue_comment|...",
      "timestamp": "2025-11-01T10:30:00Z",
      "title": "PR #234: Add user auth",
      "url": "https://github.com/org/repo/pull/234"
    }
  ]
}
```

**Structured data**: Direct activity objects from other skills.

Extract from markdown using regex:
- Time: `\d{2}:\d{2}`
- Icon: `🔨|🔀|✅|🔍|💬|🆕`
- Title: Text in quotes or after colon
- URL: Markdown links `[#\d+](url)`

Convert timestamps to local timezone using config.

### 3. Calculate Time Blocks (Backdate Algorithm)

**Key insight**: Activity timestamps represent **completion time**, not start time.
- Commit timestamp = when pushed (work already done)
- PR timestamp = when created (coding already finished)

**Backdate calculation**: `start_time = timestamp - duration`

| Activity Type | Duration | Example: timestamp 09:00 |
|---------------|----------|--------------------------|
| Commits       | 30 min   | → 08:30-09:00 |
| PR Created    | 60 min   | → 08:00-09:00 |
| PR Review     | 45 min   | → 08:15-09:00 |
| Issue Comment | 15 min   | → 08:45-09:00 |

For detailed duration rules: [references/duration-guide.md](references/duration-guide.md)

**Time snapping** (15-minute grid for calendar readability):
```
08:37 start → snap to 08:30
08:52 start → snap to 08:45
```

### 4. Build Work Sessions

Group related activities into coherent work sessions for clean calendar visualization.

**Session formation rules:**
1. Sort activities by timestamp (completion time)
2. Backdate each activity to get time range
3. Merge overlapping/adjacent activities (gap ≤ 30min) into sessions
4. Same repository activities prefer single session

**Example transformation:**

Raw activity data:
```
09:00 🔨 Commit A (30min work)
09:30 🔨 Commit B (30min work)
10:00 🔀 PR #234 created (60min work)
```

**Before (forward projection - wrong):**
```
09:00-09:30 🔨 Commit A
09:30-10:00 🔨 Commit B
10:00-11:00 🔀 PR #234     ← extends into future!
```

**After (backdate + session merge - correct):**
```
08:30-10:00 🔨🔀 Work session: 2 commits + PR #234 in org/repo
```
- Session start: earliest backdate (09:00 - 30min = 08:30)
- Session end: latest timestamp (10:00, when PR completed)

**Overlap resolution** (when backdated blocks collide):
```
Input:
  09:00 🔨 Commit (30min) → 08:30-09:00
  09:15 💬 Comment (15min) → 09:00-09:15

Resolution: Merge into 08:30-09:15 session
```

**Session output format:**
- **Title**: `{icons} {summary} in {repo}`
- **Start**: Earliest backdated start (snapped to 15min)
- **End**: Latest activity timestamp
- **Description**: Timeline of activities
  ```
  Work session timeline:
  08:30 → 🔨 Started coding
  09:00 → 🔨 Commit A pushed
  09:30 → 🔨 Commit B pushed
  10:00 → 🔀 PR #234 created

  https://github.com/org/repo/pull/234
  ```

**User override:** "without grouping" or "separate events" to disable session merge.

### 5. Check for Duplicates (Optional)

Query existing events using gcalcli:

```bash
gcalcli --calendar "email" agenda "start_time" "end_time"
```

Compare by:
- Time window (±30 minutes)
- Icon matching
- PR/Issue number matching
- Text similarity (60% threshold)

Prompt user for duplicate handling: `y` (add anyway), `n` (skip), `s` (skip all duplicates).

**Default**: Duplicate check enabled. Disable with explicit user request: "without duplicate check".

### 6. Generate gcalcli Commands

Output executable bash script with backdated sessions:

```bash
#!/bin/bash
set +e  # Continue on error

SUCCESS=0
FAILED=0
FAILED_COMMANDS=()

# Session: backdated from 09:30 (last commit) by 30min
echo -n "[1] 2025-11-01 09:00-09:30 🔨 Work session... "
if gcalcli add --calendar "email" \
  --title "🔨 3 commits in org/repo" \
  --when "2025-11-01 09:00" \
  --duration 30 \
  --description "Session: 09:00-09:30
09:10 → Commit: Setup auth
09:20 → Commit: Add tests
09:30 → Commit: Update docs
https://github.com/org/repo" \
  --where "GitHub" > /dev/null 2>&1; then
  echo "✓"
  ((SUCCESS++))
else
  echo "✗"
  ((FAILED++))
  FAILED_COMMANDS+=("gcalcli add ...")
fi

# Summary
echo "Import Summary: $SUCCESS/$TOTAL succeeded"
[ $FAILED -gt 0 ] && {
  printf '%s\n' "${FAILED_COMMANDS[@]}" > "$FAILED_LOG"
  echo "Failed commands: $FAILED_LOG"
  exit 1
}
```

**Log location**: `~/.claude/tmp/calendar-sync/logs/failed_imports_YYYYMMDD_HHMMSS.log`

## Activity Type Mapping

| Type | Icon | Title Prefix | Duration | Where |
|------|------|--------------|----------|-------|
| commit | 🔨 | "Commits" | 30 min | GitHub |
| pr_created | 🔀 | "PR Created" | 60 min | GitHub |
| pr_merged | ✅ | "PR Merged" | 15 min | GitHub |
| pr_review | 🔍 | "PR Review" | 45 min | GitHub |
| issue_comment | 💬 | "Issue Comment" | 15 min | GitHub |
| issue_created | 🆕 | "Issue Created" | 30 min | GitHub |
| linear_issue_created | 🎫 | "Linear Issue" | 30 min | Linear |
| linear_status_change | 🔄 | "Status Change" | 15 min | Linear |

## References

- [references/gcalcli-reference.md](references/gcalcli-reference.md): gcalcli command reference
- [references/duration-guide.md](references/duration-guide.md): Activity duration estimation rules

## Usage Examples

- "Sync GitHub report to calendar" → Parse markdown, group overlapping activities, generate gcalcli commands
- "Import yesterday's activities" → Process activity JSON, add to calendar with grouping
- "Convert markdown to calendar events" → Auto-detect format, create events
- "Sync ~/reports/github-2025-11-01.json without duplicate check" → Fast import with grouping
- "Sync activities without grouping" → Create separate calendar events for each activity

## Troubleshooting

### No Calendars Available

**Error**: `gcalcli list` returns empty or fails.

**Solution**:
1. Run `gcalcli --help` to trigger OAuth authentication
2. Follow browser prompts to grant calendar access
3. Verify calendars exist in Google Calendar web interface

### Authorization Error

**Error**: gcalcli OAuth token expired.

**Solution**: Run `gcalcli --help` to trigger OAuth re-authentication flow. Follow browser prompts to grant access.

### Invalid Date Format

**Error**: gcalcli rejects timestamp.

**Solution**: Ensure timestamps are `YYYY-MM-DD HH:MM` format. Check timezone conversion is applied correctly from config.

### Duplicate Events

**Cause**: Events already exist in calendar for specified time range.

**Solution**:
- Enable duplicate detection (default)
- Review existing events with `gcalcli agenda start_date end_date`
- Manually delete duplicates or skip during import

### Failed Command Retry

**Cause**: Some gcalcli commands failed during batch import.

**Solution**: Check failed command log at `~/.claude/tmp/calendar-sync/logs/failed_imports_*.log`. Resolve issues (auth, format, network) and run log file as bash script to retry.
