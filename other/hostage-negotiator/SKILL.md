---
name: hostage-negotiator
description: Keep a small requested change focused when optional refactors, architectural redesign, or unrelated cleanup threaten to expand its scope.
---

# Hostage Negotiator

> Release the button. The architecture stays.

Read the requested behavior, existing implementation and local requirements together. Use actual paths; keep discovery, including instruction searches, inside the permitted project boundary.

For each supporting change, identify the acceptance condition that would fail without it. Implement that dependency, not adjacent improvements. Small scope does not mean few lines: necessary state, error handling, correctness and security remain required. Ask only for a missing material product decision.

Follow stateful behavior through entry, completion and recovery in its existing owner. Preserve results, errors and cancellation cleanup. Reuse existing tests; add checks for missing behavior rather than a parallel harness. Async checks must terminate when the implementation is broken: bound dependent waits and clean up controlled tasks.

Review the diff against acceptance conditions, preserving user changes and removing only your unjustified additions. A static edit needs no new test framework. Deliver the change, decisive verification and actual limits; stop when required behavior is verified. Review alone authorizes recommendations, not edits. Defer optional refactors; publication requires authorization.
