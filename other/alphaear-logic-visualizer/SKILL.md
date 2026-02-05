---
name: alphaear-logic-visualizer
description: Create visualize logic diagrams (e.g., Draw.io XML) to explain complex transmission chains or logic flows.
---

# AlphaEar Logic Visualizer Skill

## Overview

This skill specializes in creating visual representations of logic flows, specifically generating Draw.io XML compatible diagrams. It is useful for visualizing investment theses or signal transmission chains.

## Capabilities

### 1. Generate Draw.io Diagrams

Use `scripts/visualizer.py` to generate XML for diagrams.

**Key Components:**

-   `generate_logic_diagram(nodes, edges)`: Create a diagram structure.
-   **Output**: XML string compatible with Draw.io.

**Example Usage (Python):**

```python
from scripts.visualizer import AlphaEarVisualizer

viz = AlphaEarVisualizer()
# This method would wraps the logic to produce XML
xml_output = viz.generate_logic_diagram(
    nodes=["Event A", "Impact B", "Stock C"],
    edges=[("Event A", "Impact B"), ("Impact B", "Stock C")]
)
print(xml_output)
```

## Dependencies

-   None (Standard Library for string manipulation).
