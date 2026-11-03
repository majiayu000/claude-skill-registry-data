---
name: opendesigner-export
description: Exports an OpenDesigner system to CSS variables, Tailwind, DTCG, Swift, Compose, Figma and Paper, and writes it into Figma or Paper through their MCP servers when connected.
license: MIT
compatibility: Python 3.10+ (standard library). Figma writes need Figma's remote MCP (signed in, Full seat); Paper writes need Paper Desktop running.
metadata:
  version: "0.1.0"
  homepage: "https://github.com/ckryptickunal/OpenDesigner"
---

# OpenDesigner: export and round trip

Use this when the person wants their system in code, in Figma or in Paper. It works after an OpenDesigner interview or on any existing `opendesigner/` folder.

The DTCG files in `opendesigner/tokens/` are the source of truth. Every other format is generated from them. Never edit an export by hand: change the decision and regenerate.

The engine is `scripts/engine.py` in this skill when it was installed from a release zip. Otherwise it is the sibling opendesigner skill's `scripts/engine.py`. Run it from the project root.

## 1. Code exports (always available)
```
python3 <engine> build                      generate, validate, then every export, DESIGN.md and the preview
python3 <engine> export --format tailwind   one format only: css tailwind dtcg figma paper swift compose artifact, or all
```
| Format | Output in `opendesigner/` | Use it |
|---|---|---|
| (canonical) | `tokens/` (DTCG sets plus `opendesigner.resolver.json` for modes) | Style Dictionary, Terrazzo, Tokens Studio, Penpot |
| `dtcg` | `build/dtcg/<name>.resolver.json` | A single resolver file for tools that take one entry point |
| `css` | `build/css/tokens.css` (custom properties, light and dark) | Import once at the app root |
| `tailwind` | `build/tailwind/theme.css` (Tailwind v4 `@theme`; it imports `../css/tokens.css` itself) | One line after Tailwind in the main CSS file (below) |
| `swift` | `build/swift/DesignTokens.swift` (Dynamic Type text styles; body 17 pt) | Add to the iOS target |
| `compose` | `build/compose/DesignTokens.kt` | Add to the Android UI module |
| `figma` | `build/figma/variables.json` and `build/figma/import/<Collection>.<Mode>.tokens.json` | Import in Figma (below) when there is no MCP |
| `paper` | `build/paper/tokens.json`, `build/paper/tokens.light.css`, `tokens.dark.css` | Paper tokens (below) |
| `artifact` | `build/artifact/project/` (the system as a Claude Design System artifact's files: index, tokens, README) | Publish the system as a browsable design-system page in Claude |

**Tailwind v4 wiring.** In the main CSS file, for example `src/index.css`:
```css
@import "tailwindcss";
@import "../opendesigner/build/tailwind/theme.css";
```
- Adjust the relative path to where the CSS file sits. `theme.css` brings in `tokens.css`, so light and dark, density and reduced motion work through CSS variables.
- Utility classes follow the token roles, for example `bg-action-primary`, `text-fg-primary`, `rounded-control` and `h-control-md`. DESIGN.md lists the class for each role.
- By default the export switches off Tailwind's own palette, radius, shadow and text sizes, so a stray `bg-blue-600` or `rounded-lg` doesn't compile. To keep them, run `engine.py set exports.tailwindReset false`, then `engine.py build`.

**Fonts per platform.** If `raw.fontLicence` says the brand font's licence doesn't cover apps, the Swift and Compose files use the system font instead, and say so. Tell the person in one line before they ship an app build.

Ask before wiring an export into the person's code, such as their main CSS file, Tailwind config or build. For an engineer, name the exact files and lines, as above. Offer to append `<opendesigner>/assets/output/AGENTS-snippet.md` to their AGENTS.md, so later agents use the tokens.

## 2. Figma
Detect what is connected before promising anything:
- **Remote Figma MCP with `use_figma`** (signed in, Full seat; canvas writes are in beta): it can create variables, styles and frames. If Figma's official skills are installed (`figma-use`, `figma-generate-library`), load them and follow their rules. They know the current API.
- **Figma desktop MCP only** (`get_variable_defs`, `get_design_context`, `get_screenshot`): read-only. Use it to check, not to write.
- **Nothing connected:** hand over `build/figma/import/` (one DTCG file per collection and mode) for Figma's variables import, or `build/figma/variables.json` for Tokens Studio. Say that Figma imports DTCG only in part: one mode per file, sRGB, px, and no composite tokens.

Write flow with `use_figma`:
1. Confirm the target file with the person and suggest working on a duplicate first.
2. Create the five collections in `build/figma/variables.json`, in its order:
   - **Primitives:** ramps and raw sizes, no modes, hidden from publishing.
   - **Color:** color roles aliased to primitives, one mode per color scheme (Light and Dark).
   - **Density:** spacing and control sizes, one mode per density (spacious, comfortable, compact).
   - **Motion:** durations and easings, with Standard and Reduced modes.
   - **Tokens:** everything that does not change by mode (radius, weights, font families and the like).

   The Figma plan caps the modes per collection (`exports.figmaPlan`, set by Q-tool-03). The engine splits a collection that goes over the cap and warns. Check the plan before adding more themes.
3. Create variables with explicit scopes (never "all scopes"), and set code syntax to the CSS variable name so developers see `var(--...)`.
4. Add text styles for the type scale and effect styles for the elevation levels.
5. Build one specimen frame per foundation (palette, type, spacing, radius, elevation) and a component sheet, bound to the variables.
6. Read back with `get_variable_defs` and compare against `tokens/`; report any mismatch.
7. When the person or a designer edits in Figma, read the changes back. Apply them as decisions (`engine.py set ... --why "changed in Figma by <name>"`), never by editing token files.

## 3. Paper
Paper's MCP server runs inside Paper Desktop (local, `127.0.0.1:29979/mcp`). If its tools are present:
1. Load Paper's guide first (`get_guide` with topic `paper-mcp-instructions`). Then call `get_basic_info` to see the file.
2. Write tokens from `build/paper/tokens.json` with `create_tokens` or `set_tokens`. Paper tokens are CSS variables without modes. Write the light values, and add the dark ones as a separate, clearly named set.
3. Call `get_font_family_info` before any typography. Then write specimen artboards with `write_html`, one visual group per call: palette, type ladder, spacing ruler, radius, elevation, component sheet. The HTML in `<opendesigner>/assets/templates/` (component sheet, palette) is a good start. Use the person's tokens, not sample data.
4. Review each artboard with `get_screenshot`. Fix clipping by setting the artboard height to fit its content.
5. Call `finish_working_on_nodes` when done.
6. Designer comments (`list_comment_threads`) and selections (`get_selection`) come back as decisions through the engine, like Figma edits.

## 4. Before you hand over
- Explain each export in one plain sentence, then give the path. For example: "This file gives your web app the colors as CSS variables."
- `engine.py validate` passes, or each remaining warning has a written waiver.
- The person knows the source of truth is the DTCG files in `opendesigner/tokens/`, and that exports are regenerated, not edited.
- Record the export in the summary: formats, destinations (file names, Figma file, Paper file) and date.
- If an export was missing, wrong or confusing, record it with `engine.py feedback "..." --kind gap|bug|confusing|idea` (see `references/improve.md` in the opendesigner skill). Nothing is posted without the person's OK.
