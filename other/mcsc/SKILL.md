---
name: mcsc
description: Delegate a task to another installed CLI harness (Antigravity/agy, OpenCode, Codex) from inside an AOS repo. Use this instead of shelling out to that CLI directly whenever one is installed — it wraps the wrapper flags for you and streams live tool-call telemetry to agenttrail, which is why the board updates in real time. Reach for it any time you're about to delegate work to another harness.
category: bdb-core
metadata:
  version: "0.1.0"
---

# mcsc — Multi-CLI Subagent Configurator

mcsc (`mcps/mcsc/`) is AOS's own cross-harness delegation engine. It is the
mandatory path for delegating work to another CLI harness inside an
AOS-installed repo — not a Claude-Code-only convenience.

## Why this exists

Three separate, harness-specific delegation paths already exist (the Claude
Code plugins `antigravity:delegate`, `opencode:opencode-rescue`,
`codex:codex-rescue` — see AGENTS.md's "Delegating to an external CLI"). Those
are fine for interactive delegation *from a Claude Code session*, but they are
Claude-Code-only, and none of them tell agenttrail's live board what is
happening. mcsc's adapters
(`mcps/mcsc/packages/core/src/adapters/{agy,codex,opencode}.js`) wrap each CLI
once, work from any harness, and call `emitTrail()` around every delegated run
— `SessionStart`/`SessionEnd`, plus live `PreToolUse`/`PostToolUse` where the
underlying CLI supports structured/streaming output — so a delegated run shows
up on the board the moment it starts, without any extra setup.

Skipping mcsc doesn't just lose convenience — it makes the delegated agent
invisible to anyone watching the live map, and to anyone in this repo who asks
"what are the other agents doing right now."

## How to use it

Once installed (`mcsc` in `mcp_config.json`, entry point
`mcps/mcsc/server.js`), it registers up to four MCP tools — one per
installed CLI, only exposed when that CLI is detected as `ready` in the local
inventory, and never offered back to a caller that's already running as that
same CLI (`MCSC_CALLER` env var, avoids self-delegation loops):

- `delegate_agy` — `{ prompt, model? }` → Antigravity / Gemini. **READ-ONLY until tested:** use it for research, review and analysis, never for edits. The adapter can pass `--mode accept-edits` (`write: true`), but that path is untested and not part of the contract.
- `delegate_opencode` — `{ prompt, model?, variant? }` → OpenCode
- `delegate_codex` — `{ prompt, model? }` → Codex
- `delegate_smart` — `{ task_type, prompt }` → reads `rulebook.yaml` (or the
  bundled default) and picks the best CLI for that task type automatically

Call the tool that matches the harness you want, with a complete,
self-contained `prompt` — the adapter underneath handles the CLI's actual
flags, streams tool-call telemetry to agenttrail as it runs, and returns the
final output. `variant` (OpenCode only) maps to `--variant` (reasoning
effort).

## Depth limit: one level, like a fork

Every adapter sets `MCSC_DEPTH` to the caller's depth plus one in the child's
environment. An mcsc server that starts with `MCSC_DEPTH >= 1` lists no tools and
refuses every call. A delegated agent therefore cannot delegate again, so
agy -> codex -> agy chains are impossible. `MCSC_CALLER` alone only excluded the
caller's own CLI and was overwritten by each adapter.

## What it is not

- Not a replacement for the Claude Code delegation plugins for a quick,
  interactive, single-turn ask inside a Claude Code session — those remain
  fine for that case.
- Not itself a review/QA step — verify a delegated result the same way
  AGENTS.md already says to: read the actual diff, never trust the returned
  status field alone.
