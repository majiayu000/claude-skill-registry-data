---
name: cc-drawio-studio
description: Use when creating editable technical diagrams with draw.io / diagrams.net sources, including architecture diagrams, ERD, UML, sequence diagrams, flowcharts, ML model diagrams, official shape lookup, brand symbols, Graphviz auto-layout, codebase structure maps, .drawio validation, or draw.io CLI export fallback. Do not use for ordinary raster image generation, freehand sketches, interactive canvas/Three.js scenes, or decorative SVG animation. Chinese triggers include draw.io, diagrams.net, editable architecture diagrams, .drawio, ER diagrams, UML, sequence diagrams, auto layout, shape retrieval, code structure diagrams.
---

# Editable technical chart workflow

## Purpose

Generate, verify and export draw.io / diagrams.net technical diagrams that can be edited further.

## Procedure

1. Determine the chart route
   - Simple diagrams in Markdown that need long-term maintenance, Mermaid is preferred.
   - Use this workflow when you need official icons, swimlanes, complex layouts, layers/tags/metadata, editable PNG/SVG/PDF or `.drawio` sources.
   - When you need fast browser opening or sharing, use [diagram-url.mjs](scripts/diagram-url.mjs) to generate the URL; when you need local auditable delivery, always save the `.drawio` source.
   - If the user already has Mermaid or CSV content, they can use `diagram-url.mjs --create --type mermaid|csv` to import it to diagrams.net; when long-term maintenance or precise shape is required, convert it to XML.
   - If the draw.io MCP App/Tool has been configured on the current host, it can be used as a preview or editing entrance; this skill does not require the installation of MCP server.
   - Go the image generation route when you need photos, posters, visual concepts or bitmap editing.

2. Create chart specifications
   - Clarify diagram type, audience, output format, node list, relationships, hierarchical grouping and save location.
   - Read [diagram-patterns.md](references/diagram-patterns.md) when the user specifies Flowchart, Architecture, Sequence, UML Class, ERD, Mindmap, Network Topology or ML/DL diagrams.
   - For process, workflow, approval, release or incident-response flowcharts that must open cleanly in diagrams.net, also read [flowchart-quality.md](references/flowchart-quality.md).
   - To select XML, Mermaid, CSV, container, layer, tag, metadata or dark mode policy, read [xml-and-mermaid.md](references/xml-and-mermaid.md).
   - When you need a specific vendor/cloud/network/flowchart shape, run [shape-query.mjs](scripts/shape-query.mjs); when you need AI, database or infrastructure brand symbols, run [brand-symbols.mjs](scripts/brand-symbols.mjs).

3. Generate `.drawio` source
   - Draw.io XML can be manually generated for small drawings when exact node coordinates, sizes and connections are easier to reason about directly.
   - When there are more than about 15 nodes, dependency graphs or code structure graphs, first generate graph JSON and then use [layout-graph.mjs](scripts/layout-graph.mjs) for automatic layout.
   - For manually placed XML, align coordinates to a 10px grid, keep generous gaps between sibling nodes, use `whiteSpace=wrap;html=1`, prefer `fontSize=14`, encode forced line breaks as `&#xa;`, and size containers to their content instead of leaving one-sided blank areas.
   - For manually authored flowcharts, keep `pageWidth` in the readable 600-800 range unless a wide cross-functional table is intentional; use swimlane containers for real stages and route loop or rollback edges around the margin with explicit waypoints.
   - Code structure diagram can be used first [scan-js-modules.mjs](scripts/scan-js-modules.mjs), [scan-ts-modules.mjs](scripts/scan-ts-modules.mjs), [scan-python-modules.mjs](scripts/scan-python-modules.mjs), [scan-go-packages.mjs](scripts/scan-go-packages.mjs), [scan-rust-modules.mjs](scripts/scan-rust-modules.mjs) or [scan-python-classes.mjs](scripts/scan-python-classes.mjs) to generate graph JSON.

4. Checksum preview
   - Run after each generation of `.drawio`:
     ```bash
     node skills/cc-drawio-studio/scripts/diagram-lint.mjs diagram.drawio --format markdown
     ```
   - If the machine has draw.io desktop CLI, do not embed XML when exporting the preview PNG, and control the width:
     ```bash
     node skills/cc-drawio-studio/scripts/drawio-export.mjs diagram.drawio --format png --output diagram.png --width 2000
     ```
   - If CLI is not available, use [diagram-url.mjs](scripts/diagram-url.mjs) to generate diagrams.net viewer/editor URL; first read [data-residency.md](references/data-residency.md) when strictly offline or data residency is sensitive.

5. Deliver the final product
   - Save `.drawio` source files and PNG/SVG/PDF/JPG required by users.
   - If the final PNG is embedded in XML using draw.io `-e`, run after exporting:
     ```bash
     node skills/cc-drawio-studio/scripts/drawio-export.mjs diagram.drawio --format png --output diagram.drawio.png --scale 2 --embed
     node skills/cc-drawio-studio/scripts/png-embed-fix.mjs diagram.drawio.png
     ```
   - Report source files, exported files, verification results, and external dependencies that cannot be automatically verified.

## Tool Resources

Tool script sharing [studio-core.mjs](scripts/studio-core.mjs). Offline query uses [shape-index.json](data/shape-index.json) and [brand-icons.json](data/brand-icons.json). Style preset resources include [schema.json](styles/schema.json), [default.json](styles/built-in/default.json), [corporate.json](styles/built-in/corporate.json) and [handdrawn.json](styles/built-in/handdrawn.json).

## Constraints

- Do not use draw.io as a normal image model; text-heavy or structured images must remain editable source.
- Don't guess complex `shape=mxgraph.*` styles; use the shape query tool to get the official styles first.
- The MCP server runtime dependency is not introduced for the draw.io workflow; MCP App/Tool is only used as an optional interoperability entry when the user environment already exists.
- Mermaid/CSV URLs are import shortcuts and do not replace `.drawio` source files, lint and editable delivery.
- Do not embed XML in preview PNGs; embedding is for final delivery only.
- Graphviz, draw.io desktop, and networked branding icons are all optional external capabilities; they must be downgraded instead of retried when missing. `drawio-export.mjs` may detect local draw.io paths and print installation guidance, but it must not install draw.io automatically.
- Brand icons and third-party shape indexes follow the source and licensing instructions in [THIRD_PARTY_NOTICES.md](data/THIRD_PARTY_NOTICES.md).
- When referring to the external draw.io MCP ecosystem, only absorb routes, constraints and interoperability experience, and do not copy its service implementation or long prompts.

## Expected Output

Deliver editable `.drawio` source and required export format, with structural verification results. The diagram should have complete nodes, traceable connections, non-truncated labels, non-overlapping layouts, and a diagrams.net fallback that can be opened when external tools are missing.
