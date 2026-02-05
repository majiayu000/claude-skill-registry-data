---
name: llm-call-tracing
description: Instrument LLM API calls with proper spans, tokens, and latency
triggers:
  - "trace LLM calls"
  - "instrument model calls"
  - "LLM observability"
  - "track model latency"
priority: 1
---

# LLM Call Tracing

Instrument LLM API calls to track latency, tokens, costs, and errors.

## Core Principle

Every LLM call should capture:
1. **What model** was called
2. **How long** it took
3. **How many tokens** were used
4. **Did it succeed** or fail
5. **Why it failed** (if applicable)

## Essential Span Attributes

```python
# Required (P0)
span.set_attribute("llm.model", "claude-3-opus-20240229")
span.set_attribute("llm.provider", "anthropic")
span.set_attribute("llm.latency_ms", 2340)
span.set_attribute("llm.success", True)

# Token tracking (P1)
span.set_attribute("llm.tokens.input", 1500)
span.set_attribute("llm.tokens.output", 350)
span.set_attribute("llm.tokens.total", 1850)

# Cost (P1)
span.set_attribute("llm.cost_usd", 0.025)

# Configuration (P2)
span.set_attribute("llm.temperature", 0.7)
span.set_attribute("llm.max_tokens", 4096)
span.set_attribute("llm.stop_reason", "end_turn")

# Error context (when applicable)
span.set_attribute("llm.error.type", "rate_limit")
span.set_attribute("llm.error.message", "Rate limit exceeded")
span.set_attribute("llm.retry_count", 2)
```

## What NOT to Log

**Never log full prompts/responses:**
```python
# BAD - PII risk, storage explosion
span.set_attribute("llm.prompt", messages)
span.set_attribute("llm.response", completion.content)

# GOOD - Safe metadata
span.set_attribute("llm.prompt.message_count", len(messages))
span.set_attribute("llm.prompt.system_length", len(system_prompt))
span.set_attribute("llm.response.length", len(completion.content))
```

## Streaming Considerations

For streaming responses:
- Start span when stream begins
- Update token counts as chunks arrive
- End span when stream completes
- Track time-to-first-token (TTFT)

```python
span.set_attribute("llm.streaming", True)
span.set_attribute("llm.ttft_ms", 145)  # Time to first token
span.set_attribute("llm.chunks", 47)     # Number of chunks
```

## Cost Calculation

Calculate cost from tokens and model pricing:

```python
PRICING = {
    "claude-3-opus": {"input": 15.00, "output": 75.00},  # per 1M tokens
    "claude-3-sonnet": {"input": 3.00, "output": 15.00},
    "claude-3-haiku": {"input": 0.25, "output": 1.25},
    "gpt-4-turbo": {"input": 10.00, "output": 30.00},
    "gpt-4o": {"input": 5.00, "output": 15.00},
}

def calculate_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    pricing = PRICING.get(model, {"input": 0, "output": 0})
    input_cost = (input_tokens / 1_000_000) * pricing["input"]
    output_cost = (output_tokens / 1_000_000) * pricing["output"]
    return round(input_cost + output_cost, 6)
```

## Framework-Specific Patterns

### LangChain
```python
from langfuse.callback import CallbackHandler

handler = CallbackHandler()
chain.invoke(input, config={"callbacks": [handler]})
```

### Direct Anthropic SDK
```python
from langfuse.decorators import observe

@observe(as_type="generation")
def call_claude(messages):
    response = client.messages.create(...)
    return response
```

### OpenAI SDK
```python
from langfuse.openai import openai

# Automatic instrumentation
client = openai.OpenAI()
```

## Error Handling

Capture errors with context:
```python
try:
    response = client.messages.create(...)
except RateLimitError as e:
    span.set_attribute("llm.error.type", "rate_limit")
    span.set_attribute("llm.error.retry_after", e.retry_after)
    raise
except APIError as e:
    span.set_attribute("llm.error.type", "api_error")
    span.set_attribute("llm.error.status", e.status_code)
    raise
```

## Anti-Patterns

See `references/anti-patterns/llm-tracing.md`:
- Logging full prompts (PII, storage)
- Blocking on telemetry (latency)
- Missing token counts (cost blindness)
- No retry tracking (hidden failures)

## Related Skills
- `token-cost-tracking` - Detailed cost attribution
- `error-retry-tracking` - Error handling patterns
