---
name: heleni-whatsapp
description: "Complete WhatsApp management for OpenClaw agents: per-conversation memory (groups + DMs), unanswered message tracking, loop prevention, and multi-PA coordination. Use when: tracking conversation context, recalling past decisions, finding unanswered messages, or preventing echo/duplicate message loops."
---

# WhatsApp Skill

Covers two responsibilities in one skill:
1. **Per-conversation memory** — separate context files per group and DM
2. **Unanswered message tracking** — file-based inbox, no DB required

---

## Dedup — Queued Message Double-Delivery (OpenClaw bug #34041)

OpenClaw runs the agent twice on the same message when queued messages are present.
This causes duplicate content in a single reply.

**Workaround:** Run dedup check at the start of every turn.

```bash
python3 /path/to/workspace/tools/dedup_check.py "<message_id>"
# exit 0 = already seen → respond with exactly: NO_REPLY
# exit 1 = new message → proceed normally
```

The `message_id` comes from the inbound metadata block (`message_id` field).
The script uses a 120-second TTL cache at `/tmp/heleni_dedup.json`.

**Note:** `NO_REPLY` is an OpenClaw platform token — it is stripped before delivery, never shown to the user.

**Install:** Script is at `workspace/tools/dedup_check.py` — no dependencies, runs on any Python 3.

---

## Load Local Context
```bash
CONTEXT_FILE="/path/to/workspace/skills/heleni-whatsapp/.context"
[ -f "$CONTEXT_FILE" ] && source "$CONTEXT_FILE"
# Then use: $OWNER_PHONE, $JID_CORE_TEAM, $INBOX_FILE, etc.
```

## Minimum Model
Any model. All operations are file-based. No reasoning required.
Use a medium+ model only when deciding *what* is worth logging.

---

## Directory Structure

```
memory/
  whatsapp/
    groups/
      YOUR_GROUP_JID-sanitized/    ← sanitized JID
        meta.json                 ← group name, JID, participants
        context.md                ← running conversation context
        decisions.md              ← key decisions
        people.md                 ← who participates and their role
    dms/
      972XXXXXXXXX/               ← sanitized phone number
        meta.json                 ← name, phone, relationship
        context.md                ← running DM context
        notes.md                  ← tasks, preferences, important facts

inbox/
  pending.json                    ← unanswered message tracking
```

---

## DB Mode (if PA_DB_URL is set)

If `PA_DB_URL` is available and the DB is reachable, prefer SQL over file-based operations.

### Check availability
```bash
python3 -c "
import os, psycopg2
url = os.environ.get('PA_DB_URL') or os.environ.get('HELENI_DB_URL')
if not url: exit(1)
try:
    conn = psycopg2.connect(url)
    conn.close()
    print('DB_AVAILABLE')
except: exit(1)
"
```

### Search history via SQL
```python
import os, psycopg2
url = os.environ['PA_DB_URL']
conn = psycopg2.connect(url)
cur = conn.cursor()
# Full-text search
cur.execute("""
    SELECT created_at, sender_name, chat_name, body
    FROM wa_messages
    WHERE body ILIKE %s
    ORDER BY created_at DESC LIMIT 20
""", ('%search_term%',))
for row in cur.fetchall():
    print(row)
conn.close()
```

### Find unanswered messages via SQL
```python
import os, psycopg2
url = os.environ['PA_DB_URL']
conn = psycopg2.connect(url)
cur = conn.cursor()
cur.execute("""
    SELECT chat_id, chat_name, MAX(created_at) as last_msg, COUNT(*) as unread
    FROM wa_messages
    WHERE is_from_me = false
      AND chat_id NOT IN (
          SELECT DISTINCT chat_id FROM wa_messages
          WHERE is_from_me = true
            AND created_at > NOW() - INTERVAL '24 hours'
      )
      AND created_at > NOW() - INTERVAL '24 hours'
    GROUP BY chat_id, chat_name
    ORDER BY last_msg DESC
""") 
for row in cur.fetchall():
    print(row)
conn.close()
```

### Log is automatic
When DB mode is active, the `wa-audit-log` hook writes every message to `wa_messages` automatically. No manual logging needed.

### File fallback
If `PA_DB_URL` is unset or DB is unreachable, use the file-based approach: `inbox/pending.json` and `memory/whatsapp/` context files (existing behavior below).

### Recall & Missing Context Rule
For questions like "what happened", "what did X say", "what did we decide", or "אין לי הקשר": do not rely on context files alone.

Check in this order when relevant:
1. durable memory / wiki
2. semantic-vector memory
3. PostgreSQL WhatsApp history
4. local `memory/whatsapp/` files as supporting context

If only one layer was checked, say that explicitly. Do not ask the owner to repeat context before checking the first three layers.

---

## Production Behavioral Rules (MANDATORY)

### Reaction Protocol
- **React 👍 immediately** when receiving a task message in DM from owner — before starting work
- **React ✅ when task is complete**
- 👎 from owner = poor result — fix and log lesson

### "my pleasure / you're welcome" Rule
- When anyone says "thank you" → always reply **"my pleasure / you're welcome"** (no exceptions)

### Outbound DM Tracking Rule
- When **I initiate a DM** (not responding — I'm the one who started) → add to inbox as `"waiting_reply": true`
- At every heartbeat → check for pending outbound DMs and whether a reply came in
- If reply came → read it, update context.md, mark resolved
- If no reply after 30min → note in context.md but don't re-ping unless the owner asks
- This solves the blind spot: when the other party replies in a new session, I still track it

### Post-Send Group Monitoring Rule
- After sending a message to a group, move on immediately — do NOT wait/poll for replies
- Replies will arrive as new inbound messages and be handled in a new turn
- The heartbeat check (every 2h) catches unanswered threads

### Silence Rules (NO_REPLY)
- Casual acks from PAs: 👍, "got it", "thank you", "noted" → **NO_REPLY** unless directly asked
- Echo prevention: if sender is your own agent/number → **NO_REPLY** immediately
- In groups: only respond if directly addressed or you add genuine value

### Memory Write Rule
- After every significant interaction → write to appropriate memory file:
  - Group: `memory/whatsapp/groups/<JID-sanitized>/context.md`
  - DM: `memory/whatsapp/dms/<PHONE-sanitized>/context.md`
- Sanitize: replace `@`, `.`, `+` with `-`
- What to log: tasks assigned, decisions made, important context
- What NOT to log: casual greetings, short acks, duplicates

### ⚠️ CONTEXT RULE (MANDATORY — every conversation)
**After every significant exchange** — incoming OR outgoing — create or update the DM context file.
This is not optional. Sessions restart constantly. Without a context file, you have zero memory of who this person is or what was discussed.

**Triggers:**
- You send a message to someone → write context immediately
- Someone messages you → read existing context first, then update after replying
- Decision made / task assigned / status changed → update context

Template:
```
mkdir -p memory/whatsapp/dms/<PHONE>/
# Write to memory/whatsapp/dms/<PHONE>/context.md:
# Name, role, last interaction date, what was discussed, current status
```

**No exceptions. Every DM = a context file.**

---

## Part 1: Conversation Memory

### Setup

```bash
init_whatsapp_memory() {
  TYPE="$1"       # "group" or "dm"
  ID="$2"         # JID or phone number
  NAME="$3"       # Human-readable name

  SAFE_ID=$(echo "$ID" | tr '@.+' '---')

  if [ "$TYPE" = "group" ]; then
    DIR="$HOME/.openclaw/workspace/memory/whatsapp/groups/$SAFE_ID"
    mkdir -p "$DIR"
    cat > "$DIR/meta.json" << EOF
{"type": "group", "jid": "$ID", "name": "$NAME", "created": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"}
EOF
    touch "$DIR/context.md" "$DIR/decisions.md" "$DIR/people.md"
  else
    DIR="$HOME/.openclaw/workspace/memory/whatsapp/dms/$SAFE_ID"
    mkdir -p "$DIR"
    cat > "$DIR/meta.json" << EOF
{"type": "dm", "phone": "$ID", "name": "$NAME", "created": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"}
EOF
    touch "$DIR/context.md" "$DIR/notes.md"
  fi

  echo "Initialized WhatsApp memory: $NAME"
}

# Examples:
# init_whatsapp_memory "group" "YOUR_GROUP_JID@g.us" "PA Team"
# init_whatsapp_memory "dm" "+PHONE_NUMBER" "Contact Name"
```

### Writing Memory

```bash
wa_log() {
  TYPE="$1"                        # "group" or "dm"
  ID="$2"                          # JID or phone
  CONTENT="$3"                     # what to log
  FILE_NAME="${4:-context.md}"     # context.md / decisions.md / notes.md

  SAFE_ID=$(echo "$ID" | tr '@.+' '---')
  BASE="$HOME/.openclaw/workspace/memory/whatsapp"

  if [ "$TYPE" = "group" ]; then
    FILE="$BASE/groups/$SAFE_ID/$FILE_NAME"
  else
    FILE="$BASE/dms/$SAFE_ID/$FILE_NAME"
  fi

  if [ ! -f "$FILE" ]; then
    mkdir -p "$(dirname "$FILE")"
    touch "$FILE"
  fi

  echo "[$(date -u +%Y-%m-%d\ %H:%M)] $CONTENT" >> "$FILE"
}
```

### Reading Memory

```bash
wa_context() {
  TYPE="$1"
  ID="$2"
  LINES="${3:-20}"

  SAFE_ID=$(echo "$ID" | tr '@.+' '---')
  BASE="$HOME/.openclaw/workspace/memory/whatsapp"

  if [ "$TYPE" = "group" ]; then
    DIR="$BASE/groups/$SAFE_ID"
  else
    DIR="$BASE/dms/$SAFE_ID"
  fi

  if [ ! -d "$DIR" ]; then
    echo "No memory for this conversation yet."
    return
  fi

  NAME=$(python3 -c "
import json
with open('$DIR/meta.json') as f:
    print(json.load(f).get('name', '?'))
" 2>/dev/null || echo "?")

  echo "=== $NAME ==="
  echo "--- Recent ---"
  tail -"$LINES" "$DIR/context.md" 2>/dev/null || echo "(empty)"
  echo "--- Notes/Decisions ---"
  cat "$DIR/notes.md" "$DIR/decisions.md" 2>/dev/null | tail -10 || echo "(none)"
}
```

### Search Across All Memory

```bash
wa_search() {
  QUERY="$1"
  BASE="$HOME/.openclaw/workspace/memory/whatsapp"

  echo "Searching WhatsApp memory for: '$QUERY'"
  grep -r "$QUERY" "$BASE" --include="*.md" -l 2>/dev/null | while read file; do
    DIR=$(dirname "$file")
    NAME=$(python3 -c "
import json
with open('$DIR/meta.json') as f:
    print(json.load(f).get('name', '?'))
" 2>/dev/null || echo "?")
    echo "Found in: $NAME"
    grep -n "$QUERY" "$file" | head -3
    echo ""
  done
}
```

### What to Log

| File | Use for |
|---|---|
| context.md | Ongoing conversation events, tasks assigned |
| decisions.md | Agreed outcomes, group decisions |
| people.md | Who's in the group, their role/style |
| notes.md | DM tasks, owner preferences, follow-ups |

Never log: casual greetings, duplicate info, credentials.

### Before Responding — Inject Context

```
1. Extract JID or phone from inbound metadata
2. If group: run wa_context "group" "$JID" 10
   If DM:    run wa_context "dm" "$PHONE" 10
3. Use context to inform your response
4. After responding: log anything worth remembering
```

---

## Part 2: Unanswered Message Tracking

Inbox file: `/path/to/workspace/inbox/pending.json`

### File Structure

```json
{
  "version": 1,
  "messages": [
    {
      "id": "MSG_ID",
      "ts": "2026-04-02T10:00:00Z",
      "chat_id": "+972XXXXXXXXX",
      "chat_name": "Owner",
      "chat_type": "direct",
      "sender_name": "Owner",
      "sender_phone": "+972XXXXXXXXX",
      "body": "message text...",
      "answered": false,
      "answered_at": null
    }
  ]
}
```

### Log an Incoming Message

```python
import json, datetime

INBOX = "/path/to/workspace/inbox/pending.json"

with open(INBOX) as f:
    data = json.load(f)

data["messages"].append({
    "id": "<message_id>",
    "ts": datetime.datetime.utcnow().isoformat() + "Z",
    "chat_id": "<chat_id>",
    "chat_name": "<chat_name>",
    "chat_type": "direct",  # or "group"
    "sender_name": "<sender_name>",
    "sender_phone": "<sender_phone>",
    "body": "<message body, max 300 chars>",
    "answered": False,
    "answered_at": None
})

with open(INBOX, "w") as f:
    json.dump(data, f, indent=2)
```

### Mark as Answered

```python
import json, datetime

INBOX = "/path/to/workspace/inbox/pending.json"

with open(INBOX) as f:
    data = json.load(f)

for msg in data["messages"]:
    if msg["id"] == "<message_id>":
        msg["answered"] = True
        msg["answered_at"] = datetime.datetime.utcnow().isoformat() + "Z"

with open(INBOX, "w") as f:
    json.dump(data, f, indent=2)
```

### Find Unanswered (Last 24h)

```python
import json
from datetime import datetime, timedelta, timezone

INBOX = "/path/to/workspace/inbox/pending.json"
MAX_AGE_HOURS = 24

with open(INBOX) as f:
    data = json.load(f)

cutoff = datetime.now(timezone.utc) - timedelta(hours=MAX_AGE_HOURS)
unanswered = [
    m for m in data["messages"]
    if not m["answered"]
    and datetime.fromisoformat(m["ts"].replace("Z", "+00:00")) > cutoff
]

for m in sorted(unanswered, key=lambda x: x["ts"]):
    ts = datetime.fromisoformat(m["ts"].replace("Z", "+00:00")).strftime("%d/%m %H:%M")
    print(f"📩 {m['sender_name']} | {m['chat_name']} | {ts}")
    print(f"   > {m['body'][:100]}")
```

### Heartbeat Integration

During heartbeat, check for unanswered messages from the last 2 hours:

```python
import json
from datetime import datetime, timedelta, timezone

INBOX = "/path/to/workspace/inbox/pending.json"

with open(INBOX) as f:
    data = json.load(f)

cutoff = datetime.now(timezone.utc) - timedelta(hours=2)
unanswered = [
    m for m in data["messages"]
    if not m["answered"]
    and datetime.fromisoformat(m["ts"].replace("Z", "+00:00")) > cutoff
]

if unanswered:
    for m in unanswered:
        print(f"⚠️ No reply to {m['sender_name']}: {m['body'][:80]}")
```

### Cleanup (Weekly)

```python
import json
from datetime import datetime, timedelta, timezone

INBOX = "/path/to/workspace/inbox/pending.json"

with open(INBOX) as f:
    data = json.load(f)

cutoff = datetime.now(timezone.utc) - timedelta(days=7)
data["messages"] = [
    m for m in data["messages"]
    if not m["answered"]
    or datetime.fromisoformat(m["ts"].replace("Z", "+00:00")) > cutoff
]

with open(INBOX, "w") as f:
    json.dump(data, f, indent=2)
```

---

## Loop Prevention Rules (CRITICAL)

### Context Isolation
**NEVER** share information across chat contexts:
- Internal status updates → send ONLY to owner, NEVER to other contacts
- Task details from owner's DM → never mention to third parties
- When replying to person X → do NOT include context from conversation with person Y
- Progress reports → owner in private DM only
- ❌ Never write "To the owner:" or any internal framing inside a message to a third party
- ❌ Never include the owner's name or intent in outbound messages to PAs or contacts

### Close the Loop With the Requester
When the owner asks you to check in with someone:
- Contact the person ✔️
- Report back to the owner what they said ✔️
- ❌ Do NOT swallow the answer — the owner asked because they want to know
- Always use [[reply_to_current]] when responding to a specific person's message — this is mandatory, not optional
- ❌ Never respond to a message without [[reply_to_current]] when the context is a specific inbound message

### Echo Prevention
Before responding to ANY message, check `sender_id` from inbound metadata.
- If sender is your own agent/number → **NO_REPLY** immediately.

### No Duplicate Sends
Before sending to a group or DM:
- Check if identical message was already sent in this session
- If yes → skip.

### Verify Recipient Before Sending (MANDATORY)
- Before every send (group or DM), verify the JID/phone against MEMORY.md
- If JID/phone not found in MEMORY.md → ask before sending, never guess
- Never infer a JID from a group name alone — look it up
- When owner says "send to X" → look up X in MEMORY.md contacts/JIDs first
- ❌ Do NOT send to the first matching name/number that comes to mind

### Multi-PA Coordination
- Only ONE PA should respond to each group message
- If another PA already responded → stay silent (NO_REPLY)
- Never impersonate another PA without disclosure
- Give other PAs time before intervening

---

## Integration

- **Before each response** → load context via `wa_context`
- **After important exchanges** → log to context.md / notes.md
- **With git-backup** → push after memory updates
- **With owner-briefing** → include DM follow-ups in morning briefing
- **Heartbeat** → check inbox for unanswered messages every 2h

---

## Cost Tips

- All memory operations are file reads/writes — no LLM tokens
- Use `tail -10` instead of reading full context files
- Batch log multiple events before pushing backup
- Small model OK for all memory operations

---

## Troubleshooting

Use this section when the agent is not responding to WhatsApp messages.

**Step 1 — Classify the problem:**
- Dashboard shows "Disconnected" → **Connection issue**: re-link WhatsApp in OpenClaw settings, scan QR code with WhatsApp Business app. Session expires after ~14 days of inactivity.
- Dashboard shows "Connected" but Messages = 0 → **Ingest issue**: run `openclaw gateway restart`, wait 30s, check if count increments.
- Messages count increments but no reply → **Runtime issue**: check billing and API key.

**Step 2 — Fix ingest issues (Messages = 0):**
```bash
openclaw gateway status
openclaw gateway restart
# Wait 30 seconds, then test
openclaw gateway logs --last 50  # Look for: binding failed, session dropped, ingest error
```
If errors persist → escalate to platform admin (infrastructure issue).

**Step 3 — Fix runtime issues (no reply despite incoming messages):**
```bash
# Check for billing errors
grep -i "billing\|402\|credits" ~/.openclaw/logs/agent.log | tail -20

# Verify API key (expect HTTP 200)
curl -s -o /dev/null -w "%{http_code}" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  https://api.anthropic.com/v1/models
# 200 = OK | 401 = invalid key | 402 = billing error
```

**Prevention:**
- Send at least one message every 7 days to prevent session expiry
- Check Messages count during heartbeat to catch ingest issues early
- Never use the same phone number on two devices simultaneously

**When to escalate:** Gateway restart doesn't fix Messages = 0, logs show `socket`/`binding`/`session` errors, or multiple agents affected at the same time.
