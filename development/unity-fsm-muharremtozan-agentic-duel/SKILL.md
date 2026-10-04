---
name: unity-fsm
description: Specialized skill for implementing a robust, extensible Finite State Machine in Unity using the State and Strategy patterns. Based on the pattern by Adam Myhre (3D Platformer). Use when creating complex AI, player controllers, or any system requiring structured state management.
---

# Unity Finite State Machine (FSM)

This skill provides a modular, object-oriented State Machine architecture for Unity, specifically refactored to match the implementation in Adam Myhre's 3D Platformer.

## Core Features
- **Object-Oriented**: Each state is a dedicated class.
- **Hybrid Support**: Support for both "Heavy" (classes) and "Light" (`ActionState`) states.
- **Strategy-Based Transitions**: Uses Predicates and Detection Strategies.
- **Timer System**: Includes Adam Myhre's `CountdownTimer` and `StopwatchTimer`.
- **Namespace Support**: Uses `Platformer` and `Utilities` namespaces.

## Core Files (assets/code/)
- `IState.cs.txt`, `StateMachine.cs.txt`, `IPredicate.cs.txt`: Base FSM logic.
- `ActionState.cs.txt`: **New!** Lambda-based state to reduce boilerplate.
- `Timer.cs.txt`: AI cooldown management.
- `IDetectionStrategy.cs.txt`, `ConeDetectionStrategy.cs.txt`: Sensing logic.
- `PlayerDetector.cs.txt`, `Enemy.cs.txt`, `EnemyBaseState.cs.txt`: AI templates.

## Usage Guides
- [GUIDE.md](references/guide.md): General FSM setup and wiring.
- [ENEMY-AI.md](references/enemy-ai.md): Specific guide for implementing AI with Detection Strategies.

## Implementation Pattern
1. **Define** your states by inheriting from `BaseState`.
2. **Wire** them in your `PlayerController` or `EnemyAI` using `stateMachine.AddTransition`.
3. **Execute** via `Update()` and `FixedUpdate()` calls to the machine.
