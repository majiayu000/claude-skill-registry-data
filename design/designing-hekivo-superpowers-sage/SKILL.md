---
name: superpowers-sage:designing
description: >
  Design UI/UX in a Sage project — Figma to Blade, design tokens to Tailwind v4,
  Paper/Figma MCP integration, component design, layout design, responsive design,
  design-to-code workflow, visual design review, design system alignment,
  design approval before implementation
user-invocable: true
---

# Designing — Design Tool Integration

Route to the right design tool based on the URL the user provides — Paper (preferred), Stitch, Figma, or local assets — to extract layout, content, and visual references for implementation.

## When to use
- Starting implementation of a visual design
- Need to capture design reference before building
- Comparing implementation against design
- Populating plan assets directory with screenshots

## Inputs required
- Design source: Stitch project ID, Figma file URL, or local asset path
- Optional: specific section/screen name to extract

## Procedure

### 0) Determine source from user input (URL-based routing)

Routing is driven by what the user provided, not by which MCPs happen to be configured.

1. **URL match** — inspect the user's input for a design URL:
   - `paper.design/*` or `*.paper.design/*` → **paper** branch (use `mcp__paper__*`)
   - `figma.com/*` → **figma** branch (use `mcp__figma__*` / `mcp__claude_ai_Figma__*`)
   - `stitch.withgoogle.com/*` (or other known stitch hosts) → **stitch** branch (use `mcp__stitch__*`)
2. **Path match** — inspect user input for a `.pen` reference:
   - Input ends in `.pen` OR input starts with `design/` → **pencil** branch
   - No input provided AND `design/` exists in the project root with `.pen` files:
     list the available `.pen` page files (exclude `*.lib.pen`) and ask the user
     which page to extract before proceeding.
3. **Local fallback** — if no URL but `docs/plans/<active-plan>/assets/section-*.png` exists → **offline** branch
4. **Ask** — if neither URL nor local assets are present, ask the user for one

**MCP gate:** once the branch is known, ToolSearch the corresponding `mcp__<tool>__*` namespace. If the MCP is NOT configured, stop with this message:

```
⛔ You sent a {paper|figma|stitch} link but the `{tool}` MCP is not configured.

Configure it and re-run, or send a link from another source.
```

Do NOT silently fall back to a different MCP.

**Pencil MCP gate:** For the pencil branch, ToolSearch `mcp__pencil__open_document`.
If NOT configured:

```
⛔ .pen file detected but the Pencil MCP is not configured.

Install: claude mcp add pencil -- npx -y @anthropic/pencil-mcp
Restart the session after installing.
```

### 1) Extract design data (per section, never full design at once)

#### Paper workflow (preferred when source is paper.design):
1. `mcp__paper__get_basic_info` — get document metadata
2. `mcp__paper__get_tree_summary` — locate the target section node
3. `mcp__paper__get_node_info` on the section — capture structure, text, hierarchy
4. `mcp__paper__get_screenshot` — save as `assets/section-{name}.png`
5. `mcp__paper__get_computed_styles` — save as `assets/section-{name}.styles.json` (typography, colors, spacing — exact values; consumed by `verifying` for the style spot-check)
6. `mcp__paper__get_jsx` — save as `assets/section-{name}.reference.jsx` with this header comment as the FIRST lines of the file:
   ```
   // REFERÊNCIA ESTRUTURAL APENAS — NÃO COPIAR.
   // Sage usa Blade, não React. Use isso só para entender
   // hierarquia de componentes e nesting.
   ```
7. Produce the structured output (see step 2) — same schema as the other branches.

#### Stitch workflow:
1. `mcp__stitch__list_projects` — find the project
2. `mcp__stitch__list_screens` — enumerate all screens
3. `mcp__stitch__get_screen` — extract one section at a time
4. For each section, capture: headline, body text, components, colors, layout structure

#### Figma workflow:
1. `mcp__figma__get_file` — load the file structure
2. Navigate frames to find sections
3. Extract text layers, colors, component structure per section

#### Pencil workflow:
1. `open_document(filePath)` — open the `.pen` file the user indicated
2. `get_editor_state()` — confirm top-level nodes and document is active
3. `batch_get` with no nodeIds, `readDepth: 1` — map all available sections
4. For each section to extract: delegate to `pencil-extractor` in SURGICAL mode,
   passing `filePath`, `sectionId`, and `planPath`
5. After all sections: optionally invoke `pencil-extractor` in COMPONENT_MAP mode
   to produce `design/component-map.md`

#### Offline workflow:
1. Read images from `docs/plans/<plan>/assets/section-*.png`
2. Claude reads images natively — describe layout, content, colors
3. If no assets exist, ask user to provide screenshots

### 2) Structure the output

For each section extracted, output:

```
### Section: {name}

**Layout:** {grid structure, column arrangement, alignment}
**Headline:** "{exact text}"
**Body:** "{exact text}"
**Components:** {cards, buttons, icons, images — with details}
**Colors:** {background, text, accent — hex values if visible}
**Typography:** {heading size, body size, weight, font family}
**Spacing:** {padding, margins, gaps — approximate}
**Icons:** {icon names/types, from which set}
```

### 3) Save to plan assets (if active plan exists)

If there's an active plan in `docs/plans/`:
- Save extracted data as structured notes in `assets/section-{name}.md`
- If screenshots are available, note their paths
- Update `plan.md` frontmatter with `design-tool: paper|stitch|figma|offline`

## Key Principles
- **Granular extraction** — always per-section, never full design at once (prevents context overflow)
- **Exact content** — copy text verbatim, don't paraphrase headlines or body text
- **Persist to disk** — save everything to plan assets/ so it survives context compression
- **Re-read before implementing** — always re-read assets from disk, never rely on context memory
