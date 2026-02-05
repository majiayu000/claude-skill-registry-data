---
name: tmux-orchestrator
description: This skill should be used when orchestrating tmux sessions for multi-component development workflows. Use when creating complex multi-window, multi-pane tmux layouts via the Bash tool, especially for projects requiring simultaneous backend/frontend development, microservices, or parallel task execution. This skill provides patterns for session creation, pane management, and command orchestration using the user's custom tmux configuration.
---

# Tmux Orchestrator

## Overview

This skill enables orchestration of tmux sessions through programmatic tmux commands via the Bash tool. It provides patterns for creating multi-window, multi-pane development environments suitable for complex projects requiring simultaneous work on multiple components.

The user has a custom tmux configuration with non-standard keybindings. Reference `references/keybindings.md` for the full configuration details.

## Core Concepts

### Session Structure

A tmux session consists of:
- **Session**: Top-level container (e.g., "project-dev")
- **Windows**: Tabs within a session (e.g., "backend", "frontend", "logs")
- **Panes**: Split sections within a window (side-by-side or stacked)

### Pane Naming Convention

Panes are numbered starting from 1 (due to user's base-index configuration):
- `session:window.1` - First pane in window
- `session:window.2` - Second pane in window
- And so on

### Split Types

**Important**: tmux split naming can be counterintuitive:
- `-h` (horizontal split) creates a **vertical divider** resulting in side-by-side panes
- `-v` (vertical split) creates a **horizontal divider** resulting in stacked panes

## Creating Sessions via Bash Tool

### Basic Pattern

```bash
# Check if session exists
tmux has-session -t session-name 2>/dev/null

# Create new session with first window
tmux new-session -d -s session-name -n window-name -c /path/to/dir

# Split panes
tmux split-window -h -t session-name:window-name -c /path/to/dir  # Side-by-side
tmux split-window -v -t session-name:window-name -c /path/to/dir  # Stacked

# Create additional windows
tmux new-window -t session-name -n second-window -c /path/to/other-dir

# Send commands to specific panes
tmux send-keys -t session-name:window-name.1 "command here" C-m

# Select default window
tmux select-window -t session-name:first-window

# Attach (use os.execvp in scripts, or direct command in bash)
tmux attach-session -t session-name
```

### Example: Two-Component Project

```bash
# Create session with backend window
tmux new-session -d -s myproject -n backend -c /path/to/backend
tmux split-window -h -t myproject:backend -c /path/to/backend

# Create frontend window
tmux new-window -t myproject -n frontend -c /path/to/frontend
tmux split-window -h -t myproject:frontend -c /path/to/frontend

# Optional: Send startup commands
tmux send-keys -t myproject:backend.1 "npm run dev" C-m
tmux send-keys -t myproject:frontend.1 "npm start" C-m

# Select backend window by default
tmux select-window -t myproject:backend

# Attach
tmux attach-session -t myproject
```

## Common Patterns

### Pattern 1: Editor + Terminal Layout

Single window with editor on left, terminal on right:

```bash
tmux new-session -d -s dev -n main -c /path/to/project
tmux split-window -h -t dev:main -c /path/to/project
tmux send-keys -t dev:main.1 "nvim" C-m
tmux attach-session -t dev
```

### Pattern 2: Multi-Service Development

Multiple windows, one per service:

```bash
SESSION="services"

# API service
tmux new-session -d -s "$SESSION" -n api -c /path/to/api
tmux split-window -h -t "$SESSION:api" -c /path/to/api
tmux send-keys -t "$SESSION:api.1" "go run main.go" C-m
tmux send-keys -t "$SESSION:api.2" "go test -v ./..." C-m

# Frontend service
tmux new-window -t "$SESSION" -n frontend -c /path/to/frontend
tmux send-keys -t "$SESSION:frontend" "npm run dev" C-m

# Database/logs
tmux new-window -t "$SESSION" -n infra -c /path/to/project
tmux send-keys -t "$SESSION:infra" "docker compose up" C-m

tmux select-window -t "$SESSION:api"
tmux attach-session -t "$SESSION"
```

### Pattern 3: Three-Pane Development

Editor + two terminals in same window:

```bash
tmux new-session -d -s dev -n main -c /path/to/project
tmux send-keys -t dev:main "nvim" C-m

# Split right
tmux split-window -h -t dev:main -c /path/to/project

# Split bottom right
tmux split-window -v -t dev:main -c /path/to/project

# Result: Editor on left, two terminals stacked on right
tmux attach-session -t dev
```

## Using Existing Tools

The user has shell aliases and scripts for tmux management. Leverage these when appropriate:

### Shell Aliases

- `tma session-name` - Attach to session
- `tmn session-name` - Create new session
- `tml` - List sessions
- `tmk session-name` - Kill session
- `tms` - Interactive session manager (fzf-based)
- `tmd` - Create 3-pane dev session automatically

### When to Use Existing Tools vs Custom Sessions

- Use `tmd` for simple single-project development (creates nvim + 2 terminals)
- Use custom tmux commands for multi-component projects requiring specific layouts
- Use `tms` to list/switch between sessions interactively

## Session Management

### Check Session Exists

```bash
if tmux has-session -t session-name 2>/dev/null; then
    echo "Session exists"
    tmux attach-session -t session-name
else
    # Create session
fi
```

### List Running Sessions

```bash
tmux list-sessions
# Or use alias
tml
```

### Kill Session

```bash
tmux kill-session -t session-name
# Or use alias
tmk session-name
```

## Sending Commands to Panes

### Basic Command

```bash
tmux send-keys -t session:window.pane "command" C-m
```

The `C-m` sends a carriage return (Enter key).

### Examples

```bash
# Send to first pane of backend window
tmux send-keys -t myproject:backend.1 "npm run dev" C-m

# Send to specific pane without executing (no C-m)
tmux send-keys -t myproject:frontend.2 "docker compose up -d"

# Send multiple commands
tmux send-keys -t myproject:backend.1 "cd src" C-m
tmux send-keys -t myproject:backend.1 "npm install" C-m
tmux send-keys -t myproject:backend.1 "npm run dev" C-m
```

## Working Directory Handling

All panes default to opening in the specified directory (`-c` flag). The user's tmux config is set to preserve the current path when creating new panes/windows.

```bash
# Window opens in /path/to/backend
tmux new-window -t session -n backend -c /path/to/backend

# This pane also opens in /path/to/backend (inherits from window)
tmux split-window -h -t session:backend -c /path/to/backend

# Override path for specific pane
tmux split-window -h -t session:backend -c /path/to/different/dir
```

## Session Persistence

The user has tmux-resurrect and tmux-continuum plugins:

- Sessions auto-save every 15 minutes
- Sessions survive system restarts
- No need to recreate sessions manually after reboot

Once a session is created, it will persist across reboots via the continuum plugin.

## Navigation Reference

Users navigate tmux with these keybindings (from `references/keybindings.md`):

- **Switch windows**: `Shift + Left/Right` (no prefix)
- **Switch panes**: `Alt + Arrow Keys` (no prefix)
- **Prefix key**: `Ctrl+a` (not the default `Ctrl+b`)

## Template Script

See `scripts/session-template.sh` for a complete example bash script demonstrating session creation patterns. This script can be adapted for specific projects.

## Best Practices

1. **Check for existing sessions** before creating to avoid duplicates
2. **Use descriptive window names** that indicate purpose (backend, frontend, logs, etc.)
3. **Send commands after pane creation**, not during creation, for reliability
4. **Select a default window** before attaching to control which window appears first
5. **Use full paths** for working directories (no `~` expansion needed)
6. **Preserve session names** across recreations for consistency with resurrect/continuum
7. **Leverage existing tools** (`tms`, `tmd`) when they fit the use case

## Resources

### scripts/session-template.sh

Generic bash script template demonstrating how to create multi-window, multi-pane sessions. Shows:
- Session existence checking
- Window creation
- Pane splitting
- Command sending
- Session attachment

Adapt this template for project-specific session creation scripts.

### references/keybindings.md

Complete reference of the user's custom tmux configuration including:
- Custom prefix key (`Ctrl+a`)
- Pane navigation (`Alt + arrows`)
- Window switching (`Shift + arrows`)
- All split, resize, and management keybindings
- Available shell aliases
- Plugin information (resurrect, continuum, etc.)

Load this reference when users ask about navigation or keybindings, or when debugging tmux behavior.
