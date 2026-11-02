---
name: nexora-mod-resource-quota
description: "Enforces per-mod CPU, memory, entity, asset, and network quotas to prevent one extension from exhausting shared resources."
---

# nexora mod resource quota

## Purpose

Use this workflow for NEXORA-scale engine work when mod resource quotas and denial of service. Inspect the current code before proposing implementation details; do not assume an unverified subsystem exists.

## Required inputs

- Relevant source files, owning crates/modules, and the current diff or incident.
- Acceptance criteria, compatibility constraints, and known resource budgets.
- Existing tests, logs, fixtures, and reproduction steps where available.
- Explicit unknowns and assumptions requiring confirmation.

## Workflow

1. Define measurable resource classes and accounting ownership.
2. assign per-mod limits and global ceilings.
3. charge work before expensive allocation or dispatch.
4. prevent quota bypass through shared handles.
5. define throttling and rejection semantics.
6. test concurrent and nested requests.
7. release reservations on cancellation and unload.
8. expose usage and denial metrics.
9. document trusted-mod exceptions.

## Validation checklist

- [ ] The invariant and measurable acceptance criteria are explicit.
- [ ] Ownership, lifecycle, and failure handling are documented.
- [ ] Tests cover normal, boundary, repeated, and failure cases.
- [ ] Changes preserve source/plugin byte parity and catalog uniqueness.
- [ ] Focused tests, formatting, and applicable static checks pass; skipped checks are listed.
- [ ] Performance and reliability claims include reproducible evidence.

## Required output

Provide the decision and scope, invariants, code paths reviewed or changed, tests and results, compatibility implications, and unresolved risks.

## Boundaries and failure handling

Per-mod usage is bounded and quota enforcement cannot be bypassed through shared-resource APIs.

Do not rely on cooperative declarations alone. Keep accounting consistent across async tasks and shared allocations.

## Trigger examples

- **Positive:** A code change or incident directly involves mod resource quotas and denial of service and needs reproducible validation.
- **Positive:** Reviewers need explicit invariants, boundary cases, and failure recovery for this subsystem.
- **Negative:** The task is unrelated to this subsystem or asks for speculative changes without source evidence.
- **Negative:** The request is only documentation/content work with no runtime or code behavior impact.
