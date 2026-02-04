---
name: streamable-http-mcp-server
description: Creates and configures Streamable HTTP Model Context Protocol (MCP) server connections for OpenAI Agents SDK
---

# Streamable HTTP MCP Server Skill

This skill helps create and configure Streamable HTTP Model Context Protocol (MCP) server connections for OpenAI Agents SDK.

## Purpose
- Create MCPServerStreamableHttp configurations
- Configure HTTP connection parameters and authentication
- Set up caching and retry mechanisms
- Connect to HTTP-based MCP servers with direct connection management

## MCPServerStreamableHttp Constructor Parameters
- **params** (MCPServerStreamableHttpParams): Connection parameters for the server
  - **url** (str): The URL of the server
  - **headers** (dict[str, str], optional): The headers to send to the server
  - **timeout** (timedelta | float, optional): The timeout for the HTTP request (default: 5 seconds)
  - **sse_read_timeout** (timedelta | float, optional): The timeout for the SSE connection (default: 5 minutes)
  - **terminate_on_close** (bool, optional): Whether to terminate on close
  - **httpx_client_factory** (HttpClientFactory, optional): Custom HTTP client factory for configuring httpx.AsyncClient behavior
- **cache_tools_list** (bool): Whether to cache the list of available tools (default: False)
- **name** (string | None): A readable name for the server (default: None, auto-generated from URL)
- **client_session_timeout_seconds** (float | None): Read timeout for the MCP ClientSession (default: 5)
- **tool_filter** (ToolFilter): The tool filter to use for filtering tools (default: None)
- **use_structured_content** (bool): Whether to use tool_result.structured_content when calling an MCP tool (default: False)
- **max_retry_attempts** (int): Number of times to retry failed list_tools/call_tool calls (default: 0)
- **retry_backoff_seconds_base** (float): The base delay, in seconds, for exponential backoff between retries (default: 1.0)
- **message_handler** (MessageHandlerFnT | None): Optional handler invoked for session messages (default: None)

## Usage Context
Use this skill when:
- Managing HTTP connections yourself
- Running servers locally or remotely with direct connection management
- Needing to keep latency low with your own infrastructure
- Wanting to run the server inside your own infrastructure

## Basic Example
```python
import asyncio
import os

from agents import Agent, Runner
from agents.mcp import MCPServerStreamableHttp
from agents.model_settings import ModelSettings

async def main() -> None:
    token = os.environ["MCP_SERVER_TOKEN"]
    async with MCPServerStreamableHttp(
        name="Streamable HTTP Python Server",
        params={
            "url": "http://localhost:8000/mcp",
            "headers": {"Authorization": f"Bearer {token}"},
            "timeout": 10,
        },
        cache_tools_list=True,
        max_retry_attempts=3,
    ) as server:
        agent = Agent(
            name="Assistant",
            instructions="Use the MCP tools to answer the questions.",
            mcp_servers=[server],
            model_settings=ModelSettings(tool_choice="required"),
        )

        result = await Runner.run(agent, "Add 7 and 22.")
        print(result.final_output)

asyncio.run(main())
```
