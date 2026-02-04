---
name: ptk-styling
description: This skill should be used when the user asks about "prompt_toolkit Style", "styling", "colors", "formatted text", "HTML text", "ANSI", "FormattedText", "pygments", "syntax highlighting", "themes", or needs to style text and UI elements in prompt_toolkit applications.
---

# prompt_toolkit Styling System

The styling system provides comprehensive control over colors, text attributes, and syntax highlighting. It supports CSS-like style definitions, Pygments integration, and multiple formatted text formats.

## Style Basics

```python
from prompt_toolkit.styles import Style

style = Style.from_dict({
    'prompt': 'bold #00ff00',
    'input': '#ffffff',
    'error': 'bg:#ff0000 #ffffff bold',
})

app = Application(style=style)
```

## Color Formats

### Named Colors
```python
'red', 'green', 'blue', 'yellow', 'magenta', 'cyan', 'white', 'black'
```

### ANSI Colors (Terminal-Safe)
```python
'ansiblack', 'ansired', 'ansigreen', 'ansiyellow',
'ansiblue', 'ansimagenta', 'ansicyan', 'ansiwhite',
'ansibrightblack', 'ansibrightred', 'ansibrightgreen', 'ansibrightyellow',
'ansibrightblue', 'ansibrightmagenta', 'ansibrightcyan', 'ansibrightwhite'
```

### Hex Colors
```python
'#ff0000'   # 6-digit hex
'#f00'      # 3-digit hex (expanded to #ff0000)
```

### Background Colors
```python
'bg:#ff0000'        # Red background
'bg:ansigreen'      # Green background
```

## Text Attributes

```python
'bold'        # Bold text
'italic'      # Italic text
'underline'   # Underlined
'blink'       # Blinking (terminal support varies)
'reverse'     # Swap foreground/background
'hidden'      # Hidden text
'strike'      # Strikethrough

# Negations
'nobold', 'noitalic', 'nounderline', 'noblink', 'noreverse'
```

## Style Syntax

Combine colors and attributes with spaces:

```python
style = Style.from_dict({
    # Foreground color
    'text': '#ffffff',

    # Foreground + background
    'highlight': '#000000 bg:#ffff00',

    # Foreground + background + attributes
    'error': '#ffffff bg:#ff0000 bold underline',

    # Just attributes
    'emphasis': 'bold italic',

    # Class-based (for layouts)
    'class:header': 'bold reverse',
    'class:footer': 'bg:#333333',
})
```

## Formatted Text Types

### Plain String
```python
text = "Hello, World!"
```

### Style Tuples
```python
text = [
    ('class:prompt', '>>> '),
    ('class:input', 'user input here'),
    ('', '\n'),  # No style
]
```

### HTML-like Formatting
```python
from prompt_toolkit.formatted_text import HTML

text = HTML('''
<b>Bold</b> and <i>italic</i>
<style fg="red">Red text</style>
<style bg="yellow" fg="black">Highlighted</style>
<u>Underlined</u>
''')
```

### ANSI Escape Codes
```python
from prompt_toolkit.formatted_text import ANSI

text = ANSI('\x1b[31mRed\x1b[0m normal')
```

## FormattedTextControl

Display styled text in layouts:

```python
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout import Window

def get_status():
    return [
        ('class:status.mode', ' NORMAL '),
        ('class:status.file', ' file.py '),
        ('class:status.pos', ' 1:1 '),
    ]

status_bar = Window(
    FormattedTextControl(get_status),
    height=1,
    style='class:status',
)
```

## Pygments Integration

Use Pygments for syntax highlighting:

```python
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.styles import style_from_pygments_cls
from pygments.lexers import PythonLexer
from pygments.styles import get_style_by_name

# Apply Pygments lexer to buffer
control = BufferControl(
    buffer=code_buffer,
    lexer=PygmentsLexer(PythonLexer),
)

# Use Pygments style
pygments_style = style_from_pygments_cls(get_style_by_name('monokai'))
app = Application(style=pygments_style)
```

## Merging Styles

Combine multiple style definitions:

```python
from prompt_toolkit.styles import merge_styles

base_style = Style.from_dict({...})
theme_style = Style.from_dict({...})
user_style = Style.from_dict({...})

combined = merge_styles([base_style, theme_style, user_style])
```

## Dynamic Styles

Change styles at runtime:

```python
from prompt_toolkit.styles import DynamicStyle

def get_current_style():
    if dark_mode:
        return dark_style
    return light_style

app = Application(
    style=DynamicStyle(get_current_style),
)
```

## Style Classes in Layouts

Reference styles in containers:

```python
Window(
    content=my_control,
    style='class:editor',
)

HSplit([
    Window(header, style='class:header'),
    Window(body, style='class:body'),
    Window(footer, style='class:footer'),
])
```

## Common Style Definitions

```python
style = Style.from_dict({
    # Prompt styles
    'prompt': 'bold #00aa00',
    'prompt.arg': '#888888',

    # Completion menu
    'completion-menu': 'bg:#333333 #ffffff',
    'completion-menu.completion': '',
    'completion-menu.completion.current': 'bg:#00aa00 #000000',
    'completion-menu.meta.completion': 'bg:#444444 #999999',
    'completion-menu.meta.completion.current': 'bg:#00aa00 #000000',

    # Scrollbar
    'scrollbar.background': 'bg:#333333',
    'scrollbar.button': 'bg:#888888',

    # Search
    'search': 'bg:#ffff00 #000000',
    'search.current': 'bg:#ff8800 #000000',

    # Validation
    'validation-toolbar': 'bg:#ff0000 #ffffff',
})
```

## Reference Codebase

For detailed API and built-in styles:
- **Source**: `/Users/brandon/src/python-prompt-toolkit/src/prompt_toolkit/styles/`
- **Source**: `/Users/brandon/src/python-prompt-toolkit/src/prompt_toolkit/formatted_text/`
- **Examples**: `/Users/brandon/src/python-prompt-toolkit/examples/print-text/`

## Additional Resources

### Reference Files
- **`references/style-api.md`** - Complete Style API
- **`references/themes.md`** - Pre-built theme examples
