---
name: project-modeling
description: "Build one canonical project model — entities, boundaries, owners, lifecycle state, and end-to-end traces — and record its authoritative names in `00-control/terminology-and-ownership.md` (`TM-####`), then project that single model into every audience view without ever forking it. Use when starting Phase 2, when the project type is ambiguous, or when two documents describe the same component differently. This skill MUST be consulted because multiple independent mental models produce documents that contradict each other under diligence, and audience-specific rewriting is the single most common source of drift in a documentation package."
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
context: fork
agent: Explore
---

# Project Modeling

Phase 2. Builds the one model that all 23 documents are views over, and the vocabulary they all use.

## Iron Law

**ONE MODEL, MANY VIEWS. If a view needs a new fact, the fact goes in the model first.**

The moment a document invents a component name, an owner, or a boundary that the model does not carry, the package has two models. It will not notice, and the contradiction surfaces during diligence rather than during drafting.

## What the model contains

| Element | Captures | Where it surfaces |
|---|---|---|
| Product intent vs implemented behaviour | What it is for, and what it actually does — separately | `01-project/` |
| Actors, journeys, roles, permissions | Who does what, and what they may do | `01-project/`, `02-architecture/` |
| Components and deployment units | Purpose, owner, runtime, interfaces, state, criticality | `02-architecture/components-and-codebase.md` |
| Interfaces and contracts | Producers, consumers, transport, versioning | `02-architecture/interfaces-and-integrations.md` |
| Data and its lifecycle | Stores, classes, residency, retention, deletion | `02-architecture/data-and-ai.md` |
| Infrastructure and environments | Topology, promotion path, differences between environments | `02-architecture/infrastructure-and-deployment.md` |
| Boundaries | Control, data, trust, failure, tenancy | Everywhere. The most load-bearing element |
| Owners and decision rights | Who owns, who decides, who escalates | `00-control/terminology-and-ownership.md` |
| Lifecycle and target state | What exists now vs what is planned | Every document, kept visibly distinct |
| Assets, dependencies, licenses, risks | Provenance and exposure | `05-due-diligence/` |

Every element is an evidence-backed claim. A component with no evidenced owner is `unassigned` — never the last committer, never the most active contributor. During an incident, a fabricated owner is worse than an admitted gap.

## Classify first

Classify the project from evidence before modelling it, and record the classification with its supporting evidence IDs. The classification changes which elements carry weight — not which files exist. See `references/project-type-adaptation.md`.

Do not force web-service assumptions onto a library, a model, a device, or an offline tool. A library's "deployment" is a registry publish; a device's "rollback" may not exist at all.

## Test the model against three flows

A model that has not been walked end to end is a diagram, not a model. Trace at least:

1. **One primary user or business flow** — entry point through to the effect the user cares about
2. **One change-to-production flow** — commit through test, review, build, deploy, and rollback
3. **One credible failure, recovery, or abuse flow** — a dependency outage, a partial failure, a malicious input, or an incident from alert to recovery

Where one is genuinely inapplicable, substitute a different flow and **explain why** — never silently drop it. A project with no deployment still has an artifact-publication flow; a project with no users still has a consumer.

Each trace either confirms the model or produces a gap. Both outcomes are valuable; only the first is comfortable. Trace failures become `AQ-` or `CT-` rows before any drafting begins, because a model corrected in Phase 2 costs one edit and a model corrected in Phase 6 costs a rewrite of everything downstream.

These same traces are what verification pass B later attempts to falsify. Record them explicitly so the pass can execute them independently rather than inventing its own.

## Canonical names

Every entity gets one authoritative name in `TM-####`, plus its aliases. Aliases are not noise — source material genuinely uses old names, and a reader who greps for the old one must land somewhere.

Name these classes: product and project; components, services, modules, repositories, packages; user, customer, administrator, and operator roles; environments and deployment units; external systems and partners; data classes and domain entities; interfaces and events; owners and teams.

Once recorded, the canonical name is used in **all** documents. A document that calls the same service by two names inside one file is a Medium finding; two documents disagreeing is a High one, because a reader cannot tell whether they describe one system or two.

## Projecting to views

A view **selects and abstracts**. It never adds.

| Legitimate | Illegitimate |
|---|---|
| Omitting internal components from a partner view | Renaming a component to sound cleaner externally |
| Generalizing "PostgreSQL 15 on RDS" to "a managed relational database" | Describing a boundary that the model does not carry |
| Dropping evidence IDs from public text | Dropping a limitation that made the claim true |
| Summarizing five failure modes as "degrades to read-only" **when that is what all five do** | Summarizing them that way when one does not |

The public projection has its own rules and its own gate — see `disclosure-gating`. This skill's obligation is narrower and absolute: the underlying model must be identical across every view.

## Current versus target

Keep them visibly separate in the model itself, not just in prose. A model that merges "the planned event bus" with "the current synchronous call" produces an architecture document describing a system nobody has built.

Planned elements carry a `planned` marker and the evidence for the plan — an approved decision record, not a conversation. A plan with no approved record is `R` at best and frequently `U`.

## Output Format

Write the model to `<outputRoot>/00-control/.project-model.json` and the vocabulary to `00-control/terminology-and-ownership.md`.

```markdown
## Canonical Entities

| ID | Canonical name | Class | Aliases | Definition | Owner | Evidence |
|---|---|---|---|---|---|---|
| TM-0001 | {name} | component / role / environment / data-class / interface / external-system | {old names} | {one sentence} | {role or `unassigned`} | [EV-####] |

## Ownership

| Area | Component owner | Decision owner | Operational owner | Documentation owner | Bus-factor concern |
|---|---|---|---|---|---|

## End-to-End Traces

### Trace {N}: {name} ({primary | change-to-production | failure})
| Step | Component | Interface | State touched | Evidence | Confirms or contradicts model |
|---|---|---|---|---|---|
```

The ownership table's `unassigned` entries and bus-factor concerns feed `05-due-diligence/` directly. Do not soften them.

## Rationalization Prevention

| Excuse | Response |
|--------|----------|
| "The partner guide needs a simpler name for this service" | Then the canonical name is wrong, or the simplification is a lie. Fix one; do not maintain two. |
| "I will trace the flows after drafting the architecture" | Then the architecture document is a hypothesis and everything downstream inherits its errors. |
| "This component has no owner in any file, but Alex touches it most" | `unassigned`. Commit frequency is not ownership, and paging the wrong person at 3am is a real cost. |
| "The diagram is clearer if I add this connection" | Every node and edge needs evidence. An inferred connection is labelled inferred, in the internal document, or it is not drawn. |
| "The team is migrating to the new architecture, so I will document that" | Document what exists, mark what is planned, and cite the approved decision. A target state written as current is a false statement. |
| "Both names appear in the code, so both are canonical" | One is canonical, the other is an alias. Pick using evidence and record the alias. |
| "The third trace does not apply to this project" | Then substitute one and say why. Silently running two traces is not running three. |

## Integration

Invoked in Phase 2 of `/dossier:baseline` and re-validated by `/dossier:refresh` when the blast radius touches components, interfaces, data, or infrastructure. Loaded by `dossier-pass-b-falsification`, which attempts to break the traces recorded here. Every `dossier-doc-drafter` dispatch receives the model as input.

References: `references/project-type-adaptation.md`, `references/register-schemas.md`, `references/package-contract-02-architecture.md`.
