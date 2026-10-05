---
name: session-conversation
description: Send messages to and receive replies from another active opencode session. Use when orchestrating multi-session dialogues, relaying turns between two sessions, or injecting a user message into a separately running session.
---

# Session Conversation Skill

This skill enables one opencode session to send messages to and receive replies from another session — enabling inter-session communication, multi-agent dialogues, and cross-session orchestration.

## How It Works

There are two ways to inject a message into another session. **Pick based on the target's agent:**

| Method | Works with primary agents (e.g. Sisyphus)? | Use when |
|---|---|---|
| **A — `task(session_id=...)`** | ❌ No — errors `Cannot delegate to primary agent "..." via task` | Target runs a delegatable **subagent** you spawned |
| **B — opencode web HTTP API** | ✅ Yes — no agent restriction | Target runs **any** agent, including primary Sisyphus (the common case) |

Most interactive sessions run a primary agent (Sisyphus), so **Method B is the default**. Method A is only viable for subagent sessions.

Both deliver the message as a normal user turn; the target processes it and returns its response. Method B is also cross-project: the opencode web server addresses **every** session by ID regardless of which project directory it lives in.

## Step 1 — Find the Target Session

### Option A: session_list (current project, fast)

```typescript
session_list(limit=20)
```

Returns sessions scoped to the current working directory. Check the title and agent columns to identify the right one.

### Option B: find-session skill (cross-project, SQLite)

Load the `find-session` skill for cross-project search. Or query directly:

```bash
sqlite3 ~/.local/share/opencode/opencode.db \
  "SELECT id, title, directory, datetime(time_updated/1000,'unixepoch') as last_active
   FROM session
   ORDER BY time_updated DESC
   LIMIT 20;"
```

### Option C: Verify identity before sending

Read the first few messages to confirm it's the right session:

```typescript
session_read(session_id="ses_abc123", limit=5)
```

Check the opening messages — the user typically sets the session's role/instructions there.

## Step 2 — Send a Message

### Method B — opencode web HTTP API (RECOMMENDED; works with Sisyphus)

The `opencode web` server exposes a REST API that injects a message into any session by ID, with **no primary-agent restriction**. This is how the web UI itself sends messages, so it works for Sisyphus and every other agent.

**1. Find the opencode web server port** (default `4096`; discover if not running there):

```bash
# Default is 4096. To discover: probe opencode listening ports for the one that serves /session.
PORT=4096
for p in 4096 $(lsof -nP -iTCP -sTCP:LISTEN 2>/dev/null | grep -i opencode \
      | grep -oE '127\.0\.0\.1:[0-9]+' | cut -d: -f2 | sort -u); do
  if curl -s -m 2 "http://127.0.0.1:$p/session" | grep -q '"id":"ses_'; then PORT=$p; break; fi
done
echo "opencode web port: $PORT"
```

**2. POST the message** — only `parts` is required; the session reuses its own agent + model:

```bash
SID=ses_abc123
curl -s -m 180 -X POST "http://127.0.0.1:$PORT/session/$SID/message" \
  -H 'content-type: application/json' \
  -d '{"parts":[{"type":"text","text":"Your message here"}]}'
```

The call blocks until the target finishes its turn, then returns the full assistant message as JSON (text is in `.parts[].text`). Extract the reply:

```bash
curl -s -m 180 -X POST "http://127.0.0.1:$PORT/session/$SID/message" \
  -H 'content-type: application/json' \
  -d '{"parts":[{"type":"text","text":"Your message here"}]}' \
  | python3 -c "import sys,json;print(''.join(p.get('text','') for p in json.load(sys.stdin)['parts'] if p.get('type')=='text'))"
```

Verify the target is reachable first with `GET /session/$SID` (returns its `title` and `agent`).

### Method A — `task(session_id=...)` (subagent sessions only)

Only works if the target runs a delegatable subagent. Against a primary agent (Sisyphus) it errors `Cannot delegate to primary agent "..." via task`.

```typescript
task(
  session_id="ses_abc123",                  // target session ID
  subagent_type="Sisyphus (Ultraworker)",   // must match the agent in that session
  load_skills=[],
  run_in_background=false,                  // MUST be false — see Limitations
  description="Brief label for this turn",
  prompt="Your message here"
)
```

The call blocks until the target session responds. The full response text is returned.

## Step 3 — Continue the Conversation

Repeat the same call with the same `session_id` for each subsequent turn. The session retains full context across calls — no re-introduction needed.

```bash
# Method B — each POST to the same SID is one more turn; context is preserved
curl -s -X POST "http://127.0.0.1:$PORT/session/$SID/message" \
  -H 'content-type: application/json' \
  -d '{"parts":[{"type":"text","text":"Follow-up based on their reply"}]}'
```

## Multi-Session Dialogue Pattern

To orchestrate a back-and-forth between two independently running sessions (e.g. Bot A and Bot B), the **orchestrating session acts as the relay**:

```
User
 └─► Session A (you, the orchestrator)
       ├─► task(session_id=B) → B replies
       ├─► formulate A's response
       ├─► task(session_id=B) → B replies again
       └─► ... repeat for N turns
```

Each POST (Method B) or `task()` call (Method A) is one conversational turn. You receive B's reply, generate A's next message, and send it back. Display both sides to the user as you go.

```bash
# Method B relay — orchestrator drives each turn against Bot B's session
SID_B=ses_B
reply=$(curl -s -X POST "http://127.0.0.1:$PORT/session/$SID_B/message" \
  -H 'content-type: application/json' \
  -d '{"parts":[{"type":"text","text":"<A'\''s message>"}]}' \
  | python3 -c "import sys,json;print(''.join(p.get('text','') for p in json.load(sys.stdin)['parts'] if p.get('type')=='text'))")
# Show both sides, formulate A's next message from $reply, repeat for N turns
```

## Limitations

### Method B (HTTP API)

| Limitation | Detail |
|---|---|
| Requires `opencode web` running | The REST server must be up (default port `4096`). If no port serves `/session`, start it with `opencode web`. |
| Sequential turns | The POST blocks until the target finishes its turn. No passive push/subscribe — drive each turn explicitly. |
| Local only | Server binds to `127.0.0.1`. Cross-machine is not supported. |
| Triggers a real turn | The target actually processes the message and incurs cost. Use `"noReply": true` in the body to inject a user message without triggering a response. |

### Method A (`task(session_id=...)`)

| Limitation | Detail |
|---|---|
| Primary agents blocked | Errors `Cannot delegate to primary agent "..." via task`. Sisyphus is primary, so Method A does **not** work for it — use Method B. |
| `run_in_background=true` fails | Error: "Task not found for session". Always use `run_in_background=false`. |
| `subagent_type` must match | Must match the subagent running in the target session. |
| Same process only | Both sessions must be running in the same opencode process/instance. |

## Worked Example (Method B — verified against a live Sisyphus session)

```bash
# 1. Find the target session (cross-project) via the find-session skill / SQLite
sqlite3 ~/.local/share/opencode/opencode.db \
  "SELECT id, title, directory FROM session WHERE title LIKE '%sandbox%' ORDER BY time_updated DESC LIMIT 5;"
# → ses_19eab2b32ffe0PftUbk85Lttj7 | sandbox | /Users/rs/Bunch/code/apps

# 2. Find the opencode web port and confirm identity (returns title + agent)
PORT=4096
SID=ses_19eab2b32ffe0PftUbk85Lttj7
curl -s "http://127.0.0.1:$PORT/session/$SID" | python3 -c "import sys,json;d=json.load(sys.stdin);print(d['title'],'|',d['agent'])"
# → sandbox | Sisyphus - ultraworker   (a PRIMARY agent — task() would refuse this)

# 3. Inject the message — works despite the primary agent
curl -s -X POST "http://127.0.0.1:$PORT/session/$SID/message" \
  -H 'content-type: application/json' \
  -d '{"parts":[{"type":"text","text":"test"}]}' \
  | python3 -c "import sys,json;print(''.join(p.get('text','') for p in json.load(sys.stdin)['parts'] if p.get('type')=='text'))"
# → test   (HTTP 200 — round-trip confirmed)

# 4. Repeat step 3 with the same SID for each further turn; context is preserved.
```

## Related Skills

- `find-session` — locate sessions across all projects via SQLite when `session_list` is insufficient
