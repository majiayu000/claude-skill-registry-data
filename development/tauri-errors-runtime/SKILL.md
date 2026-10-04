---
name: tauri-errors-runtime
description: >
  Use when encountering runtime panics, state errors, or unexpected app crashes in Tauri 2.
  Prevents unhandled unwrap() panics in production and unmanaged state type mismatches that crash the app.
  Covers window not found, state not managed panics, plugin not initialized, asset resolution, event name validation, and panic handling.
  Keywords: tauri runtime error, panic, state not managed, window not found, plugin not initialized, unwrap, crash.
license: MIT
compatibility: "Designed for Claude Code. Requires Tauri 2.x."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# tauri-errors-runtime

## Quick Diagnosis

When a Tauri 2 app crashes or behaves unexpectedly at runtime, identify the error category:

```
Runtime Error Categories:
1. State panics       --> Type mismatch, unmanaged state
2. IPC errors         --> Command not found, permission denied, argument mismatch
3. Window errors      --> Window/webview not found, already destroyed
4. Plugin errors      --> Plugin not initialized, missing permissions
5. Event errors       --> Invalid event name, listener leaks
6. Asset errors       --> File not found, protocol not configured
7. Panic/crash        --> Unhandled panic, thread panic
```

**ALWAYS** check the terminal/console output -- Tauri prints panics and errors to stderr.

**NEVER** ignore `unwrap()` calls in production code -- they cause panics that crash the app.

---

## Error Lookup Table: State Management

### ERR-R001: State type mismatch panic

**Error**: `state not managed for field "state" on command "my_command"` or `called Option::unwrap() on a None value` at runtime.

**Cause**: The type in `State<'_, T>` does not match the type passed to `manage()`. This is a RUNTIME panic, not a compile error.

```rust
// WRONG -- register Mutex<Counter>, access as Counter
app.manage(Mutex::new(Counter::default()));

#[tauri::command]
fn bad(state: State<'_, Counter>) { }  // PANIC at runtime!

// CORRECT -- types must match exactly
app.manage(Mutex::new(Counter::default()));

#[tauri::command]
fn good(state: State<'_, Mutex<Counter>>) {
    let mut counter = state.lock().unwrap();
    counter.value += 1;
}
```

**ALWAYS** ensure the generic type in `State<'_, T>` matches exactly what was passed to `manage()`.

### ERR-R002: State not registered

**Error**: `state not managed for field "state"` -- app panics when the command is first invoked.

**Cause**: Forgot to call `.manage()` on the Builder or in `setup()`.

**Fix**: ALWAYS register state before it is accessed:

```rust
tauri::Builder::default()
    .manage(AppConfig { api_url: "https://api.example.com".into() })
    .manage(Mutex::new(Counter::default()))
    // ... state must be registered before commands use it
```

### ERR-R003: Deadlock from nested Mutex locks

**Error**: App freezes (hangs) -- no panic, no error, just unresponsive.

**Cause**: Locking the same `Mutex` twice in the same call chain.

**Fix**: NEVER lock the same Mutex more than once in a scope. Use `RwLock` for read-heavy patterns:

```rust
// WRONG -- deadlock
#[tauri::command]
fn bad(state: State<'_, Mutex<Data>>) {
    let data = state.lock().unwrap();
    helper(&state);  // Tries to lock again -> DEADLOCK
}

fn helper(state: &Mutex<Data>) {
    let data = state.lock().unwrap();  // Hangs forever
}

// CORRECT -- lock once, pass the guard
#[tauri::command]
fn good(state: State<'_, Mutex<Data>>) {
    let mut data = state.lock().unwrap();
    helper(&mut data);
}

fn helper(data: &mut Data) {
    // Works with the already-locked data
}
```

### ERR-R004: Wrapping state in unnecessary Arc

**Error**: No error, but redundant allocation. Can cause confusion when accessing state.

**Cause**: Tauri already wraps managed state in `Arc` internally.

```rust
// WRONG -- double Arc
app.manage(Arc::new(MyState::default()));

// CORRECT -- Tauri handles Arc internally
app.manage(MyState::default());
```

---

## Error Lookup Table: IPC / Commands

### ERR-R010: Command not found at runtime

**Error**: Frontend receives `command my_command not found` or promise rejects with "command not allowed."

**Causes** (check in order):
1. Command not registered in `generate_handler![]`
2. Permission not granted in capabilities file
3. Command name mismatch (Rust uses snake_case, JS passes the same name)

**Fix checklist**:

```
[ ] Command listed in generate_handler![my_command]
[ ] Permission defined in src-tauri/permissions/*.toml
[ ] Permission referenced in src-tauri/capabilities/default.json
[ ] Command name matches exactly (including module path for plugin commands)
```

### ERR-R011: Argument type mismatch

**Error**: `invalid type: expected X, found Y` or `missing field "fieldName"` at runtime.

**Cause**: Frontend passes wrong types or wrong key names to `invoke()`.

**Rules**:
- Frontend keys MUST be camelCase (Tauri auto-converts to Rust snake_case)
- Types must match: JS `number` -> Rust `i32`/`u64`/`f64`, JS `string` -> Rust `String`, etc.

```typescript
// WRONG -- snake_case keys
await invoke('save_file', { file_path: '/doc.txt' });

// CORRECT -- camelCase keys
await invoke('save_file', { filePath: '/doc.txt' });
```

### ERR-R012: Unhandled invoke rejection

**Error**: `Unhandled Promise Rejection` in the browser console.

**Cause**: Rust command returns `Err(...)` but frontend does not catch the error.

```typescript
// WRONG
const data = await invoke('risky_operation');

// CORRECT
try {
    const data = await invoke('risky_operation');
} catch (error) {
    console.error('Operation failed:', error);
}
```

**ALWAYS** wrap `invoke()` calls in try/catch when the Rust command returns `Result`.

---

## Error Lookup Table: Window / Webview

### ERR-R020: Window not found

**Error**: `get_webview_window("label")` returns `None`, causing unwrap panic or silent failure.

**Cause**: Window label does not match, window was destroyed, or window was not created yet.

**Fix**: ALWAYS use `Option` handling:

```rust
// WRONG
let window = app.get_webview_window("settings").unwrap();  // PANIC if not found

// CORRECT
if let Some(window) = app.get_webview_window("settings") {
    window.show().unwrap();
    window.set_focus().unwrap();
} else {
    // Window does not exist -- create it or log the issue
}
```

### ERR-R021: Window operations after destruction

**Error**: Various errors when calling methods on a destroyed window.

**Fix**: ALWAYS check if the window still exists before operating on it. Use `try_*` methods where available.

---

## Error Lookup Table: Plugin Errors

### ERR-R030: Plugin not initialized

**Error**: `plugin X not initialized` or `plugin command not found` at runtime.

**Cause**: Plugin not registered in the Builder chain.

**Fix**: ALWAYS register plugins before using their commands:

```rust
tauri::Builder::default()
    .plugin(tauri_plugin_fs::init())
    .plugin(tauri_plugin_dialog::init())
    .plugin(tauri_plugin_shell::init())
    .plugin(tauri_plugin_opener::init())
    // ...
```

### ERR-R031: Plugin permissions not configured

**Error**: `Unhandled Promise Rejection: command plugin:fs|read not allowed` or similar.

**Cause**: Plugin is registered in Rust but permissions are not granted in capabilities.

**Fix**: Add permissions to capability file:

```json
{
  "$schema": "../gen/schemas/desktop-schema.json",
  "identifier": "default",
  "windows": ["main"],
  "permissions": [
    "core:default",
    "fs:default",
    "fs:allow-read-file",
    "dialog:default",
    "shell:default"
  ]
}
```

**ALWAYS** add both the plugin Cargo dependency AND the capability permissions.

---

## Error Lookup Table: Events

### ERR-R040: Event name validation panic

**Error**: Panic with message about invalid event name characters.

**Cause**: Event names may ONLY contain: alphanumeric characters, `-`, `/`, `:`, and `_`. Spaces, dots, and special characters cause panics.

```rust
// WRONG -- dot in event name
app_handle.emit("data.updated", payload)?;  // PANIC

// WRONG -- space in event name
app_handle.emit("data updated", payload)?;  // PANIC

// CORRECT
app_handle.emit("data-updated", payload)?;
app_handle.emit("data:updated", payload)?;
app_handle.emit("data_updated", payload)?;
app_handle.emit("data/updated", payload)?;
```

**NEVER** use characters other than `[a-zA-Z0-9-/:_]` in event names.

### ERR-R041: Event listener memory leak

**Error**: Increasing memory usage, duplicate event handling, React component "ghost" listeners.

**Cause**: Event listeners not cleaned up when components unmount.

```typescript
// WRONG -- listener leaks on unmount
useEffect(() => {
    listen('update', handler);
}, []);

// CORRECT
useEffect(() => {
    const promise = listen('update', handler);
    return () => { promise.then(fn => fn()); };
}, []);
```

**ALWAYS** return the unlisten function in cleanup handlers.

### ERR-R042: Forgetting await on listen

**Error**: `TypeError: unlisten is not a function` when trying to unsubscribe.

**Cause**: `listen()` returns `Promise<UnlistenFn>`, not `UnlistenFn` directly.

```typescript
// WRONG
const unlisten = listen('event', handler);
unlisten();  // TypeError!

// CORRECT
const unlisten = await listen('event', handler);
unlisten();
```

---

## Error Lookup Table: Assets & Protocols

### ERR-R050: Asset protocol not working

**Error**: Images/files not loading, `asset://` URLs return 404.

**Cause**: Asset protocol not enabled or scope not configured.

**Fix**: Enable and scope in `tauri.conf.json`:

```json
{
  "app": {
    "security": {
      "assetProtocol": {
        "enable": true,
        "scope": ["$APPDATA/**", "$RESOURCE/**"]
      }
    }
  }
}
```

### ERR-R051: CSP blocking resources

**Error**: `Refused to load the script/image/style` in browser console.

**Cause**: Content Security Policy too restrictive.

**Fix**: Update CSP in `tauri.conf.json`:

```json
{
  "app": {
    "security": {
      "csp": "default-src 'self'; img-src 'self' asset: https://asset.localhost data:; connect-src ipc: http://ipc.localhost"
    }
  }
}
```

---

## Error Lookup Table: Panics & Crashes

### ERR-R060: Unhandled panic crashes the app

**Error**: App exits abruptly with panic message in console.

**Cause**: `unwrap()` or `expect()` on `None`/`Err` values.

**Fix**: ALWAYS handle errors with `Result` and `Option`:

```rust
// WRONG -- panics on error
let content = std::fs::read_to_string(path).unwrap();

// CORRECT -- return Result
#[tauri::command]
fn read_file(path: String) -> Result<String, AppError> {
    let content = std::fs::read_to_string(path)?;
    Ok(content)
}
```

### ERR-R061: Main thread blocked

**Error**: App window freezes, becomes unresponsive, or shows "Not Responding."

**Cause**: Synchronous command doing I/O or heavy computation on the main thread.

**Fix**: ALWAYS use `async` for I/O operations:

```rust
// WRONG -- blocks main thread
#[tauri::command]
fn read_big_file(path: String) -> String {
    std::fs::read_to_string(path).unwrap()  // Freezes UI
}

// CORRECT -- async, runs on tokio runtime
#[tauri::command]
async fn read_big_file(path: String) -> Result<String, String> {
    tokio::fs::read_to_string(path).await.map_err(|e| e.to_string())
}
```

---

## Diagnostic Decision Tree

```
App crashes or misbehaves at runtime?
|
+-- Is it a panic (app exits)?
|   +-- "state not managed" --> ERR-R001, ERR-R002
|   +-- "unwrap on None" --> ERR-R020, ERR-R060
|   +-- Event name invalid --> ERR-R040
|
+-- Is the UI frozen?
|   +-- Sync command doing I/O --> ERR-R061
|   +-- Deadlock --> ERR-R003
|
+-- Is a command failing?
|   +-- "command not found/allowed" --> ERR-R010, ERR-R031
|   +-- "invalid type" or argument error --> ERR-R011
|   +-- "Unhandled Promise Rejection" --> ERR-R012
|
+-- Are assets not loading?
|   +-- asset:// 404 --> ERR-R050
|   +-- CSP blocking --> ERR-R051
|
+-- Memory growing / duplicate events?
    +-- Listener leak --> ERR-R041
    +-- Await missing --> ERR-R042
```

---

## Panic Prevention Checklist

1. **NEVER** use `.unwrap()` in command handlers -- use `?` with `Result`
2. **NEVER** use `&str` in async command parameters -- use `String`
3. **ALWAYS** match `State<'_, T>` exactly with the type passed to `manage()`
4. **ALWAYS** guard `get_webview_window()` with `if let Some`
5. **ALWAYS** use only `[a-zA-Z0-9-/:_]` in event names
6. **ALWAYS** clean up event listeners on component unmount
7. **ALWAYS** use `async` commands for I/O, network, or heavy computation
8. **ALWAYS** wrap `invoke()` in try/catch on the frontend

---

## Reference Links

- [references/methods.md](references/methods.md) -- Error types, state API, panic handling API
- [references/examples.md](references/examples.md) -- Error handling patterns and recovery strategies
- [references/anti-patterns.md](references/anti-patterns.md) -- Runtime mistakes with fixes

### Official Sources

- https://v2.tauri.app/develop/calling-rust/
- https://v2.tauri.app/develop/state-management/
- https://v2.tauri.app/develop/debug/
