---
name: game-state
description: Design Godot game/application state with explicit authority, lifecycle, transitions, save/load boundaries, scene synchronization, deterministic updates, and separation between durable state and presentation instances.
---
# Godot Game State

Use when gameplay, simulation, UI, progression, world, or application state must survive or coordinate across scenes and systems.

## Procedure
1. Classify state by authority and lifetime: transient scene/UI state, current session/run state, world/gameplay state, player/profile progression, configuration/preferences, and durable save data as relevant.
2. Give each fact one authoritative owner. Scene nodes may display or cache state, but avoid multiple mutable copies that can diverge without an explicit synchronization protocol.
3. Define state transitions/events and invariants before wiring signals. For multi-step modes, prefer explicit states/transitions over many independent booleans that permit impossible combinations.
4. Separate simulation/domain state from visual scene instances where reload, pooling, streaming, or multiple views can occur. Recreating a scene should not accidentally create a new authoritative world fact.
5. Decide which state belongs in scene ownership, Resources/data objects, autoload/application services, or dedicated model objects according to lifetime and project conventions rather than convenience alone.
6. Define initialization and synchronization order when a scene enters: load authoritative state, instantiate views, connect observers, then apply subsequent changes without duplicate initialization.
7. For save/load, version the durable format, validate inputs, define migration/default behavior, avoid serializing ephemeral node references, and test recovery from missing/older/partial data according to product requirements.
8. Handle pause, scene transition, restart/new game, respawn, disconnect/reconnect, rollback/reset, and duplicated event delivery where they affect state authority.
9. Keep state changes observable enough for UI/animation/audio/network systems without letting observers become hidden secondary writers.
10. Test transitions and save/load across scene reloads and application restart, including invalid transition attempts and old-version data when supported.

## Decision rules
- The scene tree is not automatically the durable game-state model.
- Signals notify; they do not replace clear ownership of who is allowed to change a fact.
- Do not persist runtime object/node references as durable identity; save stable domain identifiers/data instead.
- Multiplayer/distributed authoritative state requires a networking/game architecture decision beyond this local state skill when applicable.

## Quality gate
State architecture is ready when each important fact has one authority and lifecycle, transitions cannot create contradictory states, scene recreation preserves intended game truth, save/load has a version/recovery story, observers do not become hidden writers, and tests prove representative transitions plus restart/reload behavior.