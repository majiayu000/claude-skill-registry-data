---
name: agent-browser
slug: agent-browser
version: 1.1.0
description: Self-contained browser automation. Navigates websites, fills forms, takes screenshots, extracts data. Runtime auto-installs on first use — no npm, Node.js, or Chrome required on the host.
setup: bootstrap.sh
allowed-tools: Bash(agent-browser:*)
---

# Browser Automation with agent-browser

## Runtime Setup (MANDATORY — run before any command)

Before executing ANY agent-browser command, you MUST ensure the runtime is installed:

1. Check if `runtime/version.txt` exists in this skill's directory
2. If it does NOT exist, run the bootstrap script:
   - **macOS / Linux**: `bash "<SKILL_DIR>/bootstrap.sh"`
   - **Windows**: `powershell -ExecutionPolicy Bypass -File "<SKILL_DIR>/bootstrap.ps1"`
   This downloads ~230MB runtime (one-time). Tell the user: "正在首次准备浏览器环境，请稍候..."
3. After bootstrap, ALL commands must go through the wrapper:
   - **macOS / Linux**: `"<SKILL_DIR>/agent-browser" <command> [args...]`
   - **Windows**: `"<SKILL_DIR>/agent-browser.cmd" <command> [args...]`

Replace `<SKILL_DIR>` with the absolute path to this skill's directory.

NEVER call `agent-browser` directly without the skill directory prefix. Always use `"<SKILL_DIR>/agent-browser"` (macOS/Linux) or `"<SKILL_DIR>/agent-browser.cmd"` (Windows).

## Quick start

```bash
"<SKILL_DIR>/agent-browser" open <url>        # Navigate to page
"<SKILL_DIR>/agent-browser" snapshot -i       # Get interactive elements with refs
"<SKILL_DIR>/agent-browser" click @e1         # Click element by ref
"<SKILL_DIR>/agent-browser" fill @e2 "text"   # Fill input by ref
"<SKILL_DIR>/agent-browser" close             # Close browser
```

## Core workflow

1. Navigate: `"<SKILL_DIR>/agent-browser" open <url>`
2. Snapshot: `"<SKILL_DIR>/agent-browser" snapshot -i` (returns elements with refs like `@e1`, `@e2`)
3. Interact using refs from the snapshot
4. Re-snapshot after navigation or significant DOM changes

## Command Reference

Below, `AB` is shorthand for `"<SKILL_DIR>/agent-browser"`. Replace `<SKILL_DIR>` with the absolute path to this skill's directory in every invocation.

### Navigation

```bash
"<SKILL_DIR>/agent-browser" open <url>
"<SKILL_DIR>/agent-browser" back
"<SKILL_DIR>/agent-browser" forward
"<SKILL_DIR>/agent-browser" reload
"<SKILL_DIR>/agent-browser" close
"<SKILL_DIR>/agent-browser" connect 9222    # Connect via CDP port
```

### Snapshot (page analysis)

```bash
"<SKILL_DIR>/agent-browser" snapshot            # Full accessibility tree
"<SKILL_DIR>/agent-browser" snapshot -i         # Interactive elements only (recommended)
"<SKILL_DIR>/agent-browser" snapshot -c         # Compact output
"<SKILL_DIR>/agent-browser" snapshot -d 3       # Limit depth to 3
"<SKILL_DIR>/agent-browser" snapshot -s "#main" # Scope to CSS selector
```

### Interactions (use @refs from snapshot)

```bash
"<SKILL_DIR>/agent-browser" click @e1
"<SKILL_DIR>/agent-browser" dblclick @e1
"<SKILL_DIR>/agent-browser" fill @e2 "text"     # Clear and type
"<SKILL_DIR>/agent-browser" type @e2 "text"     # Type without clearing
"<SKILL_DIR>/agent-browser" press Enter
"<SKILL_DIR>/agent-browser" hover @e1
"<SKILL_DIR>/agent-browser" check @e1
"<SKILL_DIR>/agent-browser" uncheck @e1
"<SKILL_DIR>/agent-browser" select @e1 "value"
"<SKILL_DIR>/agent-browser" scroll down 500
"<SKILL_DIR>/agent-browser" scrollintoview @e1
"<SKILL_DIR>/agent-browser" drag @e1 @e2
"<SKILL_DIR>/agent-browser" upload @e1 file.pdf
```

### Get information

```bash
"<SKILL_DIR>/agent-browser" get text @e1
"<SKILL_DIR>/agent-browser" get html @e1
"<SKILL_DIR>/agent-browser" get value @e1
"<SKILL_DIR>/agent-browser" get attr @e1 href
"<SKILL_DIR>/agent-browser" get title
"<SKILL_DIR>/agent-browser" get url
"<SKILL_DIR>/agent-browser" get count ".item"
```

### Screenshots & PDF

```bash
"<SKILL_DIR>/agent-browser" screenshot
"<SKILL_DIR>/agent-browser" screenshot path.png
"<SKILL_DIR>/agent-browser" screenshot --full    # Full page
"<SKILL_DIR>/agent-browser" pdf output.pdf
```

### Wait

```bash
"<SKILL_DIR>/agent-browser" wait @e1
"<SKILL_DIR>/agent-browser" wait 2000
"<SKILL_DIR>/agent-browser" wait --text "Success"
"<SKILL_DIR>/agent-browser" wait --url "**/dashboard"
"<SKILL_DIR>/agent-browser" wait --load networkidle
```

### Semantic locators

```bash
"<SKILL_DIR>/agent-browser" find role button click --name "Submit"
"<SKILL_DIR>/agent-browser" find text "Sign In" click
"<SKILL_DIR>/agent-browser" find label "Email" fill "user@test.com"
```

### Cookies & Storage

```bash
"<SKILL_DIR>/agent-browser" cookies
"<SKILL_DIR>/agent-browser" cookies set name value
"<SKILL_DIR>/agent-browser" cookies clear
"<SKILL_DIR>/agent-browser" storage local
```

### Tabs

```bash
"<SKILL_DIR>/agent-browser" tab
"<SKILL_DIR>/agent-browser" tab new [url]
"<SKILL_DIR>/agent-browser" tab 2
"<SKILL_DIR>/agent-browser" tab close
```

### Dialogs

```bash
"<SKILL_DIR>/agent-browser" dialog accept [text]
"<SKILL_DIR>/agent-browser" dialog dismiss
```

### JavaScript

```bash
"<SKILL_DIR>/agent-browser" eval "document.title"
```

## Global options

```bash
"<SKILL_DIR>/agent-browser" --session <name> ...    # Isolated browser session
"<SKILL_DIR>/agent-browser" --json ...              # JSON output for parsing
"<SKILL_DIR>/agent-browser" --headed ...            # Show browser window
"<SKILL_DIR>/agent-browser" --proxy <url> ...       # Use proxy server
```

## Example: Form submission

```bash
"<SKILL_DIR>/agent-browser" open https://example.com/form
"<SKILL_DIR>/agent-browser" snapshot -i
"<SKILL_DIR>/agent-browser" fill @e1 "user@example.com"
"<SKILL_DIR>/agent-browser" fill @e2 "password123"
"<SKILL_DIR>/agent-browser" click @e3
"<SKILL_DIR>/agent-browser" wait --load networkidle
"<SKILL_DIR>/agent-browser" snapshot -i
```

## Example: Authentication with saved state

```bash
"<SKILL_DIR>/agent-browser" open https://app.example.com/login
"<SKILL_DIR>/agent-browser" snapshot -i
"<SKILL_DIR>/agent-browser" fill @e1 "username"
"<SKILL_DIR>/agent-browser" fill @e2 "password"
"<SKILL_DIR>/agent-browser" click @e3
"<SKILL_DIR>/agent-browser" wait --url "**/dashboard"
"<SKILL_DIR>/agent-browser" state save auth.json

# Later: load saved state
"<SKILL_DIR>/agent-browser" state load auth.json
"<SKILL_DIR>/agent-browser" open https://app.example.com/dashboard
```
