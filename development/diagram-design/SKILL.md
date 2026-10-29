---
name: diagram-design
description: "Use when a change, analysis, or document needs a diagram — architecture, request flow, sequence, state machine, ER model, timeline, or comparison — and a picture explains it better than prose. Produces one self-contained HTML + inline SVG file with no build step, no external asset, and no runtime dependency, styled by a fixed editorial design system and validated against a density, contrast, and geometry checklist before it ships."
license: MIT
metadata:
  author: "Petr Král (pekral.cz)"
---

## Constraints
- Self-contained: one HTML file with inline CSS and inline SVG. No build step, no framework, no bundler, no external stylesheet, font file, image, or script.
- The file opens from disk in any modern browser, offline. A diagram that needs a network request to render is a defect.
- Vanilla HTML/CSS/SVG. JavaScript is allowed only for optional motion controls and the file must be complete and readable with JavaScript disabled.
- Apply `@rules/writing/general.md` to every label, caption, and annotation in the diagram — one idea per label, active voice, one term per concept.
- Density is a hard gate: at most 12 nodes and at most 2 focal elements per diagram. Split into two diagrams rather than crowding one.
- Never invent structure. Every node, edge, and label states something read out of the code, the schema, the assignment, or the migration — never a plausible guess.
- Accessibility is required: WCAG AA contrast on every text/background pair, a `<title>` and `<desc>` on the root `<svg>`, and `prefers-reduced-motion` honored when motion is used.

## Use when
- A pull request description, an analysis report, or a documentation page needs to show a structure that prose describes badly — a request path across layers, a queue topology, a state machine, a schema relation.
- An existing Mermaid or draw.io diagram must be redrawn as a presentable, self-contained artifact.
- A reviewer or a tester needs to see the blast radius of a change as a picture.

## Do not use when
The gate below runs **first**, before any type is chosen. Reach for text when any of these holds:

| Situation | Use instead |
|-----------|-------------|
| Two or three items compared on a few attributes | a Markdown table |
| An ordered list of steps with no branching and no parallel actor | a numbered list |
| A single box, a single arrow, or one label in a frame | a sentence |
| A before/after of one value | a sentence, or a two-row table |
| The picture would restate the paragraph above it | delete the picture |

The test: **deleting the diagram must cost the reader understanding.** When it costs only decoration, it does not ship.

## Execution

### 1. Read the source before drawing
Read the actual files the diagram claims to describe — the routes, the Action, the job class, the migration, the config. Map every node you intend to draw to a concrete `file:line`. A node you cannot anchor is a node you do not draw. When the assignment and the code disagree, stop and surface the discrepancy rather than drawing either version.

### 2. Choose one type by the question the diagram answers
Do not pick a type by what the data looks like — pick it by the reader's question. `references/diagram-types.md` carries the full catalog with the layout grammar and the density ceiling of each type. The routing table:

| The reader asks | Type |
|-----------------|------|
| What talks to what? | architecture |
| What happens next, and where does it branch? | flowchart |
| In what order do these participants exchange messages? | sequence |
| What states exist and what moves between them? | state machine |
| How do these tables relate? | ER |
| What happened when? | timeline |
| Who owns which step? | swimlane |
| How do these options score on two axes? | quadrant |
| What contains what? | nested / tree / layers |
| Where does this data go? | data flow |

When two types both fit, take the one with fewer edges. A picture is read along its edges, and edges are what make it unreadable.

### 3. Apply the design system
`references/style-guide.md` is the single source of truth for tokens. It is not decoration — the constraints are what keep an agent-generated diagram from looking machine-made:

- **One accent.** Exactly one hue carries meaning; everything else is neutral. Two accents mean the reader must learn a legend before reading the picture.
- **1px hairlines, no shadows, radius ≤ 10px.** Depth effects add pixels and no information.
- **Every measurement divisible by 4.** Positions, sizes, gaps, and stroke offsets snap to a 4px grid.
- **Three type roles.** A display face for the title, a sans face for labels, a mono face for identifiers — each declared with a complete local fallback stack, never loaded from a font host.

### 4. Build the file
Start from `templates/diagram.html` and replace the `<svg>` body. The template already carries the token block, the light/dark handling, the accessible root `<svg>`, and the reduced-motion guard.

Rules that decide whether the output looks drawn or generated:

- Lay the geometry out on the 4px grid by hand, in absolute SVG coordinates. Do not center by eyeballing — compute the coordinate.
- Give every text element an explicit `text-anchor` and `dominant-baseline`. Defaults differ between renderers and a label that is centered in one browser drifts in another.
- Route edges orthogonally (horizontal and vertical runs joined at right angles) or as a single cubic Bézier. Never a diagonal straight line between boxes.
- An edge label sits on the edge with a background rectangle in the canvas color behind it, so the line does not strike through the text.
- Reserve the top 64px for the title and the bottom 48px for the caption. The caption names what the reader should take away, not what the picture contains.

### 5. Optional motion
Static is the default and always ships. Add motion only when the sequence itself is the message — a request travelling through layers, a state machine walking its transitions.

- Motion is CSS animation on SVG elements, or a small inline script for step controls. No animation library.
- Every animated element renders in its final, complete state when animation is off.
- `@media (prefers-reduced-motion: reduce)` shows that final frame and hides the controls.

### 6. Self-check before handoff
Run every item in `references/self-check.md`. It covers density, contrast, label overlap, edge crossings, the 4px grid, the offline guarantee, and the anchoring of every node to a real `file:line`. A diagram that fails an item is fixed, not shipped with a caveat.

## Output
- One file: `<name>.html`, self-contained, opened from disk to verify it renders.
- A one-paragraph handoff naming the file path, the chosen type, the question the diagram answers, and the `file:line` anchors behind the nodes.
- When the diagram accompanies a pull request or a tracker comment, embed the exported SVG or a rendered PNG there — a raw HTML file is not readable inside a tracker comment.

## Anti-patterns
- A node whose label is a category (`Service`, `Handler`) rather than the real symbol (`OrderPaymentAction`).
- Rainbow palettes where color carries no meaning.
- A legend explaining shapes the picture could have made obvious.
- Drop shadows, gradients, and 3D boxes standing in for hierarchy that spacing should carry.
- A diagram redrawn from the issue text without opening the code it describes.
- Mermaid pasted into an HTML file and called self-contained — the renderer is an external dependency.

## References
- `references/style-guide.md` — the token set: palette, type roles, spacing grid, stroke and radius rules
- `references/diagram-types.md` — the catalog: every type with its layout grammar and density ceiling
- `references/self-check.md` — the pre-handoff checklist
- `templates/diagram.html` — the scaffold to start from

## Done when
- The gate in *Do not use when* was applied and the diagram survived it.
- Every node is anchored to a real `file:line` and the anchors are listed in the handoff.
- The file renders correctly from disk with the network disabled and with JavaScript disabled.
- Node count is at most 12, focal elements at most 2, and one accent hue carries all the meaning.
- Every text/background pair passes WCAG AA and the root `<svg>` carries a `<title>` and a `<desc>`.
- Every checklist item in `references/self-check.md` passes.

## Output Humanization
- Use [blader/humanizer](https://github.com/blader/humanizer) for all skill outputs to keep the text natural and human-friendly.
