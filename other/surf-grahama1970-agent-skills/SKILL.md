---
name: surf
description: >
  Unified browser automation and CDP management for AI agents.
  Single entry point for ALL Chrome/browser interactions:
  - Start/stop Chrome with CDP for Puppeteer-based testing
  - Navigate, click, type, screenshot via surf-cli
  - Manage browser state across tools and test frameworks
allowed-tools: Bash, Read
triggers:
  # CDP/Chrome management
  - open browser
  - start chrome
  - start cdp
  - launch chrome
  - chrome devtools
  - cdp
  - puppeteer
  - headless chrome
  # Browser automation
  - click on
  - fill form
  - take screenshot
  - screenshot
  - navigate to
  - go to url
  - automate browser
  - browser automation
  - read webpage
  - scrape page
  # Testing
  - run ui tests
  - smoke tests with browser
  - browser tests
  - e2e tests
  - end to end tests
  # Troubleshooting
  - check browser
  - browser not working
  - cdp not connecting
metadata:
  short-description: Unified browser automation for AI agents
  cdp-port: 9222
---

# Surf - Unified Browser Automation

**Single entry point for ALL Chrome/browser interactions.**

## Quick Start

```bash
# Start Chrome with CDP (required for Puppeteer/smoke tests)
surf cdp start

# Check status
surf cdp status

# Navigate and interact (via surf-cli)
surf go "https://example.com"
surf read
surf click e5

# Stop Chrome
surf cdp stop
```

## CDP Management (for Puppeteer/Testing)

Chrome DevTools Protocol is required for Puppeteer-based tests (smoke tests, UI automation).

```bash
# Start Chrome with CDP on default port 9222
surf cdp start

# Start on custom port
surf cdp start 9223

# Check if CDP is running
surf cdp status

# Stop Chrome CDP
surf cdp stop

# Get connection info for scripts
surf cdp env    # Outputs export commands
```

After starting CDP, set environment for tests:
```bash
eval "$(surf cdp env)"
# Now BROWSERLESS_DISCOVERY_URL and BROWSERLESS_WS are set
```

## Integration with Make/Test Targets

```bash
# Start CDP, run smoke tests
surf cdp start
BROWSERLESS_DISCOVERY_URL=http://127.0.0.1:9222/json/version make smokes
surf cdp stop

# Or use the smokes-full target (auto-manages Chrome)
make smokes-full
```

## Command Types

| Type | Commands | Requirements | Use Case |
|------|----------|--------------|----------|
| **CDP** (standalone) | `cdp start/stop/status/env` | Chrome only | Puppeteer tests, smoke tests |
| **surf-cli** (extension) | `go/read/click/type/snap` | Chrome + Extension | Interactive automation |

## Navigation & Interaction (via surf-cli)

> **Note:** These commands require the [surf-cli Chrome extension](https://github.com/nicobailon/surf-cli) to be installed. CDP commands above work without the extension.

```bash
surf go "https://example.com"    # Navigate to URL
surf read                        # Get page content with element refs
surf click e5                    # Click element by ref
surf type "hello@example.com"    # Type text
surf type "query" --submit       # Type and press Enter
surf snap                        # Take screenshot
```

## Element References

`surf read` returns an accessibility tree with stable element refs:

```
[e1] button "Submit"
[e2] textbox "Email"
[e3] link "Sign up"
```

Use these refs: `surf click e1`, `surf type "text" --ref e2`

## Screenshots

```bash
surf snap                        # Quick screenshot to /tmp
surf screenshot --output /tmp/page.png
surf screenshot --annotate       # With element labels
surf screenshot --fullpage       # Entire scrollable page
```

## Tab Management

```bash
surf tab.list                    # List all tabs
surf tab.new "https://example.com"
surf tab.switch 123
surf tab.close 123
```

## JavaScript Execution

```bash
surf js "return document.title"
surf js "document.querySelector('.btn').click()"
```

## Waiting

```bash
surf wait 2                      # Wait 2 seconds
surf wait.element ".loaded"      # Wait for element
surf wait.network                # Wait for network idle
surf wait.url "/dashboard"       # Wait for URL pattern
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `CDP_PORT` | 9222 | Chrome DevTools Protocol port |
| `CHROME_USER_DATA` | /tmp/chrome-cdp-profile | Chrome profile directory |
| `BROWSERLESS_DISCOVERY_URL` | - | Set by `surf cdp env` |
| `BROWSERLESS_WS` | - | Set by `surf cdp env` |

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    surf skill                           │
│                  (single entry point)                   │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────┐    ┌─────────────┐    ┌────────────┐  │
│  │ surf cdp    │    │ surf-cli    │    │ Puppeteer  │  │
│  │ (manage)    │    │ (interact)  │    │ (tests)    │  │
│  └──────┬──────┘    └──────┬──────┘    └─────┬──────┘  │
│         │                  │                 │         │
│         └──────────────────┼─────────────────┘         │
│                            │                           │
│                    ┌───────▼───────┐                   │
│                    │    Chrome     │                   │
│                    │ (CDP :9222)   │                   │
│                    └───────────────┘                   │
└─────────────────────────────────────────────────────────┘
```

## Sanity Check

Run the sanity script to verify everything works:

```bash
./sanity.sh
```

This checks:
1. Chrome is installed
2. CDP can start/stop
3. CDP endpoint responds
4. Environment commands work

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "No CDP endpoint" in tests | Run `surf cdp start` first |
| Chrome not found | Install Google Chrome or Chromium |
| Port already in use | `surf cdp stop` then `surf cdp start` |
| Tests timeout | Ensure frontend is running at BASE_URL |
| surf-cli commands fail | Ensure Chrome extension is loaded |
| Sanity check fails | Run `./sanity.sh` for diagnostics |
