---
name: sessions
description: >-
  Session and incident records: session logs (Freebuff dumps, orchestrator
  debug), postmortems, error memory (recurring error → known fix), and
  cross-session handoff documents. Use when starting/ending a session needs
  a record, an incident needs a postmortem, or work must continue in another
  session without losing context. One contract; the parts under parts/
  carry the procedures.
---



# sessions — records and handoff

> A record exists so the next session does not repeat the work or the
> mistake. Write it once, point at it, do not restate it.

## Choosing a part

| Situation | Part |
|---|---|
| Log a session: what was done, what remains | `parts/session-log/` |
| Scoped interrupted-session recovery / separate crash diagnosis | `parts/freebuff-session-logs/`, `parts/freebuff-orchestrator-debug/` |
| Incident postmortem (what broke, why, what changes) | `parts/postmortem/` |
| Record a recurring error and its fix for next time | `parts/error-memory/` |
| Hand work to a future session or parallel agent | `parts/handoff/` (120K) |

## Rules

- Startup orientation is `BOOT.md`; health checks are task-relevant, not a ritual.
- Use authorized host thread access when available and explicitly referenced;
  otherwise use local read-only history within the owner's scope. Never scan
  excluded private workspaces or recover hidden reasoning. Legacy examples in
  parts do not widen this boundary.
- Check scope, source dates and supersession before promoting historical decisions.
  If apparently familiar work has no trace after targeted retrieval, ask whether
  a similar task existed; do not impose this interview on explicitly new work.
- Postmortems record causes and fixes, never blame.
- Handoff must include: state, decisions taken, open branches, and where the
  plan file lives — verified, not assumed.
- Memory servers (hermes-memory, iai-mcp-memory-server) are infrastructure
  configured in MCP, not part of this router.
