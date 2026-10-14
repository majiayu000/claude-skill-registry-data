---
name: architecture-impact-review
description: "Trigger: architecture impact review, layer boundaries. Decide whether legacy risk is local or architectural."
license: Apache-2.0
metadata:
  author: gentle-ai
  adapted_by: andresnator
  source: gentle-ai/plan-refactor
  version: "1.1.3"
  status: testing
---

# Architecture Impact Review
Decide whether the target problem is local or architectural.

## Look for

- Layer violations.
- Domain logic mixed with infrastructure.
- Business logic in controllers, repositories, or DTOs.
- Circular dependencies.
- Coupled modules.
- God classes and services with too many responsibilities.
- Hidden business rules.
- Boundary-crossing dependencies.

Verify coupling, cycles, and boundary crossings from imports, build-file dependencies, or a code-graph index (for example, Graphify MCP/CLI) when available; every boundary claim cites `file:line`.

Keep broad architectural cleanup as follow-up unless it is required for safe characterization.

## Routing rules (local vs architectural)

- **Modules first, deployment last**: modularizing inside the current deployable is always the safe local move and belongs to refactor plans. Extracting a deployable (service) is an architectural decision — defer it to its last responsible moment, the point where not deciding would eliminate the alternative, and route it to the architecture domain.
- **Consistency boundary test**: components that must stay transactionally consistent belong in the same module (local concern); where eventual consistency and domain events are acceptable, a module boundary — and possibly an architectural decision — is in play.
- **Language boundary test**: when the same term means different things across the code under review ("policy", "account"), the scope is straddling a bounded-context boundary; escalate the boundary question instead of refactoring across it.
- **Problem nature test**: if nobody can predict whether the restructuring will work (a complex, experiment-first problem rather than a complicated, analyzable one), recommend the Plan discovery route (`operation=deep-plan intent=discovery`), not an executable change.
