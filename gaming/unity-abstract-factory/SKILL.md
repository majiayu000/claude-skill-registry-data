---
name: unity-abstract-factory
description: Factory pattern for creating families of related objects. Supports both ScriptableObject composition and simple prefab instantiation.
---

# Unity Abstract Factory

Minimal factory pattern implementation for object creation.

## Core Features
1. **Generic Interface**: `IFactory<T>` for type-safe creation
2. **SO-Based Factories**: Data-driven object families
3. **Simple Prefab Factory**: Quick GameObject spawning

## Core Files (2 files)
- `Factory.cs.txt`: Complete factory pattern (interface + SO base + prefab factory)
- `EquipmentFactory.cs.txt`: Example themed factory implementation

## Usage
Inherit from `Factory<T>` for complex families, or use `PrefabFactory` for simple spawning.
