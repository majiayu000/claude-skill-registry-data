---
name: ghostty-terminal-automation
description: Automate Ghostty terminal sessions via MCP. Use when you need to send commands to terminals, read terminal output, capture screenshots, resize windows, open new tabs/windows, or interact with TUI apps like Neovim, htop, or any CLI tool running in Ghostty.
---

# Ghostty Terminal Automation

Control Ghostty terminals programmatically via the MCP server. Built on the ghostty-automator library with Playwright-style ergonomics.

## Available MCP Tools

### `list_terminals`

List all open terminal surfaces. Returns IDs, titles, dimensions, focus state, and working directory.

```json
[
  {
    "id": "0x13604ba00",
    "title": "~/dev/project",
    "rows": 33,
    "cols": 135,
    "focused": true,
    "pwd": "/Users/bliss/dev/project"
  }
]
```

### `terminal`

Interact with a specific terminal. Single supertool with 18 actions.

**Required:** `terminal_id`, `action`

#### Input Actions

| Action | Params | Description |
|--------|--------|-------------|
| `send` | `text` | Send command + Enter |
| `type` | `text`, `delay_ms?` | Type text without Enter |
| `key` | `key`, `mods?` | Press key combination |

#### Mouse Actions

| Action | Params | Description |
|--------|--------|-------------|
| `click` | `x`, `y`, `button?`, `mods?` | Click at position |
| `double_click` | `x`, `y`, `button?` | Double-click |
| `drag` | `from_x`, `from_y`, `to_x`, `to_y`, `steps?` | Drag operation |
| `scroll` | `delta_y`, `delta_x?`, `mods?` | Scroll terminal |

#### Screen Actions

| Action | Params | Returns |
|--------|--------|---------|
| `read` | `screen_type?` | `{text, plain_text, cursor_x, cursor_y}` |
| `cells` | `screen_type?` | `{cells: [...], cursor_x, cursor_y, rows, cols}` |
| `screenshot` | `output_path` | `{path}` |

#### Waiting Actions (Critical for Automation!)

| Action | Params | Description |
|--------|--------|-------------|
| `wait_text` | `pattern`, `regex?`, `timeout_ms?` | Wait for text/regex to appear |
| `wait_prompt` | `prompt_pattern?`, `timeout_ms?` | Wait for shell prompt |
| `wait_idle` | `stable_ms?`, `timeout_ms?` | Wait for screen to stabilize |

#### Assertion Actions

| Action | Params | Description |
|--------|--------|-------------|
| `expect` | `text`, `timeout_ms?` | Assert text is present |
| `expect_not` | `text`, `timeout_ms?` | Assert text is NOT present |

#### Management Actions

| Action | Params | Description |
|--------|--------|-------------|
| `focus` | - | Bring window to front |
| `close` | - | Close terminal |
| `resize` | `rows?`, `cols?` | Change dimensions |

### `new_terminal`

Create a new Ghostty window or tab.

| Param | Type | Description |
|-------|------|-------------|
| `type` | `"window"` or `"tab"` | Type of terminal to create |
| `command` | `list[str]?` | Optional command to run |

Returns: `{terminal_id, title, pwd}`

## Core Workflow

1. **Discover terminals** with `list_terminals`
2. **Read current state** with `action="read"` to see what's on screen
3. **Send commands** with `action="send"`
4. **Wait for completion** with `action="wait_text"` or `action="wait_prompt"`
5. **Verify results** by reading again or taking a screenshot

## Examples

### Run a Command and Wait for Output

```
1. list_terminals                                    # Get terminal_id
2. terminal(id, action="send", text="npm test")      # Run command
3. terminal(id, action="wait_text", pattern="PASS")  # Wait for result
4. terminal(id, action="read")                       # Read output
```

### Press Keys

```
# Press Enter
terminal(id, action="key", key="Enter")

# Ctrl+C to interrupt
terminal(id, action="key", key="KeyC", mods="ctrl")

# Arrow keys for navigation
terminal(id, action="key", key="ArrowUp")

# Tab completion
terminal(id, action="key", key="Tab")

# Escape (exit modes in vim, etc)
terminal(id, action="key", key="Escape")
```

Key names follow W3C standard: `Enter`, `Tab`, `Escape`, `Backspace`, `Delete`, `Space`, `ArrowUp`, `ArrowDown`, `ArrowLeft`, `ArrowRight`, `Home`, `End`, `PageUp`, `PageDown`, `F1`-`F12`, `KeyA`-`KeyZ`, `Digit0`-`Digit9`.

### Type Without Executing

```
# Type partial input (no Enter)
terminal(id, action="type", text="git commit -m \"")

# Type slowly for effect
terminal(id, action="type", text="Hello", delay_ms=50)
```

### Wait for Shell Prompt

```
# After running a long command
terminal(id, action="send", text="npm install")
terminal(id, action="wait_prompt")  # Waits for $ or similar
terminal(id, action="send", text="npm start")
```

### Wait for Screen to Stabilize

```
# For streaming output or animations
terminal(id, action="send", text="curl https://example.com")
terminal(id, action="wait_idle", stable_ms=1000)  # Wait for 1s of no changes
```

### Assertions

```
# Assert success message appears
terminal(id, action="expect", text="Build successful")

# Assert no errors
terminal(id, action="expect_not", text="ERROR")
```

### Mouse Interactions

```
# Click at pixel position
terminal(id, action="click", x=100, y=200)

# Double-click to select word
terminal(id, action="double_click", x=100, y=200)

# Drag to select text
terminal(id, action="drag", from_x=50, from_y=100, to_x=200, to_y=100)

# Scroll down
terminal(id, action="scroll", delta_y=3)
```

### Get Styled Cell Data (for TUI inspection)

```
# Get cell-level data with colors and formatting
terminal(id, action="cells")

# Returns cells with: char, x, y, fg, bg, bold, italic, underline, etc.
```

### Screenshots

```
terminal(id, action="screenshot", output_path="/tmp/capture.png")
# Then use Read tool on /tmp/capture.png to view
```

### Create New Terminal

```
# New window
new_terminal(type="window")

# New tab with command
new_terminal(type="tab", command=["python", "-i"])
```

## Working with TUI Apps

### Neovim

```
1. terminal(id, action="send", text="nvim file.py")
2. terminal(id, action="wait_text", pattern="file.py")
3. terminal(id, action="key", key="KeyI")           # Enter insert mode
4. terminal(id, action="type", text="print('hello')")
5. terminal(id, action="key", key="Escape")
6. terminal(id, action="type", text=":wq")
7. terminal(id, action="key", key="Enter")
```

### htop / btop

```
1. terminal(id, action="send", text="htop")
2. terminal(id, action="wait_idle")                  # Wait for UI to render
3. terminal(id, action="screenshot", output_path="/tmp/htop.png")
4. terminal(id, action="key", key="KeyQ")           # Quit
```

## Python Client

For scripting, use the ghostty-automator library directly:

```python
from ghostty_automator import Ghostty

async with Ghostty.connect() as ghostty:
    # Get first terminal
    terminal = await ghostty.terminals.first()

    # Run command and wait for output
    await terminal.send("ls -la")
    await terminal.wait_for_text("package.json")

    # Assert text present
    await terminal.expect.to_contain("src/")

    # Take screenshot
    await terminal.screenshot("/tmp/result.png")
```

Sync API also available:

```python
from ghostty_automator.sync_api import Ghostty

with Ghostty.connect() as ghostty:
    terminal = ghostty.terminals.first()
    terminal.send("echo hello")
    terminal.wait_for_prompt()
```

## Tips

- **Always discover first**: Call `list_terminals` before assuming terminal IDs
- **Use wait actions**: Don't assume commands complete instantly
- **Read before sending**: Check screen state to understand context
- **Use `wait_prompt` after commands**: Ensures shell is ready for next command
- **Use `cells` for TUI inspection**: Get color and style information
- **Screenshot for verification**: Visual confirmation of complex operations
