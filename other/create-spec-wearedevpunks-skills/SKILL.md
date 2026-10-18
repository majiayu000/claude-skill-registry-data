---
name: create-spec
description: Compile confirmed product decisions and retained ARCHITECTURE.md into SPEC.md. Use when requirements are closed or explicitly parked and a provider-neutral specification is needed before backlog or planning.
---

# Create Spec

`create-spec` is the no-interview compiler of confirmed decisions. Upstream
Wayfinder, research, prototyping, and grilling own uncertainty. This skill asks
no questions, runs no local grill, and performs no backlog mutation.

## Inputs

Require the current retained sibling `ARCHITECTURE.md` from `create-architecture`
with its verified immutable blob URL and exact source identities. Accept
confirmed decision evidence: grill status and logs, research reports,
prototype verdicts, ADRs, glossary, axioms, constraints, system facts, accepted
implementation and testing decisions, dependency evidence, and accepted
parent/base constraints. Provider backlog items may be source evidence, but
they are not specification identities or readiness prerequisites.

## Steps

Before naming or rewriting domain concepts, read the canonical glossary in the
routed `requirements-grill` status artifact. Preserve its canonical terms;
route proposed terminology changes through `requirements-grill` instead of
silently renaming them.

1. Resolve the planning surface using
   [folder-naming.md](references/folder-naming.md).
2. Validate readiness using [readiness.md](references/readiness.md). If required
   evidence is missing, return one atomic `spec-not-ready` result and write no
   partial `SPEC.md`.
3. Draft [SPEC-TEMPLATE.md](assets/SPEC-TEMPLATE.md). Preserve confirmed decisions
   and existing `OUT-###` / `AC-###` identities. Incorporate accepted architecture
   constraints and exact technical details without copying the narrative.
   Serialize `Dependency Readiness` and `Branch/Base Intent` using the readiness
   contract.
4. Invoke `$show-me` to place the completed spec's useful explanatory views in
   `SPEC.md`. Derive them only from confirmed decisions; add no approval gate or
   new closure. Finalize all spec content before mapping or retention.
5. Complete the [Spec traceability contract](../create-architecture/references/artifact-contract.md#spec-traceability)
   in `ARCHITECTURE.md` using the draft's real spec codes, stable architecture
   selectors and exact grill question/log-entry evidence anchors. This is a
   metadata-only amendment; new design decisions return to Requirements Grill.
   Validate complete mapping and both drafts before replacing either artifact.
6. Retain the enriched architecture first, using `create-architecture`'s retention
   contract. Verify its immutable blob URL and bytes, then record that final
   identity as the spec's `Architecture Source` and frontmatter link. Link each
   outcome and criterion back to its canonical architecture mapping and sections.
7. Apply [spec-quality-bar.md](references/spec-quality-bar.md).
8. Update existing planning-surface indexes through
   [wiki-bookkeeping.md](references/wiki-bookkeeping.md).
9. Persist the completed spec and bookkeeping in a dedicated git commit. Never
   stage unrelated changes.
10. Push or explicitly retain the spec commit through the repository-approved
    remote mechanism. Verify the retained ref contains the spec commit, and
    construct and verify its stable blob URL before `write-backlog` may consume it.
    A local commit SHA plus path is insufficient.
11. Return `spec-written`, `readiness: agent-ready`, and both verified immutable
    artifact URLs. If retention or URL verification fails, return one atomic
    `spec-not-ready` result and do not invoke backlog projection.

## Boundaries

- `SPEC.md` is the provider-neutral authority for resolved requirements. It
  identifies requirements and outcomes as `OUT-###`; these identifiers imply
  no provider Epic, Story, or Task identity or count.
- `write-backlog` receives only the verified stable blob URL, then derives or
  reuses the provider Epic, Stories, Tasks, and blocker graph supported by the
  compiled requirements and current provider evidence.
- A mutable path or local-only commit is not a backlog handoff.
- `ARCHITECTURE.md` is the source-attributed design companion; the spec owns
  resolved requirements, outcomes and acceptance criteria. Both must agree with
  current grill decisions. A conflict returns to Requirements Phase and
  `requirements-grill`; neither artifact silently overrides the other.
- Accepted architecture constraints and technical and testing decisions belong
  in the spec. Detailed task choreography does not. Architecture diagrams
  explain accepted decisions; they cannot accept new ones.
- `create-plan` preserves provider Task identities and owns files, commands,
  workers, and validation detail.
- `Dependency Readiness` and `Branch/Base Intent` preserve accepted dependency
  evidence and parent/base constraints for `create-plan`.
- `readiness: agent-ready` is sufficient downstream. Do not add a review or
  approval stop; pause only for a user-requested HITL checkpoint.
- Compiler state is `compiled`. Human approval, when explicitly requested, is
  a separate optional action and is never inferred or stamped by the compiler.
