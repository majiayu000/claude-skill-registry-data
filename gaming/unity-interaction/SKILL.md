---
name: unity-interaction
description: Generic raycast-based interaction system. Works for any game genre (RPG, Platformer, Simulation).
---

# Unity Interaction System

Minimal, generic interaction pattern using interfaces and raycasting.

## Core Features
1. **Interface-Based**: `IInteractable` works on any object type
2. **Dual Actions**: Primary (E) and Alternative (F) interactions
3. **Raycast Detection**: Automatic target selection based on player facing
4. **Zero Dependencies**: Self-contained, no external skill requirements

## Core Files (2 files only)
- `IInteractable.cs.txt`: Core interfaces for interactables and interactors
- `InteractionController.cs.txt`: Raycast-based detection and input handling

## Usage
See [guide.md](references/guide.md) for implementation examples.
