---
name: tauri-impl-design-patterns
description: >
  Use when designing Tauri 2 app architecture, choosing between IPC approaches, or planning application structure.
  Prevents using commands for streaming data, events for request/response, and putting business logic in the frontend.
  Covers commands vs events vs channels, state architecture, frontend-backend split, offline-first, and application archetypes.
  Keywords: tauri design patterns, architecture, commands vs events, Channel, offline-first, error boundary, IPC design.
license: MIT
compatibility: "Designed for Claude Code. Requires Tauri 2.x."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# tauri-impl-design-patterns

## IPC Decision Tree: Commands vs Events vs Channels

Choose the right IPC mechanism based on data flow pattern:

```
What is the communication pattern?
|
+-- Request/Response (frontend asks, Rust answers)
|   --> Use COMMANDS (invoke)
|   Examples: load file, save data, compute result, CRUD operations
|
+-- Push Notification (Rust notifies frontend, or frontend broadcasts)
|   --> Use EVENTS (emit/listen)
|   Examples: background task done, settings changed, new data available
|
+-- Streaming Data (continuous flow from Rust to frontend)
|   --> Use CHANNELS (Channel<T>)
|   Examples: download progress, log streaming, live sensor data
|
+-- Bidirectional Real-Time
    --> Use EVENTS for both directions
    Examples: chat messages, collaborative editing, sync status
```

### IPC Mechanism Comparison

| Feature | Commands | Events | Channels |
|---------|----------|--------|----------|
| Direction | Frontend -> Rust -> Frontend | Bidirectional | Rust -> Frontend |
| Cardinality | 1 request : 1 response | 1 emit : N listeners | 1 command : N messages |
| Lifetime | Single invocation | App lifetime | Tied to command call |
| Targeting | Specific command | Broadcast or filtered | Specific caller |
| Error handling | Result<T, E> | Fire-and-forget | Send errors possible |
| Typing | Strong (generics) | Payload-based | Strong (generics) |
| Use when | CRUD, queries, actions | Notifications, state sync | Progress, streaming |

### When to Combine

```
Pattern: Command + Channel
Use: Long-running operations with progress
Example: File download -- invoke starts it, channel streams progress

Pattern: Command + Event
Use: Action triggers background work, result broadcast later
Example: Start scan -> emit "scan-complete" when done

Pattern: Event + Event
Use: Multi-window state synchronization
Example: Window A emits "data-changed", Window B listens and refreshes
```

---

## State Architecture

### Where to Put State

```
+--------------------------------------------------+
|                STATE DECISION MATRIX               |
+------------------+----------------+---------------+
| Data Type        | Put In Rust    | Put In JS     |
+------------------+----------------+---------------+
| Persistent data  | YES            | Cache only    |
| User settings    | YES (Store)    | Mirror/cache  |
| Auth tokens      | YES (secure)   | Never store   |
| Database conn    | YES            | Never         |
| UI state         | No             | YES           |
| Form values      | No             | YES           |
| Animation state  | No             | YES           |
| Ephemeral flags  | No             | YES           |
| Shared/multi-win | YES            | Per-window    |
| Heavy compute    | YES (result)   | Display only  |
+------------------+----------------+---------------+
```

**Rule of thumb**: If it survives a page reload, it belongs in Rust. If it is UI-only, it belongs in JS.

### Lock Strategy Decision

```
What is the access pattern?
|
+-- Read-heavy, rare writes
|   --> Use RwLock<T>
|   Multiple concurrent readers, exclusive writer
|
+-- Balanced read/write
|   --> Use std::sync::Mutex<T>
|   Simple, safe, no async needed
|
+-- Lock held across .await points
|   --> Use tokio::sync::Mutex<T>
|   Required when doing async I/O while locked
|
+-- Simple counter or flag
|   --> Use AtomicU64, AtomicBool
|   Lock-free, fastest option
|
+-- Complex state with multiple fields
    --> Use Mutex<T> with a struct
    Lock the struct, modify fields, unlock
```

### State Architecture Pattern

```
                    +-----------+
                    |  Frontend |
                    |  (React)  |
                    +-----+-----+
                          |
                   invoke() / events
                          |
                    +-----+-----+
                    |   Tauri    |
                    |  Commands  |
                    +-----+-----+
                          |
               +----------+----------+
               |                     |
        +------+------+     +-------+------+
        | State Layer |     | Plugin Layer |
        | Mutex<App>  |     | fs, dialog,  |
        | RwLock<DB>  |     | store, http  |
        +------+------+     +-------+------+
               |                     |
        +------+------+     +-------+------+
        |  Business   |     |   System     |
        |   Logic     |     |   Access     |
        +-------------+     +--------------+
```

---

## Frontend-Backend Responsibility Split

### What Belongs Where

| Responsibility | Rust Backend | JS Frontend |
|---------------|-------------|-------------|
| File I/O | YES -- all reads/writes | Display only |
| Database queries | YES -- via sqlx/rusqlite | Display results |
| Cryptography | YES -- via ring/sodiumoxide | Never |
| HTTP to external APIs | YES -- via reqwest/plugin | Display responses |
| Heavy computation | YES -- CPU-intensive work | Never |
| Image processing | YES -- via image crate | Display results |
| JSON parsing (large) | YES -- serde | Small payloads OK |
| Form validation | Basic server-side | YES -- UX feedback |
| UI rendering | Never | YES -- DOM/framework |
| Animation | Never | YES -- CSS/JS |
| Routing (SPA) | Never | YES -- router lib |
| Local UI state | Never | YES -- useState etc. |
| Drag-and-drop UX | Receive files | YES -- visual feedback |

### The Golden Rule

> **Heavy in Rust, Pretty in JS**
>
> If it touches the filesystem, network, or CPU for more than 10ms: Rust.
> If it touches the DOM, CSS, or user interaction: JavaScript.

---

## Common App Archetypes

### Archetype 1: Note-Taking / Document App

```
Architecture:
+- Commands: save_note, load_note, list_notes, delete_note, search_notes
+- Plugins: fs (file storage), dialog (file picker), store (settings)
+- State: Mutex<NoteIndex> (in-memory index for search)
+- Events: "note-saved" (sync across windows if multi-window)
+- Frontend: Editor component, sidebar file list

IPC Pattern: Primarily Commands (CRUD)
State: Rust owns file data, JS owns editor state
Key Decision: Store notes as files (fs plugin) or in database (sql plugin)?
  - Files: Simple, user can access directly, git-friendly
  - Database: Faster search, atomic operations, complex queries
```

### Archetype 2: Dashboard / Monitoring App

```
Architecture:
+- Commands: get_initial_data, start_monitoring, stop_monitoring
+- Plugins: notification (alerts), store (thresholds)
+- State: Mutex<MonitorConfig>, background task handle
+- Channels: Channel<MetricsUpdate> for live data streaming
+- Events: "alert-triggered" for threshold breaches
+- Frontend: Charts, gauges, real-time displays

IPC Pattern: Channels for streaming + Events for alerts
State: Rust owns data collection, JS owns visualization
Key Decision: Polling vs push?
  - Channels: Rust pushes data at controlled intervals
  - Events: Good for sporadic alerts
  - Commands: For on-demand data refreshes
```

### Archetype 3: File Manager

```
Architecture:
+- Commands: list_dir, copy_file, move_file, delete_file, get_metadata
+- Plugins: fs (filesystem), dialog (new folder name), opener (open files)
+- State: RwLock<FsCache> (directory listing cache)
+- Events: "fs-changed" via file watcher
+- Custom Protocol: asset:// for thumbnail previews
+- Frontend: File grid/list, breadcrumb nav, drag-drop

IPC Pattern: Commands (CRUD) + Events (watcher) + Custom Protocol (thumbnails)
State: Rust owns file operations, JS owns selection/view state
Key Decision: How to handle thumbnails?
  - Asset protocol: Best for images, native performance
  - Base64 in commands: Works but slow for large sets
  - Channel streaming: Good for generating thumbnails on-demand
```

### Archetype 4: Chat / Messaging App

```
Architecture:
+- Commands: send_message, load_history, get_contacts
+- Plugins: notification, http (API), store (draft messages)
+- State: tokio::sync::Mutex<WsConnection> (WebSocket)
+- Events: "new-message" (Rust receives via WS, emits to frontend)
+- Channels: Channel<FileChunk> for file transfer progress
+- Frontend: Message list, input, contact sidebar

IPC Pattern: Events for real-time + Commands for history + Channels for transfers
State: Rust owns connection + message queue, JS owns UI scroll position
Key Decision: WebSocket management?
  - Rust-side WS (tokio-tungstenite): Full control, reconnection logic
  - Plugin WS: Simpler setup, less control
```

### Archetype 5: Developer Tool

```
Architecture:
+- Commands: run_script, get_output, kill_process, open_project
+- Plugins: shell (process spawning), fs, dialog, opener
+- State: Mutex<HashMap<ProcessId, ChildHandle>>
+- Events: "process-output" for streaming stdout/stderr
+- Multi-window: Main editor + output panel + settings
+- Frontend: Code editor, terminal emulator, project tree

IPC Pattern: Commands (actions) + Events (process output) + Multi-window events
State: Rust owns processes + file I/O, JS owns editor state
Key Decision: Shell scope security
  - ALWAYS whitelist specific commands in shell permission scope
  - NEVER grant blanket shell:default without restrictions
```

---

## Performance Patterns

### Debounced IPC

For rapid user input that triggers Rust operations:

```typescript
// Frontend -- debounce search input
let debounceTimer: number;
function onSearchInput(query: string) {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
        invoke('search', { query });
    }, 300);  // 300ms debounce
}
```

### Batch Operations

Instead of many small IPC calls, batch into one:

```rust
// WRONG -- N IPC calls
for item in items {
    invoke('save_item', { item });
}

// CORRECT -- 1 IPC call with batch
invoke('save_items', { items: allItems });
```

```rust
#[tauri::command]
async fn save_items(items: Vec<Item>) -> AppResult<u32> {
    let count = items.len() as u32;
    // Process all at once
    Ok(count)
}
```

### Lazy Loading

Load data on-demand, not all at startup:

```typescript
// Load initial page only
const firstPage = await invoke<Item[]>('list_items', { page: 0, pageSize: 50 });

// Load more on scroll
async function loadMore(page: number) {
    const items = await invoke<Item[]>('list_items', { page, pageSize: 50 });
    appendToList(items);
}
```

### Asset Protocol for Large Files

Use `convertFileSrc()` instead of loading through commands:

```typescript
import { convertFileSrc } from '@tauri-apps/api/core';

// WRONG -- loads entire image through IPC (slow, memory-heavy)
const imageData = await invoke<number[]>('read_image', { path });
const blob = new Blob([new Uint8Array(imageData)]);
img.src = URL.createObjectURL(blob);

// CORRECT -- native asset protocol (zero-copy, fast)
img.src = convertFileSrc(imagePath);
```

---

## Offline-First Pattern

```
+--------------------------------------------------+
|              OFFLINE-FIRST ARCHITECTURE            |
+--------------------------------------------------+
|                                                    |
|  Frontend                                          |
|  +--------+    +--------+    +--------+           |
|  |  UI    |--->| Store  |--->| Sync   |           |
|  |        |<---| (cache)|<---| Engine |           |
|  +--------+    +--------+    +---+----+           |
|                                  |                 |
|  Rust Backend                    |                 |
|  +--------+    +--------+    +---+----+           |
|  | Local  |<-->| Merge  |<-->| Remote |           |
|  | DB     |    | Logic  |    | API    |           |
|  +--------+    +--------+    +--------+           |
+--------------------------------------------------+

Strategy:
1. Store plugin for settings/preferences (immediate, local)
2. Local database for app data (sql plugin or custom)
3. Sync engine checks connectivity, pushes/pulls changes
4. Merge logic resolves conflicts (last-write-wins or custom)
5. Events notify frontend of sync status changes
```

Key patterns:
- ALWAYS write to local store first, sync later
- Use events to notify UI of sync status: "sync-started", "sync-complete", "sync-conflict"
- Handle network errors gracefully in Rust, never in JS

---

## Error Boundary Design

```
+--------------------------------------------------+
|              ERROR FLOW ARCHITECTURE               |
+--------------------------------------------------+
|                                                    |
|  Rust Command                                      |
|  fn action() -> Result<T, AppError>               |
|       |                                            |
|       +-- Ok(T) ---------> invoke resolves         |
|       |                    Frontend uses data       |
|       +-- Err(AppError) -> invoke rejects          |
|                            Frontend catches         |
|                                                    |
|  Error Categories:                                 |
|  +-- Recoverable (show message, retry button)     |
|  +-- User Error (validation feedback)             |
|  +-- System Error (log + generic message)         |
|  +-- Fatal (log + restart prompt)                 |
+--------------------------------------------------+
```

### Error Boundary Implementation

```rust
// Rust: structured errors for frontend
#[derive(serde::Serialize)]
#[serde(tag = "severity")]
enum AppError {
    #[serde(rename = "recoverable")]
    Recoverable { message: String, retry: bool },
    #[serde(rename = "validation")]
    Validation { field: String, message: String },
    #[serde(rename = "system")]
    System { message: String },
    #[serde(rename = "fatal")]
    Fatal { message: String },
}
```

```typescript
// Frontend: global error handler
async function safeInvoke<T>(cmd: string, args?: object): Promise<T> {
    try {
        return await invoke<T>(cmd, args);
    } catch (error: any) {
        switch (error.severity) {
            case 'recoverable':
                showRetryDialog(error.message);
                break;
            case 'validation':
                highlightField(error.field, error.message);
                break;
            case 'system':
                showErrorToast(error.message);
                console.error('System error:', error);
                break;
            case 'fatal':
                showFatalError(error.message);
                break;
            default:
                showErrorToast(String(error));
        }
        throw error;
    }
}
```

### Global Panic Recovery

```rust
.setup(|app| {
    let handle = app.handle().clone();
    std::panic::set_hook(Box::new(move |info| {
        eprintln!("PANIC: {info}");
        let _ = handle.emit("app-panic", info.to_string());
    }));
    Ok(())
})
```

---

## Architecture Decision Record Template

When making architectural choices, document them:

```
## ADR-001: [Decision Title]

### Context
What is the situation that requires a decision?

### Decision
Commands / Events / Channels? Rust state / JS state? Which plugins?

### Consequences
+ Positive outcomes
- Tradeoffs accepted

### Alternatives Considered
What other approaches were evaluated and why rejected?
```

---

## Reference Links

- [references/methods.md](references/methods.md) -- IPC API signatures, state API, plugin capabilities
- [references/examples.md](references/examples.md) -- Complete architectural examples for each archetype
- [references/anti-patterns.md](references/anti-patterns.md) -- Architectural mistakes and their consequences

- Official sources: [Calling Rust](https://v2.tauri.app/develop/calling-rust/), [State](https://v2.tauri.app/develop/state-management/), [IPC](https://v2.tauri.app/concept/inter-process-communication/)
