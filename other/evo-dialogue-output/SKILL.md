---
name: evo-dialogue-output
description: Serializes dialogue graph to JSON file and generates Graphviz DOT visualization. Handles UTF-8 encoding, DOT node styling by type, and edge labeling.
---

# Dialogue Output

Exports a dialogue graph to JSON and Graphviz DOT format.

## Key Functions
- `export_json(graph, path)` - Write graph to JSON with UTF-8
- `export_dot(graph, path)` - Generate DOT file with styled nodes
- `generate_dot_visualization(graph, path)` - Alias for export_dot
