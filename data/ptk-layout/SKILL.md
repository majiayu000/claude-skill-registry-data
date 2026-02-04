---
name: ptk-layout
description: This skill should be used when the user asks about "prompt_toolkit layout", "HSplit", "VSplit", "Window", "Float", "FloatContainer", "ConditionalContainer", "DynamicContainer", "split pane", "terminal UI layout", "prompt_toolkit containers", or needs to compose visual layouts for terminal applications.
---

# prompt_toolkit Layout System

The layout system in prompt_toolkit provides a compositional approach to building terminal UIs. Layouts are trees of containers that define how content is arranged on screen.

## Core Concepts

### Layout Tree Structure

Every prompt_toolkit application has a `Layout` that wraps a root container. The layout manages focus and provides methods to navigate between focusable elements.

```python
from prompt_toolkit.layout import Layout, HSplit, VSplit, Window

layout = Layout(
    container=HSplit([...]),
    focused_element=some_window  # Optional initial focus
)
```

### Container Types

**HSplit** - Stack children vertically (horizontal split lines between them):
```python
HSplit([
    Window(content=header_control, height=1),
    Window(content=body_control),
    Window(content=footer_control, height=1),
])
```

**VSplit** - Stack children horizontally (vertical split lines between them):
```python
VSplit([
    Window(content=sidebar, width=30),
    Window(width=1, char='│'),  # Divider
    Window(content=main_content),
])
```

**Window** - The basic container that displays a UIControl:
```python
Window(
    content=BufferControl(buffer=my_buffer),
    width=Dimension(min=10, preferred=40),
    height=Dimension(min=5),
    wrap_lines=True,
)
```

**FloatContainer** - Overlay floating elements on top of content:
```python
FloatContainer(
    content=main_layout,
    floats=[
        Float(content=dialog, top=2, left=5),
        Float(content=completion_menu, xcursor=True, ycursor=True),
    ]
)
```

## Dimensions

Control sizing with `Dimension` objects:

```python
from prompt_toolkit.layout.dimension import Dimension, D

# Fixed size
Window(height=Dimension.exact(5))
Window(height=5)  # Shorthand for exact

# Flexible with constraints
Window(width=Dimension(min=10, max=50, preferred=30))

# Using D shorthand
Window(width=D(min=10, preferred=30))
```

## Conditional Containers

Show/hide containers based on filters:

```python
from prompt_toolkit.layout import ConditionalContainer
from prompt_toolkit.filters import Condition, has_focus

show_sidebar = Condition(lambda: app_state.sidebar_visible)

ConditionalContainer(
    content=sidebar_window,
    filter=show_sidebar
)
```

## Dynamic Containers

Swap containers at runtime:

```python
from prompt_toolkit.layout import DynamicContainer

def get_current_view():
    if mode == 'edit':
        return editor_container
    return viewer_container

DynamicContainer(get_container=get_current_view)
```

## Focus Management

Navigate focus within the layout:

```python
# In key binding handler
@kb.add('tab')
def _(event):
    event.app.layout.focus_next()

@kb.add('s-tab')
def _(event):
    event.app.layout.focus_previous()

# Focus specific element
event.app.layout.focus(specific_window)
```

## Common Layout Patterns

### Two-Pane Split
```python
VSplit([
    Window(BufferControl(left_buffer), width=D(weight=1)),
    Window(width=1, char='│'),
    Window(BufferControl(right_buffer), width=D(weight=1)),
])
```

### Header/Body/Footer
```python
HSplit([
    Window(FormattedTextControl(title), height=1, style='class:header'),
    Window(BufferControl(main_buffer)),
    Window(FormattedTextControl(status), height=1, style='class:footer'),
])
```

### Floating Dialog
```python
FloatContainer(
    content=main_layout,
    floats=[
        Float(
            content=ConditionalContainer(
                content=dialog_frame,
                filter=dialog_visible
            )
        )
    ]
)
```

## Reference Codebase

For detailed API signatures and advanced patterns, consult:
- **Source**: `/Users/brandon/src/python-prompt-toolkit/src/prompt_toolkit/layout/containers.py`
- **Source**: `/Users/brandon/src/python-prompt-toolkit/src/prompt_toolkit/layout/layout.py`
- **Examples**: `/Users/brandon/src/python-prompt-toolkit/examples/full-screen/`

## Additional Resources

### Reference Files
- **`references/containers-api.md`** - Complete container class signatures
- **`references/layout-patterns.md`** - Production layout patterns
