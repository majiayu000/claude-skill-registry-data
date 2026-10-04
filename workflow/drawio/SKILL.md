---
name: drawio
description: Use when the user asks to create, edit, rebuild, or refine editable diagrams in `.drawio` / diagrams.net format, especially for academic figures such as system architecture diagrams, technical roadmaps, workflow diagrams, method pipelines, module relationship diagrams, and experiment flowcharts. Use this skill when the user wants publication-ready outputs with both an editable source file and a PNG export, or when an existing figure image needs to be rebuilt into a clean editable academic-style diagram.
---

# Drawio

## Overview

This skill creates and updates editable `diagrams.net` / `.drawio` figures for academic and thesis workflows.

Its default delivery contract is:
- one editable `.drawio` source file
- one matching `PNG` export

These are mandatory defaults unless the user explicitly overrides them:
- all in-diagram text must use `26px`
- the editable `.drawio` source file must always be delivered together with the rendered image output
- draw connectors with orthogonal routing that uses explicit anchors plus bend points, not straight point-to-point segments

## Publication Quality Bar

- Treat every requested figure as a paper-ready asset unless the user explicitly asks for a rough draft.
- The figure must be understandable on its own without oral explanation of arrow meaning or reading order.
- The final output should be suitable for direct insertion into a thesis, report, or paper without manual cleanup in another tool.

## When To Use

Use this skill when the user asks for:
- a system architecture diagram
- a technical roadmap
- a workflow or method pipeline figure
- a module relationship diagram
- an experiment design or ablation flowchart
- an editable `.drawio` version rebuilt from an image
- a thesis figure that must remain readable on A4 pages

Do not use this skill for:
- raster illustration generation
- slide deck authoring
- data charts that should be produced from tables or plotting tools

## Required Output Standard

Unless the user explicitly asks otherwise, always deliver:
- `.drawio` source
- `PNG` export

Keep names, contents, and versions aligned.

Treat both files as required outputs, not optional nice-to-haves. If you revise an existing figure, update the editable `.drawio` source and the exported `PNG` together.

## Hard Layout And Delivery Requirements

- Always produce an editable `.drawio` file that opens correctly in diagrams.net.
- Always produce a matching `PNG` export from the same final diagram state.
- Never deliver only an image when the task is handled by this skill; the `.drawio` source file is required.
- Keep the `.drawio` filename and `PNG` filename aligned so the pair is obviously related.
- Ensure the exported `PNG` is readable when inserted into an A4 thesis or paper page at normal viewing scale.
- Do not stop after generating raw boxes and arrows; finish the layout to a presentation-ready state.
- If a diagram still has awkward connector overlaps, crowded labels, or unreadable text, it is not finished.

## Export Requirements

- Export `PNG` with an opaque white or very light background unless the user explicitly asks for transparency.
- Export at publication-ready resolution; target roughly 2200 px or more on the longer side unless the user requests another size.
- Ensure no text, arrowheads, container labels, or outer shapes are clipped by the export bounds.
- Keep a small outer margin so the figure does not appear cramped against the PNG edges.
- If the figure is intended for single-column placement, optimize for narrow width before adding more detail.
- If the figure is intended for full-width placement, use the extra width to improve spacing rather than packing in more text.

## Reading Order

Read these references as needed:
- `references/academic-diagram-style.md`
  Use for academic-paper visual rules and readability checks.
- `references/figure-types.md`
  Use when deciding whether the target figure should be an architecture diagram, roadmap, or process flow.

Use this script when starting from scratch:
- `scripts/new-drawio-figure.ps1`
  Creates a clean starter `.drawio` file that opens in diagrams.net and includes an orthogonal anchor-plus-waypoint connector sample.
- `scripts/export-drawio-png.ps1`
  Exports a finalized `.drawio` file to a matching `PNG` using the installed draw.io / diagrams.net desktop app.

## Workflow

1. Identify the figure type and where it will appear in the paper.
2. Decide the right granularity so the new figure does not duplicate the role of another figure.
3. Build or revise the editable `.drawio` source first.
4. Adjust node positions, connector routing, spacing, and typography until the figure is presentation-ready.
5. Export a `PNG` from the same finalized content, preferably with `scripts/export-drawio-png.ps1`.
6. Check text density, connector clarity, box sizing, and A4 readability.
7. Run the final quality gate before considering the task complete.
8. If the user already established a delivery rule, keep following that rule.

## Figure-Type Guidance

### System Architecture

Use architecture diagrams to show:
- modules
- boundaries
- data flow
- component interaction

The emphasis should be on system composition and runtime relationship.

### Technical Roadmap

Use technical roadmaps to show:
- research stages
- method progression
- experiment path
- stage outputs

The emphasis should be on progression rather than runtime structure.

### Workflow Or Process Figure

Use process figures to show:
- step order
- decision points
- branching
- loops or fallback paths

The emphasis should be on execution sequence and control logic.

## Practical Rules

- Prefer concise noun phrases inside nodes.
- Avoid paragraph-length node text.
- Use low-saturation colors and restrained decoration.
- Do not let architecture diagrams and roadmaps collapse into the same visual grammar.
- If the desktop draw.io app is unavailable, it is acceptable to generate standard `.drawio` XML directly, as long as diagrams.net can open it.
- When revising an existing figure, preserve the user's semantics unless a redesign is explicitly requested.
- Prefer one dominant reading direction per figure: top-to-bottom or left-to-right.
- Keep sibling nodes aligned and visually balanced instead of hand-placing everything irregularly.
- Use labels on connectors only when the meaning cannot be made obvious through layout and arrow direction alone.

## Geometry And Spacing Requirements

- Keep sibling nodes on a visible grid rather than near-aligned by eye.
- Keep adjacent nodes typically separated by about 24-40 px of whitespace at starter-canvas scale.
- Keep major layers or grouped sections typically separated by about 40-80 px.
- Keep text away from box borders with enough internal padding to avoid a cramped appearance.
- Use consistent border widths and corner radii for comparable elements.
- Keep visually related nodes at comparable sizes unless size is being used intentionally to encode meaning.
- If a figure contains grouped subsystems, use labeled containers or background bands rather than loose visual proximity alone.

## Connector Routing Requirements

- Do not leave default messy connector paths if they create avoidable overlaps or visual ambiguity.
- Place connectors so they do not run through text, cut across boxes, or obscure arrowheads.
- Use orthogonal routing as the default connector strategy for structured diagrams.
- Do not draw connectors as direct start-to-end straight segments when the path should turn around layout constraints.
- Attach connectors to explicit side anchors so the flow direction reads naturally at the source and target nodes.
- When a connector needs one or more turns, define explicit bend points or waypoints rather than relying on loose diagonal segments or implicit auto-routing.
- Reduce line crossings aggressively; if crossings remain, they should be rare and justified by the layout.
- Adjust elbow points, bend points, and box positions manually when needed rather than accepting awkward auto-routing.
- Keep enough whitespace around connector bends so the path is visually traceable.
- If a connector path becomes too crowded, move the surrounding nodes instead of compressing the line further.
- Keep connector stroke style and arrowhead style consistent for the same semantic relationship.
- Use decision labels such as `Yes` / `No` only where branching would otherwise be ambiguous.

## Typography Requirements

- Use a clean sans-serif font family consistently across the figure.
- Use `26px` for all text inside the diagram unless the user explicitly requests a different size.
- Choose wording and box sizes so `26px` text remains readable without being compressed or clipped.
- Make title text and major section labels visibly larger than node text.
- Shorten wording before shrinking text to force content into a box.
- Resize boxes to fit text cleanly; do not let text sit cramped against borders.
- Keep terminology consistent across all nodes; do not mix synonyms for the same concept inside one figure.
- Prefer title case or a single consistent capitalization scheme instead of mixing styles.

## Final Quality Gate

Do not consider the figure complete until all of these are true:

- Both `.drawio` and `PNG` outputs exist and match each other.
- The exported `PNG` is sharp, unclipped, and ready for direct paper insertion.
- All in-diagram text uses `26px` unless the user explicitly approved another size.
- Main labels are readable at normal page zoom without manual zooming.
- Connector routing is clean enough that the reading order is obvious.
- Any connector that needs turns uses orthogonal anchor-plus-waypoint routing with explicit bend points.
- There are no avoidable line crossings, cramped boxes, or text collisions.
- Colors remain distinguishable in grayscale or low-saturation print conditions.
- The figure type is visually appropriate for structure, progression, or process rather than a hybrid mess.
