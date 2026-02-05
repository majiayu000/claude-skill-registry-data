---
name: streaming
description: Use when building real-time chat interfaces, displaying incremental LLM responses, or streaming output from OpenAI, Anthropic, Google, or Ollama - async iteration with usage tracking works across all providers
---

# Streaming Responses

## Installation

```bash
# With uv (recommended)
uv add llmring

# With pip
pip install llmring
```

**Provider SDKs (install what you need):**
```bash
uv add openai>=1.0      # OpenAI
uv add anthropic>=0.67   # Anthropic
uv add google-genai      # Google Gemini
uv add ollama>=0.4       # Ollama
```

## API Overview

This skill covers:
- `LLMRing.chat_stream()` - Stream response chunks
- `StreamChunk` - Individual chunk structure
- Usage tracking in streaming responses
- Async iteration patterns

## Quick Start

**First, create your lockfile** (see llmring:lockfile skill):
```bash
llmring lock init
llmring bind chatbot anthropic:claude-3-5-haiku-20241022
```

**Then use streaming:**
```python
from llmring import LLMRing, LLMRequest, Message
from llmring.schemas import StreamChunk  # Optional: for type hints

async with LLMRing() as service:
    request = LLMRequest(
        model="chatbot",  # YOUR alias from llmring.lock
        messages=[Message(role="user", content="Count to 10")]
    )

    # Stream response
    async for chunk in service.chat_stream(request):
        print(chunk.delta, end="", flush=True)
    print()  # Newline after streaming
```

## Complete API Documentation

### LLMRing.chat_stream()

Stream a chat completion response as chunks.

**Signature:**
```python
async def chat_stream(
    request: LLMRequest,
    profile: Optional[str] = None
) -> AsyncIterator[StreamChunk]
```

**Parameters:**
- `request` (LLMRequest): Request configuration with messages and parameters
- `profile` (str, optional): Profile name for environment-specific configuration

**Returns:**
- `AsyncIterator[StreamChunk]`: Async iterator yielding response chunks

**Raises:**
- `ProviderNotFoundError`: If provider is not configured
- `ModelNotFoundError`: If model is not available
- `ProviderAuthenticationError`: If API key is invalid
- `ProviderRateLimitError`: If rate limit exceeded

**Example:**
```python
from llmring import LLMRing, LLMRequest, Message

async with LLMRing() as service:
    request = LLMRequest(
        model="chatbot",  # Your streaming alias
        messages=[Message(role="user", content="Write a haiku")]
    )

    async for chunk in service.chat_stream(request):
        print(chunk.delta, end="", flush=True)
```

### StreamChunk

A chunk of a streaming response.

**Attributes:**
- `delta` (str): Text content in this chunk
- `model` (str): Model identifier (present in all chunks)
- `finish_reason` (str, optional): Why generation stopped (only in final chunk)
- `usage` (dict, optional): Token usage statistics (only in final chunk)
- `tool_calls` (list, optional): Tool calls being constructed (incremental)

**Example:**
```python
async for chunk in service.chat_stream(request):
    print(f"Delta: '{chunk.delta}'")
    if chunk.model:
        print(f"Model: {chunk.model}")
    if chunk.finish_reason:
        print(f"Finished: {chunk.finish_reason}")
    if chunk.usage:
        print(f"Tokens: {chunk.usage}")
```

## Common Patterns

### Basic Streaming with Flush

```python
from llmring import LLMRing, LLMRequest, Message

async with LLMRing() as service:
    request = LLMRequest(
        model="chatbot",  # Your streaming alias
        messages=[Message(role="user", content="Tell me a joke")]
    )

    # Print each chunk immediately
    async for chunk in service.chat_stream(request):
        print(chunk.delta, end="", flush=True)
    print()  # Newline when done
```

### Capturing Usage Statistics

The final chunk contains usage statistics. Capture them:

```python
from llmring import LLMRing, LLMRequest, Message

async with LLMRing() as service:
    request = LLMRequest(
        model="chatbot",  # Your streaming alias
        messages=[Message(role="user", content="Explain quantum computing")]
    )

    accumulated_usage = None
    full_response = ""

    async for chunk in service.chat_stream(request):
        print(chunk.delta, end="", flush=True)
        full_response += chunk.delta

        # Capture usage from final chunk
        if chunk.usage:
            accumulated_usage = chunk.usage

    print()  # Newline

    if accumulated_usage:
        print(f"\nTokens used: {accumulated_usage.get('total_tokens', 0)}")
        print(f"Prompt tokens: {accumulated_usage.get('prompt_tokens', 0)}")
        print(f"Completion tokens: {accumulated_usage.get('completion_tokens', 0)}")
```

### Building Full Response

```python
from llmring import LLMRing, LLMRequest, Message

async with LLMRing() as service:
    request = LLMRequest(
        model="chatbot",  # Your streaming alias
        messages=[Message(role="user", content="Write a story")]
    )

    chunks = []
    async for chunk in service.chat_stream(request):
        print(chunk.delta, end="", flush=True)
        chunks.append(chunk.delta)

    # Reconstruct complete response
    full_response = "".join(chunks)
    print(f"\n\nFull response length: {len(full_response)} characters")
```

### Streaming with Custom Display

```python
from llmring import LLMRing, LLMRequest, Message
import sys

async with LLMRing() as service:
    request = LLMRequest(
        model="chatbot",  # Your streaming alias
        messages=[Message(role="user", content="Describe the ocean")]
    )

    word_count = 0
    async for chunk in service.chat_stream(request):
        # Custom processing per chunk
        sys.stdout.write(chunk.delta)
        sys.stdout.flush()

        # Count words in real-time
        word_count += len(chunk.delta.split())

    print(f"\n\nTotal words: {word_count}")
```

### Streaming with Temperature

```python
from llmring import LLMRing, LLMRequest, Message

async with LLMRing() as service:
    # Higher temperature for creative streaming
    request = LLMRequest(
        model="chatbot",  # Your streaming alias
        messages=[Message(role="user", content="Write a creative story")],
        temperature=1.2
    )

    async for chunk in service.chat_stream(request):
        print(chunk.delta, end="", flush=True)
```

### Multi-Turn Streaming Conversation

```python
from llmring import LLMRing, LLMRequest, Message

async with LLMRing() as service:
    messages = [
        Message(role="system", content="You are a helpful assistant."),
        Message(role="user", content="What is Python?")
    ]

    # First streaming response
    request = LLMRequest(model="chatbot",  # Your streaming alias messages=messages)
    response_text = ""

    print("Assistant: ", end="")
    async for chunk in service.chat_stream(request):
        print(chunk.delta, end="", flush=True)
        response_text += chunk.delta
    print()

    # Add to history
    messages.append(Message(role="assistant", content=response_text))

    # Second turn
    messages.append(Message(role="user", content="Give me an example"))
    request = LLMRequest(model="chatbot",  # Your streaming alias messages=messages)
    response_text = ""

    print("Assistant: ", end="")
    async for chunk in service.chat_stream(request):
        print(chunk.delta, end="", flush=True)
        response_text += chunk.delta
    print()
```

### Streaming with Max Tokens

```python
from llmring import LLMRing, LLMRequest, Message

async with LLMRing() as service:
    # Limit streaming response length
    request = LLMRequest(
        model="chatbot",  # Your streaming alias
        messages=[Message(role="user", content="Write a long essay")],
        max_tokens=50  # Stop after 50 tokens
    )

    async for chunk in service.chat_stream(request):
        print(chunk.delta, end="", flush=True)

    # Check finish_reason in final chunk
    if chunk.finish_reason == "length":
        print("\n[Response truncated due to max_tokens]")
```

## Detecting Stream Completion

```python
from llmring import LLMRing, LLMRequest, Message

async with LLMRing() as service:
    request = LLMRequest(
        model="chatbot",  # Your streaming alias
        messages=[Message(role="user", content="Hello")]
    )

    async for chunk in service.chat_stream(request):
        print(chunk.delta, end="", flush=True)

        # Final chunk has finish_reason
        if chunk.finish_reason:
            print(f"\nStream ended: {chunk.finish_reason}")
            # finish_reason values:
            # - "stop": Natural completion
            # - "length": Hit max_tokens limit
            # - "tool_calls": Model wants to call tools
```

## Error Handling

```python
from llmring import LLMRing, LLMRequest, Message
from llmring.exceptions import (
    ProviderAuthenticationError,
    ModelNotFoundError,
    ProviderRateLimitError,
    ProviderTimeoutError
)

async with LLMRing() as service:
    try:
        request = LLMRequest(
            model="chatbot",  # Your streaming alias
            messages=[Message(role="user", content="Hello")]
        )

        async for chunk in service.chat_stream(request):
            print(chunk.delta, end="", flush=True)

    except ProviderAuthenticationError:
        print("\nInvalid API key")

    except ModelNotFoundError as e:
        print(f"\nModel not available: {e}")

    except ProviderRateLimitError as e:
        print(f"\nRate limited - retry after {e.retry_after}s")

    except ProviderTimeoutError:
        print("\nRequest timed out")

    except Exception as e:
        print(f"\nStream error: {e}")
```

## Performance Considerations

### Buffer for UI Updates

If updating UI, buffer chunks to avoid excessive redraws:

```python
from llmring import LLMRing, LLMRequest, Message
import asyncio

async with LLMRing() as service:
    request = LLMRequest(
        model="chatbot",  # Your streaming alias
        messages=[Message(role="user", content="Write a paragraph")]
    )

    buffer = ""
    last_update = asyncio.get_event_loop().time()
    UPDATE_INTERVAL = 0.05  # Update UI every 50ms

    async for chunk in service.chat_stream(request):
        buffer += chunk.delta

        # Update UI at intervals, not every chunk
        now = asyncio.get_event_loop().time()
        if now - last_update >= UPDATE_INTERVAL or chunk.finish_reason:
            print(buffer, end="", flush=True)
            buffer = ""
            last_update = now
```

## Common Mistakes

### Wrong: Not Flushing Output

```python
# DON'T DO THIS - output buffered, appears all at once
async for chunk in service.chat_stream(request):
    print(chunk.delta, end="")  # No flush!
```

**Right: Always Flush**

```python
# DO THIS - see output in real-time
async for chunk in service.chat_stream(request):
    print(chunk.delta, end="", flush=True)
```

### Wrong: Checking Usage on Every Chunk

```python
# DON'T DO THIS - usage only in final chunk
async for chunk in service.chat_stream(request):
    if chunk.usage:  # Only true once!
        tokens = chunk.usage["total_tokens"]
```

**Right: Accumulate Then Check**

```python
# DO THIS - capture usage from final chunk
accumulated_usage = None
async for chunk in service.chat_stream(request):
    print(chunk.delta, end="", flush=True)
    if chunk.usage:
        accumulated_usage = chunk.usage

# Use usage after streaming completes
if accumulated_usage:
    print(f"\nTokens: {accumulated_usage['total_tokens']}")
```

### Wrong: Forgetting to Build Full Response

```python
# DON'T DO THIS - loses full response for history
async for chunk in service.chat_stream(request):
    print(chunk.delta, end="", flush=True)
# Can't add to conversation history!
```

**Right: Accumulate for History**

```python
# DO THIS - keep full response for multi-turn
response_text = ""
async for chunk in service.chat_stream(request):
    print(chunk.delta, end="", flush=True)
    response_text += chunk.delta

# Now can add to history
messages.append(Message(role="assistant", content=response_text))
```

## Provider Differences

All providers support streaming with the same API:

| Provider | Streaming | Usage Stats | Notes |
|----------|-----------|-------------|-------|
| **OpenAI** | Yes | Final chunk | Fast, reliable |
| **Anthropic** | Yes | Final chunk | Large context support |
| **Google** | Yes | Final chunk | 2M+ token context |
| **Ollama** | Yes | Final chunk | Local models |

**No code changes needed** to switch between providers - same streaming API works for all.

## Related Skills

- `llmring-chat` - Basic non-streaming chat
- `llmring-tools` - Streaming with tool calls
- `llmring-structured` - Streaming structured output
- `llmring-lockfile` - Configure model aliases
- `llmring-providers` - Provider-specific optimizations

## When to Use Streaming

**Use streaming when:**
- Building chat interfaces (show text as it generates)
- Long responses (user sees progress)
- Real-time interaction is important
- Processing chunks before completion

**Use regular chat when:**
- Need complete response before processing
- Integrating with batch systems
- Simple CLI scripts
- Testing and debugging
