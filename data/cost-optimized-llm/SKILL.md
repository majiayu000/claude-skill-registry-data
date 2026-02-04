---
name: cost-optimized-llm
description: Implement cost-optimized LLM routing with NO OpenAI. Use tiered model selection (DeepSeek, Haiku, Sonnet) to achieve 70-90% cost savings. Triggers on "LLM costs", "model selection", "cost optimization", "which model", "DeepSeek", "Claude pricing", "reduce AI costs".
---

# Cost-Optimized LLM Routing

Achieve 70-90% cost savings with intelligent model routing. NO OpenAI allowed.

## Critical Rule

**NEVER use OpenAI models in this ecosystem.**

Allowed providers:
- Anthropic Claude (Haiku, Sonnet, Opus)
- Google Gemini (Flash, Pro)
- DeepSeek (via OpenRouter)
- Qwen (via OpenRouter)
- Cerebras (speed-critical)
- Local: Ollama, sentence-transformers

## Cost Comparison

| Model | Cost per 1M tokens | Use Case |
|-------|-------------------|----------|
| DeepSeek V3 | $0.14 input / $0.28 output | Simple queries, classification |
| Claude Haiku | $0.25 input / $1.25 output | Moderate complexity |
| Gemini Flash | FREE (limited) | MVP, prototyping |
| Claude Sonnet | $3.00 input / $15.00 output | Complex reasoning |
| Claude Opus | $15.00 input / $75.00 output | Expert tasks only |

## Tiered Routing Strategy

### Tier 1: Simple Tasks → DeepSeek ($0.0001/1K)

Use for:
- Text classification
- Simple extractions
- Formatting
- Basic Q&A
- Sentiment analysis

```python
from openai import OpenAI  # OpenRouter uses OpenAI SDK

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"]
)

response = client.chat.completions.create(
    model="deepseek/deepseek-chat",
    messages=[{"role": "user", "content": prompt}],
    max_tokens=500
)
```

### Tier 2: Moderate Tasks → Claude Haiku ($0.00075/1K)

Use for:
- Code review
- Summarization
- Multi-step reasoning
- Data analysis

```python
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-3-5-haiku-20241022",
    max_tokens=1024,
    messages=[{"role": "user", "content": prompt}]
)
```

### Tier 3: Complex Tasks → Claude Sonnet ($0.009/1K)

Use for:
- Architecture decisions
- Complex code generation
- Multi-file refactoring
- Nuanced analysis

```python
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=4096,
    messages=[{"role": "user", "content": prompt}]
)
```

## Automatic Routing Implementation

```python
from enum import Enum
from typing import Literal

class TaskComplexity(Enum):
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"

def route_to_model(complexity: TaskComplexity) -> str:
    """Route to appropriate model based on complexity."""
    routing = {
        TaskComplexity.SIMPLE: "deepseek/deepseek-chat",
        TaskComplexity.MODERATE: "claude-3-5-haiku-20241022",
        TaskComplexity.COMPLEX: "claude-sonnet-4-20250514"
    }
    return routing[complexity]

def estimate_complexity(prompt: str) -> TaskComplexity:
    """Estimate task complexity from prompt characteristics."""
    # Simple heuristics
    word_count = len(prompt.split())
    has_code = "```" in prompt or "def " in prompt or "function" in prompt
    has_analysis = any(w in prompt.lower() for w in ["analyze", "compare", "evaluate"])

    if word_count < 50 and not has_code and not has_analysis:
        return TaskComplexity.SIMPLE
    elif word_count < 200 or (has_code and not has_analysis):
        return TaskComplexity.MODERATE
    else:
        return TaskComplexity.COMPLEX

def smart_complete(prompt: str, force_model: str = None) -> str:
    """Complete with automatic model routing."""
    if force_model:
        model = force_model
    else:
        complexity = estimate_complexity(prompt)
        model = route_to_model(complexity)

    # Route to appropriate client
    if model.startswith("deepseek"):
        return call_openrouter(model, prompt)
    else:
        return call_anthropic(model, prompt)
```

## Free Tier Strategy (Gemini Flash)

For MVPs and prototyping, use Gemini Flash (FREE):

```python
import google.generativeai as genai

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

response = model.generate_content(prompt)
```

Limits:
- 15 requests/minute
- 1 million tokens/day
- 1,500 requests/day

## Cost Tracking

Track costs per project:

```python
import json
from datetime import datetime
from pathlib import Path

COST_LOG = Path.home() / ".claude" / "llm_costs.jsonl"

def log_cost(project: str, model: str, input_tokens: int, output_tokens: int):
    """Log LLM usage for cost tracking."""
    costs = {
        "deepseek/deepseek-chat": (0.00014, 0.00028),
        "claude-3-5-haiku-20241022": (0.00025, 0.00125),
        "claude-sonnet-4-20250514": (0.003, 0.015),
        "gemini-1.5-flash": (0, 0)  # Free
    }

    input_cost, output_cost = costs.get(model, (0.01, 0.03))
    total = (input_tokens / 1_000_000 * input_cost) + (output_tokens / 1_000_000 * output_cost)

    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "project": project,
        "model": model,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "cost_usd": round(total, 6)
    }

    with open(COST_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")

    return total
```

## Voice AI Cost Optimization

For voice pipelines (vozlux, solarvoice-ai):

### STT (Speech-to-Text)
- **Deepgram Nova-2**: $0.0043/min (recommended)
- **AssemblyAI**: $0.00025/sec

### TTS (Text-to-Speech)
- **Cartesia Sonic-3**: ~$0.01/1K chars (quality)
- **AWS Polly**: ~$0.004/1K chars (budget)

### Tier-Based Voice Routing

```python
def get_voice_tier(subscription: str) -> dict:
    tiers = {
        "starter": {
            "tts": "polly",
            "stt": "deepgram-base",
            "llm": "deepseek"
        },
        "pro": {
            "tts": "cartesia",
            "stt": "deepgram-nova",
            "llm": "haiku"
        },
        "enterprise": {
            "tts": "cartesia",
            "stt": "deepgram-nova",
            "llm": "sonnet"
        }
    }
    return tiers.get(subscription, tiers["starter"])
```

## Monthly Budget Estimates

For a typical Scientia project:

| Usage Level | DeepSeek Heavy | Mixed Tier | Sonnet Heavy |
|-------------|----------------|------------|--------------|
| Light (10K queries) | $1.40 | $8 | $90 |
| Medium (100K queries) | $14 | $80 | $900 |
| Heavy (1M queries) | $140 | $800 | $9,000 |

**Recommendation**: Use Mixed Tier routing for 90%+ of use cases.

## Environment Variables

Required in `.env`:

```bash
# Primary (Anthropic)
ANTHROPIC_API_KEY=sk-ant-...

# Cost optimization (OpenRouter for DeepSeek)
OPENROUTER_API_KEY=sk-or-...

# Free tier (Google)
GOOGLE_API_KEY=AIza...

# NEVER set these:
# OPENAI_API_KEY=  # FORBIDDEN
```

## Validation

lang-core enforces NO OpenAI at runtime:

```python
def validate_environment():
    """Block OpenAI usage."""
    if os.environ.get("OPENAI_API_KEY"):
        raise EnvironmentError(
            "OpenAI is not allowed in Scientia projects. "
            "Use ANTHROPIC_API_KEY or OPENROUTER_API_KEY instead."
        )
```
