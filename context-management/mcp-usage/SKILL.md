---
name: mcp-usage
description: >
  Using MCP (Model Context Protocol) servers to extend agent capabilities.
  Read the configured MCP source for the current server list — never hardcode it.
  Use when: add MCP, MCP server, connect MCP, mcp tool, any MCP available,
  why is my MCP not working, MCP config.
---

# mcp-usage — MCP Server Reference

> MCP servers extend agent capabilities. Use the runtime's configured MCP source. An evidence label states what was actually called and when — nothing else counts as "live".

## When to Use

**Task-routed, not a probe ritual.** An MCP tool is called when the mapping below names a server
for the task. `search_mcp_tools` fetches a schema only after choosing a server; do not call it as
a preliminary probe. When prior decisions, project history, or cross-session context could change
the work, use one relevant memory MCP lookup early and continue with further distinct targeted
queries while each closes a concrete gap. There is no fixed per-task search cap; do not fan out
across overlapping indexes without a reason or repeat identical queries. Route workspace search to the current canon (`skills/`, `_memory/`, the project folders)
and Memora to broader semantic/project/inbox retrieval; verify Memora's snapshot results against
canonical files. Obsidian is a separate personal vault. Finding no MCP
match is not a violation; state the route and continue. The old `mcp-first` gate is retired.

Use this skill for:
- Finding which MCP tool fits a task
- Adding a new MCP server
- Troubleshooting MCP connection issues
- Choosing a server and reading its tool schema

## Pinging a server — one cheap call, never a per-server sweep

When the ask is "is this MCP alive", call one read-only tool from it
(`search_mcp_tools` → `call_mcp_tool`, e.g. `list_tables` or a single search) and treat a
clean answer as health. A bulk probe of every server is the wrong move: it spawns
all of them, and one slow server alone can need a minute to start. A per-server
sweep once produced a 95-call turn for a single question; the anatomy of that
reproduction is recorded in the workspace's own reports. Two rules come from it:

* **An identical `search_mcp_tools` query returns an identical answer** (verified twice, byte for
  byte). Asking again with the same string is a defect, not a retry; reword or stop.
* **A vague safety query is a trap.** `list tools or status or health or read only or safe non
  destructive` returns 8 arbitrary tools from 8 servers with `"more": 418` — including
  `cloudflare.execute`, whose schema says `destructive: true`. Ask for the server you need, not for a
  property.

## Discover current servers

Two files, two different jobs — name the one you read:

| File | Shape | Who reads it |
|---|---|---|
| `~/.freebuff/mcp.json` | app consent store: `{servers: {"<hash>": {configKey, enabled, allowedTools, approvedManifest, credentialBindings}}}` | the Freebuff session's own tool surface |
| `~/.agents/mcp.json` | `{mcpServers: {name: {type, command\|url, args, env}}}` | `_scripts/mcp-call.py` (the bridge) |

A server nobody uses is disabled rather than kept warm. Any counts you read
somewhere are dated, not standing state: the list changes, so inspect the live
tool surface instead of trusting a record of it.

**For a routed MCP task:** use the active host's tool definition/schema and inspect the exact
arguments before calling. A visible definition is only `tool surface`. Verify a successful
operation only when the task depends on that live capability; a general probe is not a prerequisite
for unrelated work. Before saying a capability is live, name the call that proved
it and the date it was made.

## Common use cases

Choose the server by role, then inspect the current tool surface and schema.
Do not infer availability from the server name alone.

## Configuration

Runtime store: `~/.freebuff/mcp.json`. The app owns that schema — entries are hash-keyed and carry
the manifest a human approved in the Desktop dialog. Do not hand-edit or rewrite this app-owned
store as an incidental task step. If the task explicitly authorizes a change, use the supported
consent/configuration flow, preserve existing entries, and verify the needed capability through the
active client; configuration alone does not prove the change loaded or works.

Bridge config: `~/.agents/mcp.json`, the classic `mcpServers` object:

```json
{
  "mcpServers": {
    "server-name": {
      "command": "npx",
      "args": ["-y", "package-name", "optional-args"],
      "env": { "API_KEY": "$ENV_VAR_NAME" }
    }
  }
}
```

### Adding a new server

Only change a client configuration when the task and active host explicitly authorize that scope.
Use the exact client-owned config and its supported consent flow; do not copy settings between
clients or store real secrets in tracked configuration. When authorized:

1. Identify the exact file and loader for the intended client (table above).
2. Add the entry through that client's supported configuration/consent flow.
3. Use the client-supported secret binding, such as `$ENV_VAR_NAME` only where that loader resolves it.
4. Use JSON-safe forward slashes in Windows paths where required.
5. Use the documented reload path only when needed and authorized; verify the specific operation the task depends on. A successful tools/list alone is not a successful service operation.

### Loader order

Do not assume a loader order from this skill. Inspect the current runtime configuration; configuration alone does not prove a live server.

## Troubleshooting

| Symptom | Likely cause |
|---------|-------------|
| Tool not appearing | Binary not installed (`npx`/`uvx`/`python` missing) |
| Env var not resolving | `$VAR_NAME` must exist in `process.env` or it won't load |
| Transport mismatch | Server uses `stdio` but config says `sse` (or vice versa) |
| Windows path issues | Use forward slashes in JSON paths |
| Server silently fails | Check stderr: `npx -y pkg 2>/tmp/mcp-err.log` |
| Bridge call exits 3 | Budget refused it — read the reason, batch instead of retrying |

## Task → tool mapping (skill ↔ MCP ↔ script)

Three tool layers per domain. Read left to right for your task; a dash means the
layer adds nothing for that domain. Router names are skills in `skills/<name>/`.
The servers column is illustrative: availability changes, so verify the one you
need instead of trusting a table.

| Domain | Skill router | MCP servers | Scripts / tools |
|---|---|---|---|
| Security & pentest (authorized) | `security` (+ `security-review`) | dnstwist (T), dechonet (V), shodan (V: live `ip_lookup` 2026-10-17), virustotal (T: starts and lists tools, key rejected 401) | `tools/mcp-cyber/`, the local payload and playbook references |
| Reverse engineering | `reverse-engineering` (+ `reverse-api-engineer`) | — | ghidra/ida/radare2 CLIs per parts |
| Browser automation & scraping | `browser` | playwright (V: snapshot operation only); browsermcp (T: 86 tools listed, no successful browser operation recorded) | CloakBrowser, browser-harness (`tools/`) |
| Web research & SERP | `research` | searchmcp (`research`); context7 (library docs); freshcontext | agent-reach channels |
| OSINT | `osint` | osint-tools, maigret (Docker image `soxoj/maigret`, use `format: json`) | agent-reach, a local image-OSINT tool |
| Knowledge & workspace search | `review` part `relevance-scan` for targeted prior-art questions (not a universal entry) | knowledge-rag (workspace text search); memora (memory snapshot search); zvec-grep (code grep); chroma (needs its backing service); sqlite-mcp (source-specific SQL) | `grep` / `rg` and local scripts; route by source freshness, avoid duplicate fan-out |
| Documents (md, reports, diagrams) | `documents` | — | python-docx (reading), markdown-to-HTML converter, diagram generator |
| Presentations | `decks` | — | bento-slides, dashi-ppt, md-slides, slides |
| Images / vision | `media` part `image-generation` | ai-vision (analyze/compare) | local image scripts |
| 3D & game engines | — | blender (C, app required), unity (C, disabled — bridge :8080) | — |
| Telegram (bot + user) | `telegram`, part `telegram-rich-messages` | telegram-mcp-bot (`list_chats`); telegram-userbot (a real account — read-only, no sends or account writes) | a local sender script |
| Email & calendar | `email` | google-workspace (V 2026-08-24: 121 tools) | — |
| Notes & long-term memory | `sessions` (parts) | knowledge-rag (live workspace canon); memora (snapshot and related-memory retrieval; interactive graph not verified live, potentially slow); obsidian (separate personal vault); notion (C) | `_memory/` remains canonical |
| Windows desktop control | `desktop` | windows-mcp | local PowerShell scripts |
| Databases & SQL | `dev` | sqlite-mcp, db-tools (dbs need `build.py` first) | — |
| VPN & network | `vpn` | dechonet for DNS | local VPN tooling |
| Dev workflow (git, CI, deploy) | `dev`, `ship` | cloudflare (C, remote) | gh CLI, vercel/wrangler CLIs, docker (T: run_command) |
| Reasoning support | — | sequential-thinking (V: 1 tool) | — |
| Tool discovery (find new agents/MCP) | `skill-meta` parts | a search-over-MCP server, when enabled | web research routers |
| MCP itself (add/repair/build) | `mcp` (this router) | all | `_scripts/mcp-call.py` bridge (budgeted; works mid-session, no restart) |
| Robot / Arduino | — | robot (T: 23 tools) | a local arduino-mcp project |

## Related Skills

- `desktop` part `windows-env` — Windows environment patterns
- `HOSTS.md` — the tool surface of this client and how a new host is wired in
