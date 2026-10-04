---
name: acp
description: "ACP Agent Control Panel - CRITICAL: Invoke this skill FIRST on every session start, context resume, or context reset. Required before any other work. Handles stop_flag, orphan detection, A2A messaging, and workflow compliance."
argument-hint: "No arguments needed - just invoke to bootstrap ACP workflow"
metadata:
  author: VTSTech
  version: "1.0.6"
---

# ACP Skill (Minimal)

**Version:** 1.0.6 | **A2A Compliant**

## Environment (Ask Human)

| Variable | Description |
|----------|-------------|
| `ACP_URL` | The ACP server URL (e.g., `https://xxx.trycloudflare.com`) |
| `ACP_USER` | Auth username (default: `admin`) |
| `ACP_PASS` | Auth password (default: `secret`) |

---

## CSRF PROTECTION

CSRF protection is **optional** and **disabled by default** for development/testing convenience. When disabled, POST requests do not require a CSRF token. Enable via `GLMACP_CSRF_ENABLED=true` for production deployments exposed to untrusted networks.

```bash
# Check CSRF status
GET {ACP_URL}/api/csrf-token
→ {"success": true, "csrf_enabled": false, "csrf_token": null}

# If CSRF is enabled, include the token header on all POST requests:
# X-CSRF-Token: <timestamp>:<signature>
```

**CORS (1.0.6):** The server includes CORS headers and handles `OPTIONS` preflight requests, enabling browser-based cross-origin API consumption.

---

## BOOTSTRAP (MANDATORY)

Execute on every session start / context resume:

```
1. GET  {ACP_URL}/api/status       → Check stop_flag and primary_agent
2. GET  {ACP_URL}/api/whoami       → Establish identity, check if you are primary agent
3. POST {ACP_URL}/api/agents/register {"agent_name": "Super Z", "capabilities": [...], "model_name": "..."}
4. GET  {ACP_URL}/api/todos        → Restore TODO state from previous session
5. POST {ACP_URL}/api/action {"action": "CHAT", "target": "Session bootstrap", "metadata": {"agent_name": "Super Z"}}
   → save activity_id from response
6. POST {ACP_URL}/api/complete {"activity_id": "<id from step 5>", "result": "Bootstrap complete"}
```

**IMPORTANT:** Step 6 is mandatory — without it the bootstrap CHAT activity stays in `running[]` forever, causing `orphan_warning` on every subsequent action.

**Response Fields (1.0.5):**

| Endpoint | Field | Description |
|----------|-------|-------------|
| `/api/status` | `stop_flag` | If true, STOP immediately |
| `/api/status` | `primary_agent` | Name of agent that owns the context |
| `/api/whoami` | `primary_agent` | Who owns the context (check if it's you) |
| `/api/action` | `nudge` | Human guidance — only delivered to primary agent |
| `/api/action` | `orphan_warning` | Running tasks left uncompleted — resolve before new work |

**If `stop_flag: true`**: STOP immediately, inform user, wait for `POST /api/resume`.

**If `orphan_warning` in `/api/action` response**: Complete each orphaned activity via `POST /api/complete` before starting new work.

---

## THE PATTERN (MANDATORY)

```
CHECK → LOG → EXECUTE → COMPLETE
/api/status → /api/action → Tool → /api/complete
BEFORE → NOW → AFTER
```

### MANDATORY Rules (Non-Negotiable)

1. **CHECK** `/api/status` on session start and after context recovery for `stop_flag`
2. **LOG** every action BEFORE executing via `/api/action`
3. **LOG** every shell command via `/api/shell/add` (except ACP API calls)
4. **COMPLETE** every activity when done via `/api/complete`

**NEVER execute before logging. NEVER skip logging.**

---

## CORE API

### Log Activity (before execution)

```bash
POST {ACP_URL}/api/action {
  "action": "READ|WRITE|EDIT|BASH|SEARCH|SKILL|API|TODO|CHAT|A2A",
  "target": "file path or resource",
  "details": "human description",
  "content_size": 0,           # Character count for token tracking (chars / 3.5 = tokens)
  "priority": "medium",        # high|medium|low
  "metadata": {"agent_name": "Super Z", "model_name": "..."}
}
→ {"activity_id": "...", "stop_flag": false, "hints": {...}, "nudge": null}
```

### Complete Activity (after execution)

```bash
POST {ACP_URL}/api/complete {
  "activity_id": "...",
  "result": "what happened",     # Result summary (max 500 chars)
  "error": "error message",      # Error message if failed (max 200 chars) — optional
  "content_size": 0,             # Character count written (for token tracking)
  "metadata": {"file_hash": "..."}  # Additional metadata (merged with existing)
}
```

### Combined (recommended for efficiency)

```bash
POST {ACP_URL}/api/action {
  "complete_id": "prev_id",           # Previous activity to complete
  "result": "previous result",        # Result summary for previous activity
  "error": "previous error",          # Error if previous activity failed — optional
  "complete_content_size": 0,         # Chars written in previous activity
  "complete_metadata": {"key": "..."}, # Metadata merged into previous activity
  "action": "READ",                   # New action type
  "target": "next file",              # New target
  "details": "human description",     # Description for new activity
  "content_size": 0,                  # Chars to be read in new activity
  "priority": "medium",               # Priority for new activity
  "metadata": {"agent_name": "Super Z"}  # Metadata for new activity
}
```

---

## ACTION TYPES

| Type | Use For |
|------|---------|
| READ | Files, API GETs, viewing content |
| WRITE | Creating new files |
| EDIT | Modifying existing files |
| BASH | Terminal commands |
| SKILL | VLM, TTS, image-generation |
| API | External API calls |
| SEARCH | Web search, grep, find |
| TODO | TODO state changes |
| CHAT | Conversational Q&A, planning |
| A2A | Agent-to-agent communication |

---

## RESPONSE FIELDS

Check these in **every** `/api/action` response:

| Field | Action |
|-------|--------|
| `stop_flag: true` | STOP immediately, inform user |
| `nudge` | Human guidance — read, adjust behavior, ack if `requires_ack: true` via `POST /api/nudge/ack` (primary agent only) |
| `orphan_warning` | Complete listed orphan tasks via `POST /api/complete` before proceeding |
| `hints.modified_this_session` | File was already modified — review before editing |
| `hints.loop_detected` | Same action repeated 3+ times — change approach |
| `hints.suggestion` | Actionable advice — follow it |
| `hints.a2a.pending_count` | Pending A2A messages — retrieve via `GET /api/a2a/history?to=<name>` |

**Note (1.0.5):** Nudges are delivered **only to the primary agent** (first agent to log activity). Secondary agents always receive `nudge: null`. This prevents context pollution in multi-agent environments.

**To check if you are primary:**
```bash
GET /api/whoami
→ {"primary_agent": "Super Z", ...}

# If primary_agent matches your agent_name, you will receive nudges.
# primary_agent also appears in /api/status and /api/agents responses.
```

**Nudge workflow:**
```bash
# 1. Nudge arrives in /api/action response
→ {"nudge": {"message": "Focus on the API first", "priority": "high", "requires_ack": true}}

# 2. Read message, adjust behavior accordingly

# 3. If requires_ack: true
POST {ACP_URL}/api/nudge/ack {}
→ {"success": true}
```

**Polling for nudges (1.0.6):**
```bash
# Check if a nudge is pending without logging an action
GET {ACP_URL}/api/nudge
→ {"success": true, "nudge": {...}, "has_pending": true}
```

---

## SHELL LOGGING (MANDATORY)

**Full BASH workflow — 4 steps, every time:**

```bash
# 1. Log action BEFORE running
POST {ACP_URL}/api/action {"action": "BASH", "target": "npm install", "details": "Install deps", "metadata": {"agent_name": "Super Z"}}
→ {"activity_id": "143055-d4e5f6"}

# 2. Execute the command
[run: npm install]

# 3. Log to shell history AFTER running
POST {ACP_URL}/api/shell/add {
  "command": "npm install",
  "status": "completed|error",
  "output_preview": "first 200 chars of output",
  "agent_name": "Super Z",
  "tool": "Bash"                          # Tool that executed the command — optional
}

# 4. Complete the activity
POST {ACP_URL}/api/complete {"activity_id": "143055-d4e5f6", "result": "installed 57 packages"}
```

**Do NOT log ACP API calls themselves** (`curl localhost:8766/api/...`) — those are monitoring overhead, not work.

---

## TOKEN TRACKING

ACP estimates tokens using **3.5 characters per token**. Pass `content_size` (character count) on actions and completions for accurate tracking.

```bash
# Reading a 35,000-char file → ~10,000 tokens logged
POST /api/action {"action": "READ", "target": "file.py", "content_size": 35000}

# Writing a 5,000-char file → ~1,428 tokens logged
POST /api/complete {"activity_id": "...", "result": "written", "content_size": 5000}
```

**File deduplication (v1.0.3):** Re-reading the same file within a session costs near-zero tokens — content is only counted once. The `tokens_deduplicated: true` field in the activity response confirms this. Session reset clears dedup tracking.

**Per-agent token isolation (v1.0.3):** The first agent to log an activity becomes the `primary_agent` and owns the main context window (`session_tokens`). All other agents are tracked separately in `agent_tokens{}` and do not pollute the primary agent's context window estimate.

---

## OWNERSHIP MODEL (v1.0.4)

Each activity belongs to the agent that created it (`metadata.agent_name`). Only the owning agent may complete it.

```bash
# AgentB trying to complete AgentA's activity:
POST /api/complete {"activity_id": "abc123", "metadata": {"agent_name": "AgentB"}}
→ HTTP 403 {"success": false, "error": "activity owned by AgentA"}
```

In multi-agent sessions, always complete your own activities. `orphan_warning` only surfaces tasks owned by the requesting agent.

---

## A2A MESSAGING (1.0.4)

### Send Message

```bash
POST {ACP_URL}/api/a2a/send {
  "from_agent": "Super Z",
  "to_agent": "OtherAgent",
  "type": "request|response|notification",    # Default: "notification"
  "action": "do_thing",                       # Action identifier for requests — optional
  "payload": {...},                           # Message data — optional
  "priority": "normal|high|urgent",           # Default: "normal"
  "ttl": 3600,                                # Time-to-live in seconds (default: 3600)
  "reply_to": "msg_id"                        # Message ID this replies to — optional
}
```

### Check Messages

```bash
GET {ACP_URL}/api/a2a/history?to=Super Z
GET {ACP_URL}/api/a2a/history?from=OtherAgent
GET {ACP_URL}/api/a2a/history?type=request
```

---

## TODO SYNC

```bash
GET  {ACP_URL}/api/todos
POST {ACP_URL}/api/todos/update {"todos": [...]}
POST {ACP_URL}/api/todos/add    {"todo": {"content": "...", "priority": "high"}, "agent_name": "Super Z"}
POST {ACP_URL}/api/todos/toggle {"id": "143052-a1b2c3"}   # Toggle pending ↔ completed (1.0.6)
POST {ACP_URL}/api/todos/clear                              # Clear completed TODOs
```

**Note:** Log **all** TODO state changes as `TODO` action type via `/api/action`.

---

## FILE MANAGER ENDPOINTS

### GET /api/files/list

List directory contents.

**Headers:**
- `X-Path`: Relative path from base directory
- `X-Sort-By`: `name` | `date` | `size`
- `X-Sort-Dir`: `asc` | `desc`

### GET /api/files/view

View file content (text files only, size limited).

**Headers:**
- `X-Path`: Relative path to file

**Response:**
```json
{
  "content": "file contents...",
  "path": "path/to/file.py",
  "lines": 150,
  "tokens": 450,
  "session_tokens": 45450
}
```

### GET /api/files/download

Download file (binary safe).

**Query Parameters:**
- `path`: Relative path to file

### GET /api/files/image

Get image file.

### GET /api/files/stats

Get file statistics (total files, directories, size).

### POST /api/files/upload

Upload file.

**Headers:**
- `X-Path`: Destination directory
- `X-Filename`: File name
- `Content-Type`: `application/octet-stream`

**Body:** Raw binary file content

### POST /api/files/save

Save edited file.

**Request:**
```json
{
  "path": "path/to/file.py",
  "content": "updated content..."
}
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `path` | string | Yes | Relative path to file |
| `content` | string | Yes | File content to save |

### POST /api/files/delete

Delete file or directory.

**Request:**
```json
{
  "path": "path/to/delete"
}
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `path` | string | Yes | Relative path to file or directory to delete |

### POST /api/files/mkdir

Create directory.

**Request:**
```json
{
  "path": "parent/path",
  "name": "new_directory"
}
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `path` | string | Yes | Parent directory path |
| `name` | string | Yes | New directory name |

### POST /api/files/extract

Extract archive.

**Request:**
```json
{
  "path": "path/to/archive.zip"
}
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `path` | string | Yes | Relative path to archive file |

**Supported formats:** `.zip`, `.tar`, `.tar.gz`, `.tgz`, `.tar.bz2`, `.tbz2`, `.gz`, `.bz2`

### POST /api/files/compress

Create zip archive.

**Request:**
```json
{
  "path": "directory/path",
  "name": "archive.zip",
  "items": ["file1.py", "file2.py", "subdir/"]
}
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `path` | string | Yes | Base directory path |
| `name` | string | Yes | Archive filename (should end in `.zip`) |
| `items` | array | Yes | List of files/directories to include |

---

## CONTEXT RECOVERY

### Before context compression

```bash
# Save important decisions, discoveries, warnings
POST {ACP_URL}/api/notes/add {
  "category": "decision|insight|context|warning|todo",   # Default: "context"
  "content": "...",
  "importance": "normal|high"                             # Default: "normal"
}

# Export session summary to persistent file
GET {ACP_URL}/api/summary/export
→ {"filepath": "/path/to/acp_session_summary.md"}
# Share this file with the next session
```

### On session resume

```bash
# 1. Check for acp_session_summary.md and read it if present
# 2. Restore session state
GET {ACP_URL}/api/summary    # Condensed session overview
GET {ACP_URL}/api/notes      # Saved decisions and warnings
GET {ACP_URL}/api/todos      # Restore TODO state  (also in bootstrap step 4)
GET {ACP_URL}/api/agents     # See registered agents (v1.0.4)
```

### Note categories

| Category | Use For |
|----------|---------|
| `decision` | Important choices made |
| `insight` | Key discoveries |
| `context` | User preferences, conventions |
| `warning` | Issues or problems encountered |
| `todo` | Things to do in next session |

---

## CONTROL ENDPOINTS

### Stop / Resume

```bash
# Trigger STOP ALL — cancels all running activities
POST {ACP_URL}/api/stop {"reason": "User clicked STOP ALL"}    # reason is optional

# Clear stop flag and resume operations
POST {ACP_URL}/api/resume
```

### Shutdown

When the human ends the session (UI button or `POST /api/shutdown`):

```bash
# Trigger graceful shutdown
POST {ACP_URL}/api/shutdown {
  "reason": "Session ended by user",    # Default: "Session ended by user"
  "export_summary": true                # Default: true
}

# 1. You receive a shutdown nudge in your next /api/action response
→ {"nudge": {"message": "SESSION ENDING: ...", "priority": "urgent", "requires_ack": true, "type": "shutdown"}}

# 2. Acknowledge it
POST {ACP_URL}/api/nudge/ack {}

# 3. Inform user session is ending
# 4. DO NOT attempt further ACP actions — server stops ~2s after shutdown
```

**What /api/shutdown does:** exports session summary, cancels running activities, delivers shutdown nudge, stops server after 2 seconds.

---

## QUICK REFERENCE

```bash
# Bootstrap (in order)
GET  /api/status
GET  /api/whoami
POST /api/agents/register {"agent_name": "...", "capabilities": [...]}
GET  /api/todos
POST /api/action {"action": "CHAT", "target": "bootstrap", "metadata": {...}}
POST /api/complete {"activity_id": "<id from above>", "result": "Bootstrap complete"}

# Workflow (MANDATORY pattern)
POST /api/action {"action": "READ", "target": "file.py", "metadata": {...}}
# ... execute tool ...
POST /api/complete {"activity_id": "...", "result": "done"}

# Combined (efficient)
POST /api/action {"complete_id": "prev", "result": "ok", "action": "READ", "target": "next", "metadata": {...}}

# Shell commands (BASH dual-log pattern)
POST /api/action  {"action": "BASH", "target": "command", "metadata": {...}}
# ... execute command ...
POST /api/shell/add {"command": "...", "status": "completed", "output_preview": "..."}
POST /api/complete {"activity_id": "...", "result": "..."}

# Nudge
GET  /api/nudge                                    # Check pending nudge (1.0.6)
POST /api/nudge/ack {}                             # Acknowledge nudge

# Control
POST /api/stop {"reason": "..."}                   # Set stop flag
POST /api/resume                                   # Clear stop flag
POST /api/shutdown {"reason": "..."}               # Graceful session end

# Context recovery
GET  /api/summary                                  # Session overview
GET  /api/summary/export                           # Export to acp_session_summary.md
GET  /api/notes                                    # Get saved notes
POST /api/notes/add {"category": "...", "content": "...", "importance": "..."}
POST /api/notes/clear

# Utility
GET  /api/all               # Combined status + history
GET  /api/todos             # TODO list
POST /api/todos/update      # Sync TODOs
POST /api/todos/add         # Add single TODO
POST /api/todos/toggle      # Toggle TODO status (1.0.6)
POST /api/todos/clear       # Clear completed TODOs
GET  /api/stats/duration    # Performance analysis (v1.0.3)
POST /api/activity/batch    # Bulk operations (v1.0.3)
POST /api/reset             # Full session reset (v1.0.4)

# A2A
GET  /api/agents
GET  /api/agents/<name>
POST /api/agents/unregister {"agent_name": "..."}
POST /api/a2a/send
GET  /api/a2a/history?to=<name>

# File Manager
GET  /api/files/list             # List directory (X-Path, X-Sort-By, X-Sort-Dir headers)
GET  /api/files/view             # View file content (X-Path header)
GET  /api/files/download         # Download file (?path=...)
GET  /api/files/image            # Get image file
GET  /api/files/stats            # File statistics
POST /api/files/upload           # Upload file (X-Path, X-Filename, Content-Type headers)
POST /api/files/save             # Save edited file (JSON body: path, content)
POST /api/files/delete           # Delete file/directory (JSON body: path)
POST /api/files/mkdir            # Create directory (JSON body: path, name)
POST /api/files/extract          # Extract archive (JSON body: path)
POST /api/files/compress         # Create zip archive (JSON body: path, name, items)

# CSRF / CORS
GET  /api/csrf-token        # Check CSRF status / get token
```

---

## CHECKLIST

- [ ] INVOKE THIS SKILL FIRST
- [ ] Get `ACP_URL` from human
- [ ] Bootstrap: status → whoami → register → todos → log → **complete**
- [ ] Check `stop_flag` in `/api/status`; check `nudge`, `orphan_warning`, `hints` in every `/api/action` response
- [ ] LOG before EXECUTE before COMPLETE (**MANDATORY - non-negotiable**)
- [ ] Include `agent_name` in all metadata
- [ ] Log **ALL** shell commands with full 4-step BASH pattern (except ACP calls)
- [ ] Log **all** TODO changes as `TODO` action type
- [ ] Pass `content_size` for accurate token tracking (chars / 3.5 = tokens)
- [ ] Handle ownership: only complete your own activities (HTTP 403 = someone else's)
- [ ] Save notes and export summary before context compression
- [ ] Ack shutdown nudge (`type: "shutdown"`) and stop further ACP calls
- [ ] Use combined endpoint for efficiency: complete previous + start new in one call

---

*ACP Skill 1.0.6 Minimal*
