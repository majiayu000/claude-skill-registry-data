---
name: unity-dependency-injection
description: Implements Dependency Inversion and Injection patterns. Decouples high-level logic from concrete implementations using attributes and reflection.
---

# Unity Dependency Injection (DI)

A lightweight system to satisfy the "D" in SOLID. Allows classes to request dependencies via `[Inject]` without knowing who provides them.

## Core Features
1. **Attribute-Based Injection**: Use `[Inject]` to mark fields and `[Provide]` to define sources.
2. **Interface Focus**: Encourages programming to abstractions, making systems hot-swappable.
3. **Automated Wiring**: Scene-wide injection happens on Awake, ensuring dependencies are ready before Start.
4. **Diagnostic Logging**: Tracks successful injections and warns about missing providers.

## Core Files (Max 3)
- `DIAttributes.cs.txt`: Contains the marker attributes for the compiler.
- `DependencyInjector.cs.txt`: The engine that finds and wires dependencies in the scene.
- `DIExample.cs.txt`: Shows how to decouple a Hero from an AbilitySystem.

## Usage

### 1. Define an Interface
```csharp
public interface IWeapon { void Fire(); }
```

### 2. Provide the Implementation
```csharp
public class PlasmaRifle : MonoBehaviour, IWeapon {
    [Provide] public IWeapon GetWeapon() => this;
    public void Fire() { /* ... */ }
}
```

### 3. Inject into Client
```csharp
public class Player : MonoBehaviour {
    [Inject] private IWeapon currentWeapon;
    void Start() => currentWeapon.Fire();
}
```

### 4. Setup
Place a `DependencyInjector` component in your scene or persistent prefab.
