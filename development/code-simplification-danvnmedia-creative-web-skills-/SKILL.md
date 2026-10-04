---
name: code-simplification
description: Use after behavior is verified to simplify recently changed code for clarity and maintainability without changing product behavior, public contracts, or validated security/performance properties.
---
# Code Simplification

1. Operate only on recently changed scope unless explicitly asked broader.
2. Preserve exact behavior and public contracts.
3. Prefer explicit readable control flow over clever density.
4. Remove accidental duplication and unnecessary abstraction; preserve abstractions that encode real boundaries.
5. Avoid combining unrelated concerns or performing speculative refactors.
6. Rerun the relevant fresh checks after simplification because prior evidence may be stale.
