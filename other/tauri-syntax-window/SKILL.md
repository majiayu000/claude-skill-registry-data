---
name: tauri-syntax-window
description: >
  Use when creating windows, handling window events, or managing multi-window layouts in Tauri 2.
  Prevents window label collisions and incorrect WebviewWindowBuilder usage that causes runtime panics.
  Covers WebviewWindowBuilder, window labels, window configuration, WindowEvent handling, and JavaScript Window class.
  Keywords: tauri window, WebviewWindowBuilder, window events, window label, Window class, monitor, multi-window.
license: MIT
compatibility: "Designed for Claude Code. Requires Tauri 2.x with Rust and TypeScript."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# tauri-syntax-window

## Quick Reference

### Window Config in tauri.conf.json (`app.windows[]`)

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `label` | `string` | `"main"` | Unique window identifier |
| `title` | `string` | -- | Window title bar text |
| `url` | `string` | `"/"` | URL or path to load |
| `width` / `height` | `number` | -- | Dimensions in logical pixels |
| `x` / `y` | `number` | -- | Window position |
| `minWidth` / `minHeight` | `number` | -- | Minimum dimensions |
| `maxWidth` / `maxHeight` | `number` | -- | Maximum dimensions |
| `resizable` | `boolean` | `true` | Allow resizing |
| `fullscreen` | `boolean` | `false` | Start fullscreen |
| `focus` | `boolean` | `true` | Focus on creation |
| `create` | `boolean` | `true` | Create at startup (set `false` for programmatic creation) |
| `transparent` | `boolean` | `false` | Enable transparency |
| `decorations` | `boolean` | `true` | Show title bar / borders |
| `alwaysOnTop` | `boolean` | `false` | Stay above other windows |

### WindowEvent Enum (Rust)

| Variant | Fields | Description |
|---------|--------|-------------|
| `Resized` | `PhysicalSize<u32>` | Window client area resized |
| `Moved` | `PhysicalPosition<i32>` | Window position changed |
| `CloseRequested` | `api: CloseRequestApi` | Close requested; call `api.prevent_close()` to cancel |
| `Destroyed` | -- | Window has been destroyed |
| `Focused` | `bool` | `true` = gained focus, `false` = lost focus |
| `ScaleFactorChanged` | `scale_factor: f64, new_inner_size: PhysicalSize<u32>` | DPI/display scale changed |
| `DragDrop` | `DragDropEvent` | File drag-and-drop event |
| `ThemeChanged` | `Theme` | System theme changed (not supported on Linux) |

### JS Window Event Methods

| Method | Callback Payload | Description |
|--------|-----------------|-------------|
| `onCloseRequested(cb)` | `CloseRequestedEvent` | Close requested (call `event.preventDefault()` to cancel) |
| `onResized(cb)` | `PhysicalSize` | Window resized |
| `onMoved(cb)` | `PhysicalPosition` | Window moved |
| `onFocusChanged(cb)` | `boolean` | Focus gained/lost |
| `onThemeChanged(cb)` | `Theme` | System theme changed |
| `onScaleChanged(cb)` | `{ scaleFactor, size }` | DPI scale changed |
| `onDragDropEvent(cb)` | `DragDropEvent` | File drag-and-drop |

### JS Window State Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `innerSize()` | `Promise<PhysicalSize>` | Client area size |
| `outerSize()` | `Promise<PhysicalSize>` | Total window size |
| `innerPosition()` | `Promise<PhysicalPosition>` | Client area position |
| `outerPosition()` | `Promise<PhysicalPosition>` | Window frame position |
| `isMaximized()` | `Promise<boolean>` | Maximized state |
| `isMinimized()` | `Promise<boolean>` | Minimized state |
| `isVisible()` | `Promise<boolean>` | Visibility state |
| `isFullscreen()` | `Promise<boolean>` | Fullscreen state |
| `title()` | `Promise<string>` | Current title |

### JS Monitor Functions

| Function | Returns | Import |
|----------|---------|--------|
| `availableMonitors()` | `Promise<Monitor[]>` | `@tauri-apps/api/window` |
| `currentMonitor()` | `Promise<Monitor \| null>` | `@tauri-apps/api/window` |
| `primaryMonitor()` | `Promise<Monitor \| null>` | `@tauri-apps/api/window` |
| `cursorPosition()` | `Promise<PhysicalPosition>` | `@tauri-apps/api/window` |

### Size/Position Types

| Type | Import | Description |
|------|--------|-------------|
| `LogicalSize` | `@tauri-apps/api/dpi` | Size in logical pixels (DPI-independent) |
| `PhysicalSize` | `@tauri-apps/api/dpi` | Size in physical pixels |
| `LogicalPosition` | `@tauri-apps/api/dpi` | Position in logical pixels |
| `PhysicalPosition` | `@tauri-apps/api/dpi` | Position in physical pixels |

### Critical Warnings

**NEVER** use duplicate window labels -- each label MUST be unique across the application. Duplicate labels cause runtime panics in Rust and silent failures in JS.

**NEVER** call `window.destroy()` when `window.close()` suffices -- `destroy()` skips the `CloseRequested` event and prevents cleanup handlers from running.

**NEVER** forget to call `api.prevent_close()` inside `CloseRequested` if you want to cancel the close -- the window closes by default.

**ALWAYS** use `app.get_webview_window("label")` (not `app.get_window("label")`) in Tauri 2 -- `get_window` returns the raw Window, not the WebviewWindow.

**ALWAYS** check for `None`/`null` when retrieving windows by label -- the window may not exist yet or may have been closed.

---

## Essential Patterns

### Pattern 1: Creating Windows from Rust

```rust
use tauri::webview::WebviewWindowBuilder;
use tauri::WebviewUrl;

// In setup() or any context with Manager access
let window = WebviewWindowBuilder::new(
    app,
    "settings",                              // unique label
    WebviewUrl::App("settings.html".into()), // URL to load
)
    .title("Settings")
    .inner_size(800.0, 600.0)
    .center()
    .resizable(true)
    .build()?;
```

### Pattern 2: Creating Windows from JavaScript

```typescript
import { Window } from '@tauri-apps/api/window';

const webview = new Window('settings-window', {
  url: '/settings',
  title: 'Settings',
  width: 600,
  height: 400,
  center: true,
  decorations: true,
  resizable: true,
});
```

### Pattern 3: Getting Window References (JS)

```typescript
import { getCurrentWindow, Window, getAllWindows } from '@tauri-apps/api/window';

const win = getCurrentWindow();                      // current window
const settings = await Window.getByLabel('settings'); // by label (may be null)
const allWindows = await getAllWindows();             // all windows
const focused = await Window.getFocusedWindow();     // focused window (may be null)
```

### Pattern 4: Window Events in Rust

```rust
.on_window_event(|window, event| {
    match event {
        WindowEvent::CloseRequested { api, .. } => {
            api.prevent_close();
            window.hide().unwrap();
        }
        WindowEvent::Focused(focused) => {
            if *focused {
                println!("{} gained focus", window.label());
            }
        }
        _ => {}
    }
})
```

### Pattern 5: Window Events in JavaScript

```typescript
const win = getCurrentWindow();

await win.onCloseRequested(async (event) => {
  const confirmed = await confirm('Are you sure?');
  if (!confirmed) {
    event.preventDefault();
  }
});

await win.onResized(({ payload: size }) => {
  console.log('New size:', size.width, size.height);
});
```

### Pattern 6: Multi-Window Communication

```rust
// Show/hide from a command
#[tauri::command]
fn show_settings(app: tauri::AppHandle) {
    if let Some(window) = app.get_webview_window("settings") {
        window.show().unwrap();
        window.set_focus().unwrap();
    }
}
```

```typescript
// JS: send event to a specific window
import { emitTo } from '@tauri-apps/api/event';

await emitTo('settings', 'settings-update-requested', {
  key: 'theme',
  value: 'dark',
});
```

### Pattern 7: Window Manipulation (JS)

```typescript
const win = getCurrentWindow();

// Position and size
await win.center();
await win.setPosition(new LogicalPosition(100, 100));
await win.setSize(new LogicalSize(800, 600));

// Visibility and state
await win.show();
await win.hide();
await win.maximize();
await win.minimize();
await win.toggleMaximize();
await win.setFullscreen(true);

// Properties
await win.setTitle('My App - Document.txt');
await win.setDecorations(false);
await win.setAlwaysOnTop(true);
await win.setResizable(false);

// Lifecycle
await win.close();    // triggers CloseRequested event
await win.destroy();  // force-closes without events
```

### Pattern 8: Monitor Queries

```typescript
import { availableMonitors, currentMonitor, primaryMonitor, cursorPosition } from '@tauri-apps/api/window';

const monitors = await availableMonitors();
const current = await currentMonitor();   // monitor containing the window
const primary = await primaryMonitor();   // primary display
const cursor = await cursorPosition();    // cursor PhysicalPosition
```

---

## Key Enums (JS)

```typescript
type Theme = 'light' | 'dark';
type TitleBarStyle = 'visible' | 'transparent' | 'overlay';
enum UserAttentionType { Critical = 1, Informational = 2 }
enum ProgressBarStatus { None, Normal, Indeterminate, Paused, Error }
```

---

## WebviewWindowBuilder Key Methods (Rust)

```rust
// Window geometry
.inner_size(width: f64, height: f64)
.min_inner_size(w: f64, h: f64)
.max_inner_size(w: f64, h: f64)
.position(x: f64, y: f64)
.center()

// Window behavior
.title(title: impl Into<String>)
.visible(bool)
.focused(bool)
.maximized(bool)
.fullscreen(bool)
.resizable(bool)
.closable(bool)
.minimizable(bool)
.maximizable(bool)
.focusable(bool)
.transparent(bool)

// Webview configuration
.initialization_script(script: impl Into<String>)
.user_agent(ua: &str)
.devtools(enabled: bool)
.disable_javascript()
.zoom_hotkeys_enabled(bool)

// Event handlers
.on_page_load(F)
.on_navigation(F)
.on_web_resource_request(F)
.on_download(F)
.on_document_title_changed(F)
.on_new_window(F)
```

---

## Manager Trait Window Methods (Rust)

```rust
fn get_webview_window(&self, label: &str) -> Option<WebviewWindow<R>>
fn webview_windows(&self) -> HashMap<String, WebviewWindow<R>>
fn get_window(&self, label: &str) -> Option<Window<R>>
fn get_focused_window(&self) -> Option<Window<R>>
fn windows(&self) -> HashMap<String, Window<R>>
```

---

## Permissions

Window management requires `core:window:default` or specific permissions like `core:window:allow-set-title`, `core:window:allow-close`, `core:window:allow-minimize`, `core:window:allow-maximize` in the capability file.

---

## Reference Links

- [references/methods.md](references/methods.md) -- Complete API signatures for WebviewWindowBuilder, Window (JS), and monitor functions
- [references/examples.md](references/examples.md) -- Working code examples for window management patterns
- [references/anti-patterns.md](references/anti-patterns.md) -- What NOT to do with windows, with WHY explanations

### Official Sources

- https://v2.tauri.app/develop/window-customization/
- https://docs.rs/tauri/2.10.2/tauri/webview/struct.WebviewWindowBuilder.html
- https://v2.tauri.app/reference/javascript/api/namespacewindow/
