---
name: evo-dialogue-dotgen
description: Generates Graphviz DOT visualization files from parsed dialogue graph structures using the graphviz 0.20.3 Python API.
---

# evo-dialogue-dotgen

Generates DOT visualization from dialogue graphs.

## Key Functions

- `generate_dot(graph: dict, output_path: str)` - Generate DOT file from graph
- `escape_label(text: str) -> str` - Safely escape text for DOT labels
- `style_node(node_type: str) -> dict` - Get visual styling by node type

## Usage
```python
import sys
sys.path.insert(0, "/app/environment/skills/evo-dialogue-dotgen/scripts")
from utils import generate_dot

generate_dot(graph, "/app/dialogue.dot")
```
