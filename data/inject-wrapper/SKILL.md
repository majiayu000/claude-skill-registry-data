---
name: inject-wrapper
description: Works with the Inject<T> wrapper type — cloning, destructuring, converting to Arc, and using ptr_eq for singleton assertions. Use when accessing the inner Arc, passing to non-DI code, or testing singleton semantics.
---

# `Inject<T>` Wrapper

`Inject<T>` wraps `Arc<T>` and implements `Deref<Target = T>`.

## Common operations

```rust
use injectable::prelude::*;

let inject: Inject<Database> = ctx.extract().await?;

// Call methods directly via Deref
inject.query("SELECT 1").await?;

// Get Arc<T>
let arc: Arc<Database> = inject.arc();         // clones the Arc
let arc: Arc<Database> = inject.into_inner();  // consumes Inject<T>
let arc: &Arc<Database> = inject.inner();      // borrows the Arc

// Clone (cheap — just clones the Arc)
let copy: Inject<Database> = inject.clone();

// Convert
let arc: Arc<Database> = inject.into();
let inject: Inject<Database> = arc.into();
```

## Destructuring (Axum pattern)

```rust
// Extract Arc<T> directly in handler signature:
async fn handler(Inject(db): Inject<Database>) -> impl IntoResponse {
    // db: Arc<Database>
    db.query("SELECT 1").await;
}
```

## Singleton assertion

```rust
let a: Inject<Database> = ctx.extract().await?;
let b: Inject<Database> = ctx.extract().await?;
assert!(a.ptr_eq(&b), "Database must be the same singleton instance");
```

## AsRef / Borrow

```rust
fn needs_ref(db: impl AsRef<Database>) { /* … */ }
needs_ref(&inject);   // works because Inject<T>: AsRef<T>

use std::borrow::Borrow;
fn needs_borrow<T: Borrow<Database>>(t: T) { /* … */ }
needs_borrow(inject); // works because Inject<T>: Borrow<T>
```

## HashMap key / PartialEq

```rust
let mut map: HashMap<Inject<UserId>, String> = HashMap::new();
// Inject<T>: Hash + Eq when T: Hash + Eq
map.insert(user_id_inject, "Alice".into());
```

See [guides/06-inject-wrapper.md](../../guides/06-inject-wrapper.md).
