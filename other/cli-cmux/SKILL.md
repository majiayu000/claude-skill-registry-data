---
name: cli-cmux
description: 'Deep expertise in cmux — the terminal multiplexer with native browser views. Use when managing panes, reading terminal output, sending keystrokes, opening browser views, or manually testing web UIs and TUIs inside cmux. Triggers on: cmux, open a browser pane, split terminal, read screen, send keys, test this UI in cmux, preview in cmux.'
---

# cmux — Terminal Multiplexer with Native Browser

cmux manages terminal panes and browser views through a Unix socket CLI.
You are already running inside cmux — your current pane has env vars
`CMUX_WORKSPACE_ID` and `CMUX_SURFACE_ID` set automatically.

## Mental Model

```
window → workspace(s) → pane(s) → surface(s)
                                    ↑
                              terminal OR browser
```

- **Window**: OS window
- **Workspace**: A tab within a window (like tmux sessions)
- **Pane**: A visual split region
- **Surface**: The content inside a pane (terminal or browser); panes can have multiple surfaces as tabs

## Addressing

cmux uses **short refs** by default: `workspace:1`, `pane:2`, `surface:3`.
Most commands auto-target the caller's workspace/surface via env vars.

```bash
# Discover current layout
cmux identify            # What workspace/pane/surface am I in?
cmux list-panes          # Panes in current workspace
cmux list-workspaces     # All workspaces
```

## Core Operations

### Layout — Splits and Panes

```bash
# Create a new terminal pane (split from current)
cmux new-pane --direction right
cmux new-pane --direction down

# Create a browser pane
cmux new-pane --type browser --direction right --url http://localhost:3000

# Focus a pane
cmux focus-pane --pane pane:3

# Resize
cmux resize-pane --pane pane:2 -R --amount 20   # grow rightward
cmux resize-pane --pane pane:2 -D --amount 10   # grow downward
```

### Terminal I/O — Read and Send

```bash
# Read what's on screen in another pane
cmux read-screen --surface surface:2
cmux read-screen --surface surface:2 --scrollback --lines 100

# Send text (like typing)
cmux send --surface surface:2 "npm run dev"
cmux send --surface surface:2 $'\n'              # press Enter

# Send special keys
cmux send-key --surface surface:2 Enter
cmux send-key --surface surface:2 Up
cmux send-key --surface surface:2 Ctrl+C
```

### Browser — Navigate and Interact

```bash
# Open URL in an existing browser surface
cmux browser --surface surface:3 navigate http://localhost:3000

# Snapshot the DOM (interactive elements)
cmux browser --surface surface:3 snapshot --interactive

# Click, fill, type using CSS selectors
cmux browser --surface surface:3 click "button.submit"
cmux browser --surface surface:3 fill "input[name=email]" "test@example.com"
cmux browser --surface surface:3 type "input[name=search]" "query"

# Press keys, scroll
cmux browser --surface surface:3 press Enter
cmux browser --surface surface:3 scroll --dy 500

# Read state
cmux browser --surface surface:3 get url
cmux browser --surface surface:3 get title
cmux browser --surface surface:3 get text "h1"

# Wait for conditions
cmux browser --surface surface:3 wait --selector ".loaded"
cmux browser --surface surface:3 wait --load-state complete
cmux browser --surface surface:3 wait --text "Dashboard"
```

---

## Workflow: Testing a Web UI

The pattern: start the dev server in a terminal pane, open a browser pane
pointing at it, then interact via snapshot → act → re-snapshot.

```bash
# 1. Start dev server in a new pane
cmux new-pane --direction down
# note the surface ref from output, e.g. surface:2
cmux send --surface surface:2 "npm run dev"
cmux send-key --surface surface:2 Enter

# 2. Wait for server to be ready
# (read screen until you see the ready message)
cmux read-screen --surface surface:2

# 3. Open browser pane pointing at dev server
cmux new-pane --type browser --direction right --url http://localhost:3000
# note the browser surface ref, e.g. surface:3

# 4. Snapshot → interact → re-snapshot loop
cmux browser --surface surface:3 snapshot --interactive
cmux browser --surface surface:3 click "nav a[href='/settings']"
cmux browser --surface surface:3 wait --load-state complete
cmux browser --surface surface:3 snapshot --interactive

# 5. Fill a form
cmux browser --surface surface:3 fill "input[name=username]" "testuser"
cmux browser --surface surface:3 fill "input[name=password]" "secret"
cmux browser --surface surface:3 click "button[type=submit]"
cmux browser --surface surface:3 wait --text "Welcome"
cmux browser --surface surface:3 snapshot --interactive
```

### Snapshot Tips

- `--interactive` returns only interactive elements — much smaller output
- `--compact` reduces whitespace for smaller snapshots
- `--selector "main"` scopes to a region of the page
- `--max-depth 5` limits DOM tree depth
- Always re-snapshot after navigation or DOM mutations

## Workflow: Testing a TUI

The pattern: launch the TUI in a new pane, read-screen to observe, send/send-key to interact.

```bash
# 1. Launch the TUI
cmux new-pane --direction right
# note surface ref, e.g. surface:2
cmux send --surface surface:2 "my-cli-wizard"
cmux send-key --surface surface:2 Enter

# 2. Read → interact → read loop
cmux read-screen --surface surface:2
cmux send-key --surface surface:2 ArrowDown
cmux send-key --surface surface:2 ArrowDown
cmux send-key --surface surface:2 Enter
cmux read-screen --surface surface:2

# 3. Type text input
cmux send --surface surface:2 "my-project-name"
cmux send-key --surface surface:2 Enter
cmux read-screen --surface surface:2

# 4. Test cancellation
cmux send-key --surface surface:2 Ctrl+C
cmux read-screen --surface surface:2

# 5. Clean up
cmux send-key --surface surface:2 Ctrl+C
```

### TUI Tips

- Use `read-screen` (not `read-screen --scrollback`) for current viewport
- Add `--lines 50` with `--scrollback` to limit output size
- Send `Ctrl+C` to kill the TUI when done
- Read the screen after each interaction to confirm state changes

## Context Management

cmux interactions are context-expensive. Minimize round-trips:

1. **Batch related commands** — don't read-screen between every single keystroke
2. **Use `--interactive` and `--compact`** for browser snapshots
3. **Scope snapshots** with `--selector` when you only care about part of the page
4. **Delegate long test sessions to a Task subagent** — the subagent runs the
   full interaction loop and returns only findings

## Sidebar Metadata

cmux provides sidebar status, progress, and logging for visibility:

```bash
cmux set-status "phase" "testing" --icon "🧪"
cmux set-progress 0.5 --label "Running tests..."
cmux log "Found 3 issues" --level warn
cmux clear-progress
```

## Reference

For full command details, see:

- [reference/browser-commands.md](reference/browser-commands.md) — All browser subcommands
- [reference/terminal-io.md](reference/terminal-io.md) — Terminal read/send/key commands
- [reference/layout-commands.md](reference/layout-commands.md) — Pane, workspace, window management
