---
name: command
description: Encapsulate a request as an object, enabling undo/redo, queuing, and logging of operations.
license: MIT
metadata:
  author: Satcomx00-x00
  version: 1.0.0
  category: code-quality
  type: behavioral-pattern
---

# Command

Turns a request into a stand-alone object containing all information about the request. Decouples the object that invokes the operation from the one that performs it.

## When to Use

- You need undoable operations (`execute()` / `undo()`)
- Operations should be queued, scheduled, or executed asynchronously
- You want to parameterise objects with operations (callbacks as objects)
- Transactional behaviour — rollback if any command in a batch fails

## How to Apply

1. Define a `Command` interface with `execute()` (and optionally `undo()`)
2. Create concrete command classes that store the receiver and all needed parameters
3. Create an `Invoker` that stores and triggers commands
4. Wiring: client creates commands, sets receivers, passes commands to the invoker

## Example

```ts
interface Command { execute(): void; undo(): void; }

class TextEditor {
  private text = '';
  insert(s: string) { this.text += s; }
  delete(n: number) { this.text = this.text.slice(0, -n); }
  getText() { return this.text; }
}

class InsertCommand implements Command {
  constructor(private editor: TextEditor, private text: string) {}
  execute() { this.editor.insert(this.text); }
  undo()    { this.editor.delete(this.text.length); }
}

class CommandHistory {
  private history: Command[] = [];
  execute(cmd: Command) { cmd.execute(); this.history.push(cmd); }
  undo() { this.history.pop()?.undo(); }
}

const editor = new TextEditor();
const history = new CommandHistory();
history.execute(new InsertCommand(editor, 'Hello'));
history.execute(new InsertCommand(editor, ' World'));
history.undo();  // removes ' World'
```

## References

- [refactoring.guru/design-patterns/command](https://refactoring.guru/design-patterns/command)
