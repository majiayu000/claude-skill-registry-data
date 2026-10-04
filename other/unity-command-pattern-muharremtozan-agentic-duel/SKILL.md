---
name: unity-command-pattern
description: Encapsulate actions as objects for queuing, undo/redo, and async execution.
---

# Unity Command Pattern

Minimal command pattern with async support.

## Core Features
1. **Async Interface**: `ICommand` with Task-based execution
2. **SO Commands**: Data-driven actions for simple cases
3. **Command Queue**: Sequential execution system

## Core Files (1 file)
- `Command.cs.txt`: Complete command pattern (interface + SO + queue)

## Usage
Implement `ICommand` for complex logic, or inherit `CommandSO` for inspector-configurable actions.
