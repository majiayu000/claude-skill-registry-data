---
name: extensibility
description: "Build extendable systems: ports/adapters, DI, stable interfaces. Abstract only on real duplication and stable concepts."
---

# extensibility

Extend without modifying: seams where variation is proven, simplicity everywhere else.

## Activate when

- A second caller/implementation appears, or a volatile dependency (I/O, vendor API, clock) needs isolation for tests.

## Do NOT activate for

- First implementations (write the simple thing); speculative "plugin systems" with one plugin.

## Inspection

Find the variation: who varies (callers, vendors, environments), how often it changed, and where tests currently can't reach.

## Decision rules

- Ports/adapters (hexagonal) only at trust or volatility boundaries: inbound ports for drivers, outbound ports for driven dependencies (DB, HTTP, clock, FS).
- DI: constructor injection of the port; no service locator; composition root at the edge.
- Stable interfaces: versioned when external; narrow when internal.
- Abstraction gate: a seam needs either two real callers or one volatile dependency — otherwise inline. Revisit when the second caller arrives.

## Procedure

1. Name the variation and its evidence (second caller or volatility + test need).
2. Extract the port (interface/protocol/trait), adapt the implementations, inject at the composition root.
3. Migrate existing callers through the port; delete the old direct path.
4. Verify: new variation added without touching existing code paths; old + new covered by contract tests.

## Failure modes

- Premature ports with one caller; leaky abstractions mirroring one vendor; DI containers hiding the object graph; God interfaces re-creating the coupling they replaced.

## Escalation

Cross-module seam design → modularity + language-modularity; cross-service → distributed/systems.

## References

- Related: `../modularity/`, `../solid/`, `../../core/refactoring/`.
