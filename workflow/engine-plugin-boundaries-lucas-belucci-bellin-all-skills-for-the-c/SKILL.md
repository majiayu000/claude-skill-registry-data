---
name: engine-plugin-boundaries
description: "Designs module and plugin boundaries for extensible engines. Use when separating runtime, renderer, physics, world generation, scripting, or user-created extensions."
---

# Engine Plugin Boundaries

## Use when
Engine modules form circular dependencies or extensions require private internal state and fragile load ordering.

## Workflow
1. Draw the dependency graph and identify stable concepts versus implementation-owned data.
2. Assign ownership for initialization, shutdown, resources, event delivery, errors, and version negotiation.
3. Define narrow capability-based interfaces and validate extension metadata before loading executable content.
4. Test missing, stale, partially initialized, and failing plugins with explicit cleanup expectations.

## Required output
A module graph, public API map, lifecycle contract, and extension compatibility test plan.

## Validation
- Core modules can compile/test without unrelated engine subsystems.
- Initialization and shutdown order are deterministic and observable.
- Failure of an optional plugin does not corrupt the engine core.

## Guardrails
Do not load untrusted native plugin binaries in-process without a deliberate trust and isolation model.
