---
name: tauri-core-config
description: >
  Use when editing tauri.conf.json, configuring build options, or setting up platform-specific bundle configuration.
  Prevents invalid configuration keys and v1 config patterns that silently fail in Tauri 2.
  Covers build settings, app settings, window configuration, bundle options, plugin configuration, and security settings.
  Keywords: tauri.conf.json, configuration, build settings, bundle options, window config, security settings.
license: MIT
compatibility: "Designed for Claude Code. Requires Tauri 2.x with Rust and TypeScript."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# tauri-core-config

## Quick Reference

### Configuration File Location

The main configuration file lives at `src-tauri/tauri.conf.json`. Tauri auto-generates JSON schemas in `src-tauri/gen/schemas/` for IDE autocompletion.

### Top-Level Keys

| Key | Type | Required | Description |
|-----|------|----------|-------------|
| `$schema` | `string` | No | Path to JSON schema for IDE validation |
| `identifier` | `string` | **Yes** | Reverse domain notation (e.g., `com.example.myapp`) |
| `productName` | `string \| null` | No | Display name of the application |
| `version` | `string \| null` | No | Semver version or path to `package.json` |
| `mainBinaryName` | `string \| null` | No | Override the compiled binary filename |
| `build` | `object` | No | Build configuration |
| `app` | `object` | No | Application runtime configuration |
| `bundle` | `object` | No | Bundling and distribution configuration |
| `plugins` | `object` | No | Per-plugin configuration (default: `{}`) |

### Schema Reference

ALWAYS include the `$schema` key for IDE autocompletion and validation:

```json
{
    "$schema": "./gen/schemas/desktop-schema.json"
}
```

Available schemas (auto-generated in `src-tauri/gen/schemas/`):
- `desktop-schema.json` -- desktop platform configuration
- `mobile-schema.json` -- mobile platform configuration
- `remote-schema.json` -- remote URL capabilities

### Critical Warnings

**NEVER** omit the `identifier` field -- it is the ONLY required field. It MUST be unique reverse-domain notation (`com.example.myapp`). Using a non-unique identifier causes conflicts with other apps on the system.

**NEVER** use `build.devUrl` without `build.beforeDevCommand` -- the dev server will not start automatically, causing Tauri to connect to nothing.

**NEVER** omit `build.beforeBuildCommand` -- frontend assets will not be compiled before bundling, producing an app with missing or stale UI.

**NEVER** set `app.security.csp` to `null` in production -- this disables all Content Security Policy restrictions, leaving the app vulnerable to XSS attacks.

**NEVER** set `app.security.dangerousDisableAssetCspModification` to `true` unless you fully understand CSP nonce injection.

**NEVER** edit files in `gen/schemas/` -- they are auto-generated and will be overwritten on the next build.

---

## Build Section

The `build` section controls how the frontend is compiled and served during development and production.

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `devUrl` | `string \| null` | `null` | Dev server URL (e.g., `http://localhost:5173`) |
| `frontendDist` | `string \| array` | -- | Path to compiled frontend assets (e.g., `../dist`) |
| `beforeDevCommand` | `string \| object` | -- | Shell command before `tauri dev` |
| `beforeBuildCommand` | `string \| object` | -- | Shell command before `tauri build` |
| `beforeBundleCommand` | `string \| object` | -- | Shell command before the bundling phase |
| `features` | `string[] \| null` | `null` | Cargo feature flags to enable |
| `additionalWatchFolders` | `string[]` | `[]` | Extra paths to watch during `tauri dev` |
| `removeUnusedCommands` | `boolean` | `false` | Remove unused commands during build based on ACL config |

### Command Object Form

`beforeDevCommand`, `beforeBuildCommand`, and `beforeBundleCommand` support an object form:

```json
{
    "beforeDevCommand": {
        "script": "npm run dev",
        "cwd": "../frontend",
        "wait": false
    }
}
```

| Property | Type | Description |
|----------|------|-------------|
| `script` | `string` | The shell command to run |
| `cwd` | `string` | Working directory (relative to project root) |
| `wait` | `boolean` | Wait for the command to finish before continuing |

### Build Rules

- **ALWAYS** pair `devUrl` with `beforeDevCommand` -- the dev server must be running before Tauri connects
- **ALWAYS** set `frontendDist` to the output directory of your frontend build tool
- **ALWAYS** set `beforeBuildCommand` to compile frontend assets for production
- `frontendDist` is relative to `src-tauri/`, so `../dist` points to `project-root/dist`

---

## App Section

The `app` section configures runtime behavior including windows, security, and platform-specific features.

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `windows` | `WindowConfig[]` | `[]` | Windows created at startup |
| `security` | `object` | -- | Security settings |
| `trayIcon` | `TrayIconConfig \| null` | `null` | System tray icon configuration |
| `withGlobalTauri` | `boolean` | `false` | Inject Tauri API on `window.__TAURI__` |
| `enableGTKAppId` | `boolean` | `false` | Set identifier as GTK app ID (Linux) |
| `macOSPrivateApi` | `boolean` | `false` | Enable transparent background + fullscreen (macOS) |

### Window Configuration (`app.windows[]`)

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `label` | `string` | `"main"` | Unique window identifier |
| `title` | `string` | -- | Window title bar text |
| `url` | `string` | `"/"` | URL or path to load |
| `width` | `number` | -- | Width in logical pixels |
| `height` | `number` | -- | Height in logical pixels |
| `x` / `y` | `number` | -- | Window position |
| `minWidth` / `minHeight` | `number` | -- | Minimum dimensions |
| `maxWidth` / `maxHeight` | `number` | -- | Maximum dimensions |
| `resizable` | `boolean` | `true` | Allow resizing |
| `fullscreen` | `boolean` | `false` | Start fullscreen |
| `focus` | `boolean` | `true` | Focus on creation |
| `create` | `boolean` | `true` | Create at startup |
| `transparent` | `boolean` | `false` | Enable window transparency |
| `decorations` | `boolean` | `true` | Show title bar / borders |
| `alwaysOnTop` | `boolean` | `false` | Stay above other windows |

#### Window Rules

- **ALWAYS** set a unique `label` for each window -- labels are used for IPC targeting and window lookup
- Set `create: false` for windows you want to create programmatically from Rust
- The `url` property accepts relative paths (`/settings.html`) or custom protocol URLs
- Use `minWidth`/`minHeight` to prevent the window from being resized too small

### Security Section (`app.security`)

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `csp` | `string \| object \| null` | `null` | Content Security Policy |
| `capabilities` | `string[]` | `[]` | Explicit capability file paths (overrides auto-discovery) |
| `freezePrototype` | `boolean` | `false` | Freeze JavaScript Object.prototype |
| `dangerousDisableAssetCspModification` | `boolean \| string[]` | `false` | Disable automatic CSP nonce injection |
| `assetProtocol.enable` | `boolean` | `false` | Enable the asset:// protocol |
| `assetProtocol.scope` | `string[]` | `[]` | Allowed paths for asset:// |
| `pattern.use` | `string` | `"brownfield"` | Application pattern (`"brownfield"` or `"isolation"`) |

#### Security Rules

- **ALWAYS** enable `freezePrototype` in production -- it prevents prototype pollution attacks
- **ALWAYS** define a restrictive CSP in production -- never leave it as `null`
- Use the `isolation` pattern for maximum security (adds an isolation layer between frontend and IPC)
- When specifying `capabilities` explicitly, auto-discovery of `src-tauri/capabilities/` is disabled

---

## Bundle Section

The `bundle` section controls application packaging and distribution.

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `active` | `boolean` | `true` | Enable/disable bundling |
| `targets` | `string \| string[]` | `"all"` | Target platforms/formats |
| `icon` | `string[]` | -- | Icon file paths (all required sizes) |
| `resources` | `object` | `{}` | Additional files/directories to bundle |
| `externalBin` | `string[]` | `[]` | External binaries to embed as sidecars |
| `fileAssociations` | `array` | `[]` | File type associations |
| `category` | `string` | -- | App category (e.g., `"Utility"`) |
| `copyright` | `string` | -- | Copyright notice |
| `publisher` | `string` | -- | Publisher name |
| `license` | `string` | -- | SPDX license identifier |
| `licenseFile` | `string` | -- | Path to license file |
| `createUpdaterArtifacts` | `boolean \| "v1Compatible"` | `false` | Generate update signatures |

### Required Icon Sizes

ALWAYS include all required icon formats:

```json
{
    "icon": [
        "icons/32x32.png",
        "icons/128x128.png",
        "icons/128x128@2x.png",
        "icons/icon.icns",
        "icons/icon.ico"
    ]
}
```

Use `tauri icon` CLI command to generate all sizes from a single source image.

### Platform-Specific Bundle Configuration

#### Windows (`bundle.windows`)

| Property | Type | Description |
|----------|------|-------------|
| `nsis` | `object` | NSIS installer configuration |
| `wix` | `object` | WiX (MSI) configuration |
| `webviewInstallMode` | `string` | `"downloadBootstrapper"` or `"offlineInstallerFromUrl"` |
| `signCommand` | `string` | Custom signing command (`%1` = file path) |
| `certificateThumbprint` | `string \| null` | Certificate thumbprint for Authenticode |
| `digestAlgorithm` | `string` | Hash algorithm (typically `"sha256"`) |
| `timestampUrl` | `string` | Timestamp server URL |
| `allowDowngrades` | `boolean` | Permit version downgrades |

#### macOS (`bundle.macOS`)

| Property | Type | Description |
|----------|------|-------------|
| `dmg` | `object` | DMG configuration (window size, positions) |
| `hardenedRuntime` | `boolean` | Enable hardened runtime (default: `true`) |
| `minimumSystemVersion` | `string` | Minimum macOS version (default: `"10.13"`) |
| `signingIdentity` | `string \| null` | Code signing identity |

#### Linux (`bundle.linux`)

| Property | Type | Description |
|----------|------|-------------|
| `deb` | `object` | Debian package config |
| `rpm` | `object` | RPM package config |
| `appimage` | `object` | AppImage config |
| `appimage.bundleMediaFramework` | `boolean` | Bundle media framework (default: `false`) |

#### iOS (`bundle.iOS`)

| Property | Type | Description |
|----------|------|-------------|
| `minimumSystemVersion` | `string` | Default: `"14.0"` |

#### Android (`bundle.android`)

| Property | Type | Description |
|----------|------|-------------|
| `minSdkVersion` | `number` | Default: `24` |
| `versionCode` | `number` | Auto-calculated from semver |
| `autoIncrementVersionCode` | `boolean` | Increment on each build |

### Updater Rules

- **ALWAYS** set `TAURI_SIGNING_PRIVATE_KEY` environment variable before enabling `createUpdaterArtifacts`
- Use `true` for new projects, `"v1Compatible"` ONLY when migrating from Tauri v1 updater
- **NEVER** lose the updater private key -- it makes pushing updates to existing installations impossible

---

## Plugins Section

The `plugins` section provides per-plugin configuration as key-value pairs:

```json
{
    "plugins": {
        "fs": {
            "scope": {
                "allow": ["$APPDATA/**", "$HOME/Documents/**"],
                "deny": ["$HOME/.ssh/**"]
            }
        },
        "http": {
            "scope": {
                "allow": ["https://api.example.com/*"]
            }
        }
    }
}
```

Plugin configuration keys match the plugin name without the `tauri-plugin-` prefix.

---

## Minimal Viable Config

The absolute minimum `tauri.conf.json` that works:

```json
{
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

---

## Reference Links

- [references/methods.md](references/methods.md) -- Complete tauri.conf.json schema reference with all properties
- [references/examples.md](references/examples.md) -- Config examples: minimal, full, platform-specific
- [references/anti-patterns.md](references/anti-patterns.md) -- Common config mistakes and how to avoid them

### Official Sources

- https://v2.tauri.app/reference/config/
- https://v2.tauri.app/develop/configuration/
- https://v2.tauri.app/distribute/
