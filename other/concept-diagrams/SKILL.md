---
name: concept-diagrams
description: "Minimal SVG diagrams as standalone HTML files."
allowed-tools:
  - write_file
  - read_file
enabled: true
related-skills: [architecture-diagram]
license: MIT
author: Adapted from hermes-agent (Nous Research, MIT); v1k22
---

# Concept Diagrams

## Overview

Generate production-quality SVG diagrams with a unified flat, minimal design
system. Output is a single self-contained HTML file that renders identically in
any modern browser, with automatic light/dark mode.

## Scope

**Best suited for:**
- Physics setups, chemistry mechanisms, math curves, biology
- Physical objects (aircraft, turbines, smartphones, mechanical watches)
- Anatomy, cross-sections, exploded layer views
- Floor plans, architectural conversions
- Narrative journeys (lifecycle of X, process of Y)
- Hub-spoke system integrations (smart city, IoT)
- Educational / textbook-style visuals in any domain

**Look elsewhere first for:**
- Software/cloud architecture with dark tech aesthetic → use
  `architecture-diagram`
- Hand-drawn whiteboard sketches → use an excalidraw-style tool

## Workflow

1. Decide on the diagram type (see below)
2. Lay out components using the Design System rules
3. Write the full HTML page with inline SVG + CSS
4. Save as a standalone `.html` file via `write_file`
5. User opens it directly in a browser — no server, no dependencies

```
write_file("diagram.html", "<full HTML with inline SVG + CSS>")
```

## Diagram Types

| Type | When |
|------|------|
| **Process flow** | Sequential steps, lifecycle, pipeline |
| **Hub-spoke** | Central system + connected components (IoT, smart city) |
| **Exploded layers** | Component breakdown, cross-section |
| **Comparison** | Side-by-side, before/after |
| **Cycle** | Circular process, feedback loop |
| **Hierarchy** | Org chart, taxonomy, tree |
| **Timeline** | Chronological events |

## Design System

### Philosophy
- **Flat, minimal, no 3D effects**
- **Semantic colors**: 9 color ramps for different element types
- **Sentence-case typography**: not Title Case
- **Automatic dark mode**: CSS `prefers-color-scheme`

### Color Ramps (light/dark aware)

```css
:root {
  /* Primary elements */
  --c-primary: #4A90D9;
  --c-secondary: #50C878;
  --c-accent: #F5A623;

  /* Semantic */
  --c-input: #7B68EE;
  --c-output: #FF6B6B;
  --c-process: #4ECDC4;
  --c-data: #95E1D3;
  --c-control: #C4A7E7;
  --c-external: #DDD;

  /* Light mode (default) */
  --bg: #FAFAFA;
  --text: #333;
  --border: #E0E0E0;
}

@media (prefers-color-scheme: dark) {
  :root {
    --bg: #1A1A2E;
    --text: #EEE;
    --border: #333;
    --c-external: #444;
  }
}
```

### SVG Structure

```html
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Diagram Title</title>
<style>
  body { margin: 0; padding: 40px; background: var(--bg); }
  svg { display: block; margin: 0 auto; }
  .label { font-family: -apple-system, sans-serif; font-size: 14px; fill: var(--text); }
  .title { font-size: 18px; font-weight: 600; }
  .box { fill: var(--c-primary); opacity: 0.15; stroke: var(--c-primary); stroke-width: 2; rx: 8; }
  .arrow { stroke: var(--text); stroke-width: 2; fill: none; marker-end: url(#arrowhead); }
</style>
</head>
<body>
<svg width="800" height="600" viewBox="0 0 800 600">
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="var(--text)"/>
    </marker>
  </defs>
  <!-- Diagram elements here -->
  <rect class="box" x="50" y="50" width="200" height="80"/>
  <text class="label title" x="150" y="90" text-anchor="middle">Input</text>
  <path class="arrow" d="M 250 90 L 350 90"/>
  <!-- ... more elements ... -->
</svg>
</body>
</html>
```

## Pitfalls

- **Too much detail**: keep diagrams minimal. One concept per diagram.
- **Inconsistent spacing**: use a grid (e.g., 50px increments) for alignment.
- **No dark mode**: always include `prefers-color-scheme` media query.
- **Font not embedded**: use system fonts (-apple-system, sans-serif) so the
  HTML works without external font files.
- **SVG overflow**: set `viewBox` correctly so the diagram isn't clipped.
