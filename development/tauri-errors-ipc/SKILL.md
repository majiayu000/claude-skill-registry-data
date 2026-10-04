---
name: tauri-errors-ipc
description: >
  Use when encountering invoke errors, serialization failures, or IPC-related panics in Tauri 2.
  Prevents silent type mismatches between Rust and JavaScript and missing Serialize on error types.
  Covers serialization failures, command not found, argument type mismatches, permission denied, async panics, and thiserror patterns.
  Keywords: tauri IPC error, invoke error, serialization failure, command not found, type mismatch, thiserror, Serialize.
license: MIT
compatibility: "Designed for Claude Code. Requires Tauri 2.x."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# tauri-errors-ipc

## Diagnostic Decision Tree

```
invoke() fails or returns unexpected result
|
+-- Error: "command <name> not found"
|   --> Step 1: Command Registration (Section 1)
|
+-- Error: "command <name> not allowed"
|   --> Permission issue. See tauri-errors-permissions skill.
|
+-- Error contains "invalid type" / "missing field" / "invalid value"
|   --> Step 2: Serialization & Type Mismatch (Section 2)
|
+-- Error: invoke returns string instead of object (or vice versa)
|   --> Step 3: Error Serialization Pattern (Section 3)
|
+-- Rust panics (app crashes, no error returned to JS)
|   --> Step 4: Async Command Panics (Section 4)
|
+-- Error caught but message is unhelpful ("null" or empty string)
|   --> Step 5: Structured Error Pattern (Section 5)
|
+-- No error, but invoke never resolves (hangs forever)
|   --> Step 6: Deadlocks & Blocking (Section 6)
```

---

## Section 1: Command Not Found

### Symptoms

- JavaScript error: `command <name> not found`
- `invoke('my_command')` rejects immediately

### Debugging Steps

**Step 1.1**: Verify the command is registered in `generate_handler![]`:
```rust
// src-tauri/src/lib.rs
tauri::Builder::default()
    .invoke_handler(tauri::generate_handler![
        my_command,           // Direct function
        commands::my_command, // Module-prefixed function
    ])
```

**Step 1.2**: Verify there is only ONE `invoke_handler()` call. Multiple calls do NOT merge -- only the last one takes effect:
```rust
// WRONG: first handler is silently overwritten
builder
    .invoke_handler(tauri::generate_handler![cmd_a])
    .invoke_handler(tauri::generate_handler![cmd_b]) // Only this one works
```

**Step 1.3**: Verify the function has the `#[tauri::command]` attribute:
```rust
#[tauri::command]  // REQUIRED -- without this, generate_handler! will fail to compile
fn my_command() -> String {
    "hello".into()
}
```

**Step 1.4**: Verify the command name matches. Rust uses `snake_case` function names. The frontend calls the same `snake_case` name:
```typescript
// Command: fn get_user_data() -> ...
await invoke('get_user_data');  // CORRECT: snake_case
await invoke('getUserData');    // WRONG: command names are NOT auto-converted
```

**Step 1.5**: If the command is in a separate module, verify it is `pub`:
```rust
// src-tauri/src/commands.rs
pub fn my_command() { }  // MUST be pub when in a module

// src-tauri/src/lib.rs
fn my_command() { }       // MUST NOT be pub when in lib.rs directly
```

---

## Section 2: Serialization & Type Mismatch

### Symptoms

- Error: `invalid type: expected <X>, found <Y>`
- Error: `missing field '<name>'`
- Error: `unknown field '<name>'`
- Command returns `null` or `undefined` unexpectedly

### Debugging Steps

**Step 2.1**: Check argument name casing. Rust parameters use `snake_case`. JavaScript arguments MUST use `camelCase`:
```rust
#[tauri::command]
fn save_file(file_path: String, file_size: u64) { }
```
```typescript
// CORRECT: camelCase keys matching snake_case params
await invoke('save_file', { filePath: '/doc.txt', fileSize: 1024 });

// WRONG: snake_case keys -- causes "missing field" error
await invoke('save_file', { file_path: '/doc.txt', file_size: 1024 });
```

**Step 2.2**: Check type compatibility. Common mismatches:

| Rust Type | JavaScript Type | Common Mistake |
|-----------|----------------|----------------|
| `String` | `string` | Passing `number` or `null` |
| `u32` / `i32` | `number` | Passing `string` like `"42"` |
| `f64` | `number` | Passing `NaN` or `Infinity` (fails serde) |
| `bool` | `boolean` | Passing `0`/`1` instead of `true`/`false` |
| `Vec<T>` | `T[]` | Passing non-array iterable |
| `Option<T>` | `T \| null` | Passing `undefined` (use `null` explicitly) |
| `PathBuf` | `string` | Passing object instead of path string |

**Step 2.3**: Check that custom struct derives `Deserialize` (for arguments) and `Serialize` (for return types):
```rust
use serde::{Deserialize, Serialize};

#[derive(Deserialize)]  // REQUIRED for command arguments
struct CreateRequest {
    name: String,
    count: u32,
}

#[derive(Serialize)]    // REQUIRED for return types
struct CreateResponse {
    id: u64,
    created: bool,
}

#[tauri::command]
fn create(request: CreateRequest) -> CreateResponse { ... }
```

**Step 2.4**: Verify `rename_all` attribute if used:
```rust
// This changes the expected JS argument convention
#[tauri::command(rename_all = "snake_case")]
fn my_cmd(user_name: String) { }
// Now JS must use: invoke('my_cmd', { user_name: 'Alice' })
```

---

## Section 3: Error Serialization Pattern

### Symptoms

- Rust command returns `Result<T, E>` but frontend receives unhelpful error
- Error is `"null"` or `""` or a raw Rust debug string
- Compilation error: `the trait Serialize is not implemented for <ErrorType>`

### The Required Pattern

The error type in `Result<T, E>` MUST implement `Serialize`. The idiomatic approach uses `thiserror` with a manual `Serialize` impl:

```rust
#[derive(Debug, thiserror::Error)]
enum Error {
    #[error(transparent)]
    Io(#[from] std::io::Error),
    #[error("database error: {0}")]
    Database(String),
    #[error("not found")]
    NotFound,
}

// REQUIRED: Manual Serialize impl -- serializes as the Display string
impl serde::Serialize for Error {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where S: serde::ser::Serializer {
        serializer.serialize_str(self.to_string().as_ref())
    }
}

#[tauri::command]
fn open_file(path: String) -> Result<String, Error> {
    let content = std::fs::read_to_string(path)?; // auto-converts via #[from]
    Ok(content)
}
```

### Critical Rules

**NEVER** use `Result<T, String>` for anything beyond prototyping. It loses error type information and makes frontend error handling fragile.

**NEVER** derive `Serialize` on error enums that contain non-serializable types (like `std::io::Error`). Use the manual `Serialize` impl pattern above.

**ALWAYS** implement `Display` (via `thiserror`) AND `Serialize` on error types. Both are required for IPC.

---

## Section 4: Async Command Panics

### Symptoms

- App crashes without returning an error to the frontend
- Console shows `thread 'tokio-runtime-worker' panicked`
- `invoke()` never resolves (hangs in the frontend)

### Debugging Steps

**Step 4.1**: Check for `.unwrap()` or `.expect()` on fallible operations inside async commands. Replace with `?` operator:
```rust
// WRONG: panics on error, crashes the tokio worker thread
#[tauri::command]
async fn read_data(path: String) -> String {
    std::fs::read_to_string(path).unwrap()  // PANICS on missing file
}

// CORRECT: returns error to frontend
#[tauri::command]
async fn read_data(path: String) -> Result<String, Error> {
    let content = std::fs::read_to_string(path)?;
    Ok(content)
}
```

**Step 4.2**: Check for borrowed references in async commands. Async commands cannot use `&str` directly:
```rust
// WRONG: compilation error or runtime panic
#[tauri::command]
async fn process(value: &str) -> String {
    value.to_uppercase()
}

// CORRECT: use owned types
#[tauri::command]
async fn process(value: String) -> String {
    value.to_uppercase()
}

// ALSO CORRECT: wrap return in Result to allow &str
#[tauri::command]
async fn process_ref(value: &str) -> Result<String, ()> {
    Ok(value.to_uppercase())
}
```

**Step 4.3**: Check for blocking calls inside async commands. Use `tokio::task::spawn_blocking` for CPU-heavy or blocking I/O work:
```rust
#[tauri::command]
async fn heavy_compute(data: Vec<u8>) -> Result<Vec<u8>, Error> {
    let result = tokio::task::spawn_blocking(move || {
        // CPU-intensive work here
        process_data(&data)
    }).await.map_err(|e| Error::Internal(e.to_string()))?;
    Ok(result)
}
```

---

## Section 5: Structured Error Pattern

### Symptoms

- Frontend catches errors but cannot distinguish error types
- All errors are plain strings, no programmatic handling possible

### Solution: Tagged Enum Errors

For errors the frontend needs to handle differently by type, use a tagged serde enum:

```rust
#[derive(serde::Serialize)]
#[serde(tag = "kind", content = "message")]
#[serde(rename_all = "camelCase")]
enum AppError {
    Io(String),
    NotFound(String),
    Unauthorized(String),
    Validation(String),
}

#[tauri::command]
fn load_data(id: u64) -> Result<Data, AppError> {
    // ...
}
```

Frontend receives typed error objects:
```typescript
try {
    await invoke('load_data', { id: 42 });
} catch (err: unknown) {
    const error = err as { kind: string; message: string };
    switch (error.kind) {
        case 'notFound':
            showNotFoundUI(error.message);
            break;
        case 'unauthorized':
            redirectToLogin();
            break;
        case 'validation':
            showValidationError(error.message);
            break;
        default:
            showGenericError(error.message);
    }
}
```

---

## Section 6: Deadlocks & Blocking

### Symptoms

- `invoke()` hangs forever, never resolves or rejects
- UI freezes completely
- App becomes unresponsive

### Debugging Steps

**Step 6.1**: Check for synchronous commands doing I/O. Sync commands run on the main thread and block the entire UI:
```rust
// WRONG: blocks main thread
#[tauri::command]
fn read_file(path: String) -> String {
    std::fs::read_to_string(path).unwrap()  // Blocks main thread
}

// CORRECT: async command runs on tokio runtime
#[tauri::command]
async fn read_file(path: String) -> Result<String, Error> {
    let content = tokio::fs::read_to_string(path).await?;
    Ok(content)
}
```

**Step 6.2**: Check for nested Mutex locks (deadlock):
```rust
// WRONG: if any code path locks the same mutex twice, deadlock
#[tauri::command]
fn update(state: tauri::State<'_, Mutex<AppData>>) {
    let mut data = state.lock().unwrap();
    // ... calls a function that also locks state ...
    helper(&state);  // DEADLOCK if helper also calls state.lock()
}
```

**Step 6.3**: Check for `std::sync::Mutex` held across `.await`:
```rust
// WRONG: std::sync::Mutex blocks the async runtime
#[tauri::command]
async fn bad(state: tauri::State<'_, std::sync::Mutex<Data>>) -> Result<(), Error> {
    let data = state.lock().unwrap();
    some_async_call().await;  // Holding std Mutex across await = potential deadlock
    Ok(())
}

// CORRECT: use tokio::sync::Mutex for locks held across await points
#[tauri::command]
async fn good(state: tauri::State<'_, tokio::sync::Mutex<Data>>) -> Result<(), Error> {
    let data = state.lock().await;
    some_async_call().await;
    Ok(())
}
```

---

## Frontend Error Handling Pattern

ALWAYS wrap `invoke()` calls in try/catch. Unhandled rejections cause silent failures:

```typescript
import { invoke } from '@tauri-apps/api/core';

// Minimal pattern
try {
    const result = await invoke<string>('my_command', { arg: 'value' });
    // handle success
} catch (error: unknown) {
    console.error('Command failed:', error);
    // handle error
}

// Typed wrapper pattern (recommended for reuse)
async function safeInvoke<T>(
    cmd: string,
    args?: Record<string, unknown>
): Promise<{ data: T; error: null } | { data: null; error: string }> {
    try {
        const data = await invoke<T>(cmd, args);
        return { data, error: null };
    } catch (err) {
        return { data: null, error: String(err) };
    }
}
```

---

## Reference Links

- [references/methods.md](references/methods.md) -- IPC API signatures and type mappings
- [references/examples.md](references/examples.md) -- Error handling code examples
- [references/anti-patterns.md](references/anti-patterns.md) -- IPC mistakes with explanations

### Official Sources

- https://v2.tauri.app/develop/calling-rust/
- https://v2.tauri.app/develop/calling-frontend/
- https://docs.rs/tauri/latest/tauri/command/index.html
