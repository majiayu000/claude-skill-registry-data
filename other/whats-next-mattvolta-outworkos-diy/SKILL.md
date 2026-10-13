---
name: whats-next
description: "Syncs Todoist, Gmail, Calendar, and Fireflies to surface untracked action items and recommend the next task to work on. Use when starting a session, asking 'what's next', or checking priorities for any project."
context: fork
---

# What's Next

## Purpose

Full-sweep sync across all project data sources, then recommend the single most important next action. Auto-creates Todoist tasks for untracked action items found in email, calendar, or meeting transcripts.

## Runtime Context

At the start of each run, retrieve user context:

```sql
SELECT email, timezone FROM user_profiles WHERE user_id = auth.uid()
```

Use the returned `email` as `USER_EMAIL` for all Gmail queries (sent-mail searches, recipient matching) and `timezone` for date calculations.

Store these values for use throughout all steps.

## Arguments

An optional project name or slug can be passed to target a specific project from any working directory.

| Invocation | Behavior |
|---|---|
| `/whats-next` | Uses the current working directory to detect the project |
| `/whats-next Sprint` | Targets the Sprint project regardless of CWD |
| `/whats-next bai-metrics` | Targets BAI Metrics by slug |

Matching is case-insensitive against both the project **name** and **slug** from the SessionStart manifest.

## Prerequisites

- Project has a `context-map.md` in its root (created by `/context-map`)
- `TODOIST_API_TOKEN` available via Vault (`$OUTWORKOS_ROOT/scripts/get-secret.sh todoist_api_token`)
- MCP tools available: Google Workspace (Gmail, Calendar), Fireflies

## Execution Steps

### Step 1: Resolve Project + Load Context

#### 1a. Resolve Target Project

If an **argument** was provided:
1. Normalize the argument to lowercase
2. Search the SessionStart manifest for a match on **project name** (case-insensitive) or **slug** (exact match after lowercasing)
3. If found, use the manifest entry's `Path` to construct the context-map path: `{manifest.Path}/context-map.md`
4. If no match, stop and list available projects with Todoist IDs so the user can pick

If **no argument** was provided:
1. Use the current working directory
2. Read `./context-map.md` from the project root
3. If not found, check if CWD matches any manifest entry's `Path` and suggest the project name

#### 1b. Load Project Context

## Data Storage Rules

- **DB is source of truth** via Supabase MCP `execute_sql`. Discover MCP tools via `ToolSearch` at runtime — never hardcode tool names.
- **Project DB IDs** come from the SessionStart manifest (injected into context). Each project entry includes `DB ID`, `Slug`, and `Todoist ID`.
- **User ID for all DB writes:** Retrieved from `auth.uid()` via authenticated session (from SessionStart hook's `SUPABASE_ACCESS_TOKEN`)
- **Graceful fallback:** If Supabase MCP is unavailable, fall back to file-only I/O.

**DB-first:** Query `SELECT todoist_project_id, context_map_md, context_map FROM projects WHERE slug = '{project_slug}'` via Supabase MCP. Extract primary email, Todoist project ID, and person name from the `context_map_md` or `context_map` JSONB fields.

**Fallback:** Read `context-map.md` from the resolved project path (from Step 1a). Extract:

| Field | Where to Find |
|-------|---------------|
| **Primary email** | People section -> primary stakeholder -> Keys by Data Source -> email |
| **Todoist project ID** | Quick Reference -> `Todoist Project ID` (or from SessionStart manifest `Todoist ID` field) |
| **Person name** | People section -> primary stakeholder name |

If any of these are missing, ask the user before proceeding.

### Step 2: Pull Open Tasks from Todoist

**IMPORTANT: Use the EXACT command below.** Todoist has no MCP server. The only reliable method is the **Sync API** via `POST /api/v1/sync`. Do NOT use REST endpoints (`/rest/v2/tasks`, `/api/v1/tasks`, etc.) — they will fail or return wrong formats.

**Cache-aware:** If `/scan` ran recently (< 5 min), reuse its cached data files instead of hitting the API. The shared sync token cache at `/tmp/todoist-sync-cache.json` and scan's data files (`/tmp/scan-items.json`, `/tmp/scan-projects.json`) are checked first.

```bash
python3 << 'PYEOF'
import json, os, time, sys, urllib.request

PROJECT_ID = 'PROJECT_ID'  # Replace with value from Step 1

CACHE_PATH = '/tmp/todoist-sync-cache.json'
CACHE_TTL = 300  # 5 minutes
SCAN_ITEMS = '/tmp/scan-items.json'
SCAN_PROJECTS = '/tmp/scan-projects.json'

# If /scan ran recently and its data files are fresh, skip the API call entirely
scan_fresh = False
if os.path.exists(SCAN_ITEMS) and os.path.exists(CACHE_PATH):
    try:
        cache_age = time.time() - os.path.getmtime(CACHE_PATH)
        items_age = time.time() - os.path.getmtime(SCAN_ITEMS)
        if cache_age < CACHE_TTL and items_age < CACHE_TTL:
            scan_fresh = True
    except OSError:
        pass

if scan_fresh:
    print('[cache] Reusing fresh scan data (< 5 min old)', file=sys.stderr)
    items = json.load(open(SCAN_ITEMS))
else:
    # Read token
    # Get Todoist token from Vault via Supabase RPC get_user_secret('todoist_api_token')
    # Or from CLAUDE_ENV_FILE if available in the session environment
    import subprocess
    TOKEN = subprocess.check_output(['bash', '-c', 'source "$CLAUDE_ENV_FILE" 2>/dev/null && echo "$TODOIST_API_TOKEN"']).decode().strip()
    if not TOKEN:
        raise RuntimeError("TODOIST_API_TOKEN not found. Check Vault or CLAUDE_ENV_FILE.")

    # Check sync token cache for incremental sync
    cached_token = '*'
    if os.path.exists(CACHE_PATH):
        try:
            cache = json.load(open(CACHE_PATH))
            age = time.time() - os.path.getmtime(CACHE_PATH)
            if age < CACHE_TTL:
                cached_token = cache.get('sync_token', '*')
        except (json.JSONDecodeError, KeyError):
            pass

    req = urllib.request.Request(
        'https://api.todoist.com/api/v1/sync',
        data=json.dumps({"sync_token": cached_token, "resource_types": ["items"]}).encode(),
        headers={'Authorization': f'Bearer {TOKEN}', 'Content-Type': 'application/json'},
        method='POST'
    )
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode('utf-8'))

    # Update shared sync token cache
    json.dump({'sync_token': data.get('sync_token', '*')}, open(CACHE_PATH, 'w'))

    items = [i for i in data.get('items', []) if not i.get('checked')]

# Filter to project and display
project_items = [i for i in items if i.get('project_id') == PROJECT_ID]
project_items.sort(key=lambda x: (x.get('due', {}).get('date', '9999') if x.get('due') else '9999'))
for i in project_items:
    due = i.get('due', {}).get('date', 'no date') if i.get('due') else 'no date'
    pri = i.get('priority', 1)
    sec = i.get('section_id', 'none')
    print(f'[p{pri}] {i["content"]} (due: {due}, id: {i["id"]}, section: {sec})')
    if i.get('description'):
        print(f'  desc: {i["description"][:150]}')
PYEOF
```

Replace `PROJECT_ID` with the value from Step 1. Store the task list for cross-referencing in Step 4.

### Step 3: Scan Data Sources (parallel)

Run these three searches in parallel. Look back **7 days** from today.

**Gmail** — search for recent emails involving known project contacts only:

1. Extract every email address from the **People section of the context-map** (all contacts, all roles).
2. Build a scoped query using those addresses:
   ```
   search_gmail_messages(query: "(from:{addr1} OR from:{addr2} OR ... OR to:{addr1} OR to:{addr2} OR ...) after:{7_days_ago}", max_results: 20)
   ```
   Do NOT use a broad `from:{USER_EMAIL} OR to:{USER_EMAIL}` query — that returns all of the user's mail and will produce false positives from unrelated threads.
3. Then batch-fetch content for the returned messages to get subjects, senders, and body summaries.

If the People section has no email addresses, fall back to the broad query but note the limitation.

**Calendar** — check upcoming events (next 7 days):
```
get_events(calendar_id: "primary", time_min: "{today}", time_max: "{today+7d}")
```
Filter to events where AT LEAST ONE attendee email matches a known project contact (from the People section of context-map.md). Do NOT include events based on inferred or indirect relevance (e.g., "this funder supports the project" or "potential pipeline"). If no attendee email matches a known contact, exclude the event entirely.

**Fireflies** — search recent meeting transcripts:
```
fireflies_search(participant: "{email}", limit: 10)
```
For any transcripts from the last 7 days, pull summaries to extract action items **assigned to the user (the project owner)**. Do NOT include action items assigned to the stakeholder — this project tracks what the user needs to do, not what the stakeholder needs to do.

### Step 3b: Validate Open Tasks Against Sent Mail (Sonnet subagent)

This step is delegated to a **Sonnet subagent** using the Task tool. Sonnet is more reliable at systematic, literal pattern-matching across every cell of the matrix — it won't shortcut or abstract.

**Before spawning the subagent**, extract all unique email addresses mentioned across:
- Task descriptions (names, email addresses, senders referenced)
- The People section of the context-map (all known email addresses for each person)

**Important: people may have multiple email addresses.** For example, a contact may use both work and personal addresses. A reply to ANY of a person's known addresses counts as evidence for tasks involving that person. Build a person-to-emails mapping from the context-map People section and task descriptions.

**Spawn the subagent** with `model: "sonnet"` and `subagent_type: "general-purpose"`. The subagent MUST do its own Gmail searches — do NOT pre-fetch emails and pass them as static data, because you may miss messages.

Pass it this prompt (fill in the bracketed values):

```
You are validating whether the user has already acted on open Todoist tasks by checking sent emails.

**Why this matters:** This matrix is the sole mechanism for determining whether tasks are complete. A false negative ("no evidence") means the user gets told to re-do work they already finished. Be thorough — a wrong verdict wastes real human time.

## Inputs

**Open tasks:**
{paste the full task list from Step 2, one per line with content + description}

**Person-to-email mapping** (from context-map):
{paste mapping, e.g.:
- Person A: persona@work.com, persona@gmail.com
- Person B: personb@company.ca
...etc}

## Instructions

1. **Search sent emails by RECIPIENT, not by thread.** For each person mentioned in any task, search ALL of their known email addresses:

   For each person with emails [email1, email2, ...]:
   ```
   search_gmail_messages(query: "from:{USER_EMAIL} (to:{email1} OR to:{email2}) after:{7_days_ago_YYYY/MM/DD}", max_results: 20)
   ```

   Collect ALL sent emails across all people into one pool. This ensures you find replies even when:
   - The user replied in a different thread than the original
   - The user replied to a different email address for the same person
   - The user sent a new email (not a reply) about the same topic

2. For EACH returned email, fetch its full content individually (format: "full"). Read the complete body text before proceeding to the matrix.

3. Build a cross-reference matrix. For EVERY combination of (task x email), fill in ALL columns:

| Task | Email Subject | Recipient | Body Summary (1-2 sentences of what the email says) | Evidence Quote (verbatim from body, or "none found") | Verdict |
|------|--------------|-----------|-----------------------------------------------------|------------------------------------------------------|---------|

**Column rules:**
- **Body Summary**: REQUIRED for every row. Summarize what this email actually discusses. This proves you read it. Writing "no reference to [task topic]" without a summary is NOT acceptable.
- **Recipient**: The actual To: address. This helps identify which person the email was for.
- **Evidence Quote**: If evidence exists, quote the exact words from the email body. If none, write "none found."
- **Verdict**: `action_taken` or `no_match`

**Evidence patterns to scan for in body text:**
- Deliverable language: "I've added", "we added", "I built", "I've updated", "take a look at", "here's the link"
- Completion language: "done", "shipped", "deployed", "sent over", "attached"
- Topic overlap: does the email discuss the same subject matter as the task, even if not using exact words? E.g., an email about "six New Brunswick companies" is evidence for a task about "regional scan for NB"
- Response to the same person about the same topic in a DIFFERENT thread still counts

**Worked example of a CORRECT row:**
| Run Saint John NB scan | Dashboard update: pipeline self-service | team@client.com | Email describes new dashboard features AND mentions "the six New Brunswick companies we added recently" with a link to the updated app | "I've added a few new features... the six New Brunswick companies we added recently" | action_taken |

**Worked example of an INCORRECT row (do NOT do this):**
| Run Saint John NB scan | Dashboard update: pipeline self-service | team@client.com | No reference to regional scan | none | no_match |
(Wrong because the agent only looked at the subject line and didn't read the body)

A single email may contain evidence for multiple tasks. Check every task against every email — do not stop after the first match.

4. Return the completed matrix and a summary list of tasks with verdict `action_taken`.
```

**After the subagent returns**, use its matrix results for the rest of the skill. Tasks flagged as `action_taken` should appear in the "Already Acted On" section in Step 6 output — not presented as open work.

### Step 4: Cross-Reference and Auto-Create Tasks

Compare findings from Step 3 against the existing Todoist tasks from Step 2.

**Contact gate (MANDATORY — apply before any other classification):**
Before classifying any email as an untracked action item, verify that at least one of the sender or recipients appears in the **People section of the context-map**. Use the exact email addresses listed there. If no sender or recipient matches a known project contact, **skip the email entirely** — do not apply thematic or topical inference to make a connection. An organizational affiliation, overlapping subject matter, or timing coincidence does NOT qualify an email for task creation.

**What counts as "untracked":**
- An email thread requesting action from the user that has no matching Todoist task, AND where at least one sender/recipient is a known project contact
- A meeting action item assigned specifically to the user (the project owner) with no matching task — do NOT create tasks for action items assigned to the stakeholder. This project tracks the user's work, not the stakeholder's work.
- An upcoming event that requires preparation from the user with no matching task
- Do NOT create tasks for items where the user has already sent a response (check Step 3b flags)
- Do NOT create tasks from engagement platform data (milestones, target dates, engagement status). Those are record systems, not task sources. Tasks only come from emails, meetings, calendar events, or manual entry.

**Matching heuristic:** Check if any existing task's `content` or `description` references the same subject, thread, or topic. Fuzzy match — don't require exact strings.

**Source ID dedup (MANDATORY):** Before creating any task, check if an existing task's description contains the same source identifier (Gmail thread_id, Fireflies transcript_id, Slack message_ts) in its `**Sources:**` block. This prevents duplicates when both `/scan` and `/whats-next` process the same signals.

**For each untracked item, auto-create a Todoist task:**

```bash
TODOIST_API_TOKEN=$("$OUTWORKOS_ROOT/scripts/get-secret.sh" todoist_api_token)
curl -s -X POST https://api.todoist.com/api/v1/sync \
  -H "Authorization: Bearer $TODOIST_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "commands": [{
      "type": "item_add",
      "temp_id": "'$(uuidgen)'",
      "uuid": "'$(uuidgen)'",
      "args": {
        "content": "[task description]",
        "project_id": "PROJECT_ID",
        "description": "[source type]: [source ID]. [context from email/meeting/event]",
        "priority": [priority 1-4]
      }
    }]
  }'
```

**Priority assignment:**
- `4` (urgent): Overdue or due today, explicit deadline mentioned
- `3` (high): Due this week, someone is waiting on a response
- `2` (medium): Action needed but no hard deadline
- `1` (normal): Nice-to-do, low urgency

**Label:** Apply the `gap` label to all auto-created tasks (indicates they were system-generated and need triage).

**Description format:** Always start with a `**Sources:**` block so tasks are traceable and dedup works:
- Gmail: `- Gmail: "{Subject}" — https://mail.google.com/mail/u/0/#inbox/{thread_id}`
- Fireflies: `- Fireflies: "{Meeting title}" — https://app.fireflies.ai/view/{transcriptId}`
- Calendar: `- Calendar: "{Event title}" — {htmlLink}`

Batch all new task commands into a single Sync API call.

### Step 5: Recommend Next Action

From the full task list (existing + newly created), recommend the **single best next action** using this priority stack:

1. **Overdue tasks** — anything past its due date
2. **Prep for imminent meetings** — events in the next 48 hours that need preparation
3. **Awaiting response** — threads where someone is waiting on the stakeholder
4. **High priority by Todoist** — p4/p3 tasks
5. **Deadlines this week** — tasks due in the next 7 days
6. **Everything else** — by creation order (oldest first)

Within each tier, prefer tasks that unblock other people.

### Step 6: Present Results

Format the output as:

```
## What's Next

**Recommended:** [task name]
[1-2 sentence rationale — why this, why now]

### Full Task List ([count] open)

[Grouped by priority tier, each showing: task name, due date, source]
[Exclude tasks flagged as action_taken — those go below]

### Already Acted On ([count])

[Tasks where sent mail confirms the user already responded or took action]
[Each shows: task name, what was sent, date — so the user can close them or confirm they're waiting]

### New Tasks Created ([count])

[List of tasks auto-created from this sync, with their source]

### Upcoming Events ([count] in next 7 days)

[Only events where a known project contact is a confirmed attendee. For each event, list the matching contact name and their email. No relevance inference — if no known contact appears in the attendee list, the event is excluded.]
```

Keep it scannable. The user should be able to glance and know what to do.

## Edge Cases

- **No context-map.md found**: Stop and suggest running `/context-map` first
- **Todoist token expired**: Flag the 401/403 and tell the user to update the token in Vault via `$OUTWORKOS_ROOT/scripts/set-secret.sh todoist_api_token <new_token>`
- **No new items found**: Just prioritize existing tasks — don't force-create work
- **Multiple stakeholders in context-map**: Ask which person to focus on
- **Google OAuth expired**: Run `./scripts/google-auth.sh --check` first; if expired, tell the user to re-auth before proceeding
