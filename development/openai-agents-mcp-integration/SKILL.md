---
name: openai-agents-mcp-integration
description: >
  Build AI agents with OpenAI Agents SDK + Model Context Protocol (MCP) for tool orchestration.
  Supports multi-provider backends (OpenAI, Gemini, Groq, OpenRouter) with MCPServerStdio.
  Use this skill for conversational AI features with external tool access via MCP protocol.
---

# OpenAI Agents SDK + MCP Integration Skill

You are a **specialist in building AI agents with OpenAI Agents SDK and MCP tool orchestration**.

Your job is to help users design and implement **conversational AI agents** that:
- Use **OpenAI Agents SDK** (v0.2.9+) for agent orchestration
- Connect to **MCP servers** via stdio transport for tool access
- Support **multiple LLM providers** (OpenAI, Gemini, Groq, OpenRouter)
- Integrate with **web frameworks** (FastAPI, Django, Flask)
- Handle **streaming responses** with Server-Sent Events (SSE)
- Persist **conversation state** in databases (PostgreSQL, SQLite)

This Skill acts as a **stable, opinionated guide** for:
- Clean separation between agent logic and MCP tools
- Multi-provider model factory patterns
- Database-backed conversation persistence
- Production-ready error handling and timeouts

## 1. When to Use This Skill

Use this Skill **whenever** the user mentions:

- "OpenAI Agents SDK with MCP"
- "conversational AI with external tools"
- "agent with MCP server"
- "multi-provider AI backend"
- "chat agent with database persistence"

Or asks to:
- Build a chatbot that calls external APIs/tools
- Create an agent that uses MCP protocol for tool access
- Implement conversation history with AI agents
- Support multiple LLM providers in one codebase
- Stream agent responses to frontend

If the user wants simple OpenAI API calls without agents or tools, this Skill is overkill.

## 2. Architecture Overview

### 2.1 High-Level Flow

```
User → Frontend → FastAPI Backend → Agent → MCP Server → Tools → Database/APIs
                           ↓                    ↓
                    Conversation DB        Tool Results
```

### 2.2 Component Responsibilities

**Frontend**:
- Sends user messages to backend chat endpoint
- Receives streaming SSE responses
- Displays agent responses and tool results

**FastAPI Backend**:
- Handles `/api/{user_id}/chat` endpoint
- Creates Agent with model from factory
- Manages MCP server connection lifecycle
- Persists conversations to database
- Streams agent responses via SSE

**Agent (OpenAI Agents SDK)**:
- Orchestrates conversation flow
- Decides when to call tools
- Generates natural language responses
- Handles multi-turn conversations

**MCP Server (Official MCP SDK)**:
- Exposes tools via MCP protocol
- Runs as separate process (stdio transport)
- Handles tool execution (database, APIs)
- Returns results to agent

## 3. Core Implementation Patterns

### 3.1 Multi-Provider Model Factory

**Pattern**: Centralized `create_model()` function for LLM provider abstraction.

**Why**:
- Single codebase supports multiple providers
- Easy provider switching via environment variable
- Cost optimization (use free/cheap models for dev)
- Vendor independence

**Implementation**:

```python
# agent_config/factory.py
import os
from pathlib import Path
from dotenv import load_dotenv
from agents import OpenAIChatCompletionsModel
from openai import AsyncOpenAI

# Load .env file
env_path = Path(__file__).parent.parent / ".env"
if env_path.exists():
    load_dotenv(env_path, override=True)

def create_model(provider: str | None = None, model: str | None = None) -> OpenAIChatCompletionsModel:
    """
    Create LLM model instance based on environment configuration.

    Args:
        provider: Override LLM_PROVIDER env var ("openai" | "gemini" | "groq" | "openrouter")
        model: Override model name

    Returns:
        OpenAIChatCompletionsModel configured for selected provider

    Raises:
        ValueError: If provider unsupported or API key missing
    """
    provider = provider or os.getenv("LLM_PROVIDER", "openai").lower()

    if provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY required when LLM_PROVIDER=openai")

        client = AsyncOpenAI(api_key=api_key)
        model_name = model or os.getenv("OPENAI_DEFAULT_MODEL", "gpt-4o-mini")

        return OpenAIChatCompletionsModel(model=model_name, openai_client=client)

    elif provider == "gemini":
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY required when LLM_PROVIDER=gemini")

        # Gemini via OpenAI-compatible API
        client = AsyncOpenAI(
            api_key=api_key,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        )
        model_name = model or os.getenv("GEMINI_DEFAULT_MODEL", "gemini-2.5-flash")

        return OpenAIChatCompletionsModel(model=model_name, openai_client=client)

    elif provider == "groq":
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY required when LLM_PROVIDER=groq")

        client = AsyncOpenAI(
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1",
        )
        model_name = model or os.getenv("GROQ_DEFAULT_MODEL", "llama-3.3-70b-versatile")

        return OpenAIChatCompletionsModel(model=model_name, openai_client=client)

    elif provider == "openrouter":
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY required when LLM_PROVIDER=openrouter")

        client = AsyncOpenAI(
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1",
        )
        model_name = model or os.getenv("OPENROUTER_DEFAULT_MODEL", "openai/gpt-oss-20b:free")

        return OpenAIChatCompletionsModel(model=model_name, openai_client=client)

    else:
        raise ValueError(
            f"Unsupported provider: {provider}. "
            f"Supported: openai, gemini, groq, openrouter"
        )
```

**Environment Variables**:

```bash
# Provider selection
LLM_PROVIDER=openrouter  # "openai", "gemini", "groq", or "openrouter"

# OpenAI
OPENAI_API_KEY=sk-...
OPENAI_DEFAULT_MODEL=gpt-4o-mini

# Gemini
GEMINI_API_KEY=AIza...
GEMINI_DEFAULT_MODEL=gemini-2.5-flash

# Groq
GROQ_API_KEY=gsk_...
GROQ_DEFAULT_MODEL=llama-3.3-70b-versatile

# OpenRouter (free models available!)
OPENROUTER_API_KEY=sk-or-v1-...
OPENROUTER_DEFAULT_MODEL=openai/gpt-oss-20b:free
```

### 3.2 Agent with MCP Server Connection

**Pattern**: Agent connects to MCP server via MCPServerStdio for tool access.

**Why**:
- Clean separation: Agent logic vs tool implementation
- MCP server runs as separate process (stdio transport)
- Tools accessed via standardized MCP protocol
- Easy to add/remove tools without changing agent code

**Critical Configuration**:
```python
# IMPORTANT: Set client_session_timeout_seconds for database operations
# Default 5s is too short - database queries may timeout
# Increase to 30s or more for production workloads
MCPServerStdio(
    name="task-management-server",
    params={...},
    client_session_timeout_seconds=30.0,  # MCP ClientSession timeout
)
```

**Implementation**:

```python
# agent_config/todo_agent.py
import os
from pathlib import Path
from agents import Agent
from agents.mcp import MCPServerStdio
from agents.model_settings import ModelSettings
from agent_config.factory import create_model

class TodoAgent:
    """
    AI agent for conversational task management.

    Connects to MCP server via stdio for tool access.
    Supports multiple LLM providers via model factory.
    """

    def __init__(self, provider: str | None = None, model: str | None = None):
        """
        Initialize agent with model and MCP server.

        Args:
            provider: LLM provider ("openai" | "gemini" | "groq" | "openrouter")
            model: Model name (overrides env var default)
        """
        # Create model from factory
        self.model = create_model(provider=provider, model=model)

        # Get MCP server module path
        backend_dir = Path(__file__).parent.parent
        mcp_server_path = backend_dir / "mcp_server" / "tools.py"

        # Create MCP server connection via stdio
        # CRITICAL: Set client_session_timeout_seconds for database operations
        # Default: 5 seconds → Setting to 30 seconds for production
        self.mcp_server = MCPServerStdio(
            name="task-management-server",
            params={
                "command": "python",
                "args": ["-m", "mcp_server"],  # Run as module
                "env": os.environ.copy(),      # Pass environment
            },
            client_session_timeout_seconds=30.0,  # MCP ClientSession timeout
        )

        # Create agent
        # ModelSettings(parallel_tool_calls=False) prevents database lock issues
        self.agent = Agent(
            name="TodoAgent",
            model=self.model,
            instructions=AGENT_INSTRUCTIONS,  # See section 3.3
            mcp_servers=[self.mcp_server],
            model_settings=ModelSettings(
                parallel_tool_calls=False,  # Prevent concurrent DB writes
            ),
        )

    def get_agent(self) -> Agent:
        """Get configured agent instance."""
        return self.agent
```

**MCP Server Lifecycle**:

```python
# MCP server must be managed with async context manager
async with todo_agent.mcp_server:
    # Server is running, agent can call tools
    result = await Runner.run_streamed(
        agent=todo_agent.get_agent(),
        messages=[{"role": "user", "content": "Add buy milk"}]
    )
    # Process streaming results...
# Server stopped automatically
```

### 3.3 Agent Instructions

**Pattern**: Clear, behavioral instructions for conversational AI.

**Why**:
- Agent understands task domain and capabilities
- Handles natural language variations
- Provides friendly, helpful responses
- Never exposes technical details to users

**Example Instructions**:

```python
AGENT_INSTRUCTIONS = """
You are a helpful task management assistant. Your role is to help users manage
their todo lists through natural conversation.

## Your Capabilities

You have access to these task management tools:
- add_task: Create new tasks with title, description, priority
- list_tasks: Show tasks (all, pending, or completed)
- complete_task: Mark a task as done
- delete_task: Remove a task permanently
- update_task: Modify task details
- set_priority: Update task priority (low, medium, high)

## Behavior Guidelines

1. **Task Creation**
   - When user mentions adding/creating/remembering something, use add_task
   - Extract clear, actionable titles from messages
   - Confirm creation with friendly message

2. **Task Listing**
   - Use appropriate status filter (all, pending, completed)
   - Present tasks clearly with IDs for easy reference

3. **Conversational Style**
   - Be friendly, helpful, concise
   - Use natural language, not technical jargon
   - Acknowledge actions positively
   - NEVER expose internal IDs or technical details

## Response Pattern

✅ Good: "I've added 'Buy groceries' to your tasks!"
❌ Bad: "Task created with ID 42. Status: created."

✅ Good: "You have 3 pending tasks: Buy groceries, Call dentist, Pay bills"
❌ Bad: "Here's the JSON: [{...}]"
"""
```

### 3.4 MCP Server with Official MCP SDK

**Pattern**: MCP server exposes tools using Official MCP SDK (FastMCP).

**Why**:
- Standard MCP protocol compliance
- Easy tool registration with decorators
- Type-safe tool definitions
- Automatic schema generation

**Implementation**:

```python
# mcp_server/tools.py
import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types
from services.task_service import TaskService
from db import get_session
from sqlmodel import Session

# Create MCP server
app = Server("task-management-server")

@app.call_tool()
async def add_task(
    user_id: str,
    title: str,
    description: str | None = None,
    priority: str = "medium"
) -> list[types.TextContent]:
    """
    Create a new task for the user.

    Args:
        user_id: User's unique identifier
        title: Task title (required)
        description: Optional task description
        priority: Task priority (low, medium, high)

    Returns:
        Success message with task details
    """
    session = next(get_session())
    try:
        task = await TaskService.create_task(
            session=session,
            user_id=user_id,
            title=title,
            description=description,
            priority=priority
        )

        return [types.TextContent(
            type="text",
            text=f"Task created: {task.title} (Priority: {task.priority})"
        )]
    finally:
        session.close()

@app.call_tool()
async def list_tasks(
    user_id: str,
    status: str = "all"
) -> list[types.TextContent]:
    """
    List user's tasks filtered by status.

    Args:
        user_id: User's unique identifier
        status: Filter by status ("all", "pending", "completed")

    Returns:
        Formatted list of tasks
    """
    session = next(get_session())
    try:
        tasks = await TaskService.get_tasks(
            session=session,
            user_id=user_id,
            status=status
        )

        if not tasks:
            return [types.TextContent(
                type="text",
                text="No tasks found."
            )]

        task_list = "\n".join([
            f"{i+1}. [{task.status}] {task.title} (Priority: {task.priority})"
            for i, task in enumerate(tasks)
        ])

        return [types.TextContent(
            type="text",
            text=f"Your tasks:\n{task_list}"
        )]
    finally:
        session.close()

# Run server
async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
```

**Module Structure for MCP Server**:

```python
# mcp_server/__init__.py
"""MCP server exposing task management tools."""

# mcp_server/__main__.py
"""Entry point for MCP server when run as module."""
from mcp_server.tools import main
import asyncio

if __name__ == "__main__":
    asyncio.run(main())
```

### 3.5 Database Persistence (Conversations)

**Pattern**: Store conversation history in database for stateless backend.

**Why**:
- Stateless backend (no in-memory state)
- Users can resume conversations
- Full conversation history available
- Multi-device support

**Models**:

```python
# models.py
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from uuid import UUID, uuid4

class Conversation(SQLModel, table=True):
    """
    Conversation session between user and AI agent.
    """
    __tablename__ = "conversations"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    messages: list["Message"] = Relationship(back_populates="conversation")
    user: "User" = Relationship(back_populates="conversations")

class Message(SQLModel, table=True):
    """
    Individual message in a conversation.
    """
    __tablename__ = "messages"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    conversation_id: UUID = Field(foreign_key="conversations.id", index=True)
    user_id: UUID = Field(foreign_key="users.id", index=True)
    role: str = Field(index=True)  # "user" | "assistant" | "system"
    content: str
    tool_calls: str | None = None  # JSON string of tool calls
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    conversation: Conversation = Relationship(back_populates="messages")
    user: "User" = Relationship()
```

**Service Layer**:

```python
# services/conversation_service.py
from uuid import UUID
from sqlmodel import Session, select
from models import Conversation, Message

class ConversationService:
    @staticmethod
    async def get_or_create_conversation(
        session: Session,
        user_id: UUID,
        conversation_id: UUID | None = None
    ) -> Conversation:
        """Get existing conversation or create new one."""
        if conversation_id:
            stmt = select(Conversation).where(
                Conversation.id == conversation_id,
                Conversation.user_id == user_id
            )
            conversation = session.exec(stmt).first()
            if conversation:
                return conversation

        # Create new conversation
        conversation = Conversation(user_id=user_id)
        session.add(conversation)
        session.commit()
        session.refresh(conversation)
        return conversation

    @staticmethod
    async def add_message(
        session: Session,
        conversation_id: UUID,
        user_id: UUID,
        role: str,
        content: str,
        tool_calls: str | None = None
    ) -> Message:
        """Add message to conversation."""
        message = Message(
            conversation_id=conversation_id,
            user_id=user_id,
            role=role,
            content=content,
            tool_calls=tool_calls
        )
        session.add(message)
        session.commit()
        session.refresh(message)
        return message

    @staticmethod
    async def get_conversation_history(
        session: Session,
        conversation_id: UUID,
        user_id: UUID
    ) -> list[dict]:
        """Get conversation messages formatted for agent."""
        stmt = select(Message).where(
            Message.conversation_id == conversation_id,
            Message.user_id == user_id
        ).order_by(Message.created_at)

        messages = session.exec(stmt).all()

        return [
            {
                "role": msg.role,
                "content": msg.content
            }
            for msg in messages
        ]
```

### 3.6 FastAPI Streaming Endpoint

**Pattern**: SSE endpoint for streaming agent responses.

**Why**:
- Real-time streaming improves UX
- Works with ChatKit frontend
- Server-Sent Events (SSE) standard protocol
- Handles long-running agent calls

**Implementation**:

```python
# routers/chat.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlmodel import Session
from uuid import UUID
from db import get_session
from agent_config.todo_agent import TodoAgent
from services.conversation_service import ConversationService
from schemas.chat import ChatRequest
from agents import Runner

router = APIRouter()

@router.post("/{user_id}/chat")
async def chat(
    user_id: UUID,
    request: ChatRequest,
    session: Session = Depends(get_session)
):
    """
    Chat endpoint with streaming SSE response.

    Args:
        user_id: User's unique identifier
        request: ChatRequest with conversation_id and message
        session: Database session

    Returns:
        StreamingResponse with SSE events
    """
    # Get or create conversation
    conversation = await ConversationService.get_or_create_conversation(
        session=session,
        user_id=user_id,
        conversation_id=request.conversation_id
    )

    # Save user message
    await ConversationService.add_message(
        session=session,
        conversation_id=conversation.id,
        user_id=user_id,
        role="user",
        content=request.message
    )

    # Get conversation history
    history = await ConversationService.get_conversation_history(
        session=session,
        conversation_id=conversation.id,
        user_id=user_id
    )

    # Create agent
    todo_agent = TodoAgent()
    agent = todo_agent.get_agent()

    # Stream response
    async def event_generator():
        try:
            async with todo_agent.mcp_server:
                response_chunks = []

                async for chunk in Runner.run_streamed(
                    agent=agent,
                    messages=history,
                    context_variables={"user_id": str(user_id)}
                ):
                    # Handle different chunk types
                    if hasattr(chunk, 'delta') and chunk.delta:
                        response_chunks.append(chunk.delta)
                        yield f"data: {chunk.delta}\n\n"

                # Save assistant response
                full_response = "".join(response_chunks)
                await ConversationService.add_message(
                    session=session,
                    conversation_id=conversation.id,
                    user_id=user_id,
                    role="assistant",
                    content=full_response
                )

                yield "data: [DONE]\n\n"

        except Exception as e:
            yield f"data: Error: {str(e)}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )
```

## 4. Common Patterns

### 4.1 Error Handling

```python
# Handle provider API failures gracefully
try:
    async with todo_agent.mcp_server:
        result = await Runner.run_streamed(agent, messages)
except Exception as e:
    # Log error
    logger.error(f"Agent execution failed: {e}")
    # Return user-friendly message
    return {"error": "AI service temporarily unavailable. Please try again."}
```

### 4.2 Timeout Configuration

```python
# CRITICAL: Increase MCP timeout for database operations
# Default 5s is too short - may cause timeouts
MCPServerStdio(
    name="server",
    params={...},
    client_session_timeout_seconds=30.0,  # Increase from default 5s
)
```

### 4.3 Parallel Tool Calls Prevention

```python
# Prevent concurrent database writes (causes locks)
Agent(
    name="MyAgent",
    model=model,
    instructions=instructions,
    mcp_servers=[mcp_server],
    model_settings=ModelSettings(
        parallel_tool_calls=False,  # Serialize tool calls
    ),
)
```

## 5. Testing

### 5.1 Unit Tests (Model Factory)

```python
# tests/test_factory.py
import pytest
from agent_config.factory import create_model

def test_create_model_openai(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "openai")
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")

    model = create_model()
    assert model is not None

def test_create_model_missing_key(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "openai")
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    with pytest.raises(ValueError, match="OPENAI_API_KEY required"):
        create_model()
```

### 5.2 Integration Tests (MCP Tools)

```python
# tests/test_mcp_tools.py
import pytest
from mcp_server.tools import add_task

@pytest.mark.asyncio
async def test_add_task(test_session, test_user):
    result = await add_task(
        user_id=str(test_user.id),
        title="Test task",
        description="Test description",
        priority="high"
    )

    assert len(result) == 1
    assert "Task created" in result[0].text
    assert "Test task" in result[0].text
```

## 6. Production Checklist

- [ ] Set appropriate MCP timeout (30s+)
- [ ] Disable parallel tool calls for database operations
- [ ] Add error handling for provider API failures
- [ ] Implement retry logic with exponential backoff
- [ ] Add rate limiting to chat endpoints
- [ ] Monitor MCP server process health
- [ ] Log agent interactions for debugging
- [ ] Set up alerts for high error rates
- [ ] Use database connection pooling
- [ ] Configure CORS for production domains
- [ ] Validate JWT tokens on all endpoints
- [ ] Sanitize user inputs before tool execution
- [ ] Set up conversation cleanup (old conversations)
- [ ] Monitor database query performance
- [ ] Add caching for frequent queries

## 7. References

- **OpenAI Agents SDK**: https://github.com/openai/agents
- **Official MCP SDK**: https://github.com/modelcontextprotocol/python-sdk
- **FastAPI SSE**: https://fastapi.tiangolo.com/advanced/custom-response/#streamingresponse
- **SQLModel**: https://sqlmodel.tiangolo.com/
- **Better Auth**: https://better-auth.com/

---

**Last Updated**: December 2024
**Skill Version**: 1.0.0
**OpenAI Agents SDK**: v0.2.9+
**Official MCP SDK**: v1.0.0+
