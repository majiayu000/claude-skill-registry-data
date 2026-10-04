---
name: tauri-errors-build
description: >
  Use when encountering Tauri 2 build errors, bundler failures, or platform-specific compilation issues.
  Prevents chasing phantom failures from stale build artifacts and misidentifying the failing build pipeline phase.
  Covers Cargo compilation failures, bundler errors, code signing failures, Linux dependencies, mobile builds, and CI/CD failures.
  Keywords: tauri build error, cargo compile, bundler error, code signing, linker error, NSIS, WiX, CI/CD failure.
license: MIT
compatibility: "Designed for Claude Code. Requires Tauri 2.x."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# tauri-errors-build

## Quick Diagnosis

When a Tauri 2 build fails, identify the phase first:

```
Build Pipeline Phases:
1. Frontend build   (beforeBuildCommand)  --> JS/TS errors
2. Cargo compile    (rustc)               --> Rust compilation errors
3. Bundler          (NSIS/WiX/DMG/deb)    --> Platform packaging errors
4. Code signing     (codesign/signtool)   --> Signing/notarization errors
```

**ALWAYS** read the FULL error output. The root cause is often buried above the final error message.

**NEVER** skip `cargo clean` when troubleshooting persistent compilation errors -- stale build artifacts cause phantom failures.

---

## Error Lookup Table: Cargo Compilation

### ERR-B001: Command function visibility in lib.rs

**Error**: `error[E0255]: the name X is defined multiple times` or cryptic macro expansion errors.

**Cause**: Command functions defined directly in `src-tauri/src/lib.rs` are marked `pub`.

**Fix**: ALWAYS remove `pub` from command functions in `lib.rs`. Commands in separate modules MUST be `pub`.

```rust
// WRONG -- in lib.rs
#[tauri::command]
pub fn greet(name: String) -> String { ... }

// CORRECT -- in lib.rs
#[tauri::command]
fn greet(name: String) -> String { ... }

// CORRECT -- in src-tauri/src/commands.rs (separate module)
#[tauri::command]
pub fn greet(name: String) -> String { ... }
```

### ERR-B002: Missing Serialize on error type

**Error**: `the trait bound MyError: Serialize is not satisfied`

**Cause**: Command return type `Result<T, E>` requires `E` to implement `serde::Serialize`.

**Fix**: ALWAYS implement `Serialize` manually for error enums that use `thiserror`:

```rust
#[derive(Debug, thiserror::Error)]
enum AppError {
    #[error(transparent)]
    Io(#[from] std::io::Error),
    #[error("not found: {0}")]
    NotFound(String),
}

impl serde::Serialize for AppError {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where S: serde::ser::Serializer {
        serializer.serialize_str(self.to_string().as_ref())
    }
}
```

### ERR-B003: Borrowed references in async commands

**Error**: `implementation of FnOnce is not general enough` or lifetime errors in async command signatures.

**Cause**: Async commands cannot use `&str` directly due to spawning on the tokio runtime.

**Fix**: Use owned types (`String`) or wrap return in `Result`:

```rust
// WRONG
#[tauri::command]
async fn process(value: &str) -> String { value.to_uppercase() }

// CORRECT -- option 1: owned type
#[tauri::command]
async fn process(value: String) -> String { value.to_uppercase() }

// CORRECT -- option 2: wrap in Result
#[tauri::command]
async fn process(value: &str) -> Result<String, ()> { Ok(value.to_uppercase()) }
```

### ERR-B004: Multiple invoke_handler calls

**Error**: Commands silently not working -- no compilation error.

**Cause**: Only the LAST `.invoke_handler()` call on `Builder` takes effect. Multiple calls do NOT merge.

**Fix**: ALWAYS use a single `generate_handler![]` with all commands:

```rust
// WRONG -- only cmd2 works
tauri::Builder::default()
    .invoke_handler(tauri::generate_handler![cmd1])
    .invoke_handler(tauri::generate_handler![cmd2])

// CORRECT
tauri::Builder::default()
    .invoke_handler(tauri::generate_handler![cmd1, cmd2])
```

### ERR-B005: Mobile crate-type missing

**Error**: `cannot produce cdylib for app_lib` or linking errors on `tauri android build` / `tauri ios build`.

**Cause**: `Cargo.toml` missing required crate types for mobile targets.

**Fix**: ALWAYS include all three crate types when targeting mobile:

```toml
[lib]
name = "app_lib"
crate-type = ["staticlib", "cdylib", "rlib"]
```

### ERR-B006: Missing mobile entry point

**Error**: App crashes immediately on mobile, or `tauri android build` / `tauri ios build` fails with missing symbol errors.

**Cause**: Missing `#[cfg_attr(mobile, tauri::mobile_entry_point)]` macro or incorrect project structure.

**Fix**: ALWAYS split into `lib.rs` + `main.rs` for mobile support:

```rust
// src-tauri/src/lib.rs
#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}

// src-tauri/src/main.rs
fn main() {
    app_lib::run();
}
```

---

## Error Lookup Table: Linux Dependencies

### ERR-B010: Missing webkit2gtk

**Error**: `Package webkit2gtk-4.1 was not found` or `error: could not find system library 'webkit2gtk-4.1'`

**Fix**: Install required system dependencies:

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y \
    libwebkit2gtk-4.1-dev \
    libappindicator3-dev \
    librsvg2-dev \
    patchelf

# Fedora
sudo dnf install webkit2gtk4.1-devel libappindicator-gtk3-devel librsvg2-devel

# Arch
sudo pacman -S webkit2gtk-4.1 libappindicator-gtk3 librsvg
```

**NEVER** install `libwebkit2gtk-4.0-dev` -- Tauri 2 requires the 4.1 variant.

### ERR-B011: Missing build tools

**Error**: `linker cc not found` or `failed to run custom build command`

**Fix**: Install base build tools:

```bash
sudo apt-get install -y build-essential curl wget file libssl-dev libgtk-3-dev \
    libayatana-appindicator3-dev
```

---

## Error Lookup Table: Bundler Errors

### ERR-B020: NSIS installer failure (Windows)

**Error**: `NSIS Error` or `MakeNSIS exited with error`

**Common causes and fixes**:
1. Path too long -- shorten `productName` or move project closer to drive root
2. Missing NSIS -- install via `choco install nsis` or `winget install NSIS.NSIS`
3. Icon format wrong -- NSIS requires `.ico` files with specific sizes

### ERR-B021: WiX/MSI failure (Windows)

**Error**: `candle.exe exited with error` or `light.exe exited with error`

**Fix**: Install WiX Toolset v3: `dotnet tool install --global wix`

### ERR-B022: DMG creation failure (macOS)

**Error**: `hdiutil: create failed` or DMG size errors

**Common causes**: Disk space insufficient, or icon file path incorrect in `tauri.conf.json`.

### ERR-B023: AppImage failure (Linux)

**Error**: `AppImage bundling failed` or missing `appimagetool`

**Fix**: Ensure `FUSE` is available. On Ubuntu 22.04+:

```bash
sudo apt-get install -y libfuse2
```

### ERR-B024: WebView2 bootstrapper (Windows)

**Error**: `Failed to download WebView2 bootstrapper`

**Fix**: Configure offline installation in `tauri.conf.json`:

```json
{
  "bundle": {
    "windows": {
      "webviewInstallMode": "offlineInstaller"
    }
  }
}
```

---

## Error Lookup Table: Code Signing

### ERR-B030: macOS unsigned app blocked

**Error**: `"MyApp" is damaged and can't be opened` or Gatekeeper rejection.

**Fix**: At minimum use ad-hoc signing for testing:

```json
{
  "bundle": {
    "macOS": {
      "signingIdentity": "-"
    }
  }
}
```

For distribution, ALWAYS use a proper Developer ID certificate.

### ERR-B031: macOS notarization failure

**Error**: `The signature of the binary is invalid` or `notarytool` errors.

**Checklist**:
1. Hardened runtime enabled: `"hardenedRuntime": true`
2. Signing identity correct: `"Developer ID Application: Name (TEAMID)"`
3. Environment variables set: `APPLE_API_ISSUER`, `APPLE_API_KEY`, `APPLE_API_KEY_PATH`
4. Certificate not expired

### ERR-B032: Windows Authenticode failure

**Error**: `SignTool Error` or `certificate thumbprint not found`

**Checklist**:
1. Certificate installed in current user store
2. Thumbprint matches: `"certificateThumbprint": "A1B2..."`
3. Timestamp URL reachable: `"timestampUrl": "http://timestamp.comodoca.com"`

---

## Error Lookup Table: CI/CD

### ERR-B040: GitHub Actions Linux build fails

**Error**: Various dependency errors in CI.

**Fix**: ALWAYS include the Linux dependency installation step:

```yaml
- name: Install Linux dependencies
  if: runner.os == 'Linux'
  run: |
    sudo apt-get update
    sudo apt-get install -y libwebkit2gtk-4.1-dev libappindicator3-dev librsvg2-dev
```

### ERR-B041: GitHub token permissions

**Error**: `Resource not accessible by integration` or `403` on release creation.

**Fix**: Set permissions in workflow:

```yaml
permissions:
  contents: write
```

And ensure repository Settings > Actions > General > Workflow permissions is set to "Read and write."

### ERR-B042: Updater artifact build fails

**Error**: `TAURI_SIGNING_PRIVATE_KEY must be set`

**Cause**: `"createUpdaterArtifacts": true` in config but no signing key.

**Fix**: Either set the environment variable in CI secrets, or set `"createUpdaterArtifacts": false` if not using auto-updater.

### ERR-B043: Cross-compilation target missing

**Error**: `error[E0463]: can't find crate for std` when building for a different architecture.

**Fix**: Install the target toolchain:

```bash
# macOS universal binary
rustup target add aarch64-apple-darwin x86_64-apple-darwin

# Android
rustup target add aarch64-linux-android armv7-linux-androideabi i686-linux-android x86_64-linux-android

# iOS
rustup target add aarch64-apple-ios x86_64-apple-ios aarch64-apple-ios-sim
```

---

## Diagnostic Decision Tree

```
Build failed?
|
+-- Is it a Rust compilation error?
|   +-- Type mismatch in command? --> Check ERR-B001, ERR-B002, ERR-B003
|   +-- Symbol/linking error? --> Check ERR-B005, ERR-B006, ERR-B043
|   +-- Commands not found at runtime? --> Check ERR-B004
|
+-- Is it a system dependency error?
|   +-- Linux? --> Check ERR-B010, ERR-B011
|   +-- Windows WebView2? --> Check ERR-B024
|
+-- Is it a bundler error?
|   +-- Windows NSIS/WiX? --> Check ERR-B020, ERR-B021
|   +-- macOS DMG? --> Check ERR-B022
|   +-- Linux AppImage? --> Check ERR-B023
|
+-- Is it a code signing error?
|   +-- macOS? --> Check ERR-B030, ERR-B031
|   +-- Windows? --> Check ERR-B032
|
+-- Is it a CI/CD error?
    +-- Linux deps? --> Check ERR-B040
    +-- Permissions? --> Check ERR-B041
    +-- Updater keys? --> Check ERR-B042
    +-- Cross-compile? --> Check ERR-B043
```

---

## General Troubleshooting Steps

1. **ALWAYS** run `cargo clean` in `src-tauri/` before retrying
2. **ALWAYS** check `tauri info` output for environment diagnostics
3. **ALWAYS** verify `tauri.conf.json` has valid JSON (use schema validation)
4. **NEVER** ignore warnings -- they often become errors in release builds
5. **NEVER** assume a build works on all platforms because it works on one

---

## Reference Links

- [references/methods.md](references/methods.md) -- Build commands, environment variables, configuration keys
- [references/examples.md](references/examples.md) -- Working build configurations and CI/CD templates
- [references/anti-patterns.md](references/anti-patterns.md) -- Build configuration mistakes with fixes

### Official Sources

- https://v2.tauri.app/start/prerequisites/
- https://v2.tauri.app/distribute/
- https://v2.tauri.app/develop/debug/
