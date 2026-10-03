---
name: implement-game-loop
description: "Use when generating the application entry point, subsystem bootstrap sequence, and main game loop with correct dependency ordering and lifecycle management."
---

## 1. Overview

Orchestrates entry point, subsystem bootstrapping, and primary execution loop in required dependency order.

## 2. Quick Reference

**Bootstrap order** (dependency-critical):
1. EventBus + Allocators
2. ECS World → register all systems from `src/systems/`
3. Behavior Tree Engine (tick at spec frequency, default 10Hz)
4. Input Handler
5. State Machine
6. Entity factories → create initial entities
7. Screen Manager (if screens defined)
8. Game loop: `world.update(dt)` only; delegate rendering to Renderer

## 3. When to Use

- **Scenarios**: Initializing main entry point; setting up bootstrap after core design specs finalized.
- **Triggers**: `implement game loop`, `bootstrap engine`, `application entry point`, `system wiring`.

## 3. Core Pattern

1. **Platform & Language Detection** — Scan project config for target platform and language.
2. **Entry Point & Bootstrap** — Generate main entry file and bootstrap module wiring EventBus, ECS World, Input Handler, State Machine, Behavior Tree Engine in dependency order.
3. **ECS Systems Registration (MANDATORY)** — After creating ECS World, scan `src/systems/` for all generated systems. Register EACH with correct component mapping and priority per `ecs_spec.md` Section 4 (Phase A → B → C). Every system must be registered.
4. **Behavior Tree Engine (MANDATORY)** — Init during bootstrap (after EventBus + ECS World). Tick in game loop at frequency from `behavior_tree_spec.md` Section 5 (default 10Hz). Connect via `assignTree(entityId, rootNode())` using factories from `implement-behavior-tree`. Interrupt on high-priority events per `behavior_tree_spec.md` Section 4.
5. **Entity Factory (MANDATORY)** — Use factories from `implement-ecs-systems` to create initial entities. Instantiate via factory functions only: `createTestEntities()` calls `createPlayer(world)` etc., creates correct entity count, assigns BT via `assignTree()`.
6. **Game Loop** — Follow `game_loop.md`: call `world.update(dt)` exclusively (delegate entity updates to ECS), `btEngine.update(currentTime)`, process input, delegate rendering to Renderer only. Web: Phaser 3 → init Phaser + GameScene; Three.js → init renderer/scene/camera + animation loop.
7. **Lifecycle** — Wire event bus subscribers, register FSM transitions, implement graceful shutdown.

## 4. Interaction Protocol

* **[Dependency Order]**: If incorrect wiring order: *"Bootstrap initializes [System X] before dependency [Y]. Crash risk. Reorder?"*
* **[Missing Subsystem]**: *"[SubSystem] not initialized or wired. Add bootstrap step?"*
* **Constraint**: Prioritize correct dependency ordering.

## 5. Red Flags

* **Dependency Order Compliance**: Initialize subsystems only after all prerequisites are ready.
* **Complete Subsystem Initialization**: Wire every component from system_roster.md to prevent null reference crashes.
* **Graceful Shutdown**: Implement clean shutdown handlers per subsystem to prevent data corruption and resource leaks.

## 6. Final Integrity Audit

- [ ] All subsystems from `system_roster.md` have init steps.
- [ ] Dependency order: EventBus/Allocators BEFORE ECS/AI.
- [ ] Matches `game_loop.md` cycle logic.
- [ ] Clean shutdown handler per subsystem.
- [ ] **All ECS systems from `src/systems/` registered** — none skipped.
- [ ] **BT engine ticked** at correct frequency (10Hz).
- [ ] **Entity factories used** — no manual component instantiation.
- [ ] **Game loop delegates to `world.update(dt)`** — no manual per-entity logic.
- [ ] **Rendering delegated to Renderer** — no manual render calls.

## 7. Execution Command

`/implement-game-loop`
