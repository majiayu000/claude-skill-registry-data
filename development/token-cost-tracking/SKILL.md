---
name: token-cost-tracking
description: Track token usage and costs across agents for budget management
triggers:
  - "track tokens"
  - "token usage"
  - "cost tracking"
  - "LLM costs"
  - "budget monitoring"
priority: 1
---

# Token and Cost Tracking

Track token usage and costs across agents for budget management and optimization.

## Core Principle

Every organization needs to answer:
1. **How much** are we spending on LLMs?
2. **Where** is the spend going (features, agents, users)?
3. **Are we within** budget?
4. **What's trending** (up or down)?

## Essential Attributes

```python
# Per-call token tracking
span.set_attribute("llm.tokens.input", 1500)
span.set_attribute("llm.tokens.output", 350)
span.set_attribute("llm.tokens.total", 1850)

# Per-call cost
span.set_attribute("llm.cost_usd", 0.025)

# Attribution
span.set_attribute("cost.feature", "document_analysis")
span.set_attribute("cost.agent", "researcher")
span.set_attribute("cost.user_id", "user_abc")  # Hashed
span.set_attribute("cost.org_id", "org_123")
```

## Model Pricing Table

Keep pricing updated (prices as of late 2024):

```python
MODEL_PRICING = {
    # Anthropic (per 1M tokens)
    "claude-3-opus": {"input": 15.00, "output": 75.00},
    "claude-3-5-sonnet": {"input": 3.00, "output": 15.00},
    "claude-3-5-haiku": {"input": 0.80, "output": 4.00},
    "claude-3-haiku": {"input": 0.25, "output": 1.25},

    # OpenAI (per 1M tokens)
    "gpt-4-turbo": {"input": 10.00, "output": 30.00},
    "gpt-4o": {"input": 2.50, "output": 10.00},
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    "gpt-3.5-turbo": {"input": 0.50, "output": 1.50},

    # Embeddings (per 1M tokens)
    "text-embedding-3-large": {"input": 0.13, "output": 0},
    "text-embedding-3-small": {"input": 0.02, "output": 0},
    "text-embedding-ada-002": {"input": 0.10, "output": 0},
}
```

## Cost Calculation

```python
def calculate_cost(
    model: str,
    input_tokens: int,
    output_tokens: int,
    cached_tokens: int = 0,
    cache_discount: float = 0.9  # 90% discount for cached
) -> float:
    """Calculate cost for an LLM call."""
    pricing = MODEL_PRICING.get(model)
    if not pricing:
        return 0.0

    # Cached tokens are discounted
    effective_input = input_tokens - cached_tokens
    cached_cost = (cached_tokens / 1_000_000) * pricing["input"] * (1 - cache_discount)
    input_cost = (effective_input / 1_000_000) * pricing["input"]
    output_cost = (output_tokens / 1_000_000) * pricing["output"]

    return round(input_cost + cached_cost + output_cost, 6)
```

## Aggregation Levels

Track at multiple granularities:

### Per-Call
```python
span.set_attribute("llm.cost_usd", 0.025)
```

### Per-Agent Run
```python
span.set_attribute("agent.total_tokens", 15000)
span.set_attribute("agent.total_cost_usd", 0.45)
span.set_attribute("agent.llm_calls", 5)
```

### Per-Session
```python
span.set_attribute("session.total_tokens", 45000)
span.set_attribute("session.total_cost_usd", 1.35)
span.set_attribute("session.agent_runs", 3)
```

### Per-User (Daily/Monthly)
Track in your observability platform, not in spans.

## Budget Alerting

Set up alerts for:
```python
BUDGET_THRESHOLDS = {
    "per_call_max": 1.00,      # Alert if single call > $1
    "per_session_max": 10.00,  # Alert if session > $10
    "per_user_daily": 50.00,   # Alert if user > $50/day
    "org_daily": 1000.00,      # Alert if org > $1000/day
}

def check_budget(cost: float, level: str, entity_id: str):
    threshold = BUDGET_THRESHOLDS.get(f"{level}_max")
    if threshold and cost > threshold:
        log_budget_alert(level, entity_id, cost, threshold)
```

## Framework Integration

### Langfuse
```python
from langfuse import Langfuse

langfuse = Langfuse()

# Automatic token/cost tracking
trace = langfuse.trace(name="agent_run")
generation = trace.generation(
    name="llm_call",
    model="claude-3-5-sonnet",
    usage={
        "input": 1500,
        "output": 350,
        "unit": "TOKENS"
    }
)
# Langfuse calculates cost automatically
```

### LangSmith
```python
from langsmith import Client

client = Client()
# Token tracking automatic via callbacks
# Cost calculation in LangSmith dashboard
```

### OpenTelemetry
```python
from opentelemetry import trace

tracer = trace.get_tracer("agent")

with tracer.start_as_current_span("llm_call") as span:
    span.set_attribute("llm.tokens.input", 1500)
    span.set_attribute("llm.tokens.output", 350)
    span.set_attribute("llm.cost_usd", calculate_cost(...))
```

## Caching Impact

Track cache hits for accurate costs:
```python
span.set_attribute("llm.cache.hit", True)
span.set_attribute("llm.cache.tokens_saved", 1200)
span.set_attribute("llm.cache.cost_saved_usd", 0.018)
```

## Optimization Signals

Track metrics that indicate optimization opportunities:
```python
# Prompt efficiency
span.set_attribute("prompt.compression_ratio", 0.7)
span.set_attribute("prompt.could_use_haiku", True)

# Model selection
span.set_attribute("model.recommendation", "could_downgrade")
span.set_attribute("model.quality_requirement", "low")
```

## Anti-Patterns

- Not tracking tokens (cost blindness)
- Missing cost attribution (can't optimize)
- Hardcoded pricing (becomes stale)
- No budget alerts (surprise bills)
- Tracking at wrong granularity

## Related Skills
- `llm-call-tracing` - LLM instrumentation
- `session-conversation-tracking` - Session aggregation
