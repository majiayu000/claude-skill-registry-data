---
name: design-diagram-authoring
description: Author game-design diagrams (quest trees, economy flows, narrative branches, level layouts) from copy-ready Mermaid templates. Authoring only — NOT an adapter.
effort: low
keywords: [design diagram, quest tree, economy flow, narrative branch, level layout, game design diagram, mermaid template]
version: 1.2.0
origin: theonekit-designer
repository: The1Studio/theonekit-designer
module: design-base
protected: false
---

# Design Diagram Authoring

Copy-ready Mermaid templates and authoring guidance for the four most common game-design diagrams. This skill ships **templates + reference docs**, not code analysis. Rendering is delegated to `/t1k:preview`.

## When This Skill Triggers
- Starting a new GDD section that needs a visual (quest tree, economy, narrative, level)
- Sketching design intent before implementation
- Updating a design diagram alongside a gameplay change
- Need a Mermaid starting snippet that's more than a blank canvas

## What This Skill Is NOT
- Not an adapter — does not parse code, does not implement `detect()`, does not register with the adapter-discovery scan
- Not a renderer — `/t1k:preview --from-file <template>` handles that via `mermaid-cli`
- Not prescriptive — templates are starting points; edit freely

## The Four Templates

| Template | Mermaid Type | Use For |
|---|---|---|
| `templates/quest-tree.mmd` | `flowchart TD` | Branching quest progression, prerequisites, hub-and-spoke structures |
| `templates/economy-flow.mmd` | `flowchart LR` | Currency sources (faucets) → sinks, conversion rates, inflation control |
| `templates/narrative-branch.mmd` | `classDiagram` | Character relationships + branching narrative lanes by Act/chapter |
| `templates/level-spatial.mmd` | `flowchart LR` | Level zones, gates (one-way vs two-way), spatial progression |

## Usage

### 1. Copy a template into your project
```bash
cp .claude/modules/design-base/skills/design-diagram-authoring/templates/quest-tree.mmd \
   docs/design/my-quest-tree.mmd
```

### 2. Edit the placeholders
Each template is heavily commented. Replace placeholder labels (`Quest A`, `Gold`, `Act 1 Intro`, `Zone A`) with your actual design.

### 3. Render with /t1k:preview
```
/t1k:preview --from-file docs/design/my-quest-tree.mmd
```

Or render inline:
```
/t1k:preview --diagram "quest tree for the prologue act"
```

### 4. Paste into your GDD
Render produces SVG/PNG. Embed in GDD markdown alongside the `.mmd` source so both are tracked in git.

## Reference Docs (pattern guidance)

- `references/quest-trees.md` — linear / branch / hub-and-spoke / Act-based patterns
- `references/economy-flows.md` — faucet/sink distinction, conversion nodes, inflation leaks
- `references/narrative-branches.md` — decision vs outcome nodes, character arcs, consequence layering
- `references/level-spatial.md` — zones, gates, one-way edges, spatial vs logical adjacency

## Scripts

- `scripts/list-templates.cjs` — lists the four template names (used by `/t1k:find-skill` and doctor integrity checks)

## Rendering prerequisite

Install `mermaid-cli` once via the base preset:
```
t1k diagram install
```
The `install.json` in this skill advertises the dependency (`requires: ["mermaid-cli"]`) with `isAdapter: false`, so the installer rolls it up without registering the skill in adapter discovery.

## Authoring tips
- **Keep diagrams under ~30 nodes.** Mermaid rendering degrades and designers stop reading beyond that.
- **One diagram per concern.** Split quest prerequisites and narrative branches into two diagrams even when they touch the same NPCs.
- **Source of truth is the `.mmd` file.** Never hand-edit rendered SVGs — edit the source and re-render.
- **Comment intent, not mechanics.** `%% Act 1 gate — player must have fire talisman` not `%% edge from A to B`.
