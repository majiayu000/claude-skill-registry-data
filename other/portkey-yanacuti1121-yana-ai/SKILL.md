---
name: portkey
description: Portkey AI gateway — unified LLM API, load balancing, fallbacks, caching, guardrails, observability
triggers:
  - portkey
  - portkey gateway
  - llm gateway portkey
  - portkey fallback
  - portkey load balance
  - portkey cache
  - portkey guardrails
  - unified llm api
  - portkey virtual key
  - portkey config
do_not_use_for:
  - single model calls without routing — use litellm directly
  - local model serving — use ollama
  - evaluation — use ragas/deepeval
see_also:
  - litellm
  - langfuse
  - ollama-patterns
---

# Portkey — AI Gateway

## Setup & Virtual Keys

```python
from portkey_ai import Portkey

# Virtual keys abstract provider credentials
client = Portkey(
    api_key="pk-...",                   # Portkey API key
    virtual_key="anthropic-vk-...",     # Virtual key for provider
)

# Drop-in OpenAI replacement
response = client.chat.completions.create(
    model="claude-sonnet-4-6",
    messages=[{"role": "user", "content": "Hello"}],
)
print(response.choices[0].message.content)
```

## Configs — Gateway Routing

```python
from portkey_ai import createHeaders, PORTKEY_GATEWAY_URL
import openai

# Config-based routing — define in Portkey dashboard or inline
config = {
    "strategy": {
        "mode": "fallback",             # fallback | loadbalance | single
    },
    "targets": [
        {
            "virtual_key": "anthropic-vk",
            "override_params": {"model": "claude-sonnet-4-6"},
            "weight": 0.7,
        },
        {
            "virtual_key": "openai-vk",
            "override_params": {"model": "gpt-4o"},
            "weight": 0.3,
        },
    ],
}

# Use with openai client (Portkey as proxy)
openai_client = openai.OpenAI(
    api_key="pk-...",
    base_url=PORTKEY_GATEWAY_URL,
    default_headers=createHeaders(
        api_key="pk-...",
        config=config,
    ),
)
```

## Load Balancing

```python
lb_config = {
    "strategy": {"mode": "loadbalance"},
    "targets": [
        {"virtual_key": "openai-vk-1", "weight": 50},
        {"virtual_key": "openai-vk-2", "weight": 30},
        {"virtual_key": "openai-vk-3", "weight": 20},
    ],
}

client = Portkey(api_key="pk-...", config=lb_config)
```

## Fallback with Retry

```python
fallback_config = {
    "strategy": {"mode": "fallback"},
    "targets": [
        {
            "virtual_key": "primary-vk",
            "override_params": {"model": "claude-opus-4-7"},
            "retry": {"attempts": 2, "on_status_codes": [429, 500, 502, 503]},
        },
        {
            "virtual_key": "backup-vk",
            "override_params": {"model": "gpt-4o"},
        },
    ],
}

client = Portkey(api_key="pk-...", config=fallback_config)
response = client.chat.completions.create(
    model="claude-opus-4-7",            # overridden by config
    messages=[{"role": "user", "content": "Complex task"}],
)
```

## Caching

```python
cache_config = {
    "cache": {
        "mode": "semantic",             # simple | semantic
        "max_age": 3600,                # seconds
    },
    "virtual_key": "openai-vk",
}

client = Portkey(api_key="pk-...", config=cache_config)
# Second identical (or semantically similar) call served from cache
r1 = client.chat.completions.create(model="gpt-4o", messages=[...])
r2 = client.chat.completions.create(model="gpt-4o", messages=[...])
print(r2.extensions.cache_status)      # HIT
```

## Guardrails

```python
# Input/output guardrails — defined in Portkey dashboard
guardrail_config = {
    "virtual_key": "anthropic-vk",
    "guardrails": {
        "input_guardrails": ["no-pii", "topic-restriction"],
        "output_guardrails": ["no-harmful-content", "length-check"],
        "on_fail": "block",             # block | warn | replace
    },
}

client = Portkey(api_key="pk-...", config=guardrail_config)
try:
    response = client.chat.completions.create(
        model="claude-sonnet-4-6",
        messages=[{"role": "user", "content": user_input}],
    )
except Exception as e:
    # Guardrail blocked the request
    print(f"Blocked: {e}")
```

## Observability & Metadata

```python
client = Portkey(
    api_key="pk-...",
    virtual_key="anthropic-vk",
)

response = client.with_options(
    metadata={
        "user_id": "user-123",
        "session_id": "sess-456",
        "environment": "production",
        "_prompt": "rag-v2",            # prompt name for dashboard grouping
    }
).chat.completions.create(
    model="claude-sonnet-4-6",
    messages=[{"role": "user", "content": query}],
)
# View traces at app.portkey.ai/logs
```

## Prompt Templates

```python
# Fetch and render prompts from Portkey dashboard
from portkey_ai import Portkey

client = Portkey(api_key="pk-...")
prompt = client.prompts.completions.create(
    prompt_id="pp-my-prompt-id",
    variables={"context": doc_context, "question": user_query},
)
print(prompt.choices[0].message.content)
```

## Anti-Fake-Pass Checks

- Virtual keys are created in Portkey dashboard — they proxy provider API keys server-side
- `config` can be a dict (inline) or a string config ID from the dashboard
- `strategy.mode: "fallback"` tries targets in order on error — not round-robin
- Semantic cache requires sentence-transformer similarity — first call always misses
- Guardrails must be created in dashboard first — referencing by name only
- `with_options()` returns a new client instance — does not mutate the original
