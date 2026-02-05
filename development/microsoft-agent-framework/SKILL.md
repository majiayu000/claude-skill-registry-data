---
name: microsoft-agent-framework
description: |
  CRITICAL development guide for Microsoft Agent Framework (MAF) in IPA Platform.

  MUST READ when working with:
  - Agents (ChatAgent, AgentThread)
  - Builders (ConcurrentBuilder, GroupChatBuilder, HandoffBuilder, MagenticBuilder)
  - Workflows (Executor, Edge, WorkflowExecutor)
  - Multi-agent orchestration
  - Any code in backend/src/integrations/agent_framework/builders/

  PREVENTS: Custom implementations instead of wrapping official API.
  REQUIRES: Import official classes, use Adapter pattern with self._builder = OfficialBuilder()
---

# Microsoft Agent Framework - Development Guide

**Purpose**: This skill guides correct implementation of Microsoft Agent Framework (MAF) in this project. Always follow these patterns instead of creating custom implementations.

## CRITICAL RULES

1. **NEVER create custom agent base classes** - Use `ChatAgent` (Python) or `ChatClientAgent` (.NET)
2. **NEVER invent custom orchestration** - Use MAF's `Workflow` with `Executor` and `Edge`
3. **NEVER create custom tool abstractions** - Use MAF's function tools or MCP tools
4. **NEVER implement Builder classes from scratch** - Use official `ConcurrentBuilder`, `GroupChatBuilder`, `HandoffBuilder`, `MagenticBuilder`
5. **ALWAYS use Adapter pattern** - Wrap official builders with `self._builder = OfficialBuilder()`
6. **ALWAYS check references/** for correct API signatures before implementing

## 🚨 BUILDER API (MOST IMPORTANT FOR THIS PROJECT)

**This is the #1 cause of implementation errors.** When working with multi-agent orchestration, you MUST:

```python
# REQUIRED IMPORTS - Always use these official classes
from agent_framework import (
    ConcurrentBuilder,       # NOT custom ConcurrentBuilderAdapter
    GroupChatBuilder,        # NOT _MockGroupChatWorkflow
    HandoffBuilder,          # NOT custom HandoffController
    MagenticBuilder,         # NOT custom MagenticManagerBase
    WorkflowExecutor,        # NOT custom WorkflowExecutorAdapter
    MagenticManagerBase,     # Import, don't define
    StandardMagenticManager, # Import, don't define
)
```

**Adapter Pattern (MUST FOLLOW):**
```python
class MyBuilderAdapter:
    def __init__(self):
        self._builder = OfficialBuilder()  # ← MUST have this line

    def build(self):
        return self._builder.build()  # ← MUST call official API
```

**Verification Command:**
```bash
cd backend && python scripts/verify_official_api_usage.py
# Expected: 5/5 checks passed
```

See **`references/builders-api.md`** for complete Builder API documentation.

## Framework Overview

Microsoft Agent Framework is the official Microsoft SDK combining Semantic Kernel + AutoGen. It provides:

- `ChatAgent` / `ChatClientAgent` - The agent abstraction (DO NOT create alternatives)
- `Workflow` - Graph-based orchestration (DO NOT create custom orchestrators)
- MCP Tools - External tool integration via Model Context Protocol
- `AgentThread` - Conversation state management

## Package Names

### Python
```
pip install agent-framework --pre
```
Imports:
```python
from agent_framework import ChatAgent, AgentThread, ChatMessage
from agent_framework.workflows import Workflow, Executor, Edge
from agent_framework import MCPStdioTool, MCPStreamableHTTPTool
from agent_framework.openai import OpenAIChatClient
from agent_framework.azure import AzureAIAgentClient
```

### .NET
```
dotnet add package Microsoft.Agents.AI --prerelease
dotnet add package Microsoft.Agents.AI.OpenAI --prerelease
```
Namespaces:
```csharp
using Microsoft.Agents.AI;
using Microsoft.Agents.AI.OpenAI;
```

## Implementation Patterns

### Creating an Agent

**CORRECT** (use ChatAgent):
```python
from agent_framework import ChatAgent
from agent_framework.azure import AzureAIAgentClient

agent = ChatAgent(
    chat_client=AzureAIAgentClient(async_credential=credential),
    instructions="Your system prompt here",
    name="agent-name",
    tools=[your_tools]
)
```

**WRONG** (do not create custom classes):
```python
# ❌ NEVER DO THIS
class MyCustomAgent:
    def __init__(self, model):
        self.model = model
    async def run(self, prompt):
        ...
```

### Adding Tools to Agents

**CORRECT** (function tools):
```python
from typing import Annotated
from pydantic import Field

def my_tool(
    param: Annotated[str, Field(description="Parameter description")]
) -> str:
    """Tool description for the LLM."""
    return f"Result: {param}"

agent = ChatAgent(
    chat_client=client,
    tools=[my_tool]  # Pass function directly
)
```

**CORRECT** (MCP tools):
```python
from agent_framework import MCPStdioTool

async with MCPStdioTool(
    name="tool-name",
    command="uvx",
    args=["mcp-server-name"]
) as mcp:
    result = await agent.run("query", tools=mcp)
```

### Multi-Agent Workflows

**CORRECT** (use Workflow):
```python
from agent_framework.workflows import Workflow, Executor, Edge, AgentExecutor

workflow = Workflow(
    executors=[
        AgentExecutor(agent=agent1, name="step1"),
        AgentExecutor(agent=agent2, name="step2"),
    ],
    edges=[
        Edge(source="start", target="step1"),
        Edge(source="step1", target="step2"),
    ]
)
```

**WRONG** (do not build custom orchestration):
```python
# ❌ NEVER DO THIS
class AgentOrchestrator:
    def __init__(self, agents):
        self.agents = agents
    async def run_sequence(self, input):
        for agent in self.agents:
            ...
```

### Conversation State

**CORRECT** (use AgentThread):
```python
from agent_framework import AgentThread

thread = AgentThread()
result1 = await agent.run("Hello", thread=thread)
result2 = await agent.run("Follow up", thread=thread)  # Has context
```

## Self-Hosted Deployment Considerations

For self-hosted environments:

1. **Model Clients**: Use `OpenAIChatClient` with custom `base_url` for local models
2. **MCP Servers**: Can run locally via `MCPStdioTool` or containerized
3. **Checkpointing**: Use `InMemoryCheckpointStore` for dev, implement custom store for production
4. **No Azure dependency**: Use `OpenAIChatClient` instead of Azure clients

### Local Model Configuration

```python
from agent_framework.openai import OpenAIChatClient

client = OpenAIChatClient(
    base_url="http://localhost:8000/v1",  # Your local model endpoint
    api_key="not-needed",  # Or your local auth
    model_id="your-model-name"
)

agent = ChatAgent(chat_client=client, instructions="...")
```

## Before Implementing, Check:

1. **`references/builders-api.md`** - ⭐ Builder patterns (ConcurrentBuilder, GroupChatBuilder, etc.)
2. **`references/python-api.md`** - Python class signatures and parameters
3. **`references/dotnet-api.md`** - .NET class signatures and parameters
4. **`references/workflows-api.md`** - Workflow patterns and orchestrations
5. **`references/common-mistakes.md`** - Anti-patterns to avoid

## Quick Reference

| Need | Use This | NOT This |
|------|----------|----------|
| Create agent | `ChatAgent` | Custom agent class |
| Add tools | Function with type hints | Custom tool wrapper |
| Multi-agent | `Workflow` + `Executor` | Custom orchestrator |
| External tools | `MCPStdioTool` | Direct API calls in agent |
| Conversation state | `AgentThread` | Custom message list |
| Streaming | `agent.run_streaming()` | Custom streaming logic |
| **Parallel execution** | `ConcurrentBuilder` | Custom parallel runner |
| **Group chat** | `GroupChatBuilder` | `_MockGroupChatWorkflow` |
| **Agent handoff** | `HandoffBuilder` | Custom `HandoffController` |
| **Magentic orchestration** | `MagenticBuilder` | Custom manager classes |
| **Nested workflows** | `WorkflowExecutor` | Custom executor adapter |
