---
name: tekton
category: design
description: >
  Tekton — the shared architecture-intent substrate for co-designing systems with the
  agent. One typed graph across six tiers (system / journey / data / infra / decisions / qualities);
  views are queries, not separate diagrams. The canonical artifact is a diff-friendly
  YAML model both human and agent read and write; it renders to Mermaid (agent-legible,
  GitHub-native) and a self-contained tabbed HTML viewer (human-visual). Cross-tier
  traceability (`tekton query <from> <to>`) answers "which infra does this user-journey
  step touch?" as a path query. USE WHEN: designing or thinking deeply about architecture,
  a system, a data model, user journeys/flows, or a technical plan WITH the agent; when a
  Category-C HTML doc isn't enough because you need to see AND edit AND traverse the design
  across tiers; "let's design X", "architect this", "model the system", "draw the flow",
  "how does this fit together", "diagram this", "/tekton". NOT FOR: a one-off throwaway
  diagram (use Mermaid inline); prose-only ADRs (write the ADR); implementation itself.
  Triggers on: design architecture, model the system, user journey, data model, tekton.
license: MIT
metadata:
  version: "0.2.0"
  homepage: "https://broomva.tech/skills/tekton"
primitive: null
required: false
---

# Tekton — co-design architecture over one shared model

## What it is
A substrate for **human↔agent architecture partnership**. The design lives in one
YAML model both of us edit; git is the round-trip. You *see* it (HTML viewer); I *read
and write* the same model. We think over the same context.

The failure it fixes: a hand-authored HTML/SVG doc is a terminal render — you can't
traverse, query, or edit it back, and its diagrams carry no meaning. Tekton moves the
live model **upstream** of the render.

## Engine
`scripts/tekton.py` (Python 3, pyyaml). Ontology in `references/ontology.md`.

```bash
python3 scripts/tekton.py validate <model.arch.yaml>       # integrity check
python3 scripts/tekton.py lint     <model.arch.yaml>       # v0.2 — fitness functions; exit 1 on violation
python3 scripts/tekton.py stats    <model.arch.yaml>       # node/edge/status/rule counts
python3 scripts/tekton.py views                            # list the 6 views
python3 scripts/tekton.py mermaid  <model.arch.yaml> <view># raw mermaid (embed/agent)
python3 scripts/tekton.py render   <model.arch.yaml> [-o out.html]  # on-brand HTML viewer
python3 scripts/tekton.py query    <model.arch.yaml> <from> <to>    # cross-tier path
```

## v0.2 ontology upgrades (from the architecture review)
- **Containment** — `parent:` on any node + `boundary` type; viewer renders nested groups,
  double-click to collapse/expand (C4-style drill-down).
- **Lifecycle** — `status:` on nodes (`current|target|deprecated`; target renders dashed =
  as-is/to-be in one model) and full Nygard ADR fields on decisions (`context`,
  `consequences`, `status`, `supersedes`).
- **Qualities** — `qualities:` block; NFRs `constrains` elements; surfaced in detail panel
  + dedicated view.
- **Fitness functions** — `rules:` block (`forbid-dep`, `no-cycle`, `layer-order`);
  `tekton lint` is CI-gateable (exit 1). The design loop's independent verifier.

## How the agent uses it in a design session
1. **Locate/create** the model: `<project>/docs/design/<name>.arch.yaml` (or `examples/` for scratch).
2. **Mutate as we think** — add/adjust nodes, edges, decisions directly in the YAML as the
   conversation surfaces components, flows, data, infra, and ADRs.
3. **`validate` + `lint`** after each substantive edit (dangling refs, bad types, fitness rules).
4. **`render`**, then — BEFORE presenting the viewer as correct — run the geometry audit:
   `bash tests/visual-audit.sh <model.arch.yaml>`. It headless-renders every view and FAILS on
   node overlaps or empty captures. Claiming "the diagram is correct" without it is the exact
   failure the first dogfood caught (disconnected in-group edges, doubled nodes — invisible to
   DOM-count probes, caught only by geometry). Deep-link a view with `#<view>` in the URL.
5. **`query`** to answer traceability questions ("what does this touch?") instead of guessing.
6. **Steer → repeat.** The human edits the YAML or the viewer intent; git diff is the handoff.

Known cosmetic residuals (not audit failures): journey loop-back edges make ELK break the
cycle at an arbitrary step (a loop must break somewhere); adjacent parallel-edge labels can
sit close in dense groups.

## Conventions
- Model files: `*.arch.yaml`. Rendered viewer: `*.view.html` (gitignore or commit — your call).
- One model per bounded system; link systems with `external` nodes + `uses` edges.
- Decisions (ADRs) are first-class nodes — pin them to what they `govern`.
- Category-C HTML reports become a **downstream export** of a model, not the source of truth.

## Rendering — why not Mermaid
The primary viewer is a **custom renderer**, not Mermaid. Mermaid's theming ceiling can't
express the Broomva Design System (OKLCH blue-axis, matte cards, earned glass, comet-glow)
and its dagre layout degrades on dense graphs. Instead: `elkjs` computes the layout
in-browser (pure JS → the output stays a single self-contained HTML file), and nodes are
drawn as Broomva matte cards (glass reserved for the floating detail panel, per the DS's
"glass is earned" rule). Design tokens are inlined from the Broomva Design System.
`tekton mermaid` stays ONLY as a throwaway embed/agent-legible target.

## Roadmap (v0 → v2)
- **v0.2 (now):** YAML model · validate + lint (fitness functions) · 6 views · **on-brand
  elkjs viewer** (containment collapse/expand, as-is/to-be, click-to-trace, glass detail
  panel) · cross-tier query · Mermaid fallback embed.
- **v1:** two-way round-trip (drag/edit in the viewer → serialize back to YAML); MCP server
  (validated mutations so the agent can't emit an invalid model); vendor the full Broomva
  Design System for a React-Flow interactive canvas.
- **v2:** CRDT (loro) real-time human↔agent co-editing; live sync into Prosopon as a surface.

## Status
v0 dogfood — internal design tool. Skillify (tested + registered) once the design loop has
been used on ≥3 real systems (rule-of-three).
