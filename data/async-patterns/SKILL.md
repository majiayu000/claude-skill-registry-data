---
name: async-patterns
version: "1.0"
description: >
  Async/await patterns with comprehensive error handling and resource cleanup for Python 3.13.
  PROACTIVELY activate for: (1) Implementing async API clients, (2) Creating concurrent data fetching,
  (3) Building async context managers, (4) Implementing retry logic, (5) Managing background tasks.
  Triggers: "async", "await", "asyncio", "concurrent", "aiohttp", "gather", "create_task", "timeout"
core-integration:
  techniques:
    primary: ["parallel_decomposition_strategies"]
    secondary: ["structured_decomposition"]
  contracts:
    input: "none"
    output: "none"
  patterns: "none"
  rubrics: "none"
---

# Async/Await Patterns with Comprehensive Error Handling

## Core Principles

Async programming in Python 3.13 enables high-performance I/O-bound operations. **All async code in Vibekit MUST include comprehensive error handling and proper resource cleanup.**

## Basic Async Functions

Every async function must handle errors properly:

```python
import asyncio
from typing import Any

# ✅ REQUIRED: Comprehensive error handling in async functions
async def fetch_data(url: str, timeout: float = 10.0) -> dict[str, Any]:
    """
    Fetch data from URL with timeout and error handling.

    Raises:
        TimeoutError: If request exceeds timeout
        ConnectionError: If network request fails
        ValueError: If response is not valid JSON
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=timeout)) as response:
                response.raise_for_status()  # Raises on 4xx/5xx
                return await response.json()
    except asyncio.TimeoutError:
        raise TimeoutError(f"Request to {url} timed out after {timeout}s")
    except aiohttp.ClientError as e:
        raise ConnectionError(f"Failed to fetch {url}: {e}")
    except ValueError as e:
        raise ValueError(f"Invalid JSON response from {url}: {e}")
    # Let other exceptions propagate

# ❌ FORBIDDEN: Async function without error handling
async def bad_fetch(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()  # No timeout, no error handling!
```

## Concurrent Execution with asyncio.gather()

Run multiple async operations concurrently:

```python
import asyncio
from typing import Any

# ✅ REQUIRED: Use asyncio.gather() for concurrent operations
async def fetch_multiple_urls(urls: list[str]) -> list[dict[str, Any]]:
    """
    Fetch multiple URLs concurrently.

    Returns list of results in same order as input URLs.
    Failed requests return None instead of raising.
    """
    tasks = [fetch_data(url) for url in urls]

    # return_exceptions=True prevents one failure from cancelling all tasks
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # Process results and exceptions
    processed: list[dict[str, Any]] = []
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            print(f"Error fetching {urls[i]}: {result}")
            processed.append(None)
        else:
            processed.append(result)

    return processed

# Alternative: Fail-fast (any error cancels all)
async def fetch_multiple_strict(urls: list[str]) -> list[dict[str, Any]]:
    """Fetch URLs concurrently, raise on first error."""
    tasks = [fetch_data(url) for url in urls]
    return await asyncio.gather(*tasks)  # return_exceptions=False (default)
```

## Task Management with create_task()

Control task lifecycle explicitly:

```python
import asyncio
from typing import Set

# ✅ REQUIRED: Track tasks and handle cleanup
class BackgroundTaskManager:
    def __init__(self):
        self.tasks: Set[asyncio.Task] = set()

    def create_task(self, coro) -> asyncio.Task:
        """Create task and track it."""
        task = asyncio.create_task(coro)
        self.tasks.add(task)
        task.add_done_callback(self.tasks.discard)  # Auto-remove when done
        return task

    async def shutdown(self) -> None:
        """Cancel all pending tasks."""
        for task in self.tasks:
            task.cancel()

        # Wait for all cancellations to complete
        await asyncio.gather(*self.tasks, return_exceptions=True)
        self.tasks.clear()

# Usage
async def main():
    manager = BackgroundTaskManager()

    # Start background tasks
    task1 = manager.create_task(long_running_operation())
    task2 = manager.create_task(periodic_cleanup())

    try:
        # Do main work
        await some_main_task()
    finally:
        # Clean shutdown
        await manager.shutdown()
```

## Async Context Managers

Ensure proper resource cleanup in async code:

```python
import asyncio
from typing import AsyncIterator

# ✅ REQUIRED: Use async context managers for resources
class AsyncDatabaseConnection:
    """Async context manager for database connections."""

    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.conn = None

    async def __aenter__(self):
        """Establish connection on enter."""
        try:
            self.conn = await asyncio.wait_for(
                connect_to_database(self.connection_string),
                timeout=5.0
            )
            return self.conn
        except asyncio.TimeoutError:
            raise TimeoutError("Database connection timeout")
        except Exception as e:
            raise ConnectionError(f"Failed to connect: {e}")

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Close connection on exit, even if exception occurred."""
        if self.conn is not None:
            try:
                await asyncio.wait_for(self.conn.close(), timeout=5.0)
            except Exception as e:
                print(f"Error closing connection: {e}")
        return False  # Don't suppress exceptions

# Usage
async def query_database():
    async with AsyncDatabaseConnection("postgresql://...") as conn:
        result = await conn.execute("SELECT * FROM users")
        return result
```

## Timeouts and Cancellation

Always set timeouts for async operations:

```python
import asyncio
from typing import Any

# ✅ REQUIRED: Use timeouts for all external I/O
async def fetch_with_timeout(url: str, timeout: float = 10.0) -> dict[str, Any]:
    """Fetch data with overall timeout."""
    try:
        return await asyncio.wait_for(
            fetch_data(url),
            timeout=timeout
        )
    except asyncio.TimeoutError:
        raise TimeoutError(f"Operation timed out after {timeout}s")

# ✅ REQUIRED: Handle cancellation gracefully
async def long_running_task():
    """Task that handles cancellation properly."""
    try:
        for i in range(100):
            await asyncio.sleep(1)
            print(f"Step {i}")
    except asyncio.CancelledError:
        print("Task was cancelled, cleaning up...")
        # Perform cleanup
        raise  # Re-raise to propagate cancellation

# ❌ FORBIDDEN: Async operation without timeout
async def bad_fetch():
    return await fetch_data("https://slow-api.com")  # No timeout!
```

## Structured Concurrency with TaskGroup (Python 3.11+)

Use TaskGroup for managing related tasks:

```python
import asyncio

# ✅ REQUIRED: Use TaskGroup for structured concurrency
async def fetch_all_data() -> list[dict]:
    """Fetch data from multiple sources using TaskGroup."""
    results = []

    async with asyncio.TaskGroup() as tg:
        # All tasks started within the group
        task1 = tg.create_task(fetch_data("https://api1.example.com"))
        task2 = tg.create_task(fetch_data("https://api2.example.com"))
        task3 = tg.create_task(fetch_data("https://api3.example.com"))

    # At this point, all tasks have completed or an exception was raised
    results = [task1.result(), task2.result(), task3.result()]
    return results

# TaskGroup automatically:
# - Waits for all tasks to complete
# - Cancels remaining tasks if one raises an exception
# - Raises the first exception that occurred
```

## Async Generators

Create async iterators for streaming data:

```python
import asyncio
from typing import AsyncIterator

# ✅ REQUIRED: Async generators for streaming data
async def fetch_paginated_data(api_url: str) -> AsyncIterator[dict]:
    """Fetch paginated data, yielding each item."""
    page = 1
    while True:
        try:
            response = await fetch_data(f"{api_url}?page={page}")
            items = response.get("items", [])

            if not items:
                break

            for item in items:
                yield item

            page += 1
            await asyncio.sleep(0.1)  # Rate limiting
        except Exception as e:
            print(f"Error fetching page {page}: {e}")
            break

# Usage
async def process_all_items():
    async for item in fetch_paginated_data("https://api.example.com/items"):
        await process_item(item)
```

## Anti-Patterns to Avoid

### No Error Handling in Async Functions
```python
# BAD: Silent failures
async def bad_fetch(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

# GOOD: Explicit error handling
async def good_fetch(url: str) -> dict:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                return await response.json()
    except aiohttp.ClientError as e:
        raise ConnectionError(f"Failed to fetch {url}: {e}")
```

### No Timeout on Async Operations
```python
# BAD: Can hang forever
result = await fetch_data(url)

# GOOD: Always use timeout
result = await asyncio.wait_for(fetch_data(url), timeout=10.0)
```

### Not Re-raising CancelledError
```python
# BAD: Suppresses cancellation
async def bad_task():
    try:
        await long_operation()
    except asyncio.CancelledError:
        print("Cancelled")
        # Missing: raise

# GOOD: Re-raise to propagate cancellation
async def good_task():
    try:
        await long_operation()
    except asyncio.CancelledError:
        print("Cancelled, cleaning up...")
        # Cleanup
        raise  # Re-raise
```

### Using Blocking Code in Async Functions
```python
# BAD: Blocks the event loop
async def bad_async():
    time.sleep(10)  # Blocking!
    return "done"

# GOOD: Use async sleep
async def good_async():
    await asyncio.sleep(10)  # Non-blocking
    return "done"
```

## When to Use This Skill

Activate this skill when:
- Implementing async API clients or server handlers
- Creating concurrent data fetching operations
- Building async context managers
- Implementing retry logic for async operations
- Working with async generators or streaming data
- Managing background tasks with proper lifecycle

## Related Resources

For additional patterns, see:
- Python asyncio Documentation: https://docs.python.org/3/library/asyncio.html
- Python 3.13 Patterns: See `python-3-13-patterns` skill
