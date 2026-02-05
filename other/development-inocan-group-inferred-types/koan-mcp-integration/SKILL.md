---
name: koan-mcp-integration
description: MCP server patterns, Code Mode integration, tool building
---

# Koan MCP Integration

## Core Principle

**Expose Koan services as MCP tools for Claude integration.** Use framework patterns for tool implementations.

## MCP Server Setup

### Basic MCP Server

```csharp
using Koan.Mcp;

var builder = WebApplication.CreateBuilder(args);
builder.Services.AddKoan();
builder.Services.AddKoanMcp(); // Adds MCP capabilities
var app = builder.Build();
app.Run();
```

### Expose Entity as MCP Tool

```csharp
public class TodoMcpTool : IMcpTool
{
    public string Name => "get_todo";
    public string Description => "Retrieve a todo by ID";

    public McpToolSchema Schema => new()
    {
        Parameters = new[]
        {
            new McpParameter { Name = "id", Type = "string", Required = true }
        }
    };

    public async Task<McpToolResult> ExecuteAsync(
        Dictionary<string, object> args,
        CancellationToken ct)
    {
        var id = args["id"].ToString();
        var todo = await Todo.Get(id, ct);

        return new McpToolResult
        {
            Content = todo != null
                ? $"Todo: {todo.Title} (Completed: {todo.Completed})"
                : "Todo not found"
        };
    }
}
```

### Configuration

```json
{
  "Koan": {
    "Mcp": {
      "ServerName": "Todo MCP Server",
      "Version": "1.0.0",
      "Transport": "stdio",
      "Capabilities": {
        "Tools": true,
        "Resources": true,
        "Prompts": false
      }
    }
  }
}
```

## Code Mode Integration

MCP servers integrate with Claude Code Mode for enhanced capabilities.

## When This Skill Applies

- ✅ Building MCP servers
- ✅ Claude integrations
- ✅ Tool development
- ✅ MCP Code Mode

## Reference Documentation

- **Guide:** `docs/guides/mcp-http-sse-howto.md`
- **Sample:** `samples/S16.PantryPal/MCP/` (MCP server example)
- **Module:** `src/Koan.Mcp/`
