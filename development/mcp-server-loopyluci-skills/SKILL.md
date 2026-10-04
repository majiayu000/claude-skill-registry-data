---
name: mcp-server
description: Build MCP servers for AI agent tool integration.
version: 1.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [mcp, ai-agents, protocol]
---

# MCP Server Construction

## When to Use This Skill

Building an MCP (Model Context Protocol) server for AI agent integration. Covers: tool registration with JSON Schema parameters, resource URI templates, prompt templates, multi-transport support (stdio, WebSocket, HTTP+SSE), and Axum-based HTTP routing.

## Core Components

An MCP server has three elements:
1. **Tools** — callable actions with typed JSON schemas (e.g., `play_track`, `search`)
2. **Resources** — URI-addressable data with RFC 6576 templates (e.g., `sovereign://track/{trackId}`)
3. **Prompts** — reusable prompt templates with named arguments for common agent workflows

## Tool Registration Pattern

### Python (recommended for build environments, quick prototypes)

Minimal JSON-RPC 2.0 server over stdin/stdout — no external dependencies beyond Python 3.10+:

```python
TOOLS = [{"name": "build", "description": "Configure and compile.", "inputSchema": {...}}]

def handle_request(request):
    if request["method"] == "tools/call":
        tool = request["params"]["name"]
        args = request["params"].get("arguments", {})
        result = TOOL_DISPATCH[tool](args)
        return {"jsonrpc": "2.0", "id": request["id"],
                "result": {"content": [{"type": "text", "text": json.dumps(result)}]}}

for line in sys.stdin:
    resp = handle_request(json.loads(line.strip()))
    if resp: sys.stdout.write(json.dumps(resp) + "\n"); sys.stdout.flush()
```

### FastMCP (Python library — recommended for most Python MCP servers)

The `mcp` package provides `FastMCP`, a high-level framework that eliminates JSON-RPC boilerplate. Tools, resources, and prompts are registered via decorators on async functions. The server handles JSON-RPC framing, transport negotiation, and capability advertisement automatically.

**Install:** `pip install 'mcp[cli]'`

#### Construction

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    "My Service",
    instructions="Description shown to the agent during capability discovery.",
    host="127.0.0.1",  # Used by SSE transport — NOT passed to run_sse_async()
    port=8090,          # Same: set here, not in the run call
)
```

Key parameter notes:
- `description` is **NOT** a parameter — use `instructions` instead
- `host` and `port` are constructor kwargs, NOT arguments to `run_sse_async()`
- `host` defaults to `127.0.0.1`, `port` defaults to `8000`

#### Tool Registration

```python
@mcp.tool()
async def my_tool(param1: str, param2: int = 0) -> dict:
    """Description visible to the agent for tool selection. Keep under 200 chars."""
    result = await do_something(param1, param2)
    return {"status": "ok", "data": result}
```

- Parameters are auto-converted to JSON Schema from Python type hints
- Return value is serialized as JSON text content
- Functions can be sync or async
- Tool names become `mcp_{server_name}_{tool_name}` in Hermes (hyphens → underscores)

#### Resource Registration

```python
@mcp.resource("config://system")
def config_resource() -> str:
    """Description shown during resource discovery."""
    import json
    return json.dumps(config.to_dict(), indent=2)
```

- URI scheme and path are arbitrary but should follow `scheme://path` convention
- Resources can be sync or async
- Return value becomes the resource's text content

#### Prompt Registration

```python
@mcp.prompt()
def troubleshoot_connection() -> str:
    """Template for common agent workflows. Name becomes the prompt ID."""
    return """Diagnose bot connection issues:
1. Check bot_status()
2. Run health_check()
3. Review gateway logs with gateway_log_tail()
"""
```

- Prompts are templates returned as text strings
- Can accept named arguments by adding function parameters
- Agents use prompt templates by name for recurring tasks

#### Running the Server

```python
# SSE transport (HTTP) — for remote/network-accessible servers
await mcp.run_sse_async()      # host/port come from constructor

# Stdio transport — for subprocess mode (Hermes spawns it)
await mcp.run_stdio_async()

# Streamable HTTP — newer transport, check SDK version
await mcp.run_streamable_http_async()
```

- **SSE** — clients connect via `http://host:port/sse`, exchange messages over `POST /messages/`
- **Stdio** — JSON-RPC over stdin/stdout; Hermes spawns the process
- Pick SSE when you want the server to run independently; pick stdio when Hermes should manage the lifecycle

#### Discovering Registered Tools

```python
import asyncio
tools = asyncio.run(mcp.list_tools())
for t in tools:
    print(f"{t.name}: {t.description}")
```

Returns a list of all registered `Tool` objects with their full schemas.

#### Example: multi-category control server pattern

```python
def register_tools(mcp):
    @mcp.tool()
    async def bot_status() -> dict: ...
    @mcp.tool()
    async def service_list() -> list[dict]: ...

    def register_telemetry(mcp):
        @mcp.tool()
        async def telemetry_snapshot() -> dict: ...
    register_telemetry(mcp)

mcp = FastMCP("Control Server", host="127.0.0.1", port=8090)
register_tools(mcp)
await mcp.run_sse_async()
```

#### Hermes Agent Configuration for FastMCP (SSE) Servers

Add to `~/.hermes/config.yaml` under the top-level `mcp_servers` key:

```yaml
mcp_servers:
  my-service:
    url: "http://127.0.0.1:8090/sse"   # the /sse path is required
    timeout: 180
    connect_timeout: 60
```

Use `hermes config set` to write it:

```bash
hermes config set mcp_servers.my-service.url "http://127.0.0.1:8090/sse"
```

The `mcp_servers` section is NOT under `mcp.servers` — it's a top-level key. After adding, restart Hermes for the tools to appear. Tool names are prefixed as `mcp_my_service_tool_name`.

### Rust (recommended for production, high-throughput)

Register all tools at init time in `McpToolRegistry::register_builtin_tools()`. Each tool has `name`, `description`, and `parameters` (JSON Schema). Dispatch in `call_tool()` via match on tool name.

Key points:
- Tool descriptions must be under 200 chars — LLMs use them for routing
- Parameter schemas must be valid JSON Schema or clients reject them
- Tool parameter names must be camelCase for LLM tokenizer compatibility
- Each handler must be idempotent where possible — MCP clients retry on timeout

## Resource Template Pattern

Use URI templates (RFC 6576), not custom patterns. Dynamic templates support flexible addressing with query parameters.

## Transport Layer

- **stdio**: JSON-RPC over stdin/stdout. Best for agent subprocess (Hermes Agent).
- **WebSocket**: Persistent connection. Best for remote agents. Add ping/pong every 30s.
- **HTTP+SSE**: Long-lived streaming. Best for real-time resource updates.

## HTTP Route Pattern (Axum)

```
GET  /                  → list all tools
POST /tools/:name       → execute a tool
GET  /resources          → list resource templates
GET  /resources/:uri     → read a specific resource
GET  /prompts            → list prompt templates
GET  /health             → health check
```

## Reference Files

| File | Covers |
|---|---|
| `references/media-streaming-mcp.md` | Patterns for building MCP servers with 25+ tools in media/streaming applications — tool categorization, resource URI templates for media entities, web frontend integration with Zustand stores, agent workflow patterns. Created from the SovereignStream project. |
| `references/build-environment-mcp.md` | Python MCP server for C/C++ build environments — 8 tools (build, test, lint, analyze, file_list, file_read, syntax_check, status) with Docker integration. Stdio transport, JSON-RPC 2.0, subprocess-based tool handlers. |
| `references/network-tools-mcp.md` | Network security MCP server (adblocker + firewall) with 10 tools across Rust, Python, TypeScript, Swift, and Kotlin clients. Hardware capabilities discovery, event subscription model, WebSocket transport. Created from the Sentinel project. |
| `references/fastmcp-patterns.md` | FastMCP Python library patterns — constructor/quirk API, tool/resource/prompt registration, SSE vs stdio transport, Hermes `mcp_servers` configuration for HTTP/SSE servers, testing instructions, and known issues. Created from a 50-tool Telegram bot control server. |
| `references/cron-watcher-pattern.md` | Cron-based autonomous watcher pattern — silent-until-action background monitors that run on Hermes cron schedules, with no_agent=True watchdog mode and origin delivery. |
| `references/mcp-auto-config.md` | MCP server auto-load configuration for Hermes Agent — configuring mcp_servers in config.yaml, YAML list format pitfalls, startup discovery sequence, and transport options. |
| `references/windows-deployment.md` | Windows-specific MCP server deployment — orphan process cleanup, port contention, signal handlers, background watchdog pattern, and Hermes MCP config cleanup. Created from a Telegram bot control server on Windows. |
| `references/json-extraction-pattern.md` | Multi-line JSON parser for extracting pretty-printed JSON from mixed stdout (log lines + JSON output) — brace-depth tracking technique. |

## Auto-Discovery Manifest (Hermes Agent Integration)

To make an MCP server auto-discoverable by Hermes Agent (and other MCP-aware
clients), provide a manifest file that describes tools, resources, prompts,
and transport options.

### Manifest location conventions

| Agent | Location |
|---|---|
| Hermes Agent | `~/.hermes/mcp/<service-name>.json` |
| Claude Desktop | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| .hermes-profile/ | `./hermes-profile/<name>-mcp.yaml` |

### Manifest structure

```json
{
  "name": "sovereign-stream",
  "description": "Self-hosted music & video streaming with full MCP agent interface",
  "version": "1.0.0",
  "transport": {
    "type": "websocket",
    "url": "ws://localhost:3001/mcp",
    "fallback": {
      "type": "stdio",
      "command": "sovereign-mcp",
      "args": ["--transport", "stdio"]
    }
  },
  "auto_discovery": {
    "enabled": true,
    "scan_ports": [3001, 3002, 3003],
    "health_endpoint": "http://localhost:3001/health",
    "timeout_seconds": 5
  },
  "capabilities": {
    "tools": { "enabled": true, "count": 25 },
    "resources": { "enabled": true,
      "templates": [
        "sovereign://tracks/{id}",
        "sovereign://albums/{id}",
        "sovereign://playlists/{id}"
      ]
    },
    "prompts": {
      "enabled": true,
      "templates": [
        {"name": "play-music", "description": "Play music by voice or text",
         "arguments": [{"name": "query", "type": "string"}]}
      ]
    }
  },
  "integration": {
    "hermes_agent": {
      "auto_register": true,
      "system_prompt_hint": "You have access to [service name]...",
      "tools": [
        {"name": "play_track", "description": "Play a specific track by ID"},
        {"name": "search", "description": "Search the media library"}
      ]
    }
  }
}
```

### Auto-connect YAML (Hermes profile)

```yaml
# ~/.hermes/profiles/<name>/mcp/sovereign-stream.yaml
name: sovereign-stream
auto_connect:
  enabled: true
  on_startup: true
  health_check:
    url: "http://localhost:3001/health"
    interval_seconds: 15
    on_failure: reconnect
  max_reconnect_attempts: -1  # infinite

transport:
  ws:
    url: "ws://localhost:3001/mcp"
    heartbeat_interval_seconds: 30

mcp:
  protocol_version: "2025-03-26"
  capabilities: { tools: true, resources: true, prompts: true }

# Tools that require user confirmation
confirmations:
  - "upload_music"
  - "delete_playlist"
  - "import_playlist"

hooks:
  on_connect:
    - command: "sovereign-mcp"
      args: ["list-resources", "sovereign://library/status"]
```

## Pitfalls

- Tool parameter schemas must be valid JSON Schema — validate before registering
- Resource URI templates must use RFC 6576 syntax, not custom glob patterns
- Stdio transport blocks the main thread — use `tokio::spawn` for async handlers
- Rate limit MCP tool calls per session to prevent agent loops from overwhelming the server
- Tool argument count should stay under 10 for LLM reliability
- **FastMCP: `description` is rejected** — use `instructions` kwarg instead
- **FastMCP: host/port in constructor** — `run_sse_async()` does NOT accept them; set them when creating FastMCP()
- **FastMCP: `/sse` path is required** — Hermes `mcp_servers.url` must end in `/sse` for SSE transport
- **Hermes `mcp_servers` is top-level** — NOT under `mcp.servers`; wrong nesting means the server won't be discovered
- **Windows signal handlers** — `loop.add_signal_handler()` raises `NotImplementedError` on Windows; catch and skip gracefully

## Verification

1. `list_tools()` returns all registered tools with valid schemas
2. `call_tool()` with invalid arguments returns structured error (not panic)
3. `read_resource()` with unknown URI returns error response, not crash
4. WebSocket connection survives 5 min idle (ping/pong keepalive)
5. Stdio transport handles concurrent JSON-RPC messages without deadlock
6. **FastMCP SSE:** `curl -s -o /dev/null -w "%{http_code}" http://host:port/` returns 200
7. **Hermes integration:** After configuring `mcp_servers`, restart Hermes and verify tools appear with `mcp_` prefix
