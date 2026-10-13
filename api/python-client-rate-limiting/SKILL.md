---
name: python-client-rate-limiting
description: >
  Use this when an SDK calls a server that publishes a rate limit, recovering
  from a 429-amplification incident, reviewing fan-out for global-rate respect,
  or wiring Retry-After / X-RateLimit-* header handling. Covers aiolimiter
  AsyncLimiter leaky-bucket per-method scoping, Retry-After parsing
  (delta-seconds + HTTP-date), AIMD adaptive shaping on sustained 429s,
  proactive shaping from X-RateLimit-Remaining/Reset, RateLimitError surfacing,
  retry that honors server hints instead of exponential backoff, and throttle
  wait-time + 429-count OTel signals.
  Triggers: aiolimiter, AsyncLimiter, rate, throttle, 429, Retry-After, X-RateLimit, token bucket, leaky bucket, RateLimitError.
---

# python-client-rate-limiting (v1.0.0)

## Rationale

Most servers will tell you the rate limit. Most clients ignore the hint and burst until they get 429s. The Python pack pattern: assume the server will tell you (`Retry-After` header on 429), respect that hint, AND pre-emptively self-limit via a client-side token bucket so the consumer doesn't get rate-limited in the first place. The combination — proactive client-side shaping + reactive server-side honoring — keeps the SDK polite and predictable.

This skill is cited by `code-reviewer-python` (resilience review-criteria), `python-asyncio-patterns` (Rule 6 Semaphore for bounded concurrency), `python-circuit-breaker-policy` (sustained 429 → breaker open), `idempotent-retry-safety` (Retry-After honoring), `python-otel-instrumentation` (throttle metrics), and `python-sdk-config-pattern` (Config rate fields).

## Activation signals

- SDK calls a server that publishes a rate limit (REST, GraphQL, RPC).
- Production incident: SDK got 429-rate-limited and didn't back off.
- TPRD §3 declares throughput sensitivity.
- Reviewing fan-out — does it respect a global rate?
- Server documentation mentions `X-RateLimit-*` or `Retry-After`.

## Library choice

| Library | License | Async | Algorithm | Recommendation |
|---------|---------|-------|-----------|----------------|
| `aiolimiter` | MIT | Yes | Leaky bucket | DEFAULT |
| `asyncio-throttle` | MIT | Yes | Token bucket (sliding window) | Acceptable alternative |
| `slowapi` | MIT | Yes (Starlette/FastAPI) | Various | Server-side; not for client SDKs |
| `tenacity` | Apache-2.0 | Yes (retry only) | n/a | For retry-with-backoff; not rate limiting per se |

`aiolimiter` is the Python pack default: small, MIT, async-native, simple `AsyncLimiter(rate, period)` API. Always vet before adoption per `python-dependency-vetting`.

## Core algorithm — leaky bucket

`aiolimiter.AsyncLimiter(max_rate, time_period)` allows at most `max_rate` operations per `time_period` seconds. Calls await at the limiter when capacity is exhausted; once enough time elapses, capacity refills.

```python
from aiolimiter import AsyncLimiter

# 100 requests per second, sustained
limiter = AsyncLimiter(max_rate=100, time_period=1.0)

async def publish(self, msg: bytes) -> None:
    async with limiter:
        await self._http.post(...)
```

`async with limiter` blocks until a slot is free. Tight loops sustain at the configured rate; bursts are smoothed.

## Rule 1 — Per-method scoping (per `python-circuit-breaker-policy` Rule 7)

```python
class Client:
    def __init__(self, config: Config) -> None:
        self._publish_limiter = AsyncLimiter(
            max_rate=config.publish_rate_per_second,
            time_period=1.0,
        )
        self._fetch_limiter = AsyncLimiter(
            max_rate=config.fetch_rate_per_second,
            time_period=1.0,
        )
```

Different endpoints have different limits. A coarse SDK-wide limiter conflates them — slow `publish` consumes capacity that was meant for fast `fetch`.

## Rule 2 — Honor `Retry-After` from 429 responses

When the server returns 429 (Too Many Requests) with `Retry-After`, the SDK MUST wait that long before the next attempt. Whether to wait silently or surface a `RateLimitError` is a per-API choice.

```python
import asyncio
import logging

logger = logging.getLogger(__name__)


class Client:
    async def publish(self, topic: str, payload: bytes) -> None:
        async with self._publish_limiter:
            response = await self._http.post(self._url(topic), data=payload)

        if response.status_code == 429:
            retry_after = self._parse_retry_after(response)
            logger.warning("rate limited; sleeping %.2fs", retry_after)
            await asyncio.sleep(retry_after)
            # Re-attempt ONCE; further failures fall through to the caller
            async with self._publish_limiter:
                response = await self._http.post(...)
            response.raise_for_status()

    @staticmethod
    def _parse_retry_after(response) -> float:
        retry_after = response.headers.get("Retry-After")
        if retry_after is None:
            return 1.0                              # default; per HTTP spec
        try:
            return float(retry_after)               # delta-seconds
        except ValueError:
            # Could be HTTP-date; parse with email.utils
            from email.utils import parsedate_to_datetime
            target = parsedate_to_datetime(retry_after)
            return max(0.0, (target - datetime.now(target.tzinfo)).total_seconds())
```

Or surface as an exception (per `python-exception-patterns` `RateLimitError`):

```python
if response.status_code == 429:
    retry_after = self._parse_retry_after(response)
    raise RateLimitError(
        f"server rate-limited; retry after {retry_after:.2f}s",
        retry_after_s=retry_after,
    )
```

The `retry_after_s` attribute is part of `RateLimitError` from `python-exception-patterns`. Consumers catch and decide whether to sleep + retry, queue, or surface to the user.

## Rule 3 — Adaptive shaping — slow down on sustained 429

If you get 429 frequently, the configured rate is wrong. Reduce the limiter dynamically:

```python
class Client:
    async def publish(self, topic: str, payload: bytes) -> None:
        async with self._publish_limiter:
            response = await self._http.post(...)

        if response.status_code == 429:
            self._on_rate_limited()
            raise RateLimitError(...)

    def _on_rate_limited(self) -> None:
        """Halve the publish rate on 429; minimum 1/s."""
        new_rate = max(1.0, self._publish_limiter.max_rate * 0.5)
        if new_rate < self._publish_limiter.max_rate:
            logger.warning(
                "reducing publish rate %s → %s after 429",
                self._publish_limiter.max_rate, new_rate,
            )
            self._publish_limiter = AsyncLimiter(max_rate=new_rate, time_period=1.0)
```

`aiolimiter`'s rate isn't mutable in place — recreate on adjustment. Increase rate slowly back up if 429s stop:

```python
def _on_success(self) -> None:
    """Slowly increase rate after sustained success."""
    self._success_streak += 1
    if self._success_streak >= self._config.rate_recovery_threshold:
        self._success_streak = 0
        target_rate = min(
            self._config.publish_rate_per_second,
            self._publish_limiter.max_rate * 1.1,
        )
        if target_rate > self._publish_limiter.max_rate:
            self._publish_limiter = AsyncLimiter(max_rate=target_rate, time_period=1.0)
```

This is "additive increase, multiplicative decrease" (AIMD) — TCP-style congestion control adapted for HTTP rate limiting.

## Rule 4 — Honor `X-RateLimit-*` proactive headers

Many APIs return per-response headers describing the current limit:

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 23
X-RateLimit-Reset: 1700000000   # Unix timestamp
```

A polite SDK reads these and shapes itself BEFORE hitting 429:

```python
async def publish(self, topic: str, payload: bytes) -> None:
    async with self._publish_limiter:
        response = await self._http.post(...)

    self._update_from_headers(response)

def _update_from_headers(self, response) -> None:
    remaining = response.headers.get("X-RateLimit-Remaining")
    reset = response.headers.get("X-RateLimit-Reset")
    if remaining is None or reset is None:
        return

    remaining_i = int(remaining)
    reset_i = int(reset)
    seconds_until_reset = max(1.0, reset_i - time.time())

    if remaining_i < 5:
        # Close to limit; throttle proactively to avoid 429
        new_rate = remaining_i / seconds_until_reset
        if new_rate < self._publish_limiter.max_rate:
            logger.info(
                "approaching rate limit (%d remaining, %.0fs until reset); "
                "shaping to %.2f/s",
                remaining_i, seconds_until_reset, new_rate,
            )
            self._publish_limiter = AsyncLimiter(max_rate=new_rate, time_period=1.0)
```

Headers are advisory and not standardized — different APIs use `RateLimit-*` (RFC 9237 draft), `X-RateLimit-*` (de facto), or `X-Rate-Limit-*` (variant). The SDK's parser should accept the variants the target server uses; document which ones.

## Rule 5 — Combine with retry — but don't multiply

```python
import random

async def publish_with_retry(self, topic: str, payload: bytes) -> None:
    max_retries = self._config.max_retries
    for attempt in range(max_retries + 1):
        try:
            async with self._publish_limiter:
                response = await self._http.post(self._url(topic), data=payload)

            if response.status_code == 429:
                retry_after = self._parse_retry_after(response)
                self._on_rate_limited()
                if attempt < max_retries:
                    await asyncio.sleep(retry_after)        # honor server hint
                    continue
                raise RateLimitError(
                    "rate limit exhausted after retries",
                    retry_after_s=retry_after,
                )

            response.raise_for_status()
            self._on_success()
            return

        except (NetworkError, SDKTimeoutError):
            if attempt >= max_retries:
                raise
            delay = (2 ** attempt) * 0.1 + random.uniform(0, 0.05)
            await asyncio.sleep(delay)
```

The retry loop honors `Retry-After` for 429 (server's hint) and exponential backoff for network failures (no hint). NEVER blindly retry 429 with exponential backoff — the server told you when to come back.

## Rule 6 — Observe rate-limit signals

```python
from opentelemetry import metrics

meter = metrics.get_meter(__name__)
rate_limited_counter = meter.create_counter(
    name="motadata.rate_limited",
    description="Count of 429 responses received",
)
throttle_wait_histogram = meter.create_histogram(
    name="motadata.throttle.wait",
    unit="s",
    description="Time spent waiting at the client-side limiter",
)
```

Operators see rate-limit incidents (`rate_limited_counter`) and proactive shaping cost (`throttle_wait`). Sustained `rate_limited` events → tune `Config.publish_rate_per_second` down. Persistent `throttle_wait` → either rate is OK (proactive shaping is working) or operator wants to raise it.

To capture wait time at the limiter:

```python
import time
async def _bounded_publish(self, topic: str, payload: bytes) -> None:
    start = time.perf_counter()
    async with self._publish_limiter:
        wait_s = time.perf_counter() - start
        throttle_wait_histogram.record(wait_s, {"endpoint": "publish"})
        await self._http.post(...)
```

## Rule 7 — Test the rate limit holds

```python
import asyncio
import pytest

async def test_publisher_respects_rate(client: Client) -> None:
    """100 requests against a 10/s limit should take ~10 seconds."""
    cfg = Config(publish_rate_per_second=10, ...)
    async with Client(cfg) as c:
        start = asyncio.get_event_loop().time()
        await asyncio.gather(*[c.publish("t", b"x") for _ in range(100)])
        elapsed = asyncio.get_event_loop().time() - start
        assert 9.0 < elapsed < 12.0       # 100 / 10/s = 10s, with slop


async def test_honors_retry_after(respx_mock) -> None:
    cfg = Config(publish_rate_per_second=1000, ...)  # rate not the issue here
    respx_mock.post("...").mock(
        return_value=httpx.Response(429, headers={"Retry-After": "2"}),
    )
    async with Client(cfg) as c:
        with pytest.raises(RateLimitError) as exc_info:
            await c.publish("t", b"x")
        assert exc_info.value.retry_after_s == 2.0
```

Keep test rates LOW (10/s, not 100k/s) — a flaky test under high CPU contention is worse than a slow test.

## Rule 8 — Config exposes the knobs

```python
@dataclass(frozen=True, slots=True, kw_only=True)
class Config:
    base_url: str
    api_key: str
    publish_rate_per_second: int = 100
    fetch_rate_per_second: int = 200
    rate_recovery_threshold: int = 50         # successes before increasing rate
    rate_max_retries: int = 3                 # retries on 429 before giving up
```

`publish_rate_per_second = 0` SHOULD disable the limiter (consumer has their own throttling):

```python
self._publish_limiter = (
    None
    if config.publish_rate_per_second <= 0
    else AsyncLimiter(max_rate=config.publish_rate_per_second, time_period=1.0)
)

async def publish(self, topic: str, payload: bytes) -> None:
    if self._publish_limiter is not None:
        async with self._publish_limiter:
            return await self._do_publish(topic, payload)
    return await self._do_publish(topic, payload)
```

## GOOD: full client method with rate limiting + retry + adaptive shaping

```python
import asyncio
import logging
import random
import time
from email.utils import parsedate_to_datetime
from datetime import datetime

from aiolimiter import AsyncLimiter
from opentelemetry import metrics

from motadatapysdk.errors import (
    MotadataError, NetworkError, RateLimitError, SDKTimeoutError, ServerError,
)

logger = logging.getLogger(__name__)
meter = metrics.get_meter(__name__)
rate_limited_counter = meter.create_counter(
    "motadata.rate_limited", description="429 responses received"
)
throttle_wait_histogram = meter.create_histogram(
    "motadata.throttle.wait", unit="s", description="Limiter wait time"
)


class Client:
    def __init__(self, config: Config) -> None:
        self._config = config
        self._publish_limiter: AsyncLimiter | None = (
            None if config.publish_rate_per_second <= 0
            else AsyncLimiter(config.publish_rate_per_second, 1.0)
        )
        self._success_streak = 0

    async def publish(self, topic: str, payload: bytes) -> None:
        for attempt in range(self._config.max_retries + 1):
            try:
                if self._publish_limiter is not None:
                    start = time.perf_counter()
                    async with self._publish_limiter:
                        wait_s = time.perf_counter() - start
                        throttle_wait_histogram.record(wait_s, {"endpoint": "publish"})
                        response = await self._http.post(self._url(topic), data=payload)
                else:
                    response = await self._http.post(self._url(topic), data=payload)

                if response.status_code == 429:
                    rate_limited_counter.add(1, {"endpoint": "publish"})
                    retry_after = self._parse_retry_after(response)
                    self._on_rate_limited()
                    if attempt < self._config.max_retries:
                        await asyncio.sleep(retry_after)
                        continue
                    raise RateLimitError(
                        f"rate limit exhausted after {attempt + 1} attempts",
                        retry_after_s=retry_after,
                    )

                response.raise_for_status()
                self._on_success()
                self._update_from_headers(response)
                return

            except (NetworkError, SDKTimeoutError):
                if attempt >= self._config.max_retries:
                    raise
                delay = (2 ** attempt) * 0.1 + random.uniform(0, 0.05)
                await asyncio.sleep(delay)

    def _on_rate_limited(self) -> None:
        if self._publish_limiter is None:
            return
        new_rate = max(1.0, self._publish_limiter.max_rate * 0.5)
        if new_rate < self._publish_limiter.max_rate:
            logger.warning(
                "reducing publish rate %s → %s after 429",
                self._publish_limiter.max_rate, new_rate,
            )
            self._publish_limiter = AsyncLimiter(new_rate, 1.0)
        self._success_streak = 0

    def _on_success(self) -> None:
        if self._publish_limiter is None:
            return
        self._success_streak += 1
        if self._success_streak >= self._config.rate_recovery_threshold:
            self._success_streak = 0
            target = min(
                self._config.publish_rate_per_second,
                self._publish_limiter.max_rate * 1.1,
            )
            if target > self._publish_limiter.max_rate:
                self._publish_limiter = AsyncLimiter(target, 1.0)

    @staticmethod
    def _parse_retry_after(response) -> float:
        ra = response.headers.get("Retry-After")
        if ra is None:
            return 1.0
        try:
            return float(ra)
        except ValueError:
            target = parsedate_to_datetime(ra)
            return max(0.0, (target - datetime.now(target.tzinfo)).total_seconds())
```

Demonstrates: per-method limiter (Rule 1), Retry-After honored (Rule 2), adaptive shaping AIMD (Rule 3), throttle observation (Rule 6), Config-driven (Rule 8), retry distinguished from 429 retry.

## BAD anti-patterns

```python
# 1. No client-side limit; rely on 429 alone
async def publish(self, topic, payload):
    response = await self._http.post(...)        # bursts until throttled
    if response.status_code == 429:
        await asyncio.sleep(1)                    # blind retry; ignores Retry-After

# 2. Coarse SDK-wide limiter
limiter = AsyncLimiter(100, 1.0)                  # publish + fetch share capacity
# slow publish blocks fast fetch

# 3. New limiter per call
async def publish(self, topic, payload):
    limiter = AsyncLimiter(100, 1.0)              # state per-call → no rate effect

# 4. Ignore Retry-After
async def publish(self, topic, payload):
    response = await self._http.post(...)
    if response.status_code == 429:
        await asyncio.sleep(1)                    # always 1s; ignores server's hint

# 5. Exponential backoff on 429
if response.status_code == 429:
    delay = 2 ** attempt + random.random()        # could be much longer than Retry-After
    await asyncio.sleep(delay)

# 6. Limiter outside async with
asyncio.create_task(limiter.acquire())            # not paired with release; leaks tokens

# 7. Test asserts exact ms timing
elapsed = ...
assert elapsed == 10.0                           # flaky; tolerate slop

# 8. Mutable max_rate field (some libraries forbid)
limiter.max_rate = new_rate                      # may not propagate; recreate instead

# 9. No metric on throttle wait
# Operator can't tell if rate is the bottleneck

# 10. Retry-After as integer-only
return int(response.headers["Retry-After"])      # may be HTTP-date; raises ValueError
```

## Cross-references

- `python-asyncio-patterns` Rule 6 (Semaphore) — bounded concurrency complement.
- `python-exception-patterns` (`RateLimitError` extends `MotadataError`).
- `python-circuit-breaker-policy` — sustained 429 should also trigger breaker.
- `python-otel-instrumentation` — throttle counter + histogram.
- `python-sdk-config-pattern` — rate config fields with 0=disabled.
- `python-dependency-vetting` — vet `aiolimiter` before adoption.
- `idempotent-retry-safety` — Retry-After honored when retrying.
- `network-error-classification` — 429 is retriable with hint; 500 is retriable with backoff.
