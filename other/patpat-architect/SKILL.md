---
name: patpat-architect
description: Design a repository-native change before implementation. Use for architecture, migrations, public contracts, security-sensitive boundaries, cross-cutting work, or decisions with meaningful compatibility risk.
---

# Patpat Architect

When invoked directly, read the [operating protocol](../patpat-loop/references/operating-protocol.md) in full. Do not load the router.

Read [repository truth](../patpat-loop/principles/repository-truth.md), [smallest safe change](../patpat-loop/principles/smallest-safe-change.md), and [preserve safety](../patpat-loop/principles/preserve-safety.md). Apply the [architecture change playbook](../patpat-loop/playbooks/architecture-change.md).

Ground the design in current repository evidence. Name the contract, its callers, the changed behavior, migration impact, compatibility risk, rollback path, and proof contract.

For a material architecture decision or a change that crosses a meaningful boundary, the architecture output must include a compact caller usage sketch, the core data or type shape, boundary-relevant signatures, failure modes, rejected alternatives, and the proof that will show implementation still preserves the chosen shape. If implementation needs an unplanned parameter, state escape hatch, or compatibility path, stop and revisit the sketch before adding a workaround. Keep smaller local changes on the bounded-change path.

Prefer a design that reduces degrees of freedom and reuses repository structure. When proposing structural change, prefer a compact before/after or flow from [earned representation](../patpat-loop/references/earned-representation.md). Seek independent review before implementing auth, billing, permissions, destructive migrations, production infrastructure, or public contract changes. Stop for explicit approval when required.

Keep architecture work read-only by default. Do not edit implementation files. When the user also requested implementation, finish the design gate and hand the authorized unit to `patpat-change` under `patpat-loop` instead of implementing inside this workflow.

When an observable experiment can settle a design fork, apply the [prototype playbook](../patpat-loop/playbooks/prototype.md). Keep prototypes in an isolated scratch area outside production paths and treat them as disposable evidence, not implementation.

Produce a concise sequence in this form:

```text
1. <step> -> verify: <targeted check or observation>
2. <step> -> verify: <targeted check or observation>
```

## Mutation boundary

Remain read-only with respect to repository implementation and external delivery. Limit incidental verifier artifacts to the declared proof contract, clean them up, and hand any authorized mutation back to `patpat-loop`.
