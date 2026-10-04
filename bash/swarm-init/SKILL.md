---
name: swarm-init
description: Initialize a Ruflo swarm and coordinate Codex-native follow-up work
argument-hint: "[--topology hierarchical|mesh|ring]"
allowed-tools: Bash(npx *) mcp__claude-flow__swarm_init mcp__claude-flow__swarm_status
---
Initialize a hierarchical swarm for coordinated multi-agent work. Ruflo records swarm state; Codex remains responsible for executing the actual code and shell work.

Via MCP: `mcp__claude-flow__swarm_init({ topology: "hierarchical", maxAgents: 8, strategy: "specialized" })`

Or via CLI:
```bash
npx @claude-flow/cli@latest swarm init --topology hierarchical --max-agents 8 --strategy specialized
```

After initialization, continue work in Codex immediately. Use Codex `spawn_agent` only when the user explicitly asks for subagents, delegation, or parallel agent work. When subagents are authorized, give each worker a bounded task and disjoint file ownership, and do not wait for Ruflo to execute code on its own.

For larger teams or cross-module efforts, use hierarchical-mesh topology:
```bash
npx @claude-flow/cli@latest swarm init --topology hierarchical-mesh --max-agents 15 --strategy specialized
```

Codex replacement for Claude Code team primitives:
- Use a Ruflo swarm init plus a Codex plan for team setup.
- Use Codex `spawn_agent` only after explicit user authorization.
- Use Codex `send_input` to coordinate with an existing authorized subagent.
- Track implementation state in Codex updates and Ruflo memory/task tools.