---
name: architecture-diagram
description: "Dark-themed SVG architecture/cloud/infra diagrams as HTML."
allowed-tools:
  - write_file
  - read_file
enabled: true
related-skills: [concept-diagrams]
license: MIT
author: Adapted from hermes-agent (Nous Research, MIT); Cocoon AI
---

# Architecture Diagram

## Overview

Generate professional, dark-themed technical architecture diagrams as
standalone HTML files with inline SVG graphics. No external tools, no API keys,
no rendering libraries — just write the HTML file and open it in a browser.

## Scope

**Best suited for:**
- Software system architecture (frontend / backend / database layers)
- Cloud infrastructure (VPC, regions, subnets, managed services)
- Microservice / service-mesh topology
- Database + API map, deployment diagrams
- Anything with a tech-infra subject that fits a dark, grid-backed aesthetic

**Look elsewhere first for:**
- Physics, chemistry, math, biology → use `concept-diagrams`
- Floor plans, educational visuals → use `concept-diagrams`
- Hand-drawn sketches → use excalidraw

## Workflow

1. User describes their system architecture (components, connections,
   technologies)
2. Generate the HTML file following the design system below
3. Save with `write_file` to a `.html` file
4. User opens in any browser — works offline, no dependencies

```
write_file("architecture.html", "<full HTML with inline SVG + CSS>")
```

### Output Location

```bash
# Default to current working directory
./[project-name]-architecture.html
```

## Design System

### Aesthetic
- **Dark background**: deep navy or black (#0a0a1a, #111)
- **Grid pattern**: subtle dot or line grid in background
- **Neon accents**: luminous colors for different component types
- **Monospace labels**: for technical authenticity
- **Rounded corners**: on boxes (rx=6)
- **Glow effects**: subtle box-shadow on key components

### Color Palette

```css
:root {
  --bg: #0a0a1a;
  --grid: #1a1a2e;

  /* Component types */
  --c-frontend: #00D9FF;    /* cyan */
  --c-backend: #50C878;     /* green */
  --c-database: #F5A623;    /* orange */
  --c-external: #C4A7E7;    /* purple */
  --c-queue: #FF6B6B;       /* red */
  --c-cache: #FFD700;       /* gold */

  --text: #E0E0E0;
  --text-dim: #888;
  --border: #333;
}
```

### SVG Template

```html
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Architecture Diagram</title>
<style>
  body {
    margin: 0; padding: 40px;
    background: var(--bg);
    background-image: radial-gradient(circle, var(--grid) 1px, transparent 1px);
    background-size: 30px 30px;
  }
  svg { display: block; margin: 0 auto; }
  .component {
    stroke-width: 2; rx: 6; ry: 6;
    fill-opacity: 0.1;
  }
  .label {
    font-family: 'SF Mono', 'Fira Code', monospace;
    font-size: 13px; fill: var(--text);
  }
  .label-type {
    font-size: 10px; fill: var(--text-dim);
    text-transform: uppercase; letter-spacing: 1px;
  }
  .connection {
    stroke: var(--text-dim); stroke-width: 1.5;
    fill: none; stroke-dasharray: 4 2;
    marker-end: url(#arrow);
  }
</style>
</head>
<body>
<svg width="1000" height="700" viewBox="0 0 1000 700">
  <defs>
    <marker id="arrow" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">
      <path d="M0,0 L8,3 L0,6 Z" fill="var(--text-dim)"/>
    </marker>
  </defs>

  <!-- Frontend Layer -->
  <rect class="component" x="50" y="50" width="200" height="80"
        stroke="var(--c-frontend)" fill="var(--c-frontend)"/>
  <text class="label" x="150" y="85" text-anchor="middle">Web App</text>
  <text class="label-type" x="150" y="105" text-anchor="middle">Frontend</text>

  <!-- Backend Layer -->
  <rect class="component" x="400" y="50" width="200" height="80"
        stroke="var(--c-backend)" fill="var(--c-backend)"/>
  <text class="label" x="500" y="85" text-anchor="middle">API Server</text>
  <text class="label-type" x="500" y="105" text-anchor="middle">Backend</text>

  <!-- Database Layer -->
  <rect class="component" x="750" y="50" width="200" height="80"
        stroke="var(--c-database)" fill="var(--c-database)"/>
  <text class="label" x="850" y="85" text-anchor="middle">PostgreSQL</text>
  <text class="label-type" x="850" y="105" text-anchor="middle">Database</text>

  <!-- Connections -->
  <path class="connection" d="M 250 90 L 400 90"/>
  <path class="connection" d="M 600 90 L 750 90"/>
</svg>
</body>
</html>
```

## Diagram Patterns

### Layered Architecture
- Frontend (top) → Backend (middle) → Database (bottom)
- Horizontal layers with vertical connections

### Microservice Topology
- Central API gateway + surrounding services
- Bidirectional connections for sync, one-way for async

### Cloud Infrastructure
- VPC as a large container box
- Subnets as inner boxes
- Managed services as icons (S3, Lambda, RDS)

### Data Flow
- Left-to-right flow
- Different line styles for sync (solid) vs async (dashed)

## Pitfalls

- **Too many components**: keep to 5-10 boxes max. More = unreadable.
  Split into multiple diagrams if needed.
- **Crossing lines**: route connections to minimize crossings. Use right-angle
  paths.
- **No legend**: if using color-coded component types, include a legend.
- **Font sizing**: labels must be readable. 13px minimum for component names.
