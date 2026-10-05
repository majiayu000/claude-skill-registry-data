---
name: excalidraw
description: |
  Generates Excalidraw diagrams programmatically as hand-drawn-style JSON. Use when creating architecture diagrams, flowcharts, or hand-drawn-style visuals for documentation, or when converting existing diagrams to editable Excalidraw JSON.
metadata:
  processkit:
    apiVersion: processkit.projectious.work/v1
    id: SKILL-excalidraw
    version: "1.1.0"
    created: 2026-04-06T00:00:00Z
    category: design
---

# Excalidraw

## Intro

Excalidraw files are JSON with a top-level `elements` array of shapes,
text, and arrows. Generate them directly to produce hand-drawn-style
architecture diagrams, flowcharts, and documentation visuals that stay
editable in the Excalidraw app.

## Overview

### File shape

An `.excalidraw` file has a fixed envelope and a list of elements:

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "generated",
  "elements": [],
  "appState": {
    "viewBackgroundColor": "#ffffff",
    "gridSize": 20
  },
  "files": {}
}
```

Every element carries `id` (unique 8+ char string), `type`, position
(`x`, `y`), dimensions, and styling: `strokeColor`, `backgroundColor`,
`fillStyle` (`solid` / `hachure` / `cross-hatch`), `strokeWidth`
(1/2/4), `roughness` (0 architect, 1 artist, 2 cartoonist), `opacity`
(0-100), plus `groupIds` and `boundElements` for linking.

### Element types

Use `rectangle` (with `roundness: { type: 3 }` for rounded corners)
for boxes and containers, `ellipse` for soft nodes, `diamond` for
decisions, `text` for labels, and `arrow` / `line` for connections.
`freedraw` and `image` are available but rarely generated.

```json
{
  "id": "rect1", "type": "rectangle",
  "x": 100, "y": 100, "width": 200, "height": 80,
  "strokeColor": "#1e1e1e", "backgroundColor": "#a5d8ff",
  "fillStyle": "solid", "strokeWidth": 2, "roughness": 1,
  "roundness": { "type": 3 }
}
```

Text elements set `text`, `fontSize`, `fontFamily` (1 = Virgil
hand-drawn, 2 = Helvetica, 3 = Cascadia mono), `textAlign`, and
`verticalAlign`. Arrows use `points` relative to `x, y` plus optional
`startBinding` / `endBinding` linking to target element IDs.

### Binding text to shapes

To label a shape, create a text element and bind both sides:

1. On the container: add `"boundElements": [{"id": "textId", "type":
   "text"}]`.
2. On the text: set `"containerId": "shapeId"` and size the text to
   fit inside the container.
3. Excalidraw auto-centers the text within the shape.

### Layout guidelines

- Align coordinates to multiples of 20 (matches the default grid).
- Leave 80-120px between connected elements.
- Use left-to-right for flows and pipelines, top-to-bottom for
  hierarchies.
- Group related elements with a shared `groupIds` entry.
- Label every shape; keep one idea per diagram and split if it grows
  beyond a single viewport.
- Titles 28-32px, labels 20-24px, annotations 16-18px, never below
  16px.
- Give similar elements the same width and height for visual rhythm.

### Semantic color palette

Pick from this palette and stay consistent within a diagram:

| Role | Fill (`backgroundColor`) | Stroke (`strokeColor`) |
|---|---|---|
| Primary / action | `#a5d8ff` | `#1971c2` |
| Secondary / support | `#d0bfff` | `#6741d9` |
| Success / positive | `#b2f2bb` | `#2f9e44` |
| Warning / caution | `#ffec99` | `#e8590c` |
| Danger / error | `#ffc9c9` | `#e03131` |
| Neutral / container | `#e9ecef` | `#495057` |

Set `"fillStyle": "solid"` when a shape is filled.

### Diagram types

- **Architecture:** rectangles for services and databases (rounded
  corners), arrows for data flow with labels, a larger container
  rectangle grouping related services, colors by layer (frontend
  blue, backend green, data yellow).
- **Flowchart:** diamonds for decisions, rectangles for processes,
  ellipses for start/end, consistent direction, "Yes"/"No" labels on
  decision arrows.
- **Sequence-style:** vertical arrangement with horizontal arrows,
  operation names on each arrow, dashed arrows for responses.

### Embedding in docs

Save the `.excalidraw` source for editing, export SVG or PNG for
embedding. GitHub renders `.excalidraw.png` directly in Markdown. The
Excalidraw VS Code extension renders `.excalidraw` files in-editor.

## Gotchas

Agent-specific failure modes — provider-neutral pause-and-self-check items:

- **Using short or sequential element IDs like "1", "2", "3".** Element IDs must be globally unique across the file. Duplicate or predictable IDs cause Excalidraw to silently overwrite or misrender elements. Use random 8+ character strings as the spec requires.
- **Placing coordinates without snapping to the 20px grid.** Elements at arbitrary coordinates (e.g., `x: 73, y: 117`) appear misaligned when the file is opened and manually edited. Snap all positions to multiples of 20 to match the default grid.
- **Omitting `boundElements` or `containerId` for labeled shapes.** A text element placed visually on top of a shape is not bound to it — moving the shape leaves the label behind. To label a shape, both the container's `boundElements` and the text's `containerId` must reference each other.
- **Generating bindings that reference non-existent element IDs.** Arrows with `startBinding` or `endBinding` pointing to IDs not present in the `elements` array fail to render their connections. Always verify that every binding target ID exists in the file before emitting.
- **Using `image` elements without populating the `files` object.** Excalidraw image elements reference a file ID that must appear as a key in the top-level `files` object with base64-encoded content. Omitting this entry renders a broken image placeholder.
- **Generating all elements at the same coordinates.** Without a deliberate layout plan — left-to-right for flows, top-to-bottom for hierarchies, 80-120px between nodes — elements overlap on open and the diagram is unusable. Plan the coordinate layout before emitting any elements.
- **Emitting incomplete JSON that omits required top-level keys.** A file missing `type`, `version`, `appState`, or `files` (even as an empty `{}`) fails validation when loaded in Excalidraw. Always emit the complete v2 envelope even for minimal diagrams.

## Full reference

### Full element property reference

Common properties across all element types:

```
id              string    Unique identifier (use descriptive IDs)
type            string    rectangle|ellipse|diamond|text|arrow|
                          line|freedraw|image
x, y            number    Position (top-left corner)
width, height   number    Bounding box size
angle           number    Rotation in radians (default 0)
strokeColor     string    Border/line color (hex)
backgroundColor string    Fill color (hex, or "transparent")
fillStyle       string    "solid" | "hachure" | "cross-hatch"
strokeWidth     number    1 (thin), 2 (normal), 4 (bold)
strokeStyle     string    "solid" | "dashed" | "dotted"
roughness       number    0 (architect) | 1 (artist) | 2 (cartoonist)
opacity         number    0-100
roundness       object    { "type": 3 } for rounded corners, null for sharp
isDeleted       boolean   Soft-delete flag (default false)
boundElements   array     [{ "id": "...", "type": "text|arrow" }]
groupIds        array     Group IDs for visually grouping elements
```

Text-specific properties:

```
text            string    The displayed text
fontSize        number    Size in px (16-32 typical)
fontFamily      number    1 (Virgil/hand), 2 (Helvetica), 3 (Cascadia/mono)
textAlign       string    "left" | "center" | "right"
verticalAlign   string    "top" | "middle"
containerId     string    ID of parent container (for bound text)
```

Arrow and line properties:

```
points          array     [[0,0], [dx,dy]] - relative to x,y
startBinding    object    { "elementId": "id", "focus": 0, "gap": 4 }
endBinding      object    { "elementId": "id", "focus": 0, "gap": 4 }
startArrowhead  string    null | "arrow" | "dot" | "bar"
endArrowhead    string    null | "arrow" | "dot" | "bar"
```

`focus` ranges from -1 to 1 and controls where the arrow attaches
(0 = center). `gap` is the space between the arrowhead and the target
border. Target elements must list the arrow in their `boundElements`.

### Minimal valid file

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "generated",
  "elements": [
    {
      "id": "box1",
      "type": "rectangle",
      "x": 100,
      "y": 100,
      "width": 200,
      "height": 80,
      "strokeColor": "#1971c2",
      "backgroundColor": "#a5d8ff",
      "fillStyle": "solid",
      "strokeWidth": 2,
      "roughness": 1,
      "opacity": 100,
      "angle": 0,
      "groupIds": [],
      "roundness": { "type": 3 },
      "boundElements": [
        { "id": "label1", "type": "text" }
      ],
      "isDeleted": false
    },
    {
      "id": "label1",
      "type": "text",
      "x": 140,
      "y": 125,
      "width": 120,
      "height": 30,
      "text": "Service A",
      "fontSize": 20,
      "fontFamily": 1,
      "textAlign": "center",
      "verticalAlign": "middle",
      "containerId": "box1",
      "strokeColor": "#1e1e1e",
      "backgroundColor": "transparent",
      "fillStyle": "solid",
      "strokeWidth": 1,
      "roughness": 1,
      "opacity": 100,
      "angle": 0,
      "groupIds": [],
      "boundElements": null,
      "isDeleted": false
    }
  ],
  "appState": {
    "viewBackgroundColor": "#ffffff",
    "gridSize": 20
  },
  "files": {}
}
```

### Common patterns

- **Container with children:** use a large rectangle as a visual
  container with smaller elements inside. Bind arrows to the
  container, not to the children.
- **Labeled arrow:** create an arrow between two shapes, then add a
  standalone text element positioned near the arrow's midpoint. Arrow
  labels do not need `containerId`.
- **Decision diamond:** use `type: "diamond"` with bound text.
  Connect "Yes" and "No" arrows from different sides and label each
  arrow with a nearby text element.
- **Grouping:** assign the same `groupIds` entry to multiple elements
  to link them as a visual group.

### References

- `references/json-schema.md` — full element schema and minimal file
  template.
