---
name: c4-diagrams
description: Use when explaining existing architecture, visualizing a new system before detailed design, mapping software boundaries, or creating C4-style ASCII or Mermaid diagrams.
license: MIT
compatibility: Codex lazy-loaded skill for OpenSpec projects.
---

# C4 Diagrams

Use this optional skill only after recommendation and user consent.

Focus on boundaries, responsibilities, actors, dependencies, and data flow.
Draw only the levels that answer the current question.

## First Gates

Establish purpose, format, and rigor. If the user has not specified them, ask a
single concise question.

- Purpose: existing code, new system, design review.
- Format: ASCII or Mermaid.
- Rigor: strict C4, lightweight C4-inspired, or hybrid.

## Workflow

1. For existing code, inspect entry points, runtime boundaries, integrations,
   persistence, and major directories before diagramming.
2. Pick the smallest useful diagram set: system context, container, component,
   dynamic, or deployment.
3. Draw in ASCII or plain Mermaid `flowchart` / `sequenceDiagram`.
4. Explain boundaries, responsibilities, assumptions, and open questions in
   3-6 bullets.
5. Stop before detailed design unless the user asks to continue.

## Output Rules

- Containers are runnable or deployable units.
- Components live inside one container.
- Do not hide uncertainty; label assumptions and unknowns.
- Avoid drawing all C4 levels by default.
