---
name: bdg-browser-debug
description: Browser debugging and telemetry via Chrome DevTools Protocol. Use when testing the Astro dev server, inspecting network requests, debugging console errors, capturing screenshots, or interacting with DOM elements on localhost:4321.
allowed-tools: Bash, Read
---

# bdg - Browser Debug Gateway

Browser telemetry via Chrome DevTools Protocol for testing the Astro dev server.

## Quick Start

```bash
# Start session on Astro dev server
bdg http://localhost:4321/

# Check status
bdg status

# Preview collected data
bdg peek

# Stop and save session
bdg stop
```

## Session Management

| Command | Description |
|---------|-------------|
| `bdg http://localhost:4321/` | Start session on dev server |
| `bdg status` | Show session status |
| `bdg stop` | Stop and save to `~/.bdg/session.json` |
| `bdg stop --kill-chrome` | Stop and close Chrome |
| `bdg cleanup` | Clean stale sessions |
| `bdg cleanup --aggressive` | Force kill all Chrome instances |

## Data Inspection

### Peek (non-destructive preview)
```bash
bdg peek                    # Summary of all data
bdg peek -n                 # Network requests only
bdg peek -c                 # Console messages only
bdg peek -d                 # DOM/A11y tree
bdg peek -f                 # Follow mode (like tail -f)
bdg peek --last 20          # Last 20 items
bdg peek -j                 # JSON output
```

### Network
```bash
bdg network list            # List all requests
bdg network list --failed   # Failed requests only
bdg network list --type XHR # Filter by type
bdg network headers         # Main document headers
bdg network headers <id>    # Specific request headers
bdg network getCookies      # List cookies
bdg network har             # Export as HAR file
```

### Console
```bash
bdg console -l              # List all messages
bdg console --level error   # Errors only
bdg console --level warning # Warnings only
bdg console -f              # Follow in real-time
bdg console --last 50       # Last 50 messages
```

### Details
```bash
bdg details request <id>    # Full request details
bdg details console <id>    # Full console message
```

## DOM Interaction

### Inspection
```bash
bdg dom a11y                # Accessibility tree
bdg dom a11y "button"       # Search a11y tree
bdg dom query "nav a"       # CSS selector query
bdg dom get "header"        # Get element structure
bdg dom get "article" --raw # Get raw HTML
```

### Actions
```bash
bdg dom click "button.submit"           # Click element
bdg dom fill "input[name=email]" "test" # Fill input
bdg dom submit "form"                   # Submit form
bdg dom pressKey "input" "Enter"        # Press key
bdg dom eval "document.title"           # Evaluate JS
```

### Screenshots
```bash
bdg dom screenshot ./shot.png           # Full page
bdg dom screenshot ./el.png -s "header" # Element only
```

## CDP Protocol Access

```bash
bdg cdp --list              # List 53 domains
bdg cdp --search cookie     # Search methods
bdg cdp --describe Network.getCookies  # Method details
bdg cdp Network.getCookies  # Execute CDP method
```

## Common Workflows

### Test page load performance
```bash
bdg http://localhost:4321/
# Browse the site...
bdg peek -n                 # Check network requests
bdg network list --failed   # Any failed requests?
bdg stop
```

### Debug console errors
```bash
bdg http://localhost:4321/
bdg console --level error   # Check for errors
bdg console -f              # Monitor in real-time
```

### Inspect accessibility
```bash
bdg http://localhost:4321/
bdg dom a11y                # Full a11y tree
bdg dom a11y "navigation"   # Find nav elements
```

### Capture visual state
```bash
bdg http://localhost:4321/
bdg dom screenshot ./screenshots/home.png
bdg dom screenshot ./screenshots/header.png -s "header"
```

## Options Reference

| Flag | Description |
|------|-------------|
| `-q, --quiet` | Minimal output for AI agents |
| `-j, --json` | JSON output (most commands) |
| `--headless` | No visible browser window |
| `-t, --timeout <s>` | Auto-stop after N seconds |
| `-p, --port <n>` | Chrome debug port (default: 9222) |
| `--debug` | Verbose logging |

## Output Files

- Session data: `~/.bdg/session.json`
- Chrome profile: `~/.bdg/chrome-profile/`
