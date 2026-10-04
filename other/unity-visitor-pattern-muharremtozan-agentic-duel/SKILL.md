---
name: unity-visitor-pattern
description: Implements the Visitor pattern for decoupled operations on object structures. Perfect for PowerUp systems and complex stat modifications.
---

# Unity Visitor Pattern

This skill provides a modular implementation of the Visitor pattern, specifically optimized for Unity systems where multiple component types need shared modification logic (e.g., PowerUps).

## Core Features
1. **Double Dispatch**: Safe and structured way to handle operations on multiple types.
2. **Scriptable Visitors**: Data-driven logic providers that can be easily configured in the Inspector.
3. **Decoupled Logic**: Keep your core components clean of "logic leakage" from external systems.

## Core Files (Max 3)
- `VisitorCore.cs.txt`: Base interfaces and visitable component base.
- `ScriptableVisitor.cs.txt`: Pro-path ScriptableObject implementation.
- `VisitorExample.cs.txt`: Concrete example for stat modification.

## Usage
Refer to [guide.md](references/guide.md) for implementation details and Pro/Light path distinctions.
