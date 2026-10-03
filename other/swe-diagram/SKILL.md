---
name: swe-diagram
description: Draw an interactive system architecture or Git-history diagram for a repo. Architecture maps start from existing rendered knowledge (graphify, codebase-memory, RAG, architecture docs) before raw code. Git-history maps render commits, branch cuts, and merges as stacked lanes from local refs. Produces a JSON spec and self-contained dependency-free HTML with pan/zoom, draggable nodes, typed edges, search, and filtering. Trigger for "draw the system diagram", "diagram this repo/architecture", "visualize the architecture", "Git commit graph", "visualize branches/merges", "git lanes", "swe-diagram", or xyflow-style repo maps. Not for data charts/dashboards or a single-algorithm flowchart.
---

# swe-diagram — Interactive Architecture and Git-History Maps

The skill interface lives here; its implementation assets are bundled under
[`utils/swe-diagram/`](https://github.com/HiQS-Labs/XYZ-forge/blob/development/utils/swe-diagram).

Produce two deliverables for the target repo:

1. `ARCHITECTURE/system-diagram.json` — the diagram spec (schema below)
2. `ARCHITECTURE/system-diagram.html` — a self-contained interactive xyflow-style
   diagram built from that JSON (no network, no dependencies)

Ask the user for a different output path only if `ARCHITECTURE/` is inappropriate
for the repo; otherwise just create it.

For a **Git-history request**, produce `ARCHITECTURE/git-history-diagram.json`
and `.html` instead, skip Steps 1–2's architecture discovery, and run:

```bash
node "<this-skill-dir>/../../utils/swe-diagram/scripts/git-history-to-json.js" \
  --repo "<target-repo>" --limit 20 \
  --output ARCHITECTURE/git-history-diagram.json
bash "<this-skill-dir>/../../utils/swe-diagram/assets/build-diagram.sh" \
  ARCHITECTURE/git-history-diagram.json
```

The generator uses local Git only. Its total limit spans every reachable local
and remote-tracking ref, orders `main`, `development`, then active feature/fix
lanes, and retains empty long-lived lanes when their refs exist. It cannot
recover deleted branch names or squash/rebase provenance; say so rather than
inventing lanes. GitHub PR enrichment is a separate, networked follow-up.

## Step 1 — Gather architecture knowledge (in this order, STOP when sufficient)

Do NOT start by grepping source code. The repo has usually already paid the
cost of describing itself — use that first. Work down this ladder and stop as
soon as you can name the major components and the edges between them:

1. **graphify output** — if `graphify-out/` exists (or the graphify skill is
   available), query it: god nodes, communities, and cross-file relationships
   map directly onto diagram nodes/edges.
2. **codebase-memory MCP graph** — if the `codebase-memory-mcp` tools are
   available, call `get_architecture` (aspects: structure, services,
   entrypoints), then `search_graph` / `trace_path` to confirm the edges
   between major components. If the repo isn't indexed, note it but don't
   index just for this — move to the next rung.
3. **ask_self RAG docs** — if the repo has an ask-self install (`/ask_self`
   skill, `Ask_Self/` or `.ask_self/` directory), query it with questions like
   "what are the major components and how do they talk to each other?" and
   "what external services/databases does this system depend on?"
4. **Written architecture docs** — `ARCHITECTURE.md`, `docs/`, `adr/` or
   `docs/adr/`, `AGENTS.md`/`CLAUDE.md`, README architecture sections,
   existing mermaid/diagram blocks. These often name components more
   accurately than code inspection.
5. **Last resort: the code itself** — only if the above yield too little.
   Read entrypoints, routing/config files, docker-compose/infra manifests,
   and top-level directory structure. Prefer targeted reads over broad greps.

Record which sources you used — they go in the JSON's `sources` field so the
diagram is auditable.

## Step 2 — Write the diagram JSON

Target 8-25 nodes: major components, not every file. Collapse helpers into
their owning service. Every edge must be justified by something you found in
Step 1 (a doc claim, a graph edge, an import/call you saw) — no decorative
arrows.

Schema (`ARCHITECTURE/system-diagram.json`):

```json
{
  "title": "MyApp — System Architecture",
  "generated": "2026-07-04",
  "sources": ["codebase-memory get_architecture", "docs/ARCHITECTURE.md"],
  "groups": [{ "id": "backend", "label": "Backend" }],
  "nodes": [
    {
      "id": "api",
      "label": "REST API",
      "type": "api",
      "group": "backend",
      "tech": "FastAPI",
      "description": "Public HTTP surface; auth + routing"
    }
  ],
  "edges": [
    { "source": "api", "target": "db", "label": "reads/writes", "kind": "sync" }
  ]
}
```

- `type` (drives node color + legend): `service`, `ui`, `api`, `database`,
  `queue`, `external`, `job`, `storage`, `commit`, `merge` — anything else
  falls back to gray.
- `kind` (drives edge style): `sync` (solid), `async` (dashed), `data`
  (dotted), `branch` (short dash), `merge` (purple long dash). Default `sync`.
- Layout is automatic; do not put coordinates in the JSON. Five layouts:
  - **`"layout": "layered"` (default, omit the field for this)** — left→right
    from edge direction. Point `source → target` in the direction of the
    call/flow — layout quality depends on it. Use for synchronous
    request/response pipelines and strict call chains (`UI → API → DB`).
  - **`"layout": "top-down"`** — top→bottom from edge direction, using the
    same deterministic longest-path ranks as `layered`. Use for deployment
    stacks, CI/CD stages, request lifecycles, or diagrams that must fit a
    narrower page. Point `source → target` in the direction of the call/flow.
  - **`"layout": "hub-ring"`** — radial: one hub node at the center, every
    other node placed on a ring around it (overflow beyond ~8 nodes spills to
    a wider concentric ring). Use for event-driven architectures where a
    central broker or gateway (Kafka, RabbitMQ, an API Gateway) talks to
    otherwise-independent services, not a linear pipeline. Optionally set
    `"hub": "<node id>"` to force which node is the center; omit it and the
    renderer picks the highest-degree (most-connected) node.
  - **`"layout": "trust-clustered"`** — bands nodes into five fixed
    trust-tier columns derived from each node's own `trust` field (see the
    vocabulary below), not from graph rank or an author-chosen `group`:
    Orchestration Spine, Turn-Shim Cluster, Untrusted Periphery, Shared
    State, and Off-Live-Path Governance & Audit. Use when trust/control-plane
    structure — not call direction — is the thing the diagram needs to make
    dominant, e.g. a containment core that must always read as a hub, never
    a leaf, regardless of how many things dispatch to it. Every node needs a
    `trust` value for this mode to place it meaningfully; an untagged node
    falls into the governance band rather than vanishing. A tier's members
    wrap into side-by-side sub-columns past 6 nodes so one tier can't dominate
    the canvas. The node whose `trust` is exactly (or starts with)
    `trusted-containment-core` is drawn with an emphasized border so it reads
    as the diagram's hub at a glance.
  - **`"layout": "git-lanes"`** — fixed horizontal branch lanes stacked as
    `lanes[].order`, with commits advancing left→right by each node's numeric
    `order`. Nodes set `lane`; edges point parent→child. Use the bundled
    generator rather than hand-authoring Git ancestry. First-parent edges are
    solid within a lane, branch cuts are dashed teal, and merge-parent edges
    are dashed purple.
  - `groups` swimlanes are supported by **`layered` and `top-down`** (their
    boxes follow contiguous rank columns or rows). They render as background
    bounding boxes containing their child nodes, labeled top-left with the
    group's `label`, and are silently skipped under `hub-ring` and
    `git-lanes`. A node opts into a group via its own `group` field, matched
    against a `groups[].id`; groups with no member nodes are skipped.
    **`trust-clustered` draws its own bands instead** — derived from each
    node's `trust` field rather than `spec.groups`/`node.group` — so
    `spec.groups` is ignored under this mode.

## Step 3 — Build the HTML

Run the bundled builder (resolve the path relative to THIS skill directory,
not the CWD):

```bash
bash "<this-skill-dir>/../../utils/swe-diagram/assets/build-diagram.sh" ARCHITECTURE/system-diagram.json
```

It inlines `../../utils/swe-diagram/assets/renderer.js` and the JSON into
`../../utils/swe-diagram/assets/template.html`,
producing `ARCHITECTURE/system-diagram.html`. If `bash`/`python3` is unavailable,
do the substitution yourself: copy the template and replace `__TITLE__`,
`__RENDERER_JS__` (contents of renderer.js), and `__DIAGRAM_JSON__` (the spec).

The output is a single file: open it in any browser. It supports pan (drag
background), zoom (wheel or +/− buttons), fit-to-view (▣), draggable nodes,
hover tooltips from `description`, edge labels, group swimlanes, a type
legend, and follows the OS light/dark theme. A top-right search box filters
by label/id/type/tech/description (case-insensitive substring); clicking a
legend type toggles it. Non-matching nodes and edges are **dimmed, not
hidden** — no re-layout, nothing disappears, easy to reset.

## Step 4 — Verify and report

1. Sanity-check the JSON: every edge's `source`/`target` matches a node `id`
   (the builder fails on invalid JSON but not on dangling edge references —
   the renderer silently drops those, so check).
2. Open or screenshot the HTML if the environment allows; otherwise state that
   it wasn't visually verified.
3. Report both file paths, the node/edge counts, which knowledge sources were
   used, and anything you were unsure about (components you inferred rather
   than found documented).
