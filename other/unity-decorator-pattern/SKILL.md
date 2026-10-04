---
name: unity-decorator-pattern
description: Dynamically modify object behavior by wrapping. Perfect for buffs, debuffs, and stat calculations.
---

# Unity Decorator Pattern

Minimal decorator pattern for stat modification.

## Core Features
1. **Generic Interface**: `IDecorator<T>` for any value type
2. **Stat Modifiers**: Percentage and flat modifications
3. **Composable**: Stack multiple decorators

## Core Files (1 file)
- `Decorator.cs.txt`: Complete decorator pattern (interface + base + modifiers)

## Usage
```csharp
IDecorator<float> damage = new BaseStat(100);
damage = new PercentageModifier(damage, 0.2f); // +20%
damage = new FlatModifier(damage, 10); // +10
float final = damage.GetValue(); // 130
```
