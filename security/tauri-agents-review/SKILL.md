---
name: tauri-agents-review
description: >
  Use when reviewing Tauri 2 code, auditing permissions, or validating a Tauri project before deployment.
  Prevents shipping apps with missing permissions, unhandled IPC errors, insecure CSP, and unregistered commands.
  Covers command signature review, permission coverage, state management, error handling, security audit, and anti-pattern detection.
  Keywords: tauri code review, validation checklist, security audit, permissions audit, anti-pattern scan, deployment readiness.
license: MIT
compatibility: "Designed for Claude Code. Requires Tauri 2.x."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# tauri-agents-review

## Review Workflow

Execute these checklists in order. Each section is independent -- report all findings, do not stop at the first issue.

```
Review Order:
1. Commands & IPC Bridge    --> Rust signatures + JS invoke pairing
2. Permissions & Capabilities --> ACL coverage
3. State Management         --> Thread safety + correctness
4. Error Handling           --> Result types + frontend catching
5. Security                 --> CSP + scopes + dangerous settings
6. Build Configuration      --> Config completeness
7. Anti-Pattern Scan        --> Known mistakes
```

---

## Checklist 1: Commands & IPC Bridge

### 1A: Rust Command Signatures

For every `#[tauri::command]` function, verify:

```
[ ] NEVER mark commands as pub if defined directly in lib.rs
[ ] ALWAYS mark commands as pub if defined in a separate module
[ ] ALWAYS use owned types (String, not &str) for async command parameters
    Exception: &str allowed if return type is Result<T, E>
[ ] ALWAYS return Result<T, E> for any fallible operation
[ ] ALWAYS implement serde::Serialize on the error type E
[ ] ALWAYS implement serde::Deserialize on all custom parameter types
[ ] ALWAYS implement serde::Serialize on all custom return value types
[ ] ALWAYS implement both Serialize AND Clone on event payload types
```

### 1B: Command Registration

```
[ ] ALWAYS list all commands in a SINGLE generate_handler![] call
    NEVER use multiple .invoke_handler() calls on Builder
[ ] ALWAYS register every #[tauri::command] function
    Cross-reference: grep for #[tauri::command] and compare with generate_handler![]
[ ] ALWAYS use correct module paths (e.g., commands::greet, not just greet)
```

### 1C: IPC Bridge Completeness

For every Rust command, verify a matching frontend invoke exists:

```
[ ] ALWAYS verify invoke('command_name', ...) call exists in TypeScript/JavaScript
[ ] ALWAYS use camelCase argument keys (NEVER use snake_case in frontend invoke calls)
[ ] ALWAYS match argument types to Rust parameter types:
    - Rust String <-> JS string
    - Rust i32/u32/u64/f64 <-> JS number
    - Rust bool <-> JS boolean
    - Rust Vec<T> <-> JS array
    - Rust Option<T> <-> JS null/undefined
[ ] ALWAYS specify return type generic: invoke<ExpectedType>('...')
[ ] ALWAYS handle error case with try/catch
```

### 1D: Channel Usage (if applicable)

```
[ ] ALWAYS pair Channel<T> parameter in Rust with matching new Channel<T>() in JS
[ ] ALWAYS set Channel.onmessage before the invoke() call
[ ] ALWAYS match Channel type parameter to Rust send() type
```

---

## Checklist 2: Permissions & Capabilities

### 2A: Plugin Permissions

For every plugin in Cargo.toml dependencies:

```
[ ] ALWAYS initialize plugin in Builder: .plugin(tauri_plugin_X::init())
[ ] ALWAYS install corresponding npm package: @tauri-apps/plugin-X
[ ] ALWAYS add permission entry in capabilities file(s)
[ ] ALWAYS grant default permission or specific allow-* permissions
```

### 2B: Custom Command Permissions

For every `#[tauri::command]`:

```
[ ] ALWAYS define permission in src-tauri/permissions/*.toml
    Format: commands.allow = ["command_name"]
[ ] ALWAYS reference permission in capabilities file
[ ] NEVER allow a custom command to be callable without explicit permission
```

### 2C: Capability File Validation

For every file in `src-tauri/capabilities/`:

```
[ ] ALWAYS include valid $schema reference
[ ] ALWAYS use unique identifier
[ ] NEVER use windows: ["*"] without documented justification
[ ] ALWAYS include all needed permissions in permissions[] array
[ ] ALWAYS use correct platforms[] values for platform-specific capabilities
[ ] NEVER duplicate permission entries across capability files
```

### 2D: Scope Verification

```
[ ] ALWAYS restrict fs plugin scopes to needed directories only
[ ] ALWAYS restrict http plugin scopes to needed URLs only
[ ] ALWAYS whitelist specific commands only in shell plugin scopes
[ ] ALWAYS keep asset protocol scope minimal ($APPDATA/**, $RESOURCE/**)
[ ] ALWAYS use deny rules to exclude sensitive paths/URLs
```

---

## Checklist 3: State Management

### 3A: Registration

```
[ ] ALWAYS ensure all State<'_, T> types used in commands have matching manage() calls
[ ] ALWAYS call manage() BEFORE any command that uses the state can execute
    (i.e., in Builder chain or early in setup())
[ ] NEVER call manage() twice for the same type (returns false)
[ ] ALWAYS ensure state types are Send + Sync + 'static
```

### 3B: Thread Safety

```
[ ] ALWAYS wrap mutable state in Mutex, RwLock, or atomic types
[ ] ALWAYS use std::sync::Mutex by default (NEVER use tokio::sync::Mutex unless lock held across .await)
[ ] NEVER wrap state in Arc (Tauri manages Arc internally)
[ ] NEVER nest locking of the same Mutex (deadlock risk)
```

### 3C: Lock Discipline

```
[ ] ALWAYS drop Mutex guards before calling other functions that may lock
[ ] ALWAYS keep lock scopes minimal (lock, operate, drop)
[ ] ALWAYS use RwLock for read-heavy state (multiple concurrent readers)
[ ] NEVER hold a lock during I/O or network operations (unless tokio Mutex)
```

---

## Checklist 4: Error Handling

### 4A: Rust Side

```
[ ] ALWAYS return Result<T, E> for commands returning data
[ ] ALWAYS use thiserror for error types (NEVER use manual Display impl)
[ ] ALWAYS implement Serialize on error types (manual impl, NEVER derive)
[ ] NEVER use unwrap() or expect() in command handlers
[ ] ALWAYS convert I/O errors via #[from] or manual From impl
[ ] ALWAYS make error messages user-friendly (NEVER expose raw debug output)
```

### 4B: Frontend Side

```
[ ] ALWAYS wrap every invoke() call in try/catch
[ ] ALWAYS handle errors in catch blocks (log, display, recover)
[ ] ALWAYS parse structured errors correctly (if using tagged enum pattern)
[ ] NEVER leave unhandled Promise rejections from invoke()
```

---

## Checklist 5: Security Audit

### 5A: Content Security Policy

```
[ ] NEVER set CSP to null in production
[ ] ALWAYS set default-src to 'self'
[ ] NEVER include 'unsafe-eval' in script-src
[ ] ALWAYS include ipc: and http://ipc.localhost in connect-src
[ ] ALWAYS include asset: and https://asset.localhost in img-src if needed
[ ] NEVER use wildcard (*) domains without documented justification
```

### 5B: Dangerous Settings

```
[ ] ALWAYS set freezePrototype to true (prevents prototype pollution)
[ ] NEVER enable dangerousDisableAssetCspModification
[ ] NEVER enable withGlobalTauri in production
[ ] NEVER use shell:default without scope restrictions
[ ] NEVER grant fs permissions without scope restrictions
[ ] NEVER grant http permissions without URL scope
```

### 5C: Capability Scope

```
[ ] NEVER use windows: ["*"] with broad permissions in any capability
[ ] ALWAYS scope platform-specific capabilities correctly
[ ] ALWAYS keep remote capabilities (if any) to minimal permissions
[ ] ALWAYS use explicit core permissions (core:default, core:window:default)
```

---

## Checklist 6: Build Configuration

### 6A: tauri.conf.json

```
[ ] ALWAYS use unique reverse-domain format for identifier
[ ] ALWAYS point build.frontendDist to correct output directory
[ ] ALWAYS configure build.beforeBuildCommand to build frontend assets
[ ] ALWAYS configure build.beforeDevCommand to start dev server
[ ] ALWAYS match build.devUrl to dev server port
[ ] ALWAYS configure at least one window in app.windows[]
[ ] ALWAYS include all required icon formats (.ico, .icns, .png) in bundle.icon
```

### 6B: Cargo.toml

```
[ ] ALWAYS use tauri dependency version 2.x
[ ] ALWAYS include tauri-build in build-dependencies
[ ] ALWAYS ensure build.rs exists and calls tauri_build::build()
[ ] ALWAYS include ["staticlib", "cdylib", "rlib"] in crate-type if targeting mobile
[ ] ALWAYS version all plugin crates at "2"
```

### 6C: Package.json

```
[ ] ALWAYS include @tauri-apps/cli in devDependencies
[ ] ALWAYS include @tauri-apps/api in dependencies
[ ] ALWAYS install all plugin npm packages (@tauri-apps/plugin-*)
[ ] ALWAYS align versions (all ^2)
```

### 6D: Source Control

```
[ ] ALWAYS commit Cargo.lock (NEVER add to .gitignore)
[ ] ALWAYS add src-tauri/target/ to .gitignore
[ ] NEVER commit secrets (.env, API keys, signing keys)
```

---

## Checklist 7: Anti-Pattern Scan

Scan the codebase for these known issues:

```
[ ] NEVER use multiple .invoke_handler() calls
[ ] NEVER use pub commands in lib.rs
[ ] NEVER wrap managed state in Arc
[ ] NEVER use &str in async command parameters (without Result return)
[ ] NEVER use .unwrap() in command handlers
[ ] NEVER use snake_case keys in frontend invoke() calls
[ ] NEVER leave event listeners without cleanup
[ ] NEVER use dots, spaces, or special characters in event names
[ ] NEVER set CSP to null
[ ] NEVER omit Serialize on error types
[ ] NEVER omit Clone on event payloads
[ ] NEVER use sync I/O operations in command handlers (ALWAYS use async)
[ ] NEVER leave installed plugins without permissions
[ ] NEVER use relative paths without BaseDirectory in fs calls
```

---

## Review Report Template

After completing all checklists, produce a report:

```
## Tauri 2 Code Review Report

### Summary
- Total issues found: X
- Critical (blocks deployment): X
- Warning (should fix): X
- Info (improvement suggestion): X

### Critical Issues
1. [CRIT-001] Description -- Location -- Fix

### Warnings
1. [WARN-001] Description -- Location -- Fix

### Passed Checks
- Commands & IPC Bridge: PASS/FAIL (X/Y checks passed)
- Permissions: PASS/FAIL
- State Management: PASS/FAIL
- Error Handling: PASS/FAIL
- Security: PASS/FAIL
- Build Config: PASS/FAIL
- Anti-Patterns: PASS/FAIL
```

---

## Decision Trees

### Is a command correctly wired?

```
Does #[tauri::command] exist on the function?
+-- No --> Add the macro
+-- Yes
    |
    Is it in generate_handler![]?
    +-- No --> Add it
    +-- Yes
        |
        Does a permission exist in src-tauri/permissions/?
        +-- No --> Create permission TOML
        +-- Yes
            |
            Is it referenced in a capability file?
            +-- No --> Add to capabilities
            +-- Yes
                |
                Does a matching invoke() call exist in JS?
                +-- No --> Add frontend invoke
                +-- Yes --> PASS
```

### Is state correctly managed?

```
Is State<'_, T> used in a command?
+-- No --> Skip
+-- Yes
    |
    Does manage(T) exist on Builder or in setup()?
    +-- No --> CRITICAL: Add manage() call
    +-- Yes
        |
        Does the generic type match exactly?
        +-- No --> CRITICAL: Fix type mismatch
        +-- Yes
            |
            Is T mutable?
            +-- No --> PASS
            +-- Yes
                |
                Is T wrapped in Mutex/RwLock?
                +-- No --> CRITICAL: Add interior mutability
                +-- Yes --> PASS (verify no deadlocks)
```

---

## Reference Links

- [references/methods.md](references/methods.md) -- Review commands, grep patterns, validation rules
- [references/examples.md](references/examples.md) -- Example review findings and reports
- [references/anti-patterns.md](references/anti-patterns.md) -- Complete anti-pattern catalog with detection patterns

### Official Sources

- https://v2.tauri.app/security/
- https://v2.tauri.app/develop/calling-rust/
- https://v2.tauri.app/security/capabilities/
