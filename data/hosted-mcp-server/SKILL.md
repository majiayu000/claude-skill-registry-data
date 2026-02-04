---
name: hosted-mcp-server
description: Creates and configures hosted Model Context Protocol (MCP) server connections for OpenAI Agents SDK
---

# Hosted MCP Server Skill

This skill helps create and configure hosted Model Context Protocol (MCP) server connections for OpenAI Agents SDK.

## Purpose
- Create HostedMCPTool configurations
- Configure server parameters and authentication
- Set up approval flows for sensitive operations
- Connect to publicly accessible MCP servers

## HostedMCPTool Properties
- **tool_config** (Mcp object/dict): The MCP tool config, which includes the server URL and other settings
- **on_approval_request** (function): An optional function that will be called if approval is requested for an MCP tool. The function takes an MCPToolApprovalRequest object as input and returns a dictionary with:
  - **approve** (bool): Whether to approve the tool call
  - **reason** (string, optional): An optional reason, if rejected
  - The function can be synchronous or asynchronous (return type can be awaitable)

## Mcp Object Properties (for tool_config)
- **type** (string, required): The type of the MCP tool. Always "mcp"
- **server_label** (string, required): A label for this MCP server, used to identify it in tool calls
- **server_url** (string): The URL for the MCP server (one of server_url or connector_id must be provided)
- **server_description** (string): Optional description of the MCP server, used to provide more context
- **connector_id** (string): Identifier for service connectors (one of server_url or connector_id must be provided)
- **authorization** (string): OAuth access token that can be used with a remote MCP server
- **headers** (dict): Optional HTTP headers to send to the MCP server (for authentication or other purposes)
- **allowed_tools** (McpAllowedTools): List of allowed tool names or a filter object
- **require_approval** (McpRequireApproval): Specify which of the MCP server's tools require approval

## MCPToolApprovalRequest Properties
- **ctx_wrapper** (RunContextWrapper): The run context
- **data** (McpApprovalRequest): The data from the MCP tool approval request

## Connector IDs Supported
- connector_dropbox
- connector_gmail
- connector_googlecalendar
- connector_googledrive
- connector_microsoftteams
- connector_outlookcalendar
- connector_outlookemail
- connector_sharepoint

## Approval Options
- "always": Always require approval
- "never": Never require approval
- Object mapping: Specific approval policies per tool

## Usage Context
Use this skill when:
- Connecting to publicly accessible MCP servers
- Using OpenAI's infrastructure for tool execution
- Working with service connectors
- Needing hosted tool execution without local callbacks

## Basic Example
```python
import asyncio

from agents import Agent, HostedMCPTool, Runner

async def main() -> None:
    agent = Agent(
        name="Assistant",
        tools=[
            HostedMCPTool(
                tool_config={
                    "type": "mcp",
                    "server_label": "gitmcp",
                    "server_url": "https://gitmcp.io/openai/codex",
                    "require_approval": "never",
                }
            )
        ],
    )

    result = await Runner.run(agent, "Which language is this repository written in?")
    print(result.final_output)

asyncio.run(main())
```

## Streaming Example
```python
result = Runner.run_streamed(agent, "Summarise this repository's top languages")
async for event in result.stream_events():
    if event.type == "run_item_stream_event":
        print(f"Received: {event.item}")
print(result.final_output)
```

## Approval Flow Example
Use when servers can perform sensitive operations that require human or programmatic approval before execution. Configure require_approval with policies ("always", "never") or a dict mapping tool names to policies.

```python
from agents import Agent, HostedMCPTool, MCPToolApprovalFunctionResult, MCPToolApprovalRequest

SAFE_TOOLS = {"read_project_metadata"}

def approve_tool(request: MCPToolApprovalRequest) -> MCPToolApprovalFunctionResult:
    if request.data.name in SAFE_TOOLS:
        return {"approve": True}
    return {"approve": False, "reason": "Escalate to a human reviewer"}

agent = Agent(
    name="Assistant",
    tools=[
        HostedMCPTool(
            tool_config={
                "type": "mcp",
                "server_label": "gitmcp",
                "server_url": "https://gitmcp.io/openai/codex",
                "require_approval": "always",
            },
            on_approval_request=approve_tool,
        )
    ],
)
```

## Connector-Backed Example
Use for OpenAI connectors instead of specifying a server_url. The Responses API handles authentication and exposes the connector's tools.

```python
import os

HostedMCPTool(
    tool_config={
        "type": "mcp",
        "server_label": "google_calendar",
        "connector_id": "connector_googlecalendar",
        "authorization": os.environ["GOOGLE_CALENDAR_AUTHORIZATION"],
        "require_approval": "never",
    }
)
```
