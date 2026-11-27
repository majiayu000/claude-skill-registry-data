---
name: simplify-design
description: "Refactor a .NET design toward KISS/DRY/YAGNI without behavior changes, excess abstractions or unrelated churn."
---

# Simplify deliberately
- State complexity pain in concrete terms: change amplification, duplicate logic, hidden flow, excessive allocations or unclear naming.
- Identify unnecessary service/repository/interface layers, one-use factories, `Helpers/Utils`, broad base classes and redundant DTO mappings.
- Reduce indirection without crossing meaningful domain/module boundaries or losing testability/security.
- Preserve external behavior and database contracts; add safety tests first; small steps and measure readability impact.
- Avoid cosmetic project-wide rewrite and don't use patterns as trophies.
