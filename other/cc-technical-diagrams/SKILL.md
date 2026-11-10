---
name: cc-technical-diagrams
description: Use when creating or exporting structured technical diagrams, including architecture, workflows, sequence diagrams, data flows, lifecycle diagrams, agent or memory flows, local interactive previews, and PNG quality checks. Use editable draw.io sources when long-term manual editing or vendor shapes matter. Do not use for UI mockups, product imagery, posters, or raster image editing.
---

# Technical diagrams

Create complete, readable technical diagrams from editable structured sources. This workflow applies across frontend, backend, infrastructure, and agent systems.

## Choose the source

Read [diagram workflows](references/diagram-workflows.md). Prefer locally available Mermaid for standard sequence and flowcharts. Use HTML technical diagrams for self-contained browser viewing, semantic architecture and agent/memory flows; read [HTML technical diagrams](references/html-technical-diagrams.md). Choose editable draw.io sources for official vendor shapes or long-term manual editing.

Use a local interactive preview when the user benefits from incremental explanation; keep JSON/SVG/PNG exports as deliverables. The live server is [interactive-diagram-server.mjs](scripts/interactive-diagram-server.mjs) and the local page is [interactive-diagram.html](assets/interactive-diagram.html).

## Render and export

Keep every node, relationship, complete label and explicit geometry. The renderer supports workflow, sequence, dataflow, lifecycle and architecture. Never silently simplify advanced sequence semantics; prefer Mermaid for activation and alt/loop/par fragments.

```sh
node skills/cc-technical-diagrams/scripts/tech-diagram-render.mjs --input diagram.json --type architecture --output diagram.html --manifest diagram.layout.json
node skills/cc-technical-diagrams/scripts/export-diagram.mjs --input diagram.html --format png --output diagram.png --theme light --scale 2 --manifest diagram.layout.json --output-manifest diagram.actual.json
node skills/cc-technical-diagrams/scripts/png-qa.mjs --png diagram.png --manifest diagram.actual.json --format json
```

Standard Mermaid sources use [mermaid-render.mjs](scripts/mermaid-render.mjs). Reuse [diagram-layout.mjs](scripts/diagram-layout.mjs) and [diagram-browser.mjs](scripts/diagram-browser.mjs); do not invent another renderer or add required browser libraries, remote scripts or downloaded icon packs.

## Verify and deliver

Inspect the actual exported image for clipping, text truncation, crossing labels, overlaps and missing content. PNG QA uses the actual scaled export manifest, not the source's estimated coordinates. Successful export alone does not prove visual acceptance. Read [PNG repair guidance](references/png-qa-autofix.md); repair the source or layout, not the output pixels. Default to at most two repair rounds and report unresolved issues.

Deliver JSON/Mermaid source, HTML where relevant, exports and QA evidence. Record tool versions, theme, scale, repair rounds and partial acceptance. Optional Mermaid/Graphviz/browser tools must fail clearly or use an available fallback; do not install them automatically or claim a missing export succeeded. Retain complete labels instead of hiding overflow at higher resolution.

Examples and fixtures: [quality examples](assets/quality-examples/README.md), [sequence JSON](assets/quality-examples/sequence.json), [workflow JSON](assets/quality-examples/workflow.json), [architecture JSON](assets/quality-examples/architecture.json), [invalid explicit geometry](assets/quality-examples/invalid-explicit.json).
