---
name: pieces-mcp-playbook
description: Connect to the Pieces MCP server (SSE) and reliably query or write to Pieces Long‑Term Memory (LTM) using query/write tool patterns (e.g., ask_pieces_ltm + create_pieces_memory), with practical troubleshooting and request-shaping examples.
license: MIT
compatibility: Any Agent Skills host that can call MCP tools and/or run local scripts; assumes PiecesOS exposes MCP on localhost (commonly port 39300) via an SSE endpoint.
metadata:
  author: anthony-demo
  version: "1.0"
---

# Pieces MCP Playbook

Use this skill when you need **high-signal, reproducible** ways to pull from (and optionally write back to) **Pieces Long‑Term Memory (LTM)** through the **Pieces MCP server**.

This skill is intentionally **procedural**: it teaches an agent (or a developer wiring an agent) how to avoid “random prompt luck” and instead follow a stable sequence: **shape the request → query → validate → refine → (optionally) write back a curated memory**.

## What this skill assumes

- PiecesOS is installed + running and LTM is enabled (see `references/PREREQS.md`).
- Your MCP host is pointed at a Pieces MCP SSE URL (commonly like `http://localhost:39300/model_context_protocol/2024-11-05/sse`).
- Your environment provides some way to call **query** and **write** operations:
  - Either directly as MCP tools (e.g., `ask_pieces_ltm`, `create_pieces_memory`)
  - Or via wrapper tools you expose to the agent (commonly named `query` and `write`)

If you are unsure what tools exist, run the discovery script: `scripts/pieces_mcp_rpc.py --list-tools` (details in `references/TROUBLESHOOTING.md`).

---

## Core concepts (don’t skip)

### 1) Retrieval is *not* the answer
Pieces MCP retrieval returns **context artifacts**, often as **JSON designed for an LLM to process**, not to show to a human verbatim. Your job is to:
1. retrieve relevant artifacts
2. summarize them into a user-facing answer
3. optionally persist *curated* summaries back to memory

### 2) Start minimal, then constrain
Over‑filtering is a common cause of “no results” or poor results. The most stable pattern is:

1. **Minimal query** (just the question)
2. **Add one constraint at a time** (time window → app sources → topics)
3. **Ask a follow‑up query** based on what you saw returned

---

## Tooling contract (framework‑agnostic)

This skill is written to be compatible with two common setups.

### Setup A — Direct MCP tools (recommended)
You call the tools exposed by Pieces MCP directly. Common tool names you may see:
- `ask_pieces_ltm` (retrieve context)
- `create_pieces_memory` (write a curated memory)

> Note: some environments may expose only `ask_pieces_ltm`. Use tool discovery to confirm.

### Setup B — Wrapper tools (`query` / `write`)
You provide two tools to the agent:
- `query(payload)` → internally calls `ask_pieces_ltm`
- `write(payload)` → internally calls `create_pieces_memory` (or equivalent)

If using wrappers, enforce the payload schemas described below.

---

## Recommended payload schemas

### Query payload (minimal + optional fields)
**Always supported (minimal):**
- `question` (string)

**Common optional fields (only include if supported in your environment):**
- `time_window` (string): e.g., `"today"`, `"yesterday"`, `"last 2 hours"`
- `application_sources` (string[]): e.g., `["Visual Studio Code", "Google Chrome"]`
- `topics` (string[]): keywords, entities, identifiers (repo name, ticket id)
- `related_questions` (string[]): follow‑ups to increase recall/coverage
- `connected_client` (string): the host app name (e.g., `"Cursor"`, `"Copilot"`)

### Write payload (curated memory)
Recommended minimum:
- `summary` (string): one‑sentence title
- `summary_description` (string): 5–15 lines, structured

Strongly recommended:
- `tags` (string[]): stable facets like project, repo, subsystem, ticket, date
- `source_hint` (string): how this memory was derived (“from LTM retrieval on 2026‑01‑02”)

---

## The reliable workflow

### Step 0 — Turn the user request into a retrieval spec
Extract:
- **time scope** (explicit date range beats “recently”)
- **workstream** (project, repo, customer, ticket)
- **apps/sources** (IDE, browser, terminal, chat)
- **desired output** (bullets, table, narrative, email, etc.)

If the user query is ambiguous, do **one minimal query first**, then ask a targeted clarifying question based on what comes back.

### Step 1 — Minimal query
Example (wrapper tool form):

```json
{
  "question": "What did I work on yesterday?"
}
```

### Step 2 — Validate the retrieval (sanity checks)
Before you synthesize, verify:
- Are the returned items actually about the time range?
- Are they from the expected sources (IDE/terminal/browser)?
- Do you see the expected entities (repo name, filenames, issue id)?

If not, do **one** of:
- broaden the time window
- remove a filter
- add a missing entity to `topics`
- ask a narrower question (“Show terminal commands in Warp from yesterday afternoon”)

### Step 3 — Refinement query (constrain)
Example:

```json
{
  "question": "Summarize the debugging work I did on the caching bug yesterday afternoon.",
  "time_window": "yesterday afternoon",
  "application_sources": ["Visual Studio Code", "Warp", "Google Chrome"],
  "topics": ["cache", "redis", "TTL", "race condition", "bugfix"]
}
```

### Step 4 — Synthesize the answer (user-facing)
Rules:
- Prefer **structured output** (bullets, headings) for “what did I do”
- Include **concrete artifacts**: filenames, commands, PR/issue ids, decisions
- Clearly mark **uncertainty** (“likely”, “appears to”) when the retrieval is thin

### Step 5 (optional) — Write back a curated memory
Only write back if it adds future value. Good write-backs:
- daily standup summary
- incident timeline + root cause
- decision record + rationale
- “how I fixed it” runbook

Example:

```json
{
  "summary": "Standup summary — 2026‑01‑01",
  "summary_description": "- Main focus: caching bug in API layer\n- Changes: adjusted TTL handling and added logging\n- Next: add regression test for race condition\n- Links: PR #123, ticket ABC-456",
  "tags": ["standup", "cache", "api", "ABC-456"],
  "source_hint": "Derived from LTM retrieval via Pieces MCP"
}
```

---

## Troubleshooting (fast path)

When something fails, do this in order:

1. **Confirm PiecesOS is running and LTM is enabled** (see `references/PREREQS.md`).
2. **Confirm you’re using the correct MCP URL and port** (see `references/MCP_ENDPOINTS.md`).
3. **List tools** via `scripts/pieces_mcp_rpc.py --list-tools`.
4. If retrieval fails but writing works, capture:
   - the exact tool name
   - request payload
   - raw error text
   and follow the checklist in `references/TROUBLESHOOTING.md`.

This skill includes known failure patterns reported publicly (e.g., retrieval tool failing while memory creation works) to help you design graceful degradation.

---

## Files in this skill

### References (read when needed)
- `references/PREREQS.md` — enabling LTM + basic host setup
- `references/MCP_ENDPOINTS.md` — endpoints, message flow, and port discovery
- `references/QUERY_PLAYBOOK.md` — query shaping patterns + examples
- `references/WRITE_PLAYBOOK.md` — write-back patterns + memory templates
- `references/TROUBLESHOOTING.md` — failure modes + how to surface actionable errors
- `references/VECTOR_SEARCH_WITH_COUCHDB.md` — how a CouchDB-backed product usually handles vector search

### Scripts (run when needed)
- `scripts/pieces_mcp_rpc.py` — list tools, call tools, and capture raw responses over SSE
- `scripts/pieces_mcp_scan.py` — find a working Pieces MCP port on localhost
- `scripts/pieces_mcp_smoke_test.py` — end-to-end “list tools → retrieve → write” test (when tools are available)
