---
name: zensical-debug
description: Debug and visually verify zensical sites with Chrome DevTools. Combines zensical development best practices with Chrome MCP port management. User-invocable with /zensical-debug.
user_invocable: true
---

# Zensical Debug Session

Starts a debugging session for visual verification of zensical sites using Chrome DevTools MCP.

## Startup Checklist

### 1. Check Chrome Debugging Ports

```bash
# Check which ports are in use
lsof -i :9222 -i :9223 -i :9224 -i :9225 2>/dev/null | grep LISTEN

# Find first available port
for port in 9222 9223 9224 9225; do
  if ! lsof -i :$port >/dev/null 2>&1; then
    echo "Available: $port"
    break
  fi
done
```

If no Chrome debugging instance is available:
```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 &
```

### 2. Check/Start Zensical Server

```bash
# Check if zensical is already running
if lsof -i :8000 >/dev/null 2>&1; then
  echo "Zensical server already running on :8000"
else
  echo "Starting zensical server..."
  source .venv/bin/activate
  zensical serve
fi
```

Server runs at `http://127.0.0.1:8000`

### 3. Connect and Verify

```python
# Navigate to the page
mcp__chrome-devtools__navigate_page(url="http://127.0.0.1:8000/")

# Take screenshot
mcp__chrome-devtools__take_screenshot()

# Hard refresh if CSS changed
mcp__chrome-devtools__navigate_page(type="reload", ignoreCache=True)
```

## Visual Verification Commands

```python
# Check all images
mcp__chrome-devtools__evaluate_script(function="""
() => {
  const images = document.querySelectorAll('img');
  return Array.from(images).map(img => ({
    src: img.src.split('/').pop(),
    displayed: img.offsetWidth + 'x' + img.offsetHeight,
    maxWidth: window.getComputedStyle(img).maxWidth
  }));
}
""")

# Check for horizontal overflow
mcp__chrome-devtools__evaluate_script(function="""
() => ({
  bodyWidth: document.body.scrollWidth,
  viewportWidth: window.innerWidth,
  overflow: document.body.scrollWidth > window.innerWidth
})
""")
```

## Troubleshooting

**"Browser is already running" or "Target closed" errors**
```bash
# Remove stale Chrome profile locks
rm -f ~/.cache/chrome-devtools-mcp/chrome-profile/SingletonLock \
      ~/.cache/chrome-devtools-mcp/chrome-profile/SingletonSocket \
      ~/.cache/chrome-devtools-mcp/chrome-profile/SingletonCookie
```
Then retry `list_pages` - the MCP will start a fresh browser instance.

## Remember

- **CSS changes require server restart** (Ctrl+C, then `zensical serve`)
- **Always hard refresh** after CSS changes: `navigate_page(type="reload", ignoreCache=True)`
- **Only one agent per debugging port** - check ports before connecting
- **MCP manages its own Chrome** - Don't manually start Chrome; just call `list_pages` to initialize
