---
name: backend-instance-creator
description: >
  Creates a permanent backend instance for Claude Imagine.
  Use this skill when the user wants to set up a new persistent backend server.
---
# Backend Instance Creator

## Instructions
1. Ask the user for the desired location of the backend instance (default: `~/claude-imagine-backend`).
2. Create the directory structure:
   - `mkdir -p <location>`
   - `mkdir -p <location>/.claude`
3. Create `CLAUDE.md` in the target directory with standard backend configuration.
4. Create `.claude/settings.json` enabling MCP tools.
5. Create `claude_config.json` pointing to the `server-mcp.js`.
6. Create a `start.sh` script to launch the instance.

## Configuration Template (.claude/settings.json)
```json
{
  "model": "sonnet",
  "tools": "",
  "systemPrompt": "You are the backend for Claude Imagine. Always use MCP tools (mcp__imagine__update_ui and mcp__imagine__log_thought) for all operations."
}
```

