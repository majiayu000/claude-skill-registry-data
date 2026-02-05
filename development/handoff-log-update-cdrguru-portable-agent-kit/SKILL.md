---
name: handoff-log-update
description: Append a structured entry to the handoff log when an agent completes work, is blocked, or needs to pass ownership.
metadata:
  short-description: Append a structured handoff entry to the log
---

# Handoff Log Update

## When to use
Use when you need to record a handoff, status, or next actions in the append-only log.

## Procedure
1. Gather the required fields: agent name, summary, handoff target, tasks, and references.
2. Run the log update script with explicit flags:

```bash
python3 .agent/tools/utilities/update_agent_conversation_log.py \
  --agent <agent> \
  --summary "<summary>" \
  --handoff <next-owner> \
  --task "<next task>" \
  --reference "<path>"
```

3. Confirm the entry was appended to `.agent/docs/agent_handoffs/agent_conversation_log.md`.

## Inputs and outputs
- Inputs: agent, summary, handoff target, tasks, references, optional context/status
- Outputs: appended entry in `.agent/docs/agent_handoffs/agent_conversation_log.md`

## Constraints
- Never edit or delete existing log entries
- Keep summaries and tasks concise
- ASCII-only

## Examples
- $handoff-log-update
