---
name: clean-code
description: "Write readable maintainable code: clear names, small units, low coupling, high cohesion. Optimize for changeability, not abstraction count; do not over-engineer."
---

# clean-code

Optimize for changeability, not abstraction count. Small, named, tested units with one reason to change.

## Activate when

- Writing or reviewing any code for readability/maintainability; naming, sizing, or duplication decisions.

## Do NOT activate for

- Architectural pattern choice (see architecture/*, language-modularity); formatting-only (see tooling/formatting).

## Procedure

1. Names: reveal intent, pronounceable, consistent with the domain glossary; no encodings, no lies.
2. Units: small functions/modules with one reason to change; nesting shallow; control flow explicit; no boolean-parameter explosions.
3. Duplication: remove real duplication (rule of three); do NOT abstract on speculation (YAGNI); DRY for knowledge, not keystrokes.
4. Smells that block: god modules/classes, hidden temporal coupling, global mutable state, circular deps, leaky abstractions, swallowed errors, stringly-typed APIs.
5. Anti-over-engineering: every abstraction must name its second caller or the volatile dependency it protects; otherwise inline.
6. Verify: reviewer can state each unit's contract in one sentence; complexity down or justified; tests unaffected in behavior.
