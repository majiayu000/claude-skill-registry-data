---
name: cli-cdp
description: 'Chrome DevTools CLI for browser automation via shell commands. Use when interacting with web pages from the command line — navigating, clicking, filling forms, inspecting console/network, taking screenshots, or extracting page content. Triggers on: browse a page, automate Chrome, inspect console, check network requests, take a screenshot, fill a form, click a button.'
---

# Chrome DevTools CLI (cdp-cli)

CLI for Chrome DevTools Protocol. All list commands output **NDJSON** (one JSON
object per line) — grep/tail/jq friendly. Requires Chrome running with remote
debugging.

## Prerequisites

Chrome must be running with `--remote-debugging-port`:

```bash
cdp-cli launch                  # macOS: launches Chrome with debugging on :9223
```

Or start Chrome manually with `--remote-debugging-port=9222` and pass
`--cdp-url http://localhost:9222`.

## Page Identification

All commands taking `<page>` accept a **page ID** or a **title substring**.
Use `cdp-cli tabs` to discover pages.

```bash
cdp-cli tabs                    # List all open pages (NDJSON)
cdp-cli tabs | grep "example"   # Find by title
```

## Token-Conscious Defaults (Critical)

cdp-cli is designed to minimize token usage by default:

- **console** returns bare strings (not JSON objects) and only the last 10
  messages. Add `--with-type`, `--with-timestamp`, `--with-source` only when
  needed. Use `-v` for all fields.
- **snapshot** defaults to accessibility tree (`--format ax`) which is compact.
  Use `--format text` for plain text, `--format dom` for full DOM (heavy).
- **network** collects for only 0.1s by default. Increase with `--duration`.

**Strategy:** Start with defaults, add verbosity flags only when needed.

## Commands

### Page Management

```bash
cdp-cli tabs                            # List all pages (NDJSON)
cdp-cli new "https://example.com"       # Open new tab
cdp-cli new                             # Open empty tab
cdp-cli go "<page>" "https://url.com"   # Navigate to URL
cdp-cli go "<page>" back                # History back
cdp-cli go "<page>" forward             # History forward
cdp-cli go "<page>" reload              # Reload
cdp-cli close "<page>"                  # Close tab
```

### Snapshot & Evaluation

```bash
cdp-cli snapshot "<page>"               # Accessibility tree (default, compact)
cdp-cli snapshot "<page>" -f text       # Plain text content
cdp-cli snapshot "<page>" -f dom        # Full DOM tree (JSON, heavy)

cdp-cli eval "<page>" "document.title"  # Evaluate JS expression
cdp-cli eval "<page>" "Array.from(document.querySelectorAll('h1')).map(h => h.textContent)"
```

Use the accessibility tree to discover elements by role/name, then construct
CSS selectors for click/fill.

### Console

```bash
cdp-cli console "<page>"               # Last 10 messages, bare strings
cdp-cli console "<page>" -n 50         # Last 50 messages
cdp-cli console "<page>" --all         # All messages (or -n -1)
cdp-cli console "<page>" -t error      # Filter by type (log/error/warn/info)
cdp-cli console "<page>" -d 2          # Collect for 2 seconds
cdp-cli console "<page>" -i            # --inspect: expand nested objects/arrays
cdp-cli console "<page>" -v            # --verbose: all fields (type, timestamp, source)
cdp-cli console "<page>" --with-type   # Add type field only
cdp-cli console "<page>" --with-source # Add source location (url, line)
```

When truncated, stderr shows: `(N messages skipped. Use --tail M or --all to see more)`

### Network

```bash
cdp-cli network "<page>"               # Requests in last 0.1s (NDJSON)
cdp-cli network "<page>" -d 5          # Collect for 5 seconds
cdp-cli network "<page>" -t fetch      # Filter by type (xhr, fetch, script, etc)
cdp-cli network "<page>" -d 5 -t fetch # Combine filters
```

Filter results with grep:

```bash
cdp-cli network "<page>" | grep '"status":4'    # 4xx errors
cdp-cli network "<page>" | grep '"status":404'  # 404s specifically
```

### Input Automation

```bash
cdp-cli click "<page>" "button"                  # Click by CSS selector
cdp-cli click "<page>" "button" -d               # Double click
cdp-cli click "<page>" "button" -g               # --user-gesture: required for
                                                 # WebXR, fullscreen, and other
                                                 # activation-gated APIs
cdp-cli click "<page>" --node 42                 # Click by backend DOM node ID
cdp-cli click "<page>" "button" -w 5000          # Wait up to 5s for selector

cdp-cli fill "<page>" "user@example.com" "input[name='email']"
cdp-cli fill "<page>" "secret" "input[type='password']"

cdp-cli key "<page>" enter
cdp-cli key "<page>" tab
cdp-cli key "<page>" escape
```

### Screenshots

```bash
cdp-cli screenshot "<page>" screenshot.jpg       # Save JPEG (default)
cdp-cli screenshot "<page>" out.png -f png       # PNG format
cdp-cli screenshot "<page>" out.webp -f webp     # WebP format
cdp-cli screenshot "<page>" out.jpg -q 50        # Lower quality (0-100)
```

## Error Handling

All errors output NDJSON with `"error": true`:

```json
{ "error": true, "message": "Page not found: example", "code": "PAGE_NOT_FOUND" }
```

## Common Workflows

### Inspect and Interact

```bash
cdp-cli tabs | grep "example"                         # Find page
cdp-cli snapshot "example"                             # Get accessibility tree
# Identify selectors from the tree, then:
cdp-cli fill "example" "query" "input"
cdp-cli click "example" "button[type='submit']"
cdp-cli screenshot "example" result.jpg
```

### Debug Console Errors

```bash
cdp-cli console "localhost" -t error -d 10             # Errors over 10 seconds
cdp-cli console "localhost" -t error -v                # With full source location
```

### Monitor Network

```bash
cdp-cli network "localhost" -d 5 | grep '"status":4'   # Failed requests
cdp-cli network "localhost" -d 5 -t fetch               # API calls only
```

### Form Automation

```bash
cdp-cli new "http://localhost:3000/login"
cdp-cli fill "localhost" "user@example.com" "#email"
cdp-cli fill "localhost" "password123" "#password"
cdp-cli click "localhost" "button[type=submit]"
sleep 2
cdp-cli eval "localhost" "document.querySelector('.success')?.textContent"
```

## Global Options

| Option      | Default                 | Description                  |
| ----------- | ----------------------- | ---------------------------- |
| `--cdp-url` | `http://localhost:9223` | Chrome DevTools Protocol URL |
| `--help`    | —                       | Show help                    |
| `--version` | —                       | Show version                 |
