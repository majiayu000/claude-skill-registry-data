---
name: chrome-devtools-extensions
description: Install, manage, reload, and trigger Chrome extensions via Chrome DevTools MCP. Enables agent-driven extension testing, side-loading unpacked extensions, and extension action automation.
origin: https://github.com/ChromeDevTools/chrome-devtools-mcp (Apache-2.0)
license: Apache-2.0
version: 1.0.0
compatibility: claude-sonnet-4-6, claude-opus-4-7
---

# Chrome DevTools Extensions

Manage Chrome extensions programmatically through 5 MCP tools — install, reload, trigger, list, uninstall.

## When to Use

- Testing an unpacked extension during development (side-load → trigger → verify)
- Automating extension regression tests (install specific version → run checks)
- Validating extension behavior after code changes without manual clicks
- Agent workflow that depends on a browser extension being active (ad-blocker, auth helper)

## Do NOT use for

- Publishing extensions to Chrome Web Store (use CWS dashboard)
- Bypassing extension security reviews for production deployments
- Installing extensions from unknown sources on production systems (security risk)

## MCP Tools (5)

```
browser_extension_install    — install extension from .crx path or unpacked dir
browser_extension_list       — list all installed extensions (id, name, version, enabled)
browser_extension_reload     — reload an extension by id (applies code changes)
browser_extension_trigger    — click extension action button (opens popup or runs background)
browser_extension_uninstall  — remove extension by id
```

## Usage Pattern

```yaml
# Development workflow: side-load → test → iterate
1. browser_extension_install: path: "./dist/my-extension"
   # → returns extensionId

2. browser_navigate: url: "https://app.example.com"
3. browser_extension_trigger: extensionId: "abc123..."
   # → triggers extension action on current page

4. browser_screenshot
   # → verify extension popup / overlay appeared

# After code change:
5. browser_extension_reload: extensionId: "abc123..."
6. browser_extension_trigger: extensionId: "abc123..."
   # → test again with updated code
```

## Extension List Response

```json
[
  {
    "id": "abc123def456",
    "name": "My Dev Extension",
    "version": "0.4.2",
    "enabled": true,
    "type": "extension"
  }
]
```

## CI Integration Pattern

```yaml
# In agent test loop:
setup:
  - browser_extension_install: path: "$EXTENSION_DIST_DIR"
  
per_test:
  - browser_navigate: url: "$TEST_URL"
  - browser_extension_trigger: extensionId: "$EXT_ID"
  - browser_wait_for: selector: "[data-ext-loaded]"
  - browser_screenshot  # capture result

teardown:
  - browser_extension_uninstall: extensionId: "$EXT_ID"
```

## Anti-Fake-Pass Checklist

- [ ] `browser_extension_install` returned a valid extensionId (not null)
- [ ] `browser_extension_list` confirms extension is `enabled: true` before trigger
- [ ] After `browser_extension_reload`, waited for extension service worker to restart
- [ ] `browser_extension_uninstall` called in teardown to avoid state leakage between tests
- [ ] Extension path is local/trusted — never install from arbitrary remote URLs
