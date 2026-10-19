---
name: vanilla-first
description: "Use when the user requests a non-trivial tool or repository change where `supported capabilities, configuration, or extension points` may already fit. Do not use for: an obvious routine supported fix."
---

# Vanilla First

Find the smallest supported path that meets the user's outcome. Check the tool's existing capabilities and architecture before proposing custom code, while keeping operator authority distinct from another project's ownership.

Use this skill when a non-trivial implementation or architecture proposal could duplicate an existing tool capability, cross an owner boundary, depend on a specific version, or require a new integration. Keep the check brief when the fit is obvious. For a small, documented, reversible fix in an authorized repository, do the fix without a full ownership exercise.

## 1. Fix the requested outcome and owner

Capture the behavior the user needs, the material constraints, the exact product/repository/version when known, and who owns each affected boundary. Separate the user problem from a proposed implementation.

Use the existing issue or project record when it helps track non-trivial work; do not create one just to satisfy this skill. An ownership map is useful when several products, teams, or repositories are involved:

```text
behavior_or_contract: <needed behavior>
product_and_repository_owner: <who owns each affected surface>
maintainer_surface: <canonical issue, documentation, maintainer statement, or unknown>
state: <documented | owner_approved | proposal | investigation | unresolved>
```

Operator authority governs work in the user's own repository, local fork, and authorized environment. Do not require an external maintainer's preapproval for an ordinary supported fix or an authorized change to owned code. Maintainer acceptance matters when changing a contract that another product or team owns, or when claiming that an upstream contribution is accepted. Keep the local fork decision separate from permission to merge or advertise the change as upstream behavior.

## 2. Check the exact supported capability

For the relevant version and surface, inspect the closest official documentation and the source, CLI, API, or runtime entry point when available. Identify existing native tools, workflows, configuration, extension points, and services that could satisfy the outcome. Reuse relevant project guidance rather than searching unrelated systems.

Record the evidence for each important claim as one of:

- **Documented:** official documentation for the relevant version describes it.
- **Source-proven:** the checked-out source contains the route or behavior.
- **Test-proven:** a named test or checker exercises it.
- **Runtime-proven:** the actual configured runtime demonstrates it.
- **Unknown or unavailable:** evidence is missing; state the gap.

Keep the exact version, command/API/config path, owner, and artifact provenance when recommending an operational route. Do not turn a copied example, a similarly named setting, a green test, or an implementation guess into a supported contract. Do not claim runtime or end-to-end behavior from source inspection alone.

## 3. Compare the smallest coherent paths

Choose from the paths that actually fit; do not force a ladder or build an adapter for its own sake:

1. Use an existing supported capability when it meets the outcome.
2. Use documented configuration or compose supported components when that is sufficient.
3. Add a thin adapter at a supported seam when it closes a demonstrated gap.
4. Contribute to the owning upstream when the gap belongs there and the user wants that route.
5. Maintain a fork when the operator selects independent ownership, release control is required, or upstream timing cannot meet an authorized need.
6. Replace the core only when evidence shows the existing architecture cannot meet the requirements or measured future ownership costs justify replacement.

For user-owned code, a small direct change may be simpler and more supportable than a new adapter. State the actual gap before recommending custom code. Compare future maintenance, migration, security, support, and operator costs as well as initial effort; label estimates and market claims that lack evidence.

## 4. Respect the boundary that owns the behavior

A documented, supported change within an authorized owner boundary can proceed under the user's request. Routine configuration and fixes do not need an extra approval ritual.

Pause implementation of a material contract owned by another product/team when its acceptance is unresolved or explicitly rejected. Continue useful investigation or a local draft within the authorized scope, and name the exact owner decision needed. An issue label, contributor agreement, local prototype, test result, or open PR is not acceptance unless it covers this contract.

When an upstream maintainer rejects a design, stop repeated rebase, review, CI, or rating loops for that design. Preserve useful evidence and identify any genuinely separate, supported, owner-compatible path. The rejection does not decide whether the operator may implement a distinct local-fork solution; that remains an operator decision with its own scope and proof.

Before refreshing an upstream contribution, verify that the underlying issue is still live, current upstream still lacks the behavior, and no merged successor superseded the patch. An open PR alone is not evidence that work remains needed. Preserve authorship and describe accepted, partial, rejected, superseded, and unresolved states accurately.

## 5. Make and verify the authorized change

When implementation is requested and authorized, make the smallest coherent change that closes the demonstrated gap. Use the supported extension or configuration surface when one exists. Do not add a new service, dependency, fork, workflow, approval gate, or migration unless the outcome requires it.

Run the focused check for the changed behavior and inspect the resulting configuration, artifact, or runtime where the task requires it. Report proof at the level actually reached, plus what remains unverified. A recommendation-only request ends with the recommendation and evidence; it does not silently become implementation.

For a non-trivial outcome, a concise return should identify:

- the supported path considered and why it fits or falls short;
- the owner and any unresolved external contract;
- the smallest chosen change and why it preserves useful behavior;
- the exact version/command/source evidence and verification result;
- any important cost, migration, security, or support gap;
- whether the result is local, fork-only, proposed upstream, or accepted upstream.

Skip this report shape for a simple task whose result is self-evident. Do not send, publish, install, or change shared state without authority for that consequence.

## References

When ownership or path selection is contested, use [scenario checks](references/scenario-checks.md) to test the boundaries. For the sources and adaptations behind this skill, see [provenance](references/provenance.md).
