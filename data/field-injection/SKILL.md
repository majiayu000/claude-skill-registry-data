---
name: field-injection
description: Implements field injection with #[injectable] on structs. Use when adding injectable to a struct, wiring Inject<T> or Arc<T> fields, or getting "non-Inject<T> fields require #[injectable(inject)]" errors.
---

# Field Injection

## Rules

- `Inject<T>` fields → auto-injected, no annotation
- `Arc<T>` or `T` fields → require `#[injectable(inject)]`
- External/non-injectable fields → use `#[injectable(ctor)]` constructor instead

## Basic patterns

```rust
use injectable::prelude::*;

// ── Inject<T>: auto-injected (most common) ──────────────────────────────────
#[injectable]
struct UserService {
    db:    Inject<Database>,   // no #[injectable(inject)] needed
    cache: Inject<Cache>,
}

// ── Arc<T>: explicit #[injectable(inject)] ──────────────────────────────────────────────
#[injectable]
struct RepoService {
    #[injectable(inject)]
    db: Arc<Database>,
}

// ── Fields with factories ────────────────────────────────────────────────────
#[injectable(factory)]
async fn make_pool(cfg: Inject<AppConfig>) -> Result<Pool<Sqlite>, sqlx::Error> {
    sqlx::SqlitePool::connect(&cfg.db_url).await
}

#[injectable]
struct Database {
    #[injectable(inject(use_factory_async = self::make_pool))]
    pool: Pool<Sqlite>,
}

// ── Non-injectable fields → use constructor ──────────────────────────────────
struct Service {
    db:   Inject<Database>,
    name: String,              // String is not injectable
}

#[injectable]
impl Service {
    #[injectable(ctor)]
    fn new(db: Inject<Database>) -> Self {
        Self { db, name: "default".into() }
    }
}
```

## Scoping

```rust
#[injectable]                          // Singleton (default)
struct Cache { db: Inject<Database> }

#[injectable(scope = Transient)]       // Fresh instance each resolution
struct RequestLogger { db: Inject<Database> }
```

## Resolve

```rust
let container = Container::builder().build().await?;
let svc = container.resolve::<UserService>().await?;
// or via context (uses singleton cache):
let svc: Inject<UserService> = container.context().extract().await?;
```

See [guides/02-field-injection.md](../../guides/02-field-injection.md) for full reference.
