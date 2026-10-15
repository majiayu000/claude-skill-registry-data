---
name: libr-delegate
description: >
  Delegate work to a running LibrAgent desktop/headless instance via the local
  HTTP Session API (`POST /api/sessions`, messages, status, children, resume,
  terminate, delete). Use from Cursor (or other external harnesses) when
  LibrAgent is up and you need a LibrAgent session to run a task — optionally
  with `parentSessionId` lineage. After work: extract message history
  (session transcript / API-side "trace"), then terminate+delete one-shot
  sessions. Triggers: Session API, /api/sessions, parentSessionId, curl
  session, HTTP delegate to LibrAgent, "LibrAgent에 위임", "세션 API로 자식
  띄워", Harbor/bench spawn, session cleanup, delete session, extract
  transcript. NEVER for LibrAgent-internal `agent__spawnSession` flows (that
  is the in-app `delegate` skill). NEVER invent MCP tool names here.
---

# Libr Delegate (Cursor → LibrAgent Session API)

Spawn and steer **LibrAgent** sessions over HTTP from Cursor. LibrAgent must
already be running (desktop or headless). This skill does **not** ship into
LibrAgent `bundled_skills`.

## vs in-app `delegate`

| Caller | Mechanism |
| --- | --- |
| Cursor / scripts / Harbor | **This skill** → HTTP `/api/sessions` |
| Inside a LibrAgent agent turn | In-app **`delegate`** → `agent__*` tools |

## Base URL

```bash
PORT=$(cat ~/.libragent/http_port 2>/dev/null || echo 3030)
BASE="http://127.0.0.1:${PORT}"
```

Port file is written when LibrAgent’s HTTP server binds; fallback is `3030`.

## Workflow

1. Confirm LibrAgent is up — `GET $BASE/api/health` (or assistants list)
2. Resolve `assistantId` — `GET $BASE/api/assistants`
3. Write a self-contained handoff (LibrAgent child does **not** see Cursor
   chat, parent workspace instructions, or workspace-local skills unless you
   pass an absolute `workspacePath`)
4. Create — write JSON payload to a file, **validate non-empty JSON**, then
   `POST $BASE/api/sessions` (include `request` or create idle). See
   `references/session-api.md` (preferred file recipe + empty-body guard)
5. If idle — `POST $BASE/api/sessions/:id/messages` with `{"content":"..."}`
6. Poll — `GET $BASE/api/sessions/:id` until terminal (prefer
   `scripts/poll-until-done.sh`)
7. Read result — `GET $BASE/api/sessions/:id/messages`
8. On paused after crash — `POST …/resume`, then poll again
9. Optional lineage — set `parentSessionId`; list with `GET …/children`
10. **Extract transcript before delete** — dump
    `GET …/messages?limit=500` to a file (see below)
11. **Cleanup one-shot sessions** — `POST …/terminate` then
    `DELETE …/sessions/:id` (delete cascades descendants)

Curl recipes: `references/session-api.md`. Handoff / isolation:
`references/handoff.md`. Poll helper: `scripts/poll-until-done.sh`.

## Extract transcript (API-side "trace") then delete

There is **no** HTTP `/api/sessions/:id/trace` and no ATIF/Markdown export
endpoint on the Session API. UI session export (Markdown / ATIF) is separate.
For Cursor/harness handoffs, the recoverable history is message JSON:

```bash
# After idle (or error) — save BEFORE delete
curl -sS "$BASE/api/sessions/$SID/messages?limit=500" \
  > ".libragent/work/libr-delegate-${SID}-messages.json"
```

- Default `limit` is 50 — use a high limit for full history
- Treat latest assistant `text` as the deliverable; keep the JSON dump when
  debugging tool calls / failures (role `user` | `assistant` | `tool`)
- Optional deeper analysis of a dumped file: Cursor skill `trace-analyzer`
  expects `.trace.json` shape — only use it if the dump matches that format;
  otherwise inspect the messages JSON directly
- **Order matters**: extract → terminate → DELETE. Delete removes DB history

One-shot / automation default: always extract (or confirm you only need the
final assistant text) then terminate+delete so sessions do not accumulate.

## Create payload essentials

```json
{
  "assistantId": "<from GET /api/assistants>",
  "request": "<self-contained task + deliverable format>",
  "workspacePath": "/absolute/path/optional",
  "parentSessionId": "<optional exact parent session id>",
  "executionMode": "normal | yolo | unsafe",
  "name": "optional label"
}
```

- Blank/omit `request` → idle (no LLM turn until messages POST)
- Unattended automation: prefer `yolo`; use `unsafe` only when hard-approval
  tools must also auto-run
- Child inherits non-`normal` parent `executionMode` when omitted on create

## Polling rules

**Wire `status` is always lowercase** (`serde(rename_all = "lowercase")`):
`idle` | `busy` | `paused` | `error` | `queued` | `provisioning`.

| Status (wire) | Action |
| --- | --- |
| `busy` / `queued` / `provisioning` | Wait with backoff; do not spam |
| `idle` (after work) | Read messages; treat latest assistant text as result |
| `paused` | `POST …/resume` once, then poll |
| `error` | Fail the handoff; do not claim success from partial prose |

Preferred poll (normalizes case; exits on terminal):

```bash
./.agents/skills/libr-delegate/scripts/poll-until-done.sh "$SID" "$BASE"
```

If writing a one-off loop, **lowercase before match**:

```bash
status=$(curl -sS "$BASE/api/sessions/$SID" \
  | python3 -c 'import sys,json; print(json.load(sys.stdin).get("status","").lower())')
case "$status" in idle|error|paused) break ;; esac
```

Follow-ups: another `POST …/messages` (queued if still `busy`).

## Isolation (critical)

The LibrAgent session is not a clone of this Cursor chat:

- Default: LibrAgent session workspace, not the Cursor CWD unless
  `workspacePath` is set to that absolute path
- Put objective, scope, paths, and output format in `request` / message body
- Require deliverables in the session’s **final assistant text**
- Do not assume Cursor files, notes, or tools are visible inside LibrAgent

## Anti-patterns

- Calling nonexistent MCP tools (`spawnSession`, `session_api__*`) from Cursor
- Echo-only stubs instead of real `POST …/messages`
- Rapid fixed-interval polls with no backoff
- Matching PascalCase statuses (`Idle`/`Busy`) — API returns `idle`/`busy`;
  a `case Idle)` branch never fires and the poll loops until timeout even
  after the session finished (postmortem: editObject smoke, 2026-04)
- Treating paused / empty history / error as success
- Deleting a session before saving `…/messages` when a transcript is needed
- Assuming `~/.libragent/traces/*.trace.json` or `/api/.../trace` exists
  (they are not part of the Session API)
- Leaving one-shot delegate sessions undeleted after the handoff completes
- Putting this skill under `src-tauri/bundled_skills` (Cursor-only)
- Referencing shell vars as bare Python names inside `<<'PY'` (e.g.
  `workspacePath: WORKSPACE`) → `NameError` → empty payload file → create
  400 `EOF while parsing a value`
- `curl -d @file` without checking the file is non-empty valid JSON first

## Related repo docs

- HTTP API: `docs/api/http_api.md`
- In-app sub-agents (product): `docs/user/guides/sub-agents.md`
