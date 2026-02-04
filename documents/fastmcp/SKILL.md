---
name: fastmcp
description: "FastMCP framework documentation - build MCP servers and clients in Python with tools, resources, prompts, auth, and middleware."
---

# FastMCP Development

> **Source:** https://github.com/jlowin/fastmcp | https://gofastmcp.com

FastMCP is a Python framework for building Model Context Protocol (MCP) servers and clients. It provides a high-level, decorator-based API for creating tools, resources, and prompts that AI assistants can use.

## Quick Start

```python
from fastmcp import FastMCP

mcp = FastMCP("My Server")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b

@mcp.resource("config://app")
def get_config() -> str:
    """Return application configuration."""
    return "debug=true"

@mcp.prompt()
def greeting(name: str) -> str:
    """Generate a greeting prompt."""
    return f"Please greet {name} warmly."
```

Run with:
```bash
fastmcp run server.py
```

## Key Concepts

### Tools

Functions that perform actions and return results:

```python
@mcp.tool()
def search_database(query: str, limit: int = 10) -> list[dict]:
    """Search the database for matching records."""
    return db.search(query, limit=limit)

# Async tools
@mcp.tool()
async def fetch_url(url: str) -> str:
    """Fetch content from a URL."""
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.text
```

### Resources

Data sources that can be read:

```python
# Static resource
@mcp.resource("file://readme")
def get_readme() -> str:
    return Path("README.md").read_text()

# Dynamic resource with parameters
@mcp.resource("user://{user_id}/profile")
def get_user_profile(user_id: str) -> dict:
    return {"id": user_id, "name": "Alice"}
```

### Prompts

Reusable prompt templates:

```python
@mcp.prompt()
def code_review(code: str, language: str = "python") -> str:
    """Generate a code review prompt."""
    return f"""Please review this {language} code:

```{language}
{code}
```

Focus on: correctness, performance, readability."""
```

### Context

Access server context in tools:

```python
from fastmcp import FastMCP, Context

@mcp.tool()
async def log_activity(ctx: Context, message: str) -> str:
    """Log an activity with request context."""
    await ctx.info(f"Activity: {message}")
    return f"Logged: {message}"
```

## Server Patterns

### Composition

Combine multiple servers:

```python
from fastmcp import FastMCP

main = FastMCP("Main")
tools = FastMCP("Tools")
resources = FastMCP("Resources")

@tools.tool()
def calculate(x: int) -> int:
    return x * 2

@resources.resource("data://info")
def get_info() -> str:
    return "Info data"

# Mount sub-servers
main.mount("/tools", tools)
main.mount("/resources", resources)
```

### Middleware

Add cross-cutting behavior:

```python
from fastmcp.server.middleware import Middleware

class LoggingMiddleware(Middleware):
    async def process_tool_call(self, call, next_handler):
        print(f"Calling tool: {call.name}")
        result = await next_handler(call)
        print(f"Tool result: {result}")
        return result

mcp.add_middleware(LoggingMiddleware())
```

### Authentication

OAuth 2.0 support:

```python
from fastmcp import FastMCP
from fastmcp.server.auth import OAuthProvider

auth = OAuthProvider(
    client_id="your-client-id",
    client_secret="your-client-secret",
    authorize_url="https://provider.com/authorize",
    token_url="https://provider.com/token"
)

mcp = FastMCP("Secure Server", auth=auth)
```

## Client Usage

Connect to MCP servers:

```python
from fastmcp import Client

async with Client("http://localhost:8000") as client:
    # List available tools
    tools = await client.list_tools()

    # Call a tool
    result = await client.call_tool("add", {"a": 1, "b": 2})
    print(result)  # 3

    # Read a resource
    data = await client.read_resource("config://app")
    print(data)
```

## Deployment

### Local Development

```bash
# Run with hot reload
fastmcp dev server.py

# Run in production mode
fastmcp run server.py
```

### HTTP Server

```bash
# Run as HTTP server
fastmcp run server.py --transport http --port 8000
```

### Docker

```dockerfile
FROM python:3.12-slim
RUN pip install fastmcp
COPY server.py .
CMD ["fastmcp", "run", "server.py", "--transport", "http"]
```

## Best Practices

1. **Use type hints** - FastMCP uses type hints for validation and schema generation

2. **Write good docstrings** - Docstrings become tool/resource descriptions for the AI

3. **Handle errors gracefully** - Return meaningful error messages, don't raise raw exceptions

4. **Use async when appropriate** - For I/O operations, use async tools for better performance

5. **Compose servers** - Break large servers into smaller, focused sub-servers

6. **Add middleware** - Use middleware for logging, rate limiting, caching

7. **Secure with auth** - Use OAuth for production deployments

## CLI Reference

```bash
# Run a server
fastmcp run server.py

# Development mode with hot reload
fastmcp dev server.py

# Install to Claude Desktop
fastmcp install server.py

# Install to Claude Code
fastmcp install server.py --target claude-code

# Show server info
fastmcp inspect server.py
```

## Integration Examples

### Claude Desktop

```json
{
  "mcpServers": {
    "my-server": {
      "command": "fastmcp",
      "args": ["run", "/path/to/server.py"]
    }
  }
}
```

### OpenAPI Import

```python
from fastmcp import FastMCP
from fastmcp.server.openapi import OpenAPIServer

# Import tools from OpenAPI spec
api = OpenAPIServer.from_url("https://api.example.com/openapi.json")
mcp = FastMCP("API Server")
mcp.mount("/api", api)
```

## Documentation Index

| Resource | When to Consult |
|----------|-----------------|
| [getting-started-quickstart.md](resources/getting-started-quickstart.md) | First-time setup |
| [servers-tools.md](resources/servers-tools.md) | Creating tools |
| [servers-resources.md](resources/servers-resources.md) | Creating resources |
| [servers-prompts.md](resources/servers-prompts.md) | Creating prompts |
| [servers-context.md](resources/servers-context.md) | Using context |
| [servers-middleware.md](resources/servers-middleware.md) | Adding middleware |
| [servers-composition.md](resources/servers-composition.md) | Composing servers |
| [servers-auth-authentication.md](resources/servers-auth-authentication.md) | Authentication setup |
| [clients-client.md](resources/clients-client.md) | Client usage |
| [deployment-http.md](resources/deployment-http.md) | HTTP deployment |
| [integrations-claude-code.md](resources/integrations-claude-code.md) | Claude Code integration |
| [patterns-testing.md](resources/patterns-testing.md) | Testing patterns |

## Syncing Documentation

```bash
cd skills/fastmcp
bun run scripts/sync-docs.ts
```
