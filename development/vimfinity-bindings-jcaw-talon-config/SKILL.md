---
name: vimfinity-bindings
description: Create vimfinity keyboard bindings for Talon voice control following project conventions - use when adding keyboard shortcuts, integrating editor actions, or setting up modal keybindings
---

# Vimfinity Binding Creator

Vimfinity is a modal keyboard system for Talon that uses vim-like key sequences. This skill helps create bindings following the project's conventions.

## Vimfinity Source Code

**Location:** `plugins/vimfinity/vimfinity.py`

This is where `vimfinity_bind_keys()` is implemented. Read this file if you need to understand:
- How the binding system works internally
- Available parameters and options
- How contexts are handled
- Debug or troubleshoot binding issues

## Binding Locations

Choose the appropriate location based on scope:

### 1. Module-Specific Bindings (Preferred)
Add bindings inline in the relevant module file using a context:

```python
# In apps/generic/code_editor.py
code_editor_context = Context()
code_editor_context.matches = r"""
tag: user.code_editor
"""

vimfinity_bind_keys(
    {
        "g": "Git",
        "g g": actions.user.git_ui,
        "g c": actions.user.git_commit,
        "g s": actions.user.git_stage_file,
    },
    code_editor_context,
)
```

### 2. Global Bindings
For cross-cutting bindings, use `misc/vimfinity_user/vimfinity_bindings.py`:

```python
vimfinity_bind_keys(
    {
        "f": "File",
        "f f": user.open_file,
    }
)
```

## Binding Patterns

### Menu Structure
- First letter creates a category/menu
- Double letters are common actions: `g g`, `f f`, `w w`
- Related actions share a prefix: `g g`, `g c`, `g s` (all git)

### Action Types

**Direct function reference:**
```python
"g s": user.git_stage_file,  # Calls action directly
```

**Lambda for delayed execution:**
```python
"up": ShiftDelayed(user.maximize),  # Waits for key release
```

**Tuple with description:**
```python
"o T": (ShiftDelayed(user.open_talon_repl), "Open Talon REPL"),
```

## Context Patterns

### Code Editors (All)
```python
code_editor_context.matches = r"""
tag: user.code_editor
"""
```

### Specific IDEs
```python
ide_context.matches = r"""
tag: user.jetbrains
tag: user.emacs
app: vscode
"""
```

### Browser
```python
browser_context.matches = r"""
tag: user.browser
"""
```

## Common Conventions

**Prefixes in use:**
- `o` = "Open" (applications, files)
- `g` = "Git" (source control)
- `f` = "File" (file operations)
- `w` = "Windows" (window management)
- `m` = "Mic/Macros" (Talon control)
- `e` = "Emacs" (Emacs-specific)
- `k` = "Program-Specific" (override per app)
- `i` = "Insert" (snippets, templates)
- `p` = "App-specific" (per-app actions)
- `=` = "Utils" (utilities, debugging)

**Reserved/Special:**
- Arrow keys = Window snapping
- `backspace`/`delete` = Special functions
- `?` = Google search
- `q`/`Q` = ChatGPT integration

## Import Requirements

Always import at the top of the file:

```python
from user.plugins.vimfinity.vimfinity import vimfinity_bind_keys
```

For module-level bindings, also need:
```python
from talon import Context
```

## Examples from Codebase

### Git Actions (apps/generic/code_editor.py)
```python
vimfinity_bind_keys(
    {
        "g": "Git",
        "g g": actions.user.git_ui,
        "g c": actions.user.git_commit,
        "g s": actions.user.git_stage_file,
    },
    code_editor_context,
)
```

### Global File Actions (misc/vimfinity_user/vimfinity_bindings.py)
```python
vimfinity_bind_keys(
    {
        "f": "File",
        "f f": user.open_file,
    }
)
```

### Browser-Specific (misc/vimfinity_user/vimfinity_bindings.py)
```python
vimfinity_bind_keys(
    {
        "k": user.rango_toggle_keyboard_clicking,
        "h": user.rango_disable,
        "r": user.rango_enable,
    },
    browser_context,
)
```

## ShiftDelayed Pattern

Use `ShiftDelayed` when the binding uses shift and the action should wait for key release:

```python
class ShiftDelayed:
    """Performs action after a short delay, to allow user to release shift key."""
    def __init__(self, action):
        self.action = action

    def __call__(self, *_, **__):
        sleep("200ms")
        return self.action(*_, **__)

# Usage
"?": ShiftDelayed(google_that),
"Q": user.chatgpt_switch_start,
```

## Don't

- **Don't** reuse existing prefixes for unrelated actions
- **Don't** create single-letter bindings without a category label
- **Don't** forget to specify context for scoped bindings
- **Don't** use symbols that require shift without ShiftDelayed

## Do

- **Do** keep related actions under the same prefix
- **Do** provide descriptive category labels
- **Do** add bindings in the most specific appropriate location
- **Do** follow existing naming patterns
- **Do** test bindings after adding them

## Testing

After creating bindings:
1. Reload Talon or restart it
2. Try the key sequence in the appropriate context
3. Check for conflicts with existing bindings
4. Verify the menu label appears correctly

## File Structure

```
apps/generic/code_editor.py          # Editor-wide bindings
misc/vimfinity_user/vimfinity_bindings.py  # Global bindings
apps/vscode.py                        # VSCode-specific bindings
```

Choose the most specific location that makes sense for your binding.
