---
name: tauri-syntax-permissions
description: >
  Use when configuring permissions, creating capability files, setting up plugin access control, or debugging permission denied errors.
  Prevents using v1 allowlist patterns and overly permissive wildcard capabilities that compromise security.
  Covers capability file structure, permission definitions in TOML, scope configuration, plugin and custom command permissions.
  Keywords: tauri permissions, capabilities, allow, deny, scope, TOML, plugin permissions, access control, ACL.
license: MIT
compatibility: "Designed for Claude Code. Requires Tauri 2.x with Rust and TypeScript."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# tauri-syntax-permissions

> This system is NEW IN TAURI 2 — it replaces the v1 allowlist entirely. Claude frequently generates v1-style `allowlist` config which does not exist in v2.

## Quick Reference

### Permission Naming Convention

| Format | Example | Description |
|--------|---------|-------------|
| `<plugin>:default` | `fs:default` | Default safe permissions for a plugin |
| `<plugin>:allow-<command>` | `fs:allow-read-file` | Allow a specific command |
| `<plugin>:deny-<command>` | `fs:deny-write-file` | Deny a specific command |
| `<plugin>:<custom-set>` | `fs:read-files` | Custom permission set |
| `core:<module>:default` | `core:window:default` | Core module defaults |
| `core:<module>:allow-<cmd>` | `core:window:allow-set-title` | Allow specific core command |
| `allow-<command>` | `allow-greet` | Custom app command (no plugin prefix) |

### File Locations

| File | Location | Format | Purpose |
|------|----------|--------|---------|
| Capability files | `src-tauri/capabilities/*.json` | JSON or TOML | Assign permissions to windows |
| App permissions | `src-tauri/permissions/*.toml` | TOML only | Define custom command permissions |
| Generated schemas | `src-tauri/gen/schemas/` | JSON | IDE autocompletion |

### Capability File Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `$schema` | `string` | No | Path to generated schema for IDE support |
| `identifier` | `string` | Yes | Unique capability name |
| `description` | `string` | No | Purpose description |
| `windows` | `string[]` | Yes | Window labels (`"*"` for all) |
| `permissions` | `string[]` | Yes | Permission identifiers |
| `platforms` | `string[]` | No | `"linux"`, `"macOS"`, `"windows"`, `"iOS"`, `"android"` |
| `remote` | `object` | No | Remote URL access config |

---

## Critical Warnings

**NEVER** use Tauri v1 `allowlist` syntax in `tauri.conf.json` — the allowlist was completely removed in v2. Use capability files instead.

**NEVER** assume plugins have permissions by default — installing a plugin crate and npm package does NOT grant any permissions. You MUST add permissions to a capability file or commands will fail with "command not allowed".

**NEVER** use `"windows": ["*"]` with broad permissions in production — this grants every window the same access. Use specific window labels.

**NEVER** write application permission definitions in JSON format — app-level permissions in `src-tauri/permissions/` MUST be TOML. Only capability files support JSON.

**ALWAYS** add `core:default` or the specific `core:*:default` permissions your app needs — core features (window management, events, paths, menus) require explicit permissions in v2.

**ALWAYS** run `cargo build` after modifying permission/capability files — permissions are validated and compiled at build time.

---

## Essential Patterns

### Pattern 1: Minimal Capability File

```json
{
  "$schema": "../gen/schemas/desktop-schema.json",
  "identifier": "default",
  "description": "Default capabilities for the main window",
  "windows": ["main"],
  "permissions": [
    "core:default",
    "core:window:default",
    "core:app:default"
  ]
}
```

Save as `src-tauri/capabilities/default.json`. Files in the `capabilities/` directory are automatically enabled.

### Pattern 2: Plugin Permissions

```json
{
  "$schema": "../gen/schemas/desktop-schema.json",
  "identifier": "default",
  "description": "Main window with plugin access",
  "windows": ["main"],
  "permissions": [
    "core:default",
    "core:window:default",
    "core:app:default",
    "core:event:default",
    "core:path:default",
    "fs:default",
    "fs:allow-read-file",
    "dialog:default",
    "dialog:allow-open",
    "shell:default",
    "http:default",
    "notification:default",
    "clipboard-manager:allow-read",
    "clipboard-manager:allow-write"
  ]
}
```

### Pattern 3: Custom Command Permissions

Step 1 — Define the Rust command:

```rust
#[tauri::command]
fn save_document(title: String, content: String) -> Result<(), String> {
    // ... save logic
    Ok(())
}

// Register in builder:
tauri::Builder::default()
    .invoke_handler(tauri::generate_handler![save_document])
```

Step 2 — Create permission file (`src-tauri/permissions/my-commands.toml`):

```toml
[[permission]]
identifier = "allow-save-document"
description = "Allows invoking the save_document command"
commands.allow = ["save_document"]

[[permission]]
identifier = "deny-save-document"
description = "Denies the save_document command"
commands.deny = ["save_document"]
```

Step 3 — Add to capability file (`src-tauri/capabilities/default.json`):

```json
{
  "$schema": "../gen/schemas/desktop-schema.json",
  "identifier": "default",
  "windows": ["main"],
  "permissions": [
    "core:default",
    "allow-save-document"
  ]
}
```

Note: Custom app command permissions do NOT use a plugin prefix.

### Pattern 4: Scope Configuration

```toml
# src-tauri/permissions/file-access.toml

[[permission]]
identifier = "scope-documents"
description = "Access to user documents directory"

[[scope.allow]]
path = "$DOCUMENT/*"

[[scope.deny]]
path = "$DOCUMENT/.secret/*"
```

```json
{
  "permissions": [
    "fs:default",
    "fs:allow-read-file",
    "scope-documents"
  ]
}
```

### Pattern 5: Permission Sets

Bundle multiple permissions under a single identifier:

```toml
# src-tauri/permissions/document-editor.toml

[[set]]
identifier = "document-editor-full"
description = "All permissions for the document editor feature"
permissions = [
    "fs:default",
    "fs:allow-read-file",
    "fs:allow-write-file",
    "dialog:allow-open",
    "dialog:allow-save",
    "allow-save-document",
    "allow-load-document"
]
```

### Pattern 6: Platform-Specific Capabilities

```json
{
  "$schema": "../gen/schemas/desktop-schema.json",
  "identifier": "desktop-only",
  "windows": ["main"],
  "platforms": ["linux", "macOS", "windows"],
  "permissions": [
    "global-shortcut:allow-register",
    "global-shortcut:allow-unregister"
  ]
}
```

```json
{
  "$schema": "../gen/schemas/mobile-schema.json",
  "identifier": "mobile-only",
  "windows": ["main"],
  "platforms": ["iOS", "android"],
  "permissions": [
    "nfc:allow-scan",
    "biometric:allow-authenticate",
    "barcode-scanner:allow-scan"
  ]
}
```

### Pattern 7: Remote API Access

```json
{
  "$schema": "../gen/schemas/remote-schema.json",
  "identifier": "remote-capability",
  "windows": ["main"],
  "remote": {
    "urls": ["https://*.example.com"]
  },
  "platforms": ["iOS", "android"],
  "permissions": [
    "nfc:allow-scan",
    "barcode-scanner:allow-scan"
  ]
}
```

---

## Common Plugin Permission Identifiers

| Plugin | Default | Common Allow | Common Deny |
|--------|---------|-------------|-------------|
| `fs` | `fs:default` | `fs:allow-read-file`, `fs:allow-write-file`, `fs:allow-mkdir` | `fs:deny-write-file` |
| `dialog` | `dialog:default` | `dialog:allow-open`, `dialog:allow-save`, `dialog:allow-message` | — |
| `shell` | `shell:default` | `shell:allow-open`, `shell:allow-execute` | — |
| `http` | `http:default` | `http:allow-fetch` | — |
| `notification` | `notification:default` | `notification:allow-notify` | — |
| `clipboard-manager` | — | `clipboard-manager:allow-read`, `clipboard-manager:allow-write` | — |
| `process` | — | `process:allow-restart`, `process:allow-exit` | — |
| `updater` | `updater:default` | `updater:allow-check`, `updater:allow-download-and-install` | — |
| `os` | `os:default` | `os:allow-platform` | — |
| `global-shortcut` | — | `global-shortcut:allow-register` | — |

### Core Module Permissions

| Module | Default | Example Allow |
|--------|---------|---------------|
| `core:app` | `core:app:default` | `core:app:allow-version` |
| `core:window` | `core:window:default` | `core:window:allow-set-title`, `core:window:allow-close` |
| `core:event` | `core:event:default` | `core:event:allow-listen`, `core:event:allow-emit` |
| `core:path` | `core:path:default` | `core:path:allow-resolve` |
| `core:menu` | `core:menu:default` | — |
| `core:tray` | `core:tray:default` | — |
| `core:resources` | `core:resources:default` | — |

---

## Window Merging Behavior

When a window appears in multiple capability files, all permissions from all capabilities are merged additively. There is no override or conflict resolution — permissions accumulate.

---

## Schema Generation

Tauri generates JSON schemas in `src-tauri/gen/schemas/`:
- `desktop-schema.json`
- `mobile-schema.json`
- `remote-schema.json`

Reference via `$schema` for IDE autocompletion. These schemas are regenerated on build.

---

## Inline Capabilities in tauri.conf.json

Capabilities can also be defined inline (less common):

```json
{
  "app": {
    "security": {
      "capabilities": [
        {
          "identifier": "inline-capability",
          "windows": ["*"],
          "permissions": ["fs:default"]
        },
        "my-external-capability"
      ]
    }
  }
}
```

---

## Reference Links

- [references/methods.md](references/methods.md) — Complete permission and capability format reference
- [references/examples.md](references/examples.md) — Complete capability file examples for common scenarios
- [references/anti-patterns.md](references/anti-patterns.md) — What NOT to do, with WHY explanations

### Official Sources

- https://v2.tauri.app/security/permissions/
- https://v2.tauri.app/security/capabilities/
- https://v2.tauri.app/develop/plugins/
