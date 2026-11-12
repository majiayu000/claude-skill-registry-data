---
name: ak-diagram
description: "Compile typed JSON IR into validated interactive maps and HTML readers of architecture, workflows, sequences, dataflow or lifecycles."
when_to_use: "Invoke for grounded graph queries; whiteboards use ak-excalidraw, static charts ak-tech-graph, inline markdown ak-mermaidjs-v11."
category: engineering
keywords: [diagram, archify, architecture, workflow, sequence, dataflow, lifecycle, interactive-map, system-map, visual-map, reader-runtime]
argument-hint: "[input-file] [--format <svg|fragment|html>] [--preset <classic|signal-flow|blueprint|editorial>] [--theme <light|dark>] [--out <path>]"
license: Proprietary; includes MIT- and ISC-licensed third-party material, see LICENSE.txt
metadata:
  author: agentkit
  version: "3.0.0"
  upstream_templates: cathrynlavery/diagram-design (MIT)
  design_reference: tt-a1i/archify (MIT; IR archetypes, presets and reader concepts only, no code vendored)
  vendored_pele_version: "1.6.0"
  mermaid_fallback_version: "11.4.1"
---

# ak-diagram - Unified System Map & Interactive Diagram Surface

Compile typed JSON IR specifications into deterministic SVGs, embeddable fragments, and self-contained interactive HTML readers without browser dependencies. The compiler owns layout: it ranks the graph, orders columns to reduce crossings, routes orthogonal edges around unrelated nodes, and renders role-aware cards with a legend, so authors describe topology and never coordinates.

## Archetype Decision Matrix

| User Intent | Archetype | Primary Entities | Key Fields |
|---|---|---|---|
| System topology, microservices, boundaries | `architecture` | `components`, `boundaries`, `connections` | `role`, `layer` (0–10), `kind` |
| Multi-step execution, lane handoffs, decisions | `workflow` | `lanes`, `steps`, `transitions` | `kind`, `lane`, `condition` |
| Ordered API calls, request/response timing | `sequence` | `participants`, `messages` | `kind: sync-call \| return` |
| ETL pipelines, stream processing, data lineage | `dataflow` | `stages`, `nodes`, `flows` | `stage`, `role`, `classification` |
| Finite state machines, status transitions | `lifecycle` | `states`, `transitions`, `lanes` | `kind: initial \| active \| ...` |

## 5-Step Execution Playbook

1. **Select Archetype**: Match user intent to one of the 5 archetypes above.
2. **Author Typed JSON IR**:
   - Set envelope: `{"schema_version": 1, "diagram_type": "<type>", "meta": {...}}`.
   - Set visual preset: `classic` (clean slate), `signal-flow` (emerald/cyan glow), `blueprint` (technical dark blue), or `editorial` (warm serif).
   - Set theme: `light` or `dark`. Every diagram plays a finite staggered entrance (nodes fade in by column, edges draw themselves). Set `animation: "trace"` to add one finite flow pass along every route after the entrance.
   - Optional guided story: add `meta.views: [{"id": "ch1", "title": "...", "narrative": "...", "focus_nodes": [...]}]` (max 5 chapters).
3. **Apply Schema Invariants**:
   - Use strict role enums on nodes (compiler validates node roles at compile time).
   - Keep IDs alphanumeric + hyphens (`^[a-zA-Z0-9_-]{1,64}$`).
   - Placement follows the IR: `layer` picks the architecture column, `lane` picks the workflow row, `stage.order` picks the dataflow column, `initial` states open a lifecycle. Unranked nodes take the longest path from their predecessors; cycles are drawn as return routes.
4. **Compile Offline (Zero Browser)**:
   ```bash
   node scripts/compiler/compile.mjs --input diagram.json --format html --out ./build/diagram.html --preset signal-flow --theme dark
   node scripts/compiler/compile.mjs --input diagram.json --format svg --out ./build/diagram.svg --preset signal-flow --theme dark
   ```
5. **Deliver & Embed**: Deliver the self-contained `.html` (interactive reader with keyboard shortcuts) or clean vector `.svg`.

## Schema Cheat Sheet & Valid Enums

Load `references/schema-and-reader.md` only for this part of the task.

## Layout & Motion Contract

- Layout is deterministic: identical IR yields identical geometry. Nodes never overlap, routes never cross an unrelated node, boundaries, lanes and stages fully contain their members (`scripts/test_layout_geometry.mjs` enforces this on every fixture).
- Each node role maps to a visual family (client, service, data, queue, cache, gateway, security, external, worker, start, success, failure, waiting, decision, process, governance, transform, filter) with its own colour token, sigil and legend entry; families are exposed as `data-family` on `.ak-node`.
- Motion is CSS only. Nodes and edges carry `data-animate` and a `--step` index (capped at 40) so the whole entrance finishes in under 8 s; `prefers-reduced-motion: reduce` renders the final frame directly. The reader's Replay button (`M`) re-arms the sequence.
- Compiler modules live under `scripts/compiler/`: validation, layered graph ranking and ordering, per-archetype layout, orthogonal routing, semantics and palettes, and the SVG emitter. The emitted `.ak-node` / `.ak-edge` attribute order is a consumer contract for the reader.

## Common Commands

```bash
# Compile typed IR to standalone interactive HTML reader
node scripts/compiler/compile.mjs --input diagram.json --format html --out ./build/diagram.html

# Compile typed IR to clean vector SVG
node scripts/compiler/compile.mjs --input diagram.json --format svg --out ./build/diagram.svg

# Compile to embeddable scoped HTML fragment
node scripts/compiler/compile.mjs --input diagram.json --format fragment --preset signal-flow --theme dark

# Legacy Python wrapper (auto-detects typed IR vs Mermaid vs legacy template)
python3 scripts/render.py --input diagram.json --out ./build/
```

## AK Render Page Embedding

Skills that compile an HTML page with AK Render (`@bestagentkits/render`) embed
diagrams through `scripts/render-page.mjs`. Put the typed IR in a
`diagram-panel` block's `spec`, then compile the whole page:

```bash
npx -y -p @bestagentkits/render@0.3.0 node <ak-diagram-dir>/scripts/render-page.mjs page.page.yaml --out page.html --json
```

The wrapper plugs this compiler into AK Render as its diagram adapter, refuses
any render version other than the pin; AK Render itself grants the page's CSP
nonce to the diagram styles. Exit 1 means an invalid spec, as with the AK Render CLI; exit 2
covers IO, environment and internal failures (the CLI reports internal failures
as a stack trace). It finds project theme presets from the spec's
folder upward and prints preset problems as warnings. Its JSON summary lists
`diagramErrors` and `themeProblems`; each failed panel keeps
AK Render's structured fallback, so repair the IR and recompile.

## Security & Boundaries

- **Zero Network**: `scripts/compiler/compile.mjs` compiles offline in pure Node.js; no remote calls, telemetry, or font downloads. `.mmd` input also renders offline through the vendored Pele bundle. Two exceptions: the AK Render page wrapper's first `npx` run downloads the pinned package from npm (cached afterwards), and a `.mmd` diagram Pele rejects falls back to a page that loads Mermaid 11.4.1 from jsDelivr (SRI-pinned; see `references/mermaid-input.md`). Compiled typed-IR pages make zero network requests.
- **Deterministic**: Compiling identical IR bytes emits identical SHA-256 output bytes across environments.
- **Finite Motion**: Entrance and trace animations are finite (under 8 s in total), replayable, and automatically disabled under `prefers-reduced-motion: reduce`.
- **Scope Limit**: For freeform whiteboard sketching, use `ak-excalidraw`. For static print infographics, use `ak-tech-graph`. For raw markdown inline doc blocks, use `ak-mermaidjs-v11`.
