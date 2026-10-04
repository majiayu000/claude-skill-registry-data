---
name: tauri-impl-project-setup
description: >
  Use when starting a new Tauri 2 project, choosing a frontend framework, or understanding project structure.
  Prevents incorrect lib.rs/main.rs split and missing build configuration that breaks dev and production builds.
  Covers create-tauri-app scaffolding, project structure, frontend framework integration, src-tauri layout, and source control.
  Keywords: tauri project setup, create-tauri-app, scaffolding, lib.rs, main.rs, frontend framework, project structure.
license: MIT
compatibility: "Designed for Claude Code. Requires Tauri 2.x with Rust and TypeScript."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# tauri-impl-project-setup

## Quick Reference

### Scaffolding Commands

| Package Manager | Command |
|----------------|---------|
| npm | `npm create tauri-app@latest` |
| yarn | `yarn create tauri-app` |
| pnpm | `pnpm create tauri-app` |
| bun | `bunx create-tauri-app` |
| cargo | `cargo create-tauri-app` |

### Project Structure

```
my-tauri-app/
├── src/                        # Frontend source (varies by framework)
│   ├── index.html
│   ├── main.ts
│   └── styles.css
├── src-tauri/                  # Rust backend
│   ├── src/
│   │   ├── lib.rs              # App logic (mobile entry point)
│   │   └── main.rs             # Desktop entry point (calls lib.rs)
│   ├── capabilities/           # Permission capability files
│   │   └── default.json        # Default window capabilities
│   ├── permissions/            # Custom command permissions (optional)
│   ├── icons/                  # Application icons (all sizes)
│   ├── gen/                    # Generated files (schemas, etc.)
│   │   └── schemas/
│   ├── Cargo.toml              # Rust dependencies
│   ├── Cargo.lock              # Deterministic build lock
│   ├── tauri.conf.json         # Main configuration
│   ├── build.rs                # Cargo build script
│   └── .taurignore             # Exclude files from watch
├── package.json                # Frontend dependencies
├── tsconfig.json               # TypeScript config
└── vite.config.ts              # Bundler config (if Vite)
```

### Key Config Files

| File | Location | Purpose |
|------|----------|---------|
| `tauri.conf.json` | `src-tauri/` | Main app configuration |
| `Cargo.toml` | `src-tauri/` | Rust crate dependencies |
| `Cargo.lock` | `src-tauri/` | Deterministic dependency lock |
| `default.json` | `src-tauri/capabilities/` | Permission grants for windows |
| `build.rs` | `src-tauri/` | Build script (plugin permission gen) |
| `package.json` | root | Frontend dependencies |

### Critical Warnings

**ALWAYS** commit `src-tauri/Cargo.lock` to source control -- it ensures deterministic builds across environments.

**ALWAYS** add `src-tauri/target/` to `.gitignore` -- build artifacts should NEVER be committed.

**NEVER** put app logic in `main.rs` only -- ALWAYS use the `lib.rs` + `main.rs` split pattern for mobile compatibility.

**NEVER** forget to set a unique `identifier` in `tauri.conf.json` -- duplicate identifiers cause conflicts with other apps on the system.

**ALWAYS** set `beforeDevCommand` and `beforeBuildCommand` in `tauri.conf.json` -- without them, the frontend dev server will not start and builds will lack compiled assets.

**NEVER** skip adding `core:default` permissions in your capability file -- basic window and event operations will fail silently.

---

## Essential Patterns

### Pattern 1: Creating a New Project

```bash
# Interactive scaffolding (recommended)
npm create tauri-app@latest

# This prompts for:
# - Project name
# - Package manager (npm, yarn, pnpm, bun, cargo)
# - Frontend language (TypeScript, JavaScript, Rust)
# - Frontend framework (React, Vue, Svelte, SolidJS, vanilla, etc.)
```

After scaffolding:

```bash
cd my-tauri-app
npm install          # Install frontend dependencies
npm run tauri dev    # Start development mode
```

### Pattern 2: The lib.rs + main.rs Split

This is the REQUIRED pattern for mobile support. Even for desktop-only apps, use this pattern to future-proof your codebase.

**`src-tauri/src/lib.rs`** -- Contains all app logic:

```rust
#[tauri::command]
fn greet(name: String) -> String {
    format!("Hello, {}!", name)
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![greet])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

**`src-tauri/src/main.rs`** -- Desktop entry point (thin wrapper):

```rust
// Prevents additional console window on Windows in release
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

fn main() {
    my_tauri_app_lib::run();
}
```

**WHY this split matters**: On mobile platforms (iOS/Android), there is no `main()` function. The `#[cfg_attr(mobile, tauri::mobile_entry_point)]` macro generates the platform-specific entry point on `lib.rs`. Without this split, your app cannot compile for mobile.

### Pattern 3: Minimal tauri.conf.json

```json
{
  "$schema": "./gen/schemas/desktop-schema.json",
  "identifier": "com.example.myapp",
  "build": {
    "devUrl": "http://localhost:5173",
    "frontendDist": "../dist",
    "beforeDevCommand": "npm run dev",
    "beforeBuildCommand": "npm run build"
  },
  "app": {
    "windows": [
      {
        "title": "My App",
        "width": 800,
        "height": 600
      }
    ]
  },
  "bundle": {
    "active": true,
    "icon": [
      "icons/32x32.png",
      "icons/128x128.png",
      "icons/128x128@2x.png",
      "icons/icon.icns",
      "icons/icon.ico"
    ]
  }
}
```

### Pattern 4: Default Capability File

**`src-tauri/capabilities/default.json`**:

```json
{
  "$schema": "../gen/schemas/desktop-schema.json",
  "identifier": "default",
  "description": "Default permissions for the main window",
  "windows": ["main"],
  "permissions": [
    "core:default",
    "core:window:default",
    "core:webview:default"
  ]
}
```

This grants the main window access to core features. Without this, even basic window operations fail.

### Pattern 5: Frontend Framework Integration

All frameworks follow the same integration pattern: the frontend runs its dev server, and Tauri proxies to it.

**Vite (React/Vue/Svelte/SolidJS):**

```json
{
  "build": {
    "devUrl": "http://localhost:5173",
    "frontendDist": "../dist",
    "beforeDevCommand": "npm run dev",
    "beforeBuildCommand": "npm run build"
  }
}
```

**Next.js (SSG mode):**

```json
{
  "build": {
    "devUrl": "http://localhost:3000",
    "frontendDist": "../out",
    "beforeDevCommand": "npm run dev",
    "beforeBuildCommand": "npm run build && npm run export"
  }
}
```

**No framework (vanilla):**

```json
{
  "build": {
    "frontendDist": "../src"
  }
}
```

When using vanilla HTML/CSS/JS without a dev server, omit `devUrl` and `beforeDevCommand`. Tauri serves the files directly.

### Pattern 6: Key Dependencies

**`package.json`:**

```json
{
  "devDependencies": {
    "@tauri-apps/cli": "^2"
  },
  "dependencies": {
    "@tauri-apps/api": "^2"
  },
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "tauri": "tauri"
  }
}
```

**`src-tauri/Cargo.toml`:**

```toml
[package]
name = "my-tauri-app"
version = "0.1.0"
edition = "2021"

[lib]
name = "my_tauri_app_lib"
crate-type = ["staticlib", "cdylib", "rlib"]

[build-dependencies]
tauri-build = { version = "2", features = [] }

[dependencies]
tauri = { version = "2", features = [] }
tauri-plugin-opener = "2"
serde = { version = "1", features = ["derive"] }
serde_json = "1"
```

The `crate-type` array is required for mobile builds: `staticlib` for iOS, `cdylib` for Android, `rlib` for desktop.

### Pattern 7: Development Commands

```bash
# Start development (hot-reload frontend + Rust backend)
npm run tauri dev

# Build for production
npm run tauri build

# Generate icons from a source image
npm run tauri icon /path/to/app-icon.png

# Generate TypeScript bindings
npm run tauri completions
```

### Pattern 8: Adding Plugins

```bash
# Install plugin (both Rust crate and npm package)
npm run tauri plugin add fs

# This does three things:
# 1. Adds tauri-plugin-fs to src-tauri/Cargo.toml
# 2. Adds @tauri-apps/plugin-fs to package.json
# 3. Registers the plugin in lib.rs
```

After installation, ALWAYS add the plugin's permissions to your capability file:

```json
{
  "permissions": [
    "core:default",
    "fs:default"
  ]
}
```

---

## Source Control Best Practices

### .gitignore

```gitignore
# Frontend build artifacts
dist/
node_modules/

# Rust build artifacts
src-tauri/target/

# Generated schemas (regenerated on build)
src-tauri/gen/

# OS-specific
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/
```

### Files to ALWAYS Commit

| File | Why |
|------|-----|
| `src-tauri/Cargo.lock` | Deterministic Rust builds |
| `src-tauri/tauri.conf.json` | App configuration |
| `src-tauri/capabilities/*.json` | Security permissions |
| `src-tauri/icons/*` | Application icons |
| `package-lock.json` / `pnpm-lock.yaml` | Deterministic JS builds |

### Files to NEVER Commit

| File/Dir | Why |
|----------|-----|
| `src-tauri/target/` | Build artifacts (large, platform-specific) |
| `node_modules/` | Installed packages (reproducible from lockfile) |
| `dist/` | Frontend build output (regenerated) |

---

## Configuration Deep Dive

### Build Section

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `devUrl` | `string` | For dev server | URL of the frontend dev server |
| `frontendDist` | `string` | Yes | Path to compiled frontend assets |
| `beforeDevCommand` | `string` | For dev server | Command to start dev server |
| `beforeBuildCommand` | `string` | Yes | Command to build frontend |
| `beforeBundleCommand` | `string` | No | Command before bundling phase |
| `features` | `string[]` | No | Cargo feature flags to enable |

### Window Configuration (`app.windows[]`)

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `label` | `string` | `"main"` | Unique window identifier |
| `title` | `string` | -- | Window title bar text |
| `url` | `string` | `"/"` | URL or path to load |
| `width` / `height` | `number` | -- | Size in logical pixels |
| `minWidth` / `minHeight` | `number` | -- | Minimum dimensions |
| `resizable` | `boolean` | `true` | Allow resizing |
| `fullscreen` | `boolean` | `false` | Start fullscreen |
| `decorations` | `boolean` | `true` | Show title bar/borders |
| `transparent` | `boolean` | `false` | Enable transparency |
| `create` | `boolean` | `true` | Create at startup |

### Top-Level Configuration

| Property | Required | Description |
|----------|----------|-------------|
| `identifier` | **Yes** | Reverse-domain notation (e.g., `com.company.app`) |
| `productName` | No | Display name of the application |
| `version` | No | Semver version string |

---

## Reference Links

- [references/methods.md](references/methods.md) -- CLI commands, Cargo.toml options, and tauri.conf.json schema
- [references/examples.md](references/examples.md) -- Complete project setup examples for different frameworks
- [references/anti-patterns.md](references/anti-patterns.md) -- Common setup mistakes and how to avoid them

### Official Sources

- https://v2.tauri.app/start/create-project/
- https://v2.tauri.app/develop/
- https://v2.tauri.app/reference/config/
