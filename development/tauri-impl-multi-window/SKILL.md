---
name: tauri-impl-multi-window
description: >
  Use when creating secondary windows, implementing splashscreen flows, or communicating between windows in Tauri 2.
  Prevents duplicate window label panics and orphaned window handles from missing lifecycle cleanup.
  Covers creating windows from Rust and JavaScript, inter-window events, show/hide patterns, splashscreen, and parent-child relationships.
  Keywords: tauri multi-window, secondary window, splashscreen, inter-window communication, window lifecycle, parent-child.
license: MIT
compatibility: "Designed for Claude Code. Requires Tauri 2.x with Rust and TypeScript."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# tauri-impl-multi-window

## Quick Reference

### Window Creation

| Method | Context | Example |
|--------|---------|---------|
| `WebviewWindowBuilder::new()` | Rust (setup, commands) | `WebviewWindowBuilder::new(app, "label", url).build()?` |
| `new Window()` | TypeScript | `new Window('label', { url: '/page' })` |
| `tauri.conf.json` windows array | Configuration | Main window auto-created on startup |

### Window Access

| Method | Context | Returns |
|--------|---------|---------|
| `app.get_webview_window("label")` | Rust | `Option<WebviewWindow<R>>` |
| `app.webview_windows()` | Rust | `HashMap<String, WebviewWindow<R>>` |
| `getCurrentWindow()` | TypeScript | `Window` |
| `Window.getByLabel("label")` | TypeScript | `Promise<Window \| null>` |
| `getAllWindows()` | TypeScript | `Promise<Window[]>` |

### Inter-Window Communication

| Method | Direction | Scope |
|--------|-----------|-------|
| `app.emit("event", payload)` | Rust to all | Broadcast |
| `app.emit_to("label", "event", payload)` | Rust to specific window | Targeted |
| `emit("event", payload)` | JS to all | Broadcast |
| `emitTo("label", "event", payload)` | JS to specific window | Targeted |
| `listen("event", handler)` | JS receive | All events |

### Critical Warnings

**NEVER** create two windows with the same label -- labels MUST be unique across the application. Duplicate labels cause a runtime error.

**NEVER** forget to await `listen()` before calling the unlisten function -- `listen()` returns `Promise<UnlistenFn>`, not `UnlistenFn`.

**NEVER** assume windows exist without checking -- ALWAYS use `get_webview_window()` and handle the `None` case.

**ALWAYS** clean up event listeners in component-based frameworks (React, Vue, Svelte) to prevent memory leaks.

**ALWAYS** use `WebviewWindowBuilder` (not `WindowBuilder`) for creating windows in Tauri 2 -- `WindowBuilder` is the v1 API.

**ALWAYS** use `WebviewUrl::App()` for local pages and `WebviewUrl::External()` for external URLs.

---

## Essential Patterns

### Pattern 1: Creating Windows from Rust

```rust
use tauri::webview::WebviewWindowBuilder;
use tauri::WebviewUrl;

// In setup() or any context with Manager access
.setup(|app| {
    let settings_window = WebviewWindowBuilder::new(
        app,
        "settings",                              // unique label
        WebviewUrl::App("settings.html".into()), // local page
    )
    .title("Settings")
    .inner_size(600.0, 400.0)
    .center()
    .resizable(true)
    .visible(false) // hidden by default
    .build()?;

    Ok(())
})
```

### Pattern 2: Creating Windows from TypeScript

```typescript
import { Window } from '@tauri-apps/api/window';

const settingsWindow = new Window('settings-window', {
    url: '/settings',
    title: 'Settings',
    width: 600,
    height: 400,
    center: true,
    decorations: true,
    resizable: true,
});
```

### Pattern 3: Show/Hide Pattern

```rust
#[tauri::command]
fn show_settings(app: tauri::AppHandle) {
    if let Some(window) = app.get_webview_window("settings") {
        window.show().unwrap();
        window.set_focus().unwrap();
    }
}

#[tauri::command]
fn hide_settings(app: tauri::AppHandle) {
    if let Some(window) = app.get_webview_window("settings") {
        window.hide().unwrap();
    }
}
```

TypeScript equivalent:

```typescript
import { Window } from '@tauri-apps/api/window';

async function toggleSettings() {
    const settings = await Window.getByLabel('settings');
    if (settings) {
        const visible = await settings.isVisible();
        if (visible) {
            await settings.hide();
        } else {
            await settings.show();
            await settings.setFocus();
        }
    }
}
```

### Pattern 4: Inter-Window Communication via Events

Rust side -- emit to a specific window:

```rust
use tauri::Emitter;

#[tauri::command]
fn notify_settings(app: tauri::AppHandle, key: String, value: String) {
    app.emit_to("settings", "config-changed", serde_json::json!({
        "key": key,
        "value": value,
    })).unwrap();
}
```

TypeScript side -- send and receive between windows:

```typescript
// In main window -- send to settings window
import { emitTo } from '@tauri-apps/api/event';

await emitTo('settings', 'config-changed', {
    key: 'theme',
    value: 'dark',
});

// In settings window -- listen for events
import { listen } from '@tauri-apps/api/event';

const unlisten = await listen<{ key: string; value: string }>('config-changed', (event) => {
    console.log(`Config changed: ${event.payload.key} = ${event.payload.value}`);
});
```

### Pattern 5: Splashscreen Pattern

Show a splashscreen while the main window loads, then swap:

```json
// tauri.conf.json -- define both windows
{
  "app": {
    "windows": [
      {
        "label": "splashscreen",
        "url": "/splashscreen",
        "width": 400,
        "height": 300,
        "decorations": false,
        "resizable": false,
        "center": true
      },
      {
        "label": "main",
        "url": "/index.html",
        "width": 1024,
        "height": 768,
        "visible": false
      }
    ]
  }
}
```

```rust
// src-tauri/src/lib.rs
#[tauri::command]
fn close_splashscreen(app: tauri::AppHandle) {
    if let Some(splash) = app.get_webview_window("splashscreen") {
        splash.close().unwrap();
    }
    if let Some(main) = app.get_webview_window("main") {
        main.show().unwrap();
        main.set_focus().unwrap();
    }
}
```

```typescript
// In main window's initialization code
import { invoke } from '@tauri-apps/api/core';

document.addEventListener('DOMContentLoaded', async () => {
    // App is loaded, close splashscreen
    await invoke('close_splashscreen');
});
```

### Pattern 6: Window Close Prevention

```rust
// Rust -- prevent close and hide instead
.on_window_event(|window, event| {
    if let tauri::WindowEvent::CloseRequested { api, .. } = event {
        if window.label() == "settings" {
            api.prevent_close();
            window.hide().unwrap();
        }
    }
})
```

```typescript
// TypeScript -- confirm before closing
import { getCurrentWindow } from '@tauri-apps/api/window';

const win = getCurrentWindow();
await win.onCloseRequested(async (event) => {
    const confirmed = await confirm('Are you sure you want to close?');
    if (!confirmed) {
        event.preventDefault();
    }
});
```

### Pattern 7: Window Event Handling

```typescript
import { getCurrentWindow } from '@tauri-apps/api/window';

const win = getCurrentWindow();

// Resize events
await win.onResized(({ payload: size }) => {
    console.log(`Window resized to ${size.width}x${size.height}`);
});

// Focus events
await win.onFocusChanged(({ payload: focused }) => {
    console.log(`Window ${focused ? 'gained' : 'lost'} focus`);
});

// Theme change events (not supported on Linux)
await win.onThemeChanged(({ payload: theme }) => {
    console.log(`Theme changed to: ${theme}`);
});
```

---

## WebviewWindowBuilder Methods

### Window Geometry

```rust
.inner_size(width: f64, height: f64)    // Window content size
.min_inner_size(w: f64, h: f64)         // Minimum size
.max_inner_size(w: f64, h: f64)         // Maximum size
.position(x: f64, y: f64)              // Window position
.center()                               // Center on screen
```

### Window Behavior

```rust
.title(title: impl Into<String>)        // Window title
.visible(bool)                          // Show on creation
.focused(bool)                          // Focus on creation
.maximized(bool)                        // Start maximized
.fullscreen(bool)                       // Start fullscreen
.resizable(bool)                        // Allow resizing
.closable(bool)                         // Allow closing
.minimizable(bool)                      // Allow minimizing
.maximizable(bool)                      // Allow maximizing
.transparent(bool)                      // Transparent background
```

### Webview Configuration

```rust
.initialization_script(script: impl Into<String>)  // JS to run on page load
.user_agent(ua: &str)                               // Custom user agent
.devtools(enabled: bool)                             // Enable DevTools
```

---

## Window Events (Rust)

| Event Variant | Fields | Description |
|---------------|--------|-------------|
| `CloseRequested` | `api: CloseRequestApi` | Close requested; `api.prevent_close()` to cancel |
| `Destroyed` | -- | Window destroyed |
| `Focused` | `bool` | Focus gained (true) or lost (false) |
| `Resized` | `PhysicalSize<u32>` | Window resized |
| `Moved` | `PhysicalPosition<i32>` | Window moved |
| `ScaleFactorChanged` | `scale_factor, new_inner_size` | DPI/display scale changed |
| `DragDrop` | `DragDropEvent` | File drag-and-drop event |
| `ThemeChanged` | `Theme` | System theme changed |

---

## Reference Links

- [references/methods.md](references/methods.md) -- Complete API signatures for WebviewWindowBuilder, Window (TS), event functions
- [references/examples.md](references/examples.md) -- Working code examples for multi-window patterns
- [references/anti-patterns.md](references/anti-patterns.md) -- Common multi-window mistakes with explanations

### Official Sources

- https://v2.tauri.app/develop/window-customization/
- https://docs.rs/tauri/latest/tauri/webview/struct.WebviewWindowBuilder.html
- https://v2.tauri.app/reference/javascript/api/namespaceevent/
