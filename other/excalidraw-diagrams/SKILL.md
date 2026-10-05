---
name: excalidraw-diagrams
description: >
  Create polished Excalidraw diagrams from text descriptions. Use when the user
  asks for a diagram, flowchart, architecture diagram, decision tree, process
  flow, data flow, system overview, or similar visual explanation, or says
  "draw this", "diagram this", "visualize this", or "make a chart". Produces
  styled `.excalidraw` files with consistent colors and can export a shareable
  excalidraw.com URL.
metadata:
  openclaw:
    emoji: "📊"
---

# Excalidraw Diagrams

Use `excalidraw-cli` to turn structured diagram plans into `.excalidraw` files. The published CLI accepts Excalidraw JSON elements, not a custom DSL, so any shorthand notation is only for planning. The executable artifact is always a JSON elements file plus the generated `.excalidraw`.

## Prerequisites

- `excalidraw-cli` must be on `PATH`.
- When you need exact field names or supported element properties, run `excalidraw-cli reference` or `excalidraw-cli ref --raw`.

## Triggering

Use this skill when the user wants:
- A flowchart, architecture diagram, decision tree, data flow, or process map
- A system or workflow visualized instead of explained in prose
- A polished Excalidraw artifact they can keep editing

## Working Model

1. Reduce the request into nodes, arrows, labels, and layout direction.
2. If helpful, sketch the structure in shorthand first:
   - `(Start)` = ellipse
   - `[Step]` = rectangle
   - `{Decision?}` = diamond
   - `[[Store]]` = storage/data node
   - `->`, `-->`, `-> "label" ->` = connectors
3. Translate that plan into Excalidraw JSON elements in an `elements.json` file.
4. For multiple diagrams, charts, or visual explanations, use the default container-grid canvas pattern below unless the user specifies a different layout.
   - Present multiple charts in one combined editable Excalidraw canvas unless the user asks for separate files.
   - If separate chart files are useful or already created, also create a single combined `.excalidraw` canvas that contains all charts.
5. Generate the diagram with `excalidraw-cli create elements.json -o output.excalidraw`.
6. Generate a local preview image for the `.excalidraw` file using Quick Look when available:
   - `qlmanage -t -s 1600 -o <preview_dir> output.excalidraw`
   - This typically produces `output.excalidraw.png`.
7. Export a browser-openable share link with `excalidraw-cli export output.excalidraw`.
8. Return the `.excalidraw` path, the preview image path, and the shareable URL.

## CLI Workflow

Core commands:

```bash
# Build a diagram from a JSON file
excalidraw-cli create elements.json -o diagram.excalidraw

# Generate a local preview PNG with macOS Quick Look
qlmanage -t -s 1600 -o previews diagram.excalidraw

# Or from inline JSON for tiny examples
excalidraw-cli create --json '[...]' -o diagram.excalidraw

# Export to a shareable excalidraw.com URL
excalidraw-cli export diagram.excalidraw

# Inspect the supported element format
excalidraw-cli reference
```

Important constraints:
- `create` expects Excalidraw JSON elements, not Mermaid and not the shorthand DSL above.
- The published CLI does not render local PNG files itself. On macOS, prefer Quick Look via `qlmanage` to generate preview images from the resulting `.excalidraw` file.
- If Quick Look is unavailable, still return the `.excalidraw` file and the share URL, and say that a local preview image could not be generated in this environment.
- Do not delete generated files unless the user asks or you are working in a temporary scratch location.

## Styling Defaults

Every diagram should look intentional. Apply a consistent palette unless the user asks for something else:

- Start/info: `#a5d8ff`
- Success/positive path: `#b2f2bb`
- Important/configuration: `#ffec99`
- Decisions/warnings/errors: `#ffc9c9`
- Storage/external systems/alternate path: `#d0bfff`

Use these heuristics:
- Action steps: `fillStyle: "hachure"`
- States and outcomes: `fillStyle: "solid"`
- Error or debug paths: dashed arrows or stronger red/pink accents
- Keep rounded, hand-drawn defaults unless the user asks for a rigid style

## Default Multi-Diagram Layout

When the user asks for multiple diagrams, many charts, a visual explainer, or a set of graphics, default to one large editable Excalidraw canvas laid out as a clean grid of contained diagram panels.

Use this pattern unless the user explicitly asks for something different:

- One `.excalidraw` file as the source of truth.
- Multiple charts must be presented together in one combined canvas by default.
- A large grid canvas, typically 3 columns when there are many panels.
- Each diagram sits inside an outer light neutral container rectangle.
- Each container has a short title at the top left, optional one-line subtitle, and a thin divider line below the header.
- Keep generous padding inside each panel.
- Use consistent panel dimensions across the grid when possible.
- Put each mini-diagram, chart, flow, comparison, or decision tree inside its own container.
- Use the same color palette across all panels so the full canvas feels like one system.
- Prefer useful teaching diagrams over decorative diagrams: capability maps, comparison matrices, workflows, decision trees, stacks, loops, ladders, demo maps, and prompt anatomy charts.
- Keep labels short and readable. Split dense ideas into more nodes instead of forcing long text into one shape.
- If the user asks for "a ton of graphics" or similar, make many useful panels on one canvas rather than many disconnected files.

Good default panel structure:

```json
[
  {
    "type": "rectangle",
    "id": "panel_1",
    "x": 80,
    "y": 80,
    "width": 1450,
    "height": 900,
    "backgroundColor": "#f8f9fa",
    "strokeColor": "#dee2e6",
    "fillStyle": "solid",
    "strokeWidth": 2,
    "roughness": 1,
    "roundness": { "type": 3 }
  },
  {
    "type": "text",
    "id": "panel_1_title",
    "x": 114,
    "y": 106,
    "text": "Diagram Title",
    "fontSize": 30,
    "strokeColor": "#1e1e1e"
  },
  {
    "type": "text",
    "id": "panel_1_subtitle",
    "x": 116,
    "y": 150,
    "text": "One short sentence explaining what this panel teaches.",
    "fontSize": 17,
    "strokeColor": "#5f6368"
  },
  {
    "type": "arrow",
    "id": "panel_1_divider",
    "x": 114,
    "y": 192,
    "width": 1382,
    "height": 0,
    "points": [[0, 0], [1382, 0]],
    "endArrowhead": null,
    "strokeColor": "#ced4da",
    "strokeWidth": 2,
    "roughness": 1
  }
]
```

For grid placement, use a predictable coordinate system such as:

- Panel width: 1450
- Panel height: 900
- Gap: 120
- Start x/y: 80, 80
- Column x: `80 + column * (1450 + 120)`
- Row y: `80 + row * (900 + 120)`

## Element Conventions

- Put a `cameraUpdate` element first and keep it 4:3, for example `1200x900`.
- Prefer the CLI's `label` shorthand on `rectangle`, `ellipse`, `diamond`, and `arrow` elements instead of manually constructing bound text elements.
- Use stable IDs so arrows can bind cleanly to shapes.
- Bind arrows with `startBinding` and `endBinding`.
- Fixed-point helpers:
  - Right edge: `[1, 0.5]`
  - Left edge: `[0, 0.5]`
  - Top edge: `[0.5, 0]`
  - Bottom edge: `[0.5, 1]`
- Use top-to-bottom layouts for flows and left-to-right layouts for architecture unless the user signals otherwise.

## Minimal JSON Pattern

Use this as a starting point and expand it to match the request:

```json
[
  { "type": "cameraUpdate", "width": 1200, "height": 900, "x": 0, "y": 0 },
  {
    "type": "ellipse",
    "id": "start",
    "x": 460,
    "y": 60,
    "width": 180,
    "height": 90,
    "backgroundColor": "#a5d8ff",
    "fillStyle": "solid",
    "label": { "text": "Start" },
    "boundElements": [{ "id": "a1", "type": "arrow" }]
  },
  {
    "type": "arrow",
    "id": "a1",
    "x": 550,
    "y": 150,
    "width": 0,
    "height": 120,
    "points": [[0, 0], [0, 120]],
    "endArrowhead": "arrow",
    "startBinding": { "elementId": "start", "fixedPoint": [0.5, 1] },
    "endBinding": { "elementId": "step", "fixedPoint": [0.5, 0] },
    "label": { "text": "continue" }
  },
  {
    "type": "rectangle",
    "id": "step",
    "x": 430,
    "y": 290,
    "width": 240,
    "height": 90,
    "backgroundColor": "#b2f2bb",
    "fillStyle": "hachure",
    "label": { "text": "Process step" },
    "boundElements": [{ "id": "a1", "type": "arrow" }]
  }
]
```

## Diagram Guidance

Prefer one of these patterns:

- Flowchart: stacked nodes, labeled yes/no arrows from diamonds
- Architecture: left-to-right services, stores, and external systems with protocol labels
- Decision tree: diamonds at branch points, short outcome labels
- Data flow: inputs, transforms, stores, and outputs with directional arrows

For large diagrams:
- Use a light background rectangle with low opacity to group zones
- Keep labels short
- Split dense concepts into multiple nodes instead of multiline labels

## Output Expectations

- The `.excalidraw` file is the source of truth.
- By default, also generate a preview image from the `.excalidraw` file when the environment supports it.
- By default, also export a URL with `excalidraw-cli export` so the user can open the diagram in Excalidraw quickly.
- When multiple diagrams or charts are created, always create and present one combined editable `.excalidraw` canvas containing all charts, with a preview image and share URL.
- If individual diagram files are also created, provide links to every individual artifact, but make the combined canvas the primary deliverable.
- When more than one diagram file is created, also create a simple Markdown index file that links to the combined canvas, all individual diagram files, preview images, and share URLs, then include that index link in the final response.
- In the final response, include:
  - a rendered image preview using Markdown image syntax when a preview file exists
  - a clickable file path to the `.excalidraw` file
  - a clickable file path to the preview image
  - the excalidraw.com share/open URL
- If the user asks for a sequence diagram, Gantt chart, pie chart, or bar chart, say this tool is a poor fit and suggest Mermaid instead.

## Portability Notes

- Specific to the author's current workflow: previews prefer macOS Quick Look when available, and default output includes an excalidraw.com share URL.
- Reusable: the JSON-elements workflow, multi-panel canvas convention, styling defaults, artifact expectations, and "Excalidraw is the source of truth" rule.
- Adapt before reuse: replace preview generation, share-link policy, scratch/output paths, and any platform-specific tooling with what the target environment supports.
