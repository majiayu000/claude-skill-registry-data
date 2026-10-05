---
name: cm-continuity
description: Working memory protocol — routes to session protocol, memory audit, MCP/URI integration, or storage details based on the current need. Keeps default continuity usage cheap.
token_budget: 1200
token_core: 420
token_refs:
  session-protocol: 420
  continuity-template: 260
  memory-architecture: 780
  mcp-context-server: 460
  cm-uri-scheme: 240
  storage-formats: 420
  memory-audit: 360
compressed: true
deprecated: false
---

# Continuity — Working Memory Protocol

## TL;DR
- **Use at** session start and end
- **Default file**: `.cm/CONTINUITY.md`
- **Goal**: preserve context, learnings, and next actions cheaply
- **Always-on**: this is a background protocol, not a one-off task skill

## When to Use
- Start of every session
- End of every session
- On errors, key decisions, or context handoffs
- When tooling needs memory, MCP, URI, or persistence details

## Choose the Need

```
Need to follow continuity correctly in normal day-to-day work?
└─ YES → Session Protocol

Need the template or expected CONTINUITY structure?
└─ YES → Continuity Template

Need to understand memory tiers, MCP bridge, URI scheme, or storage?
└─ YES → Load the relevant advanced reference

Need to audit memory quality and avoid stale/conflicting recall?
└─ YES → Memory Audit
```

| Need | Summary | Load |
|---|---|---|
| Normal usage | start / during / end protocol | `references/session-protocol.md` |
| Template | `CONTINUITY.md` shape | `references/continuity-template.md` |
| Memory model | tiers, bus, long-term memory | `references/memory-architecture.md` |
| MCP bridge | context server tools and setup | `references/mcp-context-server.md` |
| URI lookup | `cm://` resource references | `references/cm-uri-scheme.md` |
| Storage internals | learnings, decisions, formats | `references/storage-formats.md` |
| Memory audit | decay, conflict, reinforcement | `references/memory-audit.md` |

## Load Rules
- Load `session-protocol.md` for normal continuity use.
- Load `memory-architecture.md` only for advanced memory reasoning.
- Load `mcp-context-server.md` and `cm-uri-scheme.md` only for tooling/integration work.
- Load `storage-formats.md` only when editing persistence or migration logic.
- Load `memory-audit.md` only when reviewing memory quality or failure patterns.

## Non-Negotiables
- Read continuity at session start.
- Update continuity at session end.
- Record important failures and decisions.
- Keep secrets out of memory files.

## The Bottom Line
**Use continuity every session. Load advanced memory details only when the task actually touches them.**
