---
name: httpx-tenacity-asyncio
description: >-
  Use for designing or reviewing resilient asynchronous HTTP call paths that combine
  HTTPX, Tenacity, and asyncio: client lifetime, time budgets, retry eligibility,
  backoff, concurrency, cancellation, and idempotency. Do not use for generic HTTPX,
  retry, or asyncio questions that do not cross these boundaries.
---

# HTTPX + Tenacity + asyncio boundaries

Make the whole call path bounded, cancellation-safe, and semantically retryable. A
retry loop is not resilience when each attempt has an unbounded timeout, duplicates a
side effect, or overwhelms the connection pool.

Inspect the installed version of HTTPX, Tenacity, and Python and their signatures before
encoding version-sensitive exception, timeout, or cancellation behavior.

## Establish the contract

Before coding, identify:

- operation semantics: read, idempotent write, or non-idempotent write;
- end-to-end deadline and per-attempt connect/read/write/pool budgets;
- retryable failures defined by the remote protocol, not by `Exception`;
- maximum concurrency, connection-pool limits, and upstream rate limit;
- cancellation and shutdown behavior;
- idempotency key or deduplication mechanism for retryable writes.

If those facts are unknown, inspect the upstream API contract before adding retries.

## Execution model

1. Reuse one `httpx.AsyncClient` for the service lifetime. Do not create a client per
   request in a hot path.
2. Bound HTTPX connect, read, write, and pool waits. Bound the complete operation with
   an outer deadline when several attempts must share one budget.
3. Use Tenacity's `AsyncRetrying`; never block the event loop with `time.sleep` or a
   synchronous client.
4. Retry only transient transport failures and explicitly retryable status codes such
   as 429 or selected 5xx responses. Honor `Retry-After` where supported.
5. Propagate `asyncio.CancelledError`. Cancellation is control flow, not a transient
   remote failure.
6. Limit concurrency independently from connection-pool capacity. A semaphore is an
   admission control, not a timeout.
7. Close the client during application shutdown after in-flight ownership is clear.

Read [budgets.md](references/budgets.md) for deadline allocation,
[retry-semantics.md](references/retry-semantics.md) for eligibility, and
[lifecycle.md](references/lifecycle.md) for client and task ownership.

## Canonical shape

```python
import asyncio

import httpx
from tenacity import AsyncRetrying, retry_if_exception_type, stop_after_attempt
from tenacity import wait_random_exponential


async def fetch_json(client: httpx.AsyncClient, url: str) -> object:
    async with asyncio.timeout(12):
        async for attempt in AsyncRetrying(
            stop=stop_after_attempt(3),
            wait=wait_random_exponential(multiplier=0.2, max=2),
            retry=retry_if_exception_type(
                (httpx.ConnectError, httpx.ConnectTimeout, httpx.ReadTimeout)
            ),
            reraise=True,
        ):
            with attempt:
                response = await client.get(url)
                response.raise_for_status()
                return response.json()
    raise AssertionError("retry loop returned no result")
```

Do not copy this exception set blindly. For example, retrying a `ReadTimeout` after a
write may duplicate a side effect because the server might have committed it before
the response was lost.

## Completion checks

- Tests cover success, terminal 4xx, retryable failure then success, exhausted budget,
  and task cancellation.
- A retryable write has an idempotency contract.
- Total attempts and latency cannot exceed the stated budget except for bounded
  scheduler delay.
- Concurrency and pool limits are explicit and observability records attempts without
  leaking credentials or bodies.
- No blocking sleep or synchronous network call remains on the async path.
