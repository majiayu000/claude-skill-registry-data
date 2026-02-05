---
name: rust-graceful-shutdown
description: Implement graceful shutdown with signal handling and broadcast channels. Use when building long-running services or daemons.
---

# Graceful Shutdown

Patterns for clean service shutdown with proper resource cleanup.

## Signal Handling

```rust
use tokio::signal;

async fn shutdown_signal() {
    let ctrl_c = async {
        signal::ctrl_c()
            .await
            .expect("Failed to install Ctrl+C handler");
    };

    #[cfg(unix)]
    let terminate = async {
        signal::unix::signal(signal::unix::SignalKind::terminate())
            .expect("Failed to install SIGTERM handler")
            .recv()
            .await;
    };

    #[cfg(not(unix))]
    let terminate = std::future::pending::<()>();

    tokio::select! {
        _ = ctrl_c => {},
        _ = terminate => {},
    }
}
```

## Broadcast Channel Pattern

```rust
use tokio::sync::broadcast;

async fn main() -> Result<()> {
    let (shutdown_tx, _) = broadcast::channel::<()>(1);

    // Spawn workers with shutdown receivers
    let worker1 = spawn_worker(shutdown_tx.subscribe());
    let worker2 = spawn_worker(shutdown_tx.subscribe());
    let server = spawn_server(shutdown_tx.subscribe());

    // Wait for shutdown signal
    shutdown_signal().await;
    tracing::info!("Shutdown signal received");

    // Signal all receivers
    drop(shutdown_tx);

    // Wait for graceful shutdown with timeout
    let shutdown_timeout = Duration::from_secs(30);
    let _ = tokio::time::timeout(
        shutdown_timeout,
        futures::future::join_all([worker1, worker2, server]),
    )
    .await;

    tracing::info!("Shutdown complete");
    Ok(())
}

async fn spawn_worker(mut shutdown: broadcast::Receiver<()>) {
    loop {
        tokio::select! {
            _ = shutdown.recv() => {
                tracing::info!("Worker received shutdown");
                break;
            }
            _ = do_work() => {}
        }
    }

    // Cleanup
    cleanup_resources().await;
}
```

## CancellationToken Pattern

```rust
use tokio_util::sync::CancellationToken;

async fn main() -> Result<()> {
    let cancel = CancellationToken::new();

    // Spawn with cancellation
    let worker = {
        let cancel = cancel.clone();
        tokio::spawn(async move {
            worker_loop(cancel).await
        })
    };

    // Wait for shutdown
    shutdown_signal().await;
    cancel.cancel();

    // Wait for worker
    let _ = worker.await;
    Ok(())
}

async fn worker_loop(cancel: CancellationToken) {
    loop {
        tokio::select! {
            _ = cancel.cancelled() => break,
            result = process_next() => {
                if let Err(e) = result {
                    tracing::error!("Processing error: {}", e);
                }
            }
        }
    }
}
```

## Cleanup with Drop Guards

```rust
struct CleanupGuard {
    resource: Resource,
}

impl Drop for CleanupGuard {
    fn drop(&mut self) {
        // Sync cleanup - runs even on panic
        self.resource.cleanup_sync();
    }
}

async fn with_cleanup() -> Result<()> {
    let resource = Resource::new().await?;
    let _guard = CleanupGuard { resource: resource.clone() };

    // Work with resource...
    // Guard ensures cleanup on any exit path
    Ok(())
}
```

## Database Connection Cleanup

```rust
async fn shutdown_with_db(pool: PgPool, shutdown: broadcast::Receiver<()>) {
    // Wait for shutdown signal
    let _ = shutdown.recv().await;

    // Reset in-progress work
    reset_stuck_records(&pool).await;

    // Close pool gracefully
    pool.close().await;
}

async fn reset_stuck_records(pool: &PgPool) -> Result<()> {
    // Reset EMBEDDING_IN_PROGRESS → EXTRACTION_COMPLETE
    sqlx::query(
        "UPDATE video_processing SET status = 'EXTRACTION_COMPLETE'
         WHERE status = 'EMBEDDING_IN_PROGRESS'"
    )
    .execute(pool)
    .await?;

    // Reset EXTRACTION_IN_PROGRESS → PENDING
    sqlx::query(
        "UPDATE video_processing SET status = 'PENDING'
         WHERE status = 'EXTRACTION_IN_PROGRESS'"
    )
    .execute(pool)
    .await?;

    Ok(())
}
```

## Heartbeat for Stale Detection

```rust
async fn heartbeat_loop(
    pool: PgPool,
    video_id: String,
    mut shutdown: broadcast::Receiver<()>,
) {
    let mut interval = tokio::time::interval(Duration::from_secs(30));

    loop {
        tokio::select! {
            _ = shutdown.recv() => break,
            _ = interval.tick() => {
                let _ = sqlx::query(
                    "UPDATE video_processing
                     SET pc_heartbeat = NOW()
                     WHERE video_id = $1"
                )
                .bind(&video_id)
                .execute(&pool)
                .await;
            }
        }
    }
}
```

## Complete Example

```rust
#[tokio::main]
async fn main() -> Result<()> {
    let (shutdown_tx, _) = broadcast::channel::<()>(1);

    // Initialize resources
    let pool = create_db_pool().await?;
    let storage = create_storage().await?;

    // Spawn main processing loop
    let processor = {
        let pool = pool.clone();
        let shutdown = shutdown_tx.subscribe();
        tokio::spawn(async move {
            processing_loop(pool, shutdown).await
        })
    };

    // Wait for shutdown
    shutdown_signal().await;
    tracing::info!("Initiating graceful shutdown...");

    // Signal shutdown
    drop(shutdown_tx);

    // Wait with timeout
    match tokio::time::timeout(Duration::from_secs(30), processor).await {
        Ok(_) => tracing::info!("Processor shut down cleanly"),
        Err(_) => tracing::warn!("Processor shutdown timed out"),
    }

    // Final cleanup
    pool.close().await;
    tracing::info!("Shutdown complete");

    Ok(())
}
```

## Guidelines

- Always handle both SIGINT (Ctrl+C) and SIGTERM
- Use broadcast channels for multi-receiver shutdown
- Set reasonable shutdown timeouts
- Reset in-progress database records on shutdown
- Use heartbeats for stale work detection
- Clean up external resources (DB, files, connections)

## Examples

See `hercules-local-algo/src/main.rs` for production shutdown handling.
