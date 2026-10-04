---
name: tauri-impl-security
description: >
  Use when hardening Tauri 2 app security, configuring CSP, reviewing permissions, or implementing isolation patterns.
  Prevents overly permissive CSP, disabled prototype freeze, and unscoped file/shell/http permissions in production.
  Covers CSP configuration, Tauri protocols, freezePrototype, isolation pattern, scope-based access control, and dangerous permissions.
  Keywords: tauri security, CSP, Content Security Policy, freezePrototype, isolation pattern, scope, permissions audit.
license: MIT
compatibility: "Designed for Claude Code. Requires Tauri 2.x."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# tauri-impl-security

## Quick Reference

### Security Architecture (Tauri 2)

| Layer | Mechanism | Configuration |
|-------|-----------|---------------|
| **Content Security Policy** | Restricts resource loading in webview | `app.security.csp` in tauri.conf.json |
| **Permissions** | Define which IPC commands are allowed/denied | `src-tauri/permissions/*.toml` |
| **Capabilities** | Bind permissions to specific windows | `src-tauri/capabilities/*.json` |
| **Scopes** | Restrict what data commands can access | Within permission definitions |
| **Isolation Pattern** | Separate IPC from frontend context | `app.security.pattern` |
| **Prototype Freeze** | Prevent prototype pollution | `app.security.freezePrototype` |

### Tauri-Specific Protocols

| Protocol | Purpose | CSP Directive |
|----------|---------|---------------|
| `tauri:` | Internal protocol for serving frontend assets | `default-src` |
| `asset:` / `https://asset.localhost` | Access bundled resources and filesystem assets | `img-src`, `media-src` |
| `ipc:` / `http://ipc.localhost` | IPC communication between frontend and Rust | `connect-src` |

### Critical Warnings

**NEVER** set `csp` to `null` in production -- this disables all content security restrictions, exposing the app to XSS and injection attacks.

**NEVER** use `"windows": ["*"]` with broad permissions -- this grants all windows identical access. ALWAYS use specific window labels.

**NEVER** set `dangerousDisableAssetCspModification: true` unless you fully understand that it removes automatic CSP nonce injection for asset loading.

**NEVER** grant `shell:default` without scope restrictions -- this allows arbitrary command execution. ALWAYS define explicit command scopes.

**ALWAYS** enable `freezePrototype: true` in production -- it prevents JavaScript prototype pollution attacks.

**ALWAYS** add capabilities for every plugin you install -- plugins do NOT automatically receive permissions.

**ALWAYS** define deny rules for sensitive paths (e.g., `$HOME/.ssh/*`) when granting filesystem access.

---

## Essential Patterns

### Pattern 1: Content Security Policy Configuration

```json
{
  "app": {
    "security": {
      "csp": "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' asset: https://asset.localhost data:; font-src 'self' data:; connect-src ipc: http://ipc.localhost https://api.example.com; media-src 'self' asset: https://asset.localhost"
    }
  }
}
```

**Common CSP directives for Tauri:**

| Directive | Recommended Value | Purpose |
|-----------|-------------------|---------|
| `default-src` | `'self'` | Fallback for all resource types |
| `script-src` | `'self'` | JavaScript sources |
| `style-src` | `'self' 'unsafe-inline'` | Stylesheets (inline needed for most frameworks) |
| `img-src` | `'self' asset: https://asset.localhost data:` | Image sources including asset protocol |
| `font-src` | `'self' data:` | Font files |
| `connect-src` | `ipc: http://ipc.localhost` | IPC + any external APIs |
| `media-src` | `'self' asset: https://asset.localhost` | Audio/video sources |

### Pattern 2: Security Settings Block

```json
{
  "app": {
    "security": {
      "csp": "default-src 'self'; script-src 'self'",
      "freezePrototype": true,
      "dangerousDisableAssetCspModification": false,
      "assetProtocol": {
        "enable": true,
        "scope": ["$APPDATA/**", "$RESOURCE/**"]
      },
      "pattern": {
        "use": "brownfield"
      }
    }
  }
}
```

| Property | Description |
|----------|-------------|
| `freezePrototype` | Freezes `Object.prototype` to prevent pollution attacks |
| `dangerousDisableAssetCspModification` | Disables automatic CSP nonce injection for the asset protocol |
| `assetProtocol.enable` | Enable the `asset:` protocol for file access |
| `assetProtocol.scope` | Glob patterns defining allowed asset paths |
| `pattern.use` | `"brownfield"` (default) or `"isolation"` |

### Pattern 3: Permissions System

Permissions follow the naming convention:
- `<plugin>:default` -- Default permission set
- `<plugin>:allow-<command>` -- Allow a specific command
- `<plugin>:deny-<command>` -- Deny a specific command

**Defining custom permissions** (`src-tauri/permissions/my-commands.toml`):

```toml
[[permission]]
identifier = "allow-read-file"
description = "Enables the read_file command"
commands.allow = ["read_file"]

[[permission]]
identifier = "deny-write-file"
description = "Blocks the write_file command"
commands.deny = ["write_file"]
```

**Permission with scopes:**

```toml
[[permission]]
identifier = "scope-home"
description = "Access to files in $HOME but not .ssh"

[[scope.allow]]
path = "$HOME/*"

[[scope.deny]]
path = "$HOME/.ssh/*"
```

**Permission sets (bundle multiple):**

```toml
[[set]]
identifier = "allow-home-read-extended"
description = "Read access + directory creation in $HOME"
permissions = [
    "fs:read-files",
    "fs:scope-home",
    "fs:allow-mkdir"
]
```

### Pattern 4: Capabilities System

Capabilities tie permissions to specific windows. Files in `src-tauri/capabilities/` are automatically enabled.

```json
{
  "$schema": "../gen/schemas/desktop-schema.json",
  "identifier": "main-capability",
  "description": "Capability for the main window",
  "windows": ["main"],
  "permissions": [
    "core:path:default",
    "core:event:default",
    "core:window:default",
    "core:app:default",
    "core:resources:default",
    "core:menu:default",
    "core:tray:default"
  ]
}
```

**Platform-specific capabilities:**

```json
{
  "$schema": "../gen/schemas/desktop-schema.json",
  "identifier": "desktop-capability",
  "windows": ["main"],
  "platforms": ["linux", "macOS", "windows"],
  "permissions": ["global-shortcut:allow-register"]
}
```

**Remote URL access:**

```json
{
  "$schema": "../gen/schemas/remote-schema.json",
  "identifier": "remote-capability",
  "windows": ["main"],
  "remote": {
    "urls": ["https://*.tauri.app"]
  },
  "permissions": ["nfc:allow-scan"]
}
```

### Pattern 5: Scope-Based Access Control

**File system scopes:**

```json
{
  "permissions": [
    {
      "identifier": "fs:allow-read-file",
      "allow": [{ "path": "$APPDATA/**" }],
      "deny": [{ "path": "$APPDATA/secrets/**" }]
    }
  ]
}
```

**HTTP URL scopes:**

```json
{
  "permissions": [
    {
      "identifier": "http:default",
      "allow": [{ "url": "https://api.example.com/*" }],
      "deny": [{ "url": "https://api.example.com/admin/*" }]
    }
  ]
}
```

**Shell command scopes:**

```json
{
  "permissions": [
    {
      "identifier": "shell:allow-execute",
      "allow": [{
        "name": "exec-sh",
        "cmd": "sh",
        "args": ["-c", { "validator": "\\S+" }],
        "sidecar": false
      }]
    }
  ]
}
```

### Pattern 6: Accessing Scopes in Rust Commands

```rust
use tauri::ipc::{CommandScope, GlobalScope};

#[tauri::command]
async fn scoped_command<R: tauri::Runtime>(
    command_scope: CommandScope<'_, ScopeEntry>,
    global_scope: GlobalScope<'_, ScopeEntry>,
) -> Result<(), String> {
    let allowed = command_scope.allows();
    let denied = command_scope.denies();
    // Validate access against scopes
    Ok(())
}
```

---

## Windows URL Scheme Change (v2)

On Windows, production frontend files load from `http://tauri.localhost` instead of `https://tauri.localhost`. This resets IndexedDB, LocalStorage, and Cookies unless:
- `dangerousUseHttpScheme` was enabled in v1
- `app.windows[].useHttpsScheme` is set to `true` in v2

---

## Dangerous Permissions Audit Checklist

Review these permissions carefully before granting:

| Permission | Risk | Mitigation |
|------------|------|------------|
| `shell:allow-execute` | Arbitrary command execution | Define explicit command scopes with validators |
| `fs:allow-write-file` with broad scope | Data destruction/exfiltration | Restrict to `$APPDATA` or specific directories |
| `http:default` without URL scope | Unrestricted network access | Define allowed URL patterns |
| `clipboard-manager:allow-read-text` | Read sensitive clipboard data | Only grant when functionally required |
| `"windows": ["*"]` | All windows get same permissions | Use specific window labels |
| `dangerousDisableAssetCspModification` | Removes CSP nonce protection | Almost never needed |

---

## Isolation Pattern

The isolation pattern creates a separate execution context for the IPC bridge, preventing the frontend from directly accessing Tauri internals:

```json
{
  "app": {
    "security": {
      "pattern": {
        "use": "isolation",
        "options": {
          "dir": "../isolation-app"
        }
      }
    }
  }
}
```

Use `"brownfield"` (default) for standard apps. Use `"isolation"` for apps loading untrusted third-party content.

---

## Core Permissions (Built-in)

These require no plugin installation but still need explicit capability grants:

```
core:path:default
core:event:default
core:window:default
core:app:default
core:resources:default
core:menu:default
core:tray:default
core:window:allow-set-title
core:window:allow-close
core:window:allow-minimize
core:window:allow-maximize
```

---

## Reference Links

- [references/methods.md](references/methods.md) -- Security configuration properties, permission formats, scope syntax
- [references/examples.md](references/examples.md) -- Complete security configurations, capability files, permission definitions
- [references/anti-patterns.md](references/anti-patterns.md) -- Security mistakes with risk explanations

### Official Sources

- https://v2.tauri.app/security/
- https://v2.tauri.app/security/capabilities/
- https://v2.tauri.app/security/permissions/
