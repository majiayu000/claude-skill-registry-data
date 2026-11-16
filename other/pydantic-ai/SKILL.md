---
name: pydantic-ai
description: Build type-safe AI agents with PydanticAI — define Agent with result_type, system_prompt, tools (function tools + structured tools), deps injection, and run sync/async with full Pydantic validation on inputs and outputs.
triggers:
  - "pydantic ai"
  - "pydanticai"
  - "pydantic agent"
  - "agent result_type"
  - "type safe llm agent"
  - "pydantic tool agent"
  - "agent deps injection"
  - "agent system_prompt decorator"
  - "pydantic ai run"
  - "pydantic ai stream"
  - "agent with structured output pydantic"
do_not_use_for:
  - Multi-agent crew orchestration — use crewai instead
  - State graph agents — use langgraph instead
  - Workflow automation — use n8n-automation instead
see_also:
  - crewai
  - langgraph
  - instructor-structured-output
---

# PydanticAI — Type-Safe AI Agents

**Source:** pydantic/pydantic-ai (MIT) — production-grade AI agents with Pydantic validation

## Why PydanticAI

- **Type-safe by default**: result_type enforces Pydantic schema on LLM output
- **Dependency injection**: clean way to pass DB, HTTP clients, config to tools
- **First-class streaming**: stream structured responses with partial validation
- **Model-agnostic**: OpenAI, Anthropic, Google, Groq, Ollama out of the box
- **Testable**: swap models for `TestModel` in unit tests

## Install

```bash
pip install pydantic-ai
# model providers
pip install pydantic-ai[anthropic]
pip install pydantic-ai[openai]
```

## Minimal Agent

```python
from pydantic_ai import Agent

agent = Agent(
    "claude-sonnet-4-5",
    system_prompt="You are a helpful assistant.",
)

result = agent.run_sync("What is the capital of France?")
print(result.data)  # "Paris"
```

## Structured Output

```python
from pydantic import BaseModel
from pydantic_ai import Agent

class CityInfo(BaseModel):
    city: str
    country: str
    population: int
    fun_fact: str

agent = Agent(
    "claude-sonnet-4-5",
    result_type=CityInfo,
    system_prompt="Extract city information from user messages.",
)

result = agent.run_sync("Tell me about Tokyo")
info = result.data  # CityInfo instance — fully typed
print(info.city, info.population)
```

## Tools (Function Tools)

```python
from pydantic_ai import Agent, RunContext
from dataclasses import dataclass
import httpx

@dataclass
class Deps:
    http_client: httpx.AsyncClient
    api_key: str

agent = Agent(
    "claude-sonnet-4-5",
    deps_type=Deps,
    system_prompt="You can look up weather information.",
)

@agent.tool
async def get_weather(ctx: RunContext[Deps], city: str) -> str:
    """Get current weather for a city."""
    resp = await ctx.deps.http_client.get(
        f"https://api.weather.com/v1/current",
        params={"city": city, "key": ctx.deps.api_key},
    )
    data = resp.json()
    return f"{data['temp']}°C, {data['condition']}"

@agent.tool_plain  # no ctx access, pure function
def celsius_to_fahrenheit(celsius: float) -> float:
    """Convert Celsius to Fahrenheit."""
    return celsius * 9/5 + 32

async def main():
    async with httpx.AsyncClient() as client:
        deps = Deps(http_client=client, api_key="my-key")
        result = await agent.run("What's the weather in Tokyo?", deps=deps)
        print(result.data)
```

## Dynamic System Prompt

```python
from pydantic_ai import Agent, RunContext
from dataclasses import dataclass

@dataclass
class UserDeps:
    username: str
    role: str

agent = Agent("claude-sonnet-4-5", deps_type=UserDeps)

@agent.system_prompt
def build_system_prompt(ctx: RunContext[UserDeps]) -> str:
    return f"You are helping {ctx.deps.username} who is a {ctx.deps.role}."

result = agent.run_sync(
    "Help me with my task",
    deps=UserDeps(username="Alice", role="data scientist"),
)
```

## Streaming

```python
import asyncio
from pydantic_ai import Agent
from pydantic import BaseModel

class Summary(BaseModel):
    title: str
    points: list[str]

agent = Agent("claude-sonnet-4-5", result_type=Summary)

async def main():
    async with agent.run_stream("Summarize AI trends") as result:
        # stream text deltas
        async for text in result.stream_text():
            print(text, end="", flush=True)

    # structured result available after stream completes
    final = await result.get_data()
    print(final.title, final.points)

asyncio.run(main())
```

## Multi-Turn Conversations

```python
from pydantic_ai import Agent
from pydantic_ai.messages import ModelMessagesTypeAdapter

agent = Agent("claude-sonnet-4-5", system_prompt="You are a helpful assistant.")

# First turn
result1 = agent.run_sync("My name is Alice.")
print(result1.data)

# Continue conversation — pass message history
result2 = agent.run_sync(
    "What's my name?",
    message_history=result1.new_messages(),
)
print(result2.data)  # "Your name is Alice."

# Serialize history for persistence
history_json = result2.all_messages_json()
# Restore later:
history = ModelMessagesTypeAdapter.validate_json(history_json)
```

## Result Validators

```python
from pydantic_ai import Agent, ModelRetry

agent = Agent("claude-sonnet-4-5", result_type=int)

@agent.result_validator
async def validate_positive(ctx, result: int) -> int:
    if result <= 0:
        raise ModelRetry("Result must be positive. Try again.")
    return result

result = agent.run_sync("Give me a positive number")
```

## Testing with TestModel

```python
from pydantic_ai import Agent
from pydantic_ai.models.test import TestModel

agent = Agent("claude-sonnet-4-5", system_prompt="You answer math questions.")

def test_addition():
    with agent.override(model=TestModel()):
        result = agent.run_sync("What is 2+2?")
        # TestModel returns deterministic canned responses
        assert result.data is not None

# Or use FunctionModel for custom test responses
from pydantic_ai.models.function import FunctionModel, ModelContext

def my_test_model(messages, info: ModelContext):
    return "4"

with agent.override(model=FunctionModel(my_test_model)):
    result = agent.run_sync("What is 2+2?")
    assert result.data == "4"
```

## Supported Models

```python
from pydantic_ai.models.anthropic import AnthropicModel
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.models.groq import GroqModel
from pydantic_ai.models.ollama import OllamaModel

# Use model string shorthand
agent = Agent("claude-sonnet-4-5")
agent = Agent("gpt-4o")
agent = Agent("gemini-2.0-flash")

# Or explicit model instance with custom config
model = AnthropicModel("claude-opus-4-5", max_tokens=8192)
agent = Agent(model)
```

## Usage Stats

```python
result = agent.run_sync("Hello")
print(result.usage())
# Usage(requests=1, request_tokens=25, response_tokens=10, total_tokens=35)
```

## Anti-Fake-Pass Checks

- [ ] `result.data` holds the validated result, not `result.output` or `result.text`
- [ ] `@agent.tool` receives `ctx: RunContext[DepsType]` as first arg — omit for `@agent.tool_plain`
- [ ] `deps_type` must be declared on Agent for `ctx.deps` to be typed
- [ ] `ModelRetry` from `pydantic_ai` retries the LLM call — not a Python exception
- [ ] `run_sync` is a sync wrapper; use `await agent.run(...)` in async contexts
- [ ] `result.new_messages()` returns only new messages; `result.all_messages()` returns full history
