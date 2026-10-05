---
name: d3js
description: d3.js — data-driven document library for binding data to DOM, generating SVG visualizations, and creating interactive charts.
---

### selections
`d3.select(el)`, `d3.selectAll(selector)`. Chain `.attr()`, `.style()`, `.classed()`, `.text()`, `.html()`. Use `selection.call(fn)` for reusable behavior.

### data joins
`selection.data(data).join('circle')` — enter/update/exit pattern. Accessor: `d => d.value`. Key function for stable updates. `selection.datum()` for static data.

### scales
`d3.scaleLinear()`, `d3.scaleBand()` (ordinal), `d3.scaleTime()`, `d3.scaleSequential()` (color). Domain → range mapping. `.nice()` for clean axis ticks. `.clamp()` to bound output.

### axes
`d3.axisLeft(scale)`, `d3.axisBottom(scale)`. `.ticks(count)`, `.tickFormat(fn)`. Append to `<g>` with transform. Customize tick lines, labels, grid lines.

### SVG generation
Path generators: `d3.line()`, `d3.area()`, `d3.arc()` (pie), `d3.symbol()` (shapes). `d3.pie()` computes angles. `d3.curveMonotoneX` for smooth interpolation.

### transitions
`selection.transition().duration(500).ease(d3.easeCubic)`. Interpolate between values. `transition.delay()` for staggered. `transition.attrTween()` for custom.

### d3-force
`d3.forceSimulation(nodes)`. Forces: `forceLink`, `forceManyBody` (charge), `forceCenter`, `forceCollide`. `.on("tick", render)`. `simulation.alpha()` for cooling.

### geo projections
`d3.geoAlbersUsa()`, `d3.geoMercator()`, `d3.geoOrthographic()`. `.fitSize([w, h], geojson)`. `d3.geoPath(projection)` renders GeoJSON to SVG paths.

### hierarchy
`d3.hierarchy(data)`, `d3.tree()`, `d3.cluster()`, `d3.pack()` (circle packing), `d3.partition()` (icicle), `d3.treemap()`. `.descendants()`, `.links()` for data extraction.

### best practices
Use `<g>` groups for reusable chart components. Debounce resize handlers. Use Canvas for >1000 elements. Separate concerns (data prep, scale, draw, interact).
