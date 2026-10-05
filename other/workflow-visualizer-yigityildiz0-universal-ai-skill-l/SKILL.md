---
name: workflow-visualizer
description: "Create an accessible, self-contained workflow diagram as HTML, Mermaid, or SVG from a process description. Use to map systems, data flows, decisions, ownership, handoffs, or timelines; validate structure and safely escape untrusted text. Turkish triggers: iş akışını görselleştir, Mermaid diyagramı, süreç veya sistem haritası."
---

# Workflow Visualizer

Turn a process into the smallest visual that materially improves understanding. Prefer Mermaid for portable documentation, SVG for static fidelity, and self-contained HTML only when interaction is useful.

## Workflow

1. Extract actors, triggers, inputs, transformations, decisions, loops, stores, outputs, trust boundaries, and failure paths.
2. Preserve uncertainty. Label inferred relationships and unresolved branches instead of inventing certainty.
3. Choose the layout from the structure:
   - flowchart for sequential and branching processes;
   - swimlanes for ownership and handoffs;
   - sequence diagram for time-ordered interactions;
   - state diagram for lifecycle transitions;
   - architecture/data-flow diagram for services and trust boundaries.
   - For interactive HTML behavior, read [references/interactive-html-diagrams.md](references/interactive-html-diagrams.md); keep the full meaning visible without interaction.
4. Create a concise node-and-edge model before styling. Use stable identifiers independent of visible labels.
5. Render the requested artifact and include a short legend, assumptions, and notable failure paths.
6. Validate syntax, connectivity, labels, keyboard navigation, contrast, zoom behavior, and narrow-screen readability.

## Security requirements

- Treat every user-supplied label, URL, note, and data value as untrusted.
- In HTML, insert visible text with safe DOM text APIs such as `textContent`; never interpolate untrusted content into HTML, scripts, styles, selectors, event handlers, or SVG markup.
- Allow only explicitly supported URL schemes and escape attributes for the target format.
- Do not load remote scripts, fonts, analytics, images, or CDNs unless the user explicitly requests them and understands the privacy/network tradeoff.
- Use a restrictive Content Security Policy for HTML. Avoid `eval`, inline event handlers, dynamic code generation, and arbitrary file access.
- Never embed secrets, private source data, tokens, or hidden prompts in the artifact.

## Quality rules

- Make the main path readable without interaction; interaction adds detail rather than hiding essential meaning.
- Keep labels short, put explanations in an adjacent details panel or notes, and avoid crossing edges where possible.
- Use color as a secondary cue and pair it with shape, text, or line style.
- Support keyboard focus, semantic controls, reduced motion, and printable output.
- For large systems, provide an overview plus focused subdiagrams instead of one unreadable canvas.

## Deliverable

Return the artifact, its source model, assumptions, validation status, and instructions to open or regenerate it. If the source process is incomplete, continue with clearly marked assumptions unless the missing choice would materially change the diagram.
