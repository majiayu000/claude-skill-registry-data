---
name: evo-d3v6-stock-visualization
description: Generates the complete visualization.js file implementing a D3.js v6 force-simulation bubble chart with sector clustering, an interactive data table, tooltips, legends, and bidirectional click-based highlighting between chart and table.
---

# evo-d3v6-stock-visualization

Generates visualization.js with D3.js v6 force-simulation bubble chart, data table, and interactions.

## Usage

```python
import sys
sys.path.insert(0, '/app/environment/skills/evo-d3v6-stock-visualization/scripts')
from utils import generate_visualization_js

generate_visualization_js('/root/output/js/visualization.js')
```

## Functions

- `generate_visualization_js(output_path)` - Generates complete visualization.js
- `build_force_simulation_code()` - Returns JS for force simulation with sector clustering
- `build_bubble_chart_code()` - Returns JS for SVG bubble chart with labels, legend, tooltip
- `build_data_table_code()` - Returns JS for HTML data table with formatted market cap
- `build_interaction_code()` - Returns JS for bidirectional click highlighting
- `format_market_cap_js()` - Returns JS function to format numbers as 1.64T, 232.51B, etc.

## Key Design Decisions

- D3 v6 event signature: `(event, d)` not `(d, i)`
- scaleSqrt for area-proportional bubble sizing
- ETFs get uniform radius (no marketCap data)
- No tooltip shown for ETF entries
- forceX/forceY with sector-specific coordinates for clustering
- forceCollide prevents overlap
- Bidirectional click: bubble click highlights table row (scrolls into view), table row click highlights bubble
