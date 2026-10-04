---
name: unity-builder-pattern
description: Step-by-step object construction using fluent interfaces. Simplifies complex GameObject setup.
---

# Unity Builder Pattern

Minimal builder pattern for GameObject construction.

## Core Features
1. **Fluent API**: Chainable methods for readable setup
2. **Generic Interface**: `IBuilder<T>` for any object type
3. **Component Management**: Easy component addition

## Core Files (1 file)
- `Builder.cs.txt`: Complete builder pattern (interface + fluent implementation)

## Usage
```csharp
var player = new GameObjectBuilder( "Player" )
    .WithPosition( Vector3.zero )
    .AddComponent<Rigidbody>()
    .Build();
```
