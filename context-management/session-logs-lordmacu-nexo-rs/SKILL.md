---
name: Session Logs
description: Inspect this agent's stored JSONL session transcripts — list, read, search, or recall recent turns.
requires:
  bins: []
  env: []
---

# Session Logs

Use this skill when the agent needs to look at its own prior conversations:
"what did I tell you yesterday?", "search whether we ever discussed X",
"show me the last 5 things from this session". Reads the JSONL transcripts under
`transcripts_dir` (Phase 10.4 writes them).

## Use when

- Self-reflection: "what did I commit to in the previous chat?"
- Debugging: "what tool result did I see in session X?"
- Lightweight search across the agent's history
- Replaying recent turns when memory/workspace is insufficient

## Do not use when

- Long-term semantic search across all memory — use the `memory` tool
  (vector/keyword) instead; this one is per-session raw transcript
- Editing the transcript — this tool is read-only
- Cross-agent inspection — scope is limited to this agent's transcripts

## Tools

Single tool `session_logs` with action dispatch:

### `list_sessions`
- `limit` (integer, optional, 1–500, default 50) — most-recent first

Returns `{sessions: [{session_id, agent_id, source_plugin, entry_count, first_timestamp, last_timestamp}, ...]}`.

### `read_session`
- `session_id` (UUID, required)
- `limit` (integer, optional) — max entries returned
- `max_chars` (integer, optional, 20–4000, default 200) — truncate each content preview

Returns `{header, total_entries, returned, truncated, entries: [...]}`.

### `search`
- `query` (string, required) — case-insensitive substring match
- `limit` (integer, optional, default 50)
- `max_chars` (integer, optional) — preview length per hit

Returns `{hits: [{session_id, timestamp, role, source_plugin, preview}, ...]}`.

### `recent`
- `session_id` (UUID, optional) — defaults to the **current** session when omitted
- `limit` (integer, optional, default 10)
- `max_chars` (integer, optional)

Returns `{session_id, count, entries: [...]}`.

## Execution guidance

- Start with `recent` for "what did I just say" questions — cheap and
  enough for short windows.
- Use `search` for "did we ever discuss X" queries; pair with
  `list_sessions` if you need to know which session to then `read_session`.
- Always set a reasonable `max_chars` — full transcripts can blow the LLM
  context window fast.
- If `transcripts_dir` is not configured, the tool returns
  `{ok: false, error: "transcripts_dir is not configured..."}` — ask the
  operator to set `agents[].transcripts_dir` in `agents.yaml`.
- For semantic search (what I *meant* vs what I *literally typed*), use
  the `memory` tool with `mode: "vector"`.
- The tool is read-only and session-scoped to this agent — no risk of
  cross-agent bleed.
