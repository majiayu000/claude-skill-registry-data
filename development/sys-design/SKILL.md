---
name: sys-design
description: Generate the standard 4-page architecture graph suite (graph-<app_name>/index.html, file-architecture.html, system-design.html, flow-graph.html) for a codebase, in the fixed enterprise network-topology style. Use when the user asks for architecture graphs, system design diagrams, file architecture trees, or flow graphs of a project. Annotates components with evidence-based trade-offs, failure modes, scaling ceilings, and cloud managed-service equivalents (§ANALYSIS / §PROVIDER MAP). Always produces the same design, structure, and file order.
---

# sys-design — Deterministic Architecture Graph Suite

Generate exactly four HTML files in a `graph-<app_name>/` folder at the target
project root, where `<app_name>` is the exact name of the project root folder
(e.g. project `spotify-app` → folder `graph-spotify-app/`). Always name the
output folder this way — never plain `graphs/`.
The output design, structure, and order are FROZEN — every invocation must look
the same. The single source of truth is `spec.md` in this skill's folder:
read it FIRST and follow it to the letter. Never improvise styling.

## Procedure (always in this order)

1. **Resolve target(s).**
   - If the user passed a path (or several) as arguments, use those project roots.
   - Otherwise use the current working directory's project root.
   - If multiple targets: launch one general-purpose agent per project IN PARALLEL
     (one Agent tool call block), each agent given the full procedure below and
     the absolute path to this skill's `spec.md`.

2. **Read the spec.** Read `spec.md` located in the same directory as this
   SKILL.md. It defines: the diagram style (nodes, edges, zones, layout), the
   exact content of each of the four files, the frozen color/typography tokens,
   the determinism rules, and the required final summary format.

3. **Analyze the codebase thoroughly — before generating anything.**
   Read every source file, config, manifest, README, docker-compose,
   .env.example, and documentation. Skip dependency/build/IDE folders
   (.venv, node_modules, bin, obj, Debug, Release, x64, .vs, .idea, .git,
   __pycache__) except to mark top-level generated artifacts. Accuracy is
   mandatory: every label, path, function name, port, and protocol in the
   output must come from the actual codebase. Where something cannot be
   determined, write *[unresolved]* in italics — never invent values.
   As you analyze, build the §ANALYSIS record for each application/data-tier
   component, broker, cache, and external dependency (role, what it worsens,
   failure mode under stress, scaling ceiling) — every field backed by
   concrete code evidence or omitted. Map detected self-hosted tech to cloud
   managed-service equivalents via §PROVIDER MAP, but only for clouds actually
   detected in the codebase.

4. **Get the timestamp once**: PowerShell `Get-Date -Format "yyyy-MM-ddTHH:mm:ssK"`
   (or `date -u +%Y-%m-%dT%H:%M:%S%z` on POSIX). Embed the SAME value in all
   four pages.

5. **Generate the four files — always in this exact order** (folder name is
   `graph-<app_name>`, where `<app_name>` is the project root folder's name):
   1. `graph-<app_name>/index.html` — Project Overview Hub
   2. `graph-<app_name>/file-architecture.html` — File System Architecture tree
   3. `graph-<app_name>/system-design.html` — System Architecture (zoned topology)
   4. `graph-<app_name>/flow-graph.html` — Application Flow Diagrams (5 flows, tabbed)
   Each file's required content, interactions, and layout are defined in
   spec.md FILE 0–FILE 3 sections. Hand-crafted SVG only — no Mermaid,
   no vis.js, no frameworks, no build tools.

6. **Honesty rules for non-networked apps** (desktop/CLI/library): never invent
   network ports or services. Use real mechanisms as edge labels: "in-proc call",
   ".NET event", "Tk callback", "File I/O (JSON)", "GDI+ paint", "generator yield".
   Zones still apply — map them per the Desktop/CLI zone table in spec.md.
   For empty or scaffold-only projects, document the scaffold honestly with
   *[unresolved]* runtime nodes; do not fabricate an application.

7. **Verify before reporting.** Confirm all four files exist, are well-formed
   (end with `</html>`), share the same timestamp, and the nav bar on each page
   links to all four pages with the active page underlined.

8. **Output the FINAL SUMMARY** exactly in the format defined at the end of
   spec.md: FILES GENERATED table (filename | size | node count | edge count),
   five ARCHITECTURAL FINDINGS in the §ANALYSIS frame (what the architecture
   solves / worsens / its breaking point), a CAPACITY & SCALE NOTES section
   drawn only from detected config, and UNRESOLVED ITEMS with reasons.

## Hard determinism rules (never deviate)

- Same four filenames, same generation order, same nav-link order:
  Overview | File Architecture | System Design | Flow Graph.
- Fonts: IBM Plex Sans + IBM Plex Mono via Google Fonts CDN. Nothing else.
- Color tokens, node geometry, zone names/order, file-type tag palette, and
  flow-priority order are frozen in spec.md §TOKENS and §DETERMINISM.
- Flows always in priority order: startup/initialization, authentication,
  primary write path, primary read path, error/recovery — substituting the
  next most significant flow only when one is absent.
- All connectors orthogonal (H/V only). No diagonals, no shadows, no gradients.
- Layout is ALWAYS computed by ELK.js in the browser with the frozen config
  in spec.md §LAYOUT ENGINE. Never hand-place x/y coordinates, never draw
  center-to-center elbow paths — render exactly the bend points ELK returns.
  Node sizes are text-first (canvas measureText → width), labels live INSIDE
  node rects, and edge labels are passed to ELK so it reserves space for them.
- Graphs live in scrollable containers with a 75/100/125/Fit zoom control —
  NO drag-pan canvas, NO custom wheel-zoom mouse math.
- Every page embeds its data as canonical JSON in
  `<script type="application/json" id="graph-data">` per spec.md
  §DATA CONTRACT — the renderer's single data source, and what external
  tools (the AppGraph hub) ingest. The DATA CONTRACT stays schema-tagged
  `sys-design/v2`; the v3 §ANALYSIS/§PROVIDER fields are optional and
  additive so existing ingest keeps working.
- §ANALYSIS annotations (trade-offs, failure modes, scaling ceilings) and
  §PROVIDER MAP equivalents are rule-derived and evidence-gated: every claim
  cites a concrete code artifact (or a stated absence) or is omitted — never
  invented — so the same codebase always yields the same annotations.
- ZERO collisions, guaranteed by the ELK config: arrows never cross text,
  titles, labels, or nodes; text never overlaps any element; all text fits
  inside its card with ≥8px padding. Verify on the rendered output before
  reporting completion.
