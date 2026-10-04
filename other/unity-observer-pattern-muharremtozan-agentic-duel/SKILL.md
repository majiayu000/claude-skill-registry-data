---
name: unity-observer-pattern
description: Reactive Property system for Unity. Decouples data from UI and logic using observable wrappers and UnityEvents.
---

# Unity Observer Pattern (Reactive Properties)

A powerful implementation of the Observer pattern that turns standard variables into "Smart Properties." Includes full Inspector support and Edit-mode tooling based on the "Generic Observer" architecture.

## Core Features
1. **Hybrid Path**: Works with standard C# listeners (Pro Path) AND UnityEvents (Designer/Light Path).
2. **Implicit Casting**: Seamless syntax allows `int x = myObservableInt;` (no more `.Value` boilerplate).
3. **Editor Persistence**: Programmatically wire persistent calls in Edit Mode that save to scene/prefab.
4. **Diagnostic Logging**: Built-in structured logging for tracking event flows.

## Core Files (Max 3)
- `Observable.cs.txt`: The core generic wrapper with implicit casting and built-in editor wiring.
- `ObservableEditorTools.cs.txt`: Advanced reflection hacks for clearing persistent UnityEvents.
- `ObservableExample.cs.txt`: Concrete example demonstrating UI binding and lifecycle management.

## Usage

### Option A: The Light Path (Inspector)
1. Define a field: `public Observable<int> health;`.
2. In Unity Inspector, drag your UI method into the `On Value Changed` list.

### Option B: The Pro Path (Code)
```csharp
health.AddListener( val => Debug.Log( val ) );
health.Value = 50; // Automatically triggers notification
```

### Option C: Implicit Usage
```csharp
int currentHealth = health; // Works automatically via implicit operator
```

## Cleanup
Always call `RemoveListener` or `Dispose` in `OnDisable` to prevent memory leaks.
