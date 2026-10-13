---
name: process-meeting
description: "Processes a Fireflies meeting recording into a structured summary with Todoist action items and a database log entry. Use when processing meeting notes, creating tasks from meetings, or logging a recorded call."
argument-hint: ["<fireflies-url-or-transcript-id>"]
---

# Process Meeting

## Purpose

Transform a Fireflies meeting recording into a structured summary, create Todoist tasks for action items, and log the meeting to the database. One command turns a recorded call into tracked work.

## Prerequisites

- Fireflies API token in Vault (label: `fireflies_token`)
- Todoist API token in Vault (label: `todoist_api_token`)
- Supabase MCP available for database writes
- SessionStart manifest in context (for project matching)

## Execution Steps

### Step 1: Accept Input

The user provides either:
- A Fireflies URL: `https://app.fireflies.ai/view/TITLE::TRANSCRIPT_ID`
- A direct transcript ID

**Parse the transcript ID** from a URL by extracting everything after the last `::`. If the user provides a raw ID, use it directly. If no input is provided, search recent Fireflies transcripts and let the user pick.

To search recent transcripts, use Fireflies MCP tools. Discover them via ToolSearch at runtime:
```
ToolSearch: "fireflies search transcript"
```

### Step 2: Fetch Transcript

Fetch the full transcript from the Fireflies GraphQL API. See `references/fireflies-api.md` for the query structure, authentication, and field details.

```bash
FIREFLIES_TOKEN=$("$OUTWORKOS_ROOT/scripts/get-secret.sh" fireflies_token)

curl -s -X POST https://api.fireflies.ai/graphql \
  -H "Authorization: Bearer $FIREFLIES_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "query { transcript(id: \"TRANSCRIPT_ID\") { title date duration participants sentences { text speaker_name } summary { action_items overview shorthand_bullet } } }"
  }'
```

Replace `TRANSCRIPT_ID` with the parsed ID from Step 1. Extract:
- `title`, `date`, `duration`, `participants`
- `summary.overview` for the meeting summary
- `summary.shorthand_bullet` for key topics
- `summary.action_items` for tasks to create

If the API returns an error or empty result, try the Fireflies MCP tools as fallback:
```
ToolSearch: "fireflies get transcript"
```

### Step 3: Identify Project

Match the meeting to a known project using the SessionStart manifest:

1. **Check participants** against project people/contacts in the manifest
2. **Check title keywords** against project names and slugs
3. **If ambiguous**, present the top matches and ask the user to confirm
4. **If no match**, ask the user which project this meeting belongs to

Extract the project's `DB ID` and `Todoist ID` from the manifest for use in Steps 5 and 6.

### Step 4: Generate Summary

Format the transcript data using the template in `references/output-template.md`. Fill in:
- **Title** from transcript title
- **Date** formatted as YYYY-MM-DD
- **Duration** converted to human-readable (e.g., "42 minutes")
- **Attendees** from participants list
- **Summary** from `summary.overview`
- **Key Topics** from `summary.shorthand_bullet` (as bullet points)
- **Decisions** extracted from the overview and action items context
- **Action Items** from `summary.action_items` with assignee and due date where mentioned

Present the formatted summary to the user for review before proceeding.

### Step 5: Create Todoist Tasks

For each action item, create a task in the matched project's Todoist project. See `references/todoist-patterns.md` for the batch API pattern.

**Build the batch payload in Python** to avoid shell escaping issues:

```python
import json, uuid

TODOIST_PROJECT_ID = "PROJECT_ID"  # From Step 3

commands = []
for item in action_items:
    commands.append({
        "type": "item_add",
        "uuid": str(uuid.uuid4()),
        "temp_id": str(uuid.uuid4()),
        "args": {
            "content": item["task"],
            "project_id": TODOIST_PROJECT_ID,
            "description": f"Fireflies: {transcript_id}. From meeting: {meeting_title}",
            "priority": 2,
            "labels": ["from-meeting"]
        }
    })

payload = {"commands": commands}
with open("/tmp/meeting-tasks.json", "w") as f:
    json.dump(payload, f)
```

Then send the batch:
```bash
TODOIST_API_TOKEN=$("$OUTWORKOS_ROOT/scripts/get-secret.sh" todoist_api_token)
curl -s -X POST "https://api.todoist.com/api/v1/sync" \
  -H "Authorization: Bearer $TODOIST_API_TOKEN" \
  -H "Content-Type: application/json" \
  -H "X-Request-Id: $(uuidgen)" \
  -d @/tmp/meeting-tasks.json
```

Check `sync_status` in the response to verify each task was created. Use `temp_id_mapping` to get the real task IDs.

### Step 6: Log to Database

Insert a log entry via Supabase MCP `execute_sql`. Discover the tool at runtime:
```
ToolSearch: "supabase execute sql"
```

SQL to execute:
```sql
INSERT INTO log_entries (user_id, project_id, entry_date, session_title, content, source, metadata)
VALUES (
  auth.uid(),
  '{project_db_id}',
  '{YYYY-MM-DD}',
  'Meeting: {title}',
  '{full markdown summary from Step 4}',
  'fireflies',
  '{
    "transcript_id": "{transcript_id}",
    "attendees": [{attendees array}],
    "duration_minutes": {duration},
    "action_items_count": {count},
    "todoist_task_ids": [{created task IDs}]
  }'::jsonb
);
```

### Step 7: Present Results

Show the user:
1. The formatted meeting summary (from Step 4)
2. List of Todoist tasks created with their IDs
3. Confirmation that the log entry was written to the database

## Key Rules

- **Secrets from Vault only** via `$OUTWORKOS_ROOT/scripts/get-secret.sh <label>`. Never hardcode tokens.
- **Generic tool references** in all instructions. Never hardcode MCP tool names. Use ToolSearch to discover tools at runtime.
- **User ID for DB writes:** Use `auth.uid()` -- the authenticated user's ID from the current session.
- **Python for JSON payloads.** Build Todoist batch payloads in Python, write to temp file, then curl. Avoids shell escaping issues.
- **Present before committing.** Show the summary and proposed tasks to the user before creating Todoist tasks or writing DB entries.

## Edge Cases

- **No action items in transcript**: Skip Step 5, log the meeting summary only
- **Fireflies token expired**: Flag the error and tell the user to update via `$OUTWORKOS_ROOT/scripts/set-secret.sh fireflies_token <new_token>`
- **Todoist token expired**: Flag the 401/403 and tell the user to update via `$OUTWORKOS_ROOT/scripts/set-secret.sh todoist_api_token <new_token>`
- **No project match**: Ask the user; if truly ad-hoc, log to the Outwork OS project as a catch-all
- **Multiple meetings in one session**: Process each sequentially, one `/process-meeting` invocation per transcript
