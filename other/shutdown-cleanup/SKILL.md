---
name: shutdown-cleanup
description: Implements graceful shutdown with pre_destruct hooks, handling Ctrl-C signals. Use when services need to flush queues, close connections, or release resources on app shutdown.
---

# Graceful Shutdown

## pre_destruct hook

```rust
use injectable::prelude::*;

#[injectable]
impl WorkerPool {
    #[injectable(ctor)]
    fn new() -> Self { Self { running: AtomicBool::new(false), pool: vec![] } }

    #[injectable(post_construct)]
    fn start(&self) {
        self.running.store(true, Ordering::SeqCst);
        println!("[WorkerPool] started");
    }

    #[injectable(pre_destruct)]
    async fn drain(&self) -> HookResult {
        self.running.store(false, Ordering::SeqCst);
        // Drain in-flight jobs…
        println!("[WorkerPool] drained and stopped");
        Ok(())
    }
}
```

## Trigger shutdown

```rust
// Calls all #[injectable(pre_destruct)] hooks in REVERSE construction order
container.shutdown().await?;
```

## With Ctrl-C signal

```rust
#[tokio::main]
async fn main() {
    let container = Arc::new(Container::builder().build().await.unwrap());

    // Warm up
    container.context().extract::<Inject<WorkerPool>>().await.unwrap();

    let container_clone = Arc::clone(&container);
    tokio::spawn(async move {
        tokio::signal::ctrl_c().await.unwrap();
        println!("Ctrl-C received, shutting down…");
        container_clone.shutdown().await.unwrap();
        std::process::exit(0);
    });

    // Run server…
    serve(container).await;
}
```

## Shutdown error handling

```rust
match container.shutdown().await {
    Ok(()) => println!("Clean shutdown"),
    Err(InjectableError::ShutdownFailed { errors }) => {
        for e in &errors {
            eprintln!("Shutdown error: {e}");
        }
        // All hooks still ran — errors are accumulated, not short-circuited
    }
    Err(e) => eprintln!("Unexpected error: {e}"),
}
```

## Hook execution order

Given construction order A → B → C (C depends on B depends on A):
- Shutdown order: C's `pre_destruct` → B's `pre_destruct` → A's `pre_destruct`
- Ensures dependents are shut down before their dependencies
