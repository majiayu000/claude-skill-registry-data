---
name: unity-strategy-pattern
description: Implements the Strategy Pattern to encapsulate interchangeable algorithms (e.g., Spells, Attacks) using ScriptableObjects. Allows hot-swapping behavior without modifying client code. Clean Code approach.
---

# Unity Strategy Pattern

This skill implements the Strategy Behavioral Pattern to replace conditional logic (switches/ifs) with interchangeable algorithm objects.

## Core Features
1.  **Encapsulated Logic**: Each behavior (Fireball, Shield, Orbital) lives in its own `ScriptableObject` or class.
2.  **Hot-Swapping**: Change an entity's behavior at runtime by swapping the strategy asset.
3.  **Open/Closed Compliance**: Add new spells/behaviors without modifying the `PlayerController`.

## Core Files (assets/code/)
-   `SpellStrategy.cs.txt`: Base abstract ScriptableObject (The Interface).
-   `ShieldSpellStrategy.cs.txt`: Simple instantiation strategy.
-   `OrbitalSpellStrategy.cs.txt`: Complex math/logic strategy (Pro Path).

## Usage Guide
See [GUIDE.md](references/guide.md) to learn how to create flexible Ability/Spell systems using Strategies.
