---
name: browser-testing
description: Browser automation, testing, and debugging using Chrome DevTools. Use when users want to take screenshots, test websites, debug UI, inspect network requests, check console errors, or automate browser interactions.
---

# Browser Testing

Browser automation via Chrome DevTools Protocol using chrome-devtools-mcp.

## Prerequisites

- **Bun**: `curl -fsSL https://bun.sh/install | bash`
- **uv**: Already installed

## Important: UID-Based Interactions

This tool uses **element UIDs from snapshots** for interactions (click, fill, hover), NOT CSS selectors.

**Workflow:**
1. Navigate to page
2. Take snapshot to get element UIDs
3. Use UIDs for click/fill/hover

## Usage

```bash
cd /Users/roy/.claude/skills/browser-testing
uv run python scripts/browser.py <command> [args]
```

## Commands

### Navigation

```bash
# Navigate to URL
uv run python scripts/browser.py navigate --url https://example.com

# Back/forward/reload
uv run python scripts/browser.py navigate --back
uv run python scripts/browser.py navigate --forward
uv run python scripts/browser.py navigate --reload --ignore-cache

# New page
uv run python scripts/browser.py new-page https://google.com

# List/select/close pages
uv run python scripts/browser.py list-pages
uv run python scripts/browser.py select-page 1 --bring-to-front
uv run python scripts/browser.py close-page 0

# Wait for text
uv run python scripts/browser.py wait-for "Success" --timeout 5000
```

### Debug

```bash
# Screenshot
uv run python scripts/browser.py screenshot --save-path ./shot.png
uv run python scripts/browser.py screenshot --full-page --save-path ./full.png

# Snapshot (get element UIDs for interactions)
uv run python scripts/browser.py snapshot
uv run python scripts/browser.py snapshot --verbose

# Eval JavaScript (must be function syntax)
uv run python scripts/browser.py eval "() => document.title"
uv run python scripts/browser.py eval "() => document.querySelectorAll('a').length"

# Console messages
uv run python scripts/browser.py list-console --types error,warn
uv run python scripts/browser.py get-console 123
```

### Input (requires UIDs from snapshot)

```bash
# Get UIDs first
uv run python scripts/browser.py snapshot
# Output: uid=1_3 link "Learn more" ...

# Then interact using UIDs
uv run python scripts/browser.py click 1_3
uv run python scripts/browser.py click 1_3 --dbl-click
uv run python scripts/browser.py fill 1_5 "test@example.com"
uv run python scripts/browser.py hover 1_2

# Form filling
uv run python scripts/browser.py fill-form --elements '[{"uid":"1_5","value":"test"},{"uid":"1_6","value":"pass"}]'

# Keyboard
uv run python scripts/browser.py press-key Enter
uv run python scripts/browser.py press-key "Control+A"
uv run python scripts/browser.py press-key "Control+Shift+R"

# Drag and drop
uv run python scripts/browser.py drag 1_10 1_20

# File upload
uv run python scripts/browser.py upload-file 1_15 ./document.pdf

# Dialog handling
uv run python scripts/browser.py handle-dialog accept
uv run python scripts/browser.py handle-dialog dismiss --prompt-text "input"
```

### Emulation

```bash
# Network throttling
uv run python scripts/browser.py emulate --network "Slow 3G"
uv run python scripts/browser.py emulate --network "Offline"
uv run python scripts/browser.py emulate --network "No emulation"

# CPU throttling (1-20, 1=normal)
uv run python scripts/browser.py emulate --cpu 4

# Geolocation
uv run python scripts/browser.py emulate --geo "37.7749,-122.4194"
uv run python scripts/browser.py emulate --geo clear

# Viewport resize
uv run python scripts/browser.py resize 1920 1080
uv run python scripts/browser.py resize 375 667
```

### Network

```bash
uv run python scripts/browser.py list-network
uv run python scripts/browser.py list-network --types xhr,fetch
uv run python scripts/browser.py get-network --reqid 5
```

### Performance

```bash
uv run python scripts/browser.py perf-start --reload --auto-stop
uv run python scripts/browser.py perf-stop
uv run python scripts/browser.py perf-analyze <insight-set-id> DocumentLatency
```

## Session Note

Each CLI command spawns a fresh browser. For multi-step workflows, use Python directly:

```python
from fastmcp import Client
from fastmcp.client.transports import StdioTransport
import asyncio

async def test_flow():
    transport = StdioTransport(command="bunx", args=["chrome-devtools-mcp@latest"])
    async with Client(transport) as client:
        await client.call_tool("navigate_page", {"type": "url", "url": "https://example.com"})
        r = await client.call_tool("take_snapshot", {})
        print(r.content[0].text)  # Get UIDs
        await client.call_tool("click", {"uid": "1_3"})

asyncio.run(test_flow())
```
