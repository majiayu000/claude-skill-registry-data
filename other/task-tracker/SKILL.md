---
name: task-tracker
description: >
  Internal ACE turn step — Track ACE's tasks and projects on the canopy-web board, per canopy's
  fleet procedure.
user-invocable: false
---

# Task Tracker — ACE (stub over the fleet-canonical core)

1. **Resolve the installed canopy plugin and check freshness:**
   ```bash
   CANOPY=$(python3 -c "import json,os; d=json.load(open(os.path.expanduser('~/.claude/plugins/installed_plugins.json'))); print(d['plugins']['canopy@canopy'][0]['installPath'])")
   bash "$CANOPY/scripts/canopy-update-check.sh"
   ```
   `UPGRADE_AVAILABLE` → tell the human and run `/canopy:update` BEFORE following a stale core.
2. **Read `$CANOPY/agent-core/task-tracker.md`** and **follow it exactly**, bound to the
   Identity below. Where it says `<slug>`/`<mailbox>`, use this Identity.

## Identity
- Name: **ACE** · slug: `ace` · mailbox: `ace@dimagi-ai.com`
- Board: `/agents/ace` · Drive root env: `GDRIVE_ROOT_FOLDER` (canopy resolves it from `~/.<slug>/.env`)

## ACE-local notes (the ONLY hand-edited section — fleet-process changes go to canopy)
- **Board/task integration is config-gated and best-effort — it NEVER blocks a turn** (per
  `config/agent.json` `_doc`: workspace integration is best-effort; the ace-web vs canopy-web
  question is deliberately open). If `canopy agent --help` fails or no workbench token exists,
  note "board: not configured" in the close-out and move on.
- **Distinguish "not configured" from "down" — they are different close-out lines.** The board is
  backed by the **`canopy-web`** MCP (an HTTP server at `canopy.dimagi.com/api/mcp/`).
  When a canopy MCP is *unreachable* rather than *unconfigured*, say
  `board: unavailable (<server> <error>)` — reporting a live outage as `not configured` misfiles a
  transient failure as a settled state, and nobody goes looking for it again. Either way: skip the
  board write, say plainly that it was skipped and why, and carry on with the turn.
- **`canopy-gws` is NOT the board — do not attribute a board failure to it.** `canopy-gws` is
  canopy's Google-Workspace MCP; the board never touches it, so a dead `canopy-gws` takes nothing
  in this skill down with it. Its usual failure is provisioning, not the server: it exits at
  startup with `FATAL: GWS_IDENTITY_MODE is not set` when the agent's session env has no Google
  identity, which surfaces to Claude Code as an opaque `CONNECTION_CLOSED`. The remedy is
  `canopy provision` (or a `GWS_IDENTITY_MODE` / `GWS_SA_KEY_PATH` env block in
  `~/.claude/settings.json`) on the affected machine — a canopy-side fix, not an ACE one. Observed
  2026-09-02 on this workstation; raised as dimagi-internal/canopy#586.
- Per-opportunity pipeline state stays in Drive (`ACE/<opp>/runs/<run-id>/run_state.yaml` +
  comms-logs) — the board tracks counterpart-facing iterative threads/projects, not run state.
- **A live Connect program a team works on with ACE over time is a project** with a program
  context doc on top of the fleet mechanics: `skills/partner-on-connect-program`.
