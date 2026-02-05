---
name: rust-async-testing
description: Write async tests with tokio::test and configure multi-threaded test runtimes. Use when testing async code.
---

# Async Testing

Patterns for testing async Rust code with Tokio.

## Basic Async Test

```rust
#[tokio::test]
async fn test_fetch_data() {
    let result = fetch_data().await;
    assert!(result.is_ok());
    assert_eq!(result.unwrap().len(), 10);
}
```

## Multi-Threaded Test Runtime

```rust
// Test with multiple worker threads
#[tokio::test(flavor = "multi_thread", worker_threads = 2)]
async fn test_concurrent_operations() {
    let (a, b) = tokio::join!(
        operation_a(),
        operation_b(),
    );
    assert!(a.is_ok());
    assert!(b.is_ok());
}

// Current-thread runtime (simpler, deterministic)
#[tokio::test(flavor = "current_thread")]
async fn test_sequential() {
    let result = sequential_operation().await;
    assert!(result.is_ok());
}
```

## Test with Timeout

```rust
use tokio::time::{timeout, Duration};

#[tokio::test]
async fn test_with_timeout() {
    let result = timeout(Duration::from_secs(5), slow_operation())
        .await
        .expect("Operation timed out")
        .expect("Operation failed");

    assert_eq!(result, expected_value);
}
```

## Test Fixtures

```rust
struct TestContext {
    pool: PgPool,
    repo: VideoRepository,
}

impl TestContext {
    async fn new() -> Self {
        let pool = create_test_pool().await;
        let repo = VideoRepository::new(pool.clone());
        Self { pool, repo }
    }

    async fn cleanup(&self) {
        sqlx::query("DELETE FROM test_videos")
            .execute(&self.pool)
            .await
            .unwrap();
    }
}

#[tokio::test]
async fn test_with_fixture() {
    let ctx = TestContext::new().await;

    // Test code
    let result = ctx.repo.create_video("test-1").await;
    assert!(result.is_ok());

    // Cleanup
    ctx.cleanup().await;
}
```

## Testing Channels

```rust
use tokio::sync::mpsc;

#[tokio::test]
async fn test_channel_communication() {
    let (tx, mut rx) = mpsc::channel(10);

    // Spawn producer
    tokio::spawn(async move {
        for i in 0..5 {
            tx.send(i).await.unwrap();
        }
    });

    // Collect results
    let mut results = vec![];
    while let Some(value) = rx.recv().await {
        results.push(value);
    }

    assert_eq!(results, vec![0, 1, 2, 3, 4]);
}
```

## Testing with Mock Time

```rust
use tokio::time::{self, Duration, Instant};

#[tokio::test]
async fn test_with_paused_time() {
    time::pause();  // Pause time

    let start = Instant::now();

    // This completes instantly with paused time
    time::sleep(Duration::from_secs(100)).await;

    // Advance time manually
    time::advance(Duration::from_secs(50)).await;

    assert!(start.elapsed() >= Duration::from_secs(150));
}
```

## Testing Spawned Tasks

```rust
#[tokio::test]
async fn test_spawned_task() {
    let handle = tokio::spawn(async {
        compute_result().await
    });

    let result = handle.await.expect("Task panicked");
    assert_eq!(result, expected_value);
}

#[tokio::test]
async fn test_multiple_tasks() {
    let handles: Vec<_> = (0..10)
        .map(|i| tokio::spawn(async move { process(i).await }))
        .collect();

    let results: Vec<_> = futures::future::join_all(handles)
        .await
        .into_iter()
        .map(|r| r.expect("Task panicked"))
        .collect();

    assert_eq!(results.len(), 10);
}
```

## Testing Error Cases

```rust
#[tokio::test]
async fn test_error_handling() {
    let result = operation_that_fails().await;

    assert!(result.is_err());
    assert!(matches!(
        result.unwrap_err(),
        ProcessingError::NotFound(_)
    ));
}

#[tokio::test]
#[should_panic(expected = "connection refused")]
async fn test_panic_case() {
    connect_to_invalid_server().await;
}
```

## Integration Test Structure

```rust
// tests/integration_test.rs

use my_crate::{Config, Service};

async fn setup() -> Service {
    let config = Config::test_default();
    Service::new(config).await.unwrap()
}

#[tokio::test]
async fn test_full_workflow() {
    let service = setup().await;

    // Step 1
    let id = service.create_item("test").await.unwrap();

    // Step 2
    let item = service.get_item(&id).await.unwrap();
    assert_eq!(item.name, "test");

    // Step 3
    service.delete_item(&id).await.unwrap();
    assert!(service.get_item(&id).await.is_err());
}
```

## Test Organization

```rust
#[cfg(test)]
mod tests {
    use super::*;

    // Unit tests for specific functions
    mod parse_tests {
        use super::*;

        #[test]
        fn test_parse_valid() { ... }

        #[test]
        fn test_parse_invalid() { ... }
    }

    // Async tests
    mod async_tests {
        use super::*;

        #[tokio::test]
        async fn test_async_operation() { ... }
    }

    // Helper functions for tests
    fn create_test_data() -> TestData { ... }
}
```

## Guidelines

- Use `#[tokio::test]` for async tests
- Specify `flavor = "multi_thread"` for concurrent tests
- Use `time::pause()` for deterministic time-based tests
- Create test fixtures for complex setup
- Test both success and error cases
- Use `#[should_panic]` for panic tests
- Keep tests focused and independent

## Examples

See `hercules-local-algo/src/` for inline test modules.
