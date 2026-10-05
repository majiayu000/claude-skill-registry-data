---
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebFetch, WebSearch
description: 'Build production-grade applications with OpenAI APIs (direct or via
  Azure OpenAI).

  Covers structured outputs, function calling, streaming, Assistants API, Responses
  API,

  Agents SDK, cost optimization, rate limiting, error handling, and batch processing.


  IMPORTANT: Before implementing, gather context about the target environment including:

  - API provider (OpenAI direct vs Azure OpenAI)

  - Primary use cases (chat, function calling, structured outputs, assistants, agents)

  - Cost constraints and optimization requirements

  - Error handling and retry strategy needs'
name: openai-api
---

# OpenAI API Development

Build production-grade applications with OpenAI APIs. This guide covers both direct OpenAI API and Azure OpenAI, including structured outputs, function calling, streaming, Assistants API, Agents SDK, cost optimization, and error handling.

## Before You Start: Gather Context

**CRITICAL**: Before implementing OpenAI API integrations, gather the following information from the user if not already known. Do not assume defaults—ask explicitly.

### Required Context Questions

1. **API Provider**: Which OpenAI API provider are you using?
   - Direct OpenAI API (`api.openai.com`)
   - Azure OpenAI Service (Azure AI Foundry)
   - Both (multi-provider setup)

2. **Primary Use Case**: What's the main functionality needed?
   - Chat completions / conversational AI
   - Structured outputs / data extraction
   - Function calling / tool use
   - Assistants API (threads, runs, file search, code interpreter)
   - Agents SDK (multi-agent workflows)
   - Embeddings / RAG
   - Batch processing
   - Realtime API / voice

3. **Cost Constraints**: What are the cost optimization requirements?
   - Token budget limits
   - Need for caching strategies
   - Batch processing for non-time-sensitive workloads
   - Model tier selection (GPT-4o vs GPT-4o-mini vs GPT-5)

4. **Error Handling Requirements**:
   - Retry strategy (exponential backoff, circuit breaker)
   - Fallback behavior (cached responses, degraded functionality)
   - Rate limit handling approach

5. **Sync vs Async**: What execution model is needed?
   - Synchronous (blocking)
   - Asynchronous (async/await)
   - Streaming (real-time token delivery)

### Example Context Prompt

When context is unclear, ask:

> "Before I implement the OpenAI integration, I need to understand your setup:
> 1. Are you using OpenAI directly or Azure OpenAI?
> 2. What's your primary use case (chat, structured outputs, function calling, assistants)?
> 3. Do you have specific cost constraints or rate limit concerns?
> 4. Do you need streaming responses?"

---

## Provider Configuration

### Direct OpenAI API

```python
import os
from openai import OpenAI, AsyncOpenAI

# Synchronous client
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    # Optional: Configure retries and timeout
    max_retries=3,
    timeout=60.0,
)

# Asynchronous client
async_client = AsyncOpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)
```

### Azure OpenAI Service

```python
import os
from openai import AzureOpenAI, AsyncAzureOpenAI

# Azure OpenAI requires different configuration
client = AzureOpenAI(
    api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
    api_version="2024-10-21",  # Use latest stable version
    azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
    # e.g., "https://your-resource.openai.azure.com"
)

# Async Azure client
async_client = AsyncAzureOpenAI(
    api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
    api_version="2024-10-21",
    azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
)

# Azure uses deployment names instead of model names
response = client.chat.completions.create(
    model="gpt-4o-deployment",  # Your deployment name, not "gpt-4o"
    messages=[{"role": "user", "content": "Hello"}],
)
```

### Azure with Managed Identity (Entra ID)

```python
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import AzureOpenAI

# Use managed identity instead of API key
token_provider = get_bearer_token_provider(
    DefaultAzureCredential(),
    "https://cognitiveservices.azure.com/.default"
)

client = AzureOpenAI(
    azure_ad_token_provider=token_provider,
    api_version="2024-10-21",
    azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
)
```

### Provider Differences Summary

| Feature | OpenAI Direct | Azure OpenAI |
|---------|--------------|--------------|
| **Authentication** | API key | API key or Entra ID |
| **Model reference** | Model name (`gpt-4o`) | Deployment name |
| **Endpoint** | `api.openai.com` | Custom Azure endpoint |
| **API version** | Not required | Required (`api_version`) |
| **Structured Outputs** | Full support | Full support (2024-08-01-preview+) |
| **Responses API** | Supported | Not yet available |
| **Agents SDK** | Supported | Not yet available |
| **Rate limits** | Per-org | Per-deployment (configurable) |
| **Data residency** | OpenAI servers | Your Azure region |
| **Compliance** | SOC 2 | HIPAA, SOC 2, FedRAMP, etc. |

---

## Chat Completions API

### Basic Chat Completion

```python
from openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain quantum computing briefly."},
    ],
    max_tokens=500,
    temperature=0.7,
)

print(response.choices[0].message.content)
```

### Streaming Responses

```python
from openai import OpenAI

client = OpenAI()

# Streaming for real-time output
stream = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Write a haiku about coding."}],
    stream=True,
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
```

### Async Streaming

```python
import asyncio
from openai import AsyncOpenAI

async def stream_response():
    client = AsyncOpenAI()

    stream = await client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": "Explain recursion."}],
        stream=True,
    )

    async for chunk in stream:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)

asyncio.run(stream_response())
```

---

## Structured Outputs

Structured Outputs guarantee the model response matches your JSON schema exactly. This is the **recommended approach** over JSON mode for all data extraction and structured response use cases.

### When to Use Structured Outputs

| Approach | Use Case |
|----------|----------|
| **Structured Outputs (`response_format`)** | Model responds to user in structured format |
| **Function Calling with `strict: true`** | Model calls tools/functions you execute |
| **JSON Mode (legacy)** | Avoid—use Structured Outputs instead |

### Structured Outputs with Pydantic

```python
from typing import List
from pydantic import BaseModel, Field
from openai import OpenAI

class Step(BaseModel):
    explanation: str = Field(description="Explanation of this step")
    output: str = Field(description="Result of this step")

class MathSolution(BaseModel):
    steps: List[Step] = Field(description="Step-by-step solution")
    final_answer: str = Field(description="The final answer")

client = OpenAI()

# Use .parse() for automatic Pydantic parsing
completion = client.chat.completions.parse(
    model="gpt-4o-2024-08-06",  # Must use dated snapshot for strict mode
    messages=[
        {"role": "system", "content": "Solve math problems step by step."},
        {"role": "user", "content": "Solve: 2x + 5 = 13"},
    ],
    response_format=MathSolution,
)

result = completion.choices[0].message.parsed
if result:
    print(f"Answer: {result.final_answer}")
    for step in result.steps:
        print(f"  - {step.explanation}: {step.output}")
else:
    print(f"Refusal: {completion.choices[0].message.refusal}")
```

### Structured Outputs with Manual JSON Schema

```python
from openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o-2024-08-06",
    messages=[
        {"role": "user", "content": "Extract: John Doe, 30 years old, engineer"}
    ],
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "person_info",
            "strict": True,  # Guarantees schema adherence
            "schema": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "age": {"type": "integer"},
                    "occupation": {"type": "string"},
                },
                "required": ["name", "age", "occupation"],
                "additionalProperties": False,
            },
        },
    },
)

import json
data = json.loads(response.choices[0].message.content)
```

### Structured Output Schema Constraints

When using `strict: true`, schemas must follow these rules:

| Constraint | Requirement |
|------------|-------------|
| **additionalProperties** | Must be `false` on all objects |
| **required** | All properties must be listed |
| **Nullable fields** | Use `{"type": ["string", "null"]}` |
| **No unsupported keywords** | Avoid `if`, `then`, `patternProperties` |
| **Max nesting** | 5 levels deep |
| **Max properties** | 100 total across schema |
| **Enums** | Max 500 values |

### Union Types for Multiple Outputs

```python
from pydantic import BaseModel
from openai import OpenAI

class Success(BaseModel):
    data: dict
    confidence: float

class Error(BaseModel):
    error_code: str
    message: str

# Note: OpenAI uses anyOf internally for union types
from typing import Union

class Response(BaseModel):
    result: Union[Success, Error]
```

---

## Function Calling (Tool Use)

Function calling enables the model to invoke functions you define, bridging LLM capabilities with your application logic.

### Basic Function Calling

```python
from openai import OpenAI
import json

client = OpenAI()

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a location",
            "strict": True,  # Enable structured outputs for tools
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City and state, e.g., 'San Francisco, CA'",
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                    },
                },
                "required": ["location", "unit"],
                "additionalProperties": False,
            },
        },
    }
]

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "What's the weather in Tokyo?"}],
    tools=tools,
    tool_choice="auto",  # or "required" to force tool use
)

message = response.choices[0].message

if message.tool_calls:
    for tool_call in message.tool_calls:
        name = tool_call.function.name
        args = json.loads(tool_call.function.arguments)
        print(f"Function: {name}, Args: {args}")

        # Execute your function
        result = get_weather(**args)  # Your implementation

        # Return result to model
        messages = [
            {"role": "user", "content": "What's the weather in Tokyo?"},
            message,  # Assistant's tool call
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result),
            },
        ]

        # Get final response
        final = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            tools=tools,
        )
        print(final.choices[0].message.content)
```

### Function Calling with Pydantic Auto-Parsing

```python
from enum import Enum
from typing import List
from pydantic import BaseModel
from openai import OpenAI, pydantic_function_tool

class Priority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

class CreateTask(BaseModel):
    """Create a new task in the system."""
    title: str
    description: str
    priority: Priority
    tags: List[str]

client = OpenAI()

# Automatically generate tool definition from Pydantic model
completion = client.chat.completions.parse(
    model="gpt-4o-2024-08-06",
    messages=[
        {"role": "user", "content": "Create a high priority task to fix the login bug, tag it with 'backend' and 'urgent'"}
    ],
    tools=[pydantic_function_tool(CreateTask)],
)

tool_call = completion.choices[0].message.tool_calls[0]
# parsed_arguments is already a Pydantic model instance
task: CreateTask = tool_call.function.parsed_arguments
print(f"Title: {task.title}, Priority: {task.priority}")
```

### Parallel Tool Calls

By default, the model may call multiple tools in a single response. Handle this properly:

```python
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "What's the weather in Tokyo and Paris?"}],
    tools=tools,
    parallel_tool_calls=True,  # Default: True
)

message = response.choices[0].message

# IMPORTANT: Process ALL tool calls
tool_results = []
for tool_call in message.tool_calls or []:
    result = execute_tool(tool_call.function.name, tool_call.function.arguments)
    tool_results.append({
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": json.dumps(result),
    })

# Return all results together
messages = [original_message, message] + tool_results
```

**Important**: Structured Outputs (`strict: true`) is NOT compatible with parallel tool calls. Set `parallel_tool_calls=False` when using strict mode.

---

## Responses API (OpenAI Direct Only)

The Responses API is OpenAI's latest API, designed for agentic workflows. It includes built-in tools like web search, file search, and computer use.

```python
from openai import OpenAI

client = OpenAI()

# Basic usage
response = client.responses.create(
    model="gpt-4o",
    instructions="You are a coding assistant.",
    input="How do I reverse a string in Python?",
)
print(response.output_text)

# With built-in tools
response = client.responses.create(
    model="gpt-4o",
    instructions="Search the web to answer questions.",
    input="What are the latest Python 3.13 features?",
    tools=[{"type": "web_search_preview"}],
)
```

### Streaming with Responses API

```python
from openai import OpenAI

client = OpenAI()

stream = client.responses.create(
    model="gpt-4o",
    input="Explain machine learning.",
    stream=True,
)

for event in stream:
    if event.type == "response.output_text.delta":
        print(event.delta, end="", flush=True)
```

---

## Agents SDK (OpenAI Direct Only)

The Agents SDK enables building multi-agent workflows with handoffs, guardrails, and tracing.

### Installation

```bash
pip install openai-agents
# or
uv add openai-agents
```

### Basic Agent

```python
from agents import Agent, Runner

agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant.",
)

result = Runner.run_sync(agent, "Write a haiku about Python.")
print(result.final_output)
```

### Agent with Tools

```python
import asyncio
from agents import Agent, Runner, function_tool

@function_tool
def get_weather(city: str) -> str:
    """Get the weather for a city."""
    return f"Weather in {city}: Sunny, 72°F"

agent = Agent(
    name="Weather Assistant",
    instructions="Help users with weather information.",
    tools=[get_weather],
)

async def main():
    result = await Runner.run(agent, "What's the weather in Tokyo?")
    print(result.final_output)

asyncio.run(main())
```

### Multi-Agent Handoffs

```python
from agents import Agent, Runner

# Specialized agents
billing_agent = Agent(
    name="Billing Agent",
    handoff_description="Handles billing and payment questions",
    instructions="You handle billing inquiries. Be helpful and accurate.",
)

technical_agent = Agent(
    name="Technical Agent",
    handoff_description="Handles technical support questions",
    instructions="You provide technical support. Be thorough.",
)

# Triage agent routes to specialists
triage_agent = Agent(
    name="Triage Agent",
    instructions="Route users to the appropriate specialist based on their question.",
    handoffs=[billing_agent, technical_agent],
)

async def main():
    result = await Runner.run(triage_agent, "I have a question about my invoice.")
    print(f"Handled by: {result.current_agent.name}")
    print(result.final_output)
```

### Input Guardrails

```python
from pydantic import BaseModel
from agents import Agent, Runner, InputGuardrail, GuardrailFunctionOutput
from agents.exceptions import InputGuardrailTripwireTriggered

class ContentCheck(BaseModel):
    is_appropriate: bool
    reason: str

guardrail_agent = Agent(
    name="Content Checker",
    instructions="Check if user input is appropriate.",
    output_type=ContentCheck,
)

async def content_guardrail(ctx, agent, input_data):
    result = await Runner.run(guardrail_agent, input_data, context=ctx.context)
    output = result.final_output_as(ContentCheck)
    return GuardrailFunctionOutput(
        output_info=output,
        tripwire_triggered=not output.is_appropriate,
    )

main_agent = Agent(
    name="Assistant",
    instructions="Help users with their questions.",
    input_guardrails=[InputGuardrail(guardrail_function=content_guardrail)],
)

async def main():
    try:
        result = await Runner.run(main_agent, "How do I cook pasta?")
        print(result.final_output)
    except InputGuardrailTripwireTriggered:
        print("Input was blocked by guardrail.")
```

### Tracking Usage

```python
result = await Runner.run(agent, "Hello!")
usage = result.context_wrapper.usage

print(f"Requests: {usage.requests}")
print(f"Input tokens: {usage.input_tokens}")
print(f"Output tokens: {usage.output_tokens}")
print(f"Total tokens: {usage.total_tokens}")
```

---

## Assistants API

The Assistants API provides persistent threads, file handling, and built-in tools like Code Interpreter and File Search.

### Creating an Assistant

```python
from openai import OpenAI

client = OpenAI()

assistant = client.beta.assistants.create(
    name="Data Analyst",
    instructions="You analyze data and create visualizations.",
    model="gpt-4o",
    tools=[
        {"type": "code_interpreter"},
        {"type": "file_search"},
    ],
)
```

### Running a Conversation

```python
# Create a thread
thread = client.beta.threads.create()

# Add a message
client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="Analyze this data and create a chart.",
)

# Run the assistant
run = client.beta.threads.runs.create_and_poll(
    thread_id=thread.id,
    assistant_id=assistant.id,
)

if run.status == "completed":
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    for msg in messages.data:
        if msg.role == "assistant":
            print(msg.content[0].text.value)
```

### Streaming Assistant Responses

```python
from openai import OpenAI, AssistantEventHandler
from typing_extensions import override

class EventHandler(AssistantEventHandler):
    @override
    def on_text_delta(self, delta, snapshot):
        print(delta.value, end="", flush=True)

    @override
    def on_tool_call_created(self, tool_call):
        print(f"\nUsing tool: {tool_call.type}")

client = OpenAI()

with client.beta.threads.runs.stream(
    thread_id=thread.id,
    assistant_id=assistant.id,
    event_handler=EventHandler(),
) as stream:
    stream.until_done()
```

---

## Cost Optimization

### Model Selection Strategy

| Model | Best For | Input Cost | Output Cost |
|-------|----------|------------|-------------|
| **GPT-5** | Complex reasoning, coding, agents | $1.25/1M | $10.00/1M |
| **GPT-5-mini** | Simpler tasks, high volume | $0.25/1M | $2.00/1M |
| **GPT-4o** | General purpose, vision | $2.50/1M | $10.00/1M |
| **GPT-4o-mini** | Cost-effective general use | $0.15/1M | $0.60/1M |

**Strategy**: Use GPT-4o-mini for 70% of routine tasks, reserve GPT-4o/GPT-5 for complex reasoning.

### Prompt Caching

OpenAI caches common prompt prefixes. Structure prompts to maximize cache hits:

```python
# GOOD: Static system prompt at beginning
messages = [
    {"role": "system", "content": LONG_STATIC_INSTRUCTIONS},  # Cached
    {"role": "user", "content": user_input},  # Dynamic
]

# BAD: Dynamic content at beginning breaks cache
messages = [
    {"role": "system", "content": f"Current time: {now}. {LONG_INSTRUCTIONS}"},
]
```

Cached input tokens cost 50% less ($1.25/1M vs $2.50/1M for GPT-4o).

### Batch API (50% Discount)

For non-time-sensitive workloads, use the Batch API:

```python
from openai import OpenAI

client = OpenAI()

# Create batch from JSONL file
batch = client.batches.create(
    input_file_id="file-abc123",  # Upload JSONL first
    endpoint="/v1/chat/completions",
    completion_window="24h",
    metadata={"description": "Daily processing"},
)

# Check status
batch = client.batches.retrieve(batch.id)
print(f"Status: {batch.status}")
print(f"Completed: {batch.request_counts.completed}/{batch.request_counts.total}")
```

### Token Optimization

```python
# 1. Set appropriate max_tokens
response = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    max_tokens=500,  # Limit response length
)

# 2. Use concise system prompts
# BAD: "You are a helpful, friendly, knowledgeable assistant..."
# GOOD: "Answer concisely."

# 3. Count tokens before sending
token_count = client.responses.input_tokens.count(
    model="gpt-4o",
    input=messages,
)
print(f"Input tokens: {token_count.input_tokens}")
```

### Usage Monitoring

```python
response = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
)

usage = response.usage
print(f"Prompt tokens: {usage.prompt_tokens}")
print(f"Completion tokens: {usage.completion_tokens}")
print(f"Total tokens: {usage.total_tokens}")

# Check cached tokens (if applicable)
if hasattr(usage, 'prompt_tokens_details'):
    print(f"Cached tokens: {usage.prompt_tokens_details.cached_tokens}")
```

---

## Error Handling and Rate Limits

### Error Types

```python
import openai
from openai import OpenAI

client = OpenAI()

try:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": "Hello"}],
    )
except openai.APIConnectionError as e:
    print(f"Connection failed: {e}")
    # Retry with backoff
except openai.RateLimitError as e:
    print(f"Rate limit hit: {e}")
    # Wait and retry, check Retry-After header
except openai.AuthenticationError as e:
    print(f"Invalid API key: {e}")
    # Check credentials
except openai.BadRequestError as e:
    print(f"Invalid request: {e}")
    # Fix request parameters
except openai.APIStatusError as e:
    print(f"API error {e.status_code}: {e.message}")
```

### Exponential Backoff

```python
import time
import random
from openai import OpenAI, RateLimitError

def call_with_backoff(func, max_retries=5, base_delay=1.0):
    """Call function with exponential backoff on rate limits."""
    for attempt in range(max_retries):
        try:
            return func()
        except RateLimitError as e:
            if attempt == max_retries - 1:
                raise

            # Exponential backoff with jitter
            delay = base_delay * (2 ** attempt) + random.uniform(0, 1)

            # Respect Retry-After header if present
            if hasattr(e, 'response') and 'Retry-After' in e.response.headers:
                delay = float(e.response.headers['Retry-After'])

            print(f"Rate limited. Retrying in {delay:.2f}s...")
            time.sleep(delay)

client = OpenAI()

result = call_with_backoff(lambda: client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello"}],
))
```

### Rate Limit Headers

Monitor rate limits proactively using response headers:

```python
response = client.chat.completions.with_raw_response.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello"}],
)

headers = response.headers
print(f"Requests remaining: {headers.get('x-ratelimit-remaining-requests')}")
print(f"Tokens remaining: {headers.get('x-ratelimit-remaining-tokens')}")
print(f"Reset time: {headers.get('x-ratelimit-reset-requests')}")

completion = response.parse()
```

### Circuit Breaker Pattern

```python
import time
from dataclasses import dataclass
from enum import Enum

class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

@dataclass
class CircuitBreaker:
    failure_threshold: int = 5
    recovery_timeout: float = 60.0

    state: CircuitState = CircuitState.CLOSED
    failure_count: int = 0
    last_failure_time: float = 0

    def can_execute(self) -> bool:
        if self.state == CircuitState.CLOSED:
            return True
        if self.state == CircuitState.OPEN:
            if time.time() - self.last_failure_time >= self.recovery_timeout:
                self.state = CircuitState.HALF_OPEN
                return True
            return False
        return True  # HALF_OPEN allows one attempt

    def record_success(self):
        self.failure_count = 0
        self.state = CircuitState.CLOSED

    def record_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN
```

---

## Testing

### Mocking OpenAI Responses

```python
import pytest
from unittest.mock import Mock, patch
from openai.types.chat import ChatCompletion, ChatCompletionMessage
from openai.types.chat.chat_completion import Choice

def create_mock_completion(content: str) -> ChatCompletion:
    return ChatCompletion(
        id="test-id",
        created=1234567890,
        model="gpt-4o",
        object="chat.completion",
        choices=[
            Choice(
                index=0,
                message=ChatCompletionMessage(
                    role="assistant",
                    content=content,
                ),
                finish_reason="stop",
            )
        ],
    )

@patch('openai.OpenAI')
def test_chat_completion(mock_openai):
    mock_client = Mock()
    mock_openai.return_value = mock_client
    mock_client.chat.completions.create.return_value = create_mock_completion("Hello!")

    # Your code that uses OpenAI
    from your_module import get_response
    result = get_response("Hi")

    assert result == "Hello!"
    mock_client.chat.completions.create.assert_called_once()
```

### Using respx for HTTP Mocking

```python
import pytest
import respx
from httpx import Response

@respx.mock
@pytest.mark.asyncio
async def test_async_completion():
    respx.post("https://api.openai.com/v1/chat/completions").mock(
        return_value=Response(200, json={
            "id": "test",
            "object": "chat.completion",
            "created": 1234567890,
            "model": "gpt-4o",
            "choices": [{
                "index": 0,
                "message": {"role": "assistant", "content": "Test response"},
                "finish_reason": "stop",
            }],
        })
    )

    from openai import AsyncOpenAI
    client = AsyncOpenAI()

    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": "Hello"}],
    )

    assert response.choices[0].message.content == "Test response"
```

---

## Best Practices Summary

### Do's

| Practice | Reason |
|----------|--------|
| Use `strict: true` for structured outputs | Guarantees schema adherence |
| Use Pydantic models with `.parse()` | Type-safe, auto-validated |
| Implement exponential backoff | Handles rate limits gracefully |
| Monitor token usage | Prevents cost overruns |
| Use async for high-throughput | Better resource utilization |
| Cache static prompt prefixes | 50% cost reduction |
| Batch non-urgent requests | 50% cost reduction |
| Use appropriate model tiers | Match capability to task |

### Don'ts (Anti-Patterns)

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Sharing API keys across apps | Aggregate usage hits limits | Separate keys per app |
| Ignoring rate limit headers | Avoidable 429 errors | Monitor and throttle |
| No retry logic | Transient failures crash app | Exponential backoff |
| Unbounded `max_tokens` | Runaway costs | Set reasonable limits |
| Hardcoded model names | Inflexible deployments | Use configuration |
| Testing with real API | Slow, costly, flaky | Mock responses |
| Ignoring `finish_reason` | Missing truncated responses | Check for "length" |
| Using JSON mode over Structured Outputs | No schema guarantee | Use `json_schema` format |

### Common Mistakes

1. **Not handling refusals**: When using structured outputs, check `message.refusal` in addition to `message.parsed`.

2. **Parallel tool calls with strict mode**: These are incompatible. Set `parallel_tool_calls=False`.

3. **Azure deployment vs model names**: Azure uses deployment names, not model names like "gpt-4o".

4. **Missing tool results**: If the model calls multiple tools, you must return results for ALL of them.

5. **Token limits on Azure**: Azure has per-request token limits. Chunk large documents.

---

## Latest API Updates (2025-2026)

For the most current information, always check:

- [OpenAI API Documentation](https://platform.openai.com/docs)
- [OpenAI Cookbook](https://cookbook.openai.com)
- [Azure OpenAI Documentation](https://learn.microsoft.com/en-us/azure/ai-foundry/openai/)
- [OpenAI Python SDK Changelog](https://github.com/openai/openai-python/releases)

Key recent additions:
- **Responses API**: New agentic-first API with built-in tools
- **Agents SDK**: Multi-agent workflows with handoffs and guardrails
- **GPT-5 Models**: Latest flagship models for reasoning and coding
- **Realtime API**: Voice and real-time interaction support
