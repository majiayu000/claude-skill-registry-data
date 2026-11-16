---
name: refactor-safely
description: Restructure code while preserving externally observable behavior. Use for cleanup, modularization, naming, or simplification where behavior should remain unchanged.
---

# Safe Refactoring

1. Define the behavior that must remain stable and locate the tests that cover it.
2. Inspect the working tree and isolate unrelated user changes.
3. Establish a passing baseline or record existing failures.
4. Make one structural change at a time: extract, rename, move, or simplify without adding new behavior.
5. Keep public interfaces stable unless the request explicitly allows a breaking change.
6. Run focused tests after each meaningful step and the relevant suite at the end.
7. Compare before/after behavior and review the diff for accidental scope expansion.

Do not combine a broad refactor with a feature unless separation is impractical and the boundary is clear. Avoid cosmetic churn, speculative abstractions, and unrelated dead-code removal. If a behavior change becomes necessary, stop treating the work as a pure refactor and document the new contract.
