---
name: architecture-diagram
description: "Dark-themed SVG architecture/cloud/infra diagrams as HTML."
version: 1.0.0
author: Cocoon AI (hello@cocoon-ai.com), ported by Hermes Agent
license: MIT
dependencies: []
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [architecture, diagrams, SVG, HTML, visualization, infrastructure, cloud]
    related_skills: [concept-diagrams, excalidraw]
---

# Architecture Diagram Skill

Generate professional, dark-themed technical architecture diagrams as standalone HTML files with inline SVG graphics. No external tools, no API keys, no rendering libraries — just write the HTML file and open it in a browser.

## Scope

**Best suited for:**

- Software system architecture (frontend / backend / database layers)
- Cloud infrastructure (VPC, regions, subnets, managed services)
- Microservice / service-mesh topology
- Database + API map, deployment diagrams
- Anything with a tech-infra subject that fits a dark, grid-backed aesthetic

**Look elsewhere first for:**

- Physics, chemistry, math, biology, or other scientific subjects
- Physical objects (vehicles, hardware, anatomy, cross-sections)
- Floor plans, narrative journeys, educational / textbook-style visuals
- Hand-drawn whiteboard sketches (consider `excalidraw`)
- Animated explainers (consider an animation skill)

If a more specialized skill is available for the subject, prefer that. If none fits, this skill can also serve as a general SVG diagram fallback — the output will just carry the dark tech aesthetic described below.

Based on [Cocoon AI's architecture-diagram-generator](https://github.com/Cocoon-AI/architecture-diagram-generator) (MIT).

## Workflow

1. User describes their system architecture (components, connections, technologies)
2. Generate the HTML file following the design system below
3. Save with `write_file` to a `.html` file (e.g. `~/architecture-diagram.html`)
4. User opens in any browser — works offline, no dependencies

### Output Location

Save diagrams to a user-specified path, or default to the current working directory:

```
./[project-name]-architecture.html
```

### Preview

After saving, suggest the user open it:

```bash
# macOS
open ./my-architecture.html
# Linux
xdg-open ./my-architecture.html
```

## Design System & Visual Language

### Color Palette (Semantic Mapping)

Use specific `rgba` fills and hex strokes to categorize components:

| Component Type  | Fill (rgba)               | Stroke (Hex)            |
| :-------------- | :------------------------ | :---------------------- |
| **Frontend**    | `rgba(8, 51, 68, 0.4)`    | `#22d3ee` (cyan-400)    |
| **Backend**     | `rgba(6, 78, 59, 0.4)`    | `#34d399` (emerald-400) |
| **Database**    | `rgba(76, 29, 149, 0.4)`  | `#a78bfa` (violet-400)  |
| **AWS/Cloud**   | `rgba(120, 53, 15, 0.3)`  | `#fbbf24` (amber-400)   |
| **Security**    | `rgba(136, 19, 55, 0.4)`  | `#fb7185` (rose-400)    |
| **Message Bus** | `rgba(251, 146, 60, 0.3)` | `#fb923c` (orange-400)  |
| **External**    | `rgba(30, 41, 59, 0.5)`   | `#94a3b8` (slate-400)   |

### Typography & Background

- **Font:** JetBrains Mono (Monospace), loaded from Google Fonts
- **Sizes:** 12px (Names), 9px (Sublabels), 8px (Annotations), 7px (Tiny labels)
- **Background:** Slate-950 (`#020617`) with a subtle 40px grid pattern

```svg
<!-- Background Grid Pattern -->
<pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
  <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#1e293b" stroke-width="0.5"/>
</pattern>
```

## Technical Implementation Details

### Component Rendering

Components are rounded rectangles (`rx="6"`) with 1.5px strokes. To prevent arrows from showing through semi-transparent fills, use a **double-rect masking technique**:

1. Draw an opaque background rect (`#0f172a`)
2. Draw the semi-transparent styled rect on top

### Connection Rules

- **Z-Order:** Draw arrows _early_ in the SVG (after the grid) so they render behind component boxes
- **Arrowheads:** Defined via SVG markers
- **Security Flows:** Use dashed lines in rose color (`#fb7185`)
- **Boundaries:**
  - _Security Groups:_ Dashed (`4,4`), rose color
  - _Regions:_ Large dashed (`8,4`), amber color, `rx="12"`

### Spacing & Layout Logic

- **Standard Height:** 60px (Services); 80-120px (Large components)
- **Vertical Gap:** Minimum 40px between components
- **Message Buses:** Must be placed _in the gap_ between services, not overlapping them
- **Legend Placement:** **CRITICAL.** Must be placed outside all boundary boxes. Calculate the lowest Y-coordinate of all boundaries and place the legend at least 20px below it.

## Verify the geometry before delivering

A diagram fails quietly: an overflowing label and a box drawn in the wrong layer both render _something_ and look
intentional. Check the file, not the picture — and check it with a script so it can be re-run after every edit.

- **Deduplicate the masking pairs before flagging anything.** Every component is two rects at the same `x/y/width/height`
  (opaque ground, then the translucent face), so an overlap check written over all rects reports every component as
  overlapping _itself_ — a page of false positives that buries the real collision. Collapse identical geometry to one
  entry first.
- **Measure the text, not the character count.** Sublabels at 8–9 px are where content escapes its box, and nothing in
  the palette warns you: in a browser, compare `getBBox()` of each `<text>` against the rect it belongs to, or
  `getComputedTextLength()`. In monospace, the worst-case label is the one to test, not the average one.
- **Assert the layout rules that are stated as critical** — the legend below the lowest boundary, message buses in the
  gap rather than on top of a service, the minimum vertical gap — as arithmetic on the rect list. A rule with a
  "CRITICAL" beside it and no check is a rule that gets broken in the next revision.
- **Arrows drawn early are behind, not inside.** Z-order is a document order claim, so verify it from the element
  order in the file rather than from how the render looks.

## Document Structure

The generated HTML file follows a four-part layout:

1. **Header:** Title with a pulsing dot indicator and subtitle
2. **Main SVG:** The diagram contained within a rounded border card
3. **Summary Cards:** A grid of three cards below the diagram for high-level details
4. **Footer:** Minimal metadata

### Info Card Pattern

```html
<div class="card">
  <div class="card-header">
    <div class="card-dot cyan"></div>
    <h3>Title</h3>
  </div>
  <ul>
    <li>• Item one</li>
    <li>• Item two</li>
  </ul>
</div>
```

## Output Requirements

- **Single File:** One self-contained `.html` file
- **No External Dependencies:** All CSS and SVG must be inline (except Google Fonts)
- **No JavaScript:** Use pure CSS for any animations (like pulsing dots)
- **Compatibility:** Must render correctly in any modern web browser

## Template Reference

Load the full HTML template for the exact structure, CSS, and SVG component examples:

```
skill_view(name="architecture-diagram", file_path="templates/template.html")
```

The template contains working examples of every component type (frontend, backend, database, cloud, security), arrow styles (standard, dashed, curved), security groups, region boundaries, and the legend — use it as your structural reference when generating diagrams.
