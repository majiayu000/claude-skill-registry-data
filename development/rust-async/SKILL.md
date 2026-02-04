---
name: rust-async
description: Rust async/await patterns with Tokio. Use when writing async code, handling concurrency, managing tasks, working with channels, or debugging async issues.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Rust Async Patterns with Tokio

## Async Closures (Rust 1.85+)

```rust
// Async closures - stable since Rust 1.85
let fetch_data = async |url: &str| -> Result<Data, Error> {
    let response = reqwest::get(url).await?;
    response.json().await
};

// Use with higher-order functions
async fn process_urls(urls: Vec<String>) -> Vec<Result<Data, Error>> {
    let fetch = async |url: String| {
        reqwest::get(&url).await?.json().await
    };
    
    futures::future::join_all(urls.into_iter().map(fetch)).await
}

// Async closures capture by reference by default (like regular closures)
let data = vec![1, 2, 3];
let process = async || {
    // `data` is borrowed here
    data.iter().sum::<i32>()
};
```

## Task Management

### Spawning Tasks

```rust
use tokio::task::JoinSet;

// GOOD - JoinSet for scoped tasks
async fn process_items(items: Vec<Item>) -> Vec<Result<Output, Error>> {
    let mut set = JoinSet::new();
    
    for item in items {
        set.spawn(async move {
            process_item(item).await
        });
    }
    
    let mut results = Vec::with_capacity(set.len());
    while let Some(result) = set.join_next().await {
        match result {
            Ok(output) => results.push(output),
            Err(e) => results.push(Err(e.into())),
        }
    }
    results
}

// For fire-and-forget
tokio::spawn(async move {
    // Task runs independently
    background_work().await;
});
```

### Cancellation

```rust
use tokio::select;
use tokio_util::sync::CancellationToken;

async fn cancellable_operation(cancel: CancellationToken) -> Result<Output, Error> {
    select! {
        result = do_work() => result,
        _ = cancel.cancelled() => Err(Error::Cancelled),
    }
}

// Using timeout
use tokio::time::{timeout, Duration};

async fn with_timeout() -> Result<Output, Error> {
    timeout(Duration::from_secs(30), do_work())
        .await
        .map_err(|_| Error::Timeout)?
}
```

### Graceful Shutdown

```rust
use tokio::signal;
use tokio::sync::broadcast;

async fn run_with_shutdown() {
    let (shutdown_tx, _) = broadcast::channel::<()>(1);
    
    // Spawn worker with shutdown receiver
    let mut shutdown_rx = shutdown_tx.subscribe();
    let worker = tokio::spawn(async move {
        loop {
            select! {
                _ = do_work() => {}
                _ = shutdown_rx.recv() => {
                    println!("Shutting down worker");
                    break;
                }
            }
        }
    });
    
    // Wait for Ctrl+C
    signal::ctrl_c().await.expect("Failed to listen for Ctrl+C");
    
    // Signal shutdown
    let _ = shutdown_tx.send(());
    
    // Wait for worker to finish
    let _ = worker.await;
}
```

## Channels

### Bounded MPSC (Multi-Producer, Single-Consumer)

```rust
use tokio::sync::mpsc;

// For work queues - bounded prevents memory exhaustion
let (tx, mut rx) = mpsc::channel::<Work>(100);

// Producer
tokio::spawn(async move {
    tx.send(work).await.expect("receiver dropped");
});

// Consumer
while let Some(work) = rx.recv().await {
    process(work).await;
}
```

### Broadcast (Multi-Producer, Multi-Consumer)

```rust
use tokio::sync::broadcast;

// For events/notifications - stateless
let (tx, _) = broadcast::channel::<Event>(16);

// Multiple subscribers
let mut rx1 = tx.subscribe();
let mut rx2 = tx.subscribe();

// Publish
tx.send(Event::Updated)?;

// Receive
while let Ok(event) = rx1.recv().await {
    handle_event(event);
}
```

### Oneshot (Single Value)

```rust
use tokio::sync::oneshot;

// For request-response pattern
async fn request_with_response() -> Result<Response, Error> {
    let (tx, rx) = oneshot::channel();
    
    // Send request with response channel
    request_queue.send(Request { response: tx }).await?;
    
    // Wait for response
    rx.await.map_err(|_| Error::NoResponse)
}
```

### Watch (Single Value, Latest Only)

```rust
use tokio::sync::watch;

// For configuration/state that updates
let (tx, rx) = watch::channel(initial_config);

// Update
tx.send(new_config)?;

// Read latest (non-blocking)
let current = rx.borrow().clone();

// Wait for changes
let mut rx = rx.clone();
while rx.changed().await.is_ok() {
    let new_value = rx.borrow().clone();
    apply_config(new_value);
}
```

## Shared State

### RwLock (Prefer Over Mutex)

```rust
use tokio::sync::RwLock;
use std::sync::Arc;

struct SharedState {
    data: Arc<RwLock<Data>>,
}

impl SharedState {
    async fn read(&self) -> Data {
        self.data.read().await.clone()
    }
    
    async fn update(&self, new_data: Data) {
        let mut guard = self.data.write().await;
        *guard = new_data;
    }
}
```

### Downgrade Write Lock to Read Lock

```rust
use parking_lot::RwLock;

// parking_lot RwLock supports downgrade (not available in tokio::sync::RwLock)
fn update_and_read(lock: &RwLock<Data>) -> Data {
    let mut write_guard = lock.write();
    
    // Modify data
    write_guard.value += 1;
    
    // Atomically downgrade to read lock without releasing
    // Other readers can now access, but we keep our view
    let read_guard = parking_lot::RwLockWriteGuard::downgrade(write_guard);
    
    read_guard.clone()
}

// Note: std::sync::RwLockWriteGuard::downgrade stabilized in Rust 1.92 (project MSRV)
// For async code, use parking_lot or clone data before releasing write lock
```

### Avoid Holding Locks Across Await

```rust
// BAD - lock held across await point
async fn bad_example(state: Arc<RwLock<Data>>) {
    let guard = state.read().await;
    do_async_work(&guard).await;  // Lock held here!
}

// GOOD - clone data, release lock
async fn good_example(state: Arc<RwLock<Data>>) {
    let data = state.read().await.clone();
    // Lock released
    do_async_work(&data).await;
}
```

## Streams

### Processing Streams

```rust
use futures::StreamExt;
use tokio_stream::wrappers::ReceiverStream;

async fn process_stream(rx: mpsc::Receiver<Item>) {
    let stream = ReceiverStream::new(rx);
    
    stream
        .map(|item| async move { transform(item).await })
        .buffer_unordered(10)  // Concurrent processing
        .for_each(|result| async {
            handle_result(result);
        })
        .await;
}
```

### Buffering and Batching

```rust
use futures::StreamExt;
use tokio::time::Duration;

async fn batch_process(rx: mpsc::Receiver<Item>) {
    let stream = ReceiverStream::new(rx);
    
    // Collect into batches
    stream
        .chunks_timeout(100, Duration::from_millis(100))
        .for_each(|batch| async move {
            process_batch(batch).await;
        })
        .await;
}
```

## Error Handling in Async

### Propagating Errors

```rust
async fn fallible_operation() -> Result<Output, Error> {
    let data = fetch_data().await?;
    let processed = process(data).await?;
    Ok(processed)
}
```

### Handling Multiple Futures

```rust
use futures::future::try_join_all;

async fn process_all(items: Vec<Item>) -> Result<Vec<Output>, Error> {
    let futures = items.into_iter().map(|item| async move {
        process_item(item).await
    });
    
    try_join_all(futures).await
}
```

### Retry Logic

```rust
use tokio::time::{sleep, Duration};

async fn with_retry<T, E, F, Fut>(
    mut operation: F,
    max_retries: u32,
) -> Result<T, E>
where
    F: FnMut() -> Fut,
    Fut: std::future::Future<Output = Result<T, E>>,
{
    let mut attempts = 0;
    loop {
        match operation().await {
            Ok(result) => return Ok(result),
            Err(e) if attempts < max_retries => {
                attempts += 1;
                let delay = Duration::from_millis(100 * 2u64.pow(attempts));
                sleep(delay).await;
            }
            Err(e) => return Err(e),
        }
    }
}
```

## Testing Async Code

```rust
#[tokio::test]
async fn test_async_function() {
    let result = async_function().await;
    assert!(result.is_ok());
}

#[tokio::test(flavor = "multi_thread", worker_threads = 2)]
async fn test_concurrent() {
    // Test with multiple worker threads
}

// Time-based testing
#[tokio::test]
async fn test_timeout() {
    tokio::time::pause();  // Control time
    
    let start = tokio::time::Instant::now();
    tokio::time::advance(Duration::from_secs(10)).await;
    
    assert_eq!(start.elapsed(), Duration::from_secs(10));
}
```

## Blocking Work in Async Context

```rust
use tokio::task::spawn_blocking;

async fn process_with_cpu_work(data: Data) -> Result<Output, Error> {
    // Don't block the async runtime with CPU-heavy work
    let result = spawn_blocking(move || {
        // CPU-intensive computation runs on blocking thread pool
        expensive_computation(&data)
    })
    .await
    .map_err(|e| Error::TaskPanic(e.to_string()))?;
    
    Ok(result)
}

// For sync I/O in async context
async fn read_file_blocking(path: PathBuf) -> std::io::Result<String> {
    spawn_blocking(move || std::fs::read_to_string(path)).await?
}
```

## Async Anti-patterns and Pitfalls

### Common Async Issues
- **Blocking in async** - never use `std::thread::sleep`, `std::sync::Mutex`, or blocking I/O
- **Runtime mixing** - don't mix Tokio and async-std; pick one runtime
- **Send bound violations** - ensure spawned futures are Send
- **Task starvation** - yield periodically in long computations with `tokio::task::yield_now()`
- **Unbounded channel growth** - always use bounded channels for backpressure
- **Select bias** - `select!` polls randomly by default; use `biased;` for deterministic priority order
- **Cancellation unsafety** - dropped futures may leave resources in inconsistent state
- **Future leak** - spawned tasks without JoinHandle tracking can leak

### Async Recursion
```rust
// BAD - infinite stack size due to recursive future
async fn bad_recursive(n: u32) -> u32 {
    if n == 0 { 0 } else { bad_recursive(n - 1).await }
}

// GOOD - use Box::pin for async recursion
use std::pin::Pin;
use std::future::Future;

fn good_recursive(n: u32) -> Pin<Box<dyn Future<Output = u32> + Send>> {
    Box::pin(async move {
        if n == 0 { 0 } else { good_recursive(n - 1).await }
    })
}
```

### Avoiding Blocking
```rust
// BAD - blocks the async runtime
async fn bad_blocking() {
    std::thread::sleep(Duration::from_secs(1));  // Blocks!
    std::fs::read_to_string("file.txt");         // Blocks!
}

// GOOD - use async alternatives or spawn_blocking
async fn good_non_blocking() {
    tokio::time::sleep(Duration::from_secs(1)).await;
    tokio::fs::read_to_string("file.txt").await;
    
    // For unavoidable blocking:
    tokio::task::spawn_blocking(|| {
        heavy_cpu_work()
    }).await;
}
```

### Proper Mutex Usage
```rust
use tokio::sync::Mutex;  // NOT std::sync::Mutex

// GOOD - tokio Mutex for async
async fn async_safe(data: Arc<tokio::sync::Mutex<Data>>) {
    let guard = data.lock().await;
    // Use guard
}

// ALSO GOOD - parking_lot for short non-async critical sections
use parking_lot::Mutex;

async fn quick_sync(data: Arc<parking_lot::Mutex<Data>>) {
    let result = {
        let guard = data.lock();  // Very brief, OK
        guard.clone()
    };  // Lock released immediately
    do_async_work(result).await;
}
```

## Nebula-Specific Async Patterns

- Default timeout: 30s for operations
- Database operations: 5s timeout
- HTTP calls: 10s timeout
- Always include cancellation in long-running tasks
- Use `JoinSet` for managing concurrent workflow steps
- Prefer bounded channels to prevent memory exhaustion
- Use `select!` for responsive shutdown handling
- Use `spawn_blocking` for CPU-bound work
