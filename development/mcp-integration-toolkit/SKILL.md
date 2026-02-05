---
name: mcp-integration-toolkit
description: Create, configure, and integrate MCP (Model Context Protocol) servers and clients. Use when building MCP servers with FastMCP (Python) or MCP SDK (Node/TypeScript), integrating external APIs, or creating custom tools/resources for LLMs. Handles server creation, client configuration, transport protocols, and security patterns.
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep, WebFetch]
---

# MCP Integration Toolkit

## Purpose

The Model Context Protocol (MCP) is the new standard for connecting LLMs to external tools, data sources, and APIs. This Skill provides comprehensive support for:

1. **Creating MCP Servers** - Build servers in Python (FastMCP) or Node/TypeScript (MCP SDK)
2. **Client Integration** - Configure Claude Code and other clients to use MCP servers
3. **Protocol Patterns** - Implement tools, resources, and prompts correctly
4. **Security & Best Practices** - Handle authentication, rate limiting, and error handling
5. **Testing & Debugging** - Validate MCP implementations and troubleshoot issues

## When to Use This Skill

- Building MCP servers to expose APIs or services to LLMs
- Integrating third-party services (databases, APIs, file systems) via MCP
- Creating custom tools for Claude Code or other MCP clients
- Debugging MCP server/client communication issues
- Converting existing tools to MCP protocol
- Setting up MCP transport layers (stdio, SSE, HTTP)

## Core Concepts

### MCP Architecture

```
┌─────────────┐         ┌──────────────┐         ┌────────────┐
│             │         │              │         │            │
│  LLM Client │◄────────┤  MCP Server  │◄────────┤ External   │
│  (Claude)   │  MCP    │  (FastMCP/   │  API    │ Service    │
│             │  Proto  │   MCP SDK)   │  Calls  │            │
└─────────────┘         └──────────────┘         └────────────┘
```

### MCP Components

1. **Tools** - Functions the LLM can call (like API endpoints)
2. **Resources** - Data the LLM can read (files, database records, API responses)
3. **Prompts** - Pre-configured templates the LLM can use
4. **Transports** - Communication layers (stdio, Server-Sent Events, HTTP)

## Knowledge Resources

### Official Documentation

- [MCP Specification](https://spec.modelcontextprotocol.io/) - Protocol specification
- [FastMCP (Python)](https://github.com/jlowin/fastmcp) - Python framework for MCP servers
- [MCP SDK (TypeScript)](https://github.com/modelcontextprotocol/sdk) - Official TypeScript/Node.js SDK
- [MCP Documentation](https://modelcontextprotocol.io/docs) - Official guides and tutorials

### Key Patterns

**FastMCP Server (Python)**:
```python
from fastmcp import FastMCP

mcp = FastMCP("my-server")

@mcp.tool()
def search_database(query: str) -> dict:
    """Search the database for records matching query"""
    # Implementation
    return {"results": [...]}

@mcp.resource("config://settings")
def get_settings() -> str:
    """Return current configuration"""
    return json.dumps(settings)

if __name__ == "__main__":
    mcp.run()
```

**MCP SDK Server (TypeScript)**:
```typescript
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

const server = new Server({
  name: "my-server",
  version: "1.0.0",
});

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [{
    name: "search_database",
    description: "Search the database",
    inputSchema: { type: "object", properties: { query: { type: "string" } } }
  }]
}));

const transport = new StdioServerTransport();
await server.connect(transport);
```

**Claude Code Configuration** (`~/.config/claude-code/mcp.json`):
```json
{
  "mcpServers": {
    "my-server": {
      "command": "python",
      "args": ["/path/to/server.py"],
      "env": {
        "API_KEY": "${API_KEY}"
      }
    }
  }
}
```

## Common MCP Gotchas

1. **Transport Mismatch** - Server and client must use compatible transports (stdio most common for local)
2. **Schema Validation** - Tool input schemas must be valid JSON Schema (not TypeScript types)
3. **Stdio Buffering** - Use `sys.stdout.flush()` in Python or avoid logging to stdout when using stdio transport
4. **Authentication** - Handle API keys via environment variables, never hardcode in server
5. **Error Handling** - Return proper error responses, don't raise unhandled exceptions
6. **Async Operations** - FastMCP handles sync/async automatically, MCP SDK requires explicit async/await
7. **Resource URIs** - Must follow URI format: `protocol://path` (e.g., `file:///path`, `db://table/id`)
8. **Tool Discovery** - LLM clients cache tool lists, restart client after server changes

## Implementation Patterns

### Pattern 1: API Integration Server

Expose external API to LLMs with rate limiting and caching:

```python
from fastmcp import FastMCP
import httpx
from functools import lru_cache
from datetime import datetime, timedelta

mcp = FastMCP("api-integration")

# Rate limiting
last_call = {}
RATE_LIMIT_SECONDS = 1

@mcp.tool()
async def call_external_api(endpoint: str, params: dict = None) -> dict:
    """Call external API with rate limiting"""
    now = datetime.now()
    if endpoint in last_call:
        elapsed = (now - last_call[endpoint]).total_seconds()
        if elapsed < RATE_LIMIT_SECONDS:
            raise ValueError(f"Rate limit: wait {RATE_LIMIT_SECONDS - elapsed:.1f}s")

    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://api.example.com/{endpoint}", params=params)
        response.raise_for_status()
        last_call[endpoint] = now
        return response.json()
```

### Pattern 2: Database Resource Server

Expose database tables as MCP resources:

```python
from fastmcp import FastMCP
import sqlite3

mcp = FastMCP("database-server")

@mcp.resource("db://users/{user_id}")
def get_user(user_id: str) -> str:
    """Get user by ID"""
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return json.dumps(dict(row)) if row else None

@mcp.tool()
def list_users(limit: int = 10) -> list[dict]:
    """List users from database"""
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]
```

### Pattern 3: File System Server

Provide safe file system access with sandboxing:

```python
from fastmcp import FastMCP
from pathlib import Path

mcp = FastMCP("filesystem-server")

ALLOWED_PATHS = [Path("/safe/directory")]

def is_safe_path(path: str) -> bool:
    """Check if path is within allowed directories"""
    p = Path(path).resolve()
    return any(p.is_relative_to(allowed) for allowed in ALLOWED_PATHS)

@mcp.resource("file://{path}")
def read_file(path: str) -> str:
    """Read file contents (sandboxed)"""
    if not is_safe_path(path):
        raise PermissionError(f"Access denied: {path}")
    return Path(path).read_text()

@mcp.tool()
def list_directory(path: str) -> list[str]:
    """List directory contents (sandboxed)"""
    if not is_safe_path(path):
        raise PermissionError(f"Access denied: {path}")
    return [str(p) for p in Path(path).iterdir()]
```

## Testing & Debugging

### Testing MCP Servers Locally

**Test with MCP Inspector** (official debugging tool):
```bash
npm install -g @modelcontextprotocol/inspector
mcp-inspector python server.py
```

**Test with Claude Code**:
1. Add server to `~/.config/claude-code/mcp.json`
2. Restart Claude Code
3. Use `/mcp` command to list available tools
4. Test tool invocation

**Unit Testing** (FastMCP):
```python
import pytest
from server import mcp

def test_search_tool():
    result = mcp.tools["search_database"]("test query")
    assert "results" in result
    assert isinstance(result["results"], list)
```

### Debugging Checklist

1. **Server Starts** - Run server directly, check for startup errors
2. **Transport Working** - Verify stdio/SSE/HTTP transport responds
3. **Schema Valid** - Validate JSON schemas with online validator
4. **Tools Discovered** - Check client can list tools
5. **Tool Execution** - Test tool with sample inputs
6. **Error Handling** - Verify errors return proper format, don't crash server
7. **Authentication** - Test with/without credentials
8. **Logging** - Use stderr for logs (stdout reserved for protocol)

## Security Best Practices

### 1. Authentication & Authorization

```python
import os
from fastmcp import FastMCP

mcp = FastMCP("secure-server")

API_KEY = os.getenv("API_KEY")

@mcp.tool()
def protected_operation(auth_token: str, data: dict) -> dict:
    """Operation requiring authentication"""
    if auth_token != API_KEY:
        raise PermissionError("Invalid authentication")
    # Perform operation
    return {"status": "success"}
```

### 2. Input Validation

```python
from pydantic import BaseModel, Field, validator

class SearchParams(BaseModel):
    query: str = Field(..., min_length=1, max_length=500)
    limit: int = Field(10, ge=1, le=100)

    @validator("query")
    def sanitize_query(cls, v):
        # Remove SQL injection attempts
        dangerous = ["DROP", "DELETE", "INSERT", "UPDATE"]
        if any(word in v.upper() for word in dangerous):
            raise ValueError("Invalid query")
        return v

@mcp.tool()
def search(params: SearchParams) -> list:
    """Search with validated params"""
    # params is guaranteed valid
    return perform_search(params.query, params.limit)
```

### 3. Rate Limiting

```python
from collections import defaultdict
from datetime import datetime, timedelta

class RateLimiter:
    def __init__(self, calls_per_minute=60):
        self.calls = defaultdict(list)
        self.limit = calls_per_minute

    def check(self, client_id: str) -> bool:
        now = datetime.now()
        minute_ago = now - timedelta(minutes=1)

        # Clean old calls
        self.calls[client_id] = [
            t for t in self.calls[client_id] if t > minute_ago
        ]

        if len(self.calls[client_id]) >= self.limit:
            return False

        self.calls[client_id].append(now)
        return True

limiter = RateLimiter(calls_per_minute=60)

@mcp.tool()
def rate_limited_operation(client_id: str, data: dict) -> dict:
    if not limiter.check(client_id):
        raise ValueError("Rate limit exceeded")
    # Perform operation
    return {"status": "success"}
```

## Migration Patterns

### Converting Existing API to MCP

**Before (Direct API)**:
```python
@app.get("/api/search")
def search_endpoint(query: str):
    return {"results": search_database(query)}
```

**After (MCP Tool)**:
```python
from fastmcp import FastMCP

mcp = FastMCP("search-server")

@mcp.tool()
def search(query: str) -> dict:
    """Search database and return results"""
    return {"results": search_database(query)}
```

### Converting Claude Code Tool to MCP

**Before (Claude Code bash tool)**:
```python
# User calls: claude "search database for X"
# Claude uses: Bash tool to run python script
```

**After (MCP Tool)**:
```python
# User calls: claude "search database for X"
# Claude uses: MCP tool directly
# Benefits: Type safety, better error handling, no shell injection
```

## Advanced Topics

### Multi-Transport Server

Support both stdio (local) and HTTP (remote):

```python
from fastmcp import FastMCP
import os

mcp = FastMCP("multi-transport-server")

# Define tools...

if __name__ == "__main__":
    transport = os.getenv("MCP_TRANSPORT", "stdio")

    if transport == "stdio":
        mcp.run()  # Default stdio
    elif transport == "http":
        mcp.run_http(host="0.0.0.0", port=8000)
    elif transport == "sse":
        mcp.run_sse(host="0.0.0.0", port=8000)
```

### Resource Subscriptions

Notify clients when resources change:

```python
from fastmcp import FastMCP

mcp = FastMCP("subscription-server")

@mcp.resource("data://latest", notify_on_change=True)
def get_latest_data() -> str:
    """Get latest data (client receives updates)"""
    return get_current_data()

# When data changes:
mcp.notify_resource_changed("data://latest")
```

### Custom Prompts

Provide pre-configured prompt templates:

```python
@mcp.prompt("code-review")
def code_review_prompt(language: str) -> str:
    """Generate code review prompt for specific language"""
    return f"""You are reviewing {language} code. Focus on:
1. Code style and idioms for {language}
2. Performance patterns specific to {language}
3. Common {language} anti-patterns
4. Security issues relevant to {language}

Please provide detailed, actionable feedback."""
```

## Production Deployment

### Deployment Checklist

- [ ] Environment variables configured (API keys, database URLs)
- [ ] Logging to stderr (stdout reserved for MCP protocol)
- [ ] Error handling for all tools (return errors, don't crash)
- [ ] Rate limiting implemented
- [ ] Input validation for all parameters
- [ ] Authentication/authorization for sensitive operations
- [ ] Health check endpoint (if using HTTP transport)
- [ ] Monitoring and alerting setup
- [ ] Documentation for all tools and resources
- [ ] Version pinning for dependencies

### Example Production Server

```python
from fastmcp import FastMCP
import logging
import sys
from typing import Optional

# Configure logging to stderr
logging.basicConfig(
    level=logging.INFO,
    stream=sys.stderr,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

mcp = FastMCP("production-server", version="1.0.0")

@mcp.tool()
def production_tool(param: str) -> dict:
    """Production-ready tool with full error handling"""
    try:
        logger.info(f"Tool called with param: {param}")

        # Validate input
        if not param or len(param) > 1000:
            raise ValueError("Invalid param length")

        # Perform operation
        result = perform_operation(param)

        logger.info("Tool completed successfully")
        return {"status": "success", "result": result}

    except ValueError as e:
        logger.error(f"Validation error: {e}")
        return {"status": "error", "message": str(e)}
    except Exception as e:
        logger.exception("Unexpected error in production_tool")
        return {"status": "error", "message": "Internal server error"}

if __name__ == "__main__":
    logger.info("Starting MCP server")
    mcp.run()
```

## Next Steps

After creating an MCP server:

1. **Test Locally** - Use MCP Inspector or Claude Code to validate
2. **Document Tools** - Write clear descriptions for all tools/resources
3. **Add Examples** - Provide usage examples in tool descriptions
4. **Configure Client** - Add to `mcp.json` for Claude Code integration
5. **Monitor Usage** - Log tool calls and errors for debugging
6. **Iterate** - Refine based on actual LLM usage patterns

## Related Skills

- `git-mastery-suite` - For managing MCP server code in Git
- `deployment-automation-toolkit` - For deploying MCP servers to production
- `security-scanning-suite` - For security analysis of MCP implementations
- `api-integration-toolkit` - For wrapping external APIs as MCP servers

## References

- [MCP Awesome List](https://github.com/punkpeye/awesome-mcp-servers) - Community MCP servers
- [FastMCP Examples](https://github.com/jlowin/fastmcp/tree/main/examples) - Python examples
- [MCP SDK Examples](https://github.com/modelcontextprotocol/sdk/tree/main/examples) - TypeScript examples
- [Claude Code MCP Guide](https://docs.claude.com/en/docs/claude-code/mcp.md) - Integration guide