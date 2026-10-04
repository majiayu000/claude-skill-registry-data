---
name: assistant-diagrams
description: "Create Mermaid architecture, sequence, ER, flow, class, or state diagrams. Use for explicit diagram or system-flow visualization requests."
---

# Diagram Generator

Migration note: diagram contracts are v3. Consumers of v2 must replace the
singular feature-preparation evidence ref with exact
`{evidence_ref, item_id}` bindings at the root and for every traced node and
edge. `source_refs` remain the underlying code, configuration, test, or
user-provided evidence; `coverage_gaps` still disclose unavailable behavior.

## Contracts

| File | Purpose |
|---|---|
| [`contracts/input.yaml`](contracts/input.yaml) | diagram_type, scope, source_files[], format, optional exact feature-preparation evidence-row bindings |
| [`contracts/output.yaml`](contracts/output.yaml) | diagram_code, diagram_type, description, evidence sources, element trace, coverage gaps |

- `diagram_type` and `scope` are required; `format` defaults to mermaid
- `diagram_code` must be valid syntax parseable by the target renderer
- `diagram_type` is echoed back in output to confirm what was generated
- Feature-preparation diagrams carry exact `{evidence_ref, item_id}` bindings at the root and for every traced element, and disclose untraced elements as coverage gaps

Creates accurate Mermaid diagrams from code analysis. Covers the developer's visual documentation weakness.

Core principle: **Diagrams should be generated from code, not drawn from memory.**

## Goal

Generate diagrams that make real code structure or behavior easier to understand without inventing components.

## Success Criteria

- Diagram type, scope, evidence, placement, and gaps are explicit.
- Every node and edge is traceable to inspected code, configuration, or user-provided context.
- Mermaid output is small enough to read and structured enough to render.

## Constraints

- Ask only when diagram type or scope materially changes the result and cannot be inferred from prompt/context.
- If multiple diagram types are plausible, choose the best fit from source evidence or ask every material, non-discoverable question needed to select safely; group them by decision topic.
- Do not add aspirational boxes, future architecture, or unlabeled relationships unless the user explicitly asks for a proposed design.

## Available Diagram Types

| Type | File | Best for |
|---|---|---|
| **Architecture** | `arch-diagram.md` | System overview, component relationships |
| **Sequence** | `sequence-diagram.md` | Request flows, interaction patterns |
| **Entity-Relationship** | `er-diagram.md` | Data models, database schema |
| **Flow** | `flow-diagram.md` | Business logic, decision trees, algorithms |
| **Component** | `component-diagram.md` | Module boundaries, dependencies |
| **Class** | `class-diagram.md` | Type hierarchies, interfaces, relationships |
| **State** | `state-diagram.md` | State machines, lifecycle transitions |

## Auto-Selection

```
Input arrives
    │
    ├─ "architecture" / "system overview"     → arch-diagram.md
    ├─ "flow" / "how does X work"             → sequence-diagram.md or flow-diagram.md
    ├─ "data model" / "entities" / "schema"   → er-diagram.md
    ├─ "dependencies" / "modules"             → component-diagram.md
    ├─ "class hierarchy" / "types"            → class-diagram.md
    ├─ "state" / "lifecycle" / "transitions"  → state-diagram.md
    └─ ambiguous                              → ask user or pick best fit
```

Prefer picking the best fit when the user's intent and code context point clearly to one type. Ask only when the choice would materially change what gets inspected or drawn.

## General Protocol

For all diagram types:

1. **Read the relevant code** — trace the actual paths, don't guess
2. **Right-size the diagram** — show what matters, omit noise
3. **Verify accuracy** — every box/arrow must correspond to real code
4. **Use project terminology** — names from code, not generic labels
5. **Output as Mermaid** — embeddable in markdown, renderable everywhere

## Diagram Complexity Guidelines

| Project Size | Guideline |
|---|---|
| Small (< 10 files) | Single diagram can show everything |
| Medium (10-50 files) | One overview + detail diagrams per area |
| Large (50+ files) | Layered: L0 overview → L1 component → L2 detail |

## Output

Return:
- **Result** - the diagram type generated and a brief description of what it shows.
- **Diagram** - valid Mermaid inside a fenced code block:

````markdown
```mermaid
[diagram content]
```
````

- **Evidence** - code files, symbols, or paths used to derive the diagram.
- **Placement** - where the diagram was written, or "inline only" if no file changed.
- **Gaps** - any missing context, assumptions, or follow-up questions affecting accuracy.

## Where to Place Diagrams

- If generating docs (via `assistant-docs`): embed in the doc
- If user asks directly: output inline in conversation
- If generating architecture doc: embed in `docs/architecture.md`
- For standalone diagrams: `docs/diagrams/[name].md`

## Mermaid Best Practices

- Keep node labels short (2-4 words)
- Use meaningful edge labels (verb phrases: "calls", "reads from", "publishes to")
- Group related nodes with `subgraph`
- Use direction that reads naturally (TD for hierarchies, LR for flows)
- Limit to ~15-20 nodes per diagram — split larger ones

## Rules

- **Every element must exist in code** — no aspirational boxes
- **Don't show everything** — show what helps understanding
- **Label relationships** — unlabeled arrows are useless
- **Use consistent styling** — same type of component gets same shape
- **Test rendering** — Mermaid syntax errors are common, validate mentally

## Stop Rules

- Stop and ask every material, non-discoverable question when neither scope nor diagram type can be inferred safely; group them by decision topic and keep each concise.
- Stop and report gaps when required source files or relationships cannot be inspected.
- Do not finalize if the diagram contains elements without source evidence.
