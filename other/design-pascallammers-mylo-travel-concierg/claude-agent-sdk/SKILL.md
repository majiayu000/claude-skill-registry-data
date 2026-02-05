---
name: claude-agent-sdk
description: |
  Development guide for Claude Agent SDK integration in IPA Platform.

  Use when:
  - Building autonomous AI agents with Claude
  - Implementing agents that need to make independent decisions
  - Creating agents with tool usage, MCP integration, or subagent delegation
  - Integrating Claude SDK with existing Microsoft Agent Framework
  - Working with code in backend/src/integrations/claude_sdk/

  Provides: query(), ClaudeSDKClient, built-in tools, hooks, MCP, subagents patterns.
---

# Claude Agent SDK - Development Guide

**Purpose**: This skill guides correct implementation of Claude Agent SDK for autonomous AI agents in IPA Platform. Use alongside Microsoft Agent Framework for hybrid orchestration.

## When to Use Claude Agent SDK

| Scenario | Use Claude SDK | Use Agent Framework |
|----------|---------------|---------------------|
| Autonomous reasoning | Yes | No |
| Structured workflows | No | Yes |
| Independent decisions | Yes | No |
| Predefined sequences | No | Yes |
| Tool usage + reasoning | Yes | Limited |
| GroupChat/Handoff | No | Yes |

## Quick Start

### Python SDK (Recommended for this project)

```python
from claude_sdk import query, ClaudeSDKClient

# One-shot task
result = await query(
    prompt="Analyze this error and suggest fixes",
    model="claude-sonnet-4-20250514",
    max_tokens=4096
)

# Multi-turn conversation
client = ClaudeSDKClient(model="claude-sonnet-4-20250514")
session = await client.create_session()

response1 = await session.query("What files are in the project?")
response2 = await session.query("Now analyze the main.py file")
```

### TypeScript SDK

```typescript
import { query, ClaudeSDKClient } from '@anthropic/claude-sdk';

// One-shot task
const result = await query({
  prompt: "Analyze this error and suggest fixes",
  model: "claude-sonnet-4-20250514",
  maxTokens: 4096
});

// Multi-turn conversation
const client = new ClaudeSDKClient({ model: "claude-sonnet-4-20250514" });
const session = await client.createSession();

const response1 = await session.query("What files are in the project?");
const response2 = await session.query("Now analyze the main.py file");
```

## Core Components

### 1. query() - One-shot Execution

For single, complete tasks:

```python
from claude_sdk import query

result = await query(
    prompt="Debug this Python error: {error_message}",
    model="claude-sonnet-4-20250514",
    max_tokens=8192,
    tools=["Read", "Grep", "Bash"],  # Built-in tools
    allowed_commands=["python", "pytest"],  # Bash restrictions
)
```

### 2. ClaudeSDKClient - Multi-turn Sessions

For complex tasks requiring context:

```python
from claude_sdk import ClaudeSDKClient

client = ClaudeSDKClient(
    model="claude-sonnet-4-20250514",
    system_prompt="You are a senior Python developer.",
    max_tokens=16384,
)

async with client.create_session() as session:
    # Context is maintained across queries
    await session.query("Read the auth module")
    await session.query("Find security issues")
    await session.query("Generate fixes")
```

### 3. Built-in Tools

| Tool | Purpose | Example |
|------|---------|---------|
| `Read` | Read file contents | `Read("src/main.py")` |
| `Write` | Write/create files | `Write("output.txt", content)` |
| `Edit` | Edit existing files | `Edit("file.py", old, new)` |
| `Bash` | Execute commands | `Bash("pytest tests/")` |
| `Grep` | Search file contents | `Grep("pattern", "src/")` |
| `Glob` | Find files by pattern | `Glob("**/*.py")` |
| `WebSearch` | Search the web | `WebSearch("Python best practices")` |
| `WebFetch` | Fetch URL content | `WebFetch("https://example.com")` |
| `Task` | Delegate to subagent | `Task("analyze security")` |

### 4. Hooks System

Intercept and control agent behavior:

```python
from claude_sdk import Hook, HookResult

class ApprovalHook(Hook):
    """Require approval for destructive operations."""

    async def on_tool_call(self, tool_name: str, args: dict) -> HookResult:
        if tool_name in ["Write", "Edit", "Bash"]:
            approved = await self.request_approval(
                f"Agent wants to use {tool_name}: {args}"
            )
            if not approved:
                return HookResult.REJECT
        return HookResult.ALLOW

# Use with client
client = ClaudeSDKClient(hooks=[ApprovalHook()])
```

### 5. MCP Integration

Extend with custom tools via Model Context Protocol:

```python
from claude_sdk import ClaudeSDKClient
from claude_sdk.mcp import MCPServer

# Connect to MCP server
mcp = MCPServer(
    name="database-tools",
    command="uvx",
    args=["mcp-server-postgres"]
)

client = ClaudeSDKClient(
    mcp_servers=[mcp]
)
```

### 6. Subagents

Delegate complex subtasks:

```python
from claude_sdk import query

result = await query(
    prompt="Refactor the authentication system",
    subagent_config={
        "security-reviewer": {
            "prompt": "Review for security vulnerabilities",
            "tools": ["Read", "Grep"]
        },
        "test-writer": {
            "prompt": "Write unit tests for changes",
            "tools": ["Read", "Write", "Bash"]
        }
    }
)
```

## Integration with Agent Framework

For detailed hybrid architecture patterns, see [HYBRID-ARCHITECTURE.md](HYBRID-ARCHITECTURE.md).

### Basic Pattern

```python
from agent_framework import GroupChatBuilder
from claude_sdk import ClaudeSDKClient

class HybridOrchestrator:
    """Combine structured workflows with autonomous agents."""

    def __init__(self):
        # Structured workflow builder
        self._workflow_builder = GroupChatBuilder()

        # Autonomous agent
        self._autonomous_agent = ClaudeSDKClient(
            model="claude-sonnet-4-20250514",
            system_prompt="Handle unpredictable situations"
        )

    async def execute(self, task: str):
        # Try structured workflow first
        if self._is_structured_task(task):
            return await self._workflow_builder.build().execute(task)

        # Fall back to autonomous reasoning
        return await self._autonomous_agent.query(task)
```

## Reference Documentation

For detailed API documentation:

- [PYTHON-SDK.md](PYTHON-SDK.md) - Python SDK complete reference
- [TYPESCRIPT-SDK.md](TYPESCRIPT-SDK.md) - TypeScript SDK complete reference
- [TOOLS-API.md](TOOLS-API.md) - Built-in tools detailed reference
- [HOOKS-API.md](HOOKS-API.md) - Hooks system patterns
- [MCP-INTEGRATION.md](MCP-INTEGRATION.md) - MCP server integration
- [HYBRID-ARCHITECTURE.md](HYBRID-ARCHITECTURE.md) - Integration with Agent Framework

## Best Practices

### 1. Choose the Right Tool

```python
# Use query() for:
# - Single, well-defined tasks
# - Stateless operations
result = await query("Format this JSON file")

# Use ClaudeSDKClient for:
# - Multi-step investigations
# - Context-dependent tasks
# - Complex debugging sessions
async with client.create_session() as session:
    await session.query("Analyze the error")
    await session.query("Find root cause")
    await session.query("Implement fix")
```

### 2. Implement Safety Hooks

```python
# Always use hooks for production
client = ClaudeSDKClient(
    hooks=[
        ApprovalHook(),      # Human approval
        AuditHook(),         # Logging
        RateLimitHook(),     # Rate limiting
        SandboxHook(),       # Sandbox restrictions
    ]
)
```

### 3. Handle Errors Gracefully

```python
from claude_sdk import ClaudeSDKError, ToolError

try:
    result = await query("Execute complex task")
except ToolError as e:
    # Tool execution failed
    logger.error(f"Tool {e.tool_name} failed: {e.message}")
except ClaudeSDKError as e:
    # SDK-level error
    logger.error(f"SDK error: {e}")
```

## Project-Specific Implementation

In this IPA Platform project, Claude Agent SDK should be integrated at:

```
backend/src/integrations/claude_sdk/
├── __init__.py
├── client.py           # ClaudeSDKClient wrapper
├── hooks/              # Custom hooks
│   ├── approval.py     # Human-in-the-loop approval
│   ├── audit.py        # Audit logging
│   └── sandbox.py      # Security sandbox
├── tools/              # Custom tool definitions
└── adapters/           # Integration with Agent Framework
    └── hybrid_orchestrator.py
```

## Version History

- v1.0.0 (2025-12-25): Initial release for IPA Platform
