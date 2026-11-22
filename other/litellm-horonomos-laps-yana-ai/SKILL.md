---
name: litellm
description: Call 100+ LLMs through a single OpenAI-compatible interface with LiteLLM — use completion/acompletion/embedding with any provider (Anthropic, OpenAI, Google, Groq, Ollama, etc.), run a proxy server for team rate-limiting and cost tracking, load-balance across providers.
triggers:
  - "litellm"
  - "lite llm"
  - "unified llm api"
  - "llm proxy server"
  - "multi provider llm"
  - "litellm completion"
  - "litellm proxy"
  - "llm fallback"
  - "llm load balancing"
  - "litellm budget"
  - "litellm router"
  - "openai compatible proxy"
  - "switch llm provider"
do_not_use_for:
  - Fine-tuning — use llamafactory instead
  - Agent orchestration — use crewai or langgraph instead
  - Structured output validation — use pydantic-ai or instructor-structured-output instead
see_also:
  - instructor-structured-output
  - pydantic-ai
  - vercel-ai-sdk
---

# LiteLLM — Unified LLM API

**Source:** BerriAI/litellm (MIT) — call 100+ LLMs with a single OpenAI-compatible interface

## Why LiteLLM

- **One API** for OpenAI, Anthropic, Google, Groq, Mistral, Ollama, AWS Bedrock, Azure, etc.
- **OpenAI SDK compatible** — drop-in replacement, just change `base_url`
- **Proxy server** — centralize API keys, add rate limits, track costs, log requests
- **Router** — load balance + fallback across multiple models/providers

## Install

```bash
pip install litellm
# Optional: proxy server
pip install 'litellm[proxy]'
```

## Basic Completion

```python
from litellm import completion

# Anthropic
response = completion(
    model="claude-sonnet-4-5",
    messages=[{"role": "user", "content": "Hello"}],
    api_key="your-anthropic-key",
)

# OpenAI
response = completion(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello"}],
)

# Google
response = completion(
    model="gemini/gemini-2.0-flash",
    messages=[{"role": "user", "content": "Hello"}],
)

# Groq
response = completion(
    model="groq/llama-3.1-70b-versatile",
    messages=[{"role": "user", "content": "Hello"}],
)

# Local Ollama
response = completion(
    model="ollama/llama3",
    messages=[{"role": "user", "content": "Hello"}],
    api_base="http://localhost:11434",
)

# Access response (OpenAI format)
print(response.choices[0].message.content)
print(response.usage.total_tokens)
```

## Async Completion

```python
import asyncio
from litellm import acompletion

async def main():
    response = await acompletion(
        model="claude-sonnet-4-5",
        messages=[{"role": "user", "content": "Explain quantum computing"}],
    )
    print(response.choices[0].message.content)

asyncio.run(main())
```

## Streaming

```python
from litellm import completion

response = completion(
    model="claude-sonnet-4-5",
    messages=[{"role": "user", "content": "Write a poem about AI"}],
    stream=True,
)

for chunk in response:
    content = chunk.choices[0].delta.content or ""
    print(content, end="", flush=True)
```

## Function Calling / Tools

```python
from litellm import completion

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string"},
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                },
                "required": ["city"],
            },
        },
    }
]

response = completion(
    model="claude-sonnet-4-5",
    messages=[{"role": "user", "content": "What's the weather in Tokyo?"}],
    tools=tools,
    tool_choice="auto",
)

# Check if tool was called
if response.choices[0].finish_reason == "tool_calls":
    tool_call = response.choices[0].message.tool_calls[0]
    print(tool_call.function.name)    # "get_weather"
    print(tool_call.function.arguments)  # '{"city": "Tokyo"}'
```

## Embeddings

```python
from litellm import embedding

# OpenAI
resp = embedding(model="text-embedding-3-small", input=["Hello world"])

# Cohere
resp = embedding(model="cohere/embed-english-v3.0", input=["Hello world"])

# Bedrock
resp = embedding(model="bedrock/amazon.titan-embed-text-v1", input=["Hello world"])

vectors = resp.data[0]["embedding"]  # list of floats
```

## Router — Load Balancing & Fallbacks

```python
from litellm import Router

router = Router(
    model_list=[
        {
            "model_name": "claude-fast",
            "litellm_params": {
                "model": "claude-haiku-4-5",
                "api_key": "your-key",
            },
            "tpm": 100_000,  # tokens per minute limit
        },
        {
            "model_name": "claude-fast",  # same group name = load balance
            "litellm_params": {
                "model": "claude-sonnet-4-5",
                "api_key": "your-key",
            },
        },
        {
            "model_name": "fallback-model",
            "litellm_params": {"model": "gpt-4o-mini"},
        },
    ],
    fallbacks=[{"claude-fast": ["fallback-model"]}],  # fallback on error
    routing_strategy="least-busy",  # or "latency-based", "simple-shuffle"
    retry_after=5,
    num_retries=3,
)

response = router.completion(
    model="claude-fast",
    messages=[{"role": "user", "content": "Hello"}],
)
```

## Proxy Server

```bash
# Start proxy (routes all requests through LiteLLM)
litellm --model claude-sonnet-4-5 --port 8000

# Or with config file
litellm --config config.yaml
```

```yaml
# config.yaml
model_list:
  - model_name: claude-fast
    litellm_params:
      model: claude-haiku-4-5
      api_key: os.environ/ANTHROPIC_API_KEY

  - model_name: gpt4
    litellm_params:
      model: gpt-4o
      api_key: os.environ/OPENAI_API_KEY

litellm_settings:
  drop_params: true          # ignore unsupported params per model
  request_timeout: 30
  max_budget: 100            # $100 budget limit

router_settings:
  routing_strategy: least-busy
  num_retries: 3
  fallbacks: [{"claude-fast": ["gpt4"]}]
```

```python
# Use proxy with OpenAI SDK (drop-in replacement)
from openai import OpenAI

client = OpenAI(
    api_key="anything",       # proxy handles auth
    base_url="http://localhost:8000",
)

response = client.chat.completions.create(
    model="claude-fast",      # proxy routes to correct model
    messages=[{"role": "user", "content": "Hello"}],
)
```

## Cost Tracking

```python
import litellm

litellm.success_callback = ["langfuse"]  # or "langsmith", "helicone"

# Or manual cost calculation
from litellm import completion_cost, model_cost

response = completion(model="claude-sonnet-4-5", messages=[...])
cost = completion_cost(completion_response=response)
print(f"Cost: ${cost:.6f}")

# Get model pricing
pricing = model_cost["claude-sonnet-4-5"]
print(pricing["input_cost_per_token"], pricing["output_cost_per_token"])
```

## Environment Variable Config

```bash
# Set API keys as env vars — LiteLLM picks them up automatically
export ANTHROPIC_API_KEY="..."
export OPENAI_API_KEY="..."
export GOOGLE_API_KEY="..."
export GROQ_API_KEY="..."

# LiteLLM debug logging
export LITELLM_LOG="DEBUG"
```

## Drop-In for OpenAI SDK

```python
# Before (OpenAI only)
from openai import OpenAI
client = OpenAI()
response = client.chat.completions.create(model="gpt-4o", messages=[...])

# After (any provider via LiteLLM proxy)
from openai import OpenAI
client = OpenAI(base_url="http://localhost:8000", api_key="fake")
response = client.chat.completions.create(model="claude-sonnet-4-5", messages=[...])
```

## Anti-Fake-Pass Checks

- [ ] Response format is always OpenAI-compatible: `response.choices[0].message.content`
- [ ] Model string format: `provider/model` for non-OpenAI (e.g., `groq/llama3`, `ollama/mistral`)
- [ ] `anthropic/` prefix NOT needed for Anthropic — just `"claude-sonnet-4-5"` works
- [ ] Router `model_name` is the alias you call — `litellm_params.model` is the actual model
- [ ] Fallbacks need same model_name group — different names require `fallbacks` config
- [ ] `drop_params=True` in config prevents errors when sending unsupported params cross-provider
