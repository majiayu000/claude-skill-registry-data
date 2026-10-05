---
name: make-flowchart
description: Create one accurate readable flowchart from an explicit process model with verified nodes, decisions, labels, and connections. Use for process, decision, system, or workflow diagrams; do not use for infographics, floor plans, freeform illustrations, project schedules, or diagrams whose source logic is unknown.
---
# Make Flowchart

## Catalog

- Display name: Make Flowchart
- Categories: Layout & Design, Utility
- Status: Ready
- Route label: GPT Image 2 flowchart rendering
- Tone: blue
- Short description: Create one accurate readable flowchart from an explicit process model with verified nodes, decisions and connections.
## What this skill does

- Converts a process into semantically correct start, process, decision and end nodes.
- Checks graph logic before styling and keeps the final flow on one readable canvas.

## How to use

Provide process goal, actors, ordered steps, decisions, branch labels, exceptions and direction.

#### Example

```text
Create a top-down flowchart: Request received → Complete?; No → Ask for details → back; Yes → Resolve → End.
```

## Workflow

1. Normalize the process into unique node IDs and a directed edge list before drawing.
2. Validate reachability, branch labels, cycles, terminal nodes and reading direction.
3. Render the verified graph directly with GPT Image 2 Medium/2K because the final requires exact readable labels; never treat `flowchart-generator` as a model. If text still fails acceptance, render the validated graph and copy deterministically instead of changing image models.
4. Inspect text, arrow endpoints, crossings, node semantics and terminal placement.

## User-facing output

- Media type: One flowchart image
- Default quantity: 1
- Content per image: One semantically verified process diagram
- Default layout: Source-preserving or dimension-defined format
- Model policy: GPT Image 2 Medium/2K; deterministic diagram rendering is the fallback for exact-copy failure
- Downstream use: Process communication
