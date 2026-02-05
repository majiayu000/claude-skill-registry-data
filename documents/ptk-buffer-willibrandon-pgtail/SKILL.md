---
name: ptk-buffer
description: This skill should be used when the user asks about "prompt_toolkit Buffer", "Document", "cursor position", "text manipulation", "BufferControl", "text editing", "undo/redo", "selection", "copy paste", or needs to handle text input and manipulation in prompt_toolkit applications.
---

# prompt_toolkit Buffer & Document

Buffer and Document are the core abstractions for text handling in prompt_toolkit. Buffer is mutable and manages editing state; Document is immutable and represents text at a point in time.

## Buffer Overview

Buffer holds the editable text and provides:
- Text manipulation methods
- Cursor position management
- Undo/redo history
- Integration with completers, validators, history

```python
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import FileHistory

buffer = Buffer(
    completer=WordCompleter(['hello', 'world']),
    history=FileHistory('.history'),
    multiline=True,
    complete_while_typing=True,
)
```

## Creating Buffers

### Basic Buffer
```python
buffer = Buffer(name='my_buffer')
```

### Buffer with Features
```python
buffer = Buffer(
    completer=my_completer,
    history=FileHistory('~/.myapp_history'),
    validator=my_validator,
    complete_while_typing=True,
    validate_while_typing=False,
    multiline=True,
    accept_handler=on_accept,
    on_text_changed=on_change,
)
```

### Accept Handler
```python
def on_accept(buff: Buffer) -> bool:
    """Called when user presses Enter to accept input."""
    print(f"User entered: {buff.text}")
    return False  # False = clear buffer after accept

buffer = Buffer(accept_handler=on_accept)
```

## Text Manipulation

### Reading Text
```python
text = buffer.text                    # Full text
doc = buffer.document                 # Current Document
pos = buffer.cursor_position          # Cursor position (int)
```

### Inserting Text
```python
buffer.insert_text('hello')           # At cursor
buffer.insert_text('\n', move_cursor=False)  # Without moving cursor
```

### Deleting Text
```python
buffer.delete_before_cursor(count=1)  # Backspace
buffer.delete(count=1)                # Delete at cursor
buffer.delete_after_cursor(count=5)   # Delete forward
```

### Selection
```python
buffer.start_selection()              # Start selecting
buffer.copy_selection()               # Copy to clipboard
buffer.cut_selection()                # Cut to clipboard
buffer.paste_clipboard_data(data)     # Paste
```

### Undo/Redo
```python
buffer.undo()
buffer.redo()
buffer.reset()                        # Clear buffer
```

## Document (Immutable)

Document represents text state at a point in time. It's cached and optimized for repeated access.

```python
from prompt_toolkit.document import Document

doc = Document(
    text='hello world',
    cursor_position=5,  # After 'hello'
)
```

### Document Properties
```python
doc.text                      # Full text
doc.cursor_position           # Position (int)
doc.cursor_position_row       # Current line number
doc.cursor_position_col       # Column in current line
doc.line_count                # Total lines
doc.current_line              # Text of current line
doc.text_before_cursor        # Text before cursor
doc.text_after_cursor         # Text after cursor
doc.char_before_cursor        # Single char before cursor
```

### Document Navigation Methods
```python
# Get positions (returns offset, not new position)
doc.get_cursor_left_position(count=1)
doc.get_cursor_right_position(count=1)
doc.get_cursor_up_position(count=1)
doc.get_cursor_down_position(count=1)

# Word navigation
doc.get_word_before_cursor()
doc.get_word_under_cursor()
doc.find_start_of_previous_word()
doc.find_next_word_beginning()

# Line navigation
doc.get_start_of_line_position()
doc.get_end_of_line_position()
```

### Document Search
```python
doc.find('pattern')                   # Returns position or None
doc.find_all('pattern')               # List of all positions
doc.find_backwards('pattern')         # Search backwards
```

## BufferControl

BufferControl displays a Buffer in a Window:

```python
from prompt_toolkit.layout.controls import BufferControl
from prompt_toolkit.layout import Window

control = BufferControl(
    buffer=my_buffer,
    lexer=PygmentsLexer(PythonLexer),
    focus_on_click=True,
    input_processors=[...],
)

window = Window(content=control)
```

## Event Handlers

React to buffer changes:

```python
def on_text_changed(buff):
    print(f"Text changed to: {buff.text}")

def on_cursor_changed(buff):
    print(f"Cursor at: {buff.cursor_position}")

buffer = Buffer(
    on_text_changed=on_text_changed,
    on_cursor_position_changed=on_cursor_changed,
)

# Or add later
buffer.on_text_changed += another_handler
```

## Working with Multiple Buffers

Named buffers for different purposes:

```python
from prompt_toolkit.buffer import Buffer

input_buffer = Buffer(name='input')
output_buffer = Buffer(name='output', read_only=True)
search_buffer = Buffer(name='search')
```

Access in key bindings:
```python
@kb.add('c-s')
def _(event):
    input_buf = event.app.layout.get_buffer_by_name('input')
    output_buf = event.app.layout.get_buffer_by_name('output')
```

## Reference Codebase

For detailed API signatures:
- **Source**: `/Users/brandon/src/python-prompt-toolkit/src/prompt_toolkit/buffer.py`
- **Source**: `/Users/brandon/src/python-prompt-toolkit/src/prompt_toolkit/document.py`

## Additional Resources

### Reference Files
- **`references/buffer-api.md`** - Complete Buffer class API
- **`references/document-api.md`** - Complete Document class API
