---
name: xai
description: "xAI API (Grok) documentation - chat completions, reasoning, tools, image generation, and enterprise features."
---

# xAI (Grok) API Development

> **Source:** https://docs.x.ai

xAI provides the Grok family of AI models via a REST API that's OpenAI-compatible. Grok excels at truthful, insightful answers with unique capabilities like live web search and reasoning.

## Quick Start

```python
from openai import OpenAI

client = OpenAI(
    api_key="your-xai-api-key",
    base_url="https://api.x.ai/v1"
)

response = client.chat.completions.create(
    model="grok-3-latest",
    messages=[
        {"role": "user", "content": "What's happening in AI today?"}
    ]
)
print(response.choices[0].message.content)
```

## Model Selection

| Model | Best For | Context | Notes |
|-------|----------|---------|-------|
| `grok-3-latest` | General tasks | 131K | Flagship model |
| `grok-3-fast` | Speed-critical apps | 131K | Faster, lower cost |
| `grok-3-mini` | Cost-sensitive tasks | 131K | Smallest, cheapest |
| `grok-3-mini-fast` | High throughput | 131K | Speed + cost optimized |
| `grok-vision-beta` | Image understanding | 8K | Multimodal |
| `aurora` | Image generation | - | Image model |

## Key Features

### Chat with Reasoning

Grok 3 supports extended thinking for complex problems:

```python
response = client.chat.completions.create(
    model="grok-3-latest",
    messages=[{"role": "user", "content": "Solve this step by step..."}],
    reasoning_effort="high"  # low, medium, high
)
```

### Live Web Search

Enable real-time web access:

```python
response = client.chat.completions.create(
    model="grok-3-latest",
    messages=[{"role": "user", "content": "What's the latest news?"}],
    tools=[{"type": "web_search"}]
)
```

### Function Calling

```python
tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get weather for a location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {"type": "string"}
            },
            "required": ["location"]
        }
    }
}]

response = client.chat.completions.create(
    model="grok-3-latest",
    messages=[{"role": "user", "content": "Weather in Tokyo?"}],
    tools=tools,
    tool_choice="auto"
)
```

### Image Understanding

```python
response = client.chat.completions.create(
    model="grok-vision-beta",
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "What's in this image?"},
            {"type": "image_url", "image_url": {"url": "https://example.com/image.jpg"}}
        ]
    }]
)
```

### Image Generation

```python
response = client.images.generate(
    model="aurora",
    prompt="A futuristic city at sunset",
    n=1,
    size="1024x1024"
)
print(response.data[0].url)
```

### Structured Outputs

```python
response = client.chat.completions.create(
    model="grok-3-latest",
    messages=[{"role": "user", "content": "List 3 planets"}],
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "planets",
            "schema": {
                "type": "object",
                "properties": {
                    "planets": {
                        "type": "array",
                        "items": {"type": "string"}
                    }
                }
            }
        }
    }
)
```

## Best Practices

1. **Use OpenAI SDK** - xAI API is OpenAI-compatible; use the official OpenAI Python/JS SDK with `base_url="https://api.x.ai/v1"`

2. **Choose the right model** - Use `grok-3-latest` for quality, `grok-3-fast` for speed, `grok-3-mini` for cost

3. **Enable streaming** - For long responses, use `stream=True` to improve perceived latency

4. **Handle rate limits** - Implement exponential backoff; check `x-ratelimit-*` headers

5. **Use tools effectively** - Combine web search with function calling for powerful agentic workflows

6. **Regional endpoints** - Use regional endpoints for lower latency and data residency requirements

## Tools Available

Grok supports built-in tools:
- `web_search` - Real-time web search
- `code_execution` - Run Python code in sandbox
- `collection_search` - Search your uploaded documents
- Remote MCP tools - Connect to external MCP servers

## Stateful Responses API

For multi-turn conversations with memory:

```python
# Create a response with state
response = client.responses.create(
    model="grok-3-latest",
    input="Remember my name is Alice"
)

# Continue the conversation
response = client.responses.create(
    model="grok-3-latest",
    input="What's my name?",
    previous_response_id=response.id
)
```

## Documentation Index

| Resource | When to Consult |
|----------|-----------------|
| [overview.md](resources/overview.md) | Getting started |
| [models.md](resources/models.md) | Model selection and pricing |
| [guides-chat.md](resources/guides-chat.md) | Basic chat completions |
| [guides-reasoning.md](resources/guides-reasoning.md) | Extended thinking |
| [guides-tools-overview.md](resources/guides-tools-overview.md) | Tool use guide |
| [guides-function-calling.md](resources/guides-function-calling.md) | Function calling patterns |
| [guides-live-search.md](resources/guides-live-search.md) | Web search integration |
| [guides-image-understanding.md](resources/guides-image-understanding.md) | Vision capabilities |
| [guides-image-generations.md](resources/guides-image-generations.md) | Image generation |
| [guides-structured-outputs.md](resources/guides-structured-outputs.md) | JSON schema outputs |
| [api-reference.md](resources/api-reference.md) | API endpoints reference |

## Syncing Documentation

```bash
cd skills/xai
bun install        # Install playwright (first time only)
bun run scripts/sync-docs.ts
```

The sync script uses Playwright to bypass Cloudflare protection on docs.x.ai.
