---
name: langchain
description: LangChain framework for building AI agents and LLM applications with tools, memory, and streaming support
version: "1.0.0"
license: MIT
metadata:
  author: LangChain
  tags: [llm, ai, agent, langchain, python]
  official_docs: https://docs.langchain.com/oss/python/langchain
---

# LangChain

> LangChain is the easy way to build custom agents and applications powered by LLMs. With under 10 lines of code, you can connect to OpenAI, Anthropic, Google, and more.

## Preferences

- Use `create_agent` as the unified interface for creating agents
- Prefer structured output for reliable data extraction
- Always implement error handling for production agents
- Use streaming for better user experience
- Leverage middleware for cross-cutting concerns

## Core Components

| Topic | Description | Reference |
|-------|-------------|-----------|
| Agents | Core agent architecture with create_agent | [agents-basics.md](references/agents-basics.md) |
| Models | Model integration (OpenAI, Anthropic, etc.) | [models-integration.md](references/models-integration.md) |
| Messages | Message formats and conversation structure | [messages-format.md](references/messages-format.md) |
| Tools | Tool definition and dynamic tool selection | [agents-tools.md](references/agents-tools.md) |
| Memory | Short-term and conversation memory | [memory-short-term.md](references/memory-short-term.md) |
| Streaming | Streaming output for real-time responses | [streaming-output.md](references/streaming-output.md) |
| Structured Output | Structured data extraction from LLMs | [structured-output.md](references/structured-output.md) |

## Middleware

| Topic | Description | Reference |
|-------|-------------|-----------|
| Middleware Overview | Middleware architecture and patterns | [middleware-overview.md](references/middleware-overview.md) |
| Human-in-the-Loop | Add human intervention to agents | [middleware-human-in-loop.md](references/middleware-human-in-loop.md) |

## Additional Features

| Topic | Description | Reference |
|-------|-------------|-----------|
| Prompt Templates | Reusable prompt templates | [prompt-templates.md](references/prompt-templates.md) |
| RAG Basics | Retrieval Augmented Generation | [rag-basics.md](references/rag-basics.md) |
| Error Handling | Production error handling patterns | [error-handling.md](references/error-handling.md) |

## Quick Reference

### Basic Agent

```python
from langchain.agents import create_agent

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_agent(
    model="claude-sonnet-4-6",
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "what is the weather in sf"}]}
)
```

### Agent with Model Instance

```python
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

model = ChatOpenAI(
    model="gpt-4",
    temperature=0.1,
    max_tokens=1000,
    timeout=30
)

agent = create_agent(model, tools=[get_weather])
```

### Streaming Agent

```python
from langchain.agents import create_agent

agent = create_agent(
    model="gpt-4",
    tools=[get_weather],
    streaming=True
)

async for chunk in agent.stream({"messages": [...]}):
    print(chunk.content, end="", flush=True)
```

### Structured Output

```python
from pydantic import BaseModel
from langchain.agents import create_agent

class WeatherReport(BaseModel):
    city: str
    temperature: float
    condition: str

agent = create_agent(
    model="gpt-4",
    output_schema=WeatherReport
)

result = agent.invoke({"messages": [...]})
weather = result.structured_output
```

## Key Imports

```python
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain.agents.middleware import (
    wrap_model_call,
    SummarizationMiddleware,
    HumanInTheLoopMiddleware
)
```

## Official Documentation

- Main: https://docs.langchain.com/oss/python/langchain
- Agents: https://docs.langchain.com/oss/python/langchain/agents
- Models: https://docs.langchain.com/oss/python/langchain/models
- Tools: https://docs.langchain.com/oss/python/langchain/tools
- Memory: https://docs.langchain.com/oss/python/langchain/memory
- Streaming: https://docs.langchain.com/oss/python/langchain/streaming
