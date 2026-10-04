---
name: tauri-impl-plugin-development
description: >
  Use when building custom Tauri 2 plugins, adding lifecycle hooks, or defining plugin permissions.
  Prevents incorrect plugin Builder chain ordering and missing build.rs permission generation.
  Covers plugin::Builder API, plugin commands and state, lifecycle hooks, mobile plugin development, and permission patterns.
  Keywords: tauri plugin development, plugin Builder, lifecycle hooks, on_event, on_navigation, build.rs, custom plugin.
license: MIT
compatibility: "Designed for Claude Code. Requires Tauri 2.x with Rust and TypeScript."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# tauri-impl-plugin-development

## Quick Reference

### Plugin Builder API

| Method | Purpose | Example |
|--------|---------|---------|
| `Builder::new("name")` | Create plugin builder | `Builder::new("my-plugin")` |
| `.invoke_handler()` | Register plugin commands | `.invoke_handler(generate_handler![cmd])` |
| `.setup()` | Plugin initialization hook | `.setup(\|app, api\| { Ok(()) })` |
| `.on_event()` | App event handler | `.on_event(\|app, event\| { })` |
| `.on_navigation()` | Webview navigation filter | `.on_navigation(\|window, url\| true)` |
| `.on_webview_ready()` | Webview ready hook | `.on_webview_ready(\|window\| { })` |
| `.on_drop()` | Plugin cleanup hook | `.on_drop(\|app\| { })` |
| `.build()` | Finalize and return TauriPlugin | `.build()` |

### Plugin Command Invocation (Frontend)

| Pattern | Example |
|---------|---------|
| Command prefix | `plugin:<name>\|<command>` |
| JS invoke call | `invoke('plugin:my-plugin\|do_something', { arg: 'value' })` |

### Plugin Permission Generation

| Item | Description |
|------|-------------|
| `build.rs` location | Plugin crate root |
| Command list | `const COMMANDS: &[&str] = &["cmd_a", "cmd_b"];` |
| Builder call | `tauri_plugin::Builder::new(COMMANDS).build();` |
| Generated permissions | `allow-cmd-a`, `deny-cmd-a`, `allow-cmd-b`, `deny-cmd-b` |

### Critical Warnings

**NEVER** use multiple `.invoke_handler()` calls on the app `Builder` -- only the last one takes effect. Plugin commands use their own `.invoke_handler()` on the plugin `Builder`.

**NEVER** forget the `R: Runtime` generic on plugin command functions -- plugin commands MUST use `<R: Runtime>` to remain runtime-agnostic.

**NEVER** register plugin state on the app Builder -- use `app.manage()` inside the plugin's `.setup()` hook.

**NEVER** skip `build.rs` permission generation -- without it, plugin commands will fail with "command not allowed" at runtime.

**ALWAYS** use the `plugin:<name>|<command>` prefix when invoking plugin commands from JavaScript.

**ALWAYS** return `TauriPlugin<R>` (or `TauriPlugin<R, C>` with config) from the plugin init function.

---

## Essential Patterns

### Pattern 1: Minimal Plugin Structure

```rust
// src-tauri/src/plugins/my_plugin.rs (or separate crate)
use tauri::plugin::{Builder, TauriPlugin};
use tauri::Runtime;

#[tauri::command]
async fn do_something<R: Runtime>(
    app: tauri::AppHandle<R>,
    value: String,
) -> Result<String, String> {
    Ok(format!("Processed: {}", value))
}

pub fn init<R: Runtime>() -> TauriPlugin<R> {
    Builder::new("my-plugin")
        .invoke_handler(tauri::generate_handler![do_something])
        .build()
}
```

Register in the app:

```rust
// src-tauri/src/lib.rs
tauri::Builder::default()
    .plugin(my_plugin::init())
    .run(tauri::generate_context!())
    .expect("error while running tauri application");
```

### Pattern 2: Plugin with State

```rust
use std::sync::Mutex;
use tauri::plugin::{Builder, TauriPlugin};
use tauri::{Manager, Runtime};

#[derive(Default)]
struct PluginState {
    count: u32,
}

#[tauri::command]
async fn increment<R: Runtime>(
    app: tauri::AppHandle<R>,
) -> Result<u32, String> {
    let state = app.state::<Mutex<PluginState>>();
    let mut s = state.lock().unwrap();
    s.count += 1;
    Ok(s.count)
}

pub fn init<R: Runtime>() -> TauriPlugin<R> {
    Builder::new("counter")
        .invoke_handler(tauri::generate_handler![increment])
        .setup(|app, _api| {
            app.manage(Mutex::new(PluginState::default()));
            Ok(())
        })
        .build()
}
```

### Pattern 3: Plugin with Configuration

Read configuration from `tauri.conf.json` under `plugins.<name>`:

```rust
use serde::Deserialize;
use tauri::plugin::{Builder, TauriPlugin};
use tauri::Runtime;

#[derive(Deserialize)]
struct PluginConfig {
    timeout: u64,
    api_key: String,
}

pub fn init<R: Runtime>() -> TauriPlugin<R, PluginConfig> {
    Builder::<R, PluginConfig>::new("my-plugin")
        .setup(|app, api| {
            let config = api.config();
            println!("Configured timeout: {}", config.timeout);
            Ok(())
        })
        .build()
}
```

Configuration in `tauri.conf.json`:

```json
{
  "plugins": {
    "my-plugin": {
      "timeout": 30,
      "api_key": "abc123"
    }
  }
}
```

### Pattern 4: Full Lifecycle Hooks

```rust
use tauri::plugin::Builder;
use tauri::{RunEvent, Runtime};

pub fn init<R: Runtime>() -> tauri::plugin::TauriPlugin<R> {
    Builder::new("lifecycle-demo")
        .setup(|app, _api| {
            // Runs once during plugin initialization
            // Use for state registration, background tasks
            Ok(())
        })
        .on_navigation(|window, url| {
            // Return false to BLOCK navigation
            // Return true to ALLOW navigation
            url.scheme() != "forbidden"
        })
        .on_webview_ready(|window| {
            // Runs when a webview becomes ready
            // Use for per-window setup, listeners
        })
        .on_event(|app, event| {
            match event {
                RunEvent::ExitRequested { api, .. } => {
                    // Optionally prevent exit
                    // api.prevent_exit();
                }
                RunEvent::Exit => {
                    // Final cleanup before process ends
                }
                _ => {}
            }
        })
        .on_drop(|app| {
            // Runs when plugin is destroyed
            // Use for resource cleanup
        })
        .build()
}
```

### Pattern 5: Plugin Permissions via build.rs

For plugins distributed as separate crates, auto-generate permissions:

```rust
// build.rs (in the plugin crate root)
const COMMANDS: &[&str] = &["do_something", "get_status", "configure"];

fn main() {
    tauri_plugin::Builder::new(COMMANDS).build();
}
```

This generates permissions like `allow-do-something`, `deny-do-something` etc. Reference them in capability files:

```json
{
  "identifier": "default",
  "windows": ["main"],
  "permissions": [
    "my-plugin:allow-do-something",
    "my-plugin:allow-get-status"
  ]
}
```

### Pattern 6: Scoped Commands

Access command-level and global-level scopes in plugin commands:

```rust
use tauri::ipc::{CommandScope, GlobalScope};
use serde::Deserialize;

#[derive(Debug, Deserialize)]
struct ScopeEntry {
    path: String,
}

#[tauri::command]
async fn scoped_read<R: tauri::Runtime>(
    command_scope: CommandScope<'_, ScopeEntry>,
    global_scope: GlobalScope<'_, ScopeEntry>,
    path: String,
) -> Result<String, String> {
    let allowed = command_scope.allows();
    let denied = command_scope.denies();
    // Validate path against scope entries before proceeding
    Ok("data".into())
}
```

---

## Plugin File Structure

For a standalone plugin crate:

```
tauri-plugin-my-plugin/
  src/
    lib.rs          # Plugin init function, commands
    commands.rs     # Command implementations (optional split)
    state.rs        # Plugin state types (optional)
  permissions/
    default.toml    # Default permission set
  build.rs          # Permission auto-generation
  Cargo.toml
```

For an in-app plugin (simpler):

```
src-tauri/src/
  plugins/
    my_plugin.rs    # Plugin init + commands
  lib.rs            # Registers plugin via .plugin()
```

---

## Reference Links

- [references/methods.md](references/methods.md) -- Complete API signatures for plugin::Builder, TauriPlugin, PluginApi, CommandScope, GlobalScope
- [references/examples.md](references/examples.md) -- Working code examples for plugin development patterns
- [references/anti-patterns.md](references/anti-patterns.md) -- Common plugin development mistakes with explanations

### Official Sources

- https://v2.tauri.app/develop/plugins/
- https://docs.rs/tauri/latest/tauri/plugin/struct.Builder.html
- https://docs.rs/tauri/latest/tauri/plugin/type.TauriPlugin.html
