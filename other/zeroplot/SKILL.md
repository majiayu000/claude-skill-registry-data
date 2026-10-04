---
name: zeroplot
description: "Create editable charts, diagrams, figures, posters, or slides from intent, data, or references."
---

# ZeroPlot

**Plot anything with zero effort.**

## Core Scope

Use this skill when the user needs:

- a chart, diagram, scientific figure, poster, or slide;
- an editable visual reconstructed from a screenshot or reference image;
- a visual generated from data, code, text, netlists, specs, or rough sketches;
- a domain-specific visual grammar or review rubric;
- a benchmark case for visual generation.

## Non-Goals

- Do not claim to replace professional EDA, CAD, statistical, or simulation
  tools.
- Do not optimize only for visual prettiness.
- Do not invent scientific content not present in the user's materials.
- Do not flatten structured outputs when an editable format is available.

## Workflow

1. Identify artifact type, audience, and visual domain.
2. Collect source materials and constraints.
3. Read the matching domain note under `domains/` when available.
4. Convert inputs into an auditable visual spec.
5. Produce a baseline artifact in an editable format when possible.
6. Ask for or infer domain-specific failure criteria.
7. Distill failures into rubric items and skill rules.
8. Re-run generation with updated rules.
9. Save benchmark artifacts when the task is part of evaluation.

## Visual Contract

Before generation, define:

- artifact type and domain;
- audience and delivery context;
- source inputs;
- target output format;
- must-preserve entities and relationships;
- hard-fail criteria;
- stylistic conventions;
- evaluation plan.

## Output Preference

Prefer editable outputs over flat images:

1. `.drawio`, SVG, Mermaid, TikZ, matplotlib source, PPTX, or structured JSON;
2. PDF/PNG export for delivery;
3. flat raster only when no editable route is available.

## Initial Domains

Initial seed domains:

- `domains/integrated-circuits/`
- `domains/computer-science/`

Scientific figures are ZeroPlot's first proving ground, not its product
boundary. Later packs may cover general charts, posters, presentations, and
other structured visual artifacts.

### Integrated Circuits

Turn SPICE/netlists, EDA screenshots, paper text, sketches, component tables,
and visual references into readable, editable technical communication.

### Computer Science

Create system diagrams, model architectures, pipelines, dataflows, evaluation
setups, and result figures with clear structure and reproducible editing
handles.
