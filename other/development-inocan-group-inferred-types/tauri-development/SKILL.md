---
name: tauri-development
description: Guide for developing Tauri v2 desktop apps on macOS. Covers debugging native apps (Rust panics, Sentry integration, thread-local issues), app signing and updater setup, global shortcuts, Keychain secret storage, and Homebrew distribution. Use when building Tauri apps, debugging Rust backend issues, setting up auto-updates, handling keyboard shortcuts, or distributing macOS apps.
---

# Tauri Development Guide

Practical knowledge for building production-ready Tauri v2 desktop apps on macOS.

## Quick Reference

| Topic | When to Use | Reference |
|-------|-------------|-----------|
| Debugging | Rust panics disappear, Sentry not capturing | [debugging.md](references/debugging.md) |
| Signing & Updates | Setting up Tauri updater, CI signing | [signing.md](references/signing.md) |
| Shortcuts | Global hotkeys conflict, modifier keys | [shortcuts.md](references/shortcuts.md) |
| Secrets | Storing API keys securely | [secrets.md](references/secrets.md) |
| Distribution | Homebrew tap, Gatekeeper issues | [distribution.md](references/distribution.md) |

## Key Principles

### 1. Native Apps Have More Failure Modes

Unlike web apps:
- Process can abort before HTTP requests complete
- Thread-local state doesn't work across async boundaries
- Framework state (`app.manage()`) isn't always equivalent to global statics
- Logs are scattered across system logs, Tauri logs, and Rust stderr

### 2. Explicit Over Implicit

```rust
// Prefer direct API calls with explicit timeouts
client.capture_event(event, None);
client.flush(Some(Duration::from_secs(2)));

// Over convenience wrappers that may fail silently
sentry::capture_message("...", Level::Info);
```

### 3. Test Each Layer Independently

When debugging, test progressively:
1. Main thread behavior
2. Spawned thread behavior
3. Async task behavior
4. External service connectivity

### 4. macOS Security is Signature-Aware

Many APIs behave differently for unsigned/notarized apps:
- Keychain access (use `security` CLI instead of `keyring` crate)
- Gatekeeper (document `xattr -cr` workaround)
- Global shortcuts (may require accessibility permissions)

## Common Commands

```bash
# View macOS system logs
log show --predicate 'subsystem == "com.your.app"' --last 5m

# Check Keychain entries
security find-generic-password -s "com.your.app" -a "account_name" -w

# Remove quarantine attribute
xattr -cr /Applications/YourApp.app

# Generate Tauri signing key (non-empty password!)
pnpm tauri signer generate -w ~/.tauri/myapp.key
```

## Debugging Checklist

When something silently fails:

1. [ ] Add `eprintln!` debugging (works when logs don't)
2. [ ] Check user settings files (features may be disabled)
3. [ ] Verify external services (API keys, DSN, network)
4. [ ] Test unsigned vs signed behavior
5. [ ] Check process lifecycle (does it die before completing async work?)

## Safe Global Shortcut Selection

| Modifier Combo | Safety | Notes |
|----------------|--------|-------|
| ⌘⌥ + key | Low | Many apps use this |
| ⌘⇧ + key | Medium | Somewhat used |
| ⌃⌘ + key | Medium | Some apps use |
| **⌃⌥ + key** | **High** | Rarely used |
| ⌃⇧⌘ + key | High | Too complex, rarely used |

**Tip:** If clipboard operations fail intermittently, suspect shortcut conflicts—not code bugs.
