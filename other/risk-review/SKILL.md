---
name: risk-review
description: "Interactive walkthrough of the top 5 risk-labelled Todoist tasks. Pulls full context (emails, meetings, task history) for each item and helps resolve them one by one — reply, close, reschedule, or delegate. Use after /risk to work through flagged items."
argument-hint: ["(default: top 5 by priority)"]
context: fork
---

# Risk Review — Interactive Follow-Through

## What This Does

Fetches the top 5 Todoist tasks labelled `risk`, pulls full context for each (emails, meetings, task details), and walks you through them one at a time. For each item you decide what to do: reply, close, reschedule, delegate, or skip. Actions are executed immediately.

Only 5 tasks are loaded upfront. If you finish all 5 and want more, say so and the next batch will be fetched.

## Runtime Context

At the start of every run, look up the current user's profile to get dynamic values. Use Supabase MCP tools (discover via ToolSearch at runtime) to execute:

```sql
SELECT id AS user_id, email, display_name, timezone
FROM user_profiles
WHERE id = auth.uid()
LIMIT 1;
```

Use the returned values throughout this skill:
- `user_id` — for all DB reads/writes (replaces any hardcoded UUID)
- `email` — for Gmail sent-mail searches (e.g., `from:{email}`)
- `display_name` — for display purposes
- `timezone` — for date calculations

If `auth.uid()` is not available in your SQL context, retrieve the user ID from the session environment or manifest instead.

## Data Storage Rules

- **DB is source of truth** via Supabase MCP `execute_sql`. Discover MCP tools via `ToolSearch` at runtime — never hardcode tool names.
- **Secrets from Vault:** Use `$OUTWORKOS_ROOT/scripts/get-secret.sh <label>` to retrieve API tokens at runtime.

## Prerequisites

- `/risk` has been run recently (tasks have the `risk` label applied)
- `TODOIST_API_TOKEN` available via Vault
- MCP tools available: Google Workspace (Gmail, Calendar), Fireflies

---

## Phase 1: Fetch Risk Tasks

### 1a. Todoist Sync (Shared Cache)

Use the shared Todoist sync cache pattern. If `/tmp/todoist-sync-cache.json` is fresh (< 5 min), reuse cached data. Otherwise do a full sync.

```python
import json, os, time, subprocess, uuid

CACHE_PATH = '/tmp/todoist-sync-cache.json'
CACHE_TTL = 300
SCAN_ITEMS = '/tmp/scan-items.json'

scan_fresh = False
if os.path.exists(SCAN_ITEMS) and os.path.exists(CACHE_PATH):
    try:
        if (time.time() - os.path.getmtime(CACHE_PATH)) < CACHE_TTL:
            scan_fresh = True
    except OSError:
        pass

if scan_fresh:
    items = json.load(open(SCAN_ITEMS))
else:
    _ROOT = os.environ['OUTWORKOS_ROOT']
    TOKEN = subprocess.check_output(
        ['bash', '-c', 'source "$CLAUDE_ENV_FILE" 2>/dev/null && echo "$TODOIST_API_TOKEN"']
    ).decode().strip()
    if not TOKEN:
        TOKEN = subprocess.check_output(
            [_ROOT + '/scripts/get-secret.sh', 'todoist_api_token']
        ).decode().strip()

    import urllib.request
    req = urllib.request.Request(
        'https://api.todoist.com/api/v1/sync',
        data=json.dumps({"sync_token": "*", "resource_types": ["items", "sections", "projects"]}).encode(),
        headers={'Authorization': f'Bearer {TOKEN}', 'Content-Type': 'application/json'},
        method='POST'
    )
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode('utf-8'))
    json.dump({'sync_token': data.get('sync_token', '*')}, open(CACHE_PATH, 'w'))
    items = [i for i in data.get('items', []) if not i.get('checked') and not i.get('is_deleted')]
```

### 1b. Filter to Risk Label + Rank

```python
risk_tasks = [t for t in items if 'risk' in t.get('labels', [])]

# Sort by priority descending (Todoist: 4=urgent, 1=normal), then by due date ascending
risk_tasks.sort(key=lambda t: (
    -t.get('priority', 1),
    t.get('due', {}).get('date', '9999') if t.get('due') else '9999'
))

top_5 = risk_tasks[:5]
```

Save to `/tmp/risk-review-queue.json` for reference.

### 1c. Load Project Names

Map each task's `project_id` to a project name using the SessionStart manifest or the synced projects data.

### 1d. Present the Queue

Show the user what they're working through:

```
## Risk Review — 5 items to work through

| # | Task | Project | Priority | Due |
|---|------|---------|----------|-----|
| 1 | Reply to Christian MacNamara — confirm Sprint listing | Sprint | P1 | Mar 24 |
| 2 | Schedule first monthly RBCx touchpoint | RBCx | P1 | Mar 9 |
| 3 | Follow up with Adithya Rao — CH-000189 | Scale AI | P1 | — |
| 4 | Review Paul Thornton meeting notes | AI Talent WG | P1 | — |
| 5 | Follow up with Lorie McCarthy — WebEx | RBCx | P2 | Mar 11 |

Starting with #1. Let me pull the full context...
```

---

## Phase 2: Walk Through Each Task

Process tasks **one at a time**, starting with #1. For each task:

### 2a. Pull Context (parallel)

Run these searches in parallel to gather everything relevant to this task:

**Task details** — from the Todoist data already loaded: content, description, due date, priority, labels, section, date added.

**Gmail — inbound** — Use Google Workspace MCP tools (discover via ToolSearch: "+google gmail"). Search for emails related to this task's topic/person:
```
search_gmail_messages(query: "from:{person_email} OR to:{person_email} newer_than:30d", max_results: 10)
```
Fetch full content for the most recent 3-5 messages to understand the thread.

**Gmail — sent** — Check what the user has already sent. Use the `email` from the Runtime Context lookup (user_profiles) as the sender:
```
search_gmail_messages(query: "from:{user_email} to:{person_email} newer_than:30d", max_results: 10)
```
Fetch full content to identify the last outbound and any promises made.

**Calendar** — Check for upcoming meetings with this person:
```
get_events(calendar_id: "primary", time_min: "{today}", time_max: "{14_days_from_now}")
```
Filter to events mentioning the person's name or email.

**Fireflies** — Search for recent meeting transcripts (non-fatal if unavailable):
```
fireflies_search(participant: "{person_email}", limit: 5)
```

### 2b. Present Context Summary

Format a concise briefing for the user:

```
---

### #1: Reply to Christian MacNamara — confirm Sprint listing

**Project:** Sprint
**Priority:** P1 (Urgent) | **Due:** Mar 24 | **Risk:** Critical (16d)
**Person:** Christian MacNamara (christian@grovi.io)

**What happened:**
- Feb 20: Christian emailed asking to confirm Growth & Marketing Sprint listing
- Feb 22: Follow-up email from Christian
- No reply sent

**Last outbound to Christian:** None found in last 30 days

**Upcoming:** No meetings scheduled with Christian

**Task description:**
> [task description from Todoist]

---

**What would you like to do?**
- **reply** — Draft and send a reply (launches email-composer flow)
- **close** — Mark as done (already handled outside email)
- **reschedule [date]** — Push the due date (e.g., "reschedule monday")
- **delegate [person]** — Note that someone else owns this
- **skip** — Move to the next item, come back later
```

### 2c. Execute the User's Decision

**reply** — Use the email-composer skill pattern:
1. Ask the user what they want to say (or suggest a draft based on context)
2. Compose the email with proper threading (use the thread_id from the inbound email)
3. Send via Google Workspace MCP tools
4. After sending, offer to close the Todoist task

**close** — Complete the task via Todoist Sync API:
```python
commands = [{'type': 'item_close', 'uuid': str(uuid.uuid4()), 'args': {'id': task_id}}]
```
Also remove the `risk` label since it's resolved.

**reschedule [date]** — Update the due date via Todoist Sync API:
```python
commands = [{'type': 'item_update', 'uuid': str(uuid.uuid4()),
             'args': {'id': task_id, 'due': {'string': user_date}}}]
```

**delegate [person]** — Add a note to the task description that this is delegated, move to the Waiting section if one exists, and optionally send a delegation email.

**skip** — Move to the next task. No changes made.

### 2d. Confirm and Advance

After executing the action, confirm what was done:

```
Done — reply sent to Christian. Task closed.

Moving to #2: Schedule first monthly RBCx touchpoint...
```

Then repeat Phase 2 for the next task.

---

## Phase 3: Wrap Up

After all 5 tasks are processed (or the user stops early), show a summary:

```
## Risk Review Complete

| # | Task | Action | Result |
|---|------|--------|--------|
| 1 | Reply to Christian MacNamara | Replied + closed | Sent email, task closed |
| 2 | Schedule first monthly RBCx touchpoint | Skipped | Will handle in person |
| 3 | Follow up with Adithya Rao | Replied | Sent follow-up, task open |
| 4 | Review Paul Thornton meeting notes | Rescheduled | Moved to Monday |
| 5 | Follow up with Lorie McCarthy | Replied + closed | Confirmed WebEx |

**Resolved:** 3 of 5 | **Remaining risk tasks:** {total_remaining}

Want to continue with the next batch?
```

If the user wants to continue, fetch the next 5 risk-labelled tasks (re-sync from Todoist since labels/tasks may have changed) and repeat Phase 2.

---

## Edge Cases

- **No risk-labelled tasks**: Report "No tasks with the `risk` label found. Run `/risk` first to assess and label tasks." and exit.
- **Fewer than 5 risk tasks**: Work through however many exist. Don't pad.
- **User stops mid-review**: Show the summary for tasks completed so far. Remaining tasks keep their `risk` label.
- **Email send fails (OAuth expired)**: Direct user to re-auth via `$OUTWORKOS_ROOT/scripts/google-auth.sh`, then retry.
- **Todoist token expired**: Flag and tell user to update via Vault.
- **Task was already completed between /risk and /risk-review**: Skip it, note "already completed", move to next.
- **User wants to do something not listed** (e.g., "add a note", "change priority"): Handle it — the options listed are suggestions, not constraints. Execute whatever the user asks for the current task.

---

## Compatibility

- **Depends on `/risk`** — expects tasks to have the `risk` label applied by a recent `/risk` run
- **Shared Todoist cache** with `/scan`, `/whats-next`, and `/risk` at `/tmp/todoist-sync-cache.json` (5-min TTL)
- **Uses `/email-composer` patterns** for reply drafting — same threading, signature, and HTML wrapping approach
- **Does NOT modify the `risk` label** in bulk — only removes it from individually resolved tasks
- **Does NOT re-score risk** — that's `/risk`'s job. This skill is pure execution.
