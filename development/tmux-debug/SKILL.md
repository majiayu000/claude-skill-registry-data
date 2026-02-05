---
name: tmux-debug
description: |
  This skill captures and analyzes tmux pane content for debugging.
  Triggers: "debug tmux", "capture tmux output", "check other session", "tmux pane content",
  "what's in that terminal", "inspect background process", "tmux scrollback".
  Captures screen content from tmux panes to debug sessions or monitor processes.
---

# Tmux Debug

Capture screen content from tmux panes to debug other terminal sessions, monitor background processes, or inspect command output.

## Commands

### List all panes
```bash
tmux list-panes -a -F '#{session_name}:#{window_index}.#{pane_index} #{pane_title}'
```

### Capture current pane
```bash
tmux capture-pane -p
```

```bash
# With ANSI colors
tmux capture-pane -p -e 
```

### Capture specific pane
```bash
tmux capture-pane -t 'session:window.pane' -p
```

### Capture with scrollback history
```bash
# Last 100 lines of scrollback
tmux capture-pane -p -S -100

# Entire scrollback buffer
tmux capture-pane -p -S - -E -
```

## Usage

1. First list panes to find the target: `tmux list-panes -a -F '...'`
2. Capture the pane content: `tmux capture-pane -t 'target' -p`
3. Analyze the output for errors, status, or relevant information

$ARGUMENTS
