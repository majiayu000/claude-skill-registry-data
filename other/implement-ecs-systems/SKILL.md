---
name: implement-ecs-systems
description: "Use when you have an ECS spec (ecs_spec.md) and need to generate component structs, stateless systems, archetype factories, and the World orchestrator."
---

## 1. Overview
Generates complete ECS architecture: pure data components, optimized archetypes (`ecs_spec.md`), stateless systems, and a central `World` orchestrator. Enforces absolute data/logic separation.

## 2. Core Pattern

1. **Platform Detection**: Scan config for target language/platform.
2. **Component Generation** (`ecs_spec.md` Section 2): Generate all components as pure data structures. Every listed component MUST have a generated file. Group related components only when always used together (e.g., Transform + Velocity → `SpatialComponents.ts`).
3. **System & World Implementation**: Stateless systems with standard `update(dt)` signatures. Central `World` orchestrator for entity lifecycles and execution order.
4. **Game-Specific Systems (MANDATORY)**: Read `ecs_spec.md` Section 4. For EACH system in the pipeline:
    * Generate `<SystemName>System.ts` in `src/systems/`
    * Extend base `ECSSystem`, declare component `mapping`, implement `update(dt)` with specified tick frequency (`Frame` = every frame, `10Hz Tick` = throttled)
    * Route ALL inter-system communication through EventBus exclusively
    * Include header comment with execution phase and priority
5. **Entity Archetype Factories (MANDATORY)**: Read `ecs_spec.md` Section 3. For EACH archetype:
    * Generate factory function in `src/systems/entityFactories.ts` (or equivalent)
    * Accept `World` parameter → `world.createEntity()` → add ALL components → set sensible defaults → return entity ID
6. **Inter-System Communication**: Exclusively via EventBus; systems never call each other directly.

## 3. Interaction Protocol
* **[OOP Intercept]**: Component described with methods/state → "Components must be pure data. I'll strip logic, keep fields. Proceed?"
* **[Tight Coupling Intercept]**: System calls another directly → "Systems use EventBus for decoupling. I'll convert to event-driven. Proceed?"

## 4. Red Flags - STOP and Start Over
* **Pure Data Components**: Components contain only fields, no methods or internal state
* **Event Bus Communication**: Route all inter-system communication through EventBus exclusively
* **Stateless Systems**: Store all state in components or external stores, never in system implementations

## 5. Final Integrity Audit
- [ ] All components contain only data fields
- [ ] Systems follow stateless `update(dt)` signature
- [ ] Inter-system communication via EventBus only
- [ ] Archetypes match `ecs_spec.md` compositions
- [ ] **ALL systems from Section 4 generated as separate `src/systems/` files**
- [ ] **All archetypes from Section 3 have factory functions**
- [ ] `src/systems/` not empty — contains all pipeline systems
- [ ] Each system has correct priority and component mapping
