---
name: ttadev-llm
description: 'Teaches how to call an LLM using TTA.dev primitives. Use when the user wants to call an LLM, use LiteLLM, use make_resilient_llm, integrate with an LLM provider, pick a model string for groq, anthropic, openai, gemini, ollama, or openrouter, stream tokens, use tool calls, or set up Langfuse observability. Covers LiteLLMPrimitive (primary path), UniversalLLMPrimitive (fallback), LLMRequest/LLMResponse types, streaming, ToolSchema, and the primary/fallback architecture.'
---

# TTA.dev LLM Primitives

TTA.dev exposes LLMs through two primitives:

| Primitive | Role | When to use |
|-----------|------|-------------|
| `LiteLLMPrimitive` | **Primary** — 100+ providers via litellm | Default for all new code |
| `UniversalLLMPrimitive` | **Fallback** — hand-rolled provider clients | Fallback / legacy; composable via `FallbackPrimitive` |

`make_resilient_llm()` is the one-liner factory that composes `LiteLLMPrimitive` + `RetryPrimitive` + `CachePrimitive` into a production-ready stack.

## When to Use This Skill

- Making any LLM API call in TTA.dev
- Choosing the right model string for Groq, Anthropic, Ollama, Gemini, or OpenRouter
- Adding streaming to an LLM call
- Using LLM tool-calling (function calling)
- Setting up Langfuse zero-config tracing
- Building a primary/fallback LLM architecture

## Prerequisites

```bash
uv sync                        # core + litellm included
uv sync --extra groq           # Groq-specific SDK (optional — litellm handles it)
uv sync --extra anthropic      # Anthropic SDK (optional)
```

**Environment variables:**

| Provider | Variable |
|----------|----------|
| Groq | `GROQ_API_KEY` |
| Anthropic | `ANTHROPIC_API_KEY` |
| OpenAI | `OPENAI_API_KEY` |
| Gemini (Google) | `GOOGLE_API_KEY` |
| OpenRouter | `OPENROUTER_API_KEY` |
| xAI | `XAI_API_KEY` |
| Ollama | *(none — localhost:11434)* |
| Langfuse | `LANGFUSE_SECRET_KEY`, `LANGFUSE_PUBLIC_KEY` |

## Model String Format

litellm uses `"<provider>/<model-name>"`:

```python
"groq/llama-3.1-8b-instant"
"groq/llama-3.3-70b-versatile"
"anthropic/claude-3-5-haiku-20241022"
"anthropic/claude-3-5-sonnet-20241022"
"ollama/llama3.2"
"ollama/mistral"
"gemini/gemini-2.0-flash"
"openrouter/meta-llama/llama-3-70b-instruct"
```

See [`references/provider-reference.md`](./references/provider-reference.md) for the full table.

## LLMRequest and LLMResponse

```python
from ttadev.primitives.llm import LLMRequest, LLMResponse

request = LLMRequest(
    model="groq/llama-3.1-8b-instant",   # full litellm string
    messages=[{"role": "user", "content": "Hello!"}],
    system="You are a helpful assistant.",  # optional system prompt
    temperature=0.7,                        # default 0.7
    max_tokens=512,                         # optional
)

# LLMResponse fields
response: LLMResponse
response.content    # str — generated text
response.model      # str — model that responded
response.provider   # str — provider name
response.usage      # dict — {"prompt_tokens": ..., "completion_tokens": ...}
response.tool_calls # list[ToolCall] | None — when tool-calling is used
```

## Quick Start — Single LLM Call

```python
import asyncio
from ttadev.primitives import LiteLLMPrimitive, WorkflowContext
from ttadev.primitives.llm import LLMRequest

llm = LiteLLMPrimitive()
ctx = WorkflowContext.root("llm-demo")

response = asyncio.run(llm.execute(
    LLMRequest(
        model="groq/llama-3.1-8b-instant",
        messages=[{"role": "user", "content": "What is 2 + 2?"}],
    ),
    ctx,
))
print(response.content)   # "4"
```

## make_resilient_llm — Production One-Liner

`make_resilient_llm()` composes `CachePrimitive → RetryPrimitive → LiteLLMPrimitive` in one call:

```python
from ttadev.primitives import make_resilient_llm, WorkflowContext
from ttadev.primitives.llm import LLMRequest

llm = make_resilient_llm(
    "groq",                                              # provider prefix
    litellm_fallbacks=["anthropic/claude-3-haiku-20240307", "ollama/llama3.2"],
    retry_attempts=3,       # default
    cache=True,             # default — SHA-256 keyed on messages+model+params
    cache_ttl_seconds=3600, # default — 1 hour
)

ctx      = WorkflowContext.root("resilient-demo")
response = asyncio.run(llm.execute(
    LLMRequest(model="llama-3.1-8b-instant", messages=[...]),
    ctx,
))
```

The composed stack:
```
CachePrimitive       ← keyed on messages + model + params
  └─ RetryPrimitive  ← 3 attempts, exponential back-off
       └─ LiteLLMPrimitive(provider="groq", fallbacks=[...])
```

## Streaming

Use `llm.stream(request, ctx)` — returns an `AsyncIterator[str]`:

```python
import asyncio
from ttadev.primitives import LiteLLMPrimitive, WorkflowContext
from ttadev.primitives.llm import LLMRequest

async def stream_demo() -> None:
    llm = LiteLLMPrimitive()
    ctx = WorkflowContext.root("stream-demo")
    req = LLMRequest(
        model="groq/llama-3.1-8b-instant",
        messages=[{"role": "user", "content": "Tell me a short story."}],
    )
    async for chunk in llm.stream(req, ctx):
        print(chunk, end="", flush=True)
    print()

asyncio.run(stream_demo())
```

## Tool Calls

Define tools with `ToolSchema`, pass them in `LLMRequest.tools`:

```python
from ttadev.primitives import LiteLLMPrimitive, WorkflowContext
from ttadev.primitives.llm import LLMRequest, ToolSchema
import asyncio

weather_tool = ToolSchema(
    name="get_weather",
    description="Return current weather for a city.",
    parameters={
        "type": "object",
        "properties": {
            "location": {"type": "string", "description": "City name"},
        },
        "required": ["location"],
    },
)

llm = LiteLLMPrimitive()
ctx = WorkflowContext.root("tool-demo")
req = LLMRequest(
    model="groq/llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": "What is the weather in Paris?"}],
    tools=[weather_tool],
    tool_choice="auto",
)
response = asyncio.run(llm.execute(req, ctx))
if response.tool_calls:
    for tc in response.tool_calls:
        print(tc.name, tc.arguments)  # get_weather {"location": "Paris"}
```

## Langfuse Observability — Zero Config

Set env vars; tracing is automatic:

```bash
export LANGFUSE_SECRET_KEY=sk-lf-...
export LANGFUSE_PUBLIC_KEY=pk-lf-...
# LANGFUSE_HOST defaults to https://cloud.langfuse.com
```

Every `LiteLLMPrimitive.execute()` call is traced. No code changes needed.

## Primary / Fallback Architecture

Use `FallbackPrimitive` to fall back from `LiteLLMPrimitive` to `UniversalLLMPrimitive`:

```python
from ttadev.primitives import FallbackPrimitive, WorkflowContext
from ttadev.primitives.llm import LiteLLMPrimitive, UniversalLLMPrimitive, LLMProvider

primary  = LiteLLMPrimitive()                             # litellm — primary
fallback = UniversalLLMPrimitive(provider=LLMProvider.GROQ)  # direct SDK — fallback

resilient = FallbackPrimitive(primary, fallback)

ctx      = WorkflowContext.root("primary-fallback")
response = asyncio.run(resilient.execute(request, ctx))
```

## Anti-Patterns

| ❌ Never | ✅ Use instead |
|---------|---------------|
| `import anthropic; client.messages.create(...)` directly | `LiteLLMPrimitive` with model string |
| Hard-code retry loops around LLM calls | `make_resilient_llm()` |
| Cache responses in a global dict | `make_resilient_llm(cache=True)` |
| Hard-code a single provider | `litellm_fallbacks=[...]` |

## Provider Reference

Full table of model strings by provider → [`references/provider-reference.md`](./references/provider-reference.md)
