---
name: interactive-teaching-materials
description: >-
  Creates interactive HTML teaching materials with clickable state diagrams. Use
  when the user asks to produce an explorable tutorial artifact, not to answer a
  question.
effort: high
---

# Interactive Teaching Materials for Complex Processes

## Core Idea

The diagram is a navigation surface. Every element is clickable and opens a detail panel with rich text. The value is in the details, not in the arrows.

When one-word labels on arrows are enough — use Mermaid (`draw-mermaid-diagrams`). This format is for when every state and transition deserves paragraphs of context, config snippets, HTTP payloads, and debugging tips.

## Principles

1. **All states and transitions are explicit** — nothing implicit, nothing merged
2. **Every element has substance** — a node or edge without description is an error. If you can't explain what happens at this step — you don't understand the process yet
3. **Details are rich text** — HTML with paragraphs, code blocks, lists, config snippets. The detail panel is where the real teaching happens
4. **Transitions are first-class** — edges carry description and details, not just a label
5. **Minimalist chrome** — toolbar contains only: title, optional doc link, item counter. Navigation lives in the inspector panel
6. **Single self-contained HTML file** — all CSS + JS + data inline. SVG.js v3 (~16KB) loaded from CDN for cleaner SVG code, but is optional — templates work as a reference and can be rewritten with raw `document.createElementNS` if offline use is required
7. **Affordance** — interactive elements must look clickable: hover highlights, first element auto-selected on load. Navigation buttons in inspector with keyboard hints teach interaction instantly

## Anti-patterns

- Empty description or `details: {}` — every element must teach something
- Details as raw JSON without explanation — JSON shows WHAT, text explains WHY
- 3-4 simple steps with one-sentence descriptions — Mermaid is enough for that
- Overloaded diagram (40+ elements) — split into phases, one diagram each

## What Good Details Look Like

Details is an HTML string combining:
- An explanatory paragraph (what happens and why)
- A code/config/HTTP snippet in `<pre>` (the exact artifact)
- Key parameters or options in `<ul>` (what varies)
- Caveats or debugging hints (what can go wrong)

If details is a JS object instead of a string, the template renders it as highlighted JSON — useful for API payloads but not the primary mode.

## Data Schema

### Sequence diagram

```js
const TITLE = "string";         // Page title
const DOC_URL = "string";       // Optional link to external docs (shown in toolbar)
const ACTORS = ["A", "B", "C"]; // Horizontal actor columns, left to right

const STEPS = [
  {
    name: "string",        // Required. Short label on the arrow (3-5 words)
    from: "A",             // Required. Actor name (must match ACTORS)
    to: "B",               // Required. Actor name (must match ACTORS)
    preview: "string",     // Optional. Secondary label below the arrow (e.g. "GET /authorize")
    description: "string", // Required. 1-3 sentences for the inspector summary
    details: "html string" // Required. Rich HTML for the inspector detail panel
  }
];
```

### Flowchart diagram

```js
const TITLE = "string";
const DOC_URL = "string";

const NODES = [
  {
    id: "string",          // Required. Unique identifier, used in EDGES
    type: "action|state|decision|start|end", // Required. Determines shape
    label: "string",       // Required. Short label inside the shape (2-4 words)
    x: 320,                // Required. Center X position in pixels
    y: 160,                // Required. Center Y position in pixels
    description: "string", // Required. 1-3 sentences for the inspector summary
    details: "html string" // Required. Rich HTML for the inspector detail panel
  }
];

const EDGES = [
  {
    from: "node_id",       // Required. Source node id
    to: "node_id",         // Required. Target node id
    label: "string",       // Optional. Short label on the edge (e.g. "ok", "fail")
    fromSide: "bottom",    // Optional. Attach point: "top"|"bottom"|"left"|"right". Default: "bottom"
    toSide: "top",         // Optional. Attach point. Default: "top"
    description: "string", // Required. 1-3 sentences for the inspector summary
    details: "html string" // Required. Rich HTML for the inspector detail panel
  }
];
```

Node types and their shapes:
- `action` — rounded rectangle (140x44). General processing step
- `state` — rounded rectangle with gray fill. Resting/waiting state
- `decision` — diamond (60x44). Branching point
- `start` — filled circle (r=22). Entry point
- `end` — filled circle with inner ring. Terminal state

## Workflow

1. Determine type: **sequence** (actors + messages) or **flowchart** (nodes + edges)
2. Read the corresponding template from `assets/` — it has a full working example
3. Replace the DATA section (between `// === DATA ===` and `// === END DATA ===`) with your data following the schema above
4. Write to target path

## Scaling

- Templates auto-size SVG to fit content
- Long labels: keep diagram labels short (3-5 words), put context in the detail panel
- Many steps (20+): the page scrolls, that's fine
- Complex topology (loops, convergence): the flowchart template handles directional bezier routing — specify `fromSide`/`toSide` on edges

## Design Constraints (do not change)

- CSS variables define the palette — never override inline
- Inspector: always right sidebar, never modal or tooltip
- Active element: blue stroke + blue text; everything else gray
- Navigation buttons live in the inspector panel (after details), not in toolbar. Flowchart follows graph topology: node -> edge -> node. On branching, buttons show choices with number keys (1, 2, ...). Space always clicks the first/only option
