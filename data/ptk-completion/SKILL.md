---
name: ptk-completion
description: This skill should be used when the user asks about "prompt_toolkit completion", "Completer", "WordCompleter", "FuzzyCompleter", "NestedCompleter", "PathCompleter", "auto-complete", "tab completion", "completion menu", "CompletionsMenu", or needs to implement auto-completion in prompt_toolkit applications.
---

# prompt_toolkit Completion System

The completion system provides intelligent suggestions as users type. It supports simple word completion, fuzzy matching, nested commands, file paths, and custom completers.

## Basic Completion

```python
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.buffer import Buffer

completer = WordCompleter(['hello', 'world', 'help'])
buffer = Buffer(
    completer=completer,
    complete_while_typing=True,
)
```

## Built-in Completers

### WordCompleter

Simple word matching from a list:

```python
from prompt_toolkit.completion import WordCompleter

completer = WordCompleter(
    words=['SELECT', 'FROM', 'WHERE', 'INSERT', 'UPDATE'],
    ignore_case=True,
    meta_dict={
        'SELECT': 'Query columns',
        'FROM': 'Specify table',
        'WHERE': 'Filter rows',
    }
)
```

### FuzzyCompleter

Fuzzy matching wraps any completer:

```python
from prompt_toolkit.completion import FuzzyCompleter, WordCompleter

base = WordCompleter(['configuration', 'connection', 'constructor'])
completer = FuzzyCompleter(base)

# User types "cfg" → matches "configuration"
# User types "conn" → matches "connection", "constructor"
```

### NestedCompleter

Hierarchical command completion:

```python
from prompt_toolkit.completion import NestedCompleter

completer = NestedCompleter.from_nested_dict({
    'show': {
        'version': None,
        'interfaces': None,
        'ip': {
            'route': None,
            'interface': None,
        },
    },
    'set': {
        'hostname': None,
        'ip': {
            'address': None,
        },
    },
    'exit': None,
})
```

### PathCompleter

File system path completion:

```python
from prompt_toolkit.completion import PathCompleter

completer = PathCompleter(
    only_directories=False,
    expanduser=True,
)
```

## Custom Completers

Implement the `Completer` interface:

```python
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.document import Document

class MyCompleter(Completer):
    def __init__(self, data):
        self.data = data

    def get_completions(self, document: Document, complete_event):
        word = document.get_word_before_cursor()

        for item in self.data:
            if item.lower().startswith(word.lower()):
                yield Completion(
                    text=item,
                    start_position=-len(word),
                    display=item,
                    display_meta='Description here',
                )
```

## Completion Object

```python
Completion(
    text='hello',           # Text to insert
    start_position=-3,      # Replace 3 chars before cursor
    display='hello',        # Display in menu (optional)
    display_meta='Greeting', # Meta info (optional)
    style='class:completion', # Custom style (optional)
)
```

**Critical**: `start_position` is negative - it specifies how many characters before the cursor to replace.

## Completion Menu

Display completions in a floating menu:

```python
from prompt_toolkit.layout import FloatContainer, Float
from prompt_toolkit.layout.menus import CompletionsMenu

layout = FloatContainer(
    content=main_content,
    floats=[
        Float(
            xcursor=True,
            ycursor=True,
            content=CompletionsMenu(max_height=16),
        )
    ]
)
```

## Async Completers

For slow completion sources:

```python
from prompt_toolkit.completion import Completer, Completion

class AsyncCompleter(Completer):
    async def get_completions_async(self, document, complete_event):
        word = document.get_word_before_cursor()
        results = await fetch_completions(word)
        for result in results:
            yield Completion(result, start_position=-len(word))

    def get_completions(self, document, complete_event):
        # Sync fallback (optional)
        return []
```

## ThreadedCompleter

Run slow completers in a thread:

```python
from prompt_toolkit.completion import ThreadedCompleter

completer = ThreadedCompleter(SlowCompleter())
```

## Combining Completers

```python
from prompt_toolkit.completion import merge_completers

combined = merge_completers([
    WordCompleter(['command1', 'command2']),
    PathCompleter(),
])
```

## Key Bindings for Completion

```python
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.filters import has_completions

kb = KeyBindings()

@kb.add('tab', filter=~has_completions())
def start_completion(event):
    event.current_buffer.start_completion()

@kb.add('tab', filter=has_completions())
def next_completion(event):
    event.current_buffer.complete_next()

@kb.add('s-tab', filter=has_completions())
def prev_completion(event):
    event.current_buffer.complete_previous()
```

## Reference Codebase

For detailed API and patterns:
- **Source**: `/Users/brandon/src/python-prompt-toolkit/src/prompt_toolkit/completion/`
- **Examples**: `/Users/brandon/src/python-prompt-toolkit/examples/prompts/`

## Additional Resources

### Reference Files
- **`references/completer-api.md`** - Complete Completer class API
- **`references/completion-patterns.md`** - Production completion patterns
