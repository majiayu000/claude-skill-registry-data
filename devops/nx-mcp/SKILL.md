---
name: nx-mcp
description: Use the Nx MCP server to eliminate hallucinated project/target names.
---

# Using Nx MCP strategically


## Before you act
- List projects
- Show targets for a project
- Compute affected projects
- Inspect dependency graph

## Usage guideline
If MCP can answer it, do not guess it.

## Common wins
- Confirm `specs-<ctx>:all` exists before calling it
- Confirm `workspace:check` exists
- Inspect what `run-many -t all` will include
