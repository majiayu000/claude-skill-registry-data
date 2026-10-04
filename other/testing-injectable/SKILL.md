---
name: testing-injectable
description: Tests code that uses injectable for dependency injection. Use when writing unit or integration tests that need mock services, pre-built instances, or container isolation.
---

# Testing with injectable

## Pre-built mock instances

```rust
use injectable::prelude::*;

#[derive(Clone, Default)]
struct MockDb { calls: Arc<AtomicUsize> }

let container = Container::builder()
    .register(DynProvider::from_value(MockDb::default()))
    .build().await?;

let db: MockDb = container.resolve_external().await?;
```

## Optional dependency patterns

```rust
// In tests, leave optional deps unregistered — they resolve to None.
let container = Container::builder().build().await?;
let ctx = container.context();
let maybe: Option<Inject<MetricsBackend>> = ctx.extract().await?;
assert!(maybe.is_none());
```

## Container per test (isolation)

```rust
#[tokio::test]
async fn test_user_service() {
    // Each test gets its own fresh container.
    let container = Container::builder()
        .register(DynProvider::from_value(MockDatabase::default()))
        .build().await.unwrap();

    let svc = container.resolve::<UserService>().await.unwrap();
    // …
}
```

## Verify singleton semantics

```rust
#[tokio::test]
async fn test_singleton() {
    let container = Container::builder().build().await.unwrap();
    let ctx = container.context();

    let a: Inject<Database> = ctx.extract().await.unwrap();
    let b: Inject<Database> = ctx.extract().await.unwrap();

    assert!(a.ptr_eq(&b), "Database must be a singleton");
}
```

## Test registered types

```rust
let container = Container::builder().build().await.unwrap();
assert!(container.registered_types().contains(&"UserService"));
```

## Test missing dependency

```rust
let result = container.try_resolve::<UnregisteredService>().await.unwrap();
assert!(result.is_none());
```

## Test lifecycle hooks ran

```rust
static POST_CONSTRUCT_CALLED: AtomicBool = AtomicBool::new(false);

struct TestService;
#[injectable]
impl TestService {
    #[injectable(ctor)] fn new() -> Self { Self }
    #[injectable(post_construct)] fn init(&self) { POST_CONSTRUCT_CALLED.store(true, Ordering::SeqCst); }
}

let container = Container::builder().build().await.unwrap();
Inject::<TestService>::extract(container.context()).await.unwrap();
assert!(POST_CONSTRUCT_CALLED.load(Ordering::SeqCst));
```

See [guides/10-testing.md](../../guides/10-testing.md).
