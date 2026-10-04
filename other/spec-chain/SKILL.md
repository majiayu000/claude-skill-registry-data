---
name: spec-chain
description: "Preserve an approved specification through a complete implementation plan and execution. Use for major refactors, migrations, or multi-session work when a confirmed spec is authoritative; keep scope and order changes explicit."
---

# Spec Chain

Preserve an approved specification from planning through execution. The specification defines the required outcome and acceptance contract; the plan defines implementation order and technique.

## Authority

- Treat the accepted specification as the canonical authority for **what** must be implemented, **why** it exists, and **how completion is accepted**.
- Agent-authored specifications, plans, decision logs, handoffs, PR descriptions, and implementation commits are derived material. An agent-authored artifact does not become approved authority merely because it is newer, more detailed, executable, or already implemented; require evidenced applicable approval when it changes programme order, trust boundaries, or product meaning.
- A plan presented as the implementation plan for that specification must cover its entire accepted implementation scope.
- A phase, milestone, or current tranche may subdivide execution, but it may not replace the complete implementation plan or be presented as though it covers the whole specification.
- Keep explicit non-goals excluded. Keep unresolved decisions inside the full plan as decision-closing prerequisites or blockers; do not make them disappear by narrowing the plan.
- Preserve settled semantics such as naming, cardinality, ownership, compatibility, and migration behavior. Implementation convenience is not authority to reopen them.

## Establish the source contract

Before planning or editing, identify:

- Canonical specification path
- Accepted revision or commit
- Approval state and any named open decisions
- Repository baseline the specification was grounded against
- Current implementation state where it may have moved
- Present consumer, current requirement, and authorization provenance when the specification proposes a generalized protocol, new infrastructure, or a programme reorder

Use a stable path plus revision or commit. Do not calculate a hash unless an actual identity or integrity decision needs it.

If several documents contribute requirements, name one primary specification and list the exact normative companions. Do not silently choose whichever document makes the next slice smaller.

If artifacts disagree, resolve their authority rather than using recency or implementation completeness as a proxy for approval. A research implementation may remain valuable evidence while staying outside the accepted product programme.

## Build the complete implementation plan

When the request is for the full specification, create one program-level plan over the full accepted scope. An explicitly bounded tranche request needs only its applicable requirements, dependencies, and stopping point. Link an existing complete plan; if absent, note that fact and resolve only dependencies that block the tranche. Do not expand the request into whole-program planning. Retain the existing status of other requirements; do not replan them or imply they were delivered in this request.

For a full-spec plan:

1. Extract normative requirements, settled decisions, acceptance criteria, migrations, compatibility obligations, and retained non-goals.
2. Refer to existing IDs or headings instead of copying specification prose. When the specification lacks stable identifiers, create compact plan-local IDs tied to its headings.
3. Map every accepted requirement to an implementation slice and verification outcome.
4. Order slices by real dependencies. A different order from the specification is allowed only when the plan records the dependency rationale and preserves the same outcome.
5. Identify the current execution tranche without removing later slices from the program plan.
6. Include decision-closing work before any slice that depends on an unresolved product or destructive choice.

The plan may use several PRs, releases, or sessions. Full coverage does not require a mega-PR.

## Required plan contract

For a full-spec plan, keep the artifact compact and include the sections below. A tranche-only request uses the applicable subset and specification links; it does not need a whole-program coverage ledger or sequence.

### Spec authority

- Canonical path and accepted revision
- Normative companion documents, if any
- Repository baseline and freshness note

### Complete coverage ledger

For each requirement or acceptance ID, record:

- Intended outcome
- Owning implementation slice
- Dependency or decision gate
- Verification evidence
- Status: `planned`, `blocked-decision`, `in-progress`, `implemented`, or `verified`

`planned` may be scheduled later. An accepted requirement cannot be marked out of scope merely because it is outside the current tranche.

### Dependency order

Show the full program sequence or dependency graph. Distinguish definition, enforcement, migration, activation, and deployment when the specification distinguishes them.

### Scope and order deltas

List every proposed `added`, `removed`, `narrowed`, or `reordered` item with:

- Affected specification IDs
- Reason and impact
- Whether it changes product meaning or only implementation technique
- Required decision owner

No entry means no delta. Never hide a scope change inside “minimal,” “first slice,” “later,” or “implementation detail.” Obtain explicit approval before adopting a product or acceptance delta.

### Execution tranches

Name the current tranche and its stopping point. Keep later accepted scope reachable through the specification or existing complete plan. Label a tranche document `Execution Tranche`, not “the implementation plan for the specification.” Link the complete plan when one exists; otherwise link the relevant specification anchors and state the planning boundary.

### Full acceptance

Define completion against the specification coverage ledger, not only the current tranche checklist.

## Execute without losing the specification

At execution entry, read:

- The accepted specification and normative companions
- The complete implementation plan when it exists or the request requires one
- The current execution tranche, when separate
- Current repository instructions and directly affected code/tests

Before editing, check coverage against the requested scope. A full-spec plan must still cover the complete accepted specification. Repair a partial phase plan masquerading as the full plan before relying on that claim; an explicitly bounded tranche needs its applicable requirements and settled dependencies.

During implementation:

- Adapt file paths, internal abstractions, and test mechanics when repository evidence supports the same contract.
- Record any scope, meaning, acceptance, or dependency change as an explicit delta before proceeding.
- Update the coverage ledger as evidence lands.
- Report tranche completion separately from full-spec completion.
- Keep implementation, merge, migration, deployment, and live-state activation as separate authorization gates.

Do not claim the specification is implemented until every accepted coverage item is implemented and verified at the appropriate risk level.

## Token discipline

- Link to specification anchors; do not restate the document.
- Maintain one coverage ledger instead of duplicating requirements across checklists.
- Record deltas only when they exist.
- Do not add separate reviewers, hashes, or ceremonial checkpoints by default.
- Automate coverage checks only when stable IDs and repeated use make the script cheaper than manual reconciliation.

## Regression guard

If a specification settles one public operation over a package of one or many items, a plan may not implement single-item behavior first and defer package cardinality unless the specification is explicitly amended. More generally, an easier subset is not an implementation plan for the whole contract.
