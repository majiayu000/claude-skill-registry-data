---
name: tauri-impl-migration
description: >
  Use when migrating from Tauri 1 to Tauri 2, updating legacy Tauri code, or comparing v1 vs v2 APIs.
  Prevents retaining v1 allowlist config, deprecated API calls, and outdated import paths that break at compile time.
  Covers config restructuring, allowlist to permissions conversion, Rust and JS API renames, event and menu system changes.
  Keywords: tauri migration, v1 to v2, allowlist, permissions conversion, API rename, import path, upgrade.
license: MIT
compatibility: "Designed for Claude Code. Requires Tauri 2.x."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# tauri-impl-migration

## Quick Reference

### Migration CLI Command

```bash
npx @tauri-apps/cli migrate
```

This auto-converts v1 allowlist entries to capability files, updates Cargo dependencies, and restructures configuration. ALWAYS run this first before manual migration.

### Configuration Key Mapping (v1 to v2)

| Tauri v1 | Tauri v2 |
|----------|----------|
| `package.productName` | `productName` (top-level) |
| `package.version` | `version` (top-level) |
| `tauri` | `app` |
| `tauri.allowlist` | Removed -- replaced by capabilities/permissions |
| `tauri.bundle` | `bundle` (top-level) |
| `tauri.cli` | `plugins.cli` |
| `tauri.updater` | `plugins.updater` |
| `tauri.systemTray` | `app.trayIcon` |
| `tauri.allowlist.protocol.assetScope` | `app.security.assetProtocol.scope` |
| `tauri.pattern` | `app.security.pattern` |
| `build.distDir` | `build.frontendDist` |
| `build.devPath` | `build.devUrl` |
| `build.withGlobalTauri` | `app.withGlobalTauri` |
| `tauri.windows[].fileDropEnabled` | `app.windows[].dragDropEnabled` |

### Critical Warnings

**NEVER** skip running `npx @tauri-apps/cli migrate` -- manual migration is error-prone and the CLI handles most conversions automatically.

**NEVER** forget to implement update UI -- Tauri v2 removed the automatic update dialog. Without explicit update checking code, users will NEVER receive updates.

**NEVER** use old import paths after migration -- `@tauri-apps/api/tauri` is now `@tauri-apps/api/core`; module-specific APIs moved to plugin packages.

**NEVER** use `"v1Compatible"` for `createUpdaterArtifacts` in new projects -- only use it when migrating existing installations from v1 updater.

**ALWAYS** restructure for mobile support if targeting mobile -- split `main.rs` into `lib.rs` + `main.rs` with `#[cfg_attr(mobile, tauri::mobile_entry_point)]`.

**ALWAYS** add core permissions to capabilities -- v2 requires explicit permissions even for core features (windows, events, paths).

---

## Rust API Changes

### Type Renames

| Tauri v1 | Tauri v2 |
|----------|----------|
| `Window` | `WebviewWindow` |
| `WindowBuilder` | `WebviewWindowBuilder` |
| `WindowUrl` | `WebviewUrl` |
| `Manager::get_window()` | `Manager::get_webview_window()` |

### Removed Modules (Now Plugins)

| v1 Module | v2 Replacement |
|-----------|---------------|
| `api::dialog` | `tauri-plugin-dialog` |
| `api::http` | `tauri-plugin-http` |
| `api::path` | `Manager::path()` methods |
| `api::process` | `tauri-plugin-process` |
| `api::shell` | `tauri-plugin-shell` |

### Removed Manager Methods

| v1 Method | v2 Replacement |
|-----------|---------------|
| `App::clipboard_manager()` | `tauri-plugin-clipboard-manager` |
| `App::get_cli_matches()` | `tauri-plugin-cli` |
| `App::global_shortcut_manager()` | `tauri-plugin-global-shortcut` |

---

## JavaScript API Changes

### Module Renames

| Tauri v1 | Tauri v2 |
|----------|----------|
| `@tauri-apps/api/tauri` | `@tauri-apps/api/core` |
| `@tauri-apps/api/window` | `@tauri-apps/api/webviewWindow` |

### Non-Core Modules Removed

All non-core modules removed from `@tauri-apps/api`. Install per-plugin packages:

| v1 Import | v2 Plugin Package |
|-----------|------------------|
| `@tauri-apps/api/dialog` | `@tauri-apps/plugin-dialog` |
| `@tauri-apps/api/fs` | `@tauri-apps/plugin-fs` |
| `@tauri-apps/api/http` | `@tauri-apps/plugin-http` |
| `@tauri-apps/api/shell` | `@tauri-apps/plugin-shell` |
| `@tauri-apps/api/notification` | `@tauri-apps/plugin-notification` |
| `@tauri-apps/api/clipboard` | `@tauri-apps/plugin-clipboard-manager` |
| `@tauri-apps/api/os` | `@tauri-apps/plugin-os` |
| `@tauri-apps/api/process` | `@tauri-apps/plugin-process` |
| `@tauri-apps/api/updater` | `@tauri-apps/plugin-updater` |

---

## Event System Changes

| Aspect | Tauri v1 | Tauri v2 |
|--------|----------|----------|
| `emit()` | Emits to specific window | Broadcasts to ALL listeners |
| Targeted emit | N/A | New `emit_to()` function |
| Global listen | `listen_global()` | Renamed to `listen_any()` |
| Window listen | Receives all events | `WebviewWindow.listen()` only receives events for that specific window |

---

## Menu System Overhaul

| Tauri v1 | Tauri v2 |
|----------|----------|
| `Menu` | `MenuBuilder` |
| `CustomMenuItem` | `MenuItemBuilder` |
| `Submenu` | `SubmenuBuilder` |
| `MenuItem` (predefined) | `PredefinedMenuItem` |
| `SystemTray` | `TrayIconBuilder` |
| `Builder::on_menu_event()` | `App::on_menu_event()` or `AppHandle::on_menu_event()` |

---

## Feature Flag Changes

**Removed flags:**
- `reqwest-client`
- `reqwest-native-tls-vendored`
- `process-command-api`
- `shell-open-api`
- `windows7-compat`
- `updater`
- `linux-protocol-headers`
- `system-tray`

**Added flags:**
- `linux-protocol-body`

---

## Plugin Migration Table

| Feature | Cargo Crate | npm Package |
|---------|-------------|-------------|
| Clipboard | `tauri-plugin-clipboard-manager = "2"` | `@tauri-apps/plugin-clipboard-manager` |
| Dialogs | `tauri-plugin-dialog = "2"` | `@tauri-apps/plugin-dialog` |
| File System | `tauri-plugin-fs = "2"` | `@tauri-apps/plugin-fs` |
| Global Shortcuts | `tauri-plugin-global-shortcut = "2"` | `@tauri-apps/plugin-global-shortcut` |
| HTTP | `tauri-plugin-http = "2"` | `@tauri-apps/plugin-http` |
| Notifications | `tauri-plugin-notification = "2"` | `@tauri-apps/plugin-notification` |
| OS Info | `tauri-plugin-os = "2"` | `@tauri-apps/plugin-os` |
| Process | `tauri-plugin-process = "2"` | `@tauri-apps/plugin-process` |
| Shell | `tauri-plugin-shell = "2"` | `@tauri-apps/plugin-shell` |
| CLI Parsing | `tauri-plugin-cli = "2"` | `@tauri-apps/plugin-cli` |
| Updater | `tauri-plugin-updater = "2"` | `@tauri-apps/plugin-updater` |

---

## Version Feature Matrix

| Feature | Tauri v1 | Tauri v2 |
|---------|----------|----------|
| Desktop support | Yes | Yes |
| Mobile support | No | Yes (iOS + Android) |
| Permission system | Allowlist (boolean flags) | Capabilities + Permissions (fine-grained) |
| Plugin architecture | Monolithic API | Modular plugin packages |
| Menu API | Static builder | Dynamic builder pattern |
| Tray API | `SystemTray` | `TrayIconBuilder` |
| Event broadcasting | Per-window default | Global broadcast default |
| IPC Channels | Not available | `Channel<T>` for streaming |
| Window types | `Window` only | `Window` + `Webview` + `WebviewWindow` |
| Config format | Nested under `tauri` key | Flat top-level keys |
| Update dialog | Built-in automatic | Must implement manually |
| Shell open | Built into shell module | Separate `opener` plugin |
| Binary data IPC | Not optimized | `Response` type bypasses JSON |

---

## Mobile Restructuring

If targeting mobile, restructure the Rust entry point:

**Before (v1 style, desktop only):**

```rust
// src-tauri/src/main.rs
fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![])
        .run(tauri::generate_context!())
        .expect("error running app");
}
```

**After (v2 style, desktop + mobile):**

```rust
// src-tauri/src/lib.rs
#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![])
        .run(tauri::generate_context!())
        .expect("error running app");
}
```

```rust
// src-tauri/src/main.rs (minimal)
fn main() {
    app_lib::run();
}
```

**Cargo.toml for mobile:**

```toml
[lib]
name = "app_lib"
crate-type = ["staticlib", "cdylib", "rlib"]
```

---

## Reference Links

- [references/methods.md](references/methods.md) -- Complete v1-to-v2 API mapping tables
- [references/examples.md](references/examples.md) -- Before/after migration code examples
- [references/anti-patterns.md](references/anti-patterns.md) -- Migration mistakes with explanations

### Official Sources

- https://v2.tauri.app/start/migrate/from-tauri-1/
- https://v2.tauri.app/develop/
- https://v2.tauri.app/security/
