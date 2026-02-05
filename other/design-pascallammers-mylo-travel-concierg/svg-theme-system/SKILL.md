---
name: svg-theme-system
description: "Use when you need SVGs with selectable/customisable appearance: multiple palettes (WLILO / Obsidian / light), consistent typography, and repeatable agent-friendly pipelines. Triggers: svg theme, tokens, palette, WLILO, obsidian, design system, dark mode, diagram styling." 
---

# Skill: SVG Theme System (Selectable + Customisable)

## Scope

This Skill is about making SVG output:
- Consistent across diagrams
- Easy for agents to generate and evolve
- Themeable (multiple looks) without hand-editing 200 fills/strokes

It covers two practical approaches:
1. **Build-time theming**: generate per-theme SVG variants (best for `<img src="...">` usage)
2. **Runtime theming**: CSS variables inside inline SVG (best for apps that inline SVG markup)

## Inputs

- Target embedding mode:
  - **Static**: docs / `<img>` / GitHub rendering
  - **Inline**: injected SVG markup (e.g., in a UI control)
- Theme set (start with 2):
  - `obsidian` (industrial luxury)
  - `white-leather` (light)
- Constraints: readability, contrast, collision-free

## Procedure

### 1) Pick your pipeline

- If the SVG is loaded as a file (image/object): choose **build-time theming**.
- If the SVG is inlined into HTML (string/DOM): runtime theming is possible.

### 2) Define a theme token schema (keep it small)

Recommended minimum tokens:
- `background.primary`, `background.secondary`
- `surface.card`, `surface.border`
- `text.primary`, `text.secondary`, `text.muted`
- `accent.primary`, `accent.gold`
- `status.active`, `status.planned`, `status.error`, `status.warning`
- `strokeWidth.normal`, `strokeWidth.emphasis`
- Typography: `font.sans`, `font.serif`, `font.mono`

Rule: Don’t invent per-diagram tokens. Reuse the schema.

### 3) Apply the tokens consistently

Use tokens for:
- Fills (backgrounds/panels)
- Strokes (borders/connectors)
- Text colors
- Highlight glows/filters

Avoid:
- Inline hardcoded colors repeated across nodes

### 4) Theme selection patterns

#### A) Build-time (recommended default)

- Generator accepts `--theme <name>`.
- It outputs `diagram.<theme>.svg` (or into theme folders).

This works everywhere, including `<img>` embedding and markdown.

#### B) Runtime (inline SVG only)

- Put a `<style>` block inside `<defs>` that defines CSS variables.
- Reference them in attributes (e.g. `fill="var(--svg-bg)"`).

Important: runtime theming will **not** work for every renderer (depends on how SVG is embedded).

### 5) Agent-efficient iteration loop

When using agents to produce or modify SVGs:

1. **Structure/layout first** (use JSON/plan)
2. **Generate via templates** (MCP svg tools or generator script)
3. **Validate collisions** (tools are your eyes)
4. **Fix + revalidate** until clean

## Validation

- `node tools/dev/svg-collisions.js <file> --strict` (pass: zero 🔴 HIGH)
- `node tools/dev/svg-validate.js <file>` (pass: zero errors)

## Escalation / Research request

Ask for dedicated work if:
- You need a new reusable template for `svg_stamp`/`svg_create`.
- You need a shared “theme registry” used by both generator scripts and the SVG MCP server.

## References

- SVG methodology: `docs/guides/SVG_CREATION_METHODOLOGY.md`
- SVG MCP tools: `docs/guides/SVG_TOOLING_V2_QUICK_REFERENCE.md`
- WLILO style: `docs/guides/WLILO_STYLE_GUIDE.md`
- Collision tool: `tools/dev/svg-collisions.js`
