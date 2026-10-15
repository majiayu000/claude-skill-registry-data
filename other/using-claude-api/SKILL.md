---
name: using-claude-api
description: Use when writing or debugging code that calls Anthropic SDK. Covers Opus 4.7, prompt caching, tool use, vision, batch, thinking.
---

# Using Claude API — Practical Patterns

This skill complements the official `claude-api` skill with practical patterns and gotchas. Use this when you're writing or modifying code that imports `anthropic` (Python) / `@anthropic-ai/sdk` (TS).

## Iron Law

**Prompt caching is not optional on system prompts >1024 tokens. Adding `cache_control` is a 30-second change that cuts cost ~90% and latency ~85% on cache hits. If you write or modify a system prompt without it, you've left money on the table.**

## Model IDs (May 2026)

- `claude-opus-4-7` — most capable, 1M context available, supports extended thinking
- `claude-sonnet-4-6` — balanced cost/quality, 200K context, supports thinking
- `claude-haiku-4-5-20251001` — fastest/cheapest, 200K context
- Older `-20241022` / `-20250514` IDs still work but use latest when starting new code.

If migrating retired models: see official `claude-api` skill for the mapping. Don't guess.

## Prompt Caching — MUST for System Prompts

```python
client.messages.create(
    model="claude-opus-4-7",
    system=[
        {
            "type": "text",
            "text": LONG_SYSTEM_PROMPT,  # >1024 tokens
            "cache_control": {"type": "ephemeral"}
        }
    ],
    messages=[...]
)
```

- Cache lives 5 minutes (refreshes on each hit).
- Up to 4 cache breakpoints per request. Put them at stable boundaries (system / tool definitions / docs / dynamic user input).
- Order matters: cached prefix must be identical byte-for-byte to hit. Don't interpolate timestamps before the cache boundary.
- Check `usage.cache_read_input_tokens` and `cache_creation_input_tokens` in the response to verify hits.

## Tool Use Loop

`response.stop_reason` tells you what to do next:

- `"end_turn"` — model finished, return to user
- `"tool_use"` — model wants to call a tool. **You MUST run the tool and continue the conversation with a `tool_result` message.**
- `"max_tokens"` — you set `max_tokens` too low, output truncated
- `"stop_sequence"` — hit a stop_sequence

Full loop:

```python
messages = [{"role": "user", "content": "..."}]
while True:
    resp = client.messages.create(model=..., tools=[...], messages=messages)
    messages.append({"role": "assistant", "content": resp.content})
    if resp.stop_reason != "tool_use":
        break
    tool_results = []
    for block in resp.content:
        if block.type == "tool_use":
            result = run_tool(block.name, block.input)
            tool_results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": result,
            })
    messages.append({"role": "user", "content": tool_results})
```

## Streaming

```python
with client.messages.stream(...) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

Use streaming for: long outputs, latency-sensitive UI, anywhere TTFB matters. Don't use for: batch processing, when you need full response before acting.

## Vision

- Pass image as `{"type": "image", "source": {"type": "url", "url": "..."}}` — prefer URL (less bandwidth, simpler).
- Or base64: `{"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": ...}}`.
- Max image size: 5MB (base64) or larger via URL. Resize before sending to save tokens.
- Image counts as tokens (~1.6K for 1568x1568). Don't paste huge images blindly.

See `[[extracting-from-images]]` for how to interpret images Claude receives.

## Extended Thinking (Opus 4.x)

```python
client.messages.create(
    model="claude-opus-4-7",
    thinking={"type": "enabled", "budget_tokens": 8000},
    max_tokens=16000,  # MUST be > budget_tokens
    messages=[...]
)
```

- Response includes `thinking` blocks before the final answer.
- Use for hard reasoning: math, planning, debugging. Skip for chat/Q&A.
- `budget_tokens` is a soft cap; model may use less.
- Cost: thinking tokens count toward output billing.

## Batch API

```python
batch = client.messages.batches.create(requests=[
    {"custom_id": "req-1", "params": {"model": ..., "messages": ...}},
    ...
])
```

- 50% cheaper than realtime.
- SLA: 24 hours, usually much faster.
- Use for: bulk classification, eval runs, dataset processing.
- Don't use for: interactive flows, latency-sensitive work.

## Files API

For PDF/video/large docs you reference repeatedly:

```python
file = client.files.upload(file=open("doc.pdf", "rb"))
# then reference file.id in messages
```

Persists across requests; uploaded once, referenced many times. Cheaper than re-sending the doc content.

## Error Handling

| Code | Meaning | Action |
|------|---------|--------|
| 400 | Bad request (malformed) | Fix the request, don't retry |
| 401 | Auth | Check API key |
| 403 | Forbidden | Check permissions / org access |
| 429 | Rate limit | Exponential backoff (1s, 2s, 4s, 8s...) |
| 500 | Server error | Retry with backoff |
| 529 | Overloaded | Retry with longer backoff (15s, 30s...) |

Anthropic SDK has built-in retries (`max_retries`, default 2). Set higher (e.g. 5) for batch/background work, leave default for interactive.

**Don't blind-retry 400s.** They won't succeed.

## Red Flags

- You wrote a system prompt >1K tokens with no `cache_control` → you just made the user's bill 10x bigger than it needs to be.
- You hit a tool_use response and called `messages.create` again without appending the `tool_result` → API errors.
- You set `max_tokens=4096` and output got truncated → bump to 8192 or 16384. For Opus 4.7, max is much higher.
- You used `client.messages.create` in a `while True:` with no exit condition for `tool_use` → infinite loop if model loops on tools.
- You're sending the same big PDF on every request instead of using Files API.
- You used Batch API for interactive flow → user waits hours.
- You set `thinking.budget_tokens=20000` but `max_tokens=10000` → 400 error, budget must be < max.

## Not For

- Writing code against OpenAI / Cohere / Gemini / generic-LLM-wrapper SDKs.
- Pure linguistics / prompt-content questions (use `[[prompt-engineering]]`).
- Files named `*-openai.py` / `*-generic-llm.ts`.

## See Also

- `[[prompt-engineering]]` — for writing the prompt content itself.
- `[[extracting-from-images]]` — for handling image inputs.
- Official `claude-api` skill — for migration guides and the canonical reference.
- `[[using-context7]]` — `mcp__context7__resolve-library-id` with "anthropic" pulls latest SDK docs.
