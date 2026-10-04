---
name: tauri-core-architecture
description: >
  Use when creating new Tauri 2 apps, understanding project structure, or reasoning about the component model.
  Prevents mixing Tauri 1.x architecture assumptions with the v2 multi-webview and capability-based model.
  Covers Rust backend structure, webview layer, IPC bridge model, process model, project layout, and type hierarchy.
  Keywords: tauri architecture, project structure, IPC bridge, webview layer, process model, Rust backend.
license: MIT
compatibility: "Designed for Claude Code. Requires Tauri 2.x with Rust and TypeScript."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# tauri-core-architecture

## Quick Reference

### Architecture Layers (Tauri 2.x)

| Layer | Technology | Location | Role |
|-------|-----------|----------|------|
| Rust Backend | Rust + Tokio | `src-tauri/src/` | Application logic, system access, state management |
| Webview Layer | Platform-native webview | Embedded | Renders HTML/CSS/JS frontend |
| IPC Bridge | JSON-serialized messages | Internal | Connects frontend to backend via `invoke()` and events |
| Plugin System | Rust crate + npm package | `Cargo.toml` + `package.json` | Extends capabilities (fs, dialogs, HTTP, etc.) |
| Permission System | Capabilities + permissions | `src-tauri/capabilities/` | Fine-grained access control (replaces v1 allowlist) |

### Platform Webview Engines

| Platform | Webview Engine |
|----------|---------------|
| Windows | WebView2 (Chromium-based) |
| macOS | WKWebView |
| Linux | WebKitGTK |
| iOS | WKWebView |
| Android | Android WebView |

### Key Dependencies

| Package | Type | Purpose |
|---------|------|---------|
| `@tauri-apps/cli` | devDependency (npm) | CLI tooling for dev/build |
| `@tauri-apps/api` | dependency (npm) | Frontend API for invoke, events, paths |
| `tauri` | dependency (Cargo) | Core Rust framework |
| `tauri-build` | build-dependency (Cargo) | Build script helpers |
| `serde` + `serde_json` | dependency (Cargo) | Serialization for IPC |

### Critical Warnings

**NEVER** block the main thread with synchronous I/O in commands -- ALWAYS use `async` for file, network, or long-running operations. Blocking freezes the entire UI.

**NEVER** call `.invoke_handler()` more than once on Builder -- only the LAST call takes effect. Put ALL commands in a single `generate_handler![]` macro.

**NEVER** mark command functions as `pub` when defined directly in `lib.rs` -- the glue code generation prevents it. Move commands to a separate module if they need to be public.

**NEVER** wrap managed state in `Arc` -- Tauri wraps state in `Arc` internally. Using `app.manage(Arc::new(data))` adds a redundant layer.

**NEVER** use `&str` in async command parameters -- borrowed references do not work with async command spawning. ALWAYS use `String` instead.

**NEVER** use `State<'_, T>` when you registered `Mutex<T>` -- this causes a runtime panic, not a compile error. ALWAYS match the exact registered type: `State<'_, Mutex<T>>`.

---

## Process Model

Tauri 2 uses a **two-process architecture**:

### Main Process (Rust)

- Runs the Rust backend on the main thread + Tokio async runtime
- Has full system access (filesystem, network, OS APIs)
- Manages application lifecycle, windows, menus, tray icons
- Exposes `#[tauri::command]` functions as IPC endpoints
- Manages state via `app.manage()` with `Arc`-wrapped storage

### Webview Process (Frontend)

- Runs in a platform-native webview (NOT Electron/Chromium bundle)
- Renders HTML/CSS/JS like a browser tab
- Communicates with Rust ONLY through the IPC bridge
- Has NO direct system access -- all system operations go through `invoke()`
- Event listeners enable bidirectional pub/sub messaging

### IPC Bridge

The bridge between processes uses JSON-serialized messages:

```
Frontend                          Rust Backend
   |                                   |
   |--- invoke('cmd', {args}) -------->|  (JSON request)
   |                                   |--- execute command
   |<-- Result<T, E> (JSON) ----------|  (JSON response)
   |                                   |
   |--- emit('event', payload) ------->|  (event pub/sub)
   |<-- emit('event', payload) --------|  (event pub/sub)
   |                                   |
   |<-- Channel.send(data) -----------|  (streaming)
```

- `invoke()` sends a JSON object with camelCase keys; Rust receives snake_case parameters
- Events use `Serialize + Clone` payloads
- Channels enable streaming multiple messages from Rust to JS
- Binary data can bypass JSON via `tauri::ipc::Response`

---

## Project Structure

```
my-tauri-app/
├── src/                        # Frontend source (React/Vue/Svelte/vanilla)
│   ├── index.html
│   ├── main.ts
│   └── styles.css
├── src-tauri/                  # Rust backend
│   ├── src/
│   │   ├── lib.rs              # Main app logic (mobile entry point)
│   │   └── main.rs             # Desktop entry point (calls lib.rs)
│   ├── capabilities/           # Permission capability files (JSON/TOML)
│   │   └── default.json        # Default capabilities
│   ├── permissions/            # Custom command permissions (TOML only)
│   ├── icons/                  # Application icons (all required sizes)
│   ├── gen/                    # Generated files (DO NOT edit manually)
│   │   └── schemas/
│   │       ├── desktop-schema.json
│   │       ├── mobile-schema.json
│   │       └── remote-schema.json
│   ├── Cargo.toml              # Rust dependencies
│   ├── Cargo.lock              # Deterministic build lock
│   ├── tauri.conf.json         # Main configuration
│   ├── build.rs                # Cargo build script
│   └── .taurignore             # Exclude files from dev watcher
├── package.json                # Frontend dependencies
├── tsconfig.json               # TypeScript config (if applicable)
└── vite.config.ts              # Bundler config (if Vite)
```

### Source Control Rules

- **ALWAYS commit**: `src-tauri/Cargo.lock` (deterministic builds)
- **ALWAYS ignore**: `src-tauri/target/` (build artifacts)
- **NEVER edit**: `src-tauri/gen/` (auto-generated schemas)

### Entry Point Pattern (Tauri 2.x)

Desktop and mobile share logic through `lib.rs`:

```rust
// src-tauri/src/lib.rs
#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![/* commands */])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}

// src-tauri/src/main.rs (desktop only)
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]
fn main() {
    app_lib::run();
}
```

**ALWAYS** use the `lib.rs` + `main.rs` split pattern for Tauri 2 -- this is required for mobile support and is the standard project layout.

---

## Type Hierarchy

### Core Types

| Type | Description | Traits |
|------|------------|--------|
| `App` | Full application instance (only in `setup()`) | `Manager`, `Emitter`, `Listener` |
| `AppHandle` | Lightweight clone-safe handle to the app | `Manager`, `Emitter`, `Listener`, `Clone + Send + Sync` |
| `WebviewWindow` | Combined window + webview (most common) | `Manager`, `Emitter`, `Listener` |
| `Window` | OS-level window (without webview) | `Manager`, `Emitter`, `Listener` |
| `Webview` | Webview inside a window | `Manager`, `Emitter`, `Listener` |
| `State<'_, T>` | Managed state accessor in commands | -- |
| `Builder` | Application configuration builder | -- |

### The Manager Trait

The `Manager` trait is the unifying interface. It is implemented by `App`, `AppHandle`, `Webview`, `WebviewWindow`, and `Window`. Key methods:

| Method | Return Type | Purpose |
|--------|------------|---------|
| `app_handle()` | `&AppHandle<R>` | Get the AppHandle |
| `config()` | `&Config` | Access tauri.conf.json |
| `state::<T>()` | `State<'_, T>` | Access managed state |
| `try_state::<T>()` | `Option<State<'_, T>>` | Access state without panic |
| `manage(state)` | `bool` | Register new state |
| `get_webview_window(label)` | `Option<WebviewWindow<R>>` | Get window by label |
| `webview_windows()` | `HashMap<String, WebviewWindow<R>>` | Get all windows |
| `get_window(label)` | `Option<Window<R>>` | Get OS window by label |
| `path()` | `&PathResolver<R>` | Access path resolver |
| `package_info()` | `&PackageInfo` | Get package metadata |

### The Emitter Trait

| Method | Purpose |
|--------|---------|
| `emit(event, payload)` | Broadcast to ALL targets |
| `emit_to(target, event, payload)` | Emit to a specific target |
| `emit_filter(event, payload, filter_fn)` | Emit to targets matching a filter |
| `emit_str(event, json_string)` | Emit with pre-serialized JSON |

### The Listener Trait

| Method | Purpose |
|--------|---------|
| `listen(event, handler)` | Listen for events (returns EventId) |
| `once(event, handler)` | Listen once, auto-remove after first event |
| `unlisten(id)` | Remove a listener |
| `listen_any(event, handler)` | Listen from any source |

### Runtime Generic

Most types are generic over `R: Runtime`. With the default `wry` feature, `R` resolves to `Wry`. Use the generic form in plugins or for test mocking:

```rust
#[tauri::command]
async fn my_command<R: Runtime>(
    app: AppHandle<R>,
    window: WebviewWindow<R>,
) -> Result<(), String> {
    Ok(())
}
```

---

## Builder Pattern

The `Builder` is the single entry point for configuring a Tauri application:

```rust
tauri::Builder::default()
    .manage(MyState::default())                              // state
    .plugin(tauri_plugin_shell::init())                      // plugins
    .invoke_handler(tauri::generate_handler![cmd1, cmd2])    // commands
    .setup(|app| {                                           // init hook
        let handle = app.handle().clone();
        // app is &mut App -- full access, runs once
        Ok(())
    })
    .on_window_event(|window, event| { /* ... */ })          // window events
    .on_menu_event(|app, event| { /* ... */ })               // menu events
    .menu(|app| { /* build menu */ })                        // app menu
    .run(tauri::generate_context!())
    .expect("error running app");
```

### Builder Method Reference

| Method | Purpose |
|--------|---------|
| `manage(T)` | Register managed state |
| `plugin(P)` | Register a plugin |
| `invoke_handler(F)` | Register ALL command handlers |
| `setup(F)` | App initialization hook |
| `menu(F)` | Set the application menu |
| `on_menu_event(F)` | Menu event handler |
| `on_window_event(F)` | Window event handler |
| `on_webview_event(F)` | Webview event handler |
| `on_page_load(F)` | Page load handler |
| `on_tray_icon_event(F)` | Tray icon event handler |
| `build(Context)` | Build without running (returns `App`) |
| `run(Context)` | Build and run the app |
| `any_thread(self)` | Allow running on any thread |

---

## Frontend API Overview

| API Area | Key Functions | Import Path |
|----------|--------------|-------------|
| Commands | `invoke<T>()`, `Channel<T>` | `@tauri-apps/api/core` |
| Events | `listen()`, `emit()`, `emitTo()`, `once()` | `@tauri-apps/api/event` |
| Windows | `getCurrentWindow()`, `getAllWindows()` | `@tauri-apps/api/window` |
| Webviews | `getCurrentWebview()` | `@tauri-apps/api/webview` |
| Paths | `appDataDir()`, `join()`, `BaseDirectory` | `@tauri-apps/api/path` |
| Utilities | `convertFileSrc()`, `isTauri()` | `@tauri-apps/api/core` |
| Testing | `mockIPC()`, `mockWindows()`, `clearMocks()` | `@tauri-apps/api/mocks` |

---

## Reference Links

- [references/methods.md](references/methods.md) -- API signatures for App, AppHandle, Manager, Runtime, Webview, WebviewWindow
- [references/examples.md](references/examples.md) -- Working code examples verified against Tauri 2.x documentation
- [references/anti-patterns.md](references/anti-patterns.md) -- What NOT to do, with WHY explanations

### Official Sources

- https://v2.tauri.app/develop/
- https://docs.rs/tauri/latest/tauri/
- https://v2.tauri.app/reference/javascript/api/
- https://v2.tauri.app/start/create-project/
