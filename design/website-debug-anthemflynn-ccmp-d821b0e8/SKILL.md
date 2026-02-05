---
name: website-debug
description: >
  Frontend website debugging toolkit using Chrome DevTools Protocol with Playwright/WebKit fallbacks.
  Use this skill when: (1) Debugging CSS, HTML, or JavaScript issues on a webpage, (2) Taking screenshots
  to verify visual changes, (3) Inspecting DOM structure or console errors, (4) Testing responsive layouts,
  (5) Extracting selectors for automation, (6) Self-debugging frontend work Claude has created,
  (7) User says "debug this page", "check my site", "why doesn't this look right", or "fix the frontend".
  Supports Chrome (primary) and Safari/WebKit (via Playwright). Designed for agent-driven debugging loops.
---

# Website Debugging Skill

Lightweight, token-efficient browser debugging toolkit for frontend development. Uses CLI scripts instead of MCP servers to minimize context usage (~300 tokens vs 13k-18k).

## Quick Start

Use the slash commands for easiest access:
- `/debug-page <url>` - Start debugging session
- `/screenshot` - Take screenshot
- `/pick-element` - Interactive element selection
- `/test-responsive` - Test at all breakpoints
- `/verify-changes` - Verify after making changes

### Or use scripts directly:

```bash
# Start browser
node scripts/browser-start.js
node scripts/browser-start.js --profile  # Preserve logins
node scripts/browser-start.js --webkit   # Safari/WebKit

# Navigate
node scripts/browser-nav.js https://localhost:3000

# Debug
node scripts/browser-screenshot.js
node scripts/browser-eval.js 'document.title'
node scripts/browser-pick.js "Select element"
node scripts/browser-console.js --errors
node scripts/browser-network.js --failures
```

## Core Tools Reference

| Script | Purpose | Output |
|--------|---------|--------|
| `browser-start.js` | Launch Chrome/WebKit with debug port | Status message |
| `browser-nav.js <url>` | Navigate to URL | Confirmation |
| `browser-screenshot.js` | Capture viewport | File path (PNG) |
| `browser-eval.js '<js>'` | Run JS in page | Result or error |
| `browser-pick.js "<msg>"` | Interactive selector | CSS selectors |
| `browser-console.js` | Get console output | Logs/errors |
| `browser-network.js` | Network activity | Request/response data |
| `browser-dom.js "<sel>"` | Get DOM snapshot | HTML fragment |
| `browser-close.js` | Close browser | Confirmation |

## Self-Debugging Workflow

When debugging frontend code Claude has written or modified:

### 1. Visual Verification Loop
```bash
# After making CSS/HTML changes, verify visually
node scripts/browser-screenshot.js
# Claude reads the screenshot, identifies issues, iterates
```

### 2. Console Error Detection
```bash
# Check for JavaScript errors after changes
node scripts/browser-console.js --errors
# Fix any errors found, re-verify
```

### 3. Responsive Testing
```bash
# Test at different viewport sizes
node scripts/browser-resize.js 375 667   # iPhone SE
node scripts/browser-screenshot.js
node scripts/browser-resize.js 768 1024  # iPad
node scripts/browser-screenshot.js
node scripts/browser-resize.js 1920 1080 # Desktop
node scripts/browser-screenshot.js
```

### 4. Element Inspection
```bash
# When user reports "X looks wrong", have them select it
node scripts/browser-pick.js "Click on the element that looks wrong"
# Returns detailed info including computed styles
```

## Browser Engine Selection

### Chrome (Default)
Primary engine. Uses Chrome DevTools Protocol on port 9222.
- Best debugging experience
- Full DevTools compatibility  
- Use `--profile` to preserve logins

### WebKit/Safari
Fallback via Playwright's WebKit build. Closest to Safari behavior on macOS.
```bash
node scripts/browser-start.js --webkit
```
- Use for Safari-specific testing
- Layout verification
- WebKit-specific bugs

### When to Use Each

| Scenario | Engine |
|----------|--------|
| General debugging | Chrome |
| Safari layout issues | WebKit |
| Testing with logins | Chrome `--profile` |
| Cross-browser comparison | Both |
| CI/headless testing | Chrome or WebKit |

## Advanced Usage

### Detailed Documentation
For complex scenarios, load the appropriate reference:

- **CSS Debugging**: See [references/css-debug.md](references/css-debug.md)
- **JavaScript Errors**: See [references/js-debug.md](references/js-debug.md)
- **Self-Debugging**: See [references/self-debug.md](references/self-debug.md)

### Composable Output

All scripts output to files when practical, enabling:
```bash
# Capture multiple screenshots for comparison
node scripts/browser-screenshot.js --output=/tmp/before.png
# ... make changes ...
node scripts/browser-screenshot.js --output=/tmp/after.png

# Save DOM snapshot for analysis
node scripts/browser-dom.js "body" > /tmp/page-structure.html

# Export console log for review
node scripts/browser-console.js > /tmp/console-log.txt
```

### Chaining Commands
```bash
# Navigate and screenshot in one command
node scripts/browser-nav.js https://example.com && node scripts/browser-screenshot.js

# Full page audit
node scripts/browser-nav.js $URL && \
  node scripts/browser-console.js --errors > /tmp/errors.txt && \
  node scripts/browser-screenshot.js
```

## Setup Requirements

### Chrome
Chrome must be launchable from command line. The start script handles this automatically.

### WebKit (Optional)
For Safari testing, ensure Playwright is installed:
```bash
npm install -g playwright
npx playwright install webkit
```

### Dependencies
Scripts require Node.js and puppeteer-core:
```bash
npm install -g puppeteer-core
```

## Troubleshooting

### "Cannot connect to browser"
Browser may not be running or wrong port:
```bash
node scripts/browser-start.js  # Restart browser
```

### "Permission denied"
Scripts may need execute permission:
```bash
chmod +x ./scripts/*.js
```

### Chrome already running
Kill existing instances first:
```bash
killall "Google Chrome" 2>/dev/null
node scripts/browser-start.js
```

### WebKit not found
Install Playwright browsers:
```bash
npx playwright install webkit
```
