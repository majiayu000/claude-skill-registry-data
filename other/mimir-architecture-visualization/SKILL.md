---
name: mimir-architecture-visualization
description: Author architectural UML diagrams in Mermaid syntax from findings that describe a system's structure — components, modules, services, and their relationships.
---

# Architecture Visualization

## Purpose

When your research or analysis findings substantively describe a system's architecture — its components, modules, services, layers, and their structural relationships — author an architectural diagram to visualize that structure. The diagram is an analysis artifact: it makes the system's design explicit and traceable to the findings. This is not decorative illustration and not a substitute for written analysis.

## When to Use

- When your findings substantively describe a system's **architecture** — the structure of components, modules, services, or layers and how they relate to each other.
- The trigger judgment is yours: evaluate whether the material you are working with describes a system's architecture. If it does, a diagram is warranted.
- Do not diagram incidental process lists, taxonomies, or conceptual hierarchies unless they are part of describing the system's architecture itself (e.g., a data model that is part of the system's design, or a sequence that shows how components interact).
- When no architectural content is present, no diagram is produced.

## Diagram Types

Each type addresses a different architectural concern — system context (use case), static structure (component/class, object), runtime behavior (sequence, activity, state), or deployment topology (deployment/package). Choose the type whose concern matches what your findings actually describe:
- **Use case diagram** — the system's actors and what they use it for. *Not Mermaid-native* — approximate as a flowchart linking actors to functions, or use PlantUML when fidelity matters.
- **Component/class diagram** — module- and code-level structure: components, classes, and their relationships. *Mermaid: `classDiagram`* (components approximated via class stereotypes; no distinct native component-diagram type exists).
- **Object diagram** — concrete instances of classes and their links at a point in time; validates class designs against real-world scenarios. *Not Mermaid-native* — approximate via `classDiagram` instance notation, or use PlantUML for true object notation.
- **Sequence diagram** — how components interact in a critical flow. *Mermaid: `sequenceDiagram`* (native).
- **Activity diagram** — a process or workflow running through the system. *Mermaid: `flowchart`* (process flow, not structural grouping — same underlying syntax as Deployment/package view below, used for a different purpose).
- **State diagram** — a component's internal behavior. *Mermaid: `stateDiagram`* (native).
- **Deployment/package view** — whole-system structure: services, actors, and boundaries. *Mermaid: `flowchart`* with subgraphs grouping components into their containers (same underlying syntax as Activity diagram above, used for a different purpose).

## Workflow

1. **Evaluate the trigger** — does your material substantively describe a system's architecture?
2. **When it does**, author an architectural diagram, leading with the diagram whose concern is most central to your findings — see § Diagram Types.
3. **Add additional diagrams only when they convey distinct information** the primary diagram cannot show (§ Diagram Types). Each must visualize a distinct established structure; do not add diagrams for completeness.
4. **Author in Mermaid** as a fenced ` ```mermaid ` code block, placed adjacent to the analysis prose it visualizes. Mermaid is the default because it renders inline in GitHub and most markdown viewers. Use PlantUML only as an explicit fallback when Mermaid cannot adequately express the architectural structure, and note the fallback reason beside the block.
5. **Ground every element** — each component, module, service, layer, and relationship must correspond to something described in your findings. Do not invent, infer beyond evidence, or decoratively pad.
6. **Check the markup against the diagram type's grammar** — verify the Mermaid syntax is well-formed so the block renders rather than degrading to raw text. Reserved and terminator characters are per diagram type, and the quoted-string escape that protects label text in one type may not exist in another: a character is not safe here because it was safe in the type you drew last. For example, `sequenceDiagram` reads a bare `;` in message or note text as a statement terminator and `#` as a comment start, with no quoting to escape either, whereas `flowchart`/`graph` accept `;` as an optional statement terminator and protect label text inside quoted brackets. Before considering a diagram finished, scan its label, message, and note text for the reserved characters of the type you actually used — an eye pass for "looks valid" does not reliably find one stray character.

## Quality Criteria

- Your evaluation of whether the material describes a system's architecture is sound and clearly reasoned.
- When the material substantively describes a system's architecture, at least one architectural diagram is present; the structural view matching the findings' zoom level leads.
- Every diagram element traces to your findings; nothing appears in a diagram that your analysis cannot support.
- Diagrams complement your written analysis; the analysis remains complete without them.

## Anti-Patterns

- **Decorative diagramming** — drawing boxes without expressing the relationships the findings established; a diagram that adds no relational information is noise, not analysis.
- **Skipping a diagram when architecture is present** — when the material substantively describes a system's architecture, a diagram is a missed opportunity to clarify the system's design.
- **Diagram as analysis substitute** — drawing instead of writing; the diagram supplements the analysis, never replaces its reasoning.
- **Unsourced relationships** — edges or hierarchies that appear in the diagram but not in your findings.
- **Unjustified PlantUML** — defaulting to PlantUML (which does not render inline in most viewers) without stating why Mermaid could not express the architectural structure.
- **Over-triggering on non-architectural content** — treating process lists, taxonomies, or conceptual hierarchies as architecture when they are not part of describing a system's design.
- **Impression-only markup check** — eyeballing a diagram as "looks valid" instead of scanning its label, message, and note text for the reserved characters of the diagram type actually used; a single stray character degrades a rendered diagram to raw text, and a visual pass does not reliably catch it.
