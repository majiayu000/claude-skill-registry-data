---
name: tauri-impl-build-deploy
description: >
  Use when building for production, configuring installers, setting up code signing, or creating CI/CD pipelines.
  Prevents unsigned builds being rejected by OS gatekeepers and missing resource files in bundled installers.
  Covers tauri build command, platform bundlers (NSIS/MSI/DMG/AppImage/deb), sidecars, code signing, updater, and GitHub Actions CI/CD.
  Keywords: tauri build, deploy, NSIS, MSI, DMG, AppImage, code signing, auto-updater, CI/CD, GitHub Actions, sidecar.
license: MIT
compatibility: "Designed for Claude Code. Requires Tauri 2.x."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# tauri-impl-build-deploy

## Quick Reference

### Build Commands

| Command | Purpose |
|---------|---------|
| `tauri build` | Full production build with bundling |
| `tauri build --no-bundle` | Compile only, skip installers |
| `tauri bundle --bundles app,dmg` | Bundle specific formats only |
| `tauri bundle --config src-tauri/tauri.appstore.conf.json` | Build with alternate config |
| `tauri android build` | Android production build |
| `tauri ios build` | iOS production build |

### Platform Bundler Formats

| Platform | Formats | Notes |
|----------|---------|-------|
| **Windows** | NSIS installer, MSI (WiX), portable exe | WebView2 install mode configurable |
| **macOS** | App bundle (.app), DMG | Code signing + notarization required for distribution |
| **Linux** | AppImage, .deb, .rpm, Snap, Flatpak | AppImage is the most universal |
| **Android** | APK, AAB | Play Store requires AAB |
| **iOS** | IPA | App Store or TestFlight distribution |

### Critical Warnings

**NEVER** lose the updater private key -- it is impossible to push updates to existing installations without it. Back it up securely.

**NEVER** set `createUpdaterArtifacts: true` without setting the `TAURI_SIGNING_PRIVATE_KEY` environment variable -- the build will fail.

**NEVER** distribute unsigned macOS builds -- Gatekeeper quarantines them. Use at minimum ad-hoc signing (`"-"`).

**NEVER** use `"v1Compatible"` for `createUpdaterArtifacts` in new projects -- only for migrating from v1 updater.

**ALWAYS** commit `src-tauri/Cargo.lock` for deterministic builds across environments.

**ALWAYS** set GitHub token permissions to "Read and write" when using `tauri-action` for releases.

---

## Essential Patterns

### Pattern 1: Bundle Configuration

The `bundle` section in `tauri.conf.json` controls all packaging:

```json
{
  "bundle": {
    "active": true,
    "targets": "all",
    "icon": [
      "icons/32x32.png",
      "icons/128x128.png",
      "icons/128x128@2x.png",
      "icons/icon.icns",
      "icons/icon.ico"
    ],
    "identifier": "com.example.myapp",
    "resources": {
      "models/": "models/",
      "config.toml": "config.toml"
    },
    "externalBin": ["binaries/ffmpeg"],
    "category": "Utility",
    "copyright": "Copyright 2026 Example Inc.",
    "publisher": "Example Inc.",
    "license": "MIT",
    "createUpdaterArtifacts": true
  }
}
```

### Pattern 2: Resource Bundling and Sidecar Binaries

Resources are additional files bundled with the app. External binaries (sidecars) are executables embedded and spawnable at runtime.

```json
{
  "bundle": {
    "resources": {
      "models/": "models/",
      "config.toml": "config.toml"
    },
    "externalBin": ["binaries/ffmpeg"]
  }
}
```

Access bundled resources at runtime:

```typescript
import { resolveResource } from '@tauri-apps/api/path';
const modelPath = await resolveResource('models/default.bin');
```

### Pattern 3: Windows Code Signing (Authenticode)

**OV Certificate in tauri.conf.json:**

```json
{
  "bundle": {
    "windows": {
      "certificateThumbprint": "A1B1A2B2A3B3A4B4A5B5A6B6A7B7A8B8A9B9A0B0",
      "digestAlgorithm": "sha256",
      "timestampUrl": "http://timestamp.comodoca.com"
    }
  }
}
```

**Custom signing (Azure Key Vault):**

```json
{
  "bundle": {
    "windows": {
      "signCommand": "relic sign --file %1 --key azure --config relic.conf"
    }
  }
}
```

### Pattern 4: macOS Code Signing and Notarization

**Local signing:**

```json
{
  "bundle": {
    "macOS": {
      "signingIdentity": "Developer ID Application: Your Name (TEAMID)",
      "hardenedRuntime": true,
      "minimumSystemVersion": "10.13"
    }
  }
}
```

Or use `APPLE_SIGNING_IDENTITY` environment variable. For ad-hoc signing (testing only): set `signingIdentity` to `"-"`.

**Notarization environment variables:**

| Method | Variables |
|--------|-----------|
| App Store Connect API | `APPLE_API_ISSUER`, `APPLE_API_KEY`, `APPLE_API_KEY_PATH` |
| Apple ID | `APPLE_ID`, `APPLE_PASSWORD` (app-specific), `APPLE_TEAM_ID` |

### Pattern 5: Auto-Updater Setup

**Step 1: Install the updater plugin:**

```bash
npm run tauri add updater
cargo add tauri-plugin-updater --target 'cfg(any(target_os = "macos", windows, target_os = "linux"))'
```

**Step 2: Initialize in Rust:**

```rust
#[cfg(desktop)]
app.handle().plugin(tauri_plugin_updater::Builder::new().build());
```

**Step 3: Generate signing keys:**

```bash
npm run tauri signer generate -- -w ~/.tauri/myapp.key
```

**Step 4: Set build environment variables:**

```bash
export TAURI_SIGNING_PRIVATE_KEY="path or content"
export TAURI_SIGNING_PRIVATE_KEY_PASSWORD=""
```

**Step 5: Configure in tauri.conf.json:**

```json
{
  "bundle": {
    "createUpdaterArtifacts": true
  },
  "plugins": {
    "updater": {
      "pubkey": "dW50cnVzdGVkIGNvbW1lbnQ6...",
      "endpoints": [
        "https://releases.myapp.com/{{target}}/{{arch}}/{{current_version}}"
      ],
      "windows": {
        "installMode": "passive"
      }
    }
  }
}
```

**URL template variables:** `{{current_version}}`, `{{target}}` (linux/windows/darwin), `{{arch}}` (x86_64/i686/aarch64/armv7).

**Windows install modes:** `"passive"` (no interaction, default), `"basicUi"` (user interaction), `"quiet"` (no feedback).

### Pattern 6: Update Check (JavaScript)

```javascript
import { check } from '@tauri-apps/plugin-updater';
import { relaunch } from '@tauri-apps/plugin-process';

const update = await check();
if (update) {
  await update.downloadAndInstall((event) => {
    switch (event.event) {
      case 'Started':
        console.log(`Downloading: ${event.data.contentLength} bytes`);
        break;
      case 'Progress':
        console.log(`Downloaded: ${event.data.chunkLength}`);
        break;
      case 'Finished':
        console.log('Download complete');
        break;
    }
  });
  await relaunch();
}
```

### Pattern 7: Update Check (Rust)

```rust
use tauri_plugin_updater::UpdaterExt;

async fn update(app: tauri::AppHandle) -> tauri_plugin_updater::Result<()> {
    if let Some(update) = app.updater()?.check().await? {
        update.download_and_install(
            |chunk_length, content_length| {
                println!("Downloaded: {chunk_length}/{content_length:?}");
            },
            || println!("Finished"),
        ).await?;
        app.restart();
    }
    Ok(())
}
```

---

## CI/CD with GitHub Actions

### Cross-Platform Build Matrix

```yaml
name: Release
on:
  push:
    branches: [release]
  workflow_dispatch:

permissions:
  contents: write

jobs:
  release:
    strategy:
      fail-fast: false
      matrix:
        include:
          - platform: macos-latest
            args: --target aarch64-apple-darwin
          - platform: macos-latest
            args: --target x86_64-apple-darwin
          - platform: ubuntu-22.04
            args: ''
          - platform: ubuntu-22.04-arm
            args: ''
          - platform: windows-latest
            args: ''

    runs-on: ${{ matrix.platform }}
    steps:
      - uses: actions/checkout@v4

      - name: Install Linux dependencies
        if: runner.os == 'Linux'
        run: |
          sudo apt-get update
          sudo apt-get install -y libwebkit2gtk-4.1-dev libappindicator3-dev librsvg2-dev

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: lts/*

      - name: Install Rust stable
        uses: dtolnay/rust-toolchain@stable
        with:
          targets: ${{ matrix.platform == 'macos-latest' && 'aarch64-apple-darwin,x86_64-apple-darwin' || '' }}

      - name: Rust cache
        uses: swatinem/rust-cache@v2
        with:
          workspaces: './src-tauri -> target'

      - name: Install frontend dependencies
        run: npm install

      - name: Build Tauri app
        uses: tauri-apps/tauri-action@v0
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          tagName: app-v__VERSION__
          releaseName: 'App v__VERSION__'
          releaseBody: 'See the assets to download and install.'
          releaseDraft: true
          prerelease: false
          args: ${{ matrix.args }}
```

`__VERSION__` is auto-replaced with the version from `tauri.conf.json`.

### Windows Code Signing in CI

Required secrets: `WINDOWS_CERTIFICATE` (base64 `.pfx`), `WINDOWS_CERTIFICATE_PASSWORD`.

### macOS Code Signing in CI

Required secrets: `APPLE_CERTIFICATE` (base64 `.p12`), `APPLE_CERTIFICATE_PASSWORD`, `APPLE_SIGNING_IDENTITY`, `KEYCHAIN_PASSWORD`, `APPLE_API_ISSUER`, `APPLE_API_KEY`, `APPLE_API_KEY_PATH`.

---

## Generated Update Artifacts

| Platform | Update Artifact | Signature File |
|----------|----------------|----------------|
| Linux | `.AppImage.tar.gz` | `.AppImage.tar.gz.sig` |
| macOS | `.app.tar.gz` | `.app.tar.gz.sig` |
| Windows | `.exe` or `.msi` | `.exe.sig` or `.msi.sig` |

---

## Server Response Format (Auto-Updater)

**Static JSON (CDN/GitHub Releases):**

```json
{
  "version": "1.0.0",
  "notes": "Bug fixes and improvements",
  "pub_date": "2024-01-15T10:30:00Z",
  "platforms": {
    "linux-x86_64": {
      "signature": "...",
      "url": "https://cdn.example.com/app-1.0.0.AppImage.tar.gz"
    },
    "windows-x86_64": {
      "signature": "...",
      "url": "https://cdn.example.com/app-1.0.0-setup.exe"
    },
    "darwin-x86_64": {
      "signature": "...",
      "url": "https://cdn.example.com/app-1.0.0.app.tar.gz"
    }
  }
}
```

**Dynamic server:** Return HTTP 204 (no update) or HTTP 200 with version, url, signature, pub_date, notes.

---

## Reference Links

- [references/methods.md](references/methods.md) -- Build commands, bundler options, updater API signatures
- [references/examples.md](references/examples.md) -- Working CI/CD configs, signing setups, updater implementations
- [references/anti-patterns.md](references/anti-patterns.md) -- Build and deployment mistakes with explanations

### Official Sources

- https://v2.tauri.app/distribute/
- https://v2.tauri.app/plugin/updater/
- https://github.com/tauri-apps/tauri-action
