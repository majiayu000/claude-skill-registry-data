---
name: doc-gen
description: Generate and maintain documentation with drift detection
argument-hint: "[--target PATH]"
allowed-tools: Bash(npx *) mcp__claude-flow__hooks_worker-dispatch mcp__claude-flow__memory_store Read Write
---
Generate docs via MCP worker dispatch:
`mcp__claude-flow__hooks_worker-dispatch({ trigger: "document" })`

Detect drift by comparing current code against existing docs and flagging inconsistencies.

For continuous doc maintenance, use an external scheduler or CI job to trigger the document worker periodically.

Scoped generation:
- API docs: `npx @claude-flow/cli@latest hooks worker dispatch --trigger document --scope api`
- Full project: `npx @claude-flow/cli@latest hooks worker dispatch --trigger document --scope full`

Store the approach: `mcp__claude-flow__memory_store({ key: "doc-pattern", value: "APPROACH", namespace: "patterns" })`
