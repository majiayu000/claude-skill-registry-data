---
name: mcp-server-sse
description: Creates and configures HTTP with Server-Sent Events Model Context Protocol (MCP) server connections for OpenAI Agents SDK
---

# HTTP with SSE MCP Server Skill

This skill helps create and configure HTTP with Server-Sent Events Model Context Protocol (MCP) server connections for OpenAI Agents SDK.

## Purpose
- Create MCPServerSse configurations
- Configure SSE connection parameters and headers
- Connect to servers that implement HTTP with Server-Sent Events
- Use SSE transport for MCP server communication

## MCPServerSse Constructor Parameters
- **params** (MCPServerSseParams): Connection parameters for the server
  - **url** (str): SSE endpoint URL for the MCP server
  - **headers** (dict[str, str], optional): HTTP headers to include with requests
  - **timeout** (timedelta | float, optional): The timeout for the HTTP request (default: 5 seconds)
  - **sse_read_timeout** (timedelta | float, optional): The timeout for the SSE connection (default: 5 minutes)
  - **httpx_client_factory** (HttpClientFactory, optional): Custom HTTP client factory for configuring httpx.AsyncClient behavior
- **cache_tools_list** (bool): Whether to cache the list of available tools (default: False)
- **name** (string | None): A readable name for the server (default: None, auto-generated from URL)
- **tool_filter** (ToolFilter): The tool filter to use for filtering tools (default: None)
- **use_structured_content** (bool): Whether to use tool_result.structured_content when calling an MCP tool (default: False)
- **max_retry_attempts** (int): Number of times to retry failed list_tools/call_tool calls (default: 0)
- **retry_backoff_seconds_base** (float): The base delay, in seconds, for exponential backoff between retries (default: 1.0)
- **message_handler** (MessageHandlerFnT | None): Optional handler invoked for session messages (default: None)

## Usage Context
Use this skill when:
- Working with servers that implement HTTP with Server-Sent Events transport
- Needing real-time event streaming from the MCP server
- Using SSE-based MCP server implementations

## Basic Example
```python
import asyncio
from agents import Agent, Runner
from agents.model_settings import ModelSettings
from agents.mcp import MCPServerSse

workspace_id = "demo-workspace"

async def main() -> None:
    async with MCPServerSse(
        name="SSE Python Server",
        params={
            "url": "http://localhost:8000/sse",
            "headers": {"X-Workspace": workspace_id},
        },
        cache_tools_list=True,
    ) as server:
        agent = Agent(
            name="Assistant",
            mcp_servers=[server],
            model_settings=ModelSettings(tool_choice="required"),
        )
        result = await Runner.run(agent, "What's the weather in Tokyo?")
        print(result.final_output)

asyncio.run(main())
```
