---
name: mermaid-markdown
description: Create, edit, or repair Mermaid embedded in repository Markdown when the `.md` document is the primary artifact. Use for READMEs, architecture or design docs, ADRs, and compatibility fixes for common Markdown previews; use `mermaid-diagram` for standalone source or rendered visual deliverables.
---

# Mermaid in Repository Markdown

Create or revise Mermaid blocks inside Markdown documentation. Optimize first for semantic accuracy and portable preview rendering, while preserving the surrounding document and repository conventions.

## Document boundary

- Treat the Markdown file as the source artifact. Edit it in place when appropriate.
- Read applicable repository instructions, the target document, and the authoritative content sources before changing the diagram.
- Preserve unrelated prose, headings, metadata, links, traceability, and formatting.
- Keep detailed explanations, provenance, and long identifiers outside the graph when the document can carry them more clearly.
- Do not create permanent `.mmd` or rendered-image files unless the user or repository workflow requires them. Remove temporary render artifacts after verification.

## Portability defaults

When renderer capabilities are unknown, target a conservative Mermaid subset commonly supported by Markdown previews:

- Start each Mermaid block directly with a basic diagram declaration such as `flowchart`, `sequenceDiagram`, `stateDiagram-v2`, `classDiagram`, or `erDiagram`.
- Use ordinary `mermaid` fenced code blocks.
- Prefer simple nodes, quoted one-line labels, ordinary arrows, and plain subgraphs or notes.
- Prefer topology, grouping, and short labels over custom styling.
- Avoid init directives, beta-only diagram types, HTML labels, hard-coded theme colors, custom classes, and layout-only fake nodes unless the confirmed target renderers support them and the document genuinely needs them.
- Do not connect edges to subgraph identifiers when connecting real nodes expresses the relationship.
- Avoid hard-coded light or dark backgrounds so the diagram remains readable across editor themes.

If the repository declares a specific Mermaid version or renderer, use only features supported by that target. Preserve an existing advanced construct when it is required and verified rather than simplifying it blindly.

## Workflow

1. Identify the document's purpose, intended readers, renderer targets, and the semantic question the diagram must answer.
2. Choose the simplest suitable diagram type. Inventory the existing or required nodes, transitions, messages, groups, and arrow directions before editing.
3. Plan one dominant reading direction with minimal crossings and clear grouping. Shorten visual labels without changing meaning; move supporting detail into nearby Markdown when appropriate.
4. Add or edit only the necessary Mermaid block and related explanatory text explicitly requested by the user. Preserve all unrelated document content.
5. Perform a conservative syntax review: verify normal fences, a basic declaration as the first Mermaid line, balanced control structures, valid identifiers, and labels that avoid parser-sensitive syntax.
6. When available, render with the repository's own documentation tooling. `mmdc` may be used as a secondary syntax and visual check, but its success does not prove compatibility with every Markdown preview.
7. Inspect the rendered result when possible. Check every node and arrow, light/dark-theme readability, spacing, grouping, crossings, and comprehension at normal editor zoom. Refine without removing semantics.

## Verification checklist

- The diagram preserves the authoritative meaning and document scope.
- Every required node, message, state, and failure path remains present.
- Every arrow direction and label is correct.
- The Mermaid syntax stays within the known renderer capability or the conservative default.
- The main question is answerable within a few seconds at normal preview zoom.
- Surrounding Markdown and repository conventions are preserved.
- No standalone artifacts remain unless explicitly required.

In the final response, identify the Markdown files changed, the compatibility target or validation used, and any syntax that still depends on a renderer version.
