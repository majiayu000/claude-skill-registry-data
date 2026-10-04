---
name: c4-model
version: 1.0.0
description: Create or review C4 model architecture documentation (official c4model.com notation) as diagrams-as-code in Markdown — C4-PlantUML where the target renders it (GitLab.com does; verify Self-Managed instances), Mermaid flowchart/sequence conventions otherwise. Use whenever the user wants to visualize or document the architecture of a system or codebase — even if they never say "C4" — for requests like "diagram this service", "document the architecture", "how do the pieces of this repo fit together", "draw the system/containers/components", or when reviewing existing C4/Mermaid architecture diagrams for correctness. Covers system context, system landscape, container, component, dynamic, and deployment views. Do not use for generic flowcharts, ER diagrams, standalone Kubernetes topology, API contract documentation (OpenAPI/AsyncAPI), or architecture prose without diagrams.
---

# C4 Architecture Documentation

Generate C4 model architecture documentation as diagrams-as-code embedded in Markdown — in the selected notation — following the official guidance at c4model.com. The point of C4 is a small set of precise abstractions and views that stay consistent with each other — most of this skill exists to protect that precision.

## Workflow

1. **Read the repository's conventions first**: documentation language, existing architecture docs and where they live.
2. **Confirm purpose, audience, and scope.** Which views add value for this request? Context + Container is the recommended default set. Never generate every level by default — and if the user asks for one specific view, produce only that one.
3. **Separate current architecture from target architecture.** Mixing them in one view produces an ambiguous model; make two views when both are needed.
4. **Collect evidence before modeling** an existing codebase: read `references/codebase-analysis.md` and follow it. Never invent protocols, ownership, or elements the evidence does not support.
5. **Build one canonical model first**: the list of people, software systems, containers, components, and relationships — one name per element. Every view reuses these exact names; that is what makes the zoom between levels traceable.
6. **Choose the views.** Scope rules and abstraction definitions live in `references/c4-model-rules.md` — read it before modeling anything non-trivial.
7. **Generate each view** in the selected notation (see "Notation selection" below), following its rendering reference. Every view follows the output contract below.
8. **Validate**: self-review each diagram against the checklist at the end of `references/c4-model-rules.md`, and tell the user how to verify rendering on their GitLab instance.
9. **Report assumptions and unconfirmed data** explicitly in the output.

## Notation selection

Clarity is the reason this rule exists: diagram notations differ enormously in layout quality, and the C4 model is officially notation-independent.

1. If the target renders C4-PlantUML (GitLab.com does — verified 2026-08-19; for self-managed instances run the probe in `references/c4-plantuml.md`), use **C4-PlantUML for every view** → read `references/c4-plantuml.md`. Its Graphviz layout greatly reduces label overlaps and its legend is native.
2. Otherwise, use **Mermaid `flowchart` with C4 conventions** for static views and `sequenceDiagram` for dynamic views → read `references/mermaid-gitlab.md`.
3. If the user explicitly asks for Mermaid, respect that choice (rule 2 applies).
4. **Never generate Mermaid's native `C4Context`/`C4Container`/... syntax**: it is experimental, has no layout algorithm, and its relationship labels overlap boxes. Read it only when reviewing or converting existing documents.
5. Never mix both notations within the same document set.

## Non-negotiable rules

These come from the official C4 documentation (c4model.com) plus verified Mermaid behavior. Violating them produces diagrams that mislead.

**Levels and scope**
- Context, Container, Component, and Code are the four core levels. System Landscape, Dynamic, and Deployment are *supporting* diagrams — Deployment is not "level 4".
- One view, one scope: a Context covers one software system; a Landscape has no central system; a Container view covers one system's insides; a Component view covers exactly **one container**; a Deployment view covers **one environment** (development, staging, and production each get their own).
- There is no C4 code-level diagram type in either notation. If a code view is genuinely needed, use a UML class diagram and say so — better yet, generate it from the code on demand.

**Abstractions**
- A **container** is a runtime or data-storage boundary: an application, a database schema, a bucket, a queue or topic, a serverless function. Libraries, frameworks, and in-process state (an ORM, a state store inside a SPA) are NOT containers.
- A **component** groups related functionality behind a well-defined interface, inside one container. Never map packages, folders, files, or classes to components automatically — a component usually spans several of them.
- A **software system** delivers value to its users; team ownership is the usual boundary heuristic. Product domains, bounded contexts, business capabilities, and teams are not usually software systems.
- External systems are black boxes: never show the internal containers of a system outside the scope.

**Every diagram**
- Has a title stating the diagram type and scope ("Container diagram for X").
- Has a key explaining the notation actually used, and every acronym explained (in PlantUML mode `SHOW_LEGEND(false)` renders it; in Mermaid mode the key is a Markdown section — see the output contract).
- Every element shows name, type, and a short responsibility description. Every container and component states its technology. Native C4 elements carry their responsibility inside the diagram; sequence-notation participants keep compact labels, so state every participant's responsibility in the same Markdown unit (intro text or a compact participant table) — the view must stand alone.

**Relationships**
- Unidirectional, with a specific label that reads correctly in the arrow's direction — never a bare "Uses". Never use `BiRel`.
- Container-to-container relationships state the technology/protocol. Context and Landscape views do NOT: they focus on people and systems, not technology.
- A relationship can express dependency ("reads from") or data flow ("sends events to") — pick one interpretation per diagram and make labels match the arrows.

**Dynamic and Deployment**
- Dynamic views always use sequence notation: `<C4/C4_Sequence>` in PlantUML mode, `sequenceDiagram` in Mermaid mode. Never number message labels manually — ordering is the vertical order.
- A Deployment view shows *instances* of already-defined systems and containers running on deployment nodes. Kubernetes clusters and pods are deployment nodes, not C4 containers. DNS and load balancers are infrastructure nodes — never invent them as applications.

**Legibility**
- If a diagram becomes difficult to understand, split it into focused diagrams at the same abstraction level — by business area, functional grouping, use case, or a per-service view with its nearby inbound and outbound dependencies.
- Use the notation's standard C4 styling: C4-PlantUML's defaults, or the fixed palette defined in the Mermaid fallback reference. Add further colors only when they carry meaning the key explains (mind printers and color blindness).

## Output contract

Each diagram forms one complete Markdown unit:

````markdown
## Container diagram for <System>

One or two sentences: what this view shows and for whom.

```<plantuml or mermaid — the selected notation>
<the diagram code, per the selected rendering reference>
```

### Key   <!-- always in Mermaid mode; in PlantUML mode only for what SHOW_LEGEND cannot explain -->


| Notation | Meaning |
|---|---|
| Person | Human role that interacts with the system |
| Container | Application or data store inside the system |
| External system | System outside the current scope |
| Arrow | Directed relationship, labeled from the initiator |

### Acronyms

| Acronym | Meaning |
|---|---|
| ... | ... |

### Scope and assumptions

- This view represents <environment / current vs target>.
- <Unconfirmed items, if any.>

### Evidence

- `cmd/api/main.go`: the API process.
- `deploy/values-prod.yaml`: replica count.
````

Section rules: heading, intro, and diagram block — always. Key — always in Mermaid mode; in C4-PlantUML mode `SHOW_LEGEND(false)` replaces the notation table, so the Markdown Key shrinks to only what the legend cannot explain (sequence constructs like `alt`/dashed responses) or disappears. Acronyms — only when the diagram uses acronyms, and count the ones inside relationship labels too; do not introduce unnecessary ones. Scope — always, one line is fine; assumptions — only when they exist. Evidence — required when documenting an existing codebase; omit for conceptual or target designs. The Key explains only the notation this diagram uses, not all of C4.

## Output location

Priority order: (1) the location the user asked for; (2) the repository's conventions; (3) an existing architecture-docs location; (4) propose a new one (e.g. `docs/architecture/`) only when none of the above exists.

## Language

Write output documentation in the repository's established language; otherwise use the user's language. Element names follow the codebase's own naming either way.

## References

- `references/c4-model-rules.md` — the C4 model itself: abstractions, view scopes, microservices, queues, coherence, the self-review checklist. Read before modeling anything non-trivial.
- `references/c4-plantuml.md` — the primary notation: C4-PlantUML as GitLab renders it, with the verified support matrix, per-view includes, sequence and deployment rules, and the instance probe. Read before writing PlantUML diagram code.
- `references/mermaid-gitlab.md` — the fallback notation: Mermaid `flowchart` with C4 conventions plus `sequenceDiagram`, and review-only notes on Mermaid's native C4 syntax. Read before writing Mermaid diagram code.
- `references/codebase-analysis.md` — evidence-to-element mapping for real repositories (processes, schemas, queues, Kubernetes, CI). Read when documenting an existing codebase.
