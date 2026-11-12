---
name: python-async
description: "Python asyncio — TaskGroup(구조적 동시성), aiohttp, 커넥션 풀, 동기화 primitive, uvloop, 비동기 에러 처리·디버깅. Use when Python 코드를 async 로 작성·전환하거나 asyncio 데드락·블로킹 문제를 추적할 때."
---

# Python Async Patterns

asyncio 기반 동시성 프로그래밍. TaskGroup, 커넥션 풀, 동기화, 에러 처리 패턴.

## Quick Reference

```
동시성 패턴 선택?
├── 다수 I/O 병렬 실행 ─────> asyncio.TaskGroup
├── 동시 실행 제한 ─────────> asyncio.Semaphore
├── 생산자-소비자 ──────────> asyncio.Queue
├── 이벤트 대기 ────────────> asyncio.Event
├── 공유 상태 보호 ─────────> asyncio.Lock
├── CPU-bound 병렬 ─────────> ProcessPoolExecutor
└── 타임아웃 ───────────────> asyncio.timeout (3.11+)

async 라이브러리 선택?
├── HTTP 클라이언트 ────────> aiohttp / httpx
├── PostgreSQL ─────────────> asyncpg
├── Redis ──────────────────> redis.asyncio
├── 이벤트 루프 최적화 ────> uvloop
└── 웹 프레임워크 ─────────> FastAPI (uvicorn)
```

---

## asyncio Fundamentals

### Coroutines and Tasks

```python
import asyncio

# Coroutine: async def으로 정의, await으로 실행
async def fetch_data(url: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.json()

# Task: 코루틴을 이벤트 루프에 스케줄링
async def main():
    # 순차 실행 (느림)
    result1 = await fetch_data(url1)
    result2 = await fetch_data(url2)

    # 병렬 실행 (빠름) — TaskGroup 사용 권장
    async with asyncio.TaskGroup() as tg:
        task1 = tg.create_task(fetch_data(url1))
        task2 = tg.create_task(fetch_data(url2))
    # TaskGroup 블록 종료 시 모든 task 완료 보장
    result1, result2 = task1.result(), task2.result()
```

### Event Loop

```python
# Python 3.10+: asyncio.run()만 사용
asyncio.run(main())

# 동기 → async 브릿지
def sync_wrapper():
    return asyncio.run(async_function())

# async에서 동기 코드 실행 (블로킹 회피)
async def call_sync_in_async():
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, blocking_function, arg1, arg2)
```

## TaskGroup (Python 3.11+, Structured Concurrency)

```python
import asyncio

# BAD: gather — 에러 시 나머지 task 방치
async def bad_parallel():
    results = await asyncio.gather(
        fetch(url1), fetch(url2), fetch(url3),
        return_exceptions=True,  # 에러도 결과에 포함 (놓치기 쉬움)
    )

# GOOD: TaskGroup — 에러 시 나머지 자동 취소
async def good_parallel():
    async with asyncio.TaskGroup() as tg:
        t1 = tg.create_task(fetch(url1))
        t2 = tg.create_task(fetch(url2))
        t3 = tg.create_task(fetch(url3))
    # 하나라도 실패하면 ExceptionGroup 발생
    return t1.result(), t2.result(), t3.result()

# ExceptionGroup 처리
async def handle_errors():
    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(might_fail_1())
            tg.create_task(might_fail_2())
    except* ValueError as eg:
        for exc in eg.exceptions:
            logger.error("ValueError: %s", exc)
    except* ConnectionError as eg:
        for exc in eg.exceptions:
            logger.error("ConnectionError: %s", exc)
```

### Dynamic Task Creation

```python
async def process_batch(items: list[str]) -> list[dict]:
    results: list[dict] = []

    async with asyncio.TaskGroup() as tg:
        for item in items:
            tg.create_task(process_and_collect(item, results))

    return results

async def process_and_collect(item: str, results: list[dict]) -> None:
    result = await process_item(item)
    results.append(result)
```

## aiohttp

### Client Sessions

```python
import aiohttp

# BAD: Session per request
async def bad_fetch(url: str) -> dict:
    async with aiohttp.ClientSession() as session:  # 매번 새 연결
        async with session.get(url) as resp:
            return await resp.json()

# GOOD: Shared session with connection pooling
class HttpClient:
    _session: aiohttp.ClientSession | None = None

    @classmethod
    async def start(cls) -> None:
        connector = aiohttp.TCPConnector(
            limit=100,             # 전체 커넥션 수
            limit_per_host=30,     # 호스트당 커넥션 수
            ttl_dns_cache=300,     # DNS 캐시 TTL
            keepalive_timeout=30,
        )
        cls._session = aiohttp.ClientSession(
            connector=connector,
            timeout=aiohttp.ClientTimeout(total=30),
        )

    @classmethod
    async def stop(cls) -> None:
        if cls._session:
            await cls._session.close()

    @classmethod
    async def get(cls, url: str) -> dict:
        async with cls._session.get(url) as resp:
            resp.raise_for_status()
            return await resp.json()

    @classmethod
    async def post(cls, url: str, data: dict) -> dict:
        async with cls._session.post(url, json=data) as resp:
            resp.raise_for_status()
            return await resp.json()
```

## Connection Pools

### asyncpg (PostgreSQL)

```python
import asyncpg

class Database:
    pool: asyncpg.Pool | None = None

    @classmethod
    async def connect(cls, dsn: str) -> None:
        cls.pool = await asyncpg.create_pool(
            dsn,
            min_size=10,
            max_size=50,
            max_inactive_connection_lifetime=300,
            command_timeout=30,
        )

    @classmethod
    async def disconnect(cls) -> None:
        if cls.pool:
            await cls.pool.close()

    @classmethod
    async def fetch(cls, query: str, *args) -> list[asyncpg.Record]:
        async with cls.pool.acquire() as conn:
            return await conn.fetch(query, *args)

    @classmethod
    async def execute_in_transaction(cls, queries: list[tuple[str, tuple]]) -> None:
        async with cls.pool.acquire() as conn:
            async with conn.transaction():
                for query, args in queries:
                    await conn.execute(query, *args)
```

### redis.asyncio

```python
import redis.asyncio as aioredis

class RedisPool:
    _pool: aioredis.ConnectionPool | None = None

    @classmethod
    async def connect(cls, url: str = "redis://localhost:6379") -> None:
        cls._pool = aioredis.ConnectionPool.from_url(
            url,
            max_connections=50,
            decode_responses=True,
        )

    @classmethod
    def client(cls) -> aioredis.Redis:
        return aioredis.Redis(connection_pool=cls._pool)

    @classmethod
    async def close(cls) -> None:
        if cls._pool:
            await cls._pool.disconnect()

# Usage
async def cache_user(user_id: int, data: dict) -> None:
    client = RedisPool.client()
    await client.setex(f"user:{user_id}", 3600, json.dumps(data))

async def get_cached_user(user_id: int) -> dict | None:
    client = RedisPool.client()
    data = await client.get(f"user:{user_id}")
    return json.loads(data) if data else None
```

## Synchronization Primitives

### asyncio.Lock

```python
class RateLimiter:
    def __init__(self, max_per_second: int) -> None:
        self._lock = asyncio.Lock()
        self._max = max_per_second
        self._count = 0
        self._reset_time = time.monotonic()

    async def acquire(self) -> None:
        async with self._lock:
            now = time.monotonic()
            if now - self._reset_time >= 1.0:
                self._count = 0
                self._reset_time = now
            if self._count >= self._max:
                sleep_time = 1.0 - (now - self._reset_time)
                await asyncio.sleep(sleep_time)
                self._count = 0
                self._reset_time = time.monotonic()
            self._count += 1
```

### asyncio.Semaphore

```python
# Bounded concurrency: 동시에 N개만 실행
async def fetch_all_bounded(
    urls: list[str],
    max_concurrent: int = 20,
) -> list[dict]:
    semaphore = asyncio.Semaphore(max_concurrent)

    async def bounded_fetch(url: str) -> dict:
        async with semaphore:
            return await fetch(url)

    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(bounded_fetch(url)) for url in urls]

    return [t.result() for t in tasks]
```

## Patterns

### Producer-Consumer with Queue

```python
async def producer(queue: asyncio.Queue[str], items: list[str]) -> None:
    for item in items:
        await queue.put(item)
    await queue.put(None)  # Sentinel

async def consumer(queue: asyncio.Queue[str], results: list[dict]) -> None:
    while True:
        item = await queue.get()
        if item is None:
            queue.task_done()
            break
        result = await process(item)
        results.append(result)
        queue.task_done()

async def pipeline(items: list[str], num_consumers: int = 5) -> list[dict]:
    queue: asyncio.Queue[str] = asyncio.Queue(maxsize=100)
    results: list[dict] = []

    async with asyncio.TaskGroup() as tg:
        tg.create_task(producer(queue, items))
        for _ in range(num_consumers):
            tg.create_task(consumer(queue, results))

    return results
```

### Timeout Handling (Python 3.11+)

```python
async def fetch_with_timeout(url: str, timeout_sec: float = 10.0) -> dict:
    try:
        async with asyncio.timeout(timeout_sec):
            return await fetch(url)
    except TimeoutError:
        logger.warning("Timeout fetching url=%s", url)
        return {"error": "timeout", "url": url}

# Timeout with fallback
async def fetch_with_fallback(url: str, fallback: dict) -> dict:
    try:
        async with asyncio.timeout(5.0):
            return await fetch(url)
    except (TimeoutError, aiohttp.ClientError):
        return fallback
```

### Retry with Exponential Backoff

```python
import asyncio
import random

async def retry_async(
    coro_func,
    *args,
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 30.0,
    retryable_errors: tuple = (ConnectionError, TimeoutError),
) -> Any:
    for attempt in range(max_retries + 1):
        try:
            return await coro_func(*args)
        except retryable_errors as e:
            if attempt == max_retries:
                raise
            delay = min(base_delay * (2 ** attempt), max_delay)
            jitter = random.uniform(0, delay * 0.1)
            logger.warning(
                "Retry %d/%d after %.1fs: %s",
                attempt + 1, max_retries, delay + jitter, e,
            )
            await asyncio.sleep(delay + jitter)
```

## Error Handling in Async

```python
# ExceptionGroup handling (Python 3.11+)
async def robust_batch_process(items: list[str]) -> tuple[list[dict], list[Exception]]:
    results: list[dict] = []
    errors: list[Exception] = []

    async with asyncio.TaskGroup() as tg:
        tasks = {}
        for item in items:
            task = tg.create_task(safe_process(item))
            tasks[task] = item

    for task, item in tasks.items():
        result = task.result()
        if isinstance(result, Exception):
            errors.append(result)
        else:
            results.append(result)

    return results, errors

async def safe_process(item: str) -> dict | Exception:
    try:
        return await process(item)
    except Exception as e:
        logger.error("Failed to process item=%s: %s", item, e)
        return e
```

## uvloop Optimization

> **언제 사용?** CPython + Linux/macOS + I/O bound 워크로드에서만. PyPy는 자체 asyncio가 종종 더 빠르고, Python 3.12+ asyncio도 큰 폭 개선되어 격차가 좁아졌다. Windows 미지원. 도입 전 반드시 자기 워크로드 벤치마크 후 결정.

```python
# uvloop: libuv 기반 이벤트 루프 (CPython에서 2-4x faster — 워크로드별 편차 큼)
# pip install uvloop

# Option 1: Global replacement
import uvloop
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

# Option 2: uvloop.run (Python 3.12+)
import uvloop

def main():
    uvloop.run(async_main())

# FastAPI with uvloop: uvicorn 자동 사용
# uvicorn app.main:app --loop uvloop
```

## Debugging Async

```bash
# asyncio debug mode: PYTHONASYNCIODEBUG=1 python app.py
# Or: asyncio.run(main(), debug=True)
# Detects: unawaited coroutines, slow callbacks (>100ms), unclosed resources
```

## Common Pitfalls

```python
# 1. Blocking the event loop
# BAD
async def handler():
    data = requests.get(url)           # blocks!
    time.sleep(5)                       # blocks!
    result = cpu_heavy_computation()    # blocks!

# GOOD
async def handler():
    async with aiohttp.ClientSession() as s:
        data = await s.get(url)                              # non-blocking
    await asyncio.sleep(5)                                    # non-blocking
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(None, cpu_heavy)      # offload to thread

# 2. Creating coroutine without awaiting
async def bad():
    fetch_data(url)        # coroutine created but never awaited!
    # RuntimeWarning: coroutine 'fetch_data' was never awaited

async def good():
    await fetch_data(url)  # properly awaited

# 3. Sharing mutable state without lock
counter = 0
async def increment():
    global counter
    counter += 1  # race condition in async!

# GOOD
lock = asyncio.Lock()
async def safe_increment():
    async with lock:
        global counter
        counter += 1

# 4. Fire-and-forget without tracking
async def bad_fire_and_forget():
    asyncio.create_task(background_job())  # task may be GC'd!

# GOOD: Keep reference
background_tasks: set[asyncio.Task] = set()
async def safe_fire_and_forget():
    task = asyncio.create_task(background_job())
    background_tasks.add(task)
    task.add_done_callback(background_tasks.discard)
```

## Migration from Sync to Async

```python
# Replace sync libraries with async equivalents:
# requests → aiohttp / httpx | psycopg2 → asyncpg
# redis → redis.asyncio     | open() → aiofiles

# Sync calling async:
import asyncio
def sync_function():
    return asyncio.run(async_function())

# Async calling sync (blocking):
async def async_wrapper():
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, sync_blocking_function)
```
