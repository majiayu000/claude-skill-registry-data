---
name: mcp-server-stdio
description: Creates and configures stdio Model Context Protocol (MCP) server connections for OpenAI Agents SDK
---

# Stdio MCP Server Skill

This skill helps create and configure stdio Model Context Protocol (MCP) server connections for OpenAI Agents SDK.

## Purpose
- Create MCPServerStdio configurations
- Configure local subprocess parameters
- Connect to MCP servers that run as local processes
- Use stdio transport for local MCP server communication

## MCPServerStdio Constructor Parameters
- **params** (MCPServerStdioParams): Process parameters for the server
  - **command** (str): The executable to run to start the server (e.g., `python` or `node`)
  - **args** (list[str], optional): Command line args to pass to the command (e.g., `['foo.py']` or `['server.js', '--port', '8080']`)
  - **env** (dict[str, str], optional): The environment variables to set for the server
  - **cwd** (str | Path, optional): The working directory to use when spawning the process
  - **encoding** (str, optional): The text encoding used when sending/receiving messages to the server (default: `utf-8`)
  - **encoding_error_handler** (Literal["strict", "ignore", "replace"], optional): The text encoding error handler (default: `strict`)
- **cache_tools_list** (bool): Whether to cache the list of available tools (default: False)
- **name** (string | None): A readable name for the server (default: None, auto-generated)
- **client_session_timeout_seconds** (float | None): The read timeout passed to the MCP ClientSession (default: 5)
- **tool_filter** (ToolFilter): The tool filter to use for filtering tools (default: None)
- **use_structured_content** (bool): Whether to use tool_result.structured_content when calling an MCP tool (default: False)
- **max_retry_attempts** (int): Number of times to retry failed list_tools/call_tool calls (default: 0)
- **retry_backoff_seconds_base** (float): The base delay, in seconds, for exponential backoff between retries (default: 1.0)
- **message_handler** (MessageHandlerFnT | None): Optional handler invoked for session messages (default: None)

## Usage Context
Use this skill when:
- Working with MCP servers that run as local subprocesses
- Needing to communicate with command-line MCP server implementations
- Using stdio-based MCP server implementations
- Running MCP servers in local development environments
- When the server only exposes a command line entry point

## Basic Example
```python
import asyncio
from pathlib import Path
from agents import Agent, Runner
from agents.mcp import MCPServerStdio

current_dir = Path(__file__).parent
samples_dir = current_dir / "sample_files"

async def main() -> None:
    async with MCPServerStdio(
        name="Filesystem Server via npx",
        params={
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-filesystem", str(samples_dir)],
        },
    ) as server:
        agent = Agent(
            name="Assistant",
            instructions="Use the files in the sample directory to answer questions.",
            mcp_servers=[server],
        )
        result = await Runner.run(agent, "List the files available to you.")
        print(result.final_output)

asyncio.run(main())
```
