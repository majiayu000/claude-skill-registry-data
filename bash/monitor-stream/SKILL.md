---
name: monitor-stream
description: Observe Ruflo swarm status from Codex with bounded checks
argument-hint: ""
allowed-tools: Bash(npx *) mcp__claude-flow__swarm_status mcp__claude-flow__swarm_health
---
Observe swarm state from Codex. Codex does not expose Claude Code's `Monitor` tool, so prefer bounded status checks over indefinite streams.

For one-shot status, use MCP: `mcp__claude-flow__swarm_status` or `mcp__claude-flow__swarm_health`.

For CLI status:
```bash
npx @claude-flow/cli@latest swarm status
npx @claude-flow/cli@latest swarm health
```

If the user explicitly asks for a live stream, run the stream as a bounded shell command with an explicit timeout or stop condition:
```bash
npx @claude-flow/cli@latest swarm watch --stream
```

Do not assume line-by-line stream notifications are delivered to Codex automatically. Summarize observed events after the command returns or when the timeout is reached.