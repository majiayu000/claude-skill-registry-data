---
name: langchain
description: "LangChain high-level agent framework. Build agents with tools, memory, and streaming in under 10 lines of code."
---

# LangChain Development

> **Source:** https://github.com/langchain-ai/docs (src/oss/langchain/)

LangChain is the high-level API for building agents and LLM applications. It provides a simple `create_agent` interface built on top of LangGraph. Use LangChain for quick agent development; use LangGraph directly when you need fine-grained control over workflows.

## Quick Start

### Basic Agent

```python
from langchain.agents import create_agent

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's sunny in {city}!"

agent = create_agent(
    model="claude-sonnet-4-5-20250929",
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

response = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the weather in SF?"}]}
)
```

### With Streaming

```python
from langchain.agents import create_agent

agent = create_agent(
    model="gpt-4o",
    tools=[get_weather],
)

for chunk in agent.stream({"messages": [{"role": "user", "content": "Weather in NYC?"}]}):
    print(chunk)
```

## Model Selection

LangChain supports model identifier strings or direct model instances:

```python
# String identifier (auto-inferred provider)
agent = create_agent("gpt-4o", tools=tools)
agent = create_agent("claude-sonnet-4-5-20250929", tools=tools)

# Explicit provider prefix
agent = create_agent("openai:gpt-4o", tools=tools)
agent = create_agent("anthropic:claude-sonnet-4-5-20250929", tools=tools)

# Direct model instance for full control
from langchain_openai import ChatOpenAI

model = ChatOpenAI(
    model="gpt-4o",
    temperature=0.1,
    max_tokens=4096,
    timeout=30,
)
agent = create_agent(model, tools=tools)
```

## Tools

Define tools as functions with docstrings:

```python
from langchain.tools import tool

@tool
def search_database(query: str, limit: int = 10) -> list[dict]:
    """Search the database for records matching the query.

    Args:
        query: The search query string
        limit: Maximum number of results to return

    Returns:
        List of matching records
    """
    # Implementation here
    return results

agent = create_agent(
    model="gpt-4o",
    tools=[search_database],
)
```

## Memory

### Short-Term Memory (Conversation History)

```python
from langchain.agents import create_agent

agent = create_agent(
    model="gpt-4o",
    tools=tools,
)

# Memory is maintained across invocations with thread_id
config = {"configurable": {"thread_id": "user-123"}}

agent.invoke({"messages": [{"role": "user", "content": "My name is Alice"}]}, config)
agent.invoke({"messages": [{"role": "user", "content": "What's my name?"}]}, config)
# Agent remembers: "Your name is Alice"
```

### Long-Term Memory

```python
from langchain.agents import create_agent
from langchain.memory import InMemoryStore

memory_store = InMemoryStore()

agent = create_agent(
    model="gpt-4o",
    tools=tools,
    memory=memory_store,
)
```

## Middleware

Customize agent behavior with middleware:

```python
from langchain.agents import create_agent
from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse

@wrap_model_call
def log_requests(request: ModelRequest) -> ModelResponse:
    print(f"Calling model with {len(request.messages)} messages")
    response = yield request
    print(f"Got response: {response.content[:100]}...")
    return response

agent = create_agent(
    model="gpt-4o",
    tools=tools,
    middleware=[log_requests],
)
```

## Structured Output

```python
from langchain.agents import create_agent
from pydantic import BaseModel

class Analysis(BaseModel):
    summary: str
    sentiment: str
    confidence: float

agent = create_agent(
    model="gpt-4o",
    tools=tools,
    response_format=Analysis,
)

result = agent.invoke({"messages": [{"role": "user", "content": "Analyze this text..."}]})
# result.content is an Analysis instance
```

## Human-in-the-Loop

```python
from langchain.agents import create_agent

agent = create_agent(
    model="gpt-4o",
    tools=tools,
    interrupt_before=["tools"],  # Pause before tool execution
)

# Run until interrupt
result = agent.invoke({"messages": [{"role": "user", "content": "Delete all files"}]})

# Review pending tool calls, then continue or abort
if user_approves:
    result = agent.invoke(None, config)  # Continue execution
```

## Best Practices

1. **Use string model identifiers** for quick prototyping; switch to model instances for production control
2. **Define clear tool docstrings** - the model uses these to decide when/how to call tools
3. **Use middleware** for cross-cutting concerns (logging, rate limiting, caching)
4. **Enable streaming** for better UX in interactive applications
5. **Set appropriate timeouts** on model instances for production reliability
6. **Use thread_id** for conversation continuity across requests

## When to Use LangGraph Instead

Use LangGraph directly when you need:
- Complex multi-step workflows with branching logic
- Fine-grained control over state management
- Custom graph topologies beyond simple agent loops
- Heavy customization of execution flow
- Carefully controlled latency requirements

## Documentation Index

| Resource | When to Consult |
|----------|-----------------|
| [overview.md](resources/overview.md) | Getting started, core benefits |
| [quickstart.md](resources/quickstart.md) | Step-by-step first agent tutorial |
| [agents.md](resources/agents.md) | Agent architecture, ReAct pattern, core components |
| [models.md](resources/models.md) | Model selection, configuration, dynamic routing |
| [tools.md](resources/tools.md) | Tool definition, schemas, error handling |
| [streaming.md](resources/streaming.md) | Streaming responses and events |
| [structured-output.md](resources/structured-output.md) | Pydantic models, JSON schemas |
| [short-term-memory.md](resources/short-term-memory.md) | Conversation history, thread management |
| [long-term-memory.md](resources/long-term-memory.md) | Persistent memory stores |
| [middleware/](resources/middleware/) | Built-in and custom middleware |
| [human-in-the-loop.md](resources/human-in-the-loop.md) | Interrupts, approvals, review flows |
| [multi-agent.md](resources/multi-agent.md) | Multi-agent architectures |
| [guardrails.md](resources/guardrails.md) | Input/output validation, safety |
| [mcp.md](resources/mcp.md) | Model Context Protocol integration |
| [observability.md](resources/observability.md) | LangSmith tracing, debugging |
| [deploy.md](resources/deploy.md) | Deployment options |
| [errors/](resources/errors/) | Error codes and troubleshooting |

## Syncing Documentation

```bash
cd skills/langchain
bun run scripts/sync-docs.ts
```
