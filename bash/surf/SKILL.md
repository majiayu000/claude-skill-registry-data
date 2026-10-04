---
name: surf
description: Control Chrome browser via CLI for testing, automation, and debugging. Use when the user needs browser automation, screenshots, form filling, page inspection, network/CPU emulation, DevTools streaming, or AI queries via ChatGPT/Gemini/Perplexity/Grok/AI Studio.
---

# Surf Browser Automation

Control Chrome browser via CLI or Unix socket. Surf drives the user's real Chrome — sessions share the profile's cookies, logins, storage, downloads, history, and bookmarks.

## Reference files — read when the branch applies

- Command fails with `Socket connect failed` or native-messaging errors, or fresh install/WSL2 setup → read [references/troubleshooting.md](references/troubleshooting.md) before retrying.
- Controlling a browser on another machine (credentials, Tailnet, transfer limits) → read [references/remote.md](references/remote.md).
- Querying AI assistants through the browser (ChatGPT, Oracle jobs, Gemini, Perplexity, Grok, AI Studio) → read [references/ai-assistants.md](references/ai-assistants.md) first.
- Device/network emulation, network capture & HAR export, console/perf tracing, cookies, history, smoke tests, named workflows & playbooks, socket API → read [references/advanced.md](references/advanced.md).

## First Command for Independent Agents

Before the first browser command in each independent agent shell, choose a unique valid session name and ensure its target exists:

```bash
export SURF_SESSION="$(basename "$PWD" | sed 's/[^A-Za-z0-9._-]/-/g')"
surf session.ensure "$SURF_SESSION" about:blank
```

`session.ensure` is idempotent. It creates a missing session, reuses a live binding, and reopens a stale or closed tab. Keep `SURF_SESSION` set for every later tab-scoped command in that shell. Use a distinct worktree/directory name per agent; when agents share one directory, append a stable agent identifier. Use `surf session.info "$SURF_SESSION"` to inspect the target and queue state.

Each session owns one explicit tab and defaults to a separate unfocused window. Commands for the same tab are FIFO; different session tabs may run concurrently. Browser-wide writers wait for tab lanes to drain. `--no-wait` returns `tab_busy` or `browser_busy` immediately. On `tab_gone` or `session_epoch_stale`, run the exact command printed after `Recovery:`—normally `surf session.reopen <name>`. Use separate browser/profile instances and `SURF_SOCKET` values only when hard isolation is required.

```bash
# Explicit form when an environment variable is inconvenient
surf --session research go "https://example.com"
surf --session research read

# Inspect bindings and scheduler state
surf session.list --refresh
surf session.info research --refresh
```

## CLI Quick Reference

```bash
surf --help                    # Basic help
surf <group>                   # Group help (tab, scroll, page, wait, dialog, emulate, form, perf, ai)
surf --help-full               # All commands
surf --find <term>             # Search tools
surf --help-topic <topic>      # Topic guide (refs, semantic, frames, devices, windows)
```

## Core Workflow

```bash
# 1. Navigate to page
surf navigate "https://example.com"

# 2. Read page to get element refs
surf page.read

# 3. Click by ref or coordinates
surf click --ref "e1"
surf click --x 100 --y 200

# 4. Type text
surf type --text "hello"

# 5. Full-page screenshot
surf screenshot --full-page --output /tmp/shot.png

# Inspect animation/style changes as JSON
surf animate-audit --selector ".thing" --duration 2000 --fps 10
```

## Tab Management

```bash
surf tab.list
surf tab.new "https://google.com"
surf tab.switch 12345
surf tab.close 12345
surf tab.move 12345 --to-window 67890
surf tab.reload                # Reload current tab

# Named tabs (aliases)
surf tab.name myapp            # Name current tab
surf tab.switch myapp          # Switch by name
surf tab.named                 # List named tabs
surf tab.unname myapp          # Remove name

# Tab groups
surf tab.group                 # Create/add to tab group
surf tab.ungroup               # Remove from group
surf tab.groups                # List all tab groups
```

## Window Management

```bash
surf window.list                              # List all windows
surf resize 1280 720                         # Resize current browser window
surf resize 1280                             # Set current window width only
surf window.list --tabs                       # Include tab details
surf window.new                               # New window
surf window.new --url "https://example.com"   # New window with URL
surf window.new --incognito                   # New incognito window
surf window.new --unfocused                   # Don't focus new window
surf window.focus 12345                       # Focus window by ID
surf window.close 12345                       # Close window
surf window.resize --id 123 --width 1920 --height 1080
surf window.resize --id 123 --state maximized # States: normal, minimized, maximized, fullscreen
```

## Input Methods

```bash
# CDP method (real events) types at the current focus
surf type --text "hello"
surf click --x 100 --y 200

# Selector/ref targets use frame-aware DOM input
surf type "hello" --into "#input"
surf type "hello" --ref e5

# Keys
surf key Enter
surf key "cmd+a"
surf key.repeat --key Tab --count 5           # Repeat key presses

# Hover and drag
surf hover --ref e5
surf drag --from-x 100 --from-y 100 --to-x 200 --to-y 200
```

## Page Inspection

```bash
surf page.read                 # Accessibility tree with refs + page text
surf page.read --no-text       # Interactive elements only (no text content)
surf page.read --ref e5        # Get specific element details
surf page.read --depth 3       # Limit tree depth
surf page.read --compact       # Minimal output for LLM efficiency
surf page.read --max-bytes 2000 # Cap visible text at a UTF-8 byte boundary
surf page.text                 # Plain text content only
surf page.html --strip-scripts # Rendered HTML without scripts
surf page.save --selector "#artifact" --strip-scripts --output page.html # Save one static element
surf page.state                # Modals, loading state, scroll info
surf animate-audit --selector ".thing" --duration 2000 --fps 10  # JSON animation timeline
```

### Export Rendered HTML

Use `page.html` when the user wants a static copy of the current rendered DOM (works for Claude artifact pages and ordinary web pages):

```bash
surf page.save --output page.html                                # Save the active page as HTML
surf wait.dom --stable 500
surf page.html --selector "#artifact" --strip-scripts > artifact.html
```

`--selector <css>` exports its matching element only (a miss fails with an error). `--strip-scripts` removes scripts from exported markup without changing the page. Without `--selector`, `page.html` exports the whole document with its doctype, and it exports the selected frame when `frame.switch` is active. Use `page.read` first when you need refs or visible text.

## Semantic Element Location

Find and act on elements by role, text, or label instead of refs:

```bash
surf locate.role button --name "Submit" --action click
surf locate.role textbox --name "Email" --action fill --value "test@example.com"
surf locate.role link --all                    # Return all matches
surf locate.text "Sign In" --action click
surf locate.text "Accept" --exact --action click
surf locate.label "Username" --action fill --value "john"
```

**Actions:** `click`, `fill`, `hover`, `text` (get text content)

## Text Search

```bash
surf search "login"                    # Find text in page
surf search "Error" --case-sensitive   # Case-sensitive
surf search "button" --limit 5         # Limit results
surf find "login"                      # Alias for search
```

## Element Inspection

```bash
surf element.styles e5                 # Get computed styles by ref
surf element.styles ".card"            # Or by CSS selector
# Returns: font, color, background, border, padding, bounding box
```

## Scrolling

```bash
surf scroll down 800           # Scroll down 800px
surf scroll up 400             # Scroll up 400px
surf scroll bottom             # Scroll to bottom (dot form scroll.bottom also works)
surf scroll top                # Scroll to top
surf scroll.to --ref e5        # Scroll element into view
surf scroll.info               # Get scroll position
```

## Waiting

```bash
surf wait 2                    # Wait 2 seconds
surf wait.element ".loaded"    # Wait for element
surf wait.network              # Wait for network idle
surf wait.url "/success"       # Wait for URL pattern
surf wait.dom --stable 100     # Wait for DOM stability
surf wait.load                 # Wait for page load complete
```

## Dialog Handling

```bash
surf dialog.info               # Get current dialog type/message
surf dialog.accept             # Accept (OK)
surf dialog.accept --text "response"  # Accept prompt with text
surf dialog.dismiss            # Dismiss (Cancel)
```

## Form Automation

```bash
surf page.read                 # Get element refs first

# Fill by ref
surf form.fill --data '[{"ref":"e1","value":"John"},{"ref":"e2","value":"john@example.com"}]'

# Checkboxes: true/false
surf form.fill --data '[{"ref":"e7","value":true}]'

# Dropdown selection
surf select e5 "Option A"                    # By value (default)
surf select e5 "Option A" "Option B"         # Multi-select
surf select e5 --by label "Display Text"     # By visible label
surf select e5 --by index 2                  # By index (0-based)
```

## File Upload

```bash
surf upload --ref e5 --files "/path/to/file.txt"
surf upload --ref e5 --files "/path/file1.txt,/path/file2.txt"
```

## Iframe Handling

```bash
surf frame.list                # List frames with IDs
surf frame.switch --selector "#payment-iframe"
surf frame.switch --name "checkout"
surf frame.switch --index 0    # First iframe
surf frame.main                # Return to main frame
surf frame.js "return document.title" --id "FRAME_ID"

# After frame.switch, subsequent commands target that frame:
surf frame.switch --selector "#payment-iframe"
surf page.read                 # Reads iframe content
surf click --selector "#pay"   # Clicks in iframe
surf frame.main                # Back to main page
```

## JavaScript Execution

```bash
surf js "return document.title"
surf js "document.querySelector('.btn').click()"
```

## Screenshots

```bash
surf screenshot                           # Auto-saves to /tmp/surf-snap-*.png
surf screenshot --output /tmp/shot.png    # Save to specific file
surf screenshot --selector ".card"        # Element only
surf screenshot --full-page               # Full page scroll capture
surf screenshot --full-page /tmp/full.png # Full page saved to path
surf screenshot --no-save                 # Return base64 only, don't save file
```

## Multi-Step: `surf do`

Execute multi-step automation as one command with smart auto-waits — instead of 6-8 separate CLI calls with LLM orchestration between each, a workflow executes deterministically. Faster, cheaper, more reliable.

```bash
surf do 'go "https://example.com" | click e5 | screenshot'
surf do 'go "https://example.com/login" | type "user@example.com" --selector "#email" | type "pass" --selector "#password" | click --selector "button[type=submit]"'
surf batch --actions '[{"type":"frame.switch","index":0},{"type":"click","selector":"#pay"}]'
surf do 'go "url" | click e5' --dry-run   # Validate without executing
```

For reusable named workflows (JSON files with args, loops, step outputs) and site playbooks, read [references/advanced.md](references/advanced.md).

## Error Diagnostics

```bash
# Auto-capture screenshot + console on failure
surf wait.element ".missing" --auto-capture --timeout 2000
# Saves to /tmp/surf-error-*.png
```

## Common Options

```bash
--session <name>      # Target a durable named session (or set SURF_SESSION)
--tab-id <id>         # Target a specific tab
--window-id <id>      # Target a specific window
--no-wait             # Return tab_busy/browser_busy instead of queueing
--json                # Raw JSON including target metadata
--auto-capture        # Screenshot + console on error
--timeout <ms>        # Override default timeout
```

## Tips

1. **First CDP operation is slow** (~5-8s) - debugger attachment overhead, subsequent calls fast
2. **Use refs from page.read** for reliable element targeting over CSS selectors
3. **JS method for contenteditable** - Modern editors (ChatGPT, Claude, Notion) need `--method js`
4. **Named tabs for workflows** - `tab.name app` then `tab.switch app`
5. **Auto-capture for debugging** - `--auto-capture` saves diagnostics on failure
6. **Use `surf do` for multi-step tasks** - Reduces token overhead and improves reliability; `--dry-run` validates first
7. **Session first** - Set a unique `SURF_SESSION` and run `session.ensure` before the first browser command in every independent agent shell
8. **Queue diagnostics** - `session.info` distinguishes the session's own tab queue, other active tabs, and browser-wide writers; use `--no-wait` for immediate busy errors
9. **Native host diagnostics** - On socket/native-host errors, read [references/troubleshooting.md](references/troubleshooting.md) and run `surf doctor` before guessing at reinstall steps
10. **HTML export** - Use `surf page.html > artifact.html` to save Claude artifacts or any rendered page as static HTML
11. **Animation capture** - Use `surf record --duration 2000 --fps 10 --output /tmp/anim.gif` when the agent needs to see motion; use `animate-audit` for numeric timelines and `perf-audit` for jank/layout-shift snapshots
12. **Semantic locators** - `locate.role`, `locate.text`, `locate.label` for more robust element finding
13. **Frame context** - Use `frame.switch` before interacting with iframe content
