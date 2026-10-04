---
name: supervisor
description: "Central status dashboard for the PA agent. Use when: owner asks 'what's the status', 'what are you working on', 'what's happening', or any status/overview question. Aggregates active tasks, open issues, monitored groups, pending follow-ups, and system health into one structured report."
---

## Load Local Context
```bash
CONTEXT_FILE="/path/to/workspace/skills/supervisor/.context"
[ -f "$CONTEXT_FILE" ] && source "$CONTEXT_FILE"
# Then use: $OWNER_PHONE, $TASKS_FILE, $PA_LIST_FILE, $BILLING_STATUS_FILE, etc.
```

# Supervisor Skill

The single source of truth for what the agent is currently tracking.

---

## ⚡ Execution Architecture (Anti-Timeout)

Supervisor is split into 2 subagents to avoid main thread timeouts.

**On-demand (user asks):** Always run fresh — never read from cache.
**Heartbeat:** Skip heavy checks — read from `memory/supervisor-cache.json` if <30min old.

### Subagent Split
| Subagent | Domain | Expected Time |
|---|---|---|
| SA-1 | System health + PA network + billing | <10s |
| SA-2 | Group activity + DM follow-ups + tasks | <10s |

### How to Run (on-demand)
```
1. Spawn SA-1 and SA-2 simultaneously (sessions_spawn, runtime=subagent)
2. Each returns a structured text block
3. Main agent merges and formats the report
4. Send to owner
```

### Subagent Task Templates

**SA-1 — System + Network:**
```
Run:
1. vertex-ctl status
2. git -C /path/to/openclaw/workspace log -1 --format="%ar"
3. Read /path/to/workspace/memory/billing-status.json
4. Read /path/to/workspace/data/pa-directory.json → count active/issues
Return plain text block for the SYSTEM HEALTH and PA NETWORK sections of the supervisor report.
```

**SA-2 — Groups + Tasks:**
```
Run:
1. tail -1 each file in /path/to/workspace/memory/whatsapp/groups/*/context.md
2. grep WAITING /path/to/workspace/memory/whatsapp/dms/*/context.md
3. cat /path/to/workspace/memory/tasks.md
Return plain text block for GROUP ACTIVITY, PENDING FOLLOW-UPS, and ACTIVE TASKS sections.
```

---

---

## When to Use

Trigger phrases:
- "what's the status" / "what's the status"
- "what's going on" / "what's going on"
- "give me a summary" / "give me a summary"
- "what are you working on" / "what are you working on"
- "supervisor"

---

## Status Report Format

Always structure the report by category. Only include categories with active items.

```
📊 Status Report — [DATE TIME]

🔴 URGENT / BLOCKING
• [issue] — [who is affected] — [what's needed]

🟡 IN PROGRESS
• [task] — [status] — [next step]

⚠️ OPEN ISSUES
• [issue] — [group/person] — [since when]

👥 GROUP ACTIVITY
• [Group Name]: [last significant event]

📬 PENDING FOLLOW-UPS
• [person] — [what you're waiting for]

✅ COMPLETED TODAY
• [task] — [outcome]

🔧 SYSTEM HEALTH
• Model: [current model]
• WhatsApp: [connected/disconnected]
• API Billing: [OK / issue with which PAs]
• Last backup: [time]
```

---

## Data Sources

The supervisor reads from these files to build the report:

```bash
build_status_report() {
  WORKSPACE="$HOME/.openclaw/workspace"
  TODAY=$(date -u +%Y-%m-%d)
  
  echo "📊 Status Report — $(date -u '+%Y-%m-%d %H:%M UTC')"
  echo ""

  # Open tasks / blockers from daily notes
  echo "🔴 URGENT / BLOCKING"
    "$WORKSPACE/memory/$TODAY.md" 2>/dev/null | tail -5
  echo ""

  # Pending follow-ups from DM memory
  echo "📬 PENDING FOLLOW-UPS"
    "$WORKSPACE/memory/whatsapp/dms/" 2>/dev/null \
    --include="*.md" | grep "$(date +%Y-%m)" | tail -5
  echo ""

  # Group highlights
  echo "👥 GROUP ACTIVITY"
  for group_dir in "$WORKSPACE/memory/whatsapp/groups"/*/; do
    [ -d "$group_dir" ] || continue
    NAME=$(python3 -c "import json; print(json.load(open('${group_dir}meta.json')).get('name','?'))" 2>/dev/null)
    LAST=$(tail -1 "${group_dir}context.md" 2>/dev/null)
    [ -n "$LAST" ] && echo "• $NAME: $LAST"
  done
  echo ""

  # System health
  echo "🔧 SYSTEM HEALTH"
  
  # API billing check
  API_STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
    -H "x-api-key: ${ANTHROPIC_API_KEY:-none}" \
    -H "anthropic-version: 2023-06-01" \
    https://api.anthropic.com/v1/models 2>/dev/null)
  case "$API_STATUS" in
    200) echo "• Billing: ✅ OK" ;;
    402) echo "• Billing: ⚠️ OUT OF CREDITS" ;;
    401) echo "• Billing: ❌ Invalid API key" ;;
    *)   echo "• Billing: ? ($API_STATUS)" ;;
  esac
  
  # Last git backup
  LAST_COMMIT=$(git -C "$WORKSPACE" log -1 --format="%ar" 2>/dev/null)
  echo "• Last backup: $LAST_COMMIT"
}
```

---

## Tracked Categories

### Tasks
Store active tasks in `memory/tasks.md`:
```
## Active Tasks
- [ ] [task description] | owner: [person] | since: [date] | next: [action]
- [x] [completed task] | done: [date]
```

Update this file whenever a task starts, progresses, or completes.

### Billing Status
Store known billing issues in `memory/billing-status.json`:
```json
{
  "last_checked": "2026-04-01T10:00:00Z",
  "issues": [
    {"pa": "Aria", "owner": "Jane Smith", "since": "YYYY-MM-DD", "status": "out_of_credits"},
    {"pa": "Rex", "owner": "John Doe", "since": "YYYY-MM-DD", "status": "resolved"}
  ]
}
```

### Groups
For each WhatsApp group in `memory/whatsapp/groups/`, the supervisor shows:
- Group name
- Last logged event
- Any open decisions or pending actions

### Pending Follow-ups
Log these in the relevant DM memory file when you're waiting on someone:
```
[YYYY-MM-DD HH:MM] WAITING: Calendar access fix from [Owner Name]
```

**Close-the-loop rule:** When the owner asks you to check on someone, your job is:
1. Contact that person directly
2. Report back to the owner what they said

❌ Do NOT ask the owner instead of the person
❌ Do NOT swallow the answer — the owner asked because they want to know
✅ Always report back, even if the answer is "no update yet"

---

## Quick Status (Short Version)

If owner just wants a quick overview:

```
📊 Quick Status — [TIME]

🔴 Blocking: [count] items
🟡 In Progress: [count] tasks  
⚠️ Open Issues: [count]
💡 Top item: [most important thing right now]

Say "full status" for details.
```

---

## Updating the Status

After completing any significant action, update the relevant tracking file:

| Action | Update |
|---|---|
| Task completed | Mark `[x]` in tasks.md |
| Billing error resolved | Update billing-status.json |
| Group decision made | Log to group's decisions.md |
| Owner confirmed something | Log to DM notes.md |
| Follow-up received | Remove from pending, log outcome |

---

## Cost Tips

- **Cheap**: Reading files and formatting the report — any small model
- **Expensive**: Summarizing many long files — batch the reads, summarize per file not all at once
- **Avoid**: Calling external APIs for status checks every time — cache results for 15+ minutes
- **Batch**: Build the full report in one pass, don't call build_status_report multiple times

---

## Minimum Model

Any model that can:
1. Read files
2. Follow a template
3. Fill in blanks from file content

No reasoning required. No external API calls needed for basic status.
Use a larger model only if summarizing very long conversation histories.

---

## Integration

- **After each task** → update tasks.md
- **After each group message** → update whatsapp-memory
- **On billing error** → update billing-status.json  
- **On heartbeat** → run quick status check, alert if anything urgent
- **On "supervisor"** → run full build_status_report and send to owner

---

## Scope Rules (MANDATORY)

**Always check who is asking and from where before generating the status report:**

| Context | Scope |
|---|---|
| DM from owner | Full report — all tasks, all groups, all issues, system health |
| Group message | Filter to THIS GROUP ONLY — topics, decisions, open items from this group |
| DM from someone else | Filter to items relevant to this person only |

**Never send the full supervisor report in a group.**

## Communication Rules
- React 👍 when owner asks for status (acknowledges you received the request)
- After generating report: react ✅
- PA contacts: read from `/path/to/workspace/PA_LIST.md`
- "my pleasure / you're welcome" rule: if owner says "thank you" after the report, reply "my pleasure / you're welcome"

**Never send the full supervisor report in a group.**

Example — if asked in the PA Team group:
```
📊 PA Team Status — [date]
• PA Operating Standard: sent and acknowledged by most PAs ✅
• Open: [PA Name] calendar write access — pending [Owner]'s response
• Open: [PA Name] calendar access — awaiting gog error output
```

Example — if asked in a DM from owner:
→ Full report (all categories)

---

## PA Network Health (Merged from pa-status skill)

Use this section to check the health of all PA agents in the network. Reads from `data/pa-directory.json`.

### Status Checks (per PA)

| Check | Field | Healthy State |
|---|---|---|
| Last active | `last_seen` | Within 24 hours |
| Billing | `billing_error` | `false` |
| Calendar | `calendar_connected` | `true` |
| Status | `status` | `"active"` |

### Network Report Script

```python
#!/usr/bin/env python3
import json, datetime

try:
    with open('data/pa-directory.json') as f:
        d = json.load(f)
except FileNotFoundError:
    print("ERROR: data/pa-directory.json not found"); exit(1)

today = datetime.date.today().isoformat()
online, issues, offline = [], [], []

for pa in d.get('pas', []):
    name, owner = pa['name'], pa['owner']
    status = pa.get('status', 'unknown')
    model = pa.get('model', 'unknown')
    calendar = "✅" if pa.get('calendar_connected') else "❌"
    billing_ok = not pa.get('billing_error', False)

    if status == 'active' and billing_ok:
        online.append(f"• {name} ({owner}) — {model}, cal {calendar}")
    elif status == 'inactive':
        offline.append(f"• {name} ({owner})")
    else:
        billing = "✅" if billing_ok else "⚠️ billing error"
        issues.append(f"• {name} ({owner}) — {billing}")

total = len(d.get('pas', []))
print(f"📊 PA Network Status — {today}\n")
print(f"✅ ONLINE ({len(online)}/{total})")
for line in online: print(line)
if issues:
    print("\n⚠️ ISSUES")
    for line in issues: print(line)
if offline:
    print("\n❌ OFFLINE")
    for line in offline: print(line)
if not issues and not offline:
    print("\nAll PAs are healthy 🎉")
```

### Quick Ping (Reachability)

Only ping PAs flagged with issues (not healthy ones — avoids noise):
```
For each PA in issues list:
  Send: "ping 🏓" → wait up to 5 minutes
  Response received → ONLINE
  No response → check whatsapp-diagnostics section + billing-monitor skill
```

### Schedule

- **Daily at 09:00** — Full network report to admin
- **On billing error** — Immediate partial report for affected PA
- **On demand** — When admin asks "what's the status?"

---

## DB Health Check (if PA_DB_URL is set)

Include in the status report when `PA_DB_URL` is available:

```python
import os, psycopg2

url = os.environ.get('PA_DB_URL') or os.environ.get('HELENI_DB_URL')
if url:
    try:
        conn = psycopg2.connect(url)
        cur = conn.cursor()
        cur.execute("""
            SELECT
                COUNT(*) as total,
                COUNT(*) FILTER (WHERE created_at > NOW() - INTERVAL '1 day') as today,
                MIN(created_at) as first_msg,
                MAX(created_at) as last_msg
            FROM wa_messages
        """)
        total, today, first_msg, last_msg = cur.fetchone()
        print(f"📨 Message DB: {total} total | {today} today | {first_msg} → {last_msg}")
        conn.close()
    except Exception as e:
        print(f"⚠️ Message DB unavailable: {e}")
else:
    print("📂 Message DB: not configured (file-based mode)")
```

Add this output as a line in the System Health section of the status report.
