---
name: browser-tools
description: Use this skill when the user asks to test, verify, interact with, or automate web pages and browsers. Trigger for requests involving Chrome automation, browser testing, web scraping, screenshot capture, element selection, or checking web applications. Also trigger when user mentions "browser tools" explicitly.
allowed-tools: Bash(browser-start:*), Bash(browser-nav:*), Bash(browser-eval:*), Bash(browser-screenshot:*), Bash(browser-pick:*), Bash(browser-cookies:*), Bash(browser-console:*), Read, Read(/tmp/screenshot*), Glob
---

# Browser Tools

Chrome DevTools Protocol automation for agent-assisted web testing and interaction. Uses Chrome running on `:9222` with remote debugging.

## Prerequisites

**Run `/browser-tools:setup` once after plugin installation** - This installs dependencies and creates global symlinks for all browser scripts.

## Usage

When user asks to test, verify, or interact with web pages using browser tools:

1. **Start Chrome** - Launch with debugging enabled
2. **Navigate & interact** - Use scripts to navigate, evaluate JS, take screenshots
3. **Return results** - Show output/screenshots to user

**IMPORTANT**: Use command names directly (e.g., `browser-start`), NOT full paths (e.g., `~/bin/browser-start`). Commands are in PATH after setup.

## Available Scripts

All scripts located in `${CLAUDE_SKILL_DIR}/scripts/`:

### browser-start

By default use the persistent profile at `/tmp/chrome-profile-browser-tools`.

```bash
browser-start --profile    # Persistent profile
browser-start              # Fresh profile
```

Launch Chrome with remote debugging on port 9222. Use `--profile` to maintain login state between sessions.

### browser-nav

```bash
browser-nav https://example.com
browser-nav https://example.com --new
```

Navigate to URLs. Use `--new` to open in new tab instead of current tab.

### browser-eval

```bash
browser-eval 'document.title'
browser-eval 'document.querySelectorAll("a").length'
browser-eval 'Array.from(document.querySelectorAll("h1")).map(h => h.textContent)'
```

Execute JavaScript in active tab. Runs in async context. Use for:

- Extract data from pages
- Inspect page state
- Manipulate DOM
- Test page functionality

### browser-screenshot

```bash
browser-screenshot
```

Capture current viewport, returns temp file path. Use Read tool to show screenshot to user.

### browser-pick

```bash
browser-pick                      # Uses default message "Select element(s)"
browser-pick "Select the submit button"
```

**Interactive element picker** - Launches UI overlay for user to click and select elements. Returns element details (tag, id, class, text, html, parent hierarchy). Message parameter is optional.

Use when:

- User says "click that button" or "extract those items"
- Need specific selectors but page structure is unclear
- User wants to identify elements visually

Controls:

- Click to select single element
- Cmd/Ctrl+Click for multiple selections
- Enter to finish (when multiple selected)
- ESC to cancel

### browser-console

```bash
browser-console                         # Stream logs until Ctrl+C or kill
browser-console --url http://...        # Navigate and exit after load
browser-console --url http://... --no-exit  # Navigate then keep streaming
browser-console --level error,warn      # Filter by log level
```

Capture console logs (log, warn, error, info, debug) from Chrome. Includes stack traces for errors and page errors.

**Modes:**

- **Streaming** (default): Captures logs until process is killed. Best for workflow monitoring.
- **Navigation** (`--url`): Navigates to URL and exits after page load. Captures logs during page initialization.

**Claude Code usage:**

```bash
# Page load logs - auto-exits after load
browser-console --url http://localhost:3000

# Workflow monitoring - run in background, kill when done
browser-console &
browser-nav http://localhost:3000
browser-eval "triggerSomeAction()"
# Check logs via BashOutput, kill via KillShell
```

### browser-cookies

```bash
browser-cookies
```

Display all cookies for current tab (domain, path, httpOnly, secure flags). Use for debugging auth issues.

## Workflow Examples

### Test dev server feature

```bash
# Start browser with persistent profile
browser-start --profile

# Navigate to dev server
browser-nav http://localhost:3000

# Test functionality
browser-eval 'document.querySelector("#new-feature").textContent'

# Take screenshot
SCREENSHOT=$(browser-screenshot)
# Then use Read tool to show screenshot at $SCREENSHOT path
```

### Debug authentication

```bash
browser-start --profile
browser-nav https://app.example.com/login
browser-cookies
```

### Extract data from page

```bash
browser-start
browser-nav https://example.com
browser-eval 'Array.from(document.querySelectorAll(".product")).map(p => ({name: p.querySelector(".title").textContent, price: p.querySelector(".price").textContent}))'
```

## Important Notes

- **Chrome required** - Scripts use `google-chrome` binary
- **Port 9222** - Chrome runs with `--remote-debugging-port=9222`
- **Profile location** - `/tmp/chrome-profile-browser-tools` when using `--profile`
- **Temp screenshots** - Screenshots saved to OS temp directory
- **Dependencies** - Requires `chrome-remote-interface` (installed via `/browser-tools:setup`)
- **Error handling** - If scripts fail, check Chrome is running and port 9222 is available
