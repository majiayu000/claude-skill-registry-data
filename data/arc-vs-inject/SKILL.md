---
name: arc-vs-inject
description: Chooses between Arc<T> and Inject<T> for injectable fields and parameters. Use when deciding how to declare a dependency field or when getting type mismatch errors between Arc and Inject.
---

# Arc\<T\> vs Inject\<T\>

## Decision guide

| Situation | Use |
|---|---|
| Field in `#[injectable]` struct, auto-injected | `Inject<T>` (no annotation) |
| Field in `#[injectable]` struct, explicit | `Arc<T>` with `#[injectable(inject)]` |
| Constructor parameter | `Inject<T>` (auto) or `Arc<T>` with `#[injectable(inject)]` |
| Axum handler parameter | `Inject<T>` (implements FromRequestParts) |
| Storing in a non-injectable struct | `Arc<T>` (plain Arc, no DI) |
| Passing to third-party code | `Arc<T>` (convert from Inject<T>) |
| Testing singleton identity | Both work; `ptr_eq` available on both |

## Inject\<T\>

```rust
use injectable::prelude::*;

#[injectable]
struct UserService {
    db: Inject<Database>,   // auto-injected, no annotation
}

// Deref to call methods:
user_service.db.query("SELECT 1").await?;

// Get Arc<T>:
let arc: Arc<Database> = user_service.db.arc();
```

## Arc\<T\> with #[injectable(inject)]

```rust
#[injectable]
struct RepoService {
    #[injectable(inject)]
    db: Arc<Database>,
}

// Call methods directly (no Deref wrapper):
repo_service.db.query("SELECT 1").await?;
```

## Converting between them

```rust
// Inject<T> → Arc<T>
let inject: Inject<Database> = ctx.extract().await?;
let arc: Arc<Database> = inject.into_inner();   // consumes
let arc: Arc<Database> = inject.arc();           // clones

// Arc<T> → Inject<T>
let inject: Inject<Database> = Inject::new(arc);
let inject: Inject<Database> = arc.into();
```

## In constructors

```rust
#[injectable]
impl Service {
    #[injectable(ctor)]
    fn new(
        db:    Inject<Database>,       // auto-injected
        #[injectable(inject)] cache: Arc<Cache>,   // explicit #[injectable(inject)] required for Arc
    ) -> Self {
        Self { db, cache }
    }
}
```

## Summary

- Prefer `Inject<T>` for DI fields — it's the "DI-aware" smart pointer
- Use `Arc<T>` with `#[injectable(inject)]` when you need a plain `Arc` (passing to non-DI code)
- Never mix up: `Inject<T>` won't auto-coerce to `Arc<T>` in function signatures
