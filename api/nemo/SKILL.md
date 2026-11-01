---
name: nemo
description: "Search engine for MCP tools and agent skills. Use when the user needs nemo functionality."
metadata: {"minis":{"originalSource":"https://clawskills.sh/skills/mootbing-nemo","convertedAt":"2026-10-31T22:12:48.943Z","license":"Unknown"}}
---

# Nemo — MCP Tool Search Engine

Search engine for MCP tools and agent skills. Search 790+ MCP server tools and 760+ agent skills in one place, call remote MCP tools, and get full skill instructions.

**Base URL:** `https://nemo.25chenghua.workers.dev`

## MCP Tools

Nemo provides three MCP tools for discovering and invoking capabilities:

- **search_tools**: Search for MCP tools and agent skills by keyword. Returns compact results by default (tool name, server, title). Set detail='full' to include descriptions and input schemas. Use source to filter by type (all, mcp, skills).
- **call_tool**: Call a tool on a remote MCP server by specifying the endpoint, tool name, and arguments. Response is truncated to maxResponseChars (default 10000). Tracks latency and logs usage.
- **get_skill**: Get full instructions for an agent skill. Returns the complete SKILL.md content, install command, and metadata. Use after search_tools to get detailed skill instructions.

## HTTP API

Nemo also exposes REST API endpoints for direct access:

### Search
```bash
curl "https://nemo.25chenghua.workers.dev/api/search?q=QUERY&limit=5&detail=compact&source=all"
```

Each result has a `type` field: `"mcp_tool"` or `"skill"`.

### Get Skill Instructions
```bash
curl "https://nemo.25chenghua.workers.dev/api/skill/SKILL_NAME?repo=owner/repo"
```

Returns the complete instructions, install command, and metadata.

### Call a Remote MCP Tool
```bash
curl -X POST "https://nemo.25chenghua.workers.dev/api/call" \
  -H "Content-Type: application/json" \
  -d '{"endpoint": "SERVER_URL", "tool": "TOOL_NAME", "args": {}}'
```

Use the `serverEndpoint` and `toolName` from search results.

## Workflow

1. Search: `curl ".../api/search?q=file+conversion"`
2. If result is `type: "skill"` → get instructions: `curl ".../api/skill/SKILL_NAME"` → follow them
3. If result is `type: "mcp_tool"` → call it: `POST .../api/call` with `endpoint`, `tool`, `args`

Useful for AI agents that need to discover and invoke tools dynamically across a distributed network of MCP servers and agent skills.
