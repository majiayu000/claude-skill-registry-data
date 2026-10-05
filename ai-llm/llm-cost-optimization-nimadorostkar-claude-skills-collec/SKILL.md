---
name: llm-cost-optimization
description: Use when an LLM feature costs too much. Covers prompt caching, context reduction, model routing, batching, output limits, and finding where the tokens actually go.
metadata:
  category: ai
  version: 1.0.0
  tags: [cost, tokens, caching, optimization, llm]
---

# LLM Cost Optimization

## Purpose

Reduce the cost of an LLM feature without losing the quality that justified it. Most LLM bills are dominated by one or two things that nobody has measured, and the fix is usually structural rather than a matter of shaving tokens.

## When to Use

- An LLM feature that is too expensive at current or projected volume.
- Before scaling a feature from pilot to production traffic.
- A bill that grew and nobody can explain why.

## Capabilities

- Token accounting: where the spend actually is.
- Prompt caching.
- Context reduction and retrieval narrowing.
- Model routing and downgrading.
- Batch processing for non-interactive work.
- Output-length control.

## Inputs

- Token counts per call, broken down: system, context, history, output.
- Call volume, by feature and by tenant.
- The quality bar that must be maintained.

## Outputs

- A ranked list of cost drivers.
- Changes with measured cost reduction and no quality regression.
- Per-feature cost tracking so the next increase is visible.

## Workflow

1. **Measure where the tokens go** — Input versus output, and within input: system prompt, tools, retrieved context, conversation history. The answer is frequently not what anyone expected.
2. **Cache the stable prefix** — If the system prompt and tools are identical across calls, prompt caching reduces their cost by roughly 90%. This is usually the single largest and cheapest win.
3. **Cut the context, not the quality** — Retrieving twenty chunks when five suffice costs four times as much and often produces a *worse* answer. Measure the quality at each k.
4. **Route to a smaller model** — Most tasks do not need the largest model. Measure the small one before assuming it cannot.
5. **Batch what is not interactive** — Batch APIs are typically half the price for work that can wait. Overnight classification does not need a synchronous call.
6. **Cap the output** — Output tokens cost several times more than input tokens. A `max_tokens` that is generous "just in case" is a standing cost.

## Best Practices

- Output tokens typically cost 3-5x input tokens. A prompt that produces a verbose preamble before the answer is paying a premium for text nobody reads. Instruct the model to answer directly.
- Prompt caching requires a byte-identical prefix. A timestamp, a request ID, or a shuffled tool order at the top of the prompt silently disables it and nobody notices — except the bill.
- Conversation history is the cost that grows without anyone deciding to grow it. Compact it.
- A retry that resends the whole context costs the whole context again. Retry budgets are a cost control, not only a reliability one.
- Attribute cost per feature and per tenant. Without attribution, cost optimization is guesswork, and one customer's usage pattern can consume the margin invisibly.
- The cheapest call is the one you do not make. Cache the *answer*, not just the prompt — many LLM calls in production are for questions already asked.

## Examples

**Finding where the money actually goes:**

```text
Feature: support-assistant. 4.2M calls/month. $18,400/month.

Token breakdown per call (mean):
  System prompt + tools     3,100    every call, identical
  Retrieved context         9,800    top-20 chunks
  Conversation history      6,400    grows unbounded within a session
  User message                180
  Output                      420
                          -------
  Input total              19,480
  Output total                420

Findings, in order of size:
  1. The system prompt is identical on every call and is not cached.
     -> Enable prompt caching. 3,100 tokens x 4.2M at 10% of the cost.
        Saving: ~$2,900/month. Effort: one line.

  2. Retrieval returns 20 chunks. Quality on the eval set peaks at k=6
     and is flat to k=20.
     -> Reduce to k=6. Saving: ~$6,100/month. Quality: unchanged (measured).

  3. History is never compacted; long sessions carry 40k+ tokens.
     -> Compact above 8k. Saving: ~$2,400/month.

  4. 31% of questions are near-duplicates of a previous question.
     -> Semantic cache on the answer. Saving: ~$3,700/month.

  Total: $18,400 -> $3,300/month. No measurable quality change.
```

**The caching mistake that costs the most:**

```python
# This defeats prompt caching entirely, and it is not obvious.
system = f"You are a support assistant. Current time: {datetime.now()}. ..."
#                                                     ^^^^^^^^^^^^^^^^
# The prefix differs on every call, so nothing is ever a cache hit.

# Correct: keep the stable part stable; put the variable part after the
# cache breakpoint.
system = [
    {
        "type": "text",
        "text": STABLE_SYSTEM_PROMPT,           # byte-identical every call
        "cache_control": {"type": "ephemeral"},
    },
    {
        "type": "text",
        "text": f"Current time: {datetime.now().isoformat()}",   # after the breakpoint
    },
]
```

## Notes

- The single most common cost mistake is a variable value — a timestamp, a UUID, a user's name — near the top of an otherwise stable system prompt, which silently disables prompt caching. Check for this first.
- Semantic caching (embedding the question, returning a stored answer on a close match) is powerful and dangerous. It must be scoped per tenant and invalidated when the underlying data changes, or it will serve one customer another's answer.
- Reducing retrieved context often *improves* answer quality while cutting cost. It is the rare optimization with no trade-off, and it is available in most RAG systems that were built by increasing k until the answers looked good.
