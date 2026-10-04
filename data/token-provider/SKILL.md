---
name: token-provider
description: Register and resolve multiple DynProvider instances of the same type using string tokens. Use when you need e.g. multiple database pools, HTTP clients, or Redis connections differentiated by name ("primary", "replica", "analytics").
---

# Token-Based DynProvider Registration

## Pattern

```rust
use injectable::prelude::*;

// Register multiple pools of the same type with different tokens
let container = Container::builder()
    .register("primary",   DynProvider::new(|| async { Ok(primary_pool().await?) }))
    .register("replica",   DynProvider::new(|| async { Ok(replica_pool().await?) }))
    .build().await?;

// Resolve by token
let primary: Pool = container.resolve_external_with_token("primary").await?;
let replica:  Pool = container.resolve_external_with_token("replica").await?;
```

## Default token

Use `""` (or `DEFAULT_TOKEN`) for the single unnamed provider:

```rust
builder.register("", DynProvider::sync(|| Ok(Client::new())));
let client: Client = container.resolve_external().await?;  // queries token ""
```

## Inside a factory closure

```rust
.register("router", DynProvider::with_ctx(|ctx| async move {
    let primary: Pool = ctx.resolve_external_with_token("primary").await?;
    let replica:  Pool = ctx.resolve_external_with_token("replica").await?;
    Ok(DbRouter::new(primary, replica))
}))
```

## Registry directly (tests)

```rust
let mut registry = ProviderRegistry::new();
registry.register("db-a", DynProvider::from_value(DbA::new()));
registry.register("db-b", DynProvider::from_value(DbB::new()));
let ctx = ResolveContext::new(Arc::new(EmptySingletonStore), Arc::new(registry));
let a: DbA = ctx.resolve_external_with_token("db-a").await?;
```

## Check presence

```rust
registry.has::<T>()                     // default token
registry.has_with_token::<T>("primary") // named token
```

## Duplicate rules

- Same `(type, token)` twice → duplicate warning at `build()`.
- Different tokens for same type → **not** duplicates, both allowed.
- `register_or_replace(token, …)` → silent override, no warning.

See [guides/11-token-based-providers.md](../../guides/11-token-based-providers.md).
