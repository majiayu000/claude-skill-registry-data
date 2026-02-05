---
name: vibesafe
description: "Uses the Vibesafe MCP server to scan, compile, test, save, diff, and report status for Vibesafe units. Activate when the user asks to run vibesafe CLI commands (scan/compile/test/save/diff/status), regenerate code from specs, or inspect drift/checkpoints."
version: "0.2.0-pre1"
tags: ["vibesafe", "codegen", "mcp", "cli"]
allowed-tools: "MCP(vibesafe:*)"
---

# Vibesafe MCP Skill

Provides full control of the Vibesafe toolchain through the MCP server exposed by this plugin.

## When to Use
- User asks to run `vibesafe scan`, `compile`, `test`, `save`, `diff`, or `status`.
- Need to regenerate implementations from specs or check drift against checkpoints.
- Want to query registry contents, provider config, or checkpoints via the MCP tools.

## Available Tools
- `scan` — list all registered Vibesafe units with metadata.
- `compile` — generate implementations for a unit (supports `target`, `force`).
- `test` — run doctests/quality gates (optional `target`).
- `save` — activate checkpoints (optional `target`).
- `status` — report version, unit counts, environment.

## Examples
- “List all vibesafe units” → use `scan`.
- “Recompile app.math.ops/fibonacci” → call `compile` with `target`.
- “Run vibesafe tests” → call `test`.
- “Save checkpoints for all units” → call `save`.
- “Check drift” → call `diff` (via status+diff as available).
