---
name: mermaid-diagram
description: Create standalone Mermaid source and rendered diagram artifacts when the visual itself is the deliverable. Use for `.mmd`, SVG, PNG, PDF, publication, or presentation outputs; use `mermaid-markdown` when a repository Markdown document is the primary artifact.
---

# Standalone Mermaid Diagrams

Create Mermaid diagrams as independent visual artifacts. Optimize for the requested render target and viewing context, including advanced styling when the target renderer supports it.

## Output boundary

- Follow user-specified paths, formats, dimensions, and style requirements.
- Otherwise follow repository conventions; if none exist, use `figures/<descriptive-name>.mmd` as the source artifact.
- Produce rendered outputs such as SVG, PNG, or PDF when requested or when they are part of the repository workflow.
- Create an accompanying Markdown wrapper only when requested. Do not assume that repository documentation is the deliverable.
- Use descriptive kebab-case filenames unless the repository requires another convention.

## Workflow

1. Read applicable repository instructions and the authoritative content inputs.
2. Choose the diagram type that best expresses the relationships:
   - flowchart for processes and decision paths;
   - sequence diagram for ordered interactions;
   - state diagram for lifecycle transitions;
   - class or ER diagram for structural relationships;
   - timeline, Gantt, journey, mindmap, or another supported type when its semantics fit better.
3. Inventory the required nodes, labels, groups, and connections. Select one dominant reading direction and plan the layout before writing syntax.
4. Generate clean Mermaid source with semantic identifiers, concise labels, and accurate edges. Use styling, directives, alternate layouts, or math notation only when they improve the requested artifact and the target Mermaid version supports them.
5. Verify syntax with `mmdc` when available. A suitable `npx @mermaid-js/mermaid-cli` invocation is an acceptable fallback when dependency use is allowed. Fix render errors before review.
6. Inspect the rendered output, not only the source. Verify every node label and arrow direction against the authoritative input, then assess grouping, crossings, spacing, text size, contrast, and readability at the intended output size.
7. Refine and re-render until the diagram is clear. Three rounds is a reasonable default; report any remaining renderer limitation rather than changing semantics to force a layout.

## Visual quality

- Preserve semantic correctness before optimizing appearance.
- Keep related nodes visually consistent and use whitespace to communicate grouping.
- Avoid unnecessary nodes, edges, decoration, and color variation.
- For publication or presentation output, check readability at final scale and in grayscale when print use is likely.
- Use layout helpers only when they do not imply false domain relationships.
- When formulas are necessary, use Mermaid-supported math syntax and verify it with the actual target renderer; otherwise prefer plain labels.

## Verification checklist

- The selected diagram type matches the meaning of the source material.
- Every required component is present and correctly labeled.
- Every arrow points from the correct source to the correct target.
- The main structure is understandable within a few seconds.
- The source renders with the intended Mermaid toolchain.
- Permanent files match the requested deliverables; temporary review files are removed.

In the final response, list the generated artifacts, validation method, refinement performed, and any remaining visual or renderer limitation.
