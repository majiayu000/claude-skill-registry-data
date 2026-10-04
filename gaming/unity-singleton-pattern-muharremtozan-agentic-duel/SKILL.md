---
name: unity-singleton-pattern
description: Implementation of global manager access with strict lifecycle control. Supports Standard, Persistent, and Regulator variations.
---

# Unity Singleton Pattern

A robust suite of Singleton variations for global systems. Adheres to the Ohm-Yura project rule: "Use Singletons ONLY for global systems (GameManager, UIManager, InputManager)."

## Core Features
1. **Singleton<T>**: Standard management. Destroys new duplicates to keep the original.
2. **PersistentSingleton<T>**: Extends Singleton with Don't Destroy On Load (DDOL) for cross-scene state.
3. **RegulatorSingleton<T>**: Advanced inverse logic. Destroys OLD instances and keeps the NEWEST (useful for hot-swapping).
4. **StaticInstance<T>**: Lightweight global access without duplication enforcement.

## Core Files (Max 3)
- `SingletonBase.cs.txt`: Generic base classes for classic and persistent variants.
- `SingletonRegulator.cs.txt`: Logic for the time-stamped regulator variant.
- `SingletonExample.cs.txt`: Concrete examples for Game and UI managers.

## Usage

### 1. Standard Manager
```csharp
public class UIManager : Singleton<UIManager> { }
// Use via: UIManager.Instance.Show();
```

### 2. Persistent Manager
```csharp
public class InventoryManager : PersistentSingleton<InventoryManager> { }
// Survives scene changes.
```

### 3. Regulator (System Swap)
```csharp
public class MusicSystem : RegulatorSingleton<MusicSystem> { }
// Spawning a new one will automatically kill the old one.
```

## Key Principle
Always use the most restrictive version. If it doesn't need to persist cross-scene, use `Singleton<T>`. If you just need a reference but don't mind duplicates, use `StaticInstance<T>`.
