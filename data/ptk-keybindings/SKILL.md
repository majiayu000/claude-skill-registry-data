---
name: ptk-keybindings
description: This skill should be used when the user asks about "prompt_toolkit key bindings", "KeyBindings", "keyboard shortcuts", "key handler", "key sequences", "c-x c-c", "ConditionalKeyBindings", "filters for keys", "vi mode bindings", "emacs bindings", or needs to define keyboard interactions in prompt_toolkit applications.
---

# prompt_toolkit Key Bindings

Key bindings connect keyboard input to actions in prompt_toolkit applications. The system supports single keys, sequences, conditionals, and both sync and async handlers.

## Basic Key Bindings

```python
from prompt_toolkit.key_binding import KeyBindings

kb = KeyBindings()

@kb.add('c-q')  # Ctrl+Q
def quit_app(event):
    event.app.exit()

@kb.add('c-c')
def copy(event):
    event.app.clipboard.set_data(
        event.current_buffer.copy_selection()
    )
```

## Key Names

### Modifier Keys
- `c-` - Control (e.g., `'c-a'` = Ctrl+A)
- `s-` - Shift (e.g., `'s-tab'` = Shift+Tab)
- `m-` - Meta/Alt (e.g., `'m-x'` = Alt+X)
- `c-s-` - Ctrl+Shift (e.g., `'c-s-a'`)

### Special Keys
```python
'enter'      # Enter/Return
'tab'        # Tab
's-tab'      # Shift+Tab
'backspace'  # Backspace
'delete'     # Delete
'escape'     # Escape
'space'      # Space bar
'up', 'down', 'left', 'right'  # Arrow keys
'home', 'end'    # Home/End
'pageup', 'pagedown'  # Page Up/Down
'insert'     # Insert
'f1' - 'f24' # Function keys
```

### Key Sequences
```python
@kb.add('c-x', 'c-c')  # Ctrl+X followed by Ctrl+C
def _(event):
    event.app.exit()

@kb.add('g', 'g')  # Press 'g' twice (like vim)
def _(event):
    event.current_buffer.cursor_position = 0
```

## Event Object

The event parameter provides access to app state:

```python
@kb.add('c-t')
def _(event):
    event.app              # Application instance
    event.current_buffer   # Currently focused Buffer
    event.data             # Key data (for Keys.Any)
    event.key_sequence     # List of KeyPress objects
    event.is_repeat        # True if key is held down
    event.arg              # Numeric argument (vim-style)
```

## Filters (Conditional Bindings)

Enable bindings only under certain conditions:

```python
from prompt_toolkit.filters import (
    Condition,
    has_focus,
    has_selection,
    vi_mode,
    emacs_mode,
    is_searching,
    has_completions,
)

# Only when buffer 'main' is focused
@kb.add('enter', filter=has_focus('main'))
def _(event):
    process_input(event.current_buffer.text)

# Custom condition
show_menu = Condition(lambda: app_state.menu_visible)

@kb.add('up', filter=show_menu)
def _(event):
    menu.select_previous()

# Combine with operators
@kb.add('tab', filter=has_focus('input') & ~has_completions())
def _(event):
    event.current_buffer.insert_text('    ')
```

### Filter Operators
- `&` - AND
- `|` - OR
- `~` - NOT

## Decorator Parameters

```python
@kb.add(
    'c-s',
    filter=some_filter,        # When to activate
    eager=False,               # True = handle immediately, ignore longer sequences
    is_global=False,           # True = always check, ignore focus
    save_before=lambda e: True,  # Save undo state before handler
    record_in_macro=True,      # Include in macro recording
)
def _(event):
    ...
```

## Async Handlers

```python
@kb.add('c-t')
async def _(event):
    result = await fetch_data()
    event.current_buffer.insert_text(result)
```

## Merging Key Bindings

Combine multiple KeyBindings objects:

```python
from prompt_toolkit.key_binding import merge_key_bindings

app_bindings = KeyBindings()
editor_bindings = KeyBindings()

combined = merge_key_bindings([
    app_bindings,
    editor_bindings,
])
```

## Vi Mode Setup

```python
from prompt_toolkit.application import Application
from prompt_toolkit.enums import EditingMode

app = Application(
    editing_mode=EditingMode.VI,
    key_bindings=kb,
)

# Vi-specific bindings
from prompt_toolkit.filters import vi_insert_mode, vi_navigation_mode

@kb.add('j', 'k', filter=vi_insert_mode)
def _(event):
    # jk to exit insert mode (common mapping)
    event.app.vi_state.input_mode = InputMode.NAVIGATION
```

## Common Patterns

### Exit Application
```python
@kb.add('c-c')
@kb.add('c-q')
def _(event):
    event.app.exit()
```

### Focus Navigation
```python
@kb.add('tab')
def _(event):
    event.app.layout.focus_next()

@kb.add('s-tab')
def _(event):
    event.app.layout.focus_previous()
```

### Toggle State
```python
@kb.add('c-b')
def _(event):
    app_state.sidebar_visible = not app_state.sidebar_visible
    event.app.invalidate()
```

## Reference Codebase

For detailed API and built-in bindings:
- **Source**: `/Users/brandon/src/python-prompt-toolkit/src/prompt_toolkit/key_binding/key_bindings.py`
- **Built-in**: `/Users/brandon/src/python-prompt-toolkit/src/prompt_toolkit/key_binding/bindings/`
- **Examples**: `/Users/brandon/src/python-prompt-toolkit/examples/prompts/`

## Additional Resources

### Reference Files
- **`references/keybinding-api.md`** - Complete KeyBindings API
- **`references/filters.md`** - All available filters
