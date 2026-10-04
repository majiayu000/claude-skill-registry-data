---
name: unity-memento-pattern
description: Implements the Memento pattern for capturing and restoring object states. Perfect for Loadout managers, Checkpoints, and Undo/Redo systems.
---

# Unity Memento Pattern

This skill provides a structured way to handle state snapshots in Unity. Inspired by Adam Myhre's implementation, it strictly separates state data (Memento), the state producer (Originator), and the state manager (Caretaker).

## Core Features
1. **Immutable Snapshots**: Ensures saved data cannot be corrupted by subsequent changes to the original object.
2. **Loadout Management**: Built-in support for multiple save slots (Caretaker logic).
3. **Encapsulation**: State structure is hidden from the resting system, exposing only what is necessary.

## Core Files (Max 3)
- `IMemento.cs.txt`: Base interfaces and generic Memento wrapper.
- `LoadoutManager.cs.txt`: Caretaker implementation for managing list-based snapshots.
- `HotbarMementoExample.cs.txt`: Practical application for UI/Item state persistence.

## Usage
Refer to `HotbarMementoExample.cs.txt` to see how to save a list of ScriptableObjects using a copy-constructor.
