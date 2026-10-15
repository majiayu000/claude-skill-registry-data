---
name: mcp_client
description: Dynamically inspect and interact with active Server-Sent Events (SSE) Model Context Protocol servers.
---

# Model Context Protocol (MCP) Interface Skill

This skill allows the agent to dynamically inspect and interact with any active Server-Sent Events (SSE) Model Context Protocol servers.

## Available Sub-Scripts
All scripts are located in `skills/mcp/scripts/` and should be executed using Python 3 relative to the workspace root.

---

### 🔍 1. list_tools.py
- **Purpose**: Discovers and prints all available tools and parameters schema from a target MCP server URL.
- **Script Path**: `skills/mcp/scripts/list_tools.py`
- **Arguments**:
  - `--url [SSE_ENDPOINT_URL]`: Target MCP server SSE endpoint URL (Required)
- **Usage Example**:
  ```bash
  python skills/mcp/scripts/list_tools.py --url https://mcp-server-wikipedia.up.railway.app/sse
  ```

---

### ⚡ 2. execute_tool.py
- **Purpose**: Executes a specific tool on a target MCP server with specified JSON arguments.
- **Script Path**: `skills/mcp/scripts/execute_tool.py`
- **Arguments**:
  - `--url [SSE_ENDPOINT_URL]`: Target MCP server SSE endpoint URL (Required)
  - `--tool [TOOL_NAME]`: Name of the tool to execute (Required)
  - `--args [JSON_ARGUMENTS]`: JSON string arguments representing tool parameters (Required)
- **Usage Example**:
  ```bash
  python skills/mcp/scripts/execute_tool.py \
    --url https://mcp-server-wikipedia.up.railway.app/sse \
    --tool search \
    --args "{\"query\": \"인공지능\"}"
  ```
