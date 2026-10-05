---
name: visualize-floor-plan
description: Turn a supplied floor plan or dimensioned spatial brief into one readable plan or spatial visualization without changing topology. Use for communicating rooms, circulation, dimensions, and layout; do not use for room restyling, landscape redesign, construction documents, or inventing missing measurements.
---
# Visualize Floor Plan

## Catalog

- Display name: Visualize Floor Plan
- Categories: Layout & Design, Utility
- Status: Ready
- Route label: GPT Image 2 plan visualization
- Tone: cyan
- Short description: Turn a supplied floor plan or dimensioned brief into one readable visualization without changing topology.

## What this skill does

- Transforms a plan into a cleaned, furnished or axonometric plan visualization.
- Preserves room adjacency, openings, circulation and supplied dimensions; it is not construction documentation.

## How to use

Provide a plan image or dimensioned brief, room names, openings, visualization type and required labels.

#### Example

```text
Create one clean furnished top-down plan from this sketch; preserve walls, doors and adjacency; label the five rooms exactly.
```

## Workflow

1. Read topology, scale cues, labels, doors, windows and dimensions; list uncertainties.
2. Choose top-down, axonometric or rendered-plan output and lock topology invariants.
3. Use GPT Image 2 Medium for text and layout fidelity.
4. Verify every room, adjacency, opening direction, label and dimension; disclose non-construction status.

When this Skill selects GPT Image 2, use `quality: "medium"` and `imageSize: "2K"` by default; change either only when the user explicitly requests another tier.

Every GPT Image 2 call in this Skill defaults to Medium at 2K; use another tier only when the user explicitly requests it.

## User-facing output

- Media type: One floor-plan visualization
- Default quantity: 1
- Content per image: One topology-faithful plan view
- Default layout: Source-preserving or dimension-defined format
- Model policy: GPT Image 2 plan visualization
- Downstream use: Early space planning
