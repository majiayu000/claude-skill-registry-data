---
name: tauri-syntax-webview
description: >
  Use when working with multiple webviews, embedding web content, or managing webview lifecycle in Tauri 2.
  Prevents confusing Window and Webview APIs and incorrect multi-webview positioning within a single window.
  Covers multi-webview per window, getCurrentWebview(), webview sizing, reparenting, zoom control, and webview events.
  Keywords: tauri webview, getCurrentWebview, multi-webview, webview events, zoom, reparent, embedded webview.
license: MIT
compatibility: "Designed for Claude Code. Requires Tauri 2.x with Rust and TypeScript."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# tauri-syntax-webview

## Quick Reference

### Webview API Imports

| Import | Purpose | Example |
|--------|---------|---------|
| `getCurrentWebview()` | Get the current webview instance | `const wv = getCurrentWebview()` |
| `getAllWebviews()` | Get all webview instances | `const all = await getAllWebviews()` |
| `Webview` | Webview class for creation and reference | `new Webview(window, 'label', opts)` |

**Import path:** `import { Webview, getCurrentWebview, getAllWebviews } from '@tauri-apps/api/webview'`

### Webview Methods (TypeScript)

| Method | Returns | Description |
|--------|---------|-------------|
| `setZoom(factor)` | `Promise<void>` | Set webview zoom level (1.0 = 100%) |
| `clearAllBrowsingData()` | `Promise<void>` | Clear all browsing data |
| `size()` | `Promise<PhysicalSize>` | Get webview size |
| `position()` | `Promise<PhysicalPosition>` | Get webview position |
| `setSize(size)` | `Promise<void>` | Set webview size |
| `setPosition(pos)` | `Promise<void>` | Set webview position |
| `setAutoResize(enabled)` | `Promise<void>` | Auto-resize with parent window |
| `show()` | `Promise<void>` | Show the webview |
| `hide()` | `Promise<void>` | Hide the webview |
| `setFocus()` | `Promise<void>` | Focus the webview |
| `reparent(windowLabel)` | `Promise<void>` | Move webview to another window |
| `close()` | `Promise<void>` | Close and destroy the webview |
| `listen(event, handler)` | `Promise<UnlistenFn>` | Listen for events on this webview |
| `onDragDropEvent(handler)` | `Promise<UnlistenFn>` | Listen for drag-drop events |

### Webview vs Window vs WebviewWindow

| Concept | Description | Use When |
|---------|-------------|----------|
| `Window` | Native OS window container (title bar, frame) | Managing window chrome, position, visibility |
| `Webview` | Web content renderer inside a window | Multiple web panels in one window |
| `WebviewWindow` | Combined window + single webview (convenience) | Standard single-webview-per-window apps |

### Critical Warnings

**NEVER** create a `Webview` without specifying a parent `Window` -- webviews MUST live inside a window.

**NEVER** assume `getCurrentWebview()` and `getCurrentWindow()` return the same object -- a window can contain multiple webviews.

**ALWAYS** use `LogicalSize` / `LogicalPosition` from `@tauri-apps/api/dpi` for sizing and positioning to handle DPI scaling correctly.

**ALWAYS** call `setAutoResize(true)` when a webview should fill its parent window, otherwise the webview will NOT resize when the window resizes.

**NEVER** forget that `reparent()` takes a window label string, not a Window object.

---

## Essential Patterns

### Pattern 1: Getting the Current Webview

```typescript
import { getCurrentWebview } from '@tauri-apps/api/webview';

const webview = getCurrentWebview();
console.log('Webview label:', webview.label);
```

Every webview has a unique `label` string identifier. The label is set at creation time and cannot be changed.

### Pattern 2: Creating a Webview Inside an Existing Window

```typescript
import { Webview } from '@tauri-apps/api/webview';
import { getCurrentWindow } from '@tauri-apps/api/window';

const parentWindow = getCurrentWindow();

const sidePanel = new Webview(parentWindow, 'side-panel', {
  url: 'https://example.com',
  x: 0,
  y: 0,
  width: 400,
  height: 300,
});
```

The constructor parameters are: parent window, unique label, and options with `url`, `x`, `y`, `width`, `height`.

### Pattern 3: Multi-Webview Layout

```typescript
import { Webview } from '@tauri-apps/api/webview';
import { getCurrentWindow } from '@tauri-apps/api/window';
import { LogicalSize, LogicalPosition } from '@tauri-apps/api/dpi';

const win = getCurrentWindow();

// Create a sidebar webview
const sidebar = new Webview(win, 'sidebar', {
  url: '/sidebar.html',
  x: 0,
  y: 0,
  width: 250,
  height: 600,
});

// Create a main content webview
const content = new Webview(win, 'content', {
  url: '/main.html',
  x: 250,
  y: 0,
  width: 550,
  height: 600,
});
```

### Pattern 4: Webview Sizing and Positioning

```typescript
import { getCurrentWebview } from '@tauri-apps/api/webview';
import { LogicalSize, LogicalPosition } from '@tauri-apps/api/dpi';

const webview = getCurrentWebview();

// Get current dimensions
const size = await webview.size();
const pos = await webview.position();

// Resize
await webview.setSize(new LogicalSize(400, 300));

// Reposition
await webview.setPosition(new LogicalPosition(100, 50));

// Auto-resize to fill parent window
await webview.setAutoResize(true);
```

### Pattern 5: Reparenting a Webview

```typescript
import { getCurrentWebview } from '@tauri-apps/api/webview';

const webview = getCurrentWebview();

// Move this webview to a different window by label
await webview.reparent('other-window');
```

Reparenting moves the webview from its current parent window to the window identified by the given label string.

### Pattern 6: Zoom Control

```typescript
import { getCurrentWebview } from '@tauri-apps/api/webview';

const webview = getCurrentWebview();

// Set zoom to 150%
await webview.setZoom(1.5);

// Reset to default
await webview.setZoom(1.0);
```

### Pattern 7: Webview Events

```typescript
import { getCurrentWebview } from '@tauri-apps/api/webview';

const webview = getCurrentWebview();

// Listen for custom events scoped to this webview
const unlisten = await webview.listen<string>('content-loaded', (event) => {
  console.log('Content loaded:', event.payload);
});

// Drag-drop events
const unlistenDrop = await webview.onDragDropEvent((event) => {
  if (event.payload.type === 'drop') {
    console.log('Files dropped:', event.payload.paths);
  }
});

// Clean up
unlisten();
unlistenDrop();
```

### Pattern 8: Webview Events in React

```typescript
import { useEffect } from 'react';
import { getCurrentWebview } from '@tauri-apps/api/webview';

function MyComponent() {
  useEffect(() => {
    const webview = getCurrentWebview();
    const promise = webview.onDragDropEvent((event) => {
      if (event.payload.type === 'drop') {
        console.log('Dropped:', event.payload.paths);
      }
    });

    return () => {
      promise.then((unlisten) => unlisten());
    };
  }, []);

  return <div>Drop files here</div>;
}
```

**ALWAYS** clean up webview event listeners in the component teardown to prevent memory leaks.

---

## Rust Side: WebviewBuilder

For creating webviews from Rust, use `WebviewBuilder`:

```rust
use tauri::webview::WebviewBuilder;
use tauri::WebviewUrl;

// Inside setup() or any context with Manager access
let webview = WebviewBuilder::new(
    "side-panel",
    WebviewUrl::App("panel.html".into()),
)
.auto_resize()
.build()?;

// Attach to a window
window.add_child(
    webview,
    tauri::LogicalPosition::new(0.0, 0.0),
    tauri::LogicalSize::new(400.0, 600.0),
)?;
```

### Rust WebviewWindowBuilder (Combined Window + Webview)

For the common case of one webview per window:

```rust
use tauri::webview::WebviewWindowBuilder;
use tauri::WebviewUrl;

let webview_window = WebviewWindowBuilder::new(
    app,
    "editor",
    WebviewUrl::App("editor.html".into()),
)
.title("Editor")
.inner_size(800.0, 600.0)
.build()?;
```

---

## Drag-Drop Event Types

| Event Type | Fields | Description |
|------------|--------|-------------|
| `enter` | `paths: string[], position: PhysicalPosition` | Files entered the webview area |
| `over` | `position: PhysicalPosition` | Files hovering over the webview |
| `drop` | `paths: string[], position: PhysicalPosition` | Files dropped on the webview |
| `leave` | -- | Files left the webview area |

Built-in TauriEvent constants for drag-drop:

| Constant | Value |
|----------|-------|
| `TauriEvent.DRAG_ENTER` | `"tauri://drag-enter"` |
| `TauriEvent.DRAG_OVER` | `"tauri://drag-over"` |
| `TauriEvent.DRAG_DROP` | `"tauri://drag-drop"` |
| `TauriEvent.DRAG_LEAVE` | `"tauri://drag-leave"` |

---

## Permissions

Webview operations require core permissions in your capability file:

```json
{
  "$schema": "../gen/schemas/desktop-schema.json",
  "identifier": "webview-capability",
  "windows": ["main"],
  "permissions": [
    "core:webview:default",
    "core:webview:allow-create-webview",
    "core:webview:allow-set-webview-size",
    "core:webview:allow-set-webview-position",
    "core:webview:allow-set-webview-zoom",
    "core:webview:allow-reparent",
    "core:webview:allow-webview-close"
  ]
}
```

**ALWAYS** add webview permissions to your capability file. Without them, all webview API calls throw "command not allowed" errors at runtime.

---

## Reference Links

- [references/methods.md](references/methods.md) -- Complete API signatures for Webview class, WebviewBuilder, and related types
- [references/examples.md](references/examples.md) -- Working code examples for multi-webview layouts, drag-drop, and reparenting
- [references/anti-patterns.md](references/anti-patterns.md) -- What NOT to do with webviews, with explanations

### Official Sources

- https://v2.tauri.app/reference/javascript/api/namespacewebview/
- https://v2.tauri.app/reference/javascript/api/namespacedpi/
- https://docs.rs/tauri/latest/tauri/webview/index.html
