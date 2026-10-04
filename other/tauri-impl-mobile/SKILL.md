---
name: tauri-impl-mobile
description: >
  Use when targeting Android or iOS, writing platform-specific code, or setting up mobile development environment.
  Prevents missing crate-type configuration and incorrect lib.rs entry point that breaks mobile builds.
  Covers Android and iOS target setup, tauri android/ios commands, cfg attributes, lib.rs restructuring, and Cargo.toml config.
  Keywords: tauri mobile, android, ios, cfg(mobile), crate-type, mobile entry point, platform-specific code.
license: MIT
compatibility: "Designed for Claude Code. Requires Tauri 2.x with Rust and TypeScript."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# tauri-impl-mobile

## Quick Reference

### CLI Commands

| Command | Purpose |
|---------|---------|
| `tauri android init` | Initialize Android project files |
| `tauri ios init` | Initialize iOS project files (macOS only) |
| `tauri android dev` | Run on Android emulator/device |
| `tauri ios dev` | Run on iOS simulator/device |
| `tauri android build` | Production build for Android |
| `tauri ios build` | Production build for iOS |

### Platform cfg Attributes

| Attribute | Matches |
|-----------|---------|
| `#[cfg(mobile)]` | Android and iOS |
| `#[cfg(desktop)]` | Windows, macOS, Linux |
| `#[cfg(target_os = "android")]` | Android only |
| `#[cfg(target_os = "ios")]` | iOS only |
| `#[cfg(target_os = "windows")]` | Windows only |
| `#[cfg(target_os = "macos")]` | macOS only |
| `#[cfg(target_os = "linux")]` | Linux only |

### Required Cargo.toml Configuration

```toml
[lib]
name = "app_lib"
crate-type = ["staticlib", "cdylib", "rlib"]
```

### Entry Point Structure

| File | Purpose |
|------|---------|
| `src-tauri/src/lib.rs` | Shared app logic, `run()` function with `#[cfg_attr(mobile, tauri::mobile_entry_point)]` |
| `src-tauri/src/main.rs` | Desktop-only entry point, calls `app_lib::run()` |

### Critical Warnings

**NEVER** skip the `lib.rs` + `main.rs` split when targeting mobile -- mobile platforms require a library crate, not a binary.

**NEVER** omit `"staticlib"` from `crate-type` -- iOS requires static linking.

**NEVER** omit `"cdylib"` from `crate-type` -- Android requires dynamic linking.

**NEVER** forget the `#[cfg_attr(mobile, tauri::mobile_entry_point)]` attribute on the `run()` function -- without it, the mobile app has no entry point and will not start.

**ALWAYS** keep `"rlib"` in `crate-type` -- the desktop `main.rs` depends on it to import `app_lib::run()`.

**ALWAYS** test platform-specific code paths on actual target platforms -- `#[cfg]` attributes silently exclude code at compile time.

---

## Prerequisites

### Android

1. **Android Studio** with:
   - SDK Platform (API level 24+)
   - Platform-Tools
   - NDK (Side by side)
   - Build-Tools
   - Command-line Tools

2. **Environment variables**:
   ```bash
   export JAVA_HOME="/path/to/jdk"
   export ANDROID_HOME="/path/to/Android/Sdk"
   export NDK_HOME="$ANDROID_HOME/ndk/<version>"
   ```

3. **Rust targets**:
   ```bash
   rustup target add aarch64-linux-android
   rustup target add armv7-linux-androideabi
   rustup target add i686-linux-android
   rustup target add x86_64-linux-android
   ```

### iOS (macOS only)

1. **Xcode** (full installation, not just Command Line Tools)

2. **Cocoapods**:
   ```bash
   brew install cocoapods
   ```

3. **Rust targets**:
   ```bash
   rustup target add aarch64-apple-ios
   rustup target add x86_64-apple-ios
   rustup target add aarch64-apple-ios-sim
   ```

---

## Essential Patterns

### Pattern 1: Project Restructuring for Mobile

Transform a desktop-only project to support mobile:

**Before** (desktop only):
```
src-tauri/src/
  main.rs    # Contains all app logic
```

**After** (desktop + mobile):
```
src-tauri/src/
  lib.rs     # All app logic moves here
  main.rs    # Minimal desktop entry point
```

```rust
// src-tauri/src/lib.rs
#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![/* commands */])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

```rust
// src-tauri/src/main.rs
// Prevents an additional console window on Windows in release
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

fn main() {
    app_lib::run();
}
```

```toml
# src-tauri/Cargo.toml
[lib]
name = "app_lib"
crate-type = ["staticlib", "cdylib", "rlib"]
```

### Pattern 2: Platform-Specific Code

```rust
// Conditional compilation for platform-specific behavior
#[cfg(desktop)]
fn setup_desktop(app: &tauri::App) {
    // Desktop-only: system tray, global shortcuts, etc.
}

#[cfg(mobile)]
fn setup_mobile(app: &tauri::App) {
    // Mobile-only: biometrics, push notifications, etc.
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    let builder = tauri::Builder::default();

    #[cfg(desktop)]
    let builder = builder.setup(|app| {
        setup_desktop(app);
        Ok(())
    });

    #[cfg(mobile)]
    let builder = builder.setup(|app| {
        setup_mobile(app);
        Ok(())
    });

    builder
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

### Pattern 3: Platform-Specific Commands

```rust
#[cfg(desktop)]
#[tauri::command]
fn open_dev_tools(window: tauri::WebviewWindow) {
    window.open_devtools();
}

#[cfg(mobile)]
#[tauri::command]
fn request_biometric() -> Result<bool, String> {
    // Mobile biometric authentication
    Ok(true)
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![
            // Shared commands
            shared_command,
            // Platform-specific commands
            #[cfg(desktop)]
            open_dev_tools,
            #[cfg(mobile)]
            request_biometric,
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

### Pattern 4: Mobile Bundle Configuration

```json
// tauri.conf.json
{
  "bundle": {
    "iOS": {
      "minimumSystemVersion": "14.0"
    },
    "android": {
      "minSdkVersion": 24,
      "versionCode": 1
    }
  }
}
```

### Pattern 5: Initializing and Running Mobile Targets

```bash
# One-time initialization (generates platform project files)
tauri android init
tauri ios init

# Development (hot-reload)
tauri android dev
tauri ios dev

# Development on a specific device
tauri android dev --device <device-id>
tauri ios dev --device <device-id>

# Production builds
tauri android build
tauri ios build

# Production build for specific target
tauri android build --target aarch64
tauri ios build --target aarch64-apple-ios
```

### Pattern 6: Mobile Plugin Hooks

Plugins can have mobile-specific initialization:

```rust
use tauri::plugin::{Builder, TauriPlugin};
use tauri::Runtime;

pub fn init<R: Runtime>() -> TauriPlugin<R> {
    Builder::new("my-mobile-plugin")
        .setup(|app, api| {
            #[cfg(target_os = "android")]
            {
                // Android-specific plugin setup
                // Access Android-specific APIs via PluginApi
            }
            #[cfg(target_os = "ios")]
            {
                // iOS-specific plugin setup
            }
            Ok(())
        })
        .build()
}
```

---

## Crate-Type Explanation

The `crate-type` array in `Cargo.toml` controls how the Rust code is compiled:

| Crate Type | Purpose | Required For |
|------------|---------|--------------|
| `staticlib` | Static library (.a) | iOS -- statically linked into the app binary |
| `cdylib` | C-compatible dynamic library (.so/.dylib) | Android -- loaded as a JNI shared library |
| `rlib` | Rust library | Desktop -- `main.rs` imports `app_lib::run()` |

All three MUST be present for full cross-platform support.

---

## Project Structure After Mobile Init

```
my-tauri-app/
  src/                          # Frontend (shared across all platforms)
  src-tauri/
    src/
      lib.rs                    # Shared entry point
      main.rs                   # Desktop entry point
    gen/
      android/                  # Generated by `tauri android init`
        app/
          src/main/
            java/.../           # Android activity
        build.gradle.kts
      apple/                    # Generated by `tauri ios init`
        <app>.xcodeproj/
        Sources/
    Cargo.toml
    tauri.conf.json
```

---

## Reference Links

- [references/methods.md](references/methods.md) -- Complete reference for mobile CLI commands, cfg attributes, Cargo.toml configuration
- [references/examples.md](references/examples.md) -- Working code examples for mobile development patterns
- [references/anti-patterns.md](references/anti-patterns.md) -- Common mobile development mistakes with explanations

### Official Sources

- https://v2.tauri.app/start/prerequisites/#android
- https://v2.tauri.app/start/prerequisites/#ios
- https://v2.tauri.app/develop/mobile/
