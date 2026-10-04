---
name: tauri-agents-project-scaffolder
description: >
  Use when scaffolding a new Tauri 2 project, setting up initial project structure, or generating boilerplate code.
  Prevents incomplete scaffolding with missing permission files, unregistered commands, or broken IPC bridges.
  Covers configured plugins, capability files, Rust commands with TypeScript invoke calls, build pipeline, and frontend integration.
  Keywords: tauri scaffolder, project generator, boilerplate, scaffold, new project, project structure, code generation.
license: MIT
compatibility: "Designed for Claude Code. Requires Tauri 2.x."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# tauri-agents-project-scaffolder

## Scaffolding Workflow

Execute these steps in order when creating a new Tauri 2 project:

```
1. Gather requirements (app type, plugins, frontend framework)
2. Generate project structure
3. Configure Cargo.toml with dependencies
4. Configure tauri.conf.json
5. Create lib.rs with commands and plugin registration
6. Create main.rs (desktop entry point)
7. Create capability files
8. Create custom command permissions
9. Create frontend invoke wrappers
10. Create .gitignore
11. Verify completeness
```

---

## Step 1: Requirements Gathering

**ALWAYS** determine these before generating files:

```
[ ] App type: basic | multi-window | tray-app | mobile-ready
[ ] Frontend framework: vanilla | React | Vue | Svelte | SolidJS
[ ] Bundler: Vite (default) | Webpack | other
[ ] Plugins needed: fs | dialog | store | shell | http | notification | others
[ ] Target platforms: desktop-only | desktop+mobile | all
[ ] Feature requirements: auto-updater | tray icon | custom protocol | menus
```

---

## Step 2: Project Structure Template

### Basic App

```
my-tauri-app/
├── src/                           # Frontend
│   ├── index.html
│   ├── main.ts
│   ├── styles.css
│   └── lib/
│       └── tauri.ts               # Invoke wrappers
├── src-tauri/
│   ├── src/
│   │   ├── lib.rs                 # App logic + command registration
│   │   ├── main.rs                # Desktop entry point
│   │   ├── commands.rs            # Command implementations
│   │   └── error.rs               # Error types
│   ├── capabilities/
│   │   └── default.json           # Permission grants
│   ├── permissions/
│   │   └── commands.toml          # Custom command permissions
│   ├── icons/                     # App icons (all sizes)
│   ├── Cargo.toml
│   ├── Cargo.lock
│   ├── build.rs
│   └── tauri.conf.json
├── package.json
├── tsconfig.json
├── vite.config.ts
└── .gitignore
```

### Multi-Window App

Adds to basic structure:

```
src-tauri/
├── capabilities/
│   ├── main-window.json           # Main window permissions
│   └── settings-window.json       # Settings window permissions
```

### Tray App

Adds to basic structure:

```
src-tauri/src/
├── tray.rs                        # Tray icon setup + menu
```

---

## Step 3: Cargo.toml Template

```toml
[package]
name = "app"
version = "0.1.0"
description = "A Tauri 2 application"
edition = "2021"

[lib]
name = "app_lib"
crate-type = ["staticlib", "cdylib", "rlib"]

[build-dependencies]
tauri-build = { version = "2", features = [] }

[dependencies]
tauri = { version = "2", features = [] }
serde = { version = "1", features = ["derive"] }
serde_json = "1"
thiserror = "2"
tokio = { version = "1", features = ["full"] }

# Plugins -- uncomment as needed:
# tauri-plugin-opener = "2"
# tauri-plugin-fs = "2"
# tauri-plugin-dialog = "2"
# tauri-plugin-store = "2"
# tauri-plugin-shell = "2"
# tauri-plugin-http = "2"
# tauri-plugin-notification = "2"
# tauri-plugin-clipboard-manager = "2"
# tauri-plugin-os = "2"
# tauri-plugin-process = "2"
# tauri-plugin-updater = "2"
# tauri-plugin-global-shortcut = "2"
# tauri-plugin-window-state = "2"
```

**Rules**:
- ALWAYS include `serde`, `serde_json`, `thiserror`
- ALWAYS include `tokio` with full features for async commands
- ALWAYS include `crate-type` with all three types for mobile compatibility
- NEVER forget `tauri-build` in build-dependencies

---

## Step 4: tauri.conf.json Template

```json
{
  "$schema": "./gen/schemas/desktop-schema.json",
  "productName": "My App",
  "version": "0.1.0",
  "identifier": "com.yourcompany.myapp",
  "build": {
    "devUrl": "http://localhost:5173",
    "frontendDist": "../dist",
    "beforeDevCommand": "npm run dev",
    "beforeBuildCommand": "npm run build"
  },
  "app": {
    "windows": [
      {
        "label": "main",
        "title": "My App",
        "url": "/",
        "width": 800,
        "height": 600,
        "minWidth": 400,
        "minHeight": 300,
        "resizable": true,
        "center": true
      }
    ],
    "security": {
      "csp": "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' asset: https://asset.localhost data:; connect-src ipc: http://ipc.localhost",
      "freezePrototype": true
    }
  },
  "bundle": {
    "active": true,
    "targets": "all",
    "icon": [
      "icons/32x32.png",
      "icons/128x128.png",
      "icons/128x128@2x.png",
      "icons/icon.icns",
      "icons/icon.ico"
    ]
  },
  "plugins": {}
}
```

**Rules**:
- ALWAYS set a unique `identifier`
- ALWAYS set `csp` (never null)
- ALWAYS set `freezePrototype: true`
- ALWAYS include `beforeBuildCommand` and `beforeDevCommand`

---

## Step 5: lib.rs Template

```rust
mod commands;
mod error;

use tauri::Manager;

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        // -- Plugins --
        .plugin(tauri_plugin_opener::init())
        // .plugin(tauri_plugin_fs::init())
        // .plugin(tauri_plugin_dialog::init())
        // .plugin(tauri_plugin_store::init())
        // -- State --
        // .manage(std::sync::Mutex::new(AppState::default()))
        // -- Commands --
        .invoke_handler(tauri::generate_handler![
            commands::greet,
        ])
        .setup(|app| {
            // Initialization that depends on App
            let _handle = app.handle().clone();
            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

**Rules**:
- ALWAYS use `#[cfg_attr(mobile, tauri::mobile_entry_point)]`
- ALWAYS use a single `generate_handler![]`
- ALWAYS put commands in a separate module
- NEVER mark command functions as `pub` in this file

---

## Step 6: main.rs Template

```rust
// Prevents additional console window on Windows in release
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

fn main() {
    app_lib::run();
}
```

---

## Step 7: Supporting Files

### error.rs

```rust
use serde::Serialize;

#[derive(Debug, thiserror::Error)]
pub enum AppError {
    #[error(transparent)]
    Io(#[from] std::io::Error),
    #[error("{0}")]
    Custom(String),
}

impl Serialize for AppError {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where S: serde::ser::Serializer {
        serializer.serialize_str(self.to_string().as_ref())
    }
}

pub type AppResult<T> = Result<T, AppError>;
```

### commands.rs

```rust
use crate::error::AppResult;

#[tauri::command]
pub fn greet(name: String) -> String {
    format!("Hello, {}! You've been greeted from Rust!", name)
}
```

### build.rs

```rust
fn main() {
    tauri_build::build();
}
```

---

## Step 8: Capability File Template

### capabilities/default.json

```json
{
  "$schema": "../gen/schemas/desktop-schema.json",
  "identifier": "default",
  "description": "Default capabilities for the main window",
  "windows": ["main"],
  "permissions": [
    "core:default",
    "core:window:default",
    "core:app:default",
    "allow-greet"
  ]
}
```

**Rules**:
- ALWAYS include `core:default`
- ALWAYS target specific window labels
- ALWAYS add permissions for every registered plugin
- ALWAYS add permissions for every custom command

---

## Step 9: Custom Command Permissions

### permissions/commands.toml

```toml
[[permission]]
identifier = "allow-greet"
description = "Allow the greet command"
commands.allow = ["greet"]
```

**Rules**:
- ALWAYS create a permission for every custom command
- ALWAYS use TOML format for application permissions
- Name pattern: `allow-<command-name>`

---

## Step 10: Frontend Invoke Wrappers

### src/lib/tauri.ts

```typescript
import { invoke } from '@tauri-apps/api/core';

export async function greet(name: string): Promise<string> {
    return invoke<string>('greet', { name });
}
```

**Rules**:
- ALWAYS create typed wrapper functions
- ALWAYS use camelCase for argument keys
- ALWAYS specify the generic return type on invoke
- ALWAYS export functions for use in components

---

## Step 11: .gitignore Template

```gitignore
# Dependencies
node_modules/

# Build output
dist/
src-tauri/target/
src-tauri/gen/

# Environment
.env
.env.*

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Do NOT ignore Cargo.lock -- it ensures deterministic builds
```

---

## App Type Templates

### Multi-Window App

- Add second window in `app.windows[]` with `"visible": false, "create": true`
- Create separate capability file per window with targeted permissions
- Add `show_settings` command using `app.get_webview_window("label")`
- See [references/examples.md](references/examples.md) for complete code

### Tray App

- Add `trayIcon` config in `app` section of `tauri.conf.json`
- Build tray menu in `setup()` using `TrayIconBuilder` and `MenuBuilder`
- Handle `CloseRequested` event to hide instead of close: `api.prevent_close()`
- See [references/examples.md](references/examples.md) for complete code

---

## Verification Checklist

After scaffolding, verify:

```
[ ] Cargo.toml: all needed plugins listed
[ ] lib.rs: all plugins initialized with .plugin()
[ ] lib.rs: all commands in generate_handler![]
[ ] lib.rs: state registered with manage() if needed
[ ] capabilities/: permissions for all plugins and commands
[ ] permissions/: TOML file for each custom command
[ ] Frontend: invoke wrapper for each Rust command
[ ] Frontend: @tauri-apps/api and plugin packages in package.json
[ ] tauri.conf.json: identifier is unique
[ ] tauri.conf.json: CSP is set
[ ] tauri.conf.json: build commands configured
[ ] .gitignore: target/ excluded, Cargo.lock NOT excluded
[ ] build.rs: calls tauri_build::build()
```

---

## Reference Links

- [references/methods.md](references/methods.md) -- Plugin installation commands, configuration keys
- [references/examples.md](references/examples.md) -- Complete scaffolded project examples
- [references/anti-patterns.md](references/anti-patterns.md) -- Scaffolding mistakes to avoid

### Official Sources

- https://v2.tauri.app/start/create-project/
- https://v2.tauri.app/develop/
- https://v2.tauri.app/security/capabilities/
