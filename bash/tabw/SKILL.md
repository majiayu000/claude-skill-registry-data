---
name: tabw
description: Use when the user asks to "continue every session", "send this to all windows", "/ar:tabw". Acts on Claude sessions across tmux windows; destructive to in-flight work, so it states what it will do before doing it.
allowed-tools: Bash(tmux *), Bash(uv *)
argument-hint: "[A,B:continue] or [all:escape] or [awaiting:continue]"
---

# Claude Session Writer

<purpose>

Execute actions on Claude Code sessions across tmux windows.

## Context

Current tmux sessions:

Run `tmux list-sessions` and read its output before choosing a session.

## Your Task

The user's request is the task description for everything below.

If no arguments provided, discover sessions first, then ask user what action to execute.

</purpose>

<safety>

## Safety Warning

This command sends input to tmux windows. Before executing:

1. **VERIFY TARGETS** - Always show which windows will receive commands
2. **PREFER IDLE SESSIONS** - Use `awaiting:` prefix to target only idle sessions
3. **TEST SINGLE FIRST** - Test with one window before batch operations
4. **HAVE ESCAPE READY** - `all:escape` can stop runaway operations

</safety>

<workflow>

## Workflow

1. **Discover** - Get window states with `tmux_list_windows(content_lines=100)`
2. **Filter** - Use WindowList methods to select targets
3. **Verify** - Show user which windows will be affected
4. **Execute** - Run action via `tmux_dangerous_batch_execute()`

## Data Flow: tmux_list_windows -> tmux_dangerous_batch_execute

The output of `tmux_list_windows()` flows directly into `tmux_dangerous_batch_execute()`:

```python
from autorun.tmux_utils import (
    get_tmux_utilities,
    tmux_list_windows,
    tmux_dangerous_batch_execute
)

tmux = get_tmux_utilities()

# Step 1: Get all windows with Claude status info
windows = tmux_list_windows(content_lines=100)

# Step 2: Filter using WindowList chainable methods
targets = (windows
    .claude_sessions()           # Only Claude Code sessions
    .prompting_user_for_input()  # Only those awaiting input
)

# Step 3: Verify targets before executing
print("Will send to:", [f"{w['session']}:{w['w']}" for w in targets])

# Step 4: Execute batch action
result = tmux_dangerous_batch_execute(tmux, 'continue', targets)
```

## WindowList Filter Methods

| Method | Description |
|--------|-------------|
| `.claude_sessions()` | Only windows with Claude Code running |
| `.prompting_user_for_input()` | Only windows awaiting user input |
| `.actively_generating()` | Only windows where Claude is working |
| `.in_mode('plan')` | Only windows in specific mode |
| `.thinking_enabled()` | Only windows with thinking mode on |
| `.filter(key=value)` | Generic filter on any field |

## Discovery Script

```bash
uv run --project "${CLAUDE_PLUGIN_ROOT}" python -c "
from autorun.tmux_utils import get_tmux_utilities, tmux_list_windows
import json

windows = tmux_list_windows(content_lines=100)
result = []
for i, w in enumerate(windows.claude_sessions()):
    result.append({
        'label': chr(65 + i),  # A, B, C...
        'session': w['session'],
        'window': w['w'],
        'target': f\"{w['session']}:{w['w']}\",
        'mode': w.get('claude_mode', 'default'),
        'is_active': w.get('is_active', False),
        'is_thinking': w.get('is_thinking', False),
        'prompt_type': w.get('prompt_type'),
        'title': w.get('title', '')
    })
print(json.dumps(result, indent=2))
"
```

## Action Syntax

| Syntax | Action | Description |
|--------|--------|-------------|
| `A:continue` | continue | Send "continue" to resume work |
| `A,B:escape` | escape | Stop generation (Escape key) |
| `all:continue` | continue | Send to ALL Claude sessions |
| `awaiting:continue` | continue | Send only to sessions awaiting input |
| `A:send Hello` | send | Send custom message "Hello" |
| `B:exit` | exit | Exit CLI cleanly (/exit) |
| `C:kill` | kill | Force exit (Ctrl+C twice) |
| `A:toggle_thinking` | toggle_thinking | Toggle thinking mode (Tab) |
| `B:cycle_mode` | cycle_mode | Cycle to next mode (Shift+Tab) |
| `C:set_mode plan` | set_mode | Set specific mode |

## Available Actions

| Action | Keys Sent | Use Case |
|--------|-----------|----------|
| `continue` | "continue" + Enter | Resume paused work |
| `escape` / `stop` | Escape | Stop active generation |
| `exit` | "/exit" + Enter | Clean exit |
| `kill` | Ctrl+C twice | Force exit |
| `toggle_thinking` | Tab | Toggle extended thinking |
| `cycle_mode` | Shift+Tab | Cycle default/plan/accept_edits |
| `set_mode <mode>` | Multiple Shift+Tab | Set specific mode |
| `send <text>` | text + Enter | Send custom message |

## Execution Scripts

### Continue on Awaiting Sessions

```bash
uv run --project "${CLAUDE_PLUGIN_ROOT}" python -c "
from autorun.tmux_utils import get_tmux_utilities, tmux_list_windows, tmux_dangerous_batch_execute

tmux = get_tmux_utilities()
windows = tmux_list_windows(content_lines=100)
targets = windows.claude_sessions().prompting_user_for_input()

print(f'Sending continue to {len(targets)} sessions:')
for w in targets:
    print(f'  - {w[\"session\"]}:{w[\"w\"]}')

result = tmux_dangerous_batch_execute(tmux, 'continue', targets)
print(f'\\nSuccess: {result[\"success_count\"]}, Failed: {result[\"failure_count\"]}')
"
```

### Stop All Active Generation

```bash
uv run --project "${CLAUDE_PLUGIN_ROOT}" python -c "
from autorun.tmux_utils import get_tmux_utilities, tmux_list_windows, tmux_dangerous_batch_execute

tmux = get_tmux_utilities()
windows = tmux_list_windows(content_lines=100)
targets = windows.claude_sessions().actively_generating()

print(f'Sending escape to {len(targets)} active sessions:')
for w in targets:
    print(f'  - {w[\"session\"]}:{w[\"w\"]}')

result = tmux_dangerous_batch_execute(tmux, 'escape', targets)
print(f'\\nSuccess: {result[\"success_count\"]}, Failed: {result[\"failure_count\"]}')
"
```

### Send Custom Message to Specific Target

```bash
uv run --project "${CLAUDE_PLUGIN_ROOT}" python -c "
from autorun.tmux_utils import get_tmux_utilities, tmux_dangerous_batch_execute

tmux = get_tmux_utilities()
# Replace 'main:5' with actual target
result = tmux_dangerous_batch_execute(tmux, 'send', 'main:5', message='git status')
print(f'Result: {result}')
"
```

### Set Mode on Multiple Sessions

```bash
uv run --project "${CLAUDE_PLUGIN_ROOT}" python -c "
from autorun.tmux_utils import get_tmux_utilities, tmux_list_windows, tmux_dangerous_batch_execute

tmux = get_tmux_utilities()
windows = tmux_list_windows(content_lines=100)
targets = windows.claude_sessions().in_mode('default')

print(f'Setting plan mode on {len(targets)} sessions')
result = tmux_dangerous_batch_execute(tmux, 'set_mode', targets, message='plan')
print(f'Success: {result[\"success_count\"]}, Failed: {result[\"failure_count\"]}')
"
```

</workflow>

<output_contract>

## Session Table Format

Present discovered Claude sessions as:

```
| # | Target  | Mode    | Status          | Thinking |
|---|---------|---------|-----------------|----------|
| A | main:3  | default | awaiting input  | no       |
| B | main:5  | plan    | working         | yes      |
| C | main:7  | bypass  | plan approval   | no       |
```

</output_contract>

<examples>

## Example Interactions

**Send continue to all idle sessions:**
```
User: awaiting:continue
Action: Send "continue" to all sessions with prompt_type != None and is_active == False
```

**Stop all active sessions:**
```
User: all:escape
Action: Send Escape to all Claude sessions to stop generation
```

**Send custom message to specific session:**
```
User: A:send git status
Action: Send "git status" to session A
```

**Set plan mode on multiple sessions:**
```
User: A,B,C:set_mode plan
Action: Cycle mode to "plan" on sessions A, B, C
```

## Quick Reference

```bash
# Discover sessions
/ar:tabs

# Send continue to idle sessions
/ar:tabw awaiting:continue

# Stop all active generation
/ar:tabw all:escape

# Exit all sessions
/ar:tabw all:exit
```

</examples>
