---
name: solid
description: "SOLID as diagnostic tool per language, not ceremony. Ask who owns behavior, what causes change, real boundaries. Never translate Java architecture mechanically into Go/Python/Rust/TS."
---

# solid

SOLID diagnoses pain; it does not prescribe shape. Apply per language, never by rote.

## Activate when

- A class/module keeps changing for different reasons, grows god-like, or resists testing.

## Do NOT activate for

- Greenfield scaffolding (structure there follows frameworks/*); justifying speculative abstractions.

## Inspection

Read the change history of the unit: who changed it, for what reasons, what broke. Count reasons-to-change, dependents, and test seams.

## Decision rules

- SRP: more than one change reason → split along the reasons, not along imagined reuse.
- OCP: extension without modification only where variation is proven (second caller exists). Otherwise a plain conditional is correct.
- LSP: subtypes must honor the contract — check with the supertype's tests, not by reading.
- ISP: fat interfaces force fake implementations → split by consumer (Go: consumer-defined interfaces; Python: Protocols).
- DIP: depend on abstractions at volatile boundaries (I/O, time, randomness) for testability — not everywhere.
- Language fit: Java/Spring favors constructor-injected interfaces; Python prefers Protocols/composition; Go small interfaces; Rust traits; TS structural types. Never transliterate Java hierarchies into Go/Python/Rust.

## Procedure

1. Name the pain (which principle's violation, with file:line evidence).
2. Apply the smallest fix satisfying the rule above; keep the public surface stable.
3. Add the test that would have caught the violation (e.g., a second implementation for DIP, a contract test for LSP).
4. Verify: the original pain scenario now has a seam; no speculative interfaces added.

## Failure modes

- Interface-per-class ritual; speculative OCP layers with one caller; LSP violations hidden by mocks; SOLID cited to force Java shapes into Go/Rust.

## Escalation

If the fix wants a cross-module redesign, stop and route via architecture/modularity + language-modularity.

## References

- Related: `../language-modularity/`, `../cohesion-coupling/`, `../../core/refactoring/`.
