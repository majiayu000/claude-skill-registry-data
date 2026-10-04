---
name: asyncopenai-concurrency-httpx-pool
description: |
  Raise real concurrency in asyncio LLM batch scorers built on the OpenAI SDK
  (AsyncOpenAI, including OpenAI-compatible providers like DeepSeek). Use when:
  (1) raising an asyncio.Semaphore above ~100 produces no throughput gain,
  (2) a batch pipeline saturates near 100 in-flight requests despite a larger
  semaphore, (3) planning a high-concurrency campaign against a provider with
  no hard rate limit (DeepSeek v4-flash tolerates 2000+ in flight). Root cause:
  AsyncOpenAI's default httpx pool caps max_connections at 100, silently
  bottlenecking any larger semaphore — you must pass a custom http_client with
  httpx.Limits sized to the semaphore.
author: Claude Code
version: 1.0.0
date: 2026-07-17
---

# AsyncOpenAI Concurrency: the Hidden httpx Pool Cap

## Problem

Async batch scorers typically gate concurrency with `asyncio.Semaphore(N)`.
Raising N above ~100 silently does nothing: the OpenAI SDK's default httpx
transport caps the connection pool at `max_connections=100`, so excess tasks
queue inside httpx instead of reaching the provider. The semaphore looks like
the throttle but is not the binding constraint — there is no error, just a
throughput ceiling.

## Context / Trigger Conditions

- `asyncio.Semaphore(N)` with N > 100 around `client.chat.completions.create`
  shows the same throughput as N = 100
- Client constructed as `AsyncOpenAI(api_key=..., base_url=...)` with no
  `http_client` argument (the default transport)
- Provider is known to allow high concurrency (DeepSeek v4-flash: ~2500)
- Symptom check: requests-in-flight measured at the server never exceeds ~100

## Solution

Size the httpx pool to the semaphore when constructing the client:

```python
import httpx
from openai import AsyncOpenAI

CONCURRENCY = 2000
client = AsyncOpenAI(
    api_key=..., base_url="https://api.deepseek.com",
    http_client=httpx.AsyncClient(limits=httpx.Limits(
        max_connections=CONCURRENCY,
        max_keepalive_connections=CONCURRENCY)))
sem = asyncio.Semaphore(CONCURRENCY)
```

Both edits are required; either alone caps the other. Keep the per-request
retry loop — at high concurrency transient failures are more likely, and the
retry envelope is what turns them into non-events.

## Verification

Throughput scales with N. Verified 2026-07-17 on DeepSeek v4-flash
(deepseek-chat, JSON-mode unit scoring, ~1.5k-token prompts): at semaphore 50
a cold 13.8k-request chunk took ~70 min; at semaphore 2000 + matched pool, a
14.4k-request chunk took ~11 min (~40 req/s sustained, ~250/s burst on a
1.7k-request tail chunk), 0 failed requests, 0 schema-invalid responses.
Effective speedup ~7x rather than 40x — server-side queuing absorbs the rest —
but with zero reliability cost.

## Example

Specialist Directors US T1 campaign: final 8 chunks (100,243 calls) completed
in ~55 minutes for $8.08 after the fix, versus a projected ~9 hours at the old
setting. The edit is two lines in the scorer; the semaphore constant alone
would have been a silent no-op.

## Notes

- DeepSeek publishes no hard rate limit and handled 2000 in-flight cleanly;
  the practical ceiling reported is ~2500. Other providers enforce RPM/TPM
  caps — check before sizing.
- Windows: default asyncio proactor loop handled 2000 sockets without
  tuning; no ulimit-style adjustment needed.
- Companion ops lesson from the same campaign: when a run's *plan* changes
  scale (two-night legs -> one-shot), re-audit the launch glue's hardcoded
  limits — a wrapper `MAX-HOURS=10` safety cap sized for the old plan
  hard-killed a healthy runner at 97/108 chunks. Caps and budgets in
  supervisor scripts must be revisited whenever expected duration changes.
- Concurrency is a pure throughput knob: per-request outputs are unchanged
  (temperature 0, independent requests), so raising it mid-campaign does not
  create a scoring seam — unlike model/prompt changes, which do (see
  [llm-campaign-drift-gate]).
