---
name: tmux-test
description: Test klaude-code interactively using tmux with synchronous task completion. Use when testing UI features, verifying changes, or debugging interactive behavior. Eliminates polling/sleep by using KLAUDE_TEST_SIGNAL for precise synchronization.
---

# tmux-test

Test klaude-code in an interactive tmux session with synchronous task completion.

## Quick Start

```bash
# Create session and start klaude with signal
tmux new-session -d -s test -x 120 -y 30
tmux send-keys -t test 'KLAUDE_TEST_SIGNAL=done uv run klaude' Enter
sleep 3  # Wait for startup only

# Send request and wait for completion (no polling needed)
tmux send-keys -t test 'your prompt here' Enter
tmux wait-for done  # Blocks until task completes

# Capture output
tmux capture-pane -t test -p -S -50

# Cleanup
tmux kill-session -t test
```

## Key Points

- `KLAUDE_TEST_SIGNAL=<channel>`: Environment variable that enables task completion signaling
- `tmux wait-for <channel>`: Blocks until the signal is sent (task completes)
- Signal is only sent when main agent task finishes (not sub-agents)
- Use `-S -N` with capture-pane to get N lines of scrollback history

## Common Patterns

### Multiple Sequential Requests

```bash
for prompt in "request 1" "request 2"; do
  tmux send-keys -t test "$prompt" Enter
  tmux wait-for done
  tmux capture-pane -t test -p -S -30
done
```

### Capture Full Output

```bash
tmux capture-pane -t test -p -S -  # Entire scrollback
```
