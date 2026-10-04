---
name: tauri-syntax-commands
description: >
  Use when writing Tauri commands, calling invoke(), handling IPC errors, or streaming data from Rust to JavaScript.
  Prevents command registration omissions, argument type mismatches between Rust and JS, and missing error serialization.
  Covers #[tauri::command] macro, sync/async commands, argument types, return types, thiserror, invoke() API, and Channel streaming.
  Keywords: tauri command, invoke, IPC, async command, thiserror, Channel, generate_handler, command registration.
license: MIT
compatibility: "Designed for Claude Code. Requires Tauri 2.x with Rust and TypeScript."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# tauri-syntax-commands

## Quick Reference

### Command Definition (Rust)

| Pattern | Syntax | Notes |
|---------|--------|-------|
| Sync command | `#[tauri::command] fn name() -> T` | Runs on main thread |
| Async command | `#[tauri::command] async fn name() -> T` | Spawned on tokio runtime |
| Forced async | `#[tauri::command(async)] fn name() -> T` | Sync function on tokio runtime |
| Renamed args | `#[tauri::command(rename_all = "snake_case")]` | JS passes snake_case keys |

### Argument Types (Rust <- JS)

| Rust Type | JS Type | Notes |
|-----------|---------|-------|
| `i32`, `u64`, `f64` | `number` | Direct mapping |
| `bool` | `boolean` | Direct mapping |
| `String` | `string` | Owned string |
| `Vec<T>` | `T[]` | Array to Vec |
| `Option<T>` | `T \| null \| undefined` | Nullable |
| `PathBuf` | `string` | Path string |
| Custom struct | object | Must `#[derive(Deserialize)]` |

### Return Types (Rust -> JS)

| Rust Return | JS Result | Notes |
|-------------|-----------|-------|
| `()` | `void` / `null` | No return value |
| `T` (Serialize) | `T` | Direct serialization |
| `Result<T, E>` | `T` or throw `E` | E must impl `Serialize` |
| `Response` | `ArrayBuffer` | Binary data bypass |

### Special Injected Parameters (NOT passed from JS)

| Rust Parameter | Purpose | Example |
|----------------|---------|---------|
| `app: AppHandle` | Application handle | `app.emit("event", data)` |
| `window: WebviewWindow` | Calling window | `window.label()` |
| `state: State<'_, T>` | Managed state | `state.inner()` |
| `request: tauri::ipc::Request` | Raw IPC request | `request.headers()`, `request.body()` |

### Frontend invoke() API

| Feature | Syntax |
|---------|--------|
| Import | `import { invoke } from '@tauri-apps/api/core'` |
| Basic call | `await invoke('command_name')` |
| With args | `await invoke('cmd', { argName: value })` |
| Typed return | `await invoke<ReturnType>('cmd')` |
| With headers | `await invoke('cmd', args, { headers: {...} })` |
| Binary data | `await invoke('cmd', new Uint8Array([...]))` |

### Critical Warnings

**NEVER** use snake_case keys in JS `invoke()` arguments -- Tauri auto-converts camelCase to snake_case. Passing `{ file_path: "x" }` will NOT match Rust parameter `file_path`.

**NEVER** forget to implement `Serialize` on error types -- `Result<T, E>` requires E to implement `Serialize` to send errors to the frontend.

**NEVER** use `&str` parameters in async commands -- borrowed references cannot cross the async spawn boundary. Use `String` instead.

**NEVER** register commands with multiple `invoke_handler()` calls -- only the last one takes effect.

**NEVER** mark commands in `lib.rs` as `pub` -- glue code generation prevents it. Move to a separate module if `pub` is needed.

**ALWAYS** wrap invoke() calls in try/catch -- Rust `Result::Err` rejects the JS Promise.

**ALWAYS** use `Channel<T>` for streaming data instead of multiple events -- channels are tied to the command invocation and type-safe.

**ALWAYS** derive `serde::Deserialize` on custom argument types and `serde::Serialize` on custom return types.

---

## Essential Patterns

### Pattern 1: Basic Command (Rust + TypeScript)

```rust
// src-tauri/src/commands.rs
#[tauri::command]
pub fn greet(name: String) -> String {
    format!("Hello, {}!", name)
}
```

```typescript
// src/main.ts
import { invoke } from '@tauri-apps/api/core';

const greeting = await invoke<string>('greet', { name: 'World' });
console.log(greeting); // "Hello, World!"
```

### Pattern 2: Async Command with Error Handling

```rust
#[derive(Debug, thiserror::Error)]
enum Error {
    #[error(transparent)]
    Io(#[from] std::io::Error),
    #[error("not found: {0}")]
    NotFound(String),
}

// REQUIRED: Serialize impl for sending errors to frontend
impl serde::Serialize for Error {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where S: serde::ser::Serializer {
        serializer.serialize_str(self.to_string().as_ref())
    }
}

#[tauri::command]
async fn read_file(path: String) -> Result<String, Error> {
    let content = tokio::fs::read_to_string(&path).await?;
    Ok(content)
}
```

```typescript
try {
    const content = await invoke<string>('read_file', { path: '/tmp/data.txt' });
    console.log(content);
} catch (error) {
    // error is the serialized string: "not found: ..." or "io error: ..."
    console.error('Failed:', error);
}
```

### Pattern 3: Structured Error Types

For richer error handling on the frontend, use tagged enum serialization.

```rust
#[derive(serde::Serialize)]
#[serde(tag = "kind", content = "message")]
#[serde(rename_all = "camelCase")]
enum AppError {
    Io(String),
    NotFound(String),
    Unauthorized(String),
}

#[tauri::command]
async fn load_data(id: u32) -> Result<Data, AppError> {
    if id == 0 {
        return Err(AppError::NotFound("Item not found".into()));
    }
    Ok(Data { /* ... */ })
}
```

```typescript
try {
    const data = await invoke<Data>('load_data', { id: 42 });
} catch (err: any) {
    // err = { kind: 'notFound', message: 'Item not found' }
    switch (err.kind) {
        case 'notFound':
            showNotFoundUI(err.message);
            break;
        case 'unauthorized':
            redirectToLogin();
            break;
        default:
            console.error('Unexpected error:', err);
    }
}
```

### Pattern 4: Special Injected Parameters

These parameters are injected by Tauri -- the frontend does NOT pass them.

```rust
use tauri::{AppHandle, State, WebviewWindow};

#[tauri::command]
async fn complex_command(
    app: AppHandle,                       // injected: app handle
    window: WebviewWindow,                // injected: calling window
    state: State<'_, MyState>,            // injected: managed state
    // Regular parameters (passed from JS):
    query: String,
    limit: Option<u32>,
) -> Result<Vec<Item>, String> {
    println!("Called from window: {}", window.label());
    let config = state.inner();
    // ... use app, window, state as needed
    Ok(vec![])
}
```

```typescript
// Frontend only passes the regular parameters -- injected params are omitted
const items = await invoke<Item[]>('complex_command', {
    query: 'search term',
    limit: 10,
});
```

### Pattern 5: Channel Streaming (Rust -> JS)

```rust
use tauri::ipc::Channel;

#[derive(Clone, serde::Serialize)]
struct DownloadProgress {
    bytes_read: u64,
    total: u64,
    percent: f64,
}

#[tauri::command]
async fn download_file(
    url: String,
    on_progress: Channel<DownloadProgress>,
) -> Result<String, String> {
    let response = reqwest::get(&url).await.map_err(|e| e.to_string())?;
    let total = response.content_length().unwrap_or(0);
    let mut bytes_read = 0u64;

    // Stream progress updates
    on_progress.send(DownloadProgress {
        bytes_read,
        total,
        percent: 0.0,
    }).unwrap();

    // ... read chunks, updating progress ...

    Ok("download complete".into())
}
```

```typescript
import { invoke, Channel } from '@tauri-apps/api/core';

interface DownloadProgress {
    bytesRead: number;
    total: number;
    percent: number;
}

const onProgress = new Channel<DownloadProgress>();
onProgress.onmessage = (progress) => {
    updateProgressBar(progress.percent);
    console.log(`${progress.bytesRead}/${progress.total}`);
};

const result = await invoke<string>('download_file', {
    url: 'https://example.com/file.zip',
    onProgress,  // Pass the channel as a regular argument
});
```

### Pattern 6: Binary Data with Request/Response

Bypass JSON serialization for large binary payloads.

```rust
use tauri::ipc::{Request, Response};

// Receiving binary data from JS
#[tauri::command]
fn upload(request: Request) -> Result<String, String> {
    let tauri::ipc::InvokeBody::Raw(data) = request.body() else {
        return Err("Expected binary data".into());
    };
    let auth = request.headers().get("Authorization");
    println!("Received {} bytes", data.len());
    Ok(format!("Uploaded {} bytes", data.len()))
}

// Returning binary data to JS
#[tauri::command]
fn get_image(path: String) -> Response {
    let data = std::fs::read(path).unwrap();
    Response::new(data)
}
```

```typescript
// Sending binary data
const data = new Uint8Array([1, 2, 3, 4, 5]);
const result = await invoke<string>('upload', data, {
    headers: { Authorization: 'Bearer token123' },
});

// Receiving binary data
const imageData = await invoke<ArrayBuffer>('get_image', { path: '/photo.jpg' });
```

### Pattern 7: Command Registration

```rust
// src-tauri/src/lib.rs
mod commands;

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![
            commands::greet,
            commands::read_file,
            commands::download_file,
            commands::upload,
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

**Rule**: ALL commands MUST be listed in a single `generate_handler![]` macro call. Multiple `invoke_handler()` calls do NOT merge.

---

## Argument Name Mapping

Tauri automatically converts between JS camelCase and Rust snake_case.

| Rust Parameter | JS Argument Key |
|----------------|-----------------|
| `file_path: String` | `filePath` |
| `user_name: String` | `userName` |
| `item_count: u32` | `itemCount` |
| `is_active: bool` | `isActive` |

To override this behavior:

```rust
#[tauri::command(rename_all = "snake_case")]
fn my_command(file_path: String) { }
```

```typescript
// With rename_all = "snake_case", pass snake_case keys
await invoke('my_command', { file_path: '/tmp/file.txt' });
```

---

## Channel vs Events

| Feature | Channel | Events |
|---------|---------|--------|
| Direction | Rust -> JS (response stream) | Bidirectional |
| Lifetime | Tied to command invocation | App lifetime |
| Targeting | Specific caller | Broadcast or filtered |
| Type safety | Generic `Channel<T>` | Serialized JSON |
| Use case | Progress, streaming data | App-wide notifications |

**ALWAYS** use `Channel<T>` for progress updates and streaming data from a command. **NEVER** use events for command-specific streaming -- channels are scoped to the invocation.

---

## Runtime Generics (Plugin Authors)

When writing commands for plugins or libraries that need to be runtime-agnostic:

```rust
use tauri::{AppHandle, Runtime, WebviewWindow};

#[tauri::command]
async fn plugin_command<R: Runtime>(
    app: AppHandle<R>,
    window: WebviewWindow<R>,
    data: String,
) -> Result<String, String> {
    Ok(format!("Processed: {}", data))
}
```

With the default `wry` feature, `R` resolves to `Wry`. This generic is only necessary for plugin/library code.

---

## Reference Links

- [references/methods.md](references/methods.md) -- Command macro attributes, invoke signature, Channel API
- [references/examples.md](references/examples.md) -- Sync commands, async commands, binary data, channels, errors
- [references/anti-patterns.md](references/anti-patterns.md) -- All command + invoke mistakes

### Official Sources

- https://v2.tauri.app/develop/calling-rust/
- https://docs.rs/tauri/latest/tauri/command/index.html
- https://docs.rs/tauri/latest/tauri/ipc/struct.Channel.html
- https://www.npmjs.com/package/@tauri-apps/api
