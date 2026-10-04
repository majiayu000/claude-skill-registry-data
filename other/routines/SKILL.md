---
name: routines
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, ToolSearch, WebFetch, RemoteTrigger
description: 'Create, fire, and manage Claude Code cloud routines (scheduled/API/GitHub-triggered remote agents). Use for "routine", "schedule a remote agent", "webhook to Claude", "daily/weekly Claude job", "cron routine".'
---

# Routines — Cloud Scheduled Agents

Routines are **saved Claude Code configurations that run on Anthropic-managed cloud infrastructure** — a prompt + repo(s) + connectors, fired on a schedule, HTTP POST, or GitHub event. They keep working when Nick's laptop is closed.

Docs: https://code.claude.com/docs/en/routines
Fire API: https://platform.claude.com/docs/en/api/claude-code/routines-fire
Web UI: https://claude.ai/code/scheduled

## When to use routines vs other scheduling

| Need | Use |
|------|-----|
| Runs unattended in cloud, survives laptop off | **Routine** (this skill) |
| Runs inside the current REPL session only | `CronCreate` (in-session) |
| Runs on Nick's local machine with local file/MCP access | Desktop scheduled task |
| One-shot reminder later today | `CronCreate` with `recurring: false` |

**Hard constraint**: routines run in Anthropic cloud. They have **no access to**:
- Chrome DevTools MCP (Nick's logged-in X/Skool/etc. sessions)
- Local files outside the cloned repo
- Local `.env` variables
- The gmail CLI, Instantly SQLite DB, or anything on `~/Business/` not in the GitHub repo

If the task needs any of those, either adapt it to use WebFetch/WebSearch + API calls (with secrets added to the cloud env), or use a local scheduler instead.

## Canonical creation body (tested, works)

Load `RemoteTrigger` first, then call `{action: "create", body: ...}` with this exact shape:

```json
{
  "name": "DESCRIPTIVE_NAME",
  "cron_expression": "MM HH * * *",
  "enabled": true,
  "job_config": {
    "ccr": {
      "environment_id": "env_01Mxbg5dUFJhMLamQxdZc6Nb",
      "session_context": {
        "model": "claude-sonnet-4-6",
        "sources": [
          {"git_repository": {"url": "https://github.com/nickjwells/business"}}
        ],
        "allowed_tools": ["Bash", "Read", "Write", "Edit", "Glob", "Grep", "WebFetch", "WebSearch"]
      },
      "events": [
        {
          "data": {
            "uuid": "GENERATE_FRESH_LOWERCASE_V4_UUID",
            "session_id": "",
            "type": "user",
            "parent_tool_use_id": null,
            "message": {
              "role": "user",
              "content": "THE_PROMPT_HERE"
            }
          }
        }
      ]
    }
  }
}
```

### Hardcoded values for Nick's account
- **`environment_id`**: `env_01Mxbg5dUFJhMLamQxdZc6Nb` (Default, anthropic_cloud kind)
- **Default repo**: `https://github.com/nickjwells/business` — ask if a different repo (e.g., `nickjwells/email-optimizer`) is needed
- **Default model**: `claude-sonnet-4-6` (routines are research/automation, not heavy reasoning)
- **Creator UUID**: `e90448dc-83c5-4398-b3a2-8402733adf0e` (for reference; not needed in the body)

## Cron conventions

- **Cron is UTC**. Nick's timezone is `America/Edmonton` (MDT = UTC−6, MST = UTC−7). Convert and confirm with him.
- **Minimum interval: 1 hour**. `*/30 * * * *` is rejected.
- **Avoid minute 0 and 30** — every routine on the platform lands on those. Pick an off-minute (`:07`, `:17`, `:43`, `:51`).
- **Stagger multiple daily routines** by 15+ min so they don't compete for resources.

Examples (Calgary local → UTC):
- Daily at 8 AM MDT → `17 14 * * *`
- Daily at 7 AM MDT → `43 13 * * *`
- Sunday 8 PM MDT → `7 2 * * 1` (note: Monday UTC because of rollover)
- Every 2 hours → `13 */2 * * *`

## Allowed tools

Pick the smallest set the routine actually needs. Common combos:

| Routine type | Tools |
|--------------|-------|
| Web research / scanning | `Bash, Read, Write, Edit, Glob, Grep, WebFetch, WebSearch` |
| API automation (no code) | `Bash, Read, Write, Edit, WebFetch` |
| Code review / PR work | `Bash, Read, Write, Edit, Glob, Grep` |
| Data pull + report | `Bash, Read, Write, Edit, Glob, Grep, WebFetch` |

Do **not** add MCP tools — routines have no MCP connectors unless explicitly attached via `mcp_connections` (and Nick currently has none configured).

## UUID generation

Events require a fresh lowercase v4 UUID. Generate one per routine:

```bash
python3 -c "import uuid; print(uuid.uuid4())"
# or
uuidgen | tr '[:upper:]' '[:lower:]'
```

Never reuse a UUID across routines.

## Output conventions

Routines should write results to the cloned repo on a `claude/*` branch (the default allowed prefix). Standard pattern:

1. Write markdown report to `active/{routine-name}/YYYY-MM-DD-HHmm-report.md`
2. Commit to `claude/{routine-name}-YYYY-MM-DD` branch
3. Also print the report to stdout so it shows in the session transcript at claude.ai/code/scheduled/{trigger_id}

Nick can open the session URL to see output, or pull the branch if he wants the file.

## Secrets and environment variables

The Default cloud env has no custom env vars. To give a routine API access (Instantly, Fireflies, ClickUp, Resend, etc.):

1. Go to https://claude.ai/code/environments
2. Edit Default (or create a new env) and add `KEY=VALUE` pairs
3. Reference them in the prompt as `$KEY` — the routine's Bash sessions will see them

**Always check for secret presence in the prompt** and exit gracefully if missing:

```
REQUIRED ENV VAR: INSTANTLY_API_KEY must be set. If missing, print
"Missing INSTANTLY_API_KEY — add at claude.ai/code/environments" and exit.
```

Never hardcode secrets in prompts — they're logged.

## Firing a routine

**Manually (right now, for testing)**:
```
RemoteTrigger({action: "run", trigger_id: "trig_01..."})
```
Returns the trigger config (not the session URL — fire is async; the session appears at claude.ai/code/scheduled/{trigger_id}).

**Via HTTP (for webhooks)**:
```
POST https://api.anthropic.com/v1/claude_code/routines/{trigger_id}/fire
Authorization: Bearer {per-routine-token}
anthropic-version: 2023-06-01
anthropic-beta: experimental-cc-routine-2026-04-01
Content-Type: application/json

{"text": "freeform context appended to the saved prompt"}
```

The `text` field is a single string appended as a user turn. Max 65,536 chars. If sending a JSON webhook payload, stringify it — the routine can parse the string in its prompt.

**Generating the per-routine token**: Web UI only. Open the routine at https://claude.ai/code/scheduled, click pencil → Add another trigger → API → Generate token. Shown once, can't be retrieved.

## Trigger types and how to add them

| Trigger | Created via | Notes |
|---------|-------------|-------|
| Schedule | `RemoteTrigger create` (this skill) or web UI | Cron in UTC, min 1h |
| API | Web UI only (generates bearer token) | Attach to existing routine |
| GitHub event | Web UI only | Requires Claude GitHub App installed on repo |

A single routine can have multiple triggers.

## Common webhook patterns

### Pattern 1: Fireflies meeting → recap email

```
Fireflies webhook (meeting.completed)
  → POSTs {"text": "<stringified webhook JSON>"} to /fire endpoint
  → Routine parses text to get meetingId
  → curl Fireflies GraphQL API with FIREFLIES_API_KEY for full transcript
  → Claude drafts personalized recap email
  → curl Resend API with RESEND_API_KEY to send
```

Secrets needed: `FIREFLIES_API_KEY`, `RESEND_API_KEY`.

### Pattern 2: ClickUp task closed → kickoff email

```
ClickUp webhook (taskStatusUpdated, filtered to status="Closed")
  → POSTs to /fire endpoint
  → Routine calls ClickUp API with CLICKUP_API_TOKEN to get full task (client email, notes)
  → Claude drafts kickoff email with Cal.com booking link
  → Sends via Resend
```

Secrets: `CLICKUP_API_TOKEN`, `RESEND_API_KEY`, Cal.com booking link in the prompt.

### Webhook payload → /fire translation

Most third-party webhooks (Fireflies, ClickUp, Stripe, GitHub) send their own JSON shape, but `/fire` only accepts `{"text": "..."}`. Two options:

- **Configure the sender to custom body template**: set body to `{"text": "{{stringified_event}}"}`. Works for Zapier, Make, Fireflies custom webhooks.
- **Middleware**: Cloudflare Worker / Vercel function that receives the webhook, reformats, POSTs to `/fire`. Use if you want signature verification or branching logic.

## Managing routines

```
# List all
RemoteTrigger({action: "list"})

# Get one
RemoteTrigger({action: "get", trigger_id: "trig_01..."})

# Update (partial)
RemoteTrigger({action: "update", trigger_id: "trig_01...", body: {"cron_expression": "..."}})

# Fire now
RemoteTrigger({action: "run", trigger_id: "trig_01..."})
```

**Cannot delete via API**. Direct Nick to https://claude.ai/code/scheduled to delete.

**Pausing**: set `"enabled": false` via update. Re-enable by setting back to `true`.

## Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `prompt: Extra inputs are not permitted` | Put `prompt` at top level | Move to `job_config.ccr.events[0].data.message.content` |
| `job_config must have "ccr" shape` | Used `session_request` or empty `job_config` | Use `job_config.ccr.{environment_id, session_context, events}` |
| `session_request.worker: Field required` | Used old `session_request` shape | Switch to `job_config.ccr` (v2 shape) |
| `invalid cron expression` | Interval < 1h, or 6-field cron | Use 5-field, ≥1h |
| `proto: unknown field "type"` | Added unknown top-level field | Remove non-schema fields |
| Session fires but does nothing visible | Expected — fire is async, output is in session URL | Check claude.ai/code/scheduled/{trigger_id} |

## Full working example (tested 2026-04-14)

Creates a daily 6:51 AM MDT routine that scans for mentions of Nick and commits a report:

```python
# Pseudocode for the RemoteTrigger call
RemoteTrigger(action="create", body={
    "name": "Daily Mention Scan",
    "cron_expression": "51 12 * * *",  # 6:51 AM MDT = 12:51 UTC
    "enabled": True,
    "job_config": {
        "ccr": {
            "environment_id": "env_01Mxbg5dUFJhMLamQxdZc6Nb",
            "session_context": {
                "model": "claude-sonnet-4-6",
                "sources": [{"git_repository": {"url": "https://github.com/nickjwells/business"}}],
                "allowed_tools": ["Bash", "Read", "Write", "Edit", "Glob", "Grep", "WebFetch", "WebSearch"]
            },
            "events": [{
                "data": {
                    "uuid": "d8e4a2b6-5c9f-47d1-b3a7-2e8f4c6d9b17",
                    "session_id": "",
                    "type": "user",
                    "parent_tool_use_id": None,
                    "message": {
                        "role": "user",
                        "content": "Run WebSearch queries for 'Nick Saraev' with after:{today-2} date filter across reddit, x, HN, linkedin, youtube, podcasts. Filter hard for newsworthy signal (notable mentions, press, complaints, big student wins). Commit findings to claude/nick-scan-YYYY-MM-DD branch if anything interesting, else print 'No notable mentions.' and exit."
                    }
                }
            }]
        }
    }
})
```

Response includes `trigger.id` (prefix `trig_`). Store for future fire/update calls.

## Workflow checklist

When Nick asks for a new routine:

1. **Clarify the task** — what runs, when, what output, what secrets needed
2. **Check constraints** — does it need Chrome DevTools / local files / local env? If yes, redirect to local scheduler
3. **Pick schedule** — UTC, off-:00 minute, stagger against existing routines (check `RemoteTrigger list`)
4. **Pick tools** — minimum viable set (avoid adding WebFetch if not needed)
5. **Draft prompt** — self-contained, specific steps, explicit output format + save path, graceful handling of missing secrets
6. **Generate fresh UUID**
7. **Create** — `RemoteTrigger create`
8. **Test** — `RemoteTrigger run` immediately
9. **Report back** — trigger ID, schedule in local time, session URL, any secrets Nick still needs to add
10. **Add to active/todo.md if secrets are pending**

## Reference: active routines (update as they change)

Check `RemoteTrigger({action: "list"})` for the current set. Past history is on claude.ai/code/scheduled.
