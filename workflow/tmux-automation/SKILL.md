---
name: tmux-automation
description: Drive CLI tests inside isolated tmux/byobu sessions with ai-monitor integration. Use when asked to "test this CLI", "run it in tmux", "automate a terminal session", "capture the output of an interactive command", "send keystrokes to a session", or to exercise a plugin or terminal app without touching the current session. Covers session lifecycle, keystroke control, output capture, and autonomous monitoring.
---

# Automated CLI Testing with Session Management

<purpose>

**autorun-specific procedures** (read the one you need, not both):
`references/session-management.md` creates, lists, and cleans up isolated
sessions, including the rule that cleanup only ever touches names starting with
`autorun-test`. `references/isolated-testing.md` runs a command inside the
dedicated `autorun-test` session so the caller's own session is never touched.

This skill provides comprehensive capabilities for automated testing of CLI applications, plugins, and terminal workflows using tmux/byobu sessions with full ai-monitor integration. Perfect for testing Claude Code plugins, command-line tools, and automated workflows.

</purpose>

<commands>

## Core Commands

### Session Management
- `byobu new-session -d -s <session-name>` - Create new detached session
- `byobu list-sessions` - List all active sessions
- `byobu attach-session -t <session-name>` - Attach to existing session
- `byobu detach-session` - Detach from session (F6)
- `byobu kill-session -t <session-name>` - Terminate session
- `tmux list-sessions` - List tmux sessions

### Window Management
- `byobu new-window -t <session-name>` - Create new window
- `byobu list-windows -t <session-name>` - List windows in session
- `byobu kill-window -t <session-name>:<window-index>` - Kill specific window
- `byobu select-window -t <session-name>:<window-index>` - Select window

### Input and Output Control
- `byobu send-keys -t <session-name> <keys>` - Send keystrokes to window
- `byobu send-keys -t <session-name> C-m` - Send Enter/Return key
- `byobu send-keys -t <session-name> C-c` - Send Ctrl+C interrupt
- `byobu capture-pane -t <session-name>` - Capture window output
- `byobu capture-pane -t <session-name> -p -S -<lines>` - Capture last N lines

### Tmux Commands (direct)
- `tmux new-session -d -s <session-name>` - Create new detached tmux session
- `tmux list-sessions` - List all tmux sessions
- `tmux attach-session -t <session-name>` - Attach to tmux session
- `tmux detach` - Detach from tmux session

## Specific Keystroke Commands

### Control Sequences
- `C-c` - Ctrl+C (interrupt/stop current command)
- `C-m` - Ctrl+M (Enter/Return)
- `C-d` - Ctrl+D (EOF/end of input)
- `C-l` - Ctrl+L (clear screen)
- `C-a` - Ctrl+A (tmux prefix, then command)
- `C-z` - Ctrl+Z (suspend current process)
- `Tab` - Tab completion
- `Esc` - Escape key

### Byobu Specific Keys
- `F2` - Create new window
- `Shift+F2` - Split window horizontally
- `Ctrl+F2` - Split window vertically
- `F3` - Previous window
- `F4` - Next window
- `F5` - Reload profile
- `F6` - Detach session
- `F7` - Search scrollback buffer
- `F8` - Enter scrollback mode
- `F9` - Configure byobu
- `Shift+F3`/`Shift+F4` - Move window left/right
- `Ctrl+F3`/`Ctrl+F4` - Focus pane left/right

### Tmux Prefix Commands (default Ctrl+B)
- `Ctrl+B c` - Create new window
- `Ctrl+B &` - Kill current window
- `Ctrl+B ,` - Rename window
- `Ctrl+B n` - Next window
- `Ctrl+B p` - Previous window
- `Ctrl+B %` - Split window horizontally
- `Ctrl+B "` - Split window vertically
- `Ctrl+B o` - Switch panes
- `Ctrl+B d` - Detach session
- `Ctrl+B s` - List sessions

</commands>

<integrations>

## AI-Monitor Integration

The ai_monitor.py in autorun provides comprehensive tmux monitoring and automation:

### Core AI-Monitor Functions
```python
# Start monitoring a session
start_monitor(session_id, prompt="Continue working", stop_marker="COMPLETE", max_cycles=5)

# Stop monitoring
stop_monitor(session_id)

# Check if monitor is running
check_monitor(session_id)
```

### AI-Monitor Capabilities
- **Session Discovery**: Automatically finds tmux sessions and windows
- **Content Monitoring**: Tracks window content changes and detects meaningful updates
- **Change Detection**: Filters out minor changes (echoes) vs. substantial content updates
- **Automatic Re-prompting**: Sends continuation prompts when idle (configurable intervals)
- **Stop Marker Detection**: Automatically stops when specific completion markers appear
- **Cycle Management**: Limits number of re-prompt cycles to prevent infinite loops
- **Window Management**: Can target specific windows for monitoring and interaction

## autorun Command Integration

autorun provides convenient commands for tmux session automation:

### Session Discovery
- `/ar:tabs` - Discover and manage all Claude sessions across tmux windows
  - Interactive table showing session status (working, awaiting input, etc.)
  - Batch operations: `all:continue`, `awaiting:status`, `A:pwd, B:ls`
  - AI-powered session analysis (uses Claude SDK when available)

### Session Management
- `/ar:tmux` or `/ar:tm` - Create and manage isolated tmux sessions
  - `create <name>` - Create new isolated session
  - `list` - List all sessions with health status
  - `cleanup` - Remove sessions older than 1 hour

### Testing Automation
- `/ar:ttest` or `/ar:tt` - Automated CLI testing in isolated sessions
  - Tests basic functionality, help system, custom commands
  - Session killed after each test (try/finally); long-running commands are not auto-killed
  - Clean session isolation

### Related Documentation
- `skills/tabs/SKILL.md` + `commands/tabs-exec` - Session discovery (`/ar:tabs`)
- `commands/tmux.md` - Session management command (`/ar:tmux`)
- `agents/tmux-session-automation.md` - Advanced automation patterns

### Quick Reference: Commands vs Manual tmux

| Task | Manual tmux Command | autorun Shortcut |
|------|-------------------|-------------------|
| List Claude sessions | `tmux list-windows` (manual) | `/ar:tabs` |
| Create session | `tmux new-session -d -s name` | `/ar:tm create name` |
| Send to all sessions | `for s in $(tmux list-sessions); do ...` | `/ar:tabs all:continue` |
| Test CLI | Manual scripting required | `/ar:tt test my-cli` |

### AI-Monitor Configuration Options
- `--prompt/-p <text>` - Custom prompt to send when idle
- `--stop/-s <string>` - Stop marker to detect completion
- `--stop-delay-seconds <n>` - Delay before stopping after detecting stop marker
- `--max-retry-cycles/-c <n>` - Maximum number of re-prompt cycles
- `--max-runtime-minutes <n>` - Maximum runtime in minutes
- `--check-interval <n>` - Seconds between checks
- `--prompt-on-start [window]` - Send the prompt immediately on start, optionally to one window

</integrations>

<examples>

## Usage Examples

### Create Testing Session with AI-Monitor
```bash
# Create session (default: autorun)
byobu new-session -d -s "autorun"

# Navigate and start process
byobu send-keys -t "autorun" "cd /path/to/project" C-m
byobu send-keys -t "autorun" "npm test" C-m

# Start ai-monitor (from separate terminal)
uv run --project "${CLAUDE_PLUGIN_ROOT}" python -m autorun.ai_monitor "autorun" --prompt "Continue testing" --stop "Tests completed" --max-retry-cycles 3
```

### Monitor Claude Code Session
```bash
# Create Claude Code session (default: autorun unless user specifies otherwise)
byobu new-session -d -s "autorun"
byobu send-keys -t "autorun" "cd /project" C-m
byobu send-keys -t "autorun" "claude" C-m

# Start monitoring for autonomous work
uv run --project "${CLAUDE_PLUGIN_ROOT}" python -m autorun.ai_monitor "autorun" --prompt "Continue working autonomously" --stop "AUTORUN_ALL_TASKS_COMPLETED" --max-retry-cycles 10
```

### Automated Plugin Testing Workflow
```bash
# Create session for autorun testing (default: autorun)
byobu new-session -d -s "autorun"

# Navigate to project (replace with your autorun directory)
byobu send-keys -t "autorun" "cd \$HOME/.claude/autorun" C-m

# Start Claude Code
byobu send-keys -t "autorun" "claude" C-m
sleep 5

# Set model to haiku for efficiency
byobu send-keys -t "autorun" "/model haiku" C-m
sleep 2

# Install plugin locally (replace with your autorun directory)
byobu send-keys -t "autorun" "/plugin marketplace add \$HOME/.claude/autorun" C-m
sleep 3

# Install plugin
byobu send-keys -t "autorun" "/plugin install ar@autorun" C-m
sleep 5

# Test commands
byobu send-keys -t "autorun" "/afs" C-m
sleep 3

byobu send-keys -t "autorun" "/afst" C-m
sleep 3

# Capture output for verification
byobu capture-pane -t "autorun" -p -S -20
```

### Error Handling and Recovery
```bash
# Check if session exists before operations
if byobu list-sessions | grep -q "test-session"; then
    echo "Session exists, proceeding..."
else
    echo "Session not found, creating..."
    byobu new-session -d -s "test-session"
fi

# Interrupt hanging commands
byobu send-keys -t "test-session" C-c

# Kill and recreate session if needed
byobu kill-session -t "test-session"
byobu new-session -d -s "test-session"
```

</examples>

<pitfalls>

## Common Mistakes and Solutions

### CRITICAL: Control Sequence Syntax Errors

**❌ Common Mistake: Incorrect Enter Key Syntax**
```bash
# WRONG - This will NOT work as expected
byobu send-keys -t "session_name" "command" "C-m"  # WRONG syntax
byobu send-keys -t "session_name" "command C-m"     # WRONG syntax
```

**✅ CORRECT: Proper Control Sequence Syntax**
```bash
# CORRECT - Each operation is ALWAYS a separate byobu send-keys command
byobu send-keys -t "session_name" "command"   # Step 1: Type the command text
byobu send-keys -t "session_name" C-m         # Step 2: Press Enter to execute

byobu send-keys -t "session_name" "cd /path"  # Step 1: Type "cd /path"
byobu send-keys -t "session_name" C-m         # Step 2: Press Enter to execute

# EFFICIENCY TIP: Chain operations with && for single-line execution
byobu send-keys -t "session_name" C-c && byobu send-keys -t "session_name" C-m  # Interrupt + confirm

byobu send-keys -t "session_name" C-c         # Step 1: Press Ctrl+C interrupt
byobu send-keys -t "session_name" C-m         # Step 2: Press Enter to confirm (if needed)
```

**Key Rules:**
- Control sequences (C-m, C-c, C-d) must be **separate arguments**, not inside quotes
- Commands go in quotes, control sequences go outside quotes as separate args
- `C-m` = Enter/Return, `C-c` = Ctrl+C, `C-d` = EOF, `C-l` = Clear screen
- **CRITICAL**: Text input and Enter key are ALWAYS separate byobu send-keys operations
- **CRITICAL**: Enter key (C-m) must ALWAYS be sent as a separate operation after typing text
- **CRITICAL**: Ctrl+C (C-c) and Enter (C-m) are different operations and must be sent separately when needed

### Command Execution Issues

**Problem:** Commands appear to execute but fail silently
- **Cause:** Missing proper Enter key sequence (C-m)
- **Solution:** Always add `C-m` as separate argument after command

**Problem:** Commands hang or timeout
- **Cause:** Missing sleep intervals for Claude Code processing
- **Solution:** Add `sleep 2-5` between commands, especially after Claude Code startup

**Problem:** Session becomes unresponsive
- **Cause:** Commands failing without proper error handling
- **Solution:** Use Ctrl+C (`C-c`) to interrupt, recreate session if needed

### Plugin Installation Issues

**Problem:** Marketplace addition fails with "not found"
- **Cause:** Incorrect path syntax or marketplace already exists
- **Solution:** Use absolute paths and check existing marketplaces first

**Problem:** Plugin installation fails after marketplace addition
- **Cause:** Timing issues or plugin name mismatch
- **Solution:** Wait for marketplace addition to complete, use correct plugin identifier

**Discovery: Slash Commands vs Plugin Installation**
- Some functionality may be installed as slash commands in `~/.claude/commands/` rather than formal plugins
- Check slash commands first: `ls -la ~/.claude/commands/`
- Slash commands work immediately without plugin installation
- Example: `/afs`, `/afst`, `/afa`, `/afj` may be available as slash commands even when no plugins are installed

## Best Practices

1. **Session Naming**: Always use "autorun" as the default session name unless user specifies another tmux session name
2. **Default Session**: Use "autorun" as the default session name for all autorun testing workflows
3. **Existence Checks**: Always verify session existence before operations using `byobu list-sessions`
4. **Error Recovery**: Implement Ctrl+C handling for stuck commands and session recreation when needed
5. **Output Verification**: Use capture-pane for command result verification and testing validation
6. **Resource Management**: Clean up sessions after testing with `byobu kill-session`
7. **Timing**: Add appropriate sleep intervals between commands (2-5 seconds for Claude Code startup)
8. **AI-Monitor Integration**: Use ai-monitor for long-running autonomous sessions and automated workflows
9. **Model Selection**: Use haiku for automated tasks to reduce resource usage and improve performance
10. **Byobu vs Tmux**: Prefer byobu commands for user-friendly interface, tmux commands for scripting
11. **Control Sequences**: Always use proper control sequence syntax - commands in quotes, C-m/C-c as separate arguments
12. **Error Prevention**: Test control sequences manually before automation scripts
13. **Efficiency Operations**: Use `&&` to chain byobu commands for single-line execution: `byobu send-keys C-c && byobu send-keys C-m`
14. **Debugging Strategy**: Test functionality step-by-step instead of assuming installation state
15. **Slash Command Priority**: Check `~/.claude/commands/` first before plugin installation attempts

</pitfalls>

<reference>

## Implementation Notes

- This skill uses tmux as the primary backend (byobu is a tmux wrapper providing user-friendly interface)
- Byobu provides enhanced F-key shortcuts and session management over tmux
- All tmux commands work with both byobu and tmux sessions (byobu with tmux backend)
- AI-monitor provides the automation layer for autonomous workflows and session monitoring
- Control sequences (C-m for Enter, C-c for interrupt) are critical for proper command execution
- Proper timing and error handling ensure reliable automated testing workflows
- Byobu sessions can be managed with both byobu commands and direct tmux commands

## External Resources and References

### Documentation Links
- **Byobu Official Documentation** - https://www.byobu.org/
  - Use when learning byobu-specific features and configuration
  - Essential for understanding F-key shortcuts and byobu workflow
  - Visit when setting up new byobu environments

- **Tmux Manual** - https://github.com/tmux/tmux/wiki
  - Reference for advanced tmux commands and scripting
  - Use when creating complex session automation scripts
  - Essential for understanding tmux prefix commands and scripting

- **Claude Code Skills Documentation** - https://docs.claude.com/en/docs/claude-code/skills
  - Learn how to create and structure Claude Code skills
  - Use when creating additional skills or extending this one
  - Essential for understanding skill YAML frontmatter and formatting

- **Claude Code Plugin Documentation** - https://docs.claude.com/en/docs/claude-code/plugins
  - Reference for Claude Code plugin development
  - Use when developing or debugging Claude Code plugins
  - Essential for understanding plugin architecture and hook systems

- **Claude Code Plugin Examples** - https://raw.githubusercontent.com/anthropics/claude-code/refs/heads/main/plugins/README.md
  - Official examples and patterns for Claude Code plugins
  - Use when implementing plugin features or debugging issues
  - Essential for understanding best practices from official plugins

### Testing and Automation Resources
- **AI-Monitor Integration (autorun)** - `src/autorun/ai_monitor.py`
  - Built-in tmux monitoring and automation capabilities
  - Use for autonomous session monitoring and automated re-prompting
  - Essential for long-running automated workflows and testing

- **Bash Scripting Guide** - https://www.gnu.org/software/bash/manual/
  - Reference for creating automated test scripts
  - Use when writing complex test automation scripts
  - Essential for proper error handling and process control

### When to Use Each Resource

**Setup Phase:**
- Visit Byobu Documentation when first setting up your testing environment
- Check Claude Code Skills Documentation when creating new skills
- Review tmux Manual when learning advanced session management

**Development Phase:**
- Use AI-Monitor integration for implementing autonomous workflows
- Reference Claude Code Plugin Examples when developing plugins
- Consult Bash Scripting Guide for complex automation scripts

**Debugging Phase:**
- Check Claude Code Plugin Documentation when troubleshooting plugin issues
- Review tmux Manual when debugging session management problems
- Use AI-Monitor logs when monitoring automated workflows

**Best Practices:**
- Always reference official Claude Code Plugin Examples for patterns
- Keep Byobu Documentation handy for session management shortcuts
- Use tmux Manual for scripting complex automation scenarios

</reference>
