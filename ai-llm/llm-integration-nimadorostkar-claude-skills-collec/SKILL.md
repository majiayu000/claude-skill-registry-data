---
name: llm-integration
description: Use when integrating an LLM API into an application. Covers streaming, retries and rate limits, timeouts, caching, fallback across providers, and the production concerns that a tutorial integration ignores.
metadata:
  category: ai
  version: 1.0.0
  tags: [llm, api, streaming, retries, production]
---

# LLM Integration

## Purpose

Integrate a language model into a production application, where the API is slow, rate-limited, occasionally down, and billed per token — none of which the quickstart mentions.

## When to Use

- Adding an LLM to a production application.
- An LLM feature that is slow, expensive, or unreliable.
- Handling rate limits, streaming, or provider failover.
- Deciding where the model call belongs in the architecture.

## Capabilities

- Streaming responses and partial rendering.
- Retry, backoff, and rate-limit handling.
- Timeouts and cancellation.
- Prompt caching and response caching.
- Multi-provider fallback.
- Token accounting and cost control.

## Inputs

- The feature, its latency budget, and its cost budget.
- The provider's rate limits and their actual behavior under load.
- Whether the output is user-facing (stream it) or machine-consumed (do not).

## Outputs

- A client with retries, timeouts, and a circuit breaker.
- Streaming where a user is waiting.
- Cost and latency instrumented per call.

## Workflow

1. **Stream anything a human waits for** — A 12-second response that starts rendering at 400ms feels fast. The same response delivered at once feels broken. Streaming is a perceived-latency fix, not a throughput one.
2. **Handle rate limits properly** — Honor `Retry-After`. Exponential backoff with jitter. A retry storm against a rate-limited endpoint extends the outage.
3. **Set a timeout** — LLM calls can hang. An unbounded call holds a connection and a worker until something else breaks.
4. **Cache the stable prefix** — Prompt caching makes a large system prompt nearly free after the first call. This is often the largest single cost reduction available.
5. **Fail over deliberately** — A second provider or a smaller model as a fallback. Decide in advance whether a degraded answer is better than no answer for this feature.
6. **Instrument tokens and cost per call** — Attributed to the feature and the tenant. Without this, an LLM bill is an unexplainable number.

## Best Practices

- Never call an LLM synchronously inside a request that has a tight latency budget. Stream it, or move it to a job and notify.
- The model will occasionally return something unusable. Every LLM call needs a defined behavior for "the output was garbage" — usually retry once, then fall back.
- Set `max_tokens` deliberately. Without it, a runaway generation costs money and time until it hits the model's own limit.
- Retry on 429 and 5xx. Do not retry on 400 — the request is malformed and will be malformed again.
- Prompt caching requires a byte-identical prefix. A timestamp or a request ID at the top of the system prompt silently defeats it.
- Log the prompt, the response, and the token counts for a sample of calls. When quality degrades, this is the only evidence you will have.

## Examples

**A production client: timeout, retry, cache, fallback:**

```python
class LLMClient:
    def __init__(self, primary: Provider, fallback: Provider | None = None):
        self.primary = primary
        self.fallback = fallback
        self.breaker = CircuitBreaker(failure_threshold=5, reset_timeout=30)

    async def complete(
        self,
        system: str,
        messages: list[Message],
        *,
        max_tokens: int = 2048,
        timeout: float = 60.0,
    ) -> Completion:
        for attempt in range(3):
            try:
                if self.breaker.is_open:
                    break                             # skip straight to the fallback

                async with asyncio.timeout(timeout):
                    result = await self.primary.complete(
                        system=[{
                            "type": "text",
                            "text": system,
                            "cache_control": {"type": "ephemeral"},   # cache the prefix
                        }],
                        messages=messages,
                        max_tokens=max_tokens,
                    )

                self.breaker.record_success()
                metrics.record(
                    provider="primary",
                    input_tokens=result.usage.input_tokens,
                    cached_tokens=result.usage.cache_read_input_tokens,
                    output_tokens=result.usage.output_tokens,
                    cost_cents=cost_of(result.usage),
                )
                return result

            except RateLimitError as e:
                # Honor the server's instruction. Do not invent your own backoff.
                await asyncio.sleep(e.retry_after or (2 ** attempt) + random.random())

            except (APIError, TimeoutError) as e:
                self.breaker.record_failure()
                if attempt == 2:
                    break
                await asyncio.sleep((2 ** attempt) + random.random())

            except BadRequestError:
                raise                                 # malformed: retrying changes nothing

        if self.fallback:
            logger.warning("primary_llm_unavailable_using_fallback")
            return await self.fallback.complete(system=system, messages=messages,
                                                max_tokens=max_tokens)
        raise LLMUnavailable("primary failed and no fallback is configured")
```

**Streaming to the user while accumulating for storage:**

```python
async def stream_answer(question: str) -> AsyncIterator[str]:
    buffer = []
    async with client.stream(question) as stream:
        async for chunk in stream:
            buffer.append(chunk.text)
            yield chunk.text                       # to the user, immediately

    await store_answer("".join(buffer))            # complete, after the stream closes
```

## Notes

- Prompt caching typically reduces the cost of the cached portion by around 90% and reduces time-to-first-token substantially. A stable, cached system prompt is worth restructuring the code for.
- A circuit breaker matters more for LLM providers than for most dependencies: when they degrade, they degrade for everyone at once, and retrying through a provider-wide incident just adds latency to a certain failure.
- Cost attribution per tenant is not optional in a multi-tenant product. Without it, one customer's usage pattern can quietly consume the margin on the whole product.
