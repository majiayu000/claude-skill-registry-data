---
name: mcp-client
version: 1.0.0
description: Model Context Protocol (MCP) client - connect to tools, data sources and services
metadata: {"openclaw": {"emoji": "🔌", "category": "integration", "requires": {"bins": ["python"], "pip": ["requests"]}, "homepage": "https://modelcontextprotocol.io"}}
---

# MCP Client Skill

Implementation of the Model Context Protocol (MCP) client for connecting to tools and data sources.

## What it does

- **Connect to MCP Servers** - Access tools and resources from MCP-enabled services
- **Tool Invocation** - Call tools exposed by MCP servers
- **Resource Access** - Read files, databases, APIs
- **Prompt Templates** - Use structured prompts from MCP servers

## Installation

```powershell
# Install Python dependencies (requests is the only required dependency)
pip install requests
```

## Usage

### Connect to MCP Server

```powershell
.\mcp.ps1 -Action connect -ServerUrl "https://mcp-server.com" -ApiKey "your-key"
```

### List Available Tools

```powershell
.\mcp.ps1 -Action tools -ServerUrl "https://mcp-server.com"
```

### Call a Tool

```powershell
.\mcp.ps1 -Action call -ServerUrl "https://mcp-server.com" -ToolName "search" -Arguments '{"query": "AI agents"}'
```

### List Resources

```powershell
.\mcp.ps1 -Action resources -ServerUrl "https://mcp-server.com"
```

### Read a Resource

```powershell
.\mcp.ps1 -Action read -ServerUrl "https://mcp-server.com" -ResourceUri "file:///data/config.json"
```

## MCP Concepts

- **MCP Server**: Service that exposes tools, resources, and prompts
- **Tools**: Functions the LLM/agent can call
- **Resources**: Data sources (files, APIs, DBs)
- **Prompts**: Pre-defined prompt templates

## API Reference

```
POST /mcp/connect     - Connect to server
GET  /mcp/tools       - List available tools
POST /mcp/call       - Invoke a tool
GET  /mcp/resources  - List resources
GET  /mcp/read       - Read resource
GET  /mcp/prompts    - List prompt templates
```

## Examples

### Python Usage

```python
from mcp_client import MCPClient

client = MCPClient("https://mcp-server.com", api_key="key")

# List tools
tools = client.list_tools()
print(tools)

# Call tool
result = client.call_tool("search", {"query": "quantum"})
print(result)

# Read resource
data = client.read_resource("file:///config.json")
print(data)
```

## ⚠️ Security Warnings

### file:// URI Risk
The MCP protocol allows `file:///path` URIs to read files from the server. **Only connect to trusted MCP servers.** A malicious server could exfiltrate sensitive files.

### Best Practices
- Only use MCP servers you control or trust
- Don't connect to random public MCP servers
- Review what tools/resources are available before using

## Requirements
- Review what tools/resources are available before using

- Python 3.8+
- requests library

## License

MIT
