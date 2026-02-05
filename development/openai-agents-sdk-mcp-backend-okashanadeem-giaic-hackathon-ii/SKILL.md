---
name: openai-agents-sdk-mcp-backend
description: >
  Patterns for building AI-powered chatbot backends using OpenAI Agents SDK
  with MCP (Model Context Protocol) server integration in FastAPI applications.
  Supports both standalone MCP servers and function tools.
version: 2.0.0
---

# OpenAI Agents SDK + MCP Backend Skill

## When to use this Skill

Use this Skill whenever you are:

- Building an AI-powered chatbot backend using **OpenAI Agents SDK**.
- Creating **MCP servers** that expose application functionality to AI agents.
- Creating **MCP tools** using either standalone server or function tools approach.
- Implementing a **chat endpoint** that processes natural language requests.
- Integrating AI agents with existing CRUD operations via MCP.
- Building stateless conversation systems with database-backed history.

This Skill works for any FastAPI application that needs AI agent capabilities
with tool-calling functionality.

## Core Goals

- Build **production-ready AI chatbot backends** with proper error handling.
- Create **MCP servers** following the official MCP protocol specification.
- Create **reusable MCP tools** that wrap existing business logic.
- Maintain **stateless architecture** where conversation state is stored in DB.
- Follow **consistent patterns** for agent configuration and tool definition.
- Enable **natural language interfaces** for application functionality.

## Technology Stack

| Component | Technology | Version |
|-----------|------------|---------|
| AI Framework | OpenAI Agents SDK | `openai-agents>=0.6.0` |
| MCP Server | Official MCP SDK | `mcp[cli]>=1.2.0` |
| Web Framework | FastAPI | `>=0.115.0` |
| Database ORM | SQLModel | `>=0.0.22` |
| Async HTTP | httpx | `>=0.27.0` |

## Installation

```bash
# Using pip
pip install openai-agents "mcp[cli]" fastapi sqlmodel httpx

# Using uv
uv add openai-agents "mcp[cli]" fastapi sqlmodel httpx
```

Required environment variables:
```bash
# For OpenAI (default)
OPENAI_API_KEY=sk-your-api-key-here

# For Gemini (alternative)
GEMINI_API_KEY=your-gemini-api-key-here

DATABASE_URL=postgresql://user:pass@host/db
```

## Two Approaches: MCP Server vs Function Tools

The OpenAI Agents SDK supports two approaches for providing tools to agents:

### Approach 1: Standalone MCP Server (RECOMMENDED for Hackathon)

Create a separate MCP server using the **Official MCP Python SDK** that exposes
tools via the MCP protocol. The agent connects to this server.

**Advantages:**
- Follows the official MCP protocol specification
- Tools are reusable by any MCP-compatible client
- Clean separation between server and client
- Industry standard approach

**Architecture:**
```
┌─────────────────┐     ┌────────────────────┐     ┌─────────────────────┐
│  ChatKit UI     │────►│  FastAPI Backend   │     │  MCP Server         │
│                 │     │  POST /api/chat    │────►│  (Standalone)       │
│                 │     │       │            │     │  @mcp.tool()        │
│                 │◄────│       ▼            │◄────│  - add_task         │
│                 │     │  OpenAI Agent      │     │  - list_tasks       │
│                 │     │  (mcp_servers=[])  │     │  - complete_task    │
└─────────────────┘     └────────────────────┘     └─────────────────────┘
                                                           │
                                                           ▼
                                                   ┌─────────────────┐
                                                   │    Database     │
                                                   └─────────────────┘
```

**Code Example:**
```python
# mcp_server.py - Standalone MCP Server
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("todo-mcp-server")

@mcp.tool()
async def add_task(user_id: str, title: str, description: str = "") -> dict:
    """Add a new task for the user.

    Args:
        user_id: The user's unique identifier.
        title: The title of the task.
        description: Optional description.
    """
    # Database operation
    return {"task_id": 1, "status": "created", "title": title}

if __name__ == "__main__":
    mcp.run(transport="streamable-http", port=8001)
```

```python
# agent.py - Agent connects to MCP Server
from agents import Agent, Runner
from agents.mcp import MCPServerStreamableHttp

async def run_agent_with_mcp(user_message: str, user_id: str):
    async with MCPServerStreamableHttp(
        name="Todo MCP Server",
        params={"url": "http://localhost:8001/mcp"},
    ) as mcp_server:
        agent = Agent(
            name="Todo Assistant",
            instructions="Help users manage tasks.",
            mcp_servers=[mcp_server],
        )
        result = await Runner.run(
            agent,
            input=user_message,
            context={"user_id": user_id},
        )
        return result.final_output
```

### Approach 2: Function Tools (Simpler but not MCP standard)

Define tools as Python functions decorated with `@function_tool` directly
in your FastAPI application.

**Advantages:**
- Simpler setup, no separate server
- Functions can access request context directly
- Good for quick prototypes

**Disadvantages:**
- Not following official MCP protocol
- Tools are not reusable outside this agent
- Tighter coupling

**Architecture:**
```
┌─────────────────┐     ┌────────────────────────────────────────────┐
│  ChatKit UI     │────►│  FastAPI Backend                           │
│                 │     │  POST /api/chat                            │
│                 │     │       │                                    │
│                 │◄────│       ▼                                    │
│                 │     │  OpenAI Agent                              │
│                 │     │  (tools=[@function_tool])                  │
│                 │     │       │                                    │
│                 │     │       ▼                                    │
│                 │     │  Function Tools (same process)             │──► Database
│                 │     │  - add_task                                │
│                 │     │  - list_tasks                              │
└─────────────────┘     └────────────────────────────────────────────┘
```

**Code Example:**
```python
# tools.py - Function Tools (not MCP standard)
from agents import function_tool

@function_tool
async def add_task(user_id: str, title: str, description: str = "") -> dict:
    """Add a new task for the user."""
    # Database operation
    return {"task_id": 1, "status": "created", "title": title}

# agent.py
from agents import Agent

agent = Agent(
    name="Todo Assistant",
    instructions="Help users manage tasks.",
    tools=[add_task, list_tasks, complete_task],  # Direct function references
)
```

## LLM Provider Configuration

The OpenAI Agents SDK supports multiple LLM providers. You can use OpenAI,
Gemini, or any OpenAI-compatible API.

### Option 1: OpenAI (Default)

```python
from agents import Agent, Runner
import os

# Uses OPENAI_API_KEY environment variable automatically
agent = Agent(
    name="Todo Assistant",
    instructions="Help users manage tasks.",
    mcp_servers=[mcp_server],  # or tools=[...]
)

result = await Runner.run(agent, "Show my tasks")
```

### Option 2: Google Gemini

```python
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner, set_tracing_disabled
import os

# Configure Gemini client
# Reference: https://ai.google.dev/gemini-api/docs/openai
gemini_client = AsyncOpenAI(
    api_key=os.environ["GEMINI_API_KEY"],
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# Disable tracing for non-OpenAI providers
set_tracing_disabled(disabled=True)

# Create agent with Gemini model
agent = Agent(
    name="Todo Assistant",
    instructions="Help users manage tasks.",
    model=OpenAIChatCompletionsModel(
        model="gemini-2.0-flash",  # or "gemini-1.5-pro", "gemini-1.5-flash"
        openai_client=gemini_client,
    ),
    mcp_servers=[mcp_server],
)

result = await Runner.run(agent, "Show my tasks")
```

### Supported Gemini Models

| Model | Context Window | Best For |
|-------|----------------|----------|
| `gemini-2.0-flash` | 1M tokens | Fast responses, general use |
| `gemini-1.5-pro` | 2M tokens | Complex tasks, long context |
| `gemini-1.5-flash` | 1M tokens | Balance of speed and quality |

## MCP Server Implementation (Official SDK)

### FastMCP Server Pattern

```python
"""MCP Server using Official MCP Python SDK."""
from typing import Any
from mcp.server.fastmcp import FastMCP
from sqlmodel import Session, select
from app.db import engine
from app.models.task import Task

# Initialize FastMCP server
mcp = FastMCP("todo-mcp-server")


@mcp.tool()
async def add_task(
    user_id: str,
    title: str,
    description: str = "",
) -> dict[str, Any]:
    """Add a new task for the user.

    Creates a new task with the given title and optional description.
    The task is associated with the specified user.

    Args:
        user_id: The unique identifier of the user.
        title: The title of the task (required, 1-200 characters).
        description: Optional detailed description of the task.

    Returns:
        Dictionary containing task_id, status, and title.
    """
    with Session(engine) as session:
        task = Task(
            user_id=user_id,
            title=title,
            description=description,
            completed=False,
        )
        session.add(task)
        session.commit()
        session.refresh(task)
        return {
            "task_id": str(task.id),
            "status": "created",
            "title": task.title,
        }


@mcp.tool()
async def list_tasks(
    user_id: str,
    status: str = "all",
) -> dict[str, Any]:
    """List tasks for the user.

    Retrieves tasks belonging to the specified user, optionally
    filtered by completion status.

    Args:
        user_id: The unique identifier of the user.
        status: Filter by status - "all", "pending", or "completed".
                Defaults to "all".

    Returns:
        Dictionary containing tasks list, count, and filter applied.
    """
    with Session(engine) as session:
        query = select(Task).where(Task.user_id == user_id)

        if status == "pending":
            query = query.where(Task.completed == False)
        elif status == "completed":
            query = query.where(Task.completed == True)

        tasks = session.exec(query).all()
        task_list = [
            {
                "id": str(task.id),
                "title": task.title,
                "description": task.description or "",
                "completed": task.completed,
            }
            for task in tasks
        ]
        return {
            "tasks": task_list,
            "count": len(task_list),
            "filter": status,
        }


@mcp.tool()
async def complete_task(user_id: str, task_id: str) -> dict[str, Any]:
    """Mark a task as complete.

    Args:
        user_id: The unique identifier of the user.
        task_id: The ID of the task to mark as complete.

    Returns:
        Dictionary with task_id, status, and title.
    """
    with Session(engine) as session:
        task = session.get(Task, task_id)

        if not task or task.user_id != user_id:
            return {"error": "Task not found", "task_id": task_id}

        task.completed = True
        session.add(task)
        session.commit()
        return {
            "task_id": str(task.id),
            "status": "completed",
            "title": task.title,
        }


@mcp.tool()
async def delete_task(user_id: str, task_id: str) -> dict[str, Any]:
    """Delete a task from the list.

    Args:
        user_id: The unique identifier of the user.
        task_id: The ID of the task to delete.

    Returns:
        Dictionary with task_id, status, and title.
    """
    with Session(engine) as session:
        task = session.get(Task, task_id)

        if not task or task.user_id != user_id:
            return {"error": "Task not found", "task_id": task_id}

        title = task.title
        session.delete(task)
        session.commit()
        return {
            "task_id": task_id,
            "status": "deleted",
            "title": title,
        }


@mcp.tool()
async def update_task(
    user_id: str,
    task_id: str,
    title: str | None = None,
    description: str | None = None,
) -> dict[str, Any]:
    """Update a task's title or description.

    Args:
        user_id: The unique identifier of the user.
        task_id: The ID of the task to update.
        title: New title for the task (optional).
        description: New description for the task (optional).

    Returns:
        Dictionary with task_id, status, and title.
    """
    with Session(engine) as session:
        task = session.get(Task, task_id)

        if not task or task.user_id != user_id:
            return {"error": "Task not found", "task_id": task_id}

        if title is not None:
            task.title = title
        if description is not None:
            task.description = description

        session.add(task)
        session.commit()
        return {
            "task_id": str(task.id),
            "status": "updated",
            "title": task.title,
        }


# Run the MCP server
def main():
    """Run the MCP server with streamable HTTP transport."""
    mcp.run(transport="streamable-http", port=8001)


if __name__ == "__main__":
    main()
```

### Running MCP Server

```bash
# Option 1: Direct run
python mcp_server.py

# Option 2: Using uvicorn (if using HTTP transport)
uvicorn mcp_server:mcp --port 8001

# Option 3: Using uv
uv run mcp_server.py
```

## Agent Connection to MCP Server

### Using MCPServerStreamableHttp

```python
from agents import Agent, Runner
from agents.mcp import MCPServerStreamableHttp

AGENT_INSTRUCTIONS = """You are a helpful assistant that helps users manage their tasks.

## CAPABILITIES
- Add new tasks with titles and optional descriptions
- List all tasks, or filter by status (pending/completed)
- Mark tasks as complete
- Delete tasks they no longer need
- Update task titles or descriptions

## BEHAVIOR GUIDELINES
1. Always confirm actions with a friendly, concise message
2. When listing tasks, format them clearly with task IDs
3. If a task is not found, explain politely
4. Ask for clarification if the request is ambiguous
"""


async def create_agent_with_mcp_server():
    """Create agent connected to MCP server."""
    async with MCPServerStreamableHttp(
        name="Todo MCP Server",
        params={
            "url": "http://localhost:8001/mcp",
            "timeout": 30,
        },
        cache_tools_list=True,
    ) as mcp_server:
        agent = Agent(
            name="Todo Assistant",
            instructions=AGENT_INSTRUCTIONS,
            mcp_servers=[mcp_server],
        )
        yield agent


async def process_chat(user_message: str, user_id: str) -> str:
    """Process a chat message through the agent."""
    async with MCPServerStreamableHttp(
        name="Todo MCP Server",
        params={"url": "http://localhost:8001/mcp"},
    ) as mcp_server:
        agent = Agent(
            name="Todo Assistant",
            instructions=AGENT_INSTRUCTIONS,
            mcp_servers=[mcp_server],
        )
        result = await Runner.run(
            agent,
            input=user_message,
            context={"user_id": user_id},
        )
        return result.final_output
```

### MCP Server Transport Options

| Transport | Use Case | Connection Method |
|-----------|----------|-------------------|
| `streamable-http` | HTTP-based server | `MCPServerStreamableHttp` |
| `sse` | Server-Sent Events | `MCPServerSse` |
| `stdio` | Local subprocess | `MCPServerStdio` |

## Database Models for Chat

### Conversation Model

```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class Conversation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

### Message Model

```python
class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversation.id", index=True)
    user_id: str = Field(index=True)
    role: str  # "user" or "assistant"
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

## Chat Endpoint Pattern

### Request/Response Schemas

```python
from pydantic import BaseModel
from typing import Optional, List

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[int] = None

class ToolCall(BaseModel):
    name: str
    arguments: dict
    result: dict

class ChatResponse(BaseModel):
    conversation_id: int
    response: str
    tool_calls: List[ToolCall] = []
```

### Chat Router Implementation

```python
from fastapi import APIRouter, Depends, HTTPException
from agents import Agent, Runner
from agents.mcp import MCPServerStreamableHttp

router = APIRouter(prefix="/api/{user_id}", tags=["chat"])

MCP_SERVER_URL = "http://localhost:8001/mcp"

@router.post("/chat", response_model=ChatResponse)
async def chat(
    user_id: str,
    request: ChatRequest,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    # 1. Verify user authorization
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")

    # 2. Get or create conversation
    conversation = await get_or_create_conversation(
        session, user_id, request.conversation_id
    )

    # 3. Fetch conversation history
    history = await get_conversation_history(session, conversation.id)

    # 4. Store user message
    await store_message(session, conversation.id, user_id, "user", request.message)

    # 5. Run agent with MCP server
    async with MCPServerStreamableHttp(
        name="Todo MCP Server",
        params={"url": MCP_SERVER_URL},
    ) as mcp_server:
        agent = Agent(
            name="Todo Assistant",
            instructions=AGENT_INSTRUCTIONS,
            mcp_servers=[mcp_server],
        )
        result = await Runner.run(
            agent,
            input=request.message,
            context={"user_id": user_id, "history": history},
        )

    # 6. Store assistant response
    await store_message(
        session, conversation.id, user_id, "assistant", result.final_output
    )

    # 7. Return response
    return ChatResponse(
        conversation_id=conversation.id,
        response=result.final_output,
        tool_calls=extract_tool_calls(result),
    )
```

## Agent Instructions Best Practices

### Good Instructions

```python
instructions = """You are a helpful todo assistant for managing tasks.

CAPABILITIES:
- Add new tasks with titles and descriptions
- List all tasks, pending tasks, or completed tasks
- Mark tasks as complete
- Delete tasks
- Update task details

BEHAVIOR:
- Always confirm actions with a friendly message
- When listing tasks, format them clearly with IDs
- If a task is not found, explain politely
- Ask for clarification if the request is ambiguous

EXAMPLES:
- "Add a task" -> Ask for the task title
- "Show my tasks" -> Use list_tasks with status="all"
- "Mark task 3 done" -> Use complete_task with task_id=3
"""
```

## Error Handling

### Tool-Level Errors

```python
@mcp.tool()
async def complete_task(user_id: str, task_id: str) -> dict:
    """Mark a task as complete."""
    task = get_task(user_id, task_id)
    if not task:
        return {"error": "Task not found", "task_id": task_id}

    task.completed = True
    save_task(task)
    return {"task_id": task_id, "status": "completed", "title": task.title}
```

### Endpoint-Level Errors

```python
@router.post("/chat")
async def chat(user_id: str, request: ChatRequest):
    try:
        async with MCPServerStreamableHttp(...) as mcp_server:
            agent = Agent(name="Assistant", mcp_servers=[mcp_server])
            result = await Runner.run(agent, input=request.message)
        return ChatResponse(response=result.final_output)
    except Exception as e:
        logger.error(f"Agent error: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to process your request. Please try again."
        )
```

## Testing Patterns

### Unit Testing MCP Tools

```python
import pytest
from mcp_server import add_task, list_tasks

@pytest.mark.asyncio
async def test_add_task():
    result = await add_task(user_id="test-user", title="Test Task")
    assert result["status"] == "created"
    assert result["title"] == "Test Task"

@pytest.mark.asyncio
async def test_list_tasks():
    result = await list_tasks(user_id="test-user", status="all")
    assert "tasks" in result
    assert isinstance(result["tasks"], list)
```

### Integration Testing Chat

```python
from fastapi.testclient import TestClient

def test_chat_endpoint(client: TestClient, auth_headers: dict):
    response = client.post(
        "/api/test-user/chat",
        json={"message": "Add a task to buy groceries"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert "conversation_id" in data
    assert "response" in data
```

## Things to Avoid

- **Using only @function_tool for hackathon** - Use proper MCP server instead.
- **Hardcoding API keys** - Always use environment variables.
- **Ignoring rate limits** - Implement retry logic with backoff.
- **Unbounded history** - Limit conversation history length.
- **Missing error handling** - Always handle tool and agent failures.
- **Blocking operations** - Use async patterns for database and API calls.
- **Vague agent instructions** - Be specific about capabilities and behavior.

## References

- [MCP Protocol Introduction](https://modelcontextprotocol.io/docs/getting-started/intro)
- [Build MCP Server](https://modelcontextprotocol.io/docs/develop/build-server)
- [MCP Python SDK GitHub](https://github.com/modelcontextprotocol/python-sdk)
- [OpenAI Agents SDK - MCP Integration](https://openai.github.io/openai-agents-python/mcp/)
- [OpenAI Agents SDK Documentation](https://openai.github.io/openai-agents-python/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
