---
name: ai-optimization
description: AI Optimization Engineer — Institutional capability and runbook for ai-optimization.
---

# SKILL: AI Optimization Engineer
## Domain: LLM Cost, Latency, Quality Optimization, Model Selection

**Activation triggers:** AI pipeline, LLM inference cost, model selection,
caching AI responses, streaming, batching, quality evaluation, A/B testing
prompts, AI feature scaling.

---

## Model Selection Matrix

```
Task Type                          | Model                | Why
-----------------------------------|----------------------|---------------------------
Market analysis (high stakes)      | claude-opus-4-5      | Best reasoning, accuracy critical
Journal coaching (high volume)     | claude-haiku-4-5     | 5x cheaper, fast, good enough
Sentiment classification           | claude-haiku-4-5     | Simple binary task
News summarization                 | claude-sonnet-4-5    | Balance of cost + quality
Structured data extraction         | claude-haiku-4-5     | Tool use, deterministic
Portfolio-level narrative          | claude-opus-4-5      | Complex multi-factor reasoning
Code generation (internal tools)   | claude-sonnet-4-5    | Cost-efficient for code
Real-time price commentary         | claude-haiku-4-5     | Latency < 500ms needed
```

---

## Cost Estimation (Per Feature)

```python
# As of 2025 pricing (approximate):
# claude-opus-4-5:    $15/M input tokens,  $75/M output tokens
# claude-sonnet-4-5:  $3/M input tokens,   $15/M output tokens
# claude-haiku-4-5:   $0.25/M input tokens,$1.25/M output tokens

def estimate_monthly_ai_cost(
    daily_analyses: int,
    daily_coaching: int,
    daily_sentiment: int,
) -> dict:
    """Rough cost estimate for AI features."""
    # Market analysis: ~3000 input, ~500 output tokens each
    analysis_cost = daily_analyses * 30 * (
        (3000 * 15 + 500 * 75) / 1_000_000
    )  # opus

    # Journal coaching: ~800 input, ~300 output tokens each
    coaching_cost = daily_coaching * 30 * (
        (800 * 0.25 + 300 * 1.25) / 1_000_000
    )  # haiku

    # Sentiment: ~200 input, ~50 output tokens each
    sentiment_cost = daily_sentiment * 30 * (
        (200 * 0.25 + 50 * 1.25) / 1_000_000
    )  # haiku

    return {
        "market_analysis_usd": round(analysis_cost, 2),
        "journal_coaching_usd": round(coaching_cost, 2),
        "sentiment_usd": round(sentiment_cost, 2),
        "total_monthly_usd": round(analysis_cost + coaching_cost + sentiment_cost, 2),
    }
```

---

## Semantic Response Caching

```python
# Cache AI responses to avoid redundant calls for similar inputs
# Use content hash of normalized input as cache key

import hashlib
import json

async def cached_market_analysis(
    symbol: str,
    timeframe: str,
    ohlcv: list[dict],
    cache: Cache,
) -> MarketSignal:
    # Normalize: use last 20 bars + symbol + timeframe as cache key
    cache_input = {
        "symbol": symbol,
        "timeframe": timeframe,
        "bars": [{"c": b["close"], "t": b["time"]} for b in ohlcv[-20:]],
    }
    cache_key = f"ai:market:{hashlib.sha256(json.dumps(cache_input, sort_keys=True).encode()).hexdigest()[:16]}"

    # Check cache first
    cached = await cache.get(cache_key)
    if cached:
        return MarketSignal.model_validate(cached)

    # Generate fresh analysis
    signal = await analyze_symbol(symbol, timeframe, ohlcv)

    # Cache for timeframe-appropriate TTL
    ttl = {"1": 60, "5": 300, "15": 600, "60": 3600, "D": 86400}.get(timeframe, 300)
    await cache.set(cache_key, signal.model_dump(), ttl=ttl)

    return signal
```

---

## Streaming for Real-Time UX

```python
# Stream AI responses for better UX (user sees output appear progressively)
# integral-imi-backend/app/api/v1/endpoints/intelligence.py

from fastapi.responses import StreamingResponse
from anthropic import AsyncAnthropic

client = AsyncAnthropic()

@router.get("/intelligence/analyze-stream/{symbol}")
async def stream_analysis(
    symbol: str,
    current_user: User = Depends(get_current_active_user),
):
    async def generate():
        async with client.messages.stream(
            model="claude-sonnet-4-5",
            max_tokens=1024,
            system=MARKET_ANALYSIS_SYSTEM,
            messages=[{"role": "user", "content": f"Analyze {symbol}..."}],
        ) as stream:
            async for text in stream.text_stream:
                yield f"data: {json.dumps({'text': text})}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")
```

```typescript
// Frontend — consume SSE stream
async function streamAnalysis(symbol: string, onChunk: (text: string) => void) {
  const eventSource = new EventSource(
    `${EXPERT_API_URL}/intelligence/analyze-stream/${symbol}`,
    { withCredentials: true },
  );

  eventSource.onmessage = (e) => {
    if (e.data === '[DONE]') {
      eventSource.close();
      return;
    }
    const { text } = JSON.parse(e.data);
    onChunk(text);
  };

  return () => eventSource.close();
}
```

---

## Prompt Quality Evaluation

```python
# Evaluate prompt quality using a judge model
# Run this in CI or manually when changing prompts

async def evaluate_prompt_quality(
    prompt_fn: callable,
    test_cases: list[dict],
    judge_criteria: str,
) -> dict:
    results = []

    for case in test_cases:
        output = await prompt_fn(**case["input"])

        # Judge model evaluates output quality
        judgment = await client.messages.create(
            model="claude-opus-4-5",
            max_tokens=256,
            system=f"You are a quality evaluator. Criteria: {judge_criteria}\nScore 1-5 and explain briefly. Output JSON: {{\"score\": N, \"reason\": \"...\"}}",
            messages=[{
                "role": "user",
                "content": f"Input: {json.dumps(case['input'])}\nOutput: {output}\nExpected qualities: {case['expected_qualities']}"
            }],
        )

        result = json.loads(judgment.content[0].text)
        results.append({**case, "score": result["score"], "reason": result["reason"]})

    avg_score = sum(r["score"] for r in results) / len(results)
    return {"avg_score": avg_score, "cases": results, "passed": avg_score >= 3.5}
```

---

## Batching Low-Priority AI Tasks

```python
# Don't call AI synchronously for background enrichment tasks
# Use a queue + batch processor

from app.workers.ai_batch_worker import ai_batch_queue

# Enqueue journal coaching (runs in background)
await ai_batch_queue.enqueue(
    task_type="journal_coaching",
    payload={"trade_id": str(trade.id), "entry_text": entry.notes},
    priority="low",
)

# Batch processor runs every 30s, groups by task_type
# Processes up to 50 tasks per batch call using one LLM request with multiple items
```

---

## Anti-Patterns

```
✗ Using opus for every call (10x cost vs haiku for simple tasks)
✗ No response caching (same analysis requested every 5 seconds)
✗ Blocking the request path on AI inference (use background queue for non-critical)
✗ No retry with exponential backoff on API rate limits (HTTP 429)
✗ Trusting LLM output without schema validation (hallucinations break production)
✗ Streaming when a short response suffices (adds complexity for no UX gain)
✗ No cost monitoring (surprise $5000 AI bill at month end)
✗ Changing prompts in production without quality evaluation
✗ Sending user-identifying information to external LLM APIs without consent disclosure
```
