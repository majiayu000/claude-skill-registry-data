---
name: design-ecs-architecture
description: "Use when designing ECS architecture for high-scale games (1,000+ entities). Triggers: 'ECS architecture', 'data-oriented design'."
---

# design-ecs-architecture

## 1. Overview

Designs Entity-Component-System architecture for high-scale games using data-oriented principles — pure-data components, stateless systems, event-driven communication. Core principle: no state in systems, no logic in components.

## 2. When to Use

Use when:
- Designing architecture for a game expecting high entity counts (1,000+) where cache locality matters.
- Starting a new project that will benefit from data-oriented design instead of OOP hierarchies.
- Refactoring tightly coupled systems into stateless, event-driven ECS.

Do not use when:
- The game is small-scale (dozens of entities) — standard OOP may be simpler and adequate.
- You haven't identified the core systems yet — produce a system roster first.

## 3. Quality Gates
- **Components are pure data**: Components contain only fields; all behavior lives in systems.
- **Systems communicate via events**: Use an event bus for inter-system communication instead of direct method calls.
- **Systems remain stateless**: All state/data stored in components or external stores, never inside system implementations.
- **Archetype-based layout optimization**: Architectures prioritize cache locality through archetype grouping.
- **Scale-appropriate designs**: Proposed architectures must handle specified entity counts (e.g., 1,000+ entities).

## 3. Interaction Protocol

### Workflow
1.  **Entity Inventory & Scale Assessment**: Identify all entity types and approximate simultaneous counts to determine scale requirements. Reference `{TARGET_FOLDER}/docs/system_roster.md` for P0 identification.
2.  **Component Definition**: Define pure, data-only components for each entity type; ensure no methods or logic are included.
3.  **Archetype Grouping**: Organize entities into archetypes based on unique component combinations to optimize memory layout and access patterns.
4.  **System Specification**: Define stateless systems by specifying: Reads, Writes, Emits (events), Frequency, and Logic. Use `{TARGET_FOLDER}/docs/events_spec.md` for event definitions.
5.  **Architecture Validation**: Verify against the "Iron Law": No state in systems, no logic in components, and strict separation via events.
6.  **Specification Export**: Formalize findings into `{TARGET_FOLDER}/docs/ecs_spec.md`.

### Error Handling & Intercepts
- **[OOP Pattern Intercept]**: If user describes methods within components: *"I notice you're describing methods within components. In ECS, components must be pure data. I will strip the methods and focus on the data fields to maintain DOD integrity. Proceed?"*
- **[Tight Coupling Intercept]**: If a system is described as calling another directly: *"Systems should not call each other directly. I will convert that interaction into an event-driven pattern using the 'On...' event format to maintain decoupling. Proceed?"*

## 4. Language
All output MUST be in English. No exceptions.
