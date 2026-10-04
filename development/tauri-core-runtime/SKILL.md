---
name: tauri-core-runtime
description: >
  Use when configuring app initialization, using setup hooks, spawning background tasks, or managing app lifecycle.
  Prevents misconfigured Builder chains and missing plugin registration that cause silent runtime failures.
  Covers Builder configuration, setup hook, AppHandle usage, Manager trait, tokio async runtime, and app exit/restart.
  Keywords: tauri builder, setup hook, AppHandle, Manager trait, tokio runtime, app lifecycle, window events.
license: MIT
compatibility: "Designed for Claude Code. Requires Tauri 2.x with Rust and TypeScript."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# tauri-core-runtime

## Quick Reference

### Builder Method Summary (Tauri 2.x)

| Method | Purpose | Example |
|--------|---------|---------|
| `Builder::default()` | Create default builder | `tauri::Builder::default()` |
| `.setup(F)` | App initialization hook | `.setup(\|app\| { Ok(()) })` |
| `.invoke_handler(F)` | Register command handlers | `.invoke_handler(generate_handler![cmd1])` |
| `.manage(T)` | Register managed state | `.manage(MyState::default())` |
| `.plugin(P)` | Register a plugin | `.plugin(my_plugin::init())` |
| `.menu(F)` | Set application menu | `.menu(\|app\| MenuBuilder::new(app).build())` |
| `.on_window_event(F)` | Window event handler | `.on_window_event(\|window, event\| { })` |
| `.on_menu_event(F)` | Menu event handler | `.on_menu_event(\|app, event\| { })` |
| `.on_webview_event(F)` | Webview event handler | `.on_webview_event(\|webview, event\| { })` |
| `.on_page_load(F)` | Page load handler | `.on_page_load(\|webview, payload\| { })` |
| `.on_tray_icon_event(F)` | Tray icon event handler | `.on_tray_icon_event(\|app, event\| { })` |
| `.any_thread()` | Allow running on non-main thread | `.any_thread()` |
| `.build(Context)` | Build without running (returns `App`) | `.build(generate_context!())` |
| `.run(Context)` | Build and run the app | `.run(generate_context!())` |

### Manager Trait Key Methods

| Method | Returns | Available On |
|--------|---------|-------------|
| `app_handle()` | `&AppHandle<R>` | App, AppHandle, Window, WebviewWindow, Webview |
| `state::<T>()` | `State<'_, T>` | All Manager implementors |
| `try_state::<T>()` | `Option<State<'_, T>>` | All Manager implementors |
| `manage(T)` | `bool` | All Manager implementors |
| `get_webview_window(label)` | `Option<WebviewWindow<R>>` | All Manager implementors |
| `webview_windows()` | `HashMap<String, WebviewWindow<R>>` | All Manager implementors |
| `get_window(label)` | `Option<Window<R>>` | All Manager implementors |
| `get_focused_window()` | `Option<Window<R>>` | All Manager implementors |
| `config()` | `&Config` | All Manager implementors |
| `path()` | `&PathResolver<R>` | All Manager implementors |
| `package_info()` | `&PackageInfo` | All Manager implementors |

### AppHandle Properties

| Property | Description |
|----------|-------------|
| `Clone` | Can be cloned freely |
| `Send + Sync` | Safe to pass across threads |
| Implements `Manager` | Full access to state, windows, config |
| Implements `Emitter` | Can emit events |
| Implements `Listener` | Can listen for events |

### Critical Warnings

**NEVER** call `.invoke_handler()` more than once on a Builder -- only the last call takes effect. Put ALL commands in a single `generate_handler![]`.

**NEVER** use `Arc` to wrap managed state -- Tauri already wraps state in `Arc` internally. Use `app.manage(data)`, not `app.manage(Arc::new(data))`.

**NEVER** access managed state with the wrong wrapper type -- `State<'_, MyState>` when you registered `Mutex<MyState>` causes a runtime panic, not a compile error.

**ALWAYS** clone `AppHandle` before moving it into a thread or async block -- `app.handle().clone()` is the correct pattern.

**ALWAYS** use `#[cfg_attr(mobile, tauri::mobile_entry_point)]` on the `run()` function in `lib.rs` when targeting mobile platforms.

**NEVER** perform heavy I/O in `setup()` synchronously without spawning a thread -- it blocks app startup.

---

## Essential Patterns

### Pattern 1: Standard Application Entry Point (Tauri 2.x)

```rust
// src-tauri/src/lib.rs
mod commands;

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .manage(AppState::default())
        .plugin(tauri_plugin_opener::init())
        .invoke_handler(tauri::generate_handler![
            commands::greet,
            commands::fetch_data,
        ])
        .setup(|app| {
            let handle = app.handle().clone();
            // Initialization logic here
            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

```rust
// src-tauri/src/main.rs
fn main() {
    app_lib::run();
}
```

### Pattern 2: The setup() Hook

The setup hook runs after the app is initialized but before windows are shown. It receives `&mut App<R>` and returns `Result<(), Box<dyn Error>>`. Any error aborts app startup.

```rust
.setup(|app| {
    // 1. Access AppHandle for thread-safe operations
    let handle = app.handle().clone();

    // 2. Register state that depends on app paths
    let db_path = app.path().app_data_dir()?.join("data.db");
    app.manage(Database::new(&db_path)?);

    // 3. Spawn a background thread (uses cloned AppHandle)
    std::thread::spawn(move || {
        loop {
            handle.emit("heartbeat", ()).unwrap();
            std::thread::sleep(std::time::Duration::from_secs(30));
        }
    });

    // 4. Create additional windows programmatically
    let _settings = tauri::webview::WebviewWindowBuilder::new(
        app,
        "settings",
        tauri::WebviewUrl::App("settings.html".into()),
    )
    .title("Settings")
    .inner_size(600.0, 400.0)
    .visible(false)
    .build()?;

    Ok(())
})
```

### Pattern 3: AppHandle in Threads and Async Blocks

`AppHandle` is `Clone + Send + Sync`, making it the primary handle for background work.

```rust
// In setup() or from a command
let handle = app.handle().clone();

// Std thread
std::thread::spawn(move || {
    let state = handle.state::<MyState>();
    handle.emit("background-update", "data").unwrap();
    if let Some(window) = handle.get_webview_window("main") {
        window.set_title("Updated").unwrap();
    }
});

// Tokio async task
let handle = app.handle().clone();
tokio::spawn(async move {
    let result = some_async_work().await;
    handle.emit("async-done", result).unwrap();
});
```

### Pattern 4: Window Event Callbacks

```rust
.on_window_event(|window, event| {
    match event {
        tauri::WindowEvent::CloseRequested { api, .. } => {
            // Prevent close and hide instead (e.g., tray app)
            api.prevent_close();
            window.hide().unwrap();
        }
        tauri::WindowEvent::Focused(focused) => {
            if *focused {
                println!("{} gained focus", window.label());
            }
        }
        tauri::WindowEvent::Destroyed => {
            println!("{} was destroyed", window.label());
        }
        _ => {}
    }
})
```

### Pattern 5: Build vs Run

Use `.build()` when you need access to the `App` instance before running, or when you need the run callback for lifecycle events like exit.

```rust
// .run() -- simple, no run callback
tauri::Builder::default()
    .run(tauri::generate_context!())
    .expect("error running app");

// .build() + .run() -- access to RunEvent for exit handling
let app = tauri::Builder::default()
    .build(tauri::generate_context!())
    .expect("error building app");

app.run(|app_handle, event| {
    match event {
        tauri::RunEvent::ExitRequested { api, .. } => {
            // Prevent exit (e.g., keep running in tray)
            api.prevent_exit();
        }
        tauri::RunEvent::Exit => {
            // Final cleanup before process ends
            println!("Application exiting");
        }
        _ => {}
    }
});
```

### Pattern 6: Exit and Restart

```rust
// Exit from a command
#[tauri::command]
fn quit_app(app: tauri::AppHandle) {
    app.exit(0); // 0 = success exit code
}

// Restart (requires tauri-plugin-process)
#[tauri::command]
fn restart_app(app: tauri::AppHandle) {
    app.restart();
}
```

```typescript
// Frontend exit/restart (requires @tauri-apps/plugin-process)
import { exit, relaunch } from '@tauri-apps/plugin-process';

await exit(0);
await relaunch();
```

---

## Async Runtime

Tauri 2.x uses **tokio** as the async runtime. Async commands are automatically spawned on the tokio runtime -- you do NOT need to configure tokio yourself.

The `tauri::async_runtime` module provides direct access when needed:

```rust
tauri::async_runtime::spawn(async {
    // Runs on the tokio runtime
});
```

**ALWAYS** use `async` commands for I/O, network, or long-running operations. Sync commands run on the main thread and will freeze the UI if they block.

**ALWAYS** use `#[tauri::command(async)]` on a sync function if you want it to run on the async runtime instead of the main thread:

```rust
#[tauri::command(async)]
fn heavy_sync_computation(data: Vec<u8>) -> Vec<u8> {
    // Runs on tokio runtime, not main thread
    expensive_transform(data)
}
```

---

## WindowEvent Variants (Tauri 2.x)

| Variant | Fields | Description |
|---------|--------|-------------|
| `Resized` | `PhysicalSize<u32>` | Window client area resized |
| `Moved` | `PhysicalPosition<i32>` | Window position changed |
| `CloseRequested` | `api: CloseRequestApi` | Close requested; call `api.prevent_close()` to cancel |
| `Destroyed` | -- | Window has been destroyed |
| `Focused` | `bool` | `true` = gained focus, `false` = lost |
| `ScaleFactorChanged` | `scale_factor, new_inner_size` | DPI/display scale changed |
| `DragDrop` | `DragDropEvent` | File drag-and-drop event |
| `ThemeChanged` | `Theme` | System theme changed (not on Linux) |

---

## Reference Links

- [references/methods.md](references/methods.md) -- Builder methods, Manager trait methods, AppHandle methods
- [references/examples.md](references/examples.md) -- Lifecycle patterns, setup hook, background tasks
- [references/anti-patterns.md](references/anti-patterns.md) -- Lifecycle mistakes and how to avoid them

### Official Sources

- https://v2.tauri.app/develop/
- https://docs.rs/tauri/latest/tauri/struct.Builder.html
- https://docs.rs/tauri/latest/tauri/struct.AppHandle.html
- https://docs.rs/tauri/latest/tauri/trait.Manager.html
