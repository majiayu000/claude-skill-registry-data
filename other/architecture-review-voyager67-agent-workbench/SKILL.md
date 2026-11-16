---
name: architecture-review
description: Assess module boundaries and architectural change opportunities. Use when a codebase is becoming hard to change or a new feature crosses multiple components.
---

# Architecture Review

Treat architecture as a set of change-cost and responsibility trade-offs, not a diagram exercise.

1. Identify the user-facing behavior and the likely future changes the design must support.
2. Trace current responsibilities, dependencies, data ownership, and public interfaces.
3. Find concrete friction: duplicated policy, leaky abstractions, cyclic dependencies, too many reasons to change, hidden coupling, or difficult tests.
4. Propose the smallest boundary improvement that reduces a demonstrated cost.
5. Compare options by complexity, migration cost, failure isolation, performance, operational load, and reversibility.
6. Identify a seam where behavior can be tested without depending on internals.
7. Recommend a staged change and explain what should remain untouched.

Do not suggest a rewrite or new service merely because it is fashionable. Do not refactor code unrelated to the selected opportunity. Present evidence, alternatives, and a confidence level; architecture recommendations are hypotheses until validated in the codebase.
