---
name: rust-async-concurrency
description: Manage concurrent operations with channels, semaphores, locks, and streams. Use when coordinating parallel work or limiting resource usage.
---

# Async Concurrency

Patterns for managing concurrent operations in async Rust.

## Channel Selection

Choose the right channel for your use case:

```rust
use tokio::sync::{mpsc, oneshot, broadcast, watch};

// Bounded MPSC - Work queues with backpressure
let (tx, mut rx) = mpsc::channel::<Task>(100);

// Oneshot - Single response (request/reply)
let (tx, rx) = oneshot::channel::<Result>();

// Broadcast - Multiple consumers (pub/sub)
let (tx, _rx) = broadcast::channel::<Event>(16);

// Watch - Latest value (config/state)
let (tx, rx) = watch::channel(initial_config);
```

## Semaphore for Resource Limiting

```rust
use std::sync::Arc;
use tokio::sync::Semaphore;

// Limit concurrent operations
let semaphore = Arc::new(Semaphore::new(10));  // Max 10 concurrent

async fn limited_operation(semaphore: Arc<Semaphore>) -> Result<()> {
    let _permit = semaphore.acquire().await?;  // Wait for permit

    do_work().await?;

    // Permit released on drop
    Ok(())
}

// VRAM-aware scheduling (acquire multiple units)
let vram_semaphore = Arc::new(Semaphore::new(16));  // 16 GB units

async fn run_model(semaphore: Arc<Semaphore>, vram_gb: u32) -> Result<()> {
    let _permit = semaphore.acquire_many(vram_gb).await?;
    run_gpu_model().await
}
// Whisper: 5 units, VideoMAE: 5 units, CLAP: 2 units
```

## Parallel Execution with join!

```rust
use tokio::join;

// Run concurrently, wait for all
let (result_a, result_b, result_c) = join!(
    fetch_a(),
    fetch_b(),
    fetch_c(),
);

// With try_join! for early failure
let (a, b) = tokio::try_join!(
    fetch_a(),
    fetch_b(),
)?;
```

## Parallel Streams

```rust
use futures::stream::{self, StreamExt};

// Process items concurrently with limit
let results: Vec<_> = stream::iter(items)
    .map(|item| async move { process(item).await })
    .buffer_unordered(10)  // Max 10 concurrent
    .collect()
    .await;

// With semaphore for finer control
let semaphore = Arc::new(Semaphore::new(10));

let results: Vec<_> = stream::iter(items)
    .map(|item| {
        let sem = semaphore.clone();
        async move {
            let _permit = sem.acquire().await?;
            process(item).await
        }
    })
    .buffer_unordered(100)  // High buffer, semaphore limits actual concurrency
    .collect()
    .await;
```

## Shared State with Locks

```rust
use std::sync::Arc;
use tokio::sync::{Mutex, RwLock};

// Tokio Mutex (for async code)
let shared = Arc::new(Mutex::new(State::new()));

async fn update(shared: Arc<Mutex<State>>) {
    let mut guard = shared.lock().await;
    guard.update();
}  // Lock released

// RwLock for read-heavy workloads
let cache = Arc::new(RwLock::new(HashMap::new()));

async fn read(cache: Arc<RwLock<Cache>>) -> Option<Value> {
    cache.read().await.get(&key).cloned()
}

async fn write(cache: Arc<RwLock<Cache>>, key: Key, value: Value) {
    cache.write().await.insert(key, value);
}

// Minimize lock scope
async fn process(mutex: &Mutex<Data>) {
    let data = {
        mutex.lock().await.clone()
    };  // Lock released immediately

    do_async_work(&data).await;  // No lock held
}
```

## Parking Lot for Sync Locks

```rust
use parking_lot::{Mutex, RwLock};  // Faster than std

// Use for non-async contexts or very short critical sections
let state = Arc::new(Mutex::new(State::new()));

fn quick_update(state: &Mutex<State>) {
    state.lock().counter += 1;
}
```

## Batching with Select

```rust
use tokio::select;
use tokio::time::{interval, Duration};

async fn batch_processor(mut rx: mpsc::Receiver<Item>) {
    let mut batch = Vec::with_capacity(100);
    let mut flush_interval = interval(Duration::from_millis(100));

    loop {
        select! {
            Some(item) = rx.recv() => {
                batch.push(item);
                if batch.len() >= 100 {
                    process_batch(&batch).await;
                    batch.clear();
                }
            }
            _ = flush_interval.tick() => {
                if !batch.is_empty() {
                    process_batch(&batch).await;
                    batch.clear();
                }
            }
        }
    }
}
```

## Guidelines

- Use bounded channels for backpressure
- Prefer `buffer_unordered` over sequential awaits
- Minimize lock scope in async code
- Consider channels over shared state
- Use semaphores for resource limiting
- Use `parking_lot` for sync-only locks

## Examples

See `hercules-local-algo/src/pipeline/prefetch.rs` for production patterns.
