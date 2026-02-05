---
name: rust-dev-guidelines
description: Idiomatic Rust development patterns for async applications. Covers error handling with Result/Option, ownership and borrowing, async/await with Tokio, traits and generics, serde serialization, Arc/Mutex for shared state, and clippy best practices. Use when writing Rust code, refactoring, handling errors, or implementing async patterns.
---

# Rust Development Guidelines

## Purpose

Comprehensive guide for writing idiomatic Rust code in this project. Focuses on patterns used in async Discord bots with external API integrations.

## When to Use

- Writing new Rust code
- Refactoring existing code
- Implementing error handling
- Working with async/await
- Using shared state (Arc, Mutex, RwLock)
- Serialization with serde

---

## Error Handling

### Use `Result<T, E>` for Fallible Operations

```rust
// GOOD: Return Result for operations that can fail
pub async fn load_killmail(&self, url: String) -> Result<Killmail, String> {
    let response = self.client
        .get(&url)
        .send()
        .await
        .map_err(|e| format!("HTTP error: {}", e))?;

    response.json::<Killmail>()
        .await
        .map_err(|e| format!("Parse error: {}", e))
}

// BAD: Using unwrap/expect in production code paths
let data = response.json().await.unwrap(); // Panics on error!
```

### Use `?` Operator for Propagation

```rust
// GOOD: Clean error propagation
async fn process(&self) -> Result<Data, Error> {
    let response = self.fetch().await?;
    let parsed = self.parse(response)?;
    Ok(parsed)
}

// AVOID: Verbose match chains
async fn process(&self) -> Result<Data, Error> {
    let response = match self.fetch().await {
        Ok(r) => r,
        Err(e) => return Err(e),
    };
    // ...
}
```

### Use `Option<T>` for Optional Values

```rust
// GOOD: Use Option for values that may not exist
pub fn get_system_name(&self, id: u64) -> Option<&String> {
    self.systems.get(&id)
}

// Usage with combinators
let name = app_state.get_system_name(system_id)
    .unwrap_or(&"Unknown".to_string());

// Or with if-let
if let Some(name) = app_state.get_system_name(system_id) {
    info!("System: {}", name);
}
```

See [resources/error-handling.md](resources/error-handling.md) for custom error types and `thiserror` patterns.

---

## Async Patterns (Tokio)

### Async Functions

```rust
// Mark async functions with async keyword
pub async fn fetch_data(&self) -> Result<Data, Error> {
    let response = self.client.get(url).send().await?;
    Ok(response.json().await?)
}
```

### Spawning Tasks

```rust
// Fire-and-forget background task
tokio::spawn(async move {
    if let Err(e) = process_item(item).await {
        error!("Background task failed: {}", e);
    }
});

// Task with join handle
let handle = tokio::spawn(async move {
    expensive_computation().await
});
let result = handle.await?;
```

### Concurrent Operations

```rust
// Run multiple futures concurrently
let (result1, result2) = tokio::join!(
    fetch_user(user_id),
    fetch_permissions(user_id)
);

// Select first to complete
tokio::select! {
    result = async_operation() => handle(result),
    _ = tokio::time::sleep(Duration::from_secs(5)) => timeout(),
}
```

See [resources/async-patterns.md](resources/async-patterns.md) for channels, timeouts, and cancellation.

---

## Ownership and Borrowing

### Prefer References Over Clones

```rust
// GOOD: Borrow when you don't need ownership
fn process_data(data: &ZkData) {
    // Read-only access
}

// AVOID: Unnecessary clone
fn process_data(data: ZkData) {
    // Takes ownership when not needed
}
```

### Use `Arc` for Shared Ownership

```rust
// Shared state across async tasks
let app_state = Arc::new(AppState::new(...));

// Clone Arc (cheap, just increments refcount)
let state_clone = app_state.clone();
tokio::spawn(async move {
    state_clone.do_something().await;
});
```

### Use `RwLock` for Interior Mutability

```rust
// Multiple readers OR single writer
pub struct AppState {
    pub subscriptions: RwLock<HashMap<GuildId, Vec<Subscription>>>,
}

// Reading (many concurrent readers allowed)
let subs = app_state.subscriptions.read().unwrap();
let guild_subs = subs.get(&guild_id);

// Writing (exclusive access)
let mut subs = app_state.subscriptions.write().unwrap();
subs.insert(guild_id, new_subscriptions);
```

---

## Structs and Serialization

### Derive Common Traits

```rust
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Killmail {
    pub killmail_id: u64,
    pub killmail_time: String,
    pub solar_system_id: u64,
    pub victim: Victim,
    pub attackers: Vec<Attacker>,
}
```

### Use `#[serde(...)]` for JSON Customization

```rust
#[derive(Deserialize)]
pub struct EsiResponse {
    #[serde(rename = "killmail_id")]
    pub id: u64,

    #[serde(default)]
    pub optional_field: Option<String>,

    #[serde(skip_serializing_if = "Option::is_none")]
    pub maybe_present: Option<i32>,
}
```

---

## Pattern Matching

### Use `match` for Enums

```rust
match result {
    Ok(data) => process(data),
    Err(KillmailError::NotFound) => warn!("Not found"),
    Err(KillmailError::RateLimited) => retry_later(),
    Err(e) => error!("Unexpected: {}", e),
}
```

### Use `if let` for Single Patterns

```rust
// When you only care about one variant
if let Some(ship_name) = get_ship_name(type_id) {
    info!("Ship: {}", ship_name);
}

// Instead of verbose match
match get_ship_name(type_id) {
    Some(name) => info!("Ship: {}", name),
    None => {},
}
```

---

## Iterators and Combinators

### Prefer Iterator Methods Over Loops

```rust
// GOOD: Functional style
let high_value_kills: Vec<_> = killmails
    .iter()
    .filter(|k| k.zkb.total_value > 1_000_000_000.0)
    .collect();

// Also good when more readable
let mut results = Vec::new();
for km in killmails {
    if km.zkb.total_value > 1_000_000_000.0 {
        results.push(km);
    }
}
```

### Common Combinators

```rust
// Transform
let names: Vec<String> = items.iter().map(|i| i.name.clone()).collect();

// Filter + Transform
let valid: Vec<_> = items.iter()
    .filter_map(|i| i.optional_field.as_ref())
    .collect();

// Find single item
let found = items.iter().find(|i| i.id == target_id);

// Check condition
let has_caps = attackers.iter().any(|a| is_capital(a.ship_type_id));
```

---

## Logging with Tracing

```rust
use tracing::{info, warn, error, debug};

// Structured logging
info!(kill_id = %kill_id, "Processing killmail");
warn!(guild_id = %guild_id, "No subscriptions found");
error!(error = %e, "Failed to send message");

// With spans for context
let span = tracing::info_span!("process_kill", kill_id = %kill_id);
let _guard = span.enter();
```

---

## Project-Specific Conventions

### This Codebase Uses

1. **Serenity 0.11** for Discord - see [serenity-discord-bot skill](../serenity-discord-bot/SKILL.md)
2. **Reqwest** for HTTP with `rustls-tls`
3. **Moka** for caching
4. **Config files** as JSON in `config/` directory

### File Organization

```
src/
  main.rs          # Entry point
  lib.rs           # Core logic, run() function
  config.rs        # Configuration loading/saving
  models.rs        # Data structures (Killmail, etc.)
  processor.rs     # Killmail → subscription matching
  discord_bot.rs   # Discord event handling
  esi.rs           # EVE ESI API client
  redis_q.rs       # zkillboard RedisQ listener
  commands/        # Discord slash commands
    mod.rs
    subscribe.rs
    unsubscribe.rs
    diag.rs
```

---

## Quick Reference

| Pattern | Use For |
|---------|---------|
| `Result<T, E>` | Operations that can fail |
| `Option<T>` | Values that may not exist |
| `?` operator | Clean error propagation |
| `Arc<T>` | Shared ownership across threads |
| `RwLock<T>` | Mutable shared state |
| `#[derive(...)]` | Auto-implement common traits |
| `.iter().filter().map()` | Transform collections |

---

## Reference Files

- [resources/error-handling.md](resources/error-handling.md) - Custom errors, thiserror, anyhow
- [resources/async-patterns.md](resources/async-patterns.md) - Tokio channels, timeouts, select
- [resources/testing.md](resources/testing.md) - Unit tests, integration tests, mocking
