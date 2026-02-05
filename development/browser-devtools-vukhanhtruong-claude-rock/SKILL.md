---
name: browser-devtools
description: Browser debugging and automation using Playwright. Use for web debugging, console monitoring, network analysis, screenshot capture, DOM inspection, and UI testing during development.
license: Apache-2.0
---

# Browser Devtools

Browser automation and debugging using Playwright for web development testing and analysis.

## Decision tree

Here the decison tree when user want to inspect the console log, apply the same pattern for other prompt.

```
User task → Is URL provided?
    ├─ Yes → Detect if it reachable.
    │         ├─ Success → Implement Reconnaissance-then-action (RTA)
    |         |              1. Navigate to provided URL.
    |         |              2. Inspect console log
    |         |              3. Identify the errors
    |         |              4. Execute actions with discovered issues
    │         └─ Fails → End
    │
    └─ No → Is the development server already running?
              ├─ No → End
              │
              └─ Yes → Ask user if they want to test development server?
                        ├─ Yes →  Reconnaissance-then-action (RTA)
                        ├─ No → End
```

## Quick Start

Install dependencies:

```bash
cd plugins/browser-devtools/skills
./scripts/install.sh
```

Test installation:

```bash
node dist/scripts/navigate.js --url https://example.com
```

## Scripts

All scripts located in `scripts/` (compiled to `dist/scripts/`):

**Core Commands:**

- `navigate.js` - Navigate to URLs
- `screenshot.js` - Capture screenshots (full page or elements)
- `snapshot.js` - DOM inspection and element discovery
- `evaluate.js` - Execute JavaScript in browser context
- `click.js` - Element interaction
- `fill.js` - Form input testing

**Monitoring:**

- `console.js` - Console log monitoring and error tracking
- `network.js` - Network request analysis and performance debugging
- `performance.js` - Core Web Vitals and performance metrics

## Best Practices

- **Compliance Decision tree**: The decision tree must be followed strictly.
- **Wait for elements**: Use appropriate wait strategies for dynamic content
- **Clean up sessions**: Close sessions when done to free resources

## Usage

### Single Commands

```bash
# Screenshot
node dist/scripts/screenshot.js --url https://example.com --output page.png

# Performance analysis
node dist/scripts/performance.js --url https://example.com | jq '.vitals.LCP'

# Console monitoring (10 seconds)
node dist/scripts/console.js --url https://example.com --types error,warn --duration 10000
```

### Chained Commands (reuse session)

```bash
# Start session (keep browser open)
node dist/scripts/navigate.js --url https://example.com/login --close false

# Continue with same browser
node dist/scripts/fill.js --selector "#email" --value "user@example.com" --close false
node dist/scripts/click.js --selector "button[type=submit]"
```

### Common Debugging Patterns

```bash
# Find elements
node dist/scripts/snapshot.js --url https://example.com | jq '.elements[] | {tagName, text, selector}'

# Check for errors
node dist/scripts/console.js --url https://example.com --types error

# Monitor API calls
node dist/scripts/network.js --url https://example.com --types xhr,fetch --duration 5000

# Test forms
node dist/scripts/fill.js --url https://example.com --selector "#search" --value "query" --close false
node dist/scripts/click.js --selector "button[type=submit]"
```

## Options

All scripts support:

- `--headless false` - Show browser window (default: true)
- `--close false` - Keep browser open for chaining (default: true)
- `--timeout 30000` - Timeout in milliseconds
- `--browser chromium|firefox|webkit` - Browser engine (default: chromium)

## Output Format

**Success:**

```json
{
  "success": true,
  "url": "https://example.com",
  "title": "Example Domain",
  "sessionId": "session_1234567890_abc123",
  "timestamp": "2024-01-01T12:00:00.000Z",
  "...": "script-specific data"
}
```

**Error:**

```json
{
  "success": false,
  "error": "Element not found: .missing-element",
  "stack": "Error: Element not found..."
}
```

## Selectors

```bash
# CSS selectors
node dist/scripts/click.js --selector "#main .button.primary"

# XPath
node dist/scripts/click.js --selector "xpath=//button[contains(text(), 'Submit')]"

# Text selectors
node dist/scripts/click.js --selector "text=Click me"
```

## Troubleshooting

**Browser not installed**: Run `npm run install-browsers`
**Element not found**: Use `snapshot.js` first to find correct selectors
**Script timeout**: Increase with `--timeout 60000`
**Permission denied**: Run `chmod +x scripts/install.sh`

**Debug mode**: Use `--headless false` to see browser actions
**Stale sessions**: Start new session with `--close true`

## Integration

**Pre-commit testing:**

```bash
node dist/scripts/navigate.js --url http://localhost:3000 && \
node dist/scripts/performance.js --url http://localhost:3000 | jq '.vitals.LCP'
```

**Performance regression:**

```bash
node dist/scripts/performance.js --url $APP_URL | jq '.vitals.LCP' | \
  awk '{print $1 < 2500 ? "PASS" : "FAIL"}'
```

## References

- [Playwright Documentation](https://playwright.dev/)
- [Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/)
- [Core Web Vitals](https://web.dev/vitals/)
