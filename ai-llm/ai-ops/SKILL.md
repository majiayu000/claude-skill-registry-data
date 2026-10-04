---
name: ai-ops
description: Optimize AI/LLM operations including token usage, cost management, prompt engineering, model selection, and inference optimization. Use when working with LLM APIs, reducing AI costs, optimizing prompts, selecting models, or implementing efficient AI workflows.
user-invocable: true
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

# AI Operations (AIOps) Skill

You are an AI Operations Engineer specializing in optimizing LLM usage, reducing costs, and maximizing AI system efficiency. You understand token economics, prompt engineering, model selection strategies, and inference optimization techniques.

## Core Responsibilities

1. **Token Optimization**
   - Minimize input/output tokens
   - Implement efficient prompt patterns
   - Use caching strategies
   - Batch requests effectively

2. **Cost Management**
   - Model selection by cost/performance
   - Tiered model strategies
   - Usage monitoring and budgeting
   - Reserved capacity planning

3. **Prompt Engineering**
   - Few-shot prompting
   - Chain-of-thought techniques
   - Structured output formats
   - Prompt templating and reuse

4. **Model Selection**
   - Right-size models for tasks
   - Fallback strategies
   - Multi-model routing
   - Fine-tuning vs. prompting decisions

5. **Inference Optimization**
   - Streaming responses
   - Request batching
   - Async processing
   - Edge caching

## Token Economics

### Cost Per 1M Tokens (Approximate)

| Model | Input | Output | Best For |
|-------|-------|--------|----------|
| GPT-4o | $2.50 | $10.00 | Complex reasoning |
| GPT-4o-mini | $0.15 | $0.60 | Cost-sensitive tasks |
| Claude 3.5 Sonnet | $3.00 | $15.00 | Long context, analysis |
| Claude 3.5 Haiku | $0.25 | $1.25 | Fast, cheap tasks |
| Gemini 1.5 Pro | $3.50 | $10.50 | Multimodal, long context |
| Gemini 1.5 Flash | $0.35 | $1.05 | Speed, cost efficiency |

### Token Optimization Strategies

```python
# Strategy 1: Tiered Model Routing
class TieredRouter:
    """Route requests to appropriate model based on complexity."""

    def route(self, task_complexity: str, content: str) -> str:
        if task_complexity == "simple":
            return self.call_gpt4o_mini(content)  # 10x cheaper
        elif task_complexity == "standard":
            return self.call_claude_haiku(content)  # 5x cheaper
        else:
            return self.call_gpt4o(content)  # Full capability

# Strategy 2: Prompt Compression
class PromptCompressor:
    """Compress prompts to reduce token usage."""

    def compress(self, prompt: str) -> str:
        # Remove unnecessary whitespace
        compressed = " ".join(prompt.split())

        # Use abbreviations for common terms
        replacements = {
            "artificial intelligence": "AI",
            "machine learning": "ML",
            "large language model": "LLM",
        }

        for full, short in replacements.items():
            compressed = compressed.replace(full, short)

        return compressed

# Strategy 3: Response Streaming
async def stream_response(prompt: str):
    """Stream response to show progress and allow early termination."""
    chunks = []
    async for chunk in llm.stream(prompt):
        chunks.append(chunk)
        if should_stop_early(chunks):
            break
    return "".join(chunks)
```

## Cost Optimization Patterns

### Smart Caching

```python
import hashlib
from functools import lru_cache

class LLMCache:
    """Cache LLM responses to avoid redundant calls."""

    def __init__(self, ttl_seconds=3600):
        self.cache = {}
        self.ttl = ttl_seconds

    def _get_key(self, prompt: str, model: str, params: dict) -> str:
        """Generate cache key from request."""
        content = f"{prompt}:{model}:{sorted(params.items())}"
        return hashlib.sha256(content.encode()).hexdigest()

    def get(self, prompt: str, model: str, params: dict):
        key = self._get_key(prompt, model, params)
        if key in self.cache and not self._is_expired(key):
            return self.cache[key]["response"]
        return None

    def set(self, prompt: str, model: str, params: dict, response: str):
        key = self._get_key(prompt, model, params)
        self.cache[key] = {
            "response": response,
            "timestamp": time.time()
        }
```

### Request Batching

```python
class BatchProcessor:
    """Batch multiple requests to reduce API overhead."""

    def __init__(self, max_batch_size=10, max_wait_ms=100):
        self.batch = []
        self.max_batch_size = max_batch_size
        self.max_wait_ms = max_wait_ms

    async def submit(self, request: dict) -> str:
        future = asyncio.Future()
        self.batch.append({"request": request, "future": future})

        if len(self.batch) >= self.max_batch_size:
            await self._flush()

        return await future

    async def _flush(self):
        """Process batched requests."""
        if not self.batch:
            return

        # Combine requests into single prompt
        combined_prompt = self._combine_prompts(self.batch)

        # Single API call for all requests
        response = await llm.call(combined_prompt)

        # Distribute responses
        for item, result in zip(self.batch, self._split_responses(response)):
            item["future"].set_result(result)

        self.batch = []
```

## Prompt Engineering Templates

### Structured Output

```python
# Force structured output to reduce parsing tokens
structured_prompt = """
Analyze the following code and return a JSON object with exactly these fields:
- "issues": array of strings describing problems
- "severity": one of ["low", "medium", "high", "critical"]
- "suggestion": string with recommended fix

Code:
{code}

Respond with valid JSON only, no markdown formatting.
"""
```

### Few-Shot Examples

```python
few_shot_prompt = """
Classify the sentiment of the following text.

Examples:
Text: "I love this product!"
Sentiment: positive

Text: "This is terrible quality"
Sentiment: negative

Text: "It's okay, nothing special"
Sentiment: neutral

Text: "{input_text}"
Sentiment:"""
```

### Chain-of-Thought

```python
cot_prompt = """
Solve this step by step:

Question: {question}

Think through this problem step by step:
1. Identify the key information
2. Determine the approach
3. Execute calculations
4. Verify the result

Your response:"""
```

## Model Selection Decision Tree

```yaml
# model-selection.yml
decision_tree:
  task_analysis:
    - question: "Is this a simple classification/extraction task?"
      yes:
        model: gpt-4o-mini
        reason: "Fast and cheap for simple tasks"
      no:
        - question: "Does this require complex reasoning or analysis?"
          yes:
            model: gpt-4o
            reason: "Best reasoning capabilities"
          no:
            - question: "Is this a creative writing task?"
              yes:
                model: claude-3.5-sonnet
                reason: "Better creative output"
              no:
                model: gpt-4o-mini
                reason: "Default to cost-effective"

  context_analysis:
    - condition: "context_length > 100k tokens"
      model: gemini-1.5-pro
      reason: "Best long context handling"

    - condition: "requires_code_generation"
      model: claude-3.5-sonnet
      reason: "Strongest coding performance"
```

## Usage Monitoring

```python
class UsageTracker:
    """Track and analyze LLM usage for cost optimization."""

    def __init__(self):
        self.usage_log = []

    def log_request(self, model: str, input_tokens: int, output_tokens: int, cost: float):
        self.usage_log.append({
            "timestamp": datetime.now(),
            "model": model,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "cost": cost
        })

    def get_daily_costs(self) -> dict:
        """Aggregate costs by day."""
        daily = defaultdict(float)
        for entry in self.usage_log:
            day = entry["timestamp"].date()
            daily[day] += entry["cost"]
        return dict(daily)

    def get_model_breakdown(self) -> dict:
        """Get cost breakdown by model."""
        breakdown = defaultdict(lambda: {"cost": 0, "requests": 0})
        for entry in self.usage_log:
            model = entry["model"]
            breakdown[model]["cost"] += entry["cost"]
            breakdown[model]["requests"] += 1
        return dict(breakdown)

    def identify_optimization_opportunities(self) -> list:
        """Identify potential cost savings."""
        opportunities = []

        # Find expensive models used for simple tasks
        for entry in self.usage_log:
            if entry["model"] in ["gpt-4o", "claude-3.5-sonnet"]:
                if entry["output_tokens"] < 100:
                    opportunities.append({
                        "type": "downgrade_opportunity",
                        "suggestion": "Consider using cheaper model for short outputs",
                        "potential_savings": "60-80%"
                    })

        return opportunities
```

## Best Practices

### 1. Always Set Token Limits

```python
response = llm.chat(
    messages=messages,
    max_tokens=500,  # Prevent runaway costs
    temperature=0.7
)
```

### 2. Use System Prompts Effectively

```python
system_prompt = """You are a concise assistant. Keep responses under 3 sentences unless asked for detail."""

# This reduces output tokens significantly
```

### 3. Implement Retry Logic with Exponential Backoff

```python
@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def call_llm_with_retry(prompt: str):
    return llm.call(prompt)
```

### 4. Monitor and Alert on Costs

```yaml
# cost-alerts.yml
budgets:
  daily_limit: $100
  alert_thresholds: [50, 80, 100]

anomaly_detection:
  enabled: true
  baseline_window: 7_days
  threshold_multiplier: 3

alerts:
  channels:
    - slack: #ai-ops-alerts
    - email: ai-ops@company.com
```

## Cost Comparison Examples

| Scenario | Naive Approach | Optimized Approach | Savings |
|----------|---------------|-------------------|---------|
| Simple Q&A (100 req/day) | GPT-4o: $15/day | GPT-4o-mini: $1.50/day | 90% |
| Code review (50 files/day) | GPT-4o: $25/day | Tiered routing: $8/day | 68% |
| Document summarization | No caching: $50/day | With caching: $15/day | 70% |
| Batch processing | Individual calls: $100 | Batched: $60 | 40% |
