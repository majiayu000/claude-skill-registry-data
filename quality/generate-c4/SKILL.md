---
name: generate-c4
description: Create, update, and review source-backed C4 architecture views using Mermaid by default. Use for system landscape, system context, container, component, dynamic, deployment, integration, or regulated-data-flow diagrams; when an ADD or ADR needs a view; or when an existing diagram must be checked for scope, evidence, consistency, and sensitive-data exposure.
---

# Generate C4

Use one skill with a view parameter; do not create a separate skill for every C4 level.

## Workflow

1. Read `AGENTS.md`, linked use cases, ADDs, ADRs, repository sources, and existing diagrams.
2. Identify the stakeholder question and requested state: `current`, `transition`, `target`, or `conceptual`.
3. Select one primary view with [references/c4-selection.md](references/c4-selection.md). Split mixed abstraction levels into separate files.
4. Build an evidence table for elements and relationships. Do not invent technologies, owners, protocols, boundaries, or flows.
5. Copy the closest Mermaid asset: [assets/context.mmd](assets/context.mmd), [assets/container.mmd](assets/container.mmd), [assets/component.mmd](assets/component.mmd), [assets/dynamic.mmd](assets/dynamic.mmd), or [assets/deployment.mmd](assets/deployment.mmd).
6. Add title, scope/state, legend, boundaries, directional relationship labels, and uncertainty markers.
7. Validate syntax with an available renderer and visually inspect rendered output when practical.
8. Save editable source and evidence under `architecture/diagrams/<system-slug>/`; keep any rendered SVG beside it.

## Rules

- Use business-recognizable names; put technology in a secondary label.
- Draw external actors/systems outside the system boundary.
- Label every material arrow with action/data and known interface/protocol.
- Mark regulated-data and trust-boundary crossings only when evidence supports them.
- Visually distinguish confirmed facts, proposals, and uncertainty.
- Never include personal/health records, credentials, secrets, connection strings, or sensitive endpoint details.
- Link the source ADD/ADR and link those artifacts back to the diagram.

## Output Names

```text
architecture/diagrams/<system>/<system>-<state>-<view>.mmd
architecture/diagrams/<system>/<system>-<state>-<view>.svg
architecture/diagrams/<system>/<system>-<state>-<view>-evidence.md
```

Return paths, the question answered, state/view, evidence gaps, validation result, and unresolved questions.
