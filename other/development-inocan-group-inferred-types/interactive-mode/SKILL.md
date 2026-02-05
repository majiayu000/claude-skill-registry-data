---
name: interactive-mode
description: Interactive mode features including keyboard shortcuts, vim mode, command history, and background tasks. Use when user asks about REPL, keyboard shortcuts, interactive features, or vim mode.
---

# Claude Code Interactive Mode

## Overview

Interactive mode provides a rich REPL (Read-Eval-Print Loop) environment with keyboard shortcuts, command history, vim editing, and background task management.

## Keyboard Controls

### Essential Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+C` | Cancel current input or generation |
| `Ctrl+D` | Exit the Claude Code session |
| `Ctrl+L` | Clear terminal screen (preserves conversation history) |
| `Ctrl+O` | Toggle verbose output (shows detailed tool usage) |
| `Ctrl+R` | Search backwards through command history |
| `Ctrl+B` | Move bash invocation to background |
| `Tab` | Switch extended thinking on and off |

### Navigation

| Shortcut | Action |
|----------|--------|
| `↑`/`↓` | Navigate through command history |
| `←`/`→` | Move cursor left/right |
| `Home` | Move to start of line |
| `End` | Move to end of line |

### Help

| Shortcut | Action |
|----------|--------|
| `?` | Show help and shortcuts |

## Multiline Input Methods

Claude Code supports several ways to create multiline inputs:

### Universal Method
```
Line 1 \
Line 2 \
Line 3
```
**Backslash + Enter** works universally across all platforms.

### macOS Default
```
Option+Enter
```
**Option+Enter** creates a newline on macOS.

### After Terminal Setup
```
Shift+Enter
```
**Shift+Enter** functions after running `/terminal-setup`.

## Vim Editor Mode

### Enabling Vim Mode

**Temporary (current session):**
```
/vim
```

**Permanent:**
```
/config
```
Then enable vim mode in configuration.

### Vim Navigation

**Movement:**
- `h` - Move left
- `j` - Move down
- `k` - Move up
- `l` - Move right
- `w` - Move forward one word
- `e` - Move to end of word
- `b` - Move backward one word
- `0` - Move to start of line
- `$` - Move to end of line

**Editing:**
- `i` - Insert mode
- `a` - Append (insert after cursor)
- `A` - Append at end of line
- `I` - Insert at start of line
- `x` - Delete character
- `dd` - Delete line
- `d$` - Delete to end of line
- `d0` - Delete to start of line
- `dw` - Delete word
- `.` - Repeat last operation

**Modes:**
- `Esc` - Return to normal mode
- `i` - Enter insert mode

## Command History & Search

### Command History

**Navigation:**
- `↑` - Previous command
- `↓` - Next command

**Organization:**
Session history is organized by working directory for better context.

### Search History

**Backward search:**
1. Press `Ctrl+R`
2. Type search term
3. Press `Ctrl+R` again to cycle through matches
4. Press `Enter` to execute
5. Press `Esc` to cancel

**Features:**
- Displays matching commands
- Highlights search terms
- Allows cycling through multiple matches

## Background Task Execution

### Overview

When Claude Code runs a command in the background, it runs the command asynchronously and immediately returns a background task ID.

### Trigger Background Execution

**Automatic:**
Claude may prompt to background long-running tasks.

**Manual:**
Press `Ctrl+B` to move regular bash invocations to the background.

### Managing Background Tasks

**View output:**
Output is buffered and can be retrieved later.

**Monitor tasks:**
Claude shows status updates for background tasks.

**Continue working:**
You can interact with Claude while background tasks run.

## Quick Command Prefixes

### Special Prefixes

| Prefix | Purpose | Example |
|--------|---------|---------|
| `#` | Add content to CLAUDE.md memory | `# Use 2-space indentation` |
| `/` | Trigger slash commands | `/help` |
| `!` | Direct bash execution (no Claude interpretation) | `!ls -la` |
| `@` | File path autocomplete | `@src/` + Tab |

### Memory Shortcut (`#`)

**Add to memory:**
```
# Always use TypeScript strict mode
```

Claude will prompt you to select the target memory file:
- Project memory (`.claude/CLAUDE.md`)
- User memory (`~/.claude/CLAUDE.md`)

### Direct Bash (`!`)

**Execute without interpretation:**
```
!git status
!npm test
!echo "Hello"
```

Benefits:
- Faster execution
- No AI interpretation overhead
- Direct command output

### File Autocomplete (`@`)

**Trigger autocomplete:**
```
@src/
```

Press `Tab` to see file suggestions.

**Attach files to conversation:**
```
Review @src/components/Button.tsx for issues
```

## Advanced Features

### Extended Thinking

**Toggle extended thinking:**
Press `Tab` to enable/disable.

**What it does:**
- Allows Claude more thinking time
- Better for complex reasoning
- Uses more tokens
- Shows thinking process in verbose mode

### Verbose Output

**Toggle verbose mode:**
Press `Ctrl+O`

**What it shows:**
- Detailed tool usage
- API calls and responses
- Token usage
- Performance metrics
- Debugging information

### Screen Management

**Clear screen:**
Press `Ctrl+L` to clear the terminal while preserving conversation history.

**Difference from `/clear`:**
- `Ctrl+L`: Clears screen only (visual)
- `/clear`: Clears conversation history (context)

## Session Management

### Exit Session

**Clean exit:**
Press `Ctrl+D` or type `/exit`

**Force exit:**
Press `Ctrl+C` multiple times

### Interrupting Operations

**Cancel current operation:**
Press `Ctrl+C` once

**Common scenarios:**
- Long-running AI generation
- Bash command execution
- File operations
- Web searches

## Tips & Tricks

### Efficient Navigation

**Quick history access:**
```
↑    # Previous command
↑↑   # Two commands back
```

**Search specific commands:**
```
Ctrl+R "test"    # Find commands with "test"
```

### Productive Workflows

**Background long tasks:**
```
# Long-running test suite
Ctrl+B to background it
Continue working on other tasks
```

**Quick iterations:**
```
↑               # Recall last command
# Edit slightly
Enter           # Execute modified version
```

**Memory building:**
```
# Use snake_case for variables
# Prefer composition over inheritance
# Write tests for all public APIs
```

### Vim Mode Power Users

**Fast editing:**
```
Esc             # Normal mode
0               # Start of line
d$              # Delete to end
i               # Insert mode
Type new content
Esc             # Back to normal
```

**Quick fixes:**
```
Esc             # Normal mode
$               # End of line
x               # Delete last character
a               # Append
Type correction
```

## Customization

### Configure Terminal

**Run setup:**
```
/terminal-setup
```

**What it configures:**
- Multiline input behavior
- Key bindings
- Shell integration
- Terminal compatibility

### Configure Settings

**Access configuration:**
```
/config
```

**Available settings:**
- Vim mode enable/disable
- Diff viewer preferences
- Permission defaults
- Output preferences

## Common Workflows

### Exploratory Development

```
# Ask questions
"explain the authentication flow"

# Make changes
"add rate limiting"

# Test
!npm test

# Adjust
↑ to recall, modify, retry
```

### Debugging Session

```
# Enable verbose
Ctrl+O

# Run with details
"analyze the memory leak"

# Review verbose output
# Identify issue
# Fix

# Disable verbose
Ctrl+O
```

### Batch Operations

```
# Background first task
"run full test suite" → Ctrl+B

# Continue with other work
"refactor user module"

# Check background task
# Complete when done
```

## Integration with Shell

### Command History Persistence

Claude Code integrates with your shell's command history, allowing you to:
- Access Claude commands in shell history
- Use shell history search (Ctrl+R)
- Mix Claude commands with regular shell commands

### Shell Compatibility

Works with:
- Bash
- Zsh
- Fish
- Other POSIX-compatible shells

### Environment Integration

Claude Code respects:
- Shell environment variables
- Shell aliases
- Shell functions
- Current working directory

## Accessibility

### Screen Reader Support

Claude Code works with screen readers for:
- Command input
- Output reading
- Navigation

### Keyboard-only Navigation

All features accessible via keyboard:
- No mouse required
- Full keyboard navigation
- Comprehensive shortcuts
