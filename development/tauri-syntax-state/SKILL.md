---
name: tauri-syntax-state
description: >
  Use when managing application state, sharing data between commands, or debugging state-related panics.
  Prevents unmanaged state panics, Mutex deadlocks, and unnecessary Arc wrapping around managed state.
  Covers app.manage(), State<T> injection, AppHandle.state(), thread-safe state with Mutex/RwLock, and initialization patterns.
  Keywords: tauri state, manage, State<T>, Mutex, RwLock, AppHandle, thread safety, state injection.
license: MIT
compatibility: "Designed for Claude Code. Requires Tauri 2.x with Rust and TypeScript."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# tauri-syntax-state

## Quick Reference

### State Registration (Tauri 2.x)

| Method | Context | Description |
|--------|---------|-------------|
| `Builder::manage(T)` | Builder chain | Register state during app construction |
| `App::manage(T)` | `setup()` hook | Register state that depends on app initialization |
| `AppHandle::manage(T)` | Any context | Register state at runtime (rare) |

### State Access

| Method | Context | Returns |
|--------|---------|---------|
| `State<'_, T>` | Command parameter | Injected automatically by Tauri |
| `app_handle.state::<T>()` | Any code with AppHandle | `State<'_, T>` (panics if not registered) |
| `app_handle.try_state::<T>()` | Any code with AppHandle | `Option<State<'_, T>>` (safe) |

### Thread-Safety Wrappers

| Wrapper | Use Case | Lock Method |
|---------|----------|-------------|
| `std::sync::Mutex<T>` | Mutable state, no `.await` while locked | `.lock().unwrap()` |
| `tokio::sync::Mutex<T>` | Mutable state with `.await` while locked | `.lock().await` |
| `std::sync::RwLock<T>` | Read-heavy access, concurrent readers | `.read().unwrap()` / `.write().unwrap()` |
| None (immutable) | Read-only config data | Direct field access |

---

## Critical Warnings

**NEVER** use `State<'_, T>` when you registered `Mutex<T>` — the type must match EXACTLY or Tauri panics at runtime, not at compile time. If you registered `Mutex<Counter>`, the command parameter must be `State<'_, Mutex<Counter>>`.

**NEVER** wrap managed state in `Arc` — Tauri already wraps all managed state in `Arc` internally. Using `app.manage(Arc::new(data))` adds a redundant layer.

**NEVER** lock the same `Mutex` twice in the same call chain — this causes a deadlock. If a function holding a lock calls another function that also locks, the thread blocks forever.

**NEVER** use `tokio::sync::Mutex` unless you need to hold the lock across `.await` points — `std::sync::Mutex` is more efficient for synchronous access.

**ALWAYS** register state before any command tries to access it — accessing unregistered state via `State<T>` causes a runtime panic.

**ALWAYS** match the exact registered type in `State<'_, T>` — including all wrappers like `Mutex`, `RwLock`, etc.

---

## Essential Patterns

### Pattern 1: Immutable State (Read-Only Config)

```rust
// Tauri 2.x — No Mutex needed for read-only data
struct AppConfig {
    api_url: String,
    max_retries: u32,
}

tauri::Builder::default()
    .manage(AppConfig {
        api_url: "https://api.example.com".into(),
        max_retries: 3,
    })
    .invoke_handler(tauri::generate_handler![get_api_url])

#[tauri::command]
fn get_api_url(config: tauri::State<'_, AppConfig>) -> String {
    config.api_url.clone()
}
```

### Pattern 2: Mutable State with std::sync::Mutex

```rust
// Tauri 2.x — Standard pattern for mutable state
use std::sync::Mutex;

#[derive(Default)]
struct Counter {
    value: u32,
}

tauri::Builder::default()
    .manage(Mutex::new(Counter::default()))
    .invoke_handler(tauri::generate_handler![increment, get_count])

#[tauri::command]
fn increment(state: tauri::State<'_, Mutex<Counter>>) -> u32 {
    let mut counter = state.lock().unwrap();
    counter.value += 1;
    counter.value
}

#[tauri::command]
fn get_count(state: tauri::State<'_, Mutex<Counter>>) -> u32 {
    state.lock().unwrap().value
}
```

### Pattern 3: Async Commands with tokio::sync::Mutex

```rust
// Tauri 2.x — Use tokio Mutex when holding lock across .await
use tokio::sync::Mutex;

struct Database {
    connection: String,
}

#[tauri::command]
async fn save_record(
    state: tauri::State<'_, Mutex<Database>>,
    data: String,
) -> Result<(), String> {
    let db = state.lock().await;
    // ... perform async database operations while holding lock ...
    Ok(())
}
```

### Pattern 4: RwLock for Read-Heavy Access

```rust
// Tauri 2.x — Multiple concurrent readers, exclusive writers
use std::sync::RwLock;

struct AppData {
    items: Vec<String>,
}

tauri::Builder::default()
    .manage(RwLock::new(AppData { items: vec![] }))

#[tauri::command]
fn list_items(state: tauri::State<'_, RwLock<AppData>>) -> Vec<String> {
    let data = state.read().unwrap(); // Multiple readers OK
    data.items.clone()
}

#[tauri::command]
fn add_item(state: tauri::State<'_, RwLock<AppData>>, item: String) {
    let mut data = state.write().unwrap(); // Exclusive access
    data.items.push(item);
}
```

### Pattern 5: State Initialization in setup()

```rust
// Tauri 2.x — State that depends on app paths or runtime info
tauri::Builder::default()
    .setup(|app| {
        let db_path = app.path().app_data_dir()?.join("data.db");
        app.manage(Database::new(&db_path)?);
        Ok(())
    })
```

### Pattern 6: Accessing State via AppHandle

```rust
// Tauri 2.x — Access state outside of commands
use std::sync::Mutex;

fn background_task(handle: tauri::AppHandle) {
    let state = handle.state::<Mutex<Counter>>();
    let mut counter = state.lock().unwrap();
    counter.value += 1;
}

// Safe variant — returns None if state not registered
fn maybe_access(handle: &tauri::AppHandle) {
    if let Some(state) = handle.try_state::<Mutex<Counter>>() {
        let counter = state.lock().unwrap();
        println!("Count: {}", counter.value);
    }
}
```

---

## Manager Trait

The `Manager` trait provides `state()` and `try_state()`. It is implemented by:

| Type | Description |
|------|-------------|
| `App` | Available in `setup()` |
| `AppHandle` | Cloneable, Send + Sync, use in threads |
| `Window` | Window instance |
| `Webview` | Webview instance |
| `WebviewWindow` | Combined window + webview |

All of these types can call `.state::<T>()` and `.try_state::<T>()`.

---

## Multiple State Types

Register multiple state types independently:

```rust
tauri::Builder::default()
    .manage(AppConfig { /* ... */ })
    .manage(Mutex::new(UserSession::default()))
    .manage(RwLock::new(DocumentStore::default()))
    .invoke_handler(tauri::generate_handler![
        get_config,
        login,
        get_document,
    ])

#[tauri::command]
fn get_config(config: tauri::State<'_, AppConfig>) -> String {
    config.api_url.clone()
}

#[tauri::command]
fn login(session: tauri::State<'_, Mutex<UserSession>>, user: String) {
    let mut s = session.lock().unwrap();
    s.username = user;
}
```

Each type is registered and accessed independently. There is no limit on the number of state types.

---

## Reference Links

- [references/methods.md](references/methods.md) — Complete state management API signatures
- [references/examples.md](references/examples.md) — Working code examples for common state patterns
- [references/anti-patterns.md](references/anti-patterns.md) — What NOT to do, with WHY explanations

### Official Sources

- https://v2.tauri.app/develop/state-management/
- https://docs.rs/tauri/2/tauri/struct.State.html
- https://docs.rs/tauri/2/tauri/trait.Manager.html
