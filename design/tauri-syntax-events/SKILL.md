---
name: tauri-syntax-events
description: >
  Use when implementing event-driven communication between Rust and JavaScript or between windows.
  Prevents event listener memory leaks from missing unlisten cleanup and payload serialization failures.
  Covers emit/listen/once patterns, Emitter and Listener traits, global vs window-scoped events, and frontend event API.
  Keywords: tauri events, emit, listen, unlisten, event payload, Emitter trait, Listener trait, window events.
license: MIT
compatibility: "Designed for Claude Code. Requires Tauri 2.x with Rust and TypeScript."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# tauri-syntax-events

## Quick Reference

### Rust Event Traits (Tauri 2.x)

| Trait | Implemented By | Purpose |
|-------|---------------|---------|
| `Emitter` | `App`, `AppHandle`, `Webview`, `WebviewWindow`, `Window` | Send events |
| `Listener` | `App`, `AppHandle`, `Webview`, `WebviewWindow`, `Window` | Receive events |

### Emitter Methods

| Method | Scope | Description |
|--------|-------|-------------|
| `emit(event, payload)` | Global | Broadcast to ALL listeners |
| `emit_str(event, payload)` | Global | Broadcast with pre-serialized JSON string |
| `emit_to(target, event, payload)` | Targeted | Send to a specific window/webview label |
| `emit_filter(event, payload, filter_fn)` | Filtered | Send to targets matching a predicate |

### Listener Methods

| Method | Fires | Returns |
|--------|-------|---------|
| `listen(event, handler)` | Every time | `EventId` |
| `once(event, handler)` | Once, then auto-removes | `EventId` |
| `listen_any(event, handler)` | Every time, any source | `EventId` |
| `once_any(event, handler)` | Once, any source | `EventId` |
| `unlisten(id)` | N/A | `()` |

### Frontend Event API (TypeScript)

| Function | Import | Description |
|----------|--------|-------------|
| `listen<T>(event, handler, options?)` | `@tauri-apps/api/event` | Listen for events, returns `Promise<UnlistenFn>` |
| `once<T>(event, handler, options?)` | `@tauri-apps/api/event` | Listen once, returns `Promise<UnlistenFn>` |
| `emit(event, payload?)` | `@tauri-apps/api/event` | Broadcast event globally |
| `emitTo(target, event, payload?)` | `@tauri-apps/api/event` | Send event to specific target |

### TauriEvent Built-in Events

| Member | Value |
|--------|-------|
| `WINDOW_RESIZED` | `"tauri://resize"` |
| `WINDOW_MOVED` | `"tauri://move"` |
| `WINDOW_CLOSE_REQUESTED` | `"tauri://close-requested"` |
| `WINDOW_DESTROYED` | `"tauri://destroyed"` |
| `WINDOW_FOCUS` | `"tauri://focus"` |
| `WINDOW_BLUR` | `"tauri://blur"` |
| `WINDOW_SCALE_FACTOR_CHANGED` | `"tauri://scale-change"` |
| `WINDOW_THEME_CHANGED` | `"tauri://theme-changed"` |
| `WINDOW_CREATED` | `"tauri://window-created"` |
| `WEBVIEW_CREATED` | `"tauri://webview-created"` |
| `DRAG_ENTER` | `"tauri://drag-enter"` |
| `DRAG_OVER` | `"tauri://drag-over"` |
| `DRAG_DROP` | `"tauri://drag-drop"` |
| `DRAG_LEAVE` | `"tauri://drag-leave"` |

---

## Critical Warnings

**NEVER** forget `Clone` on event payload structs — `emit()` requires `Serialize + Clone`. Omitting `Clone` causes a compile error that does not clearly indicate the source.

**NEVER** use special characters in event names — only alphanumeric, `-`, `/`, `:`, and `_` are allowed. Other characters cause a runtime panic.

**NEVER** forget to call the unlisten function in frontend components — this causes memory leaks. In React, ALWAYS clean up in the `useEffect` return function.

**NEVER** forget to `await` the `listen()` call in TypeScript — `listen()` returns `Promise<UnlistenFn>`, not `UnlistenFn` directly.

**ALWAYS** import the `Emitter` trait (`use tauri::Emitter;`) before calling `emit()` in Rust — the method is not available without the trait import.

**ALWAYS** import the `Listener` trait (`use tauri::Listener;`) before calling `listen()` in Rust.

---

## Essential Patterns

### Pattern 1: Rust to Frontend (Emitter)

```rust
// Tauri 2.x — Broadcast from Rust to all frontend listeners
use tauri::Emitter;

#[derive(Clone, serde::Serialize)]
struct ProgressUpdate {
    task_id: String,
    percent: f64,
    message: String,
}

// In a command or setup hook:
app_handle.emit("progress", ProgressUpdate {
    task_id: "download-1".into(),
    percent: 45.5,
    message: "Downloading file...".into(),
})?;
```

### Pattern 2: Frontend Listening

```typescript
// Tauri 2.x — Listen in TypeScript
import { listen } from '@tauri-apps/api/event';

interface ProgressUpdate {
  taskId: string;
  percent: number;
  message: string;
}

const unlisten = await listen<ProgressUpdate>('progress', (event) => {
  console.log(`${event.payload.taskId}: ${event.payload.percent}%`);
});

// When done:
unlisten();
```

### Pattern 3: Frontend to Rust (Emit + Listen)

```typescript
// Tauri 2.x — Frontend emits
import { emit } from '@tauri-apps/api/event';

await emit('user-action', { action: 'save', documentId: 42 });
```

```rust
// Tauri 2.x — Rust listens (typically in setup hook)
use tauri::Listener;

app.listen("user-action", |event| {
    println!("User action: {:?}", event.payload());
});
```

### Pattern 4: Targeted Emission

```rust
// Tauri 2.x — Emit to specific window
use tauri::Emitter;

app_handle.emit_to("main", "notification", "Update available")?;

// Emit with filter
app_handle.emit_filter("sync", payload, |target| {
    matches!(target, tauri::EventTarget::WebviewWindow { label } if label != "settings")
})?;
```

```typescript
// Tauri 2.x — Frontend targeted emit
import { emitTo } from '@tauri-apps/api/event';

await emitTo('settings', 'config-changed', { key: 'theme', value: 'dark' });
```

### Pattern 5: React Cleanup Pattern

```typescript
// Tauri 2.x — Correct cleanup in React useEffect
import { listen } from '@tauri-apps/api/event';

useEffect(() => {
  let unlisten: (() => void) | undefined;

  listen<string>('update', (event) => {
    setState(event.payload);
  }).then((fn) => { unlisten = fn; });

  return () => {
    if (unlisten) unlisten();
  };
}, []);
```

### Pattern 6: Once (Single-Fire Listener)

```rust
// Tauri 2.x — Rust: listen once, auto-removes
use tauri::Listener;

app.once("initialization-complete", |event| {
    println!("App initialized: {:?}", event.payload());
});
```

```typescript
// Tauri 2.x — TypeScript: listen once
import { once } from '@tauri-apps/api/event';

await once<string>('app-ready', (event) => {
  console.log('App initialized:', event.payload);
});
```

---

## TypeScript Event Types

```typescript
type EventName = string; // alphanumeric, hyphens, slashes, colons, underscores
type EventCallback<T> = (event: Event<T>) => void;
type UnlistenFn = () => void;

interface Event<T> {
  event: EventName;
  id: number;
  payload: T;
}

interface Options {
  target?: string | EventTarget;
}

type EventTarget =
  | { kind: 'Any' }
  | { kind: 'AnyLabel'; label: string }
  | { kind: 'Window'; label: string }
  | { kind: 'Webview'; label: string }
  | { kind: 'WebviewWindow'; label: string };
```

---

## Permissions Required

Events require `core:event:default` in the capability file:

```json
{
  "$schema": "../gen/schemas/desktop-schema.json",
  "identifier": "default",
  "windows": ["main"],
  "permissions": [
    "core:event:default"
  ]
}
```

---

## Reference Links

- [references/methods.md](references/methods.md) — Complete Emitter and Listener trait signatures
- [references/examples.md](references/examples.md) — Working code examples for common event scenarios
- [references/anti-patterns.md](references/anti-patterns.md) — What NOT to do, with WHY explanations

### Official Sources

- https://v2.tauri.app/develop/calling-rust/#event-system
- https://docs.rs/tauri/2/tauri/trait.Emitter.html
- https://docs.rs/tauri/2/tauri/trait.Listener.html
- https://v2.tauri.app/reference/javascript/api/namespaceevent/
