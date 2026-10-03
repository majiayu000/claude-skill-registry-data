---
name: forge-mindmap
description: Generates a mind map (nodes+edges) to visualize a plan or architecture. Use when a plan has enough branching that a graph reads clearer than prose — mind map, visualize the plan.
---

# Forge Mind Map (WP4)

A **Forge mind map** is a small node/edge graph — a root idea with branches and leaves — that the Lead generates to visualize a plan, an architecture, or a mission decomposition. It is built and stored by `.claude/forge-bin/forge-mindmap.cjs`, a zero-dependency writer that stores the structured JSON (and optional Mermaid/markdown sidecars) under `.claude/forge-mindmaps/`.

## When the Lead generates one
- To visualize a **plan, architecture, or mission decomposition** once it has real branching structure (a root idea with several sub-areas) — not for a flat 2-3 item list where prose is clearer.
- Typically right after a **Master Plan** or **Deep Learn Mode** pass, so the map reflects real decisions already made, not a guess.
- Not needed for a trivial, single-path task.

## How
1. Write the structure as an indented plain-text outline (2-space or tab indent = depth; the first line is the root):
   ```
   Mission Control Phase 2
     WP4 Mind Map
       Writer (forge-mindmap.cjs)
       Radial lens (dashboard)
     WP5 Next Work Package
   ```
2. Build + store it:
   ```
   node .claude/forge-bin/forge-mindmap.cjs from-outline '<outline-text>' <map_id> --write --run <run_id> --mermaid
   ```
   - Omit `--write` to preview the parsed `{nodes, edges}` JSON without persisting anything.
   - `--mermaid` also writes a `<map_id>.mmd` Mermaid sidecar (`graph TD`, guarded — never crashes on odd input).
   - `--run <run_id>` logs `mindmap_generated` to that run's dashboard events — only fires once the map was actually written.
   - Already have a built `{map_id, title?, nodes, edges}` object instead of an outline? Use `write` directly: `node .claude/forge-bin/forge-mindmap.cjs write '<map-json>' --write --run <run_id>`.

## What it produces
`.claude/forge-mindmaps/<map_id>.json` (the stored `{map_id, title, nodes, edges, _generated}`), optionally `<map_id>.mmd` (Mermaid) and `<map_id>.md` (nested outline), and an appended row in `.claude/forge-mindmaps/index.jsonl`. The dashboard's **MIND MAP** lens reads the latest stored map read-only and renders it as a root-centered radial graph (root at the center, branches/leaves on rings by depth, no node overlap).

## Honesty rule (non-negotiable)
- **Real structure only.** Every node reflects an actual part of the plan/architecture the Lead decided on — no filler branches, no invented depth just to make the map look bigger.
- **Secrets are auto-redacted.** Every string in the map is redacted (`forge-store.cjs`'s `redactValue`) before it is written to disk — never write a raw secret into a mind map.
- **The MIND MAP lens is read-only.** There is no write endpoint on the dashboard for mind maps; the only way to create or change one is `forge-mindmap.cjs write`/`from-outline`. With no stored map yet, the lens shows an honest empty state — it never fabricates nodes.
