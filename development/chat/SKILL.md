---
name: chat
description: Use when starting a new project with llmring, building an application using LLMs, making basic chat completions, or sending messages to OpenAI, Anthropic, Google, or Ollama - covers lockfile creation (MANDATORY first step), semantic alias usage, unified interface for all providers with consistent message structure and response handling
---

# Basic Chat Completions

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
- `LLMRing` - Main service class
- `LLMRequest` - Request configuration
- `LLMResponse` - Response structure
- `Message` - Message format
- Resource management with context managers

## Quick Start

**FIRST: Create your lockfile** (required for all real applications):

```bash
# Initialize lockfile
llmring lock init

# Check available models (get current names from registry):
llmring list --provider openai
llmring list --provider anthropic

# Bind aliases using CURRENT model names:
llmring bind summarizer anthropic:claude-3-5-haiku-20241022

# Or use interactive configuration (recommended - knows current models):
llmring lock chat
```

**⚠️ Important:** Check `llmring list` for current model names. Models change (e.g., gemini-2.5-pro → gemini-2.5-pro).

**THEN: Use in code:**

```python
from llmring import LLMRing, LLMRequest, Message

# Use context manager for automatic resource cleanup
async with LLMRing() as service:
    request = LLMRequest(
        model="summarizer",  # YOUR semantic alias (defined in llmring.lock)
        messages=[
            Message(role="system", content="You are a helpful assistant."),
            Message(role="user", content="Hello!")
        ]
    )

    response = await service.chat(request)
    print(response.content)
```

**⚠️ Important:** The bundled lockfile that ships with llmring is ONLY for running `llmring lock chat`. Real applications must create their own lockfile.

### Timeout Control

The library enforces a 60-second timeout by default. Override it when processing large documents, running expensive reasoning chains, or forwarding calls to slower local models.

```python
async with LLMRing(timeout=300.0) as service:  # default for this context manager
    request = LLMRequest(
        model="summarizer",
        messages=[Message(role="user", content=huge_thread)],
        timeout=None,                            # disable timeout for this request
    )
    response = await service.chat(request)
```

You can also set `LLMRING_PROVIDER_TIMEOUT_S=120` in the environment to establish a default when you don't pass the constructor argument.

## Complete API Documentation

### LLMRing

Main service class that manages providers and routes requests.

**Constructor:**
```python
LLMRing(
    origin: str = "llmring",
    registry_url: Optional[str] = None,
    lockfile_path: Optional[str] = None,
    server_url: Optional[str] = None,
    api_key: Optional[str] = None,
    log_metadata: bool = True,
    log_conversations: bool = False,
    alias_cache_size: int = 100,
    alias_cache_ttl: int = 3600,
    timeout: Optional[float] = 60.0
)
```

**Parameters:**
- `origin` (str, default: "llmring"): Origin identifier for tracking
- `registry_url` (str, optional): Custom registry URL for model information
- `lockfile_path` (str, optional): Path to lockfile for alias configuration
- `server_url` (str, optional): llmring-server URL for usage logging
- `api_key` (str, optional): API key for llmring-server
- `log_metadata` (bool, default: True): Enable logging of usage metadata (requires server_url)
- `log_conversations` (bool, default: False): Enable logging of full conversations (requires server_url)
- `alias_cache_size` (int, default: 100): Maximum cached alias resolutions
- `alias_cache_ttl` (int, default: 3600): Cache TTL in seconds
- `timeout` (float | None, default: 60.0): Default request timeout in seconds (`None` disables)

**Example:**
```python
from llmring import LLMRing

# Basic initialization (uses environment variables for API keys)
async with LLMRing() as service:
    response = await service.chat(request)

# With custom lockfile
async with LLMRing(lockfile_path="./my-llmring.lock") as service:
    response = await service.chat(request)
```

### LLMRing.chat()

Send a chat completion request and get a response.

**Signature:**
```python
async def chat(
    request: LLMRequest,
    profile: Optional[str] = None
) -> LLMResponse
```

**Parameters:**
- `request` (LLMRequest): Request configuration with messages and parameters
- `profile` (str, optional): Profile name for environment-specific configuration (e.g., "dev", "prod")

**Returns:**
- `LLMResponse`: Response with content, usage, and metadata

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
        model="responder",  # Your alias for responses
        messages=[
            Message(role="user", content="What is 2+2?")
        ],
        temperature=0.7,
        max_tokens=100
    )

    response = await service.chat(request)
    print(f"Response: {response.content}")
    print(f"Tokens: {response.total_tokens}")
    print(f"Model: {response.model}")
```

### LLMRequest

Configuration for a chat completion request.

**Constructor:**
```python
LLMRequest(
    messages: List[Message],
    model: Optional[str] = None,
    temperature: Optional[float] = None,
    max_tokens: Optional[int] = None,
    reasoning_tokens: Optional[int] = None,
    response_format: Optional[Dict[str, Any]] = None,
    tools: Optional[List[Dict[str, Any]]] = None,
    tool_choice: Optional[Union[str, Dict[str, Any]]] = None,
    cache: Optional[Dict[str, Any]] = None,
    metadata: Optional[Dict[str, Any]] = None,
    json_response: Optional[bool] = None,
    timeout: Optional[float] = None,
    extra_params: Dict[str, Any] = {}
)
```

**Parameters:**
- `messages` (List[Message], required): Conversation messages
- `model` (str, optional): Model alias (e.g., "fast") or provider:model reference (e.g., "openai:gpt-4o")
- `temperature` (float, optional): Sampling temperature (0.0-2.0). Higher = more random
- `max_tokens` (int, optional): Maximum tokens to generate
- `reasoning_tokens` (int, optional): Token budget for reasoning models (o1, etc.)
- `response_format` (dict, optional): Structured output format (see llmring-structured skill)
- `tools` (list, optional): Available functions (see llmring-tools skill)
- `tool_choice` (str/dict, optional): Tool selection strategy
- `cache` (dict, optional): Caching configuration
- `metadata` (dict, optional): Request metadata
- `json_response` (bool, optional): Request JSON format response
- `timeout` (float | None, optional): Override service-level timeout; `None` waits indefinitely
- `extra_params` (dict, default: {}): Provider-specific parameters

**Example:**
```python
from llmring import LLMRequest, Message

# Simple request
request = LLMRequest(
    model="summarizer",  # Your domain-specific alias
    messages=[Message(role="user", content="Hello")]
)

# With parameters
request = LLMRequest(
    model="explainer",  # Another semantic alias you define
    messages=[
        Message(role="system", content="You are a helpful assistant."),
        Message(role="user", content="Explain quantum computing")
    ],
    temperature=0.3,
    max_tokens=500
)
```

### Message

A message in a conversation.

**Constructor:**
```python
Message(
    role: Literal["system", "user", "assistant", "tool"],
    content: Any,
    tool_calls: Optional[List[Dict[str, Any]]] = None,
    tool_call_id: Optional[str] = None,
    timestamp: Optional[datetime] = None,
    metadata: Optional[Dict[str, Any]] = None
)
```

**Parameters:**
- `role` (str, required): Message role - "system", "user", "assistant", or "tool"
- `content` (Any, required): Message content (string or structured content for multimodal)
- `tool_calls` (list, optional): Tool calls made by assistant
- `tool_call_id` (str, optional): ID for tool result messages
- `timestamp` (datetime, optional): Message timestamp
- `metadata` (dict, optional): Provider-specific metadata (e.g., cache_control for Anthropic)

**Example:**
```python
from llmring import Message

# System message
system_msg = Message(
    role="system",
    content="You are a helpful assistant."
)

# User message
user_msg = Message(
    role="user",
    content="What is the capital of France?"
)

# Assistant response
assistant_msg = Message(
    role="assistant",
    content="The capital of France is Paris."
)

# Anthropic prompt caching
cached_msg = Message(
    role="system",
    content="Very long system prompt...",
    metadata={"cache_control": {"type": "ephemeral"}}
)
```

### LLMResponse

Response from a chat completion.

**Attributes:**
- `content` (str): Generated text content
- `model` (str): Model that generated the response
- `usage` (dict, optional): Token usage statistics
- `finish_reason` (str, optional): Why generation stopped ("stop", "length", "tool_calls")
- `tool_calls` (list, optional): Tool calls made by model
- `parsed` (dict, optional): Parsed JSON when response_format used

**Properties:**
- `total_tokens` (int, optional): Total tokens used (prompt + completion)

**Example:**
```python
response = await service.chat(request)

print(response.content)           # "The capital is Paris."
print(response.model)              # "anthropic:claude-sonnet-4-5-20250929"
print(response.total_tokens)       # 45
print(response.finish_reason)      # "stop"
print(response.usage)              # {"prompt_tokens": 20, "completion_tokens": 25}
```

## Environment Setup

**Required environment variables (set API keys for providers you want to use):**

```bash
# Add to .env file or export
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_GEMINI_API_KEY=AIza...
OLLAMA_BASE_URL=http://localhost:11434  # Optional, default shown
```

**LLMRing automatically initializes providers based on available API keys.**

## Resource Management

### Context Manager (Recommended)

Always use context manager for automatic cleanup:

```python
from llmring import LLMRing, LLMRequest, Message

# Context manager handles cleanup automatically
async with LLMRing() as service:
    request = LLMRequest(
        model="chatbot",  # Your alias for conversational AI
        messages=[Message(role="user", content="Hello")]
    )
    response = await service.chat(request)
    # Resources cleaned up when exiting context
```

### Manual Cleanup

If you can't use context manager:

```python
service = LLMRing()
try:
    response = await service.chat(request)
finally:
    await service.close()  # MUST call close()
```

## Common Patterns

### Multi-Turn Conversation

```python
from llmring import LLMRing, LLMRequest, Message

async with LLMRing() as service:
    messages = [
        Message(role="system", content="You are a helpful assistant."),
        Message(role="user", content="What is Python?")
    ]

    # First turn
    request = LLMRequest(model="assistant", messages=messages)
    response = await service.chat(request)

    # Add assistant response to history
    messages.append(Message(role="assistant", content=response.content))

    # Second turn
    messages.append(Message(role="user", content="What about JavaScript?"))
    request = LLMRequest(model="assistant", messages=messages)
    response = await service.chat(request)

    print(response.content)
```

### Using Model Aliases

```python
# Semantic aliases YOU define in your lockfile
request = LLMRequest(
    model="summarizer",  # Alias you configured for this task
    messages=[Message(role="user", content="Hello")]
)

# Use task-based names:
# model="code-reviewer"  - For code review tasks
# model="sql-generator"  - For generating SQL
# model="extractor"      - For extracting structured data
# model="analyzer"       - For analysis tasks
```

### Using Direct Model References

```python
# Direct provider:model format (escape hatch)
request = LLMRequest(
    model="anthropic:claude-sonnet-4-5-20250929",
    messages=[Message(role="user", content="Hello")]
)

# Or specific versions
request = LLMRequest(
    model="openai:gpt-4o",
    messages=[Message(role="user", content="Hello")]
)
```

### Temperature Control

```python
# Creative writing (higher temperature)
request = LLMRequest(
    model="creative-writer",  # Your alias for creative tasks
    messages=[Message(role="user", content="Write a poem")],
    temperature=1.2  # More random/creative
)

# Factual responses (lower temperature)
request = LLMRequest(
    model="factual-responder",  # Your alias for factual tasks
    messages=[Message(role="user", content="What is 2+2?")],
    temperature=0.2  # More deterministic
)
```

### Token Limits

```python
# Limit response length
request = LLMRequest(
    model="summarizer",  # Your summarization alias
    messages=[Message(role="user", content="Summarize this...")],
    max_tokens=100  # Cap at 100 tokens
)
```

## Error Handling

```python
from llmring import (
    LLMRing,
    LLMRequest,
    Message,
    ProviderAuthenticationError,
    ModelNotFoundError,
    ProviderRateLimitError,
    ProviderTimeoutError,
    ProviderNotFoundError
)

async with LLMRing() as service:
    try:
        request = LLMRequest(
            model="chatbot",  # Your conversational alias
            messages=[Message(role="user", content="Hello")]
        )
        response = await service.chat(request)

    except ProviderAuthenticationError:
        print("Invalid API key - check environment variables")

    except ModelNotFoundError as e:
        print(f"Model not available: {e}")

    except ProviderRateLimitError as e:
        print(f"Rate limited - retry after {e.retry_after}s")

    except ProviderTimeoutError:
        print("Request timed out")

    except ProviderNotFoundError:
        print("Provider not configured - check API keys")
```

## Common Mistakes

### Wrong: Forgetting Context Manager

```python
# DON'T DO THIS - resources not cleaned up
service = LLMRing()
response = await service.chat(request)
# Forgot to call close()!
```

**Right: Use Context Manager**

```python
# DO THIS - automatic cleanup
async with LLMRing() as service:
    response = await service.chat(request)
```

### Wrong: Invalid Message Role

```python
# DON'T DO THIS - invalid role
message = Message(role="admin", content="Hello")
```

**Right: Use Valid Roles**

```python
# DO THIS - valid roles only
message = Message(role="user", content="Hello")
# Valid: "system", "user", "assistant", "tool"
```

### Wrong: Missing Model

```python
# DON'T DO THIS - no model specified and no lockfile
request = LLMRequest(
    messages=[Message(role="user", content="Hello")]
)
```

**Right: Use Semantic Alias from Lockfile**

```python
# DO THIS - use your semantic alias
request = LLMRequest(
    model="chatbot",  # or "anthropic:claude-sonnet-4-5-20250929" for direct reference
    messages=[Message(role="user", content="Hello")]
)
```

## Profiles: Environment-Specific Configuration

Use different models for different environments:

```python
# Set profile via environment variable
# export LLMRING_PROFILE=dev

# Or in code
async with LLMRing() as service:
    # Uses 'dev' profile bindings (cheaper models)
    response = await service.chat(request, profile="dev")

    # Uses 'prod' profile bindings (higher quality)
    response = await service.chat(request, profile="prod")
```

See **llmring-lockfile** skill for full profile documentation.

## Related Skills

- `llmring-streaming` - Stream responses for real-time output
- `llmring-tools` - Function calling and tool use
- `llmring-structured` - JSON schema for structured output
- `llmring-lockfile` - Configure aliases and profiles
- `llmring-providers` - Multi-provider patterns and raw SDK access

## Provider Support

| Provider | Initialization | Example |
|----------|---------------|---------|
| **OpenAI** | Set `OPENAI_API_KEY` | `model="openai:gpt-4o"` |
| **Anthropic** | Set `ANTHROPIC_API_KEY` | `model="anthropic:claude-sonnet-4-5-20250929"` |
| **Google** | Set `GOOGLE_GEMINI_API_KEY` | `model="google:gemini-2.5-pro"` |
| **Ollama** | Runs automatically | `model="ollama:llama3"` |

All providers work with the same unified API - no code changes needed to switch providers.
