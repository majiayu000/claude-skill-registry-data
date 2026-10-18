---
name: write-backlog
description: Reconcile or materialize a coherent Linear or GitHub product backlog from accepted Finder, project-initialization, Normalization, planning, or delivery intent.
---

# Write Backlog

`write-backlog` is the sole physical provider mutation authority. Callers supply
semantic intent and evidence; this skill owns reconciliation, preview, provider
writes, exact readback, and residual delta. Provider adapters translate
representation and never redefine product hierarchy policy.

Before naming or rewriting domain concepts, read the canonical glossary in the
routed `requirements-grill` status artifact. Preserve its canonical terms.
Route proposed terminology changes through `requirements-grill` instead of
silently renaming them.

## Mutation Pipeline

1. Read [project context](references/project-context.md). Resolve settings,
   Product/Backlog Root, wiki, repository, actual provider workspace, and
   authenticated user. A missing or legacy destination returns exact
   `hi ensure` guidance and zero writes. Completion means every destination
   identity and the authenticated user are proven.
2. Read fresh provider state for every intended object, parent, relation,
   milestone, field, and view. Completion means the current topology is known
   by stable provider identity, not inferred from names.
3. Read [the mutation envelope](REFERENCE.md) and
   [identity reconciliation](references/issue-reconciliation.md). After a
   complete provider search, create on zero stable matches, enrich one stable
   match carrying the same durable wiki identity, and stop on ambiguity,
   conflict, or an incomplete search. Completion means every object has one
   fail-closed create, reuse, enrich, or unchanged decision.
4. Load exactly one semantic branch:
   - [initialize or reconstruct a backlog](references/backlog-initialization.md)
   - [ensure Fog, Grilling, or Research/Prototype intake](references/fog-intake.md)
   - [project Business evidence to the Initiative ceiling](references/business-projection.md)
   - [project Functional evidence to the Epic ceiling](references/functional-projection.md)
   - [derive delivery structure from an immutable specification](references/technical-projection.md)
   - [normalize current backlog state](references/normalization.md)
   - [record observed delivery state](references/delivery-status.md)
5. Construct the complete intended delta in memory. Validate authority, stable
   identity, provider-neutral hierarchy, adapter representation, source links,
   contextual `V*` membership, created-Task assignees, and the full reachable
   Task blocker graph.
   Completion means validation accepts the whole delta before the first write.
6. Use `$show-me` to preview the authority-derived topology, then continue to
   the write without waiting for a reply. Boundary, goal, parent, roadmap,
   milestone movement, duplicate closure, merge, split, reparenting,
   reorganization, and divergent-topology repair are structural changes: the
   invocation plus accepted evidence authorizes them. Ambiguity, conflict, or
   missing authority still stops with zero writes. Completion means every
   structural change is previewed and recorded for the return envelope.
7. Apply `$wait-what` when proposed ticket wording or project terms do not land.
   Re-pitch in canonical language while preserving accepted meaning.
8. Select exactly one adapter from `backlogProvider`:
   - `Linear`: read [the Linear provider branch](references/providers/linear.md).
   - `GitHub`: read [the GitHub provider branch](references/providers/github.md).
   A missing hierarchy, metadata, milestone, relation, or readback capability
   returns setup guidance and zero provider mutations.
9. Write only the validated delta. Read back every intended identity,
   parent, relation, source link, field, view, milestone, status, and provider
   object. On partial failure, stop further writes and return observed writes
   plus the exact residual delta.
10. Return stable provider IDs and URLs, durable wiki identities, operation,
   created/enriched/repaired/unchanged classification, structural changes, exact
   readback, and residual delta. Completion requires the return envelope to
   reconcile byte-for-byte with the intended provider state.

## Provider-Neutral Invariants

```text
Product/Backlog Root
└── Product Area
    └── Initiative
        └── Epic
            └── Story [one contextual V*]
                └── Task [same V* + blockers when derived]

Fog ──provenance/enrichment──> Product Area | Initiative | Epic | Story | Task
```

- Business Finder projection stops at Product Area and Initiative.
- Functional Finder projection may project that Business structure plus Epics.
  Neither Finder branch creates Stories or Tasks.
- Delivery projection consumes an agent-ready `SPEC.md` through its
  verified stable blob URL. Neutral `OUT-###` outcomes remain traceability
  while Write Backlog derives or reuses the Product Area, Initiative, Epic,
  Story, and Task identities
  supported by the requirements. Outcome count prescribes no item count.
- Every Story has exactly one contextual `V*` milestone. Every derived Task has
  its Story's milestone. Product Areas, Initiatives, and Epics may span
  iterations.
- Blockers, rather than list or milestone order, define precedence. Validate
  the complete reachable graph before mutation.
- Fog is lateral provenance, never a hierarchy parent. Historical staged
  tickets remain unchanged unless a separately authorized operation targets an
  exact ticket.

## Body Contract

Every written ticket remains understandable from its immutable specification
authority. Preserve applicable `OUT-###`/`AC-###` traceability, source links,
accepted wording, non-goals, dependencies, and provider-native relations.
Add a compact `$show-me` visual when the relationships are harder to understand than the prose.
The visual does not replace traceability, immutable evidence, or
provider-native relations.
Concrete files, commands, workers, and execution notes stay in planning and
delivery artifacts.

See [examples](EXAMPLES.md) for representative results. Finder, Requirements,
planning, and delivery callers never perform provider writes themselves.
