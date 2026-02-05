---
name: tmux-orchestration
description: Control interactive terminal processes via tmux - launch CLI applications, send input, capture output, wait for completion. This skill should be used when tasks require interactive debugging (pdb, node inspect), REPL exploration, long-running observable processes, or spawning another Claude instance for independent analysis or second opinions.
---

# Tmux Orchestration

## Overview

Direct tmux control for interactive terminal processes. No wrappers, no dependencies beyond tmux itself.

**Prerequisite**: User must be in a tmux session. Ask them to run `tmux new-session -s shared` if not.

## When to Use

Use tmux orchestration when:
- **Interactive debugging** - Step through code with pdb/node inspect, observe state, decide next action
- **REPL exploration** - Iterative code refinement beyond simple execution
- **Another Claude instance** - Fresh perspective, specialized focus, or reasoning verification
- **Observable long-running processes** - Dev servers where logs need monitoring while working

Do NOT use when:
- Simple command execution suffices (use Bash directly)
- No interactivity needed (output is final, no decisions based on it)

## Core Commands

```bash
# Create pane (horizontal split), returns immediately
tmux split-window -h

# Create pane with command
tmux split-window -h "python3"

# Send text to pane (with Enter)
tmux send-keys -t 1 "print('hello')" Enter

# Send text without Enter
tmux send-keys -t 1 "partial input"

# Capture pane output
tmux capture-pane -t 1 -p

# Capture last N lines
tmux capture-pane -t 1 -p -S -20

# List panes (see what exists)
tmux list-panes

# Kill pane
tmux kill-pane -t 1

# Send Ctrl+C
tmux send-keys -t 1 C-c
```

## Pane Targeting

After `split-window`, new pane becomes active. Use `-t` to target specific panes:

- `-t 0` - pane 0 (usually the original)
- `-t 1` - pane 1 (first split)
- `-t session:window.pane` - fully qualified

Check current panes: `tmux list-panes -F "#{pane_index}: #{pane_current_command}"`

## Wait for Output to Stabilize

```bash
# Simple: just wait
sleep 2 && tmux capture-pane -t 1 -p

# Better: wait until output stops changing
LAST=""; for i in {1..30}; do
  CURRENT=$(tmux capture-pane -t 1 -p | tail -20)
  [ "$CURRENT" = "$LAST" ] && break
  LAST="$CURRENT"; sleep 0.5
done
tmux capture-pane -t 1 -p
```

## Critical Pattern: Launch Shell First

Direct command launch loses output on error (pane closes). Launch shell first:

```bash
# CORRECT
tmux split-window -h "zsh"
tmux send-keys -t 1 "python script.py" Enter

# WRONG - if script crashes, pane dies, output lost
tmux split-window -h "python script.py"
```

## Workflows

For detailed patterns, see [references/workflows.md](references/workflows.md).

**Interactive Debugging**: shell → start pdb → send n/s/p commands → capture state → decide next step

**Claude-to-Claude**: shell → `claude` → send focused prompt → wait → capture response → integrate

**REPL Exploration**: shell → start repl → send expression → capture → refine

## Session Setup

If user isn't in tmux, they need to start a session first:

```bash
# User runs in their terminal:
tmux new-session -s shared

# Then Claude can create panes they'll see
```

To check if in tmux: `[ -n "$TMUX" ] && echo "in tmux" || echo "not in tmux"`
