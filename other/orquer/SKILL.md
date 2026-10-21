---
name: orquer
description: "Control Orquer, a high-performance terminal workspace multiplexer and explicit agent communication bus. Use only when the user explicitly mentions Orquer or asks to inspect or control panes, tabs, workspaces, commands, messaging, or subordinate agents. Requires ORQUER_ENV=1."
---

# Orquer

Orquer organizes terminals into workspaces, tabs, and panes, and provides an event-driven message bus (`orquer msg`) for deterministic, zero-polling inter-agent communication.

Before issuing any control command, verify that this agent is running inside an Orquer-managed pane:

```bash
test "${ORQUER_ENV:-}" = 1
```

If the check fails, report that you are not running inside Orquer and stop.

## Core Capabilities

1. **Topology & Pane Management:** Workspaces, tabs, and split panes (`orquer workspace`, `orquer tab`, `orquer pane`).
2. **Explicit Messaging Bus:** Structured mailbox communication with blocking RPC questions (`orquer msg`).

## CLI Discovery

The installed binary is the authority for command syntax. Check available commands:

```bash
orquer --help
orquer msg --help
orquer pane --help
orquer workspace --help
```

## Caller Context

Orquer automatically injects environment variables into each managed pane:

```bash
printf '%s\n' "$ORQUER_WORKSPACE_ID" "$ORQUER_TAB_ID" "$ORQUER_PANE_ID"
```

Use `ORQUER_PANE_ID` as your local identity handle when communicating through `orquer msg`.
