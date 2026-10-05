---
name: excalidraw
version: 1.0.0
description: "Generate Excalidraw diagram files (.excalidraw) from a description. Use when the user mentions 'excalidraw,' 'diagram,' 'flowchart,' 'process flow,' 'architecture diagram,' 'visual diagram,' or 'draw a diagram.' Outputs valid JSON that opens in Excalidraw web app, VS Code extension, or Obsidian plugin. No API key needed."
---

# Excalidraw Diagram Generator

Generate valid `.excalidraw` JSON files directly from a text description. No API keys, no external services. Output opens in Excalidraw web app, VS Code extension, or Obsidian plugin.

## Workflow

### Step 1: Intake

Gather from the user:
- **What to diagram** — the process, architecture, or concept
- **Diagram type** — flowchart (vertical/horizontal), grid/matrix, freeform, or let you decide
- **Accent nodes** — any nodes that should be visually highlighted (key decision points, human-in-the-loop steps, etc.)
- **Annotations** — any side comments or callouts needed

If the user gives a quick description ("draw a flowchart of X"), infer the rest and proceed. Don't over-ask.

### Step 2: Element Plan

Before generating JSON, present a quick element list:

```
Diagram: [name]
Type: vertical flowchart, 5 nodes

Nodes:
  1. "Input Data" (rectangle)
  2. "Process" (rectangle)
  3. "Decision" (diamond, accent)
  4. "Output A" (rectangle)
  5. "Output B" (rectangle)

Arrows: 1→2, 2→3, 3→4, 3→5
Annotations: note on node 3

Proceed?
```

If the user approves or doesn't object, generate the JSON.

### Step 3: Generate

Build the complete `.excalidraw` JSON following the schema reference below. Every element must have all required fields — Excalidraw silently breaks on missing fields.

### Step 4: Save

Save to the appropriate location:
- If part of a blog post: `drafts/{slug}/diagram-name.excalidraw`
- If standalone: ask the user where to save
- Default filename: descriptive kebab-case, e.g., `content-pipeline-flow.excalidraw`

---

## Style Defaults

| Property | Value | Notes |
|----------|-------|-------|
| strokeColor | `#1F2937` | Charcoal, default for all elements |
| accent strokeColor | `#B45309` | Rust, for highlighted nodes |
| accent backgroundColor | `#FEF3E7` | Light warm fill on accent nodes |
| annotation strokeColor | `#6B7280` | Gray, for side comments |
| annotation line strokeStyle | `dashed` | Dashed leader lines to annotations |
| viewBackgroundColor | `#FAFAF7` | Warm off-white canvas |
| fontFamily | `3` | Monospace (code-on-graph-paper aesthetic) |
| fontSize | `18-20` | Body text in nodes |
| annotation fontSize | `14` | Smaller for side notes |
| roughness | `0` | Clean lines, no hand-drawn wobble |
| strokeWidth | `2` (shapes), `1.5` (arrows), `1` (annotations) | |
| roundness | `null` | Sharp corners on all shapes |
| fillStyle | `solid` | When backgroundColor is set |

---

## Layout Rules

### Vertical Flowchart (default)
- Y spacing: **~68px gap** between bottom of one node and top of next
- X alignment: center all nodes on the same X axis
- Starting position: `x: 160, y: 60`
- Default node size: `280 × 56` (single-line), `280 × 72` (two-line), expand for more text

### Horizontal Flowchart
- X spacing: ~80px gap between right edge of one node and left of next
- Y alignment: center all nodes on the same Y axis

### Grid / Matrix
- Column width: consistent per column, sized to widest node + 40px padding
- Row height: consistent per row, sized to tallest node + 40px padding
- Gutters: 60px horizontal, 40px vertical

### Text Sizing
- Character width at fontSize 18-20: ~10-11px per character (monospace)
- Line height: `fontSize × 1.25`
- Node padding: 10px on each side (text x = node x + 10, text width = node width - 20)
- For multi-line text: height = `lineCount × fontSize × 1.25`
- Auto-size nodes to fit text: `nodeHeight = textHeight + 20` (10px top/bottom padding)

### Edge Calculation Quick Reference

| Edge | X | Y |
|------|---|---|
| Top | `x + width/2` | `y` |
| Bottom | `x + width/2` | `y + height` |
| Left | `x` | `y + height/2` |
| Right | `x + width` | `y + height/2` |

### Hub-and-Spoke Layout

For orchestrator/event-bus diagrams. 8 positions at 45-degree increments:

```
Center hub: (cx, cy), radius r = 200px

N:  (cx,        cy - r)       NE: (cx + 0.7r, cy - 0.7r)
E:  (cx + r,    cy)           SE: (cx + 0.7r, cy + 0.7r)
S:  (cx,        cy + r)       SW: (cx - 0.7r, cy + 0.7r)
W:  (cx - r,    cy)           NW: (cx - 0.7r, cy - 0.7r)
```

### Grouping Rectangles

For logical groupings (namespaces, pipeline stages, bounded contexts), use a large transparent dashed rectangle with a standalone label:

```json
// In spec, add as a node with no arrows:
{"ref": "group1", "type": "rectangle", "x": 80, "y": 50, "width": 400, "height": 300,
 "strokeStyle": "dashed", "strokeColor": "#9c36b5", "backgroundColor": "transparent"}

// Add a standalone label in freeText:
{"text": "Group Name", "x": 100, "y": 60, "fontSize": 14, "strokeColor": "#9c36b5"}
```

Size the group rectangle to encompass all child elements + 40px padding on each side.

### Diagram Complexity Thresholds

| Complexity | Max Elements | Approach |
|------------|-------------|----------|
| Simple | 5-10 | Single file, no groups |
| Medium | 10-25 | Use grouping rectangles |
| Complex | 25-50 | Split into multiple diagrams |
| 50+ | — | Multiple focused diagrams: `overview.excalidraw` + `detail-{subsystem}.excalidraw` |

### Auto-Alignment (freeText)

Use the `align` property on freeText elements for automatic positioning:
- `"align": "center"` — centers the text horizontally over all nodes
- `"align": "left"` — positions to the left of all nodes (for row labels like INPUTS, OUTPUTS)

When using `align`, the `x` value is ignored and computed automatically.

### Annotation Placement
- Position annotations to the right of the diagram: `x: nodeRightEdge + 70`
- Vertically align with the node they annotate
- Connect with a dashed horizontal line from node edge to annotation

---

## Excalidraw JSON Schema Reference

### File Wrapper

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://excalidraw.com",
  "elements": [],
  "appState": {
    "viewBackgroundColor": "#FAFAF7",
    "gridSize": null,
    "gridStep": 5,
    "gridModeEnabled": false
  },
  "files": {}
}
```

### Common Fields (every element has these)

```
type            string    "rectangle" | "text" | "arrow" | "line" | "ellipse" | "diamond"
version         number    1
versionNonce    number    unique integer (1001, 1002, ...)
index           string    fractional ordering: "a0"..."az" (62 values), then "b00"..."bzz" (3844 values)
isDeleted       boolean   false
id              string    short unique: "r1", "r2" (rectangles), "t1" (text), "a1" (arrows), "d1" (diamonds), "ll1" (lines), "at1" (annotation text)
fillStyle       string    "solid"
strokeWidth     number    2 (shapes), 1.5 (arrows), 1 (text/annotations)
strokeStyle     string    "solid" | "dashed"
roughness       number    0
opacity         number    100
angle           number    0
x               number    left edge position
y               number    top edge position
strokeColor     string    hex color
backgroundColor string    hex color or "transparent"
width           number    element width
height          number    element height
seed            number    unique integer (101, 102, ...)
groupIds        array     []
frameId         null      null
roundness       null      null (sharp corners)
boundElements   array     see binding rules below
updated         number    timestamp in ms (use 1714400000000)
link            null      null
locked          boolean   false
```

### Rectangle

All common fields plus `boundElements` linking to contained text and connected arrows.

```json
{
  "type": "rectangle",
  "boundElements": [
    {"id": "t1", "type": "text"},
    {"id": "a1", "type": "arrow"}
  ]
}
```

For accent nodes, add:
```json
{
  "strokeColor": "#B45309",
  "backgroundColor": "#FEF3E7"
}
```

### Diamond (decision node) — USE WITH CAUTION

Diamond arrow connections are unreliable in raw Excalidraw JSON because Excalidraw applies roundness to diamond vertices during rendering, causing visual offset from mathematical edge points. **Prefer a styled rectangle** (e.g., dashed stroke, accent color) for decision points. The generator emits a warning if diamonds are used.

If you must use a diamond, size it larger (~320 x 180) because the shape clips content more aggressively.

### Ellipse

Same as rectangle but `"type": "ellipse"`.

### Text (contained in a shape)

All common fields plus text-specific fields. The `containerId` binds it to the parent shape.

```json
{
  "type": "text",
  "strokeWidth": 1,
  "text": "NODE LABEL",
  "fontSize": 20,
  "fontFamily": 3,
  "textAlign": "center",
  "verticalAlign": "middle",
  "containerId": "r1",
  "originalText": "NODE LABEL",
  "autoResize": true,
  "lineHeight": 1.25,
  "boundElements": []
}
```

Position: `x = container.x + 10`, `y = container.y + (container.height - textHeight) / 2`
Size: `width = container.width - 20`, `height = lineCount × fontSize × 1.25`

For multi-line text, use `\n` in both `text` and `originalText`.

### Text (standalone / annotation)

Same as contained text but:
- `containerId`: `null`
- `verticalAlign`: `"top"`
- `textAlign`: `"left"`
- `strokeColor`: `"#6B7280"` (gray for annotations)
- `fontSize`: `14`

### Arrow

All common fields plus arrow-specific binding fields.

```json
{
  "type": "arrow",
  "strokeWidth": 1.5,
  "points": [[0, 0], [0, 68]],
  "startBinding": {
    "elementId": "r1",
    "focus": 0,
    "gap": 1
  },
  "endBinding": {
    "elementId": "r2",
    "focus": 0,
    "gap": 1
  },
  "startArrowhead": null,
  "endArrowhead": "arrow",
  "elbowed": false,
  "boundElements": []
}
```

Arrow position: calculated from the `fixedPoint` on the source shape's edge.
Points: `[[0, 0], [dx, dy]]` where dx/dy is the offset to the target's fixedPoint.

**fixedPoint bindings:** Arrows use explicit anchor points — `[0.5, 0]` = top center, `[0.5, 1]` = bottom center, `[0, 0.5]` = left center, `[1, 0.5]` = right center. When multiple arrows share the same edge, the generator aligns each exit/entry point with the connected shape's center for straight vertical/horizontal arrows.

**Arrowhead types:**

| Value | Appearance |
|-------|-----------|
| `null` | No arrowhead |
| `"arrow"` | Standard triangle (default for `endArrowhead`) |
| `"bar"` | Flat terminator line |
| `"dot"` | Circle/dot |
| `"triangle"` | Filled triangle |

For bidirectional arrows (two-way data flows), set both: `"startArrowhead": "arrow", "endArrowhead": "arrow"`.

**Arrow point patterns:**

| Pattern | Points | Use Case |
|---------|--------|----------|
| Straight down | `[[0,0], [0,h]]` | Vertical connection |
| Straight right | `[[0,0], [w,0]]` | Horizontal connection |
| L-right-down | `[[0,0], [w,0], [w,h]]` | Go right then down |
| L-down-right | `[[0,0], [0,h], [w,h]]` | Go down then right |
| L-down-left | `[[0,0], [0,h], [-w,h]]` | Go down then left |
| L-left-down | `[[0,0], [-w,0], [-w,h]]` | Go left then down |
| S-shape | `[[0,0], [0,h1], [w,h1], [w,h2]]` | Navigate around obstacles |
| U-turn (right) | `[[0,0], [50,0], [50,dy], [dx,dy]]` | Feedback loops (same-edge) |
| U-turn (bottom) | `[[0,0], [0,50], [dx,50], [dx,dy]]` | Callback arrows |

Multi-point arrows (3+ points) **must** set `"elbowed": true` for clean 90-degree rendering.

**Arrow routing decision tree** (for manual `points` overrides):

```
IF source bottom → target top:
  |dx| < 10?  → straight:  [[0,0], [0, dy]]
  otherwise   → L-shape:   [[0,0], [dx, 0], [dx, dy]]

IF source right → target left:
  |dy| < 10?  → straight:  [[0,0], [dx, 0]]
  otherwise   → L-shape:   [[0,0], [0, dy], [dx, dy]]

IF same edge (U-turn):
  clearance = 50px
  right:  [[0,0], [50, 0], [50, dy], [dx, dy]]
  bottom: [[0,0], [0, 50], [dx, 50], [dx, dy]]
```

For accent arrows (leading to/from accent nodes):
```json
{
  "strokeColor": "#B45309",
  "strokeWidth": 2
}
```

### Line (annotation leader)

Same as arrow but no bindings and no arrowheads.

```json
{
  "type": "line",
  "strokeWidth": 1,
  "strokeStyle": "dashed",
  "strokeColor": "#6B7280",
  "points": [[0, 0], [80, 0]],
  "startBinding": null,
  "endBinding": null,
  "startArrowhead": null,
  "endArrowhead": null
}
```

---

## Binding Rules (Critical)

Bindings are bidirectional. Both sides must reference each other or Excalidraw breaks silently.

**Text in a shape:**
- Shape's `boundElements` includes `{"id": "text-id", "type": "text"}`
- Text's `containerId` = shape's id

**Arrow connecting two shapes:**
- Arrow's `startBinding.elementId` = source shape id
- Arrow's `endBinding.elementId` = target shape id
- Source shape's `boundElements` includes `{"id": "arrow-id", "type": "arrow"}`
- Target shape's `boundElements` includes `{"id": "arrow-id", "type": "arrow"}`

**A shape with text AND arrows:**
```json
"boundElements": [
  {"id": "t1", "type": "text"},
  {"id": "a1", "type": "arrow"},
  {"id": "a2", "type": "arrow"}
]
```

---

## Index Ordering

Excalidraw uses `@excalidraw/fractional-indexing` with base-62 digits (`0-9`, `A-Z`, `a-z`). The head character encodes the integer length:
- `a` prefix → 2 chars total: `a0` through `az` (62 values)
- `b` prefix → 3 chars total: `b00` through `bzz` (3844 values)
- `c` prefix → 4 chars total: `c000` through `czzz`

**CRITICAL:** `b0`, `c0`, `c4` etc. are INVALID — `b` requires 2 digits after it, `c` requires 3. Fractional parts (anything after the integer) must NOT end with `0`.

Elements are assigned sequential integer-only indices. The generator handles this automatically. For 62 or fewer elements, all indices stay in `a0`–`az`. For larger diagrams, they overflow into `b00`+.

Pattern: shapes first (with their contained text interleaved), then arrows, then annotations. This keeps z-ordering correct.

---

## ID Convention

| Element type | Prefix | Example |
|-------------|--------|---------|
| Rectangle | `r` | r1, r2, r3 |
| Diamond | `d` | d1, d2 |
| Ellipse | `e` | e1, e2 |
| Contained text | `t` | t1, t2 |
| Arrow | `a` | a1, a2 |
| Annotation text | `at` | at1, at2 |
| Leader line | `ll` | ll1, ll2 |

---

## Seed and VersionNonce Ranges

Keep these in separate ranges to avoid collisions:
- Rectangle seeds: 101, 102, 103...
- Text seeds: 201, 202, 203...
- Arrow seeds: 301, 302, 303...
- Annotation text seeds: 401, 402...
- Line seeds: 501, 502...
- Diamond seeds: 601, 602...

VersionNonce follows the same pattern: 1001+ (rectangles), 2001+ (text), 3001+ (arrows), 4001+ (annotation text), 5001+ (lines), 6001+ (diamonds).

---

## Validation (Automated)

The generator runs a validation pass before outputting JSON. It catches:

1. **Orphaned bindings** — text `containerId` pointing to a missing shape, or shape `boundElements` referencing a missing text/arrow
2. **Asymmetric bindings** — arrow binds to a shape but the shape's `boundElements` doesn't list the arrow (or vice versa)
3. **Duplicate IDs** — two elements sharing the same ID
4. **Arrow bbox mismatch** — arrow `width`/`height` not matching `max(abs(point))` across all path points
5. **Multi-point elbow enforcement** — arrows with 3+ points must have `elbowed: true` and `roundness: null`
6. **Geometric proximity** — arrow start/end points must be within 15px of the bound shape's edge

If validation fails, the generator raises an error with details. Fix the spec and regenerate.

## Checklist Before Saving

1. Every shape with text has bidirectional binding (shape → text in boundElements, text → shape in containerId)
2. Every arrow has bidirectional binding (arrow → shapes in start/endBinding, shapes → arrow in boundElements)
3. All `index` values are unique, in order, and valid (`a0`–`az`, then `b00`+; never `b0`/`c0`/`c4`)
4. All `id` values are unique
5. All `seed` values are unique
6. Arrow `points` match the actual distance between source and target
7. Arrow `width`/`height` = `max(abs(point[0/1]))` across ALL points (not just the endpoint)
8. Arrow `x, y` position matches the staggered fixedPoint on the source shape's edge
9. Text fits inside its container (check character count × ~11px against container width - 20)
10. No missing required fields on any element

---

## Rules

- Always generate complete, valid JSON. Excalidraw fails silently on bad data.
- Never omit "boring" fields like `groupIds: []` or `frameId: null` — they're all required.
- Use the style defaults above unless the user requests a different look.
- For blog post diagrams, keep them simple: 3-8 nodes maximum. Complex diagrams lose clarity at typical blog content widths.
- If the user provides a rough sketch or description, interpret liberally. Ask only if genuinely ambiguous.
- Test text fitting: if a label is long, widen the node or split to two lines rather than letting it overflow.

## Related Skills

- **blog**: Diagrams often accompany blog posts
- **image-gen**: For raster illustrations (photos, editorial art). Excalidraw is for structural diagrams.

## Field-Tested Rules

- For complex diagrams (more than ~10 nodes), avoid cross-connecting elements within the main structure. Show relationships as separate workflow examples alongside the hierarchy instead.
- For diagrams with more than ~15 elements, write the spec for `generate_excalidraw.py` rather than hand-crafting JSON. Bidirectional bindings are too error-prone at scale.
- When placing side labels, compute position from the leftmost content edge across all tiers, not from a single tier's alignment.
- Generate files with `generate_excalidraw.py`. Live MCP collaboration tools render unreliably and aren't supported.
- Indices MUST follow Excalidraw's fractional-indexing format: `a` prefix = 2 chars (`a0`–`az`), `b` prefix = 3 chars (`b00`–`bzz`). Indices like `b0` or `c4` make files uneditable because Excalidraw can't generate new indices relative to malformed ones. The generator handles this; check it when hand-editing.

## Learnings

<!-- Updated by /reflect. Promote stable patterns to the main skill body. -->
