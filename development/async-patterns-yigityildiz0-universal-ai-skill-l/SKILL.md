---
name: async-patterns
description: Language-agnostic asynchronous and concurrency patterns including promises, futures, channels, actors, and structured concurrency. Use when implementing.
---

# Async Patterns

Comprehensive guidance on asynchronous programming and concurrency patterns across languages, covering async/await, channels, actors, structured concurrency, and strategies for avoiding common pitfalls like deadlocks and race conditions.

## When to Use This Skill

Use this skill for:

- Implementing async/await in Python, JavaScript, Rust, or C#
- Choosing between concurrency models (threads, coroutines, actors, CSP)
- Designing producer-consumer, fan-out/fan-in, or pipeline architectures
- Debugging race conditions, deadlocks, or resource starvation
- Adding backpressure handling to streaming systems
- Writing tests for asynchronous code
- Implementing structured concurrency with task groups and cancellation
- Converting callback-based code to async/await

**Trigger phrases**: "async", "await", "concurrency", "parallelism", "race condition", "deadlock", "promise", "future", "channel", "goroutine", "tokio", "asyncio", "actor model", "structured concurrency", "backpressure"

## What This Skill Does

Provides production-ready concurrency patterns including:

- **Async/Await**: Idiomatic patterns for Python, JavaScript, Rust, and C#
- **Concurrency Primitives**: Mutexes, semaphores, channels, and atomic operations
- **Architectural Patterns**: Producer-consumer, fan-out/fan-in, pipeline, actor model, CSP
- **Structured Concurrency**: Task groups, cancellation propagation, timeout management
- **Error Handling**: Exception propagation, partial failure recovery, supervision trees
- **Testing Strategies**: Deterministic testing of concurrent code, mocking async dependencies
- **Backpressure**: Bounded queues, rate limiting, flow control

## Instructions

### Step 1: Choose the Right Concurrency Model

**Decision Matrix**:

```
┌──────────────────────┬──────────────────┬────────────────────┬──────────────┐
│ Requirement          │ Best Model       │ Language Examples   │ Trade-offs   │
├──────────────────────┼──────────────────┼────────────────────┼──────────────┤
│ I/O-bound workloads  │ Async/Await      │ Python asyncio,    │ Low overhead │
│                      │                  │ JS Promises, C#    │ Single-thread│
├──────────────────────┼──────────────────┼────────────────────┼──────────────┤
│ CPU-bound parallel   │ Threads/Procs    │ Python multiproc,  │ True parallel│
│                      │                  │ Rust rayon, Go     │ Shared state │
├──────────────────────┼──────────────────┼────────────────────┼──────────────┤
│ Message passing      │ Channels / CSP   │ Go channels,       │ No shared    │
│                      │                  │ Rust mpsc, Elixir  │ state        │
├──────────────────────┼──────────────────┼────────────────────┼──────────────┤
│ Isolated components  │ Actor Model      │ Erlang/OTP, Akka,  │ Fault isolat │
│                      │                  │ Python Thespian    │ Overhead     │
├──────────────────────┼──────────────────┼────────────────────┼──────────────┤
│ Scoped lifetimes     │ Structured Conc. │ Python TaskGroup,  │ Predictable  │
│                      │                  │ Kotlin coroutines  │ cleanup      │
└──────────────────────┴──────────────────┴────────────────────┴──────────────┘
```

### Step 2: Implement Async/Await Patterns

**Python (asyncio)**:

```python
import asyncio
import aiohttp
from typing import list

async def fetch_url(session: aiohttp.ClientSession, url: str) -> dict:
    """Fetch a single URL with timeout and error handling."""
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
            resp.raise_for_status()
            return {"url": url, "status": resp.status, "data": await resp.json()}
    except aiohttp.ClientError as e:
        return {"url": url, "status": "error", "error": str(e)}

async def fetch_all(urls: list[str], max_concurrent: int = 10) -> list[dict]:
    """Fetch multiple URLs with bounded concurrency."""
    semaphore = asyncio.Semaphore(max_concurrent)

    async def bounded_fetch(session, url):
        async with semaphore:
            return await fetch_url(session, url)

    async with aiohttp.ClientSession() as session:
        tasks = [bounded_fetch(session, url) for url in urls]
        return await asyncio.gather(*tasks, return_exceptions=True)

# Entry point
async def main():
    urls = [f"https://api.example.com/items/{i}" for i in range(100)]
    results = await fetch_all(urls, max_concurrent=20)
    successful = [r for r in results if not isinstance(r, Exception)]
    print(f"Fetched {len(successful)} of {len(urls)} URLs")

if __name__ == "__main__":
    asyncio.run(main())
```

**JavaScript (Promises and async/await)**:

```javascript
// Concurrent fetch with error isolation
async function fetchWithRetry(url, retries = 3, backoff = 1000) {
  for (let attempt = 1; attempt <= retries; attempt++) {
    try {
      const controller = new AbortController();
      const timeout = setTimeout(() => controller.abort(), 10000);

      const response = await fetch(url, { signal: controller.signal });
      clearTimeout(timeout);

      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      return await response.json();
    } catch (error) {
      if (attempt === retries) throw error;
      await new Promise((r) => setTimeout(r, backoff * Math.pow(2, attempt - 1)));
    }
  }
}

// Fan-out with bounded concurrency
async function mapConcurrent(items, fn, concurrency = 5) {
  const results = [];
  const executing = new Set();

  for (const item of items) {
    const promise = fn(item).then((result) => {
      executing.delete(promise);
      return result;
    });
    executing.add(promise);
    results.push(promise);

    if (executing.size >= concurrency) {
      await Promise.race(executing);
    }
  }

  return Promise.allSettled(results);
}

// Usage
const urls = Array.from({ length: 50 }, (_, i) => `https://api.example.com/${i}`);
const results = await mapConcurrent(urls, fetchWithRetry, 10);
```

**Rust (tokio)**:

```rust
use tokio::sync::{mpsc, Semaphore};
use std::sync::Arc;
use reqwest::Client;

async fn fetch_url(client: &Client, url: &str) -> Result<String, reqwest::Error> {
    let response = client.get(url)
        .timeout(std::time::Duration::from_secs(10))
        .send()
        .await?;
    response.text().await
}

async fn fetch_all_bounded(urls: Vec<String>, max_concurrent: usize) -> Vec<Result<String, String>> {
    let semaphore = Arc::new(Semaphore::new(max_concurrent));
    let client = Client::new();
    let mut handles = Vec::new();

    for url in urls {
        let permit = semaphore.clone().acquire_owned().await.unwrap();
        let client = client.clone();

        let handle = tokio::spawn(async move {
            let result = fetch_url(&client, &url).await.map_err(|e| e.to_string());
            drop(permit); // Release semaphore
            result
        });
        handles.push(handle);
    }

    let mut results = Vec::new();
    for handle in handles {
        results.push(handle.await.unwrap_or_else(|e| Err(e.to_string())));
    }
    results
}

#[tokio::main]
async fn main() {
    let urls: Vec<String> = (0..100)
        .map(|i| format!("https://api.example.com/items/{}", i))
        .collect();
    let results = fetch_all_bounded(urls, 20).await;
    let ok_count = results.iter().filter(|r| r.is_ok()).count();
    println!("Fetched {ok_count} successfully");
}
```

### Step 3: Implement Channel-Based Patterns (CSP)

**Go (goroutines and channels)**:

```go
package main

import (
    "context"
    "fmt"
    "sync"
    "time"
)

// Pipeline: generator -> processor -> aggregator
func generator(ctx context.Context, items []string) <-chan string {
    out := make(chan string)
    go func() {
        defer close(out)
        for _, item := range items {
            select {
            case out <- item:
            case <-ctx.Done():
                return
            }
        }
    }()
    return out
}

func processor(ctx context.Context, in <-chan string, workerID int) <-chan string {
    out := make(chan string)
    go func() {
        defer close(out)
        for item := range in {
            select {
            case <-ctx.Done():
                return
            default:
                result := fmt.Sprintf("worker-%d processed: %s", workerID, item)
                time.Sleep(100 * time.Millisecond) // Simulate work
                out <- result
            }
        }
    }()
    return out
}

// Fan-out / fan-in pattern
func fanOut(ctx context.Context, in <-chan string, numWorkers int) <-chan string {
    var channels []<-chan string
    for i := 0; i < numWorkers; i++ {
        channels = append(channels, processor(ctx, in, i))
    }
    return merge(ctx, channels...)
}

func merge(ctx context.Context, channels ...<-chan string) <-chan string {
    var wg sync.WaitGroup
    merged := make(chan string)

    output := func(ch <-chan string) {
        defer wg.Done()
        for val := range ch {
            select {
            case merged <- val:
            case <-ctx.Done():
                return
            }
        }
    }

    wg.Add(len(channels))
    for _, ch := range channels {
        go output(ch)
    }

    go func() {
        wg.Wait()
        close(merged)
    }()

    return merged
}

func main() {
    ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
    defer cancel()

    items := []string{"a", "b", "c", "d", "e", "f", "g", "h"}

    // Pipeline: generate -> fan-out to 3 workers -> collect
    generated := generator(ctx, items)
    results := fanOut(ctx, generated, 3)

    for result := range results {
        fmt.Println(result)
    }
}
```

### Step 4: Implement Structured Concurrency

**Python (TaskGroup, Python 3.11+)**:

```python
import asyncio
from dataclasses import dataclass

@dataclass
class TaskResult:
    name: str
    data: object
    error: str | None = None

async def fetch_user(user_id: int) -> TaskResult:
    await asyncio.sleep(0.1)  # Simulate I/O
    return TaskResult(name=f"user-{user_id}", data={"id": user_id, "name": "Alice"})

async def fetch_orders(user_id: int) -> TaskResult:
    await asyncio.sleep(0.2)  # Simulate I/O
    return TaskResult(name=f"orders-{user_id}", data=[{"id": 1, "total": 99.99}])

async def fetch_preferences(user_id: int) -> TaskResult:
    await asyncio.sleep(0.05)  # Simulate I/O
    return TaskResult(name=f"prefs-{user_id}", data={"theme": "dark"})

async def load_user_dashboard(user_id: int) -> dict:
    """Structured concurrency: all tasks share a lifetime.

    If any task fails, the entire group is cancelled automatically.
    """
    results = {}

    async with asyncio.TaskGroup() as tg:
        user_task = tg.create_task(fetch_user(user_id))
        orders_task = tg.create_task(fetch_orders(user_id))
        prefs_task = tg.create_task(fetch_preferences(user_id))

    # All tasks completed successfully (or group raised ExceptionGroup)
    results["user"] = user_task.result().data
    results["orders"] = orders_task.result().data
    results["preferences"] = prefs_task.result().data
    return results

async def main():
    try:
        dashboard = await asyncio.wait_for(
            load_user_dashboard(42),
            timeout=5.0,
        )
        print(f"Dashboard loaded: {dashboard}")
    except TimeoutError:
        print("Dashboard load timed out")
    except ExceptionGroup as eg:
        print(f"Partial failures: {eg.exceptions}")

asyncio.run(main())
```

**Timeout and Cancellation (Rust tokio)**:

```rust
use tokio::time::{timeout, Duration};
use tokio::select;

async fn long_running_task() -> String {
    tokio::time::sleep(Duration::from_secs(5)).await;
    "completed".to_string()
}

async fn with_timeout_and_cancel() {
    let (tx, mut rx) = tokio::sync::oneshot::channel::<()>();

    // Spawn a task that can be cancelled
    let handle = tokio::spawn(async move {
        select! {
            result = long_running_task() => {
                println!("Task finished: {result}");
            }
            _ = &mut rx => {
                println!("Task was cancelled");
            }
        }
    });

    // Apply a timeout
    match timeout(Duration::from_secs(2), handle).await {
        Ok(Ok(())) => println!("Completed within timeout"),
        Ok(Err(e)) => println!("Task panicked: {e}"),
        Err(_) => {
            println!("Timeout reached, sending cancel signal");
            let _ = tx.send(());
        }
    }
}
```

### Step 5: Handle Concurrency Primitives Correctly

**Mutex and Shared State (Rust)**:

```rust
use std::sync::{Arc, Mutex};
use tokio::task;

#[derive(Default)]
struct SharedCounter {
    count: u64,
    errors: u64,
}

async fn increment_counter(counter: Arc<Mutex<SharedCounter>>, n: u64) {
    // Lock, modify, unlock as quickly as possible
    // NEVER hold a mutex lock across an .await point
    let mut guard = counter.lock().unwrap();
    guard.count += n;
    // guard is dropped here (lock released)
}

// WRONG: holding lock across await
async fn bad_example(counter: Arc<Mutex<SharedCounter>>) {
    let mut guard = counter.lock().unwrap();
    // DON'T DO THIS: the lock is held across the await
    // tokio::time::sleep(Duration::from_secs(1)).await;
    // guard.count += 1;

    // CORRECT: extract data, drop lock, do async work, re-acquire
    let current = guard.count;
    drop(guard); // Explicitly release lock

    tokio::time::sleep(std::time::Duration::from_secs(1)).await;

    let mut guard = counter.lock().unwrap();
    guard.count = current + 1;
}
```

**Semaphore for Rate Limiting (Python)**:

```python
import asyncio
import time

class RateLimiter:
    """Token bucket rate limiter using asyncio primitives."""

    def __init__(self, rate: float, burst: int):
        self.rate = rate          # Tokens per second
        self.burst = burst        # Max burst size
        self._sem = asyncio.Semaphore(burst)
        self._refill_task: asyncio.Task | None = None

    async def start(self):
        """Start the background token refill loop."""
        self._refill_task = asyncio.create_task(self._refill())

    async def _refill(self):
        interval = 1.0 / self.rate
        while True:
            await asyncio.sleep(interval)
            try:
                self._sem.release()
            except ValueError:
                pass  # Already at max capacity

    async def acquire(self):
        """Wait until a token is available."""
        await self._sem.acquire()

    async def stop(self):
        if self._refill_task:
            self._refill_task.cancel()
            try:
                await self._refill_task
            except asyncio.CancelledError:
                pass

# Usage
async def rate_limited_requests():
    limiter = RateLimiter(rate=10, burst=5)  # 10 req/sec, burst of 5
    await limiter.start()

    async def make_request(i):
        await limiter.acquire()
        print(f"[{time.monotonic():.2f}] Request {i}")

    tasks = [make_request(i) for i in range(20)]
    await asyncio.gather(*tasks)
    await limiter.stop()
```

### Step 6: Producer-Consumer and Pipeline Patterns

**Go (buffered channels with backpressure)**:

```go
func producerConsumer() {
    // Buffered channel provides natural backpressure
    // Producer blocks when buffer is full
    jobs := make(chan Job, 100)    // Buffer size = backpressure threshold
    results := make(chan Result, 100)
    done := make(chan struct{})

    // Start N consumers
    numWorkers := 5
    var wg sync.WaitGroup
    for i := 0; i < numWorkers; i++ {
        wg.Add(1)
        go func(id int) {
            defer wg.Done()
            for job := range jobs {
                result := process(job)
                results <- result
            }
        }(i)
    }

    // Close results channel when all workers are done
    go func() {
        wg.Wait()
        close(results)
    }()

    // Produce jobs
    go func() {
        for _, item := range getItems() {
            jobs <- Job{Data: item}  // Blocks if buffer full (backpressure)
        }
        close(jobs)
    }()

    // Collect results
    for result := range results {
        fmt.Printf("Result: %v\n", result)
    }
}
```

**Python (asyncio.Queue with backpressure)**:

```python
import asyncio
from typing import AsyncIterator

async def producer(queue: asyncio.Queue, items: list):
    """Produce items; blocks when queue is full (backpressure)."""
    for item in items:
        await queue.put(item)  # Blocks if queue.maxsize reached
    await queue.put(None)      # Sentinel to signal completion

async def consumer(queue: asyncio.Queue, consumer_id: int):
    """Consume items from the queue."""
    while True:
        item = await queue.get()
        if item is None:
            await queue.put(None)  # Re-post sentinel for other consumers
            break
        result = await process(item)
        print(f"Consumer {consumer_id}: processed {item} -> {result}")
        queue.task_done()

async def pipeline():
    queue = asyncio.Queue(maxsize=50)  # Bounded = backpressure
    items = list(range(200))

    producers = [asyncio.create_task(producer(queue, items))]
    consumers = [asyncio.create_task(consumer(queue, i)) for i in range(5)]

    await asyncio.gather(*producers)
    await queue.join()  # Wait for all items to be processed
    for c in consumers:
        c.cancel()
```

### Step 7: Debug Common Concurrency Bugs

**Deadlock Detection Checklist**:

```
Common Deadlock Causes:
1. Lock ordering violation   -> Always acquire locks in consistent order
2. Holding lock across await -> Extract data, release, do async work, re-acquire
3. Nested lock acquisition   -> Use a single coarse lock or lock hierarchy
4. Channel operations block  -> Use select/timeout to prevent indefinite blocking
```

**Race Condition Patterns**:

```python
# WRONG: check-then-act race condition
if key not in cache:         # Thread A checks
    # Thread B also checks and enters
    cache[key] = compute()   # Both threads compute and write

# CORRECT: use atomic operations or locks
import threading

lock = threading.Lock()

def safe_get_or_compute(cache, key, compute_fn):
    with lock:
        if key not in cache:
            cache[key] = compute_fn()
        return cache[key]
```

**Go Race Detector**:

```bash
# Run tests with race detection enabled
go test -race ./...

# Run a binary with race detection
go run -race main.go
```

**Rust Compile-Time Safety**:

```rust
// Rust prevents data races at compile time through the ownership system.
// This code will NOT compile:
//
// let mut data = vec![1, 2, 3];
// let handle = std::thread::spawn(|| {
//     data.push(4);  // ERROR: closure may outlive the current function
// });
//
// CORRECT: use Arc<Mutex<T>> for shared mutable state
use std::sync::{Arc, Mutex};
use std::thread;

let data = Arc::new(Mutex::new(vec![1, 2, 3]));
let data_clone = Arc::clone(&data);

let handle = thread::spawn(move || {
    let mut guard = data_clone.lock().unwrap();
    guard.push(4);
});

handle.join().unwrap();
println!("{:?}", data.lock().unwrap()); // [1, 2, 3, 4]
```

### Step 8: Test Asynchronous Code

**Python (pytest-asyncio)**:

```python
import pytest
import asyncio

@pytest.mark.asyncio
async def test_fetch_with_timeout():
    """Test that slow operations respect timeout."""
    async def slow_operation():
        await asyncio.sleep(10)
        return "done"

    with pytest.raises(asyncio.TimeoutError):
        await asyncio.wait_for(slow_operation(), timeout=0.1)

@pytest.mark.asyncio
async def test_concurrent_safety():
    """Test that shared state is safe under concurrent access."""
    counter = {"value": 0}
    lock = asyncio.Lock()

    async def increment():
        for _ in range(1000):
            async with lock:
                counter["value"] += 1

    await asyncio.gather(*[increment() for _ in range(10)])
    assert counter["value"] == 10000

@pytest.mark.asyncio
async def test_producer_consumer():
    """Test that all items are processed exactly once."""
    queue = asyncio.Queue(maxsize=10)
    processed = []

    async def producer():
        for i in range(50):
            await queue.put(i)
        await queue.put(None)

    async def consumer():
        while True:
            item = await queue.get()
            if item is None:
                break
            processed.append(item)

    await asyncio.gather(producer(), consumer())
    assert processed == list(range(50))
```

**JavaScript (Jest)**:

```javascript
describe("async patterns", () => {
  test("mapConcurrent respects concurrency limit", async () => {
    let activeCalls = 0;
    let maxActive = 0;

    const task = async (item) => {
      activeCalls++;
      maxActive = Math.max(maxActive, activeCalls);
      await new Promise((r) => setTimeout(r, 50));
      activeCalls--;
      return item * 2;
    };

    const items = Array.from({ length: 20 }, (_, i) => i);
    const results = await mapConcurrent(items, task, 5);

    expect(maxActive).toBeLessThanOrEqual(5);
    expect(results.filter((r) => r.status === "fulfilled")).toHaveLength(20);
  });

  test("fetchWithRetry retries on failure", async () => {
    let attempts = 0;
    global.fetch = jest.fn().mockImplementation(() => {
      attempts++;
      if (attempts < 3) throw new Error("Network error");
      return Promise.resolve({ ok: true, json: () => Promise.resolve({ data: 1 }) });
    });

    const result = await fetchWithRetry("https://example.com", 3, 10);
    expect(result).toEqual({ data: 1 });
    expect(attempts).toBe(3);
  });
});
```

## Best Practices

- **Prefer structured concurrency** over fire-and-forget tasks; it guarantees cleanup
- **Never hold locks across await points**; extract data, release the lock, do async work
- **Use bounded queues and semaphores** to implement backpressure; unbounded queues cause memory issues
- **Acquire locks in a consistent global order** to prevent deadlocks
- **Favour message passing over shared mutable state** when architecture allows
- **Set timeouts on every external I/O call**; never assume a remote call will return
- **Use cancellation tokens or context objects** to propagate shutdown signals
- **Test concurrency with race detectors** (Go `-race`, ThreadSanitizer, Python `asyncio` debug mode)
- **Log with correlation IDs** so concurrent request traces can be reconstructed
- **Profile before parallelizing**; concurrency adds complexity and is only worthwhile for real bottlenecks

## Common Patterns

### Pattern 1: Retry with Exponential Backoff

```python
import asyncio
import random

async def retry_with_backoff(
    coro_factory,
    retries: int = 5,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    jitter: bool = True,
):
    """Retry an async operation with exponential backoff and optional jitter."""
    for attempt in range(retries):
        try:
            return await coro_factory()
        except Exception as e:
            if attempt == retries - 1:
                raise
            delay = min(base_delay * (2 ** attempt), max_delay)
            if jitter:
                delay *= (0.5 + random.random())
            await asyncio.sleep(delay)
```

### Pattern 2: Circuit Breaker

```python
import asyncio
import time
from enum import Enum

class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

class CircuitBreaker:
    def __init__(self, failure_threshold=5, recovery_timeout=30.0):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.last_failure_time = 0.0

    async def call(self, coro):
        if self.state == CircuitState.OPEN:
            if time.monotonic() - self.last_failure_time > self.recovery_timeout:
                self.state = CircuitState.HALF_OPEN
            else:
                raise RuntimeError("Circuit breaker is OPEN")

        try:
            result = await coro
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise

    def _on_success(self):
        self.failure_count = 0
        self.state = CircuitState.CLOSED

    def _on_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.monotonic()
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN
```

### Pattern 3: Fan-Out / Fan-In with Result Aggregation

```go
// Fan-out work to N goroutines; fan-in results into a single channel
func fanOutFanIn(ctx context.Context, input []int, workers int) (int, error) {
    jobs := make(chan int, len(input))
    results := make(chan int, len(input))
    errs := make(chan error, workers)

    // Fan-out
    var wg sync.WaitGroup
    for i := 0; i < workers; i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            for job := range jobs {
                select {
                case <-ctx.Done():
                    errs <- ctx.Err()
                    return
                default:
                    results <- job * job // Example: square the number
                }
            }
        }()
    }

    // Send jobs
    for _, v := range input {
        jobs <- v
    }
    close(jobs)

    // Wait for workers, then close results
    go func() {
        wg.Wait()
        close(results)
        close(errs)
    }()

    // Fan-in: aggregate
    total := 0
    for r := range results {
        total += r
    }

    if err := <-errs; err != nil {
        return 0, err
    }
    return total, nil
}
```

### Pattern 4: Actor Model (Simplified Python)

```python
import asyncio
from typing import Any

class Actor:
    """Lightweight actor: processes messages sequentially via a mailbox."""

    def __init__(self):
        self._mailbox: asyncio.Queue = asyncio.Queue()
        self._running = False

    async def start(self):
        self._running = True
        asyncio.create_task(self._run())

    async def _run(self):
        while self._running:
            message = await self._mailbox.get()
            if message is None:
                break
            await self.handle(message)

    async def handle(self, message: Any):
        raise NotImplementedError

    async def send(self, message: Any):
        await self._mailbox.put(message)

    async def stop(self):
        self._running = False
        await self._mailbox.put(None)

class CounterActor(Actor):
    def __init__(self):
        super().__init__()
        self.count = 0

    async def handle(self, message):
        if message["type"] == "increment":
            self.count += message.get("amount", 1)
        elif message["type"] == "get":
            message["reply"].set_result(self.count)
```

## Quality Checklist

- [ ] Concurrency model matches the workload type (I/O-bound vs CPU-bound)
- [ ] All async I/O calls have explicit timeouts
- [ ] Bounded queues or semaphores enforce backpressure
- [ ] Locks are never held across await points
- [ ] Cancellation propagates through task hierarchies
- [ ] Error handling covers partial failures in concurrent operations
- [ ] Race detector or equivalent tool used during testing
- [ ] No fire-and-forget tasks without supervision
- [ ] Shared mutable state is protected by appropriate primitives
- [ ] Retry logic includes exponential backoff with jitter
- [ ] Structured concurrency is used where supported (TaskGroup, context.WithCancel)
- [ ] Concurrent tests are deterministic and do not depend on timing

## Related Skills

- `performance-testing` - Load testing concurrent systems
- `debug-with-logs` - Tracing async execution flows
- `observability-setup` - Distributed tracing for async architectures
- `event-driven-architecture` - Event-based concurrency patterns

---

**Version**: 1.0.0
**Last Updated**: March 2026

### Iterative Refinement Strategy
This skill is optimized for an iterative approach:
1. **Execute**: Perform the core steps defined above.
2. **Review**: Critically analyze the output (coverage, quality, completeness).
3. **Refine**: If targets aren't met, repeat the specific implementation steps with improved context.
4. **Loop**: Continue until the definition of done is satisfied.
