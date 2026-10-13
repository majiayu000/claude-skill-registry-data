---
name: python-connection-pool-tuning
description: >
  Use this when a Python SDK uses aiohttp / httpx / asyncpg / redis / aiokafka,
  recovering from a pool-exhaustion incident, sizing a pool for a declared
  throughput target, or hitting file-descriptor exhaustion at scale. Covers the
  ceil(rps × p99_latency) sizing heuristic, per-library Config-driven mappings
  (TCPConnector limit / limit_per_host, asyncpg min_size / max_size /
  max_inactive_connection_lifetime, redis max_connections / health_check_interval,
  httpx Limits, aiokafka max_in_flight_requests), PoolExhaustedError on
  acquire-timeout instead of silent block, pool-depth observable gauges,
  __aexit__ close ordering, cloud-DB idle-recycle / pre-ping, fork-safe
  post-fork construction, and DNS TTL tuning.
  Triggers: TCPConnector, create_pool, ConnectionPool, max_connections, min_size, max_size, pool_recycle, pool_pre_ping, idle, exhaustion, PoolExhaustedError.
---

# python-connection-pool-tuning (v1.0.0)

## Rationale

Default pool sizes are wrong for SDK code:
- `aiohttp.TCPConnector()` → `limit=100`, `limit_per_host=0` (unlimited per host) — fan-out can saturate the host's port table.
- `asyncpg.create_pool()` → `min_size=10, max_size=10` (fixed at 10) — doesn't scale up under load.
- `redis.asyncio.ConnectionPool()` → `max_connections=10` (default) — generous for some workloads, tight for others.
- `aiokafka.AIOKafkaProducer` → no explicit pool concept; one producer = one connection.

Each library's `Config` knob is named differently. The Python pack's convention: declare per-pool sizing in the SDK's `Config` (typed; not library-leak), translate to library-specific settings in the constructor, and emit pool metrics. Pool exhaustion raises a typed `PoolExhaustedError` rather than blocking forever.

This skill is cited by `code-reviewer-python` (resilience review-criteria), `python-asyncio-patterns` (Semaphore as concurrency cap analog), `python-asyncio-leak-prevention` (pool close in `__aexit__`), `python-otel-instrumentation` (pool depth metrics), `python-sdk-config-pattern` (Config pool fields).

## Activation signals

- SDK uses an HTTP / DB / Redis / Kafka client.
- TPRD §3 declares throughput / concurrency target.
- Production incident: pool exhaustion blocked the entire client.
- Reviewing default pool size — does it match the workload?
- File-descriptor exhaustion at scale.

## Sizing heuristic

```
max_connections = ceil(throughput_per_second × p99_latency_seconds)
min_connections = ceil(max_connections × 0.1)         # 10% warm
idle_timeout_s  = 300                                  # 5 min, longer than typical inter-request gap
healthcheck_interval_s = 30                            # ping idle conns to detect dead pools
```

Worked example: 500 RPS at p99 of 200ms → `max = ceil(500 × 0.2) = 100`. Round up for headroom: `max_connections = 128`. Warm pool: `min = 16`.

This is a STARTING point. Tune by watching pool depth + exhaustion-error rate in production. Document the heuristic in the Config docstring.

## Library mapping

### aiohttp

```python
import aiohttp

@dataclass(frozen=True, slots=True, kw_only=True)
class Config:
    base_url: str
    pool_max: int = 128
    pool_max_per_host: int = 32
    pool_keepalive_s: float = 30.0
    pool_idle_timeout_s: float = 300.0
    pool_dns_ttl_s: float = 10.0


def make_aiohttp_connector(config: Config) -> aiohttp.TCPConnector:
    return aiohttp.TCPConnector(
        limit=config.pool_max,
        limit_per_host=config.pool_max_per_host,
        keepalive_timeout=config.pool_keepalive_s,
        ttl_dns_cache=config.pool_dns_ttl_s,
        force_close=False,                   # reuse connections
        enable_cleanup_closed=True,          # reap closed-but-not-released
    )
```

`limit_per_host` is critical for SDKs talking to ONE host — without it, a single `base_url` can monopolize the pool budget.

`enable_cleanup_closed=True` (recommended; default False) catches a known aiohttp bug where TLS connections sometimes leave residual sockets after server-side close; the cleanup task reaps them.

### asyncpg

```python
import asyncpg

@dataclass(frozen=True, slots=True, kw_only=True)
class Config:
    db_dsn: str
    db_pool_min: int = 4
    db_pool_max: int = 32
    db_pool_max_inactive_lifetime_s: float = 300.0
    db_pool_command_timeout_s: float = 5.0


async def make_asyncpg_pool(config: Config) -> asyncpg.Pool:
    return await asyncpg.create_pool(
        dsn=config.db_dsn,
        min_size=config.db_pool_min,
        max_size=config.db_pool_max,
        max_inactive_connection_lifetime=config.db_pool_max_inactive_lifetime_s,
        command_timeout=config.db_pool_command_timeout_s,
    )
```

`max_inactive_connection_lifetime` (default 300s) recycles idle connections — essential for cloud Postgres (RDS, Cloud SQL) which often kills idle conns after 30 min.

`command_timeout` is per-statement, not per-connection-acquire — prevents a runaway query from holding a pool slot forever.

asyncpg has no built-in pool-acquisition timeout; wrap the acquire:

```python
import asyncio

async def get_conn_or_fail(pool: asyncpg.Pool, *, timeout_s: float) -> asyncpg.Connection:
    try:
        async with asyncio.timeout(timeout_s):
            return await pool.acquire()
    except builtins.TimeoutError as e:
        raise PoolExhaustedError("asyncpg pool exhausted") from e
```

### redis (redis-py >= 5.0 async)

```python
import redis.asyncio as redis

@dataclass(frozen=True, slots=True, kw_only=True)
class Config:
    redis_url: str
    redis_pool_max: int = 50
    redis_pool_socket_keepalive: bool = True
    redis_pool_health_check_interval: float = 30.0


def make_redis_pool(config: Config) -> redis.ConnectionPool:
    return redis.ConnectionPool.from_url(
        config.redis_url,
        max_connections=config.redis_pool_max,
        socket_keepalive=config.redis_pool_socket_keepalive,
        health_check_interval=config.redis_pool_health_check_interval,
        decode_responses=False,
    )

# Then in the client:
redis_pool = make_redis_pool(config)
self._redis = redis.Redis(connection_pool=redis_pool)
```

`health_check_interval=30` triggers a ping on idle connections, catching dead pools before they're handed back to the caller.

`max_connections` enforced at acquire-time; exceeded → `redis.exceptions.ConnectionError`. Wrap in `PoolExhaustedError`:

```python
try:
    async with self._redis.client() as client:
        await client.set("k", b"v")
except redis.exceptions.ConnectionError as e:
    if "Too many connections" in str(e):
        raise PoolExhaustedError("redis pool exhausted") from e
    raise
```

### httpx

```python
import httpx

@dataclass(frozen=True, slots=True, kw_only=True)
class Config:
    base_url: str
    http_pool_max_keepalive: int = 20
    http_pool_max: int = 128
    http_pool_keepalive_s: float = 30.0


def make_httpx_client(config: Config, *, ssl_ctx: ssl.SSLContext | None = None) -> httpx.AsyncClient:
    limits = httpx.Limits(
        max_keepalive_connections=config.http_pool_max_keepalive,
        max_connections=config.http_pool_max,
        keepalive_expiry=config.http_pool_keepalive_s,
    )
    return httpx.AsyncClient(
        base_url=config.base_url,
        limits=limits,
        verify=ssl_ctx if ssl_ctx is not None else True,
    )
```

`max_keepalive_connections` < `max_connections` — keepalive is a SUBSET of total. Beyond keepalive, connections are short-lived (closed after one request).

httpx blocks at acquire when pool is full, but you can layer a Semaphore + timeout for explicit `PoolExhaustedError`:

```python
self._pool_sem = asyncio.Semaphore(config.http_pool_max)

async def request(self, method: str, url: str, **kwargs) -> httpx.Response:
    try:
        async with asyncio.timeout(config.pool_acquire_timeout_s):
            async with self._pool_sem:
                return await self._http.request(method, url, **kwargs)
    except builtins.TimeoutError as e:
        raise PoolExhaustedError("http pool exhausted") from e
```

### aiokafka

```python
from aiokafka import AIOKafkaProducer

@dataclass(frozen=True, slots=True, kw_only=True)
class Config:
    kafka_bootstrap: str
    kafka_max_in_flight_requests: int = 5
    kafka_send_buffer_bytes: int = 33554432             # 32 MiB
    kafka_request_timeout_ms: int = 5000


async def make_kafka_producer(config: Config) -> AIOKafkaProducer:
    return AIOKafkaProducer(
        bootstrap_servers=config.kafka_bootstrap,
        max_in_flight_requests_per_connection=config.kafka_max_in_flight_requests,
        send_buffer_bytes=config.kafka_send_buffer_bytes,
        request_timeout_ms=config.kafka_request_timeout_ms,
    )
```

aiokafka's pool concept is INFLIGHT requests, not connections (it maintains one connection per broker). `max_in_flight_requests_per_connection` caps unacked in-flight; default 5 is conservative; increase to 100+ for high-throughput producers (with idempotent=True for ordering guarantees).

## Rule 1 — `PoolExhaustedError` is the surface

```python
from motadatapysdk.errors import MotadataError


class PoolExhaustedError(MotadataError):
    """A connection pool reached its capacity and a new acquisition timed out.

    The caller's options:
    1. Catch and wait + retry.
    2. Catch and route to a different client / pool.
    3. Catch and surface to the user with backpressure.

    Indicates either: (a) the SDK is over-loaded for its pool size,
    or (b) the downstream is slow and connections are tied up.
    """
```

Surface at every pool-acquisition path. The exception's `__cause__` carries the library-specific underlying error (`asyncio.TimeoutError`, `redis.exceptions.ConnectionError`, `asyncpg.PoolError`).

## Rule 2 — Pool depth observable

```python
from opentelemetry import metrics

meter = metrics.get_meter(__name__)


class Client:
    def __init__(self, config: Config) -> None:
        self._pool: asyncpg.Pool | None = None

        meter.create_observable_gauge(
            "motadata.db.pool.size",
            callbacks=[self._observe_pool_size],
            description="Currently held connections (busy + idle)",
        )
        meter.create_observable_gauge(
            "motadata.db.pool.idle",
            callbacks=[self._observe_pool_idle],
            description="Currently idle connections",
        )

    def _observe_pool_size(self, options) -> Iterable[metrics.Observation]:
        if self._pool is None:
            return []
        return [metrics.Observation(self._pool.get_size())]

    def _observe_pool_idle(self, options) -> Iterable[metrics.Observation]:
        if self._pool is None:
            return []
        return [metrics.Observation(self._pool.get_idle_size())]
```

Operators graph `pool.size` over time:
- Constantly at `max_size` → pool is undersized; raise `pool_max`.
- Constantly at `min_size` with `idle ~ size` → pool is oversized; lower `min_size` for memory.
- Spiky between `min` and `max` → bursty traffic; the pool is correctly absorbing burst.

asyncpg exposes `get_size()` and `get_idle_size()`; redis exposes `pool.connection_kwargs`; httpx 0.27+ exposes `httpx.AsyncClient._transport._pool` (private; use Semaphore counter as proxy).

## Rule 3 — Pool close on `__aexit__`

```python
class Client:
    async def __aexit__(self, exc_type, exc_val, tb) -> None:
        if self._pool is not None:
            await self._pool.close()                # asyncpg
            self._pool = None
        if self._redis is not None:
            await self._redis.aclose()              # redis-py 5.x
            self._redis = None
        if self._http is not None:
            await self._http.aclose()
            self._http = None
```

Per `python-asyncio-leak-prevention`, every pool ends on every exit path. Without explicit close, GC may run the destructor while the event loop is closed → `RuntimeError: Event loop is closed`.

## Rule 4 — Pool pre-ping for cloud DBs

Cloud DBs (RDS, Cloud SQL, Aurora) often terminate idle connections silently. The SDK MUST detect this BEFORE handing a stale connection to the caller.

```python
# asyncpg: max_inactive_connection_lifetime triggers reconnect
asyncpg.create_pool(
    ...,
    max_inactive_connection_lifetime=300.0,         # < cloud's idle kill of 1800s
)
```

```python
# SQLAlchemy: pool_pre_ping=True (slight latency cost; worth it)
from sqlalchemy.ext.asyncio import create_async_engine
engine = create_async_engine(
    config.db_dsn,
    pool_pre_ping=True,
    pool_recycle=300,
)
```

```python
# redis-py: health_check_interval pings idle conns
redis.ConnectionPool.from_url(..., health_check_interval=30.0)
```

`max_inactive_connection_lifetime` should be < the cloud's idle-kill timeout. AWS RDS: default `tcp_keepalives_idle = 7200s`; aggressive deployments set `5min`. Always less.

## Rule 5 — Don't share pools across processes

```python
# WRONG — pool initialized at module import; survives fork
_pool: asyncpg.Pool | None = None

async def get_pool() -> asyncpg.Pool:
    global _pool
    if _pool is None:
        _pool = await asyncpg.create_pool(...)
    return _pool

# After multiprocessing.fork(): both parent + child share file descriptors;
# concurrent pool ops corrupt asyncpg state.
```

In multi-process deployments (Gunicorn workers, multiprocessing pool, Celery), each process MUST construct its own pool POST-FORK. Provide a `Client.fork_safe_init()` or document that the Client is constructed inside `worker_init` hooks:

```python
# Gunicorn worker init
def post_fork(server, worker):
    """Per-worker init."""
    global client
    client = Client(Config(...))                # constructed AFTER fork
```

This is a classic Python deployment footgun. Document in the Client's class docstring.

## Rule 6 — `asyncio.Semaphore` as portable concurrency cap

If the SDK wraps multiple pool-using clients, a top-level `asyncio.Semaphore` enforces a shared cap regardless of per-pool sizes:

```python
class Client:
    def __init__(self, config: Config) -> None:
        self._global_inflight = asyncio.Semaphore(config.global_max_inflight)

    async def call(self, ...) -> ...:
        async with self._global_inflight:
            return await self._do_call(...)
```

Useful for memory-pressure caps that span HTTP + DB + Redis. Per `python-asyncio-patterns` Rule 6.

## Rule 7 — Test pool exhaustion

```python
import asyncio
import pytest

async def test_pool_exhaustion_raises_typed_error(client_factory) -> None:
    cfg = Config(http_pool_max=2, pool_acquire_timeout_s=0.1, ...)
    async with client_factory(cfg) as client:
        # Hold 2 connections; third should exhaust
        async with client._pool_sem, client._pool_sem:    # block both
            with pytest.raises(PoolExhaustedError):
                await client.request("GET", "/")
```

For asyncpg / redis / aiokafka, mocking pool exhaustion needs a slow downstream (the test holds connections for `timeout` + epsilon). Use a small `pool_max` + parallel calls + a tiny `acquire_timeout`.

## Rule 8 — DNS caching pitfalls

aiohttp caches DNS for `ttl_dns_cache=10` by default. For load-balanced backends with short DNS TTLs, this causes the SDK to keep hitting a stale IP after rebalance:

```python
aiohttp.TCPConnector(
    ttl_dns_cache=10,                          # 10s; respects backend's DNS TTL
    use_dns_cache=True,
)
```

Tradeoff: lower TTL = more DNS queries but faster failover; higher TTL = fewer queries but slower failover. Match backend's DNS TTL.

For multi-IP backends, also set `family=0` (default) to allow IPv4 + IPv6.

## GOOD: full client with all pools

```python
from __future__ import annotations

import asyncio
import contextlib
import ssl
from collections.abc import Iterable
from dataclasses import dataclass, field
from typing import Self

import aiohttp
import asyncpg
import redis.asyncio as redis
from opentelemetry import metrics

from motadatapysdk.errors import PoolExhaustedError, MotadataError

meter = metrics.get_meter(__name__)


@dataclass(frozen=True, slots=True, kw_only=True)
class Config:
    base_url: str
    db_dsn: str
    redis_url: str

    http_pool_max: int = 128
    http_pool_max_per_host: int = 32
    http_pool_keepalive_s: float = 30.0
    http_pool_acquire_timeout_s: float = 5.0

    db_pool_min: int = 4
    db_pool_max: int = 32
    db_pool_idle_lifetime_s: float = 300.0
    db_pool_command_timeout_s: float = 5.0

    redis_pool_max: int = 50
    redis_pool_health_check_s: float = 30.0


class Client:
    def __init__(self, config: Config) -> None:
        self._config = config
        self._http: aiohttp.ClientSession | None = None
        self._db_pool: asyncpg.Pool | None = None
        self._redis: redis.Redis | None = None
        self._closed = False

        meter.create_observable_gauge(
            "motadata.db.pool.size",
            callbacks=[self._observe_db_pool_size],
        )

    async def __aenter__(self) -> Self:
        connector = aiohttp.TCPConnector(
            limit=self._config.http_pool_max,
            limit_per_host=self._config.http_pool_max_per_host,
            keepalive_timeout=self._config.http_pool_keepalive_s,
            enable_cleanup_closed=True,
        )
        self._http = aiohttp.ClientSession(connector=connector)

        self._db_pool = await asyncpg.create_pool(
            dsn=self._config.db_dsn,
            min_size=self._config.db_pool_min,
            max_size=self._config.db_pool_max,
            max_inactive_connection_lifetime=self._config.db_pool_idle_lifetime_s,
            command_timeout=self._config.db_pool_command_timeout_s,
        )

        redis_pool = redis.ConnectionPool.from_url(
            self._config.redis_url,
            max_connections=self._config.redis_pool_max,
            health_check_interval=self._config.redis_pool_health_check_s,
        )
        self._redis = redis.Redis(connection_pool=redis_pool)
        return self

    async def __aexit__(self, exc_type, exc_val, tb) -> None:
        if self._closed:
            return
        self._closed = True
        if self._http is not None:
            await self._http.close()
            self._http = None
        if self._db_pool is not None:
            await self._db_pool.close()
            self._db_pool = None
        if self._redis is not None:
            await self._redis.aclose()
            self._redis = None

    async def db_query(self, query: str, *args) -> list[asyncpg.Record]:
        if self._db_pool is None:
            raise RuntimeError("client not entered")
        try:
            async with asyncio.timeout(self._config.http_pool_acquire_timeout_s):
                async with self._db_pool.acquire() as conn:
                    return await conn.fetch(query, *args)
        except builtins.TimeoutError as e:
            raise PoolExhaustedError("asyncpg pool exhausted") from e

    def _observe_db_pool_size(self, options) -> Iterable[metrics.Observation]:
        if self._db_pool is None:
            return []
        return [metrics.Observation(self._db_pool.get_size())]
```

Demonstrates: per-pool sizing in Config (Rule 1), aiohttp + asyncpg + redis integrated (Library mapping), `PoolExhaustedError` on acquire timeout (Rule 1), pool depth observable (Rule 2), close in `__aexit__` (Rule 3), idle-lifetime recycle (Rule 4).

## BAD anti-patterns

```python
# 1. Default pool sizes
async with aiohttp.ClientSession() as session: ...
# limit=100, limit_per_host=0 — single host can monopolize

# 2. Module-level pool init (fork-unsafe)
_pool = asyncio.run(asyncpg.create_pool(...))    # crashes after fork

# 3. No idle-lifetime recycling
asyncpg.create_pool(..., max_inactive_connection_lifetime=0.0)
# cloud DB silently kills conns; SDK gets stale handles

# 4. Block forever on pool acquire
async with self._db_pool.acquire() as conn:      # no timeout; one slow query holds N callers

# 5. Catch ConnectionError as success
try:
    async with pool.acquire() as conn: ...
except redis.exceptions.ConnectionError:
    pass                                          # operator can't see exhaustion

# 6. Pool not closed
self._db_pool = await asyncpg.create_pool(...)
# missing await self._db_pool.close()  in __aexit__

# 7. Pool size pinned regardless of workload
DB_MAX = 10                                       # works for low traffic; fails at 1000 RPS

# 8. health_check_interval=0 (off) on cloud Redis
redis.ConnectionPool.from_url(..., health_check_interval=0)
# stale conns linger; first request after idle cycles fails

# 9. limit_per_host unset for single-host SDK
aiohttp.TCPConnector(limit=100)                   # all 100 may go to one host

# 10. No OTel pool metric
# Operator can't tune; flying blind on sizing
```

## Cross-references

- `python-asyncio-patterns` Rule 6 (Semaphore for global cap).
- `python-asyncio-leak-prevention` (close pool in `__aexit__`).
- `python-client-shutdown-lifecycle` (ordered teardown — pool last).
- `python-otel-instrumentation` (pool depth observable).
- `python-sdk-config-pattern` (per-pool Config fields).
- `python-exception-patterns` (`PoolExhaustedError` extends `MotadataError`).
- `python-client-tls-configuration` — TCPConnector takes `ssl=` from TLS skill.
- `network-error-classification` (shared) — pool exhaustion vs network failure.
