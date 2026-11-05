---
name: uefn-pcg
description: Scatters props, trees and rocks over an area of a UEFN map with a PCG graph made through the MCP, instead of placing each one by hand. Use when the owner asks for a forest, a field of rocks, many props, scenery, scatter, procedural placement, or a map area that would take hours to dress by hand.
kind: discipline
last_reviewed: 2026-11-04
sources: [UEFN 43.00 PCG tools and Epic's PCG skills read in the editor, a pilot run in the lab]
---

# Dressing an area with PCG

PCG makes points inside a shape, filters them, gives each point a mesh and spawns the meshes. Through the MCP you build that as a **graph asset**, then put a **graph instance** (a PCG volume) in the level and execute it. The results are instances owned by the volume: they are not separate actors, they go away when the volume goes away. This was run once in the lab (a 20 m square, about 16 meshes) and worked; the placement lesson below cost a cleanup.

Epic serves its own PCG skills through the MCP (see `uefn-epic-skills`): read `Skill_PCGGraphGeneration` for the node rules before building. This skill is the kit's part: the order, the traps found, what to ask the owner.

## When to use
- A forest, a rock field, scattered props, grass, litter: many copies of a few meshes over an area.
- The same scenery in several places.

**When not to use:** a few hand-placed key props (use `uefn-level-devices` and the placement steps of the plan), devices and gameplay objects, anything the player interacts with.

## Workflow
1. Ask or decide: the area (size, where), what (mesh kinds), how dense, how many kinds. Keep the first run small (about 20 points) so a mistake is cheap.
2. Find the meshes: `FindAssets` with the nested filter and `assetType` StaticMesh plus a folder or a name. The farm's `PlaysetProps` are item definitions, not meshes: a search for static meshes there finds none; use the mesh the definition points to, or the engine's `/PCG/DebugObjects` for a test.
3. Make the graph in a scratch folder (`KitTest`): create the graph, add the primitive subgraph nodes, connect them, read the structure back. The simple chain that worked: shape (a square), random scatter, assign assets, filter overlaps, spawn. Copy Epic's example graph for a shape rather than inventing the nodes.
4. Put the instance **where the shape is**: the primitive that builds the square puts it at the **world origin** and ignores the volume's position. Set the shape's own position or transform under the volume (or place the volume at the origin of an empty test area) before executing. Read the bounds first.
5. Execute, then read back: the volume's bounds and the actor count before and after (the generated meshes are not actors). Take a viewport capture to see it; do not trust a count alone.
6. Show the owner the result and keep or remove: removing the volume removes what it generated; the graph asset stays for the next run.

## Rules (symptom, cause, remedy)
- Meshes appear on the farm, not on the test area: the shape was built at the origin (step 4). Remove the volume (it takes its meshes with it) and set the shape position.
- `FindActors` refuses the volume as an actor type: find it by bounds or by its outliner folder, which must already exist.
- Nothing appears and no error: the graph has no spawn node connected, or the assets list is empty; read the graph structure back.
- Bulk placement on the real island without asking: never. First run in a test folder, then the owner's yes.
- The instant graphs (`Instant_*`, under `/PCGPrimitives/Instants/`) place, spawn and transform; none scatters N props over a square. Use a full graph for a scatter.
- Memory: many instances add up; check the budget with `uefn-profiling` after a big scatter.

Order of the tools, names as in the map (`mcp_map.py --find pcg`): create graph, add subgraph node, connect node pins, get graph structure, spawn graph instance, execute graph instance, list graph instances.
