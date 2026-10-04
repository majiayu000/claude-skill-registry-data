---
name: memento
description: Capture and restore an object's internal state without violating encapsulation.
license: MIT
metadata:
  author: Satcomx00-x00
  version: 1.0.0
  category: code-quality
  type: behavioral-pattern
---

# Memento

Saves a snapshot of an object's state into a memento object so it can be restored later, without exposing the object's internals.

## When to Use

- Undo/redo functionality
- Transactional operations that may need rollback
- Taking snapshots/checkpoints of an object's state
- When a direct copy of state fields would break encapsulation

## How to Apply

1. Identify the **Originator** — the object whose state needs saving
2. Create the **Memento** class (or record) that holds a copy of the state (immutable, opaque to outsiders)
3. Add `save(): Memento` and `restore(m: Memento): void` methods to the Originator
4. Create a **Caretaker** that stores mementos and requests save/restore from the Originator

## Example

```ts
class EditorMemento {
  constructor(readonly content: string) {}
}

class Editor {
  private content = '';
  type(text: string)             { this.content += text; }
  save()                         { return new EditorMemento(this.content); }
  restore(m: EditorMemento)      { this.content = m.content; }
  getContent()                   { return this.content; }
}

// Caretaker
const editor   = new Editor();
const history: EditorMemento[] = [];

editor.type('Hello');
history.push(editor.save());

editor.type(' World');
console.log(editor.getContent()); // Hello World

editor.restore(history.pop()!);
console.log(editor.getContent()); // Hello
```

## References

- [refactoring.guru/design-patterns/memento](https://refactoring.guru/design-patterns/memento)
