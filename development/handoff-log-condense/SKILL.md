---
name: handoff-log-condense
description: Create a short summary of recent handoff log entries without modifying the append-only log.
metadata:
  short-description: Summarize recent handoff entries into a new file
---

# Handoff Log Condense

## When to use
Use when the handoff log is long and you need a short summary for a new session or review.

## Procedure
1. Choose the scope (for example, the last N entries) and write it down.
2. Copy the scoped entries into a new file under `.agent/docs/agent_handoffs/` (for example, `agent_conversation_log.summary.md`).
3. Add a brief summary at the top of the new file, then leave the original log unchanged.

## Inputs and outputs
- Inputs: `.agent/docs/agent_handoffs/agent_conversation_log.md`, chosen scope
- Outputs: new summary file under `.agent/docs/agent_handoffs/`

## Constraints
- Never modify or truncate the append-only log
- Keep summaries in a separate file
- ASCII-only

## Examples
- $handoff-log-condense
