---
name: autopilot-loop
description: Run one Codex-managed autopilot iteration using Ruflo MCP or CLI state
argument-hint: ""
allowed-tools: mcp__claude-flow__autopilot_status mcp__claude-flow__autopilot_predict mcp__claude-flow__autopilot_log mcp__claude-flow__autopilot_progress mcp__claude-flow__autopilot_disable
---
Run one autopilot iteration under Codex control. Codex does not provide Claude Code persistent-loop or wakeup primitives; treat this skill as a single iteration that the current Codex session executes immediately.

1. Check autopilot state with `mcp__claude-flow__autopilot_status`.
2. If all tasks are complete or the iteration limit is reached, call `mcp__claude-flow__autopilot_disable` and stop.
3. Ask `mcp__claude-flow__autopilot_predict` for the recommended next action.
4. Execute the predicted task directly in Codex: edit files, run commands, or use Codex subagents only when explicitly authorized by the user.
5. Record progress with `mcp__claude-flow__autopilot_log` and check `mcp__claude-flow__autopilot_progress`.
6. If more work remains, report the next concrete action to the user or continue in the same turn when it is safe and bounded.

### Codex Scheduling

There is no native persistent wakeup primitive in Codex. For long-running or periodic loops, use an explicit external scheduler, a shell script, or a user-requested follow-up session.

### Task Sources

Prefer Ruflo/MCP-backed sources that Codex can access:
- **swarm-tasks**: Ruflo or claude-flow MCP task state.
- **file-checklist**: Markdown checkbox items in tracked files.
- **session-plan**: Codex's current plan and user instructions.

Avoid Claude Code-only task sources unless the user is explicitly running this skill inside Claude Code.