---
name: async-python
description: Python async/await patterns with asyncio, concurrent.futures, threading, and multiprocessing. Covers async context managers, timeouts, cancellation, common pitfalls (blocking in async, missing await, event loop issues), and choosing between async/threading/multiprocessing. Use when writing async code, debugging async issues, choosing concurrency approaches, or testing async functions.
allowed-tools:
  - Read
  - Bash
  - Grep
---

# Python Async/Await Patterns

**Purpose:** Guide async Python development with clear patterns, pitfall avoidance, and concurrency strategy selection.

**When to use:** Writing async code, debugging async issues, choosing between async/threading/multiprocessing, testing async functions.

**For detailed examples and advanced patterns:** See reference.md

---

## Core Principles

1. **Async is for I/O, not CPU** - Use async for network/disk, not heavy computation
2. **Never block the event loop** - Blocking calls kill async performance
3. **await everything awaitable** - Missing await creates silent bugs
4. **Use async context managers** - Proper resource cleanup in async code
5. **Choose the right concurrency model** - async vs threading vs multiprocessing

---

## Quick Decision Framework

| Workload Type | Use | Why |
|--------------|-----|-----|
| **I/O-bound** (network, files) | `asyncio` | Single thread handles thousands of concurrent I/O operations |
| **CPU-bound** (computation) | `multiprocessing` | Bypasses GIL, uses multiple CPU cores |
| **Mixed I/O + blocking libs** | `ThreadPoolExecutor` + `asyncio` | Run blocking I/O in threads, coordinate with asyncio |
| **Legacy blocking code** | `run_in_executor()` | Integrate blocking code into async codebase |

**For detailed comparison and examples:** See reference.md Decision Framework section

---

## Async/Await Basics

### async def and await

```python
# Coroutine function (must await to execute)
async def fetch_data(url: str) -> dict:
    """Fetch data from URL asynchronously."""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

# await suspends execution until operation completes
async def process_user(user_id: int) -> dict:
    user = await db.fetch_user(user_id)      # Suspend here
    profile = await api.fetch_profile(user)  # And here
    return {"user": user, "profile": profile}

# Running async code (entry point)
import asyncio

async def main():
    result = await fetch_data("https://api.example.com")
    print(result)

asyncio.run(main())  # Python 3.7+
```

---

## Essential asyncio Patterns

### Pattern 1: Concurrent Execution with gather()

```python
# Run multiple coroutines concurrently
async def fetch_multiple_users(user_ids: list[int]) -> list[dict]:
    """Fetch multiple users concurrently."""
    tasks = [fetch_user(uid) for uid in user_ids]
    return await asyncio.gather(*tasks)

# With error handling
async def fetch_with_errors(user_ids: list[int]) -> list[dict]:
    """Continue on error, return None for failures."""
    tasks = [fetch_user(uid) for uid in user_ids]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return [r for r in results if not isinstance(r, Exception)]
```

### Pattern 2: Fire and Forget with create_task()

```python
# Start background task without waiting
async def handle_request(request: dict) -> dict:
    """Handle request and log asynchronously."""
    asyncio.create_task(log_request(request))  # Fire and forget
    return await process_request(request)      # Don't wait for logging
```

### Pattern 3: Timeouts with wait_for()

```python
# Add timeout to any coroutine
async def fetch_with_timeout(url: str, timeout: float = 5.0) -> dict:
    """Fetch with timeout."""
    try:
        return await asyncio.wait_for(fetch_data(url), timeout=timeout)
    except asyncio.TimeoutError:
        LOG.warning(f"Timeout fetching {url}")
        raise
```

### Pattern 4: Run Blocking Code with run_in_executor()

```python
# Run blocking I/O in thread pool
async def read_file_async(path: str) -> str:
    """Read file without blocking event loop."""
    loop = asyncio.get_running_loop()

    def blocking_read():
        with open(path, 'r') as f:
            return f.read()

    return await loop.run_in_executor(None, blocking_read)

# Run CPU-bound work in process pool
async def compute_intensive_async(data: list[int]) -> int:
    """Run CPU-bound work in process pool."""
    from concurrent.futures import ProcessPoolExecutor

    loop = asyncio.get_running_loop()
    with ProcessPoolExecutor() as pool:
        return await loop.run_in_executor(pool, compute_heavy, data)
```

### Pattern 5: Rate Limiting with Semaphore

```python
# Limit concurrent operations
async def fetch_with_rate_limit(urls: list[str], max_concurrent: int = 5):
    """Limit concurrent requests."""
    semaphore = asyncio.Semaphore(max_concurrent)

    async def fetch_one(url: str):
        async with semaphore:
            return await fetch_data(url)

    tasks = [fetch_one(url) for url in urls]
    return await asyncio.gather(*tasks)
```

---

## Async Context Managers

```python
# Using async context managers
async def fetch_users() -> list[dict]:
    """Fetch users using async context manager."""
    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.example.com") as response:
            return await response.json()

# Creating async context manager
from contextlib import asynccontextmanager

@asynccontextmanager
async def async_transaction():
    """Async transaction context manager."""
    conn = await get_connection()
    tx = await conn.begin()
    try:
        yield conn
        await tx.commit()
    except Exception:
        await tx.rollback()
        raise
    finally:
        await conn.close()

# Usage
async def update_user(user_id: int, data: dict):
    """Update user in transaction."""
    async with async_transaction() as conn:
        await conn.execute("UPDATE users SET data = $1 WHERE id = $2", data, user_id)
```

---

## Common Pitfalls and Solutions

### Pitfall 1: Blocking the Event Loop

| Problem Code | Fixed Code |
|-------------|------------|
| `time.sleep(5)` | `await asyncio.sleep(5)` |
| `requests.get(url)` | `async with aiohttp.ClientSession() as s: await s.get(url)` |
| `open(file).read()` | `await loop.run_in_executor(None, blocking_read)` |
| Heavy CPU work | `await loop.run_in_executor(pool, cpu_work)` |

**Why:** Blocking calls freeze ALL async tasks. Always use async versions or run in executor.

### Pitfall 2: Missing await

```python
# ❌ BAD - missing await
async def bad_fetch():
    result = fetch_data()  # Returns coroutine object, not data!
    print(result)  # <coroutine object...>

# ✅ GOOD - properly awaited
async def good_fetch():
    result = await fetch_data()  # Actually executes
    print(result)  # {'data': ...}
```

**Detection:** Python warns about unawaited coroutines. Always await coroutine functions.

### Pitfall 3: Event Loop Closed

```python
# ❌ BAD - loop closed after asyncio.run()
result1 = asyncio.run(fetch1())
result2 = asyncio.run(fetch2())  # ERROR: Event loop is closed

# ✅ GOOD - single event loop
async def main():
    result1 = await fetch1()
    result2 = await fetch2()
    return result1, result2

asyncio.run(main())
```

### Pitfall 4: Mixing Async and Sync

```python
# ❌ BAD - can't await in sync function
def sync_function():
    result = await fetch_data()  # SyntaxError

# ✅ GOOD - make function async
async def async_function():
    result = await fetch_data()
    return result

# ✅ GOOD - use asyncio.run (entry point only)
def sync_entry_point():
    result = asyncio.run(fetch_data())
    return result
```

### Pitfall 5: Sequential Instead of Concurrent

```python
# ❌ BAD - runs sequentially (slow)
async def sequential():
    results = []
    for url in urls:
        results.append(await fetch(url))  # One at a time
    return results

# ✅ GOOD - runs concurrently (fast)
async def concurrent():
    tasks = [fetch(url) for url in urls]
    return await asyncio.gather(*tasks)  # All at once
```

**For more pitfalls and solutions:** See reference.md Common Pitfalls section

---

## Testing Async Code

### pytest with pytest-asyncio

```python
import pytest
from unittest.mock import AsyncMock, patch

# Mark async test
@pytest.mark.asyncio
async def test_fetch_data():
    """Test async function."""
    result = await fetch_data("https://api.example.com")
    assert result["status"] == "success"

# Async fixtures
@pytest.fixture
async def async_client():
    """Create async HTTP client."""
    async with aiohttp.ClientSession() as session:
        yield session

@pytest.mark.asyncio
async def test_with_fixture(async_client):
    """Test using async fixture."""
    async with async_client.get("https://api.example.com") as resp:
        assert resp.status == 200

# Mocking async functions
@pytest.mark.asyncio
async def test_with_mock():
    """Test with mocked async dependency."""
    mock_fetch = AsyncMock(return_value={"data": "test"})

    with patch('module.fetch_data', mock_fetch):
        result = await process_data()

    assert result["data"] == "test"
    mock_fetch.assert_awaited_once()

# Testing timeouts
@pytest.mark.asyncio
async def test_timeout():
    """Test function respects timeout."""
    with pytest.raises(asyncio.TimeoutError):
        await asyncio.wait_for(slow_operation(), timeout=1.0)
```

**For more testing patterns:** See reference.md Testing Patterns section

---

## Performance Considerations

### When asyncio is Fastest

```python
# Async shines with many I/O operations
async def fetch_1000_urls(urls: list[str]) -> list[dict]:
    """Fetch 1000 URLs concurrently (seconds, not minutes)."""
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_with_session(session, url) for url in urls]
        return await asyncio.gather(*tasks)

# Single thread handles 1000+ concurrent connections!
```

### Optimization: Reuse Connections

```python
# ❌ BAD - creates new session each time
async def inefficient(urls: list[str]):
    results = []
    for url in urls:
        async with aiohttp.ClientSession() as session:  # New session!
            async with session.get(url) as response:
                results.append(await response.json())
    return results

# ✅ GOOD - reuse single session
async def efficient(urls: list[str]):
    async with aiohttp.ClientSession() as session:  # Single session
        tasks = [fetch_with_session(session, url) for url in urls]
        return await asyncio.gather(*tasks)
```

**For more optimizations:** See reference.md Performance Optimization section

---

## Quick Reference Commands

### Basic Patterns

```python
# Run async function
asyncio.run(main())

# Concurrent execution
results = await asyncio.gather(op1(), op2(), op3())

# Fire and forget
asyncio.create_task(background_work())

# Timeout
result = await asyncio.wait_for(operation(), timeout=5.0)

# Run blocking code
result = await loop.run_in_executor(None, blocking_func)

# Async context manager
async with AsyncResource() as resource:
    await resource.operation()

# Async iteration
async for item in async_iterator():
    await process(item)
```

### Common Libraries

**HTTP:** `aiohttp`, `httpx`
**Database:** `asyncpg` (PostgreSQL), `motor` (MongoDB), `aiomysql`
**Files:** `aiofiles`
**Testing:** `pytest-asyncio`, `AsyncMock`

---

## Logging in Async Code

```python
import logging

LOG = logging.getLogger(__name__)

async def async_operation():
    """Async function with logging."""
    LOG.info("Started async operation")

    try:
        result = await fetch_data()
        LOG.debug(f"Fetched {len(result)} items")
        return result
    except Exception as e:
        LOG.error(f"Error in async operation: {e}")
        raise
```

**Note:** Standard logging is thread-safe and works fine with asyncio.

---

## Real-World Example: API Client

```python
import asyncio
import aiohttp
from typing import Any

class AsyncAPIClient:
    """Async API client with connection pooling and retry."""

    def __init__(self, base_url: str, timeout: float = 30.0):
        self.base_url = base_url
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.session = None

    async def __aenter__(self):
        """Create session on context entry."""
        self.session = aiohttp.ClientSession(timeout=self.timeout)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Close session on context exit."""
        if self.session:
            await self.session.close()

    async def get(self, endpoint: str, **kwargs) -> dict[str, Any]:
        """GET request with automatic retry."""
        url = f"{self.base_url}/{endpoint}"
        return await self._request_with_retry('GET', url, **kwargs)

    async def _request_with_retry(
        self,
        method: str,
        url: str,
        max_retries: int = 3,
        **kwargs
    ) -> dict[str, Any]:
        """Make request with exponential backoff retry."""
        delay = 1.0

        for attempt in range(max_retries):
            try:
                async with self.session.request(method, url, **kwargs) as resp:
                    resp.raise_for_status()
                    return await resp.json()
            except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                if attempt == max_retries - 1:
                    raise
                LOG.warning(f"Request failed (attempt {attempt + 1}): {e}")
                await asyncio.sleep(delay)
                delay *= 2

# Usage
async def main():
    async with AsyncAPIClient("https://api.example.com") as client:
        user = await client.get("users/123")
        posts = await client.get("users/123/posts")
        return user, posts

asyncio.run(main())
```

**For more real-world examples:** See reference.md Real-World Examples section

---

## Summary: The Rules

1. **async def** creates coroutine function (must await to execute)
2. **await** suspends coroutine until operation completes
3. **Never block** the event loop (use await, not sync calls)
4. **asyncio.gather()** runs multiple coroutines concurrently
5. **create_task()** starts background work without waiting
6. **wait_for()** adds timeout to any coroutine
7. **run_in_executor()** runs blocking code in thread/process pool
8. **Use async context managers** for proper resource cleanup
9. **Test with pytest-asyncio** and AsyncMock
10. **Choose wisely:** async for I/O, multiprocessing for CPU

---

## Troubleshooting Quick Guide

| Issue | Cause | Solution |
|-------|-------|----------|
| Event loop closed | Multiple `asyncio.run()` calls | Use single `asyncio.run(main())` |
| Coroutine never executed | Missing `await` | Add `await` before coroutine call |
| Not concurrent | Sequential `await` in loop | Use `asyncio.gather()` |
| Slow performance | Blocking event loop | Use async versions or `run_in_executor()` |
| Task destroyed warning | Created task not awaited | Await task or track with callback |

**For detailed troubleshooting:** See reference.md Troubleshooting Guide section

---

**Bottom line:** async is for I/O concurrency, not CPU parallelism. Never block the event loop. Always await awaitable objects.
