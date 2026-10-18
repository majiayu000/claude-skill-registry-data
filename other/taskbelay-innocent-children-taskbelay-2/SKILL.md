---
name: taskbelay
description: "Use TaskBelay for substantial development that benefits from saved progress, verification reuse or interruption recovery, or when explicitly requested. Reuse existing user authority. Skip ordinary questions and small mechanical edits unless requested."
---

# TaskBelay for DeepSeek Harness

Read [engineering work](references/engineering.md) when starting or resuming a Task. Consult
[protocol](references/protocol.md) for tool fields and recovery; read [workspaces](references/workspace.md)
only for needed workspace operations. Load details as needed instead of reading every reference upfront.

Use tools actually exposed in this session. If unavailable, report the integration problem once and
continue authorized work using native tools; do not claim TaskBelay recorded it. A CLI success does
not prove the Host exposes MCP. Preserve data when troubleshooting storage or configuration.

Start from the actual user request in the selected/current workspace. Reuse existing authority without
an extra plan-confirmation step. Explain the approach; adjust implementation and checks within the same
outcome and restrictions. Ask only for missing information or a real change to user boundaries.

The structured hook checks write/edit/str_replace_editor paths. Other edits are observed at checkpoints. Native permissions
still apply; hooks cannot authenticate conversation or judge future code semantics. This is not a sandbox.

Default responses summarize current work. Use get_task detail:true for full history and get_run for
output. Keep operation identities after response loss; inspect saved results before repeating effects.
Report completed work, actual checks and uncertainty honestly. Git, new chat, publication and deletion
follow actual user authorization. Normal usage should not require reading plugin source.

Maintainer implementation reference: `internal/protocol/handler.go`.

Run command checks with the native process tool using the bundled Core and TASKBELAY_DATA_DIR supplied at activation. Pass the RunRequest JSON on stdin and retain the native session for long commands. MCP reads and records results; it does not start commands.
