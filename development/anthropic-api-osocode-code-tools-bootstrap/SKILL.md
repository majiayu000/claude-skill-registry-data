---
allowed-tools: Read, Grep, Glob, Bash, Write, Edit, WebFetch, WebSearch
description: 'Expert guidance for building applications with Anthropic''s Claude API.

  Covers SDK patterns (Python, TypeScript), cost optimization, prompt caching,

  batch processing, streaming, tool use, and production best practices.

  Includes anti-patterns to avoid and common mistakes with fixes.'
name: anthropic-api
---

# Anthropic Claude API Expert Guide

Build production-grade applications with Anthropic's Claude API using best practices, cost optimization strategies, and proven patterns.

## Model Selection Guide

| Model | Model ID | Best For | Input/Output Cost |
|-------|----------|----------|-------------------|
| **Claude Opus 4.5** | `claude-opus-4-5-20250514` | Most capable, complex reasoning | $5 / $25 per MTok |
| **Claude Sonnet 4.5** | `claude-sonnet-4-5-20250514` | Balanced performance/cost | $3 / $15 per MTok |
| **Claude Haiku 4.5** | `claude-haiku-4-5-20250514` | Fast, high-volume, cost-efficient | $1 / $5 per MTok |

**Decision Framework:**
- **Use Haiku** for: Classification, extraction, simple Q&A, high-volume workloads
- **Use Sonnet** for: Code generation, analysis, most production use cases (90% of Opus quality at 20% cost)
- **Use Opus** for: Complex reasoning, research, when quality is paramount

## Setup

### Python SDK

```bash
pip install anthropic
```

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ["ANTHROPIC_API_KEY"]  # Default, can be omitted
)

message = client.messages.create(
    model="claude-sonnet-4-5-20250514",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Hello, Claude"}
    ]
)
print(message.content[0].text)
```

### TypeScript SDK

```bash
npm install @anthropic-ai/sdk
```

```typescript
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});

const message = await client.messages.create({
  model: "claude-sonnet-4-5-20250514",
  max_tokens: 1024,
  messages: [{ role: "user", content: "Hello, Claude" }],
});
console.log(message.content[0].text);
```

## Cost Optimization Strategies

### 1. Prompt Caching (Up to 90% Savings)

Cache stable content like system prompts, documents, or tool definitions. Cache hits cost only 10% of base input price.

```python
from anthropic import Anthropic

client = Anthropic()

# First request - writes to cache (1.25x input cost)
response = client.messages.create(
    model="claude-sonnet-4-5-20250514",
    max_tokens=1024,
    system=[
        {
            "type": "text",
            "text": "You are an expert legal assistant...",  # Large system prompt
            "cache_control": {"type": "ephemeral"}  # 5-minute cache
        }
    ],
    messages=[{"role": "user", "content": "Analyze this contract..."}]
)

# Subsequent requests within 5 minutes - cache hit (0.1x input cost)
response2 = client.messages.create(
    model="claude-sonnet-4-5-20250514",
    max_tokens=1024,
    system=[
        {
            "type": "text",
            "text": "You are an expert legal assistant...",  # Same content
            "cache_control": {"type": "ephemeral"}
        }
    ],
    messages=[{"role": "user", "content": "Different question..."}]
)

# Check cache usage
print(f"Cache read: {response2.usage.cache_read_input_tokens}")
print(f"Cache write: {response2.usage.cache_creation_input_tokens}")
```

**Cache Duration Options:**
- `ephemeral` - 5-minute cache (1.25x write, 0.1x read)
- For 1-hour cache, use extended caching (2x write, 0.1x read)

**Minimum Token Requirements:**
- Claude 3.5+ models: 1,024 tokens minimum per cache checkpoint
- Content below minimum won't be cached

### 2. Batch API (50% Discount)

Process large volumes asynchronously with guaranteed 24-hour completion.

```python
import asyncio
from anthropic import AsyncAnthropic

client = AsyncAnthropic()

async def process_batch():
    # Create batch
    batch = await client.messages.batches.create(
        requests=[
            {
                "custom_id": "request-1",
                "params": {
                    "model": "claude-sonnet-4-5-20250514",
                    "max_tokens": 1024,
                    "messages": [{"role": "user", "content": "Summarize document 1"}]
                }
            },
            {
                "custom_id": "request-2",
                "params": {
                    "model": "claude-sonnet-4-5-20250514",
                    "max_tokens": 1024,
                    "messages": [{"role": "user", "content": "Summarize document 2"}]
                }
            }
        ]
    )

    print(f"Batch ID: {batch.id}")

    # Poll for results (or use webhooks)
    while True:
        batch = await client.messages.batches.retrieve(batch.id)
        if batch.processing_status == "ended":
            break
        await asyncio.sleep(60)

    # Get results
    async for entry in await client.messages.batches.results(batch.id):
        if entry.result.type == "succeeded":
            print(f"{entry.custom_id}: {entry.result.message.content[0].text}")
```

**When to Use Batch:**
- Background processing (reports, analysis)
- Bulk content generation
- Data enrichment pipelines
- Any non-real-time workload

### 3. Token Optimization

```python
# Count tokens before sending (estimate costs)
token_count = client.messages.count_tokens(
    model="claude-sonnet-4-5-20250514",
    messages=[{"role": "user", "content": "Your message here"}]
)
print(f"Input tokens: {token_count.input_tokens}")

# Set appropriate max_tokens (don't over-reserve)
response = client.messages.create(
    model="claude-sonnet-4-5-20250514",
    max_tokens=500,  # Set to expected output, not maximum
    messages=[{"role": "user", "content": "Brief summary of..."}]
)

# Check actual usage
print(f"Used: {response.usage.output_tokens} tokens")
```

## Streaming

### Basic Streaming

```python
from anthropic import Anthropic

client = Anthropic()

# Simple streaming
with client.messages.stream(
    model="claude-sonnet-4-5-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Tell me a story"}]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
    print()

    # Get final message after stream completes
    message = stream.get_final_message()
    print(f"Total tokens: {message.usage.output_tokens}")
```

### Async Streaming

```python
import asyncio
from anthropic import AsyncAnthropic

client = AsyncAnthropic()

async def stream_response():
    async with client.messages.stream(
        model="claude-sonnet-4-5-20250514",
        max_tokens=1024,
        messages=[{"role": "user", "content": "Explain quantum computing"}]
    ) as stream:
        async for text in stream.text_stream:
            print(text, end="", flush=True)
        print()

asyncio.run(stream_response())
```

### Handling All Event Types

```python
async with client.messages.stream(
    model="claude-sonnet-4-5-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Use a tool"}]
) as stream:
    async for event in stream:
        if event.type == "text":
            print(event.text, end="")
        elif event.type == "input_json":
            # Tool input being streamed
            print(f"Tool input delta: {event.partial_json}")
        elif event.type == "content_block_stop":
            print(f"\nBlock complete: {event.content_block}")
        elif event.type == "message_stop":
            print(f"\nFinal message: {event.message}")
```

## Tool Use

### Defining and Using Tools

```python
from anthropic import Anthropic

client = Anthropic()

# Define tools
tools = [
    {
        "name": "get_weather",
        "description": "Get current weather for a location",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City and state, e.g. 'San Francisco, CA'"
                },
                "unit": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"],
                    "description": "Temperature unit"
                }
            },
            "required": ["location"]
        }
    }
]

# Initial request
response = client.messages.create(
    model="claude-sonnet-4-5-20250514",
    max_tokens=1024,
    tools=tools,
    messages=[{"role": "user", "content": "What's the weather in Paris?"}]
)

# Check if tool use requested
if response.stop_reason == "tool_use":
    tool_use = next(block for block in response.content if block.type == "tool_use")

    # Execute tool (your implementation)
    tool_result = execute_weather_lookup(tool_use.input)

    # Continue conversation with tool result
    final_response = client.messages.create(
        model="claude-sonnet-4-5-20250514",
        max_tokens=1024,
        tools=tools,
        messages=[
            {"role": "user", "content": "What's the weather in Paris?"},
            {"role": "assistant", "content": response.content},
            {
                "role": "user",
                "content": [
                    {
                        "type": "tool_result",
                        "tool_use_id": tool_use.id,
                        "content": tool_result
                    }
                ]
            }
        ]
    )
```

### Tool Choice Options

```python
# Let Claude decide (default)
tool_choice={"type": "auto"}

# Force tool use
tool_choice={"type": "any"}

# Force specific tool
tool_choice={"type": "tool", "name": "get_weather"}

# Disable tools for this request
tool_choice={"type": "none"}
```

## Error Handling

```python
import anthropic
from anthropic import Anthropic

client = Anthropic()

try:
    response = client.messages.create(
        model="claude-sonnet-4-5-20250514",
        max_tokens=1024,
        messages=[{"role": "user", "content": "Hello"}]
    )
except anthropic.APIConnectionError as e:
    # Network issues
    print(f"Connection failed: {e.__cause__}")
except anthropic.RateLimitError as e:
    # 429 - implement exponential backoff
    print(f"Rate limited. Retry after backoff.")
except anthropic.BadRequestError as e:
    # 400 - check your request
    print(f"Bad request: {e.message}")
except anthropic.AuthenticationError as e:
    # 401 - check API key
    print(f"Auth failed: {e.message}")
except anthropic.APIStatusError as e:
    # Other API errors
    print(f"API error {e.status_code}: {e.message}")
```

### Retry Configuration

```python
from anthropic import Anthropic

# Configure retries (default is 2)
client = Anthropic(
    max_retries=3,
    timeout=60.0  # seconds (default is 10 minutes)
)

# Override per-request
response = client.with_options(
    max_retries=5,
    timeout=120.0
).messages.create(...)
```

## Anti-Patterns and Common Mistakes

### 1. Breaking Prompt Cache

```python
# BAD - Dynamic content in cached section breaks cache
system_prompt = f"You are an assistant. User: {user_name}"  # Changes per user!

# GOOD - Keep cached content stable, put dynamic content in messages
system_prompt = "You are an assistant."
messages = [
    {"role": "user", "content": f"My name is {user_name}. Help me with..."}
]
```

### 2. Not Validating Tool Inputs

```python
# BAD - Trusting tool inputs directly
def execute_tool(tool_name: str, args: dict):
    return tools[tool_name](**args)  # Dangerous!

# GOOD - Validate tool name and arguments
from pydantic import BaseModel, ValidationError

class WeatherInput(BaseModel):
    location: str
    unit: str = "celsius"

ALLOWED_TOOLS = {"get_weather": WeatherInput}

def execute_tool(tool_name: str, args: dict):
    if tool_name not in ALLOWED_TOOLS:
        raise ValueError(f"Unknown tool: {tool_name}")

    schema = ALLOWED_TOOLS[tool_name]
    validated = schema.model_validate(args)
    return tools[tool_name](**validated.model_dump())
```

### 3. Over-Reserving max_tokens

```python
# BAD - Always using maximum
response = client.messages.create(
    max_tokens=4096,  # Reserves capacity you won't use
    messages=[{"role": "user", "content": "Yes or no?"}]
)

# GOOD - Set appropriate limits
response = client.messages.create(
    max_tokens=50,  # Reasonable for short answer
    messages=[{"role": "user", "content": "Yes or no?"}]
)
```

### 4. Ignoring stop_reason

```python
# BAD - Assuming response is complete
text = response.content[0].text

# GOOD - Check stop reason
if response.stop_reason == "end_turn":
    # Normal completion
    text = response.content[0].text
elif response.stop_reason == "max_tokens":
    # Truncated - may need to continue
    print("Response was truncated")
elif response.stop_reason == "tool_use":
    # Claude wants to use a tool
    handle_tool_use(response)
```

### 5. Not Using Streaming for Long Responses

```python
# BAD - Waiting for full response (poor UX, timeout risk)
response = client.messages.create(
    max_tokens=4096,
    messages=[{"role": "user", "content": "Write a detailed analysis..."}]
)

# GOOD - Stream for better UX and reliability
with client.messages.stream(
    max_tokens=4096,
    messages=[{"role": "user", "content": "Write a detailed analysis..."}]
) as stream:
    for text in stream.text_stream:
        yield text  # Send to user immediately
```

### 6. Hardcoding API Keys

```python
# BAD - Never do this
client = Anthropic(api_key="sk-ant-...")

# GOOD - Use environment variables
import os
client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

# BETTER - Let SDK use default (ANTHROPIC_API_KEY env var)
client = Anthropic()
```

## Cloud Platform Integrations

### AWS Bedrock

```bash
pip install anthropic[bedrock]
```

```python
from anthropic import AnthropicBedrock

client = AnthropicBedrock(
    aws_region="us-east-1"
    # Uses default AWS credentials
)

message = client.messages.create(
    model="anthropic.claude-sonnet-4-5-20250514-v1:0",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello"}]
)
```

### Google Vertex AI

```bash
pip install anthropic[vertex]
```

```python
from anthropic import AnthropicVertex

client = AnthropicVertex(
    project_id="your-project-id",
    region="us-east5"
)

message = client.messages.create(
    model="claude-sonnet-4-5@20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello"}]
)
```

## Production Checklist

### Before Deployment

- [ ] API key stored securely (env vars, secrets manager)
- [ ] Appropriate model selected for use case
- [ ] max_tokens set to reasonable values
- [ ] Error handling with retries implemented
- [ ] Rate limit handling with exponential backoff
- [ ] Streaming enabled for user-facing responses
- [ ] Prompt caching configured for repeated content
- [ ] Batch API used for background processing
- [ ] Token counting for cost estimation
- [ ] Logging for debugging (but never log prompts with PII)

### Monitoring

```python
# Log usage for cost tracking
response = client.messages.create(...)

log_usage({
    "request_id": response._request_id,
    "model": response.model,
    "input_tokens": response.usage.input_tokens,
    "output_tokens": response.usage.output_tokens,
    "cache_read": getattr(response.usage, 'cache_read_input_tokens', 0),
    "cache_write": getattr(response.usage, 'cache_creation_input_tokens', 0),
    "stop_reason": response.stop_reason
})
```

## Staying Updated

For the latest API documentation, model releases, and pricing:

1. **Official Documentation**: https://docs.anthropic.com
2. **API Reference**: https://docs.anthropic.com/en/api
3. **Model Releases**: https://docs.anthropic.com/en/docs/about-claude/models
4. **Pricing**: https://docs.anthropic.com/en/docs/about-claude/pricing
5. **SDK Changelog**: https://github.com/anthropics/anthropic-sdk-python/releases

When working on a project using Claude APIs, always verify current model IDs and pricing against the official documentation, as these may change with new releases.
