---
name: autopilot-predict
description: Use learned patterns and current state to predict the optimal next Codex action
argument-hint: ""
allowed-tools: mcp__claude-flow__autopilot_predict mcp__claude-flow__autopilot_progress mcp__claude-flow__autopilot_learn mcp__claude-flow__autopilot_history
---
Predict what to work on next using Ruflo autopilot intelligence:

1. Call `mcp__claude-flow__autopilot_predict` for the recommended next action.
2. If confidence is above 0.7, execute the prediction directly in Codex.
3. If confidence is below 0.7, check `mcp__claude-flow__autopilot_progress` for task breakdown.
4. Pick the highest-priority incomplete task that is safe to handle in the current Codex turn.
5. After completing work, call `mcp__claude-flow__autopilot_learn` to update patterns.

### Learning Pipeline

- `mcp__claude-flow__autopilot_learn` -- discover success patterns from completed tasks.
- `mcp__claude-flow__autopilot_history({ query: "KEYWORD" })` -- search past completions.
- Patterns are stored in AgentDB for cross-session recall.

### Codex Iteration Model

Codex does not provide Claude Code `/loop` semantics. Use this skill as a bounded next-action selector:
- High confidence prediction -> execute immediately when it fits the user's current request.
- Low confidence -> fall back to explicit task priority or ask for clarification if the next action is risky.
- No tasks remaining -> disable autopilot or report that no further work is available.

For repeated unattended execution, use an external scheduler or a user-requested follow-up session rather than assuming Codex can wake itself.