---
name: unity-event-bus
description: Advanced code-driven event bus with reflection-based bootstrapping. Provides zero-setup global messaging.
---

# Unity Advanced Event Bus

This skill provides a high-performance, type-safe messaging hub for Unity projects. It is designed for developers who want to decouple systems without the overhead of ScriptableObject-based event channels.

## Core Features
1. **Reflection Bootstrapping**: Automatically finds all events and initializes buses on game load.
2. **Generic Performance**: Uses static generic indices for O(1) event dispatch performance.
3. **Zero Allocation**: Optimized for structs to ensure no runtime garbage collection for messages.
4. **Editor Safety**: Auto-clears all static bindings when exiting Play Mode to prevent Editor memory leaks.

## Core Files (Max 3)
- `EventBusCore.cs.txt`: Base interfaces and the static generic bus hub.
- `EventBusBootstrapper.cs.txt`: Unity-specific auto-initialization and assembly scanning.
- `EventBusExample.cs.txt`: Practical implementation of player and system events.

## Usage
Define a `struct : IEvent`, create an `EventBinding<T>`, and register it in `OnEnable`. Raise events from anywhere using `EventBus<T>.Raise()`.
