---
name: talon-development
description: Expert guidance for Talon voice control development. Use when creating voice commands, defining actions, writing .talon files, testing Talon config, or debugging Talon issues.
---

# Talon Development Guide

This skill provides guidance for developing Talon voice control configurations.

## Improving This Skill

When you discover new Talon patterns, best practices, or learn something not covered here, **update this skill**:

1. Add new patterns or examples to the relevant section
2. Correct any outdated information
3. Add new sections for uncovered topics
4. Update TESTING.md with new testing techniques

The goal is for this skill to grow into a comprehensive local reference.

## Key Resources

### Talon Code Search

Search across hundreds of Talon repositories for real-world examples:

```
https://search.talonvoice.com/api/v1/search/?q=<query>&fold_case=auto&regex=false
```

Returns JSON with matching code snippets and file locations. Use this to find how others implement patterns.

Set `regex=true` to use RE2 regex patterns in the query (e.g., `q=cron\.(after|interval)`).

### Reference Repositories

Look up patterns and examples in these repositories. Code in active repositories is more reliable than potentially outdated documentation.

| Repository | Purpose |
|------------|---------|
| [talonhub/community](https://github.com/talonhub/community) | Main community voice command set. The standard reference for Talon patterns. |
| [cursorless-dev/cursorless](https://github.com/cursorless-dev/cursorless) | Voice-controlled structural code editing. Advanced Talon integration example. |

### Documentation

| Resource | Notes |
|----------|-------|
| [talonvoice.com/docs](https://talonvoice.com/docs/) | Official API documentation. Covers Module, Context, actions, captures, settings. |
| [talon.wiki](https://talon.wiki/) | Community wiki. Good for getting started, hardware recommendations. |

**Note:** Online documentation may be outdated. When in doubt, check actual code in repositories or use the code search.

## Testing

See [TESTING.md](TESTING.md) for command-line testing instructions, including:
- Using `test_talon.sh`
- Testing actions with `cron.after()`
- Test code templates and patterns
- Debugging failed tests

## Programmatic Access

See [PROGRAMMATIC_ACCESS.md](PROGRAMMATIC_ACCESS.md) for interacting with a running Talon instance:
- Why direct REPL access isn't available
- Write-and-reload pattern for executing code
- File-based RPC (VSCode integration)

## UI Automation

See [UI_AUTOMATION.md](UI_AUTOMATION.md) for inspecting and interacting with application UI elements via Windows UI Automation / macOS Accessibility APIs.

## Canvas (Skia Graphics)

See [CANVAS.md](CANVAS.md) for drawing overlays, widgets, and visual feedback using Talon's Skia-based Canvas API.

## Eye Tracking

See `settings/api_exploration/eye_tracking/EYE_TRACKING_API_EXPLORATION.md` for the eye tracking API reference.

## Project Structure

```
user/                           # Talon user directory
├── apps/                       # App-specific commands
│   ├── generic/               # Cross-app abstractions (code_editor, browser)
│   └── [app].py/.talon        # App-specific implementations
├── misc/                       # General utilities and commands
├── plugins/                    # Reusable plugins (vimfinity, etc.)
├── settings/                   # Talon settings files
├── utils/                      # Python utility modules
└── test_talon.sh              # Testing script
```

## File Types

### .talon Files (Voice Commands)

Define voice commands and their actions:

```talon
# Context header (optional - restricts when commands are active)
app: vscode
-
# Commands below the dash
hello world: insert("Hello, World!")
go to definition: user.find_definition()
search <user.text>: user.search(text)
```

**Context examples:**
```talon
# Match by app
app: vscode
-

# Match by tag
tag: user.code_editor
-

# Match by OS
os: windows
-

# Multiple conditions (AND)
app: vscode
mode: command
-
```

### .py Files (Actions and Logic)

Define actions, modules, contexts, and complex logic:

```python
from talon import Module, Context, actions

module = Module()

# Define a tag that can be enabled/disabled
module.tag("code_editor", desc="Active in code editors")

# Define actions
@module.action_class
class Actions:
    def my_action(arg: str) -> str:
        """Action docstring - shown in help."""
        return f"Result: {arg}"
```

## Common Patterns

### Module + Context Pattern

Used to define abstract actions with app-specific implementations:

```python
# In apps/generic/code_editor.py
from talon import Module, Context, actions

module = Module()
module.tag("code_editor", desc="Active in code editors")

@module.action_class
class Actions:
    def find_definition() -> None:
        """Navigate to definition."""
        pass  # Abstract - no default implementation

# In apps/vscode.py
from talon import Context, actions

ctx = Context()
ctx.matches = r"""
app: vscode
"""
# Enable the tag when VSCode is active
ctx.tags = ["user.code_editor"]

@ctx.action_class("user")
class UserActions:
    def find_definition():
        actions.key("f12")  # VSCode-specific implementation
```

### Lists and Captures

```python
module = Module()

# Define a list
module.list("browsers", desc="Web browsers")

ctx = Context()
ctx.lists["user.browsers"] = {
    "chrome": "chrome",
    "firefox": "firefox",
    "edge": "msedge",
}

# Use in .talon:
# open <user.browsers>: user.open_app(browsers)
```

### Settings

```python
from talon import Module, settings

module = Module()
module.setting(
    "my_timeout",
    type=int,
    default=5000,
    desc="Timeout in milliseconds",
)

# Use it:
timeout = settings.get("user.my_timeout")
```

## Import Patterns

```python
# Standard Talon imports
from talon import Module, Context, actions, settings, app, clip, cron, ctrl

# For UI automation
from talon import ui

# For key simulation
actions.key("ctrl-c")
actions.insert("text")

# Internal Talon plugins (fragile - use local imports)
def my_action():
    from talon_plugins import menu
    menu.open_repl(None)
```

## Cron (Scheduled Tasks)

The `cron` module schedules tasks to run on the **main thread**. This is important because UI operations (canvas creation, etc.) require the main thread's resource context.

```python
from talon import cron

# Run once after delay
job = cron.after("1s", my_callback)

# Run repeatedly at interval
job = cron.interval("500ms", my_callback)

# Cancel a scheduled job
cron.cancel(job)
```

**Key point:** `cron.after` and `cron.interval` queue callbacks to run on the main thread. This means:
- Canvas creation/destruction works in cron callbacks
- UI operations are safe in cron callbacks
- The callback executes in a proper Talon resource context

## Quick Reference

### Common Actions

```python
actions.key("ctrl-c")           # Press keys
actions.insert("text")          # Type text
actions.edit.copy()             # Standard edit actions
actions.user.my_action()        # User-defined actions
actions.app.path()              # Get current file path
```

### Common Talon Syntax

```talon
# Simple command
hello: insert("world")

# With capture
say <phrase>: insert(phrase)

# With list
open <user.apps>: user.open_app(apps)

# Optional words
[please] save: edit.save()

# Alternative words
(quit | exit): app.quit()

# Repeater
press enter <number> times: key("enter:number")
```

## Best Practices

### Do

- Keep voice commands short and memorable
- Use abstract actions in `generic/` with app-specific overrides
- Group related commands in the same file
- Add docstrings to all actions
- Test changes before committing
- Use tags to control command availability
- Search talonhub/community for examples before inventing patterns

### Don't

- Put complex logic in `.talon` files (use Python)
- Create overlapping voice commands
- Forget to remove test code
- Use blocking operations without `cron`
- Hardcode app-specific keys in generic actions
- Trust potentially outdated documentation over working code

## File Locations by Purpose

| Purpose | Location |
|---------|----------|
| App-specific commands | `apps/[app].py` + `apps/[app].talon` |
| Cross-app abstractions | `apps/generic/` |
| General utilities | `misc/` |
| Reusable plugins | `plugins/` |
| Utility Python modules | `utils/` |
| Settings | `settings/` |
