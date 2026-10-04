---
name: tauri-errors-permissions
description: >
  Use when encountering permission denied errors, CSP violations, or capability configuration issues in Tauri 2.
  Prevents confusing core permissions with plugin permissions and missing scope restrictions on sensitive plugins.
  Covers capability misconfiguration, missing plugin permissions, scope violations, CSP violations, and debugging workflows.
  Keywords: tauri permission error, permission denied, CSP violation, capability, scope violation, plugin permissions.
license: MIT
compatibility: "Designed for Claude Code. Requires Tauri 2.x."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# tauri-errors-permissions

## Diagnostic Decision Tree

```
Permission-related error in Tauri 2
|
+-- Error: "command <name> not allowed"
|   |
|   +-- Plugin command (e.g., fs, http, dialog)?
|   |   --> Section 1: Missing Plugin Permissions
|   |
|   +-- Custom #[tauri::command]?
|   |   --> Section 2: Custom Command Permissions
|   |
|   +-- Core feature (window, event, path, menu, tray)?
|       --> Section 3: Core Permissions
|
+-- Error: CSP violation (console shows "Refused to ...")
|   --> Section 4: CSP Violations
|
+-- Error: scope violation / path access denied
|   --> Section 5: Scope Violations
|
+-- No error but feature silently does nothing
|   --> Section 6: Silent Permission Failures
|
+-- Build error related to permissions / capabilities
|   --> Section 7: Configuration Format Errors
```

---

## Section 1: Missing Plugin Permissions

### Symptoms

- Runtime error: `command <plugin>|<command> not allowed`
- Plugin API call throws immediately after `invoke()`
- Works in dev but fails in production (or vice versa)

### Debugging Workflow

**Step 1.1**: Verify the plugin is registered in Rust (`src-tauri/src/lib.rs`):
```rust
tauri::Builder::default()
    .plugin(tauri_plugin_fs::init())       // REQUIRED for each plugin
    .plugin(tauri_plugin_dialog::init())
    .plugin(tauri_plugin_http::init())
```

**Step 1.2**: Verify permissions exist in a capability file. Check `src-tauri/capabilities/default.json`:
```json
{
  "$schema": "../gen/schemas/desktop-schema.json",
  "identifier": "default",
  "windows": ["main"],
  "permissions": [
    "core:default",
    "fs:default",
    "dialog:default",
    "http:default"
  ]
}
```

**Step 1.3**: Verify the specific command is covered. `<plugin>:default` grants a safe subset. Some commands require explicit permission:

| Plugin | Commands NOT in `:default` | Required Permission |
|--------|---------------------------|-------------------|
| `fs` | write operations | `fs:allow-write-file`, `fs:allow-mkdir`, `fs:allow-remove` |
| `shell` | execute, spawn | `shell:allow-execute`, `shell:allow-spawn` |
| `clipboard-manager` | all operations | `clipboard-manager:allow-read-text`, `clipboard-manager:allow-write-text` |
| `http` | requests to URLs | Requires URL scope configuration |
| `notification` | request-permission | `notification:allow-request-permission` |

**Step 1.4**: Verify the `windows` array includes the window making the call:
```json
{
  "windows": ["main"],
  "permissions": ["fs:default"]
}
```
If the calling window label is `"settings"` but the capability only lists `"main"`, the permission is denied.

### Permission Naming Convention

```
<plugin-name>:default              -- Safe default set
<plugin-name>:allow-<command>      -- Allow specific command
<plugin-name>:deny-<command>       -- Deny specific command (overrides allow)
<plugin-name>:<custom-set>         -- Custom permission set
```

---

## Section 2: Custom Command Permissions

### Symptoms

- Custom `#[tauri::command]` returns "not allowed"
- Command works without any capability files (in early development) but fails after adding capabilities

### Debugging Workflow

**Step 2.1**: Create a permission file in `src-tauri/permissions/` (TOML format ONLY):
```toml
# src-tauri/permissions/commands.toml
[[permission]]
identifier = "allow-my-command"
description = "Allow the my_command function"
commands.allow = ["my_command"]
```

**Step 2.2**: Reference the permission in a capability file (NO plugin prefix):
```json
{
  "$schema": "../gen/schemas/desktop-schema.json",
  "identifier": "default",
  "windows": ["main"],
  "permissions": [
    "core:default",
    "allow-my-command"
  ]
}
```

**Step 2.3**: Verify the command name in the permission file matches the Rust function name exactly (snake_case):
```rust
#[tauri::command]
fn get_user_data() { }
// Permission must reference: "get_user_data"
```

### Critical Rules

**ALWAYS** use TOML format for application permission files. JSON is only valid for plugin permissions.

**NEVER** add a plugin prefix to custom command permissions. Custom commands use bare identifiers like `"allow-my-command"`, NOT `"app:allow-my-command"`.

---

## Section 3: Core Permissions

### Symptoms

- Window management operations fail silently or throw errors
- Event system calls fail
- Path resolution functions fail

### Core Permission Reference

Core features require explicit permissions in v2. These are NOT granted automatically:

```json
{
  "permissions": [
    "core:default",
    "core:window:default",
    "core:window:allow-set-title",
    "core:window:allow-close",
    "core:window:allow-minimize",
    "core:window:allow-maximize",
    "core:event:default",
    "core:path:default",
    "core:app:default",
    "core:resources:default",
    "core:menu:default",
    "core:tray:default"
  ]
}
```

**ALWAYS** include `core:default` as a minimum. It covers basic app functionality. Add specific `core:<feature>:default` or `core:<feature>:allow-<action>` as needed.

**NEVER** assume core features work without permissions. Unlike Tauri v1 which had an allowlist, v2 denies everything not explicitly permitted.

---

## Section 4: CSP Violations

### Symptoms

- Browser console: `Refused to load the script ...`
- Browser console: `Refused to connect to ...`
- Browser console: `Refused to load the image ...`
- External API calls fail, images do not load, scripts blocked

### Debugging Workflow

**Step 4.1**: Check the CSP in `src-tauri/tauri.conf.json`:
```json
{
  "app": {
    "security": {
      "csp": "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' asset: https://asset.localhost; connect-src ipc: http://ipc.localhost"
    }
  }
}
```

**Step 4.2**: Map the console error to the correct CSP directive:

| Error Message Contains | CSP Directive to Modify | Example Addition |
|----------------------|------------------------|------------------|
| "Refused to load the script" | `script-src` | `script-src 'self'` |
| "Refused to connect to" | `connect-src` | `connect-src ipc: http://ipc.localhost https://api.example.com` |
| "Refused to load the image" | `img-src` | `img-src 'self' asset: https://asset.localhost data:` |
| "Refused to load the font" | `font-src` | `font-src 'self' data:` |
| "Refused to load the stylesheet" | `style-src` | `style-src 'self' 'unsafe-inline'` |
| "Refused to load media" | `media-src` | `media-src 'self' asset: https://asset.localhost` |

**Step 4.3**: Verify Tauri-specific protocols are included:

| Protocol | Purpose | Required In |
|----------|---------|-------------|
| `ipc:` / `http://ipc.localhost` | IPC communication | `connect-src` (ALWAYS required) |
| `asset:` / `https://asset.localhost` | Bundled assets | `img-src`, `media-src` |
| `'self'` | App's own origin | `default-src` (ALWAYS required) |

**Step 4.4**: Common working CSP for most Tauri apps:
```
default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' asset: https://asset.localhost data:; font-src 'self' data:; connect-src ipc: http://ipc.localhost
```

### Critical Rules

**NEVER** set CSP to `null` in production. This disables all content security restrictions.

**NEVER** use `dangerousDisableAssetCspModification: true` unless you fully understand the implications.

**ALWAYS** include `ipc:` and `http://ipc.localhost` in `connect-src`. Without this, IPC communication fails entirely.

**ALWAYS** enable `freezePrototype: true` in production to prevent prototype pollution attacks:
```json
{
  "app": {
    "security": {
      "freezePrototype": true
    }
  }
}
```

---

## Section 5: Scope Violations

### Symptoms

- File operations fail even with `fs:allow-read-file`
- HTTP requests fail even with `http:default`
- Error mentions "scope" or path is outside allowed scope

### Debugging Workflow

**Step 5.1**: Check if the permission has scope restrictions. Add explicit scopes to capability permissions:

```json
{
  "permissions": [
    {
      "identifier": "fs:allow-read-file",
      "allow": [{ "path": "$APPDATA/**" }, { "path": "$RESOURCE/**" }],
      "deny": [{ "path": "$APPDATA/secrets/**" }]
    },
    {
      "identifier": "http:default",
      "allow": [{ "url": "https://api.example.com/*" }],
      "deny": [{ "url": "https://api.example.com/admin/*" }]
    }
  ]
}
```

**Step 5.2**: Verify path variables resolve correctly:

| Variable | Resolves To |
|----------|-------------|
| `$APPDATA` | App-specific data directory |
| `$APPCONFIG` | App-specific config directory |
| `$APPLOCALDATA` | App-specific local data |
| `$APPCACHE` | App-specific cache |
| `$APPLOG` | App-specific log directory |
| `$RESOURCE` | Bundled resource directory |
| `$HOME` | User home directory |
| `$DESKTOP` | Desktop directory |
| `$DOCUMENT` | Documents directory |
| `$DOWNLOAD` | Downloads directory |

**Step 5.3**: Remember that deny rules ALWAYS take precedence over allow rules. If both match, the operation is denied.

**Step 5.4**: For filesystem operations, verify paths are relative to a `BaseDirectory` in the frontend code:
```typescript
// WRONG: absolute path, will fail scope check
await readTextFile('/etc/passwd');

// CORRECT: relative to base directory
await readTextFile('config.json', { baseDir: BaseDirectory.AppConfig });
```

---

## Section 6: Silent Permission Failures

### Symptoms

- No error thrown, but feature does not work
- Events are not received
- Window operations have no visible effect

### Debugging Steps

**Step 6.1**: Check the Rust-side console/logs for permission warnings. Tauri may log permission denials without propagating them to the frontend.

**Step 6.2**: Verify the window label matches. If a capability targets `"main"` but the active window is `"settings"`, permissions do not apply:
```json
{
  "windows": ["main", "settings"],
  "permissions": ["core:event:default"]
}
```

**Step 6.3**: Verify capability files are in the correct location. Files in `src-tauri/capabilities/` are auto-loaded. Files elsewhere are ignored.

**Step 6.4**: Check for conflicting capabilities. Multiple capabilities for the same window are merged additively. There is no override -- permissions accumulate.

---

## Section 7: Configuration Format Errors

### Symptoms

- Build errors mentioning capability or permission parsing
- `cargo build` fails with schema validation errors
- Permission identifiers not recognized

### Debugging Steps

**Step 7.1**: Verify file format rules:

| File Type | Location | Format | Extension |
|-----------|----------|--------|-----------|
| Capability files | `src-tauri/capabilities/` | JSON or TOML | `.json` or `.toml` |
| App permission files | `src-tauri/permissions/` | TOML only | `.toml` |
| Plugin permission files | Inside plugin crate | JSON or TOML | `.json` or `.toml` |

**Step 7.2**: Verify the `$schema` reference points to the correct generated schema:
```json
{
  "$schema": "../gen/schemas/desktop-schema.json"
}
```
Run `cargo build` once to generate schemas in `src-tauri/gen/schemas/`.

**Step 7.3**: Verify permission identifiers are lowercase ASCII only (`[a-z]`, hyphens, colons). Maximum 116 characters.

**Step 7.4**: Verify inline capabilities in `tauri.conf.json` use the correct structure:
```json
{
  "app": {
    "security": {
      "capabilities": [
        {
          "identifier": "inline-cap",
          "windows": ["*"],
          "permissions": ["fs:default"]
        },
        "external-capability-file-name"
      ]
    }
  }
}
```

---

## Step-by-Step Permission Setup Workflow

For any new plugin or custom command, follow this checklist:

1. **Install**: Add Cargo crate and npm package
2. **Register**: Call `.plugin()` in Rust Builder
3. **Create capability** (if none exists): Create `src-tauri/capabilities/default.json`
4. **Add permission**: Add `"<plugin>:default"` or specific `"<plugin>:allow-<cmd>"` to the permissions array
5. **Set window scope**: Ensure the `"windows"` array includes the window that will call the API
6. **Add scopes** (if needed): Configure allow/deny paths or URLs
7. **Rebuild**: Run `cargo build` to regenerate schemas
8. **Test**: Verify the operation works in both dev and production builds

---

## Reference Links

- [references/methods.md](references/methods.md) -- Permission system API reference
- [references/examples.md](references/examples.md) -- Complete capability file examples
- [references/anti-patterns.md](references/anti-patterns.md) -- Permission configuration mistakes

### Official Sources

- https://v2.tauri.app/security/permissions/
- https://v2.tauri.app/security/capabilities/
- https://v2.tauri.app/reference/config/#securityconfig
