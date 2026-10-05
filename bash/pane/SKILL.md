---
name: pane
description: "Open a new tmux pane in the current session. Optionally launch claude with an initial command. TRIGGER when the user says \"new pane\", \"open a pane\", \"split pane\", \"another terminal\", \"new window\", \"side by side\", or any request to open a parallel terminal or claude session."
argument-hint: "[claude] [/command args...]"
---

# Pane — Open New tmux Pane

**Arguments**: $ARGUMENTS

## Step 1: Parse Arguments

Parse the arguments into:
- **Mode**: `shell` (no args) or `claude` (first arg is "claude")
- **Initial command**: everything after "claude" (optional, e.g., `/start-work LIFE-1.2`)

Examples:
- `/pane` → mode=shell, no initial command
- `/pane claude` → mode=claude, no initial command
- `/pane claude /start-work LIFE-1.2` → mode=claude, initial command="/start-work LIFE-1.2"

## Step 2: Detect tmux Session

```bash
echo "${TMUX:-NOT_IN_TMUX}"
```

If not in tmux, tell the user: "Not in a tmux session. Use `tmux` to start a session first."

Get the current session name:
```bash
tmux display-message -p '#{session_name}'
```

## Step 3: Create New Pane

Split the current window horizontally (side by side):
```bash
tmux split-window -h -c "$(pwd)"
```

## Step 4: Launch (if claude mode)

If mode is `claude`:
```bash
tmux send-keys "claude" Enter
```

If there's also an initial command, wait briefly then send it:
```bash
sleep 2
tmux send-keys "[initial command]" Enter
```

## Step 5: Confirm

```
Pane opened
===========
Mode:    [shell / claude]
Command: [initial command or "none"]

Use Ctrl+B then arrow keys to switch between panes.
```

## Rules

- **Must be in tmux** — this skill only works inside a tmux session
- **Uses split-window** — creates a side-by-side pane, not a new window
- **Sleep before initial command** — claude needs time to start before receiving slash commands
- **No orchestration required** — this is a pure tmux convenience skill
