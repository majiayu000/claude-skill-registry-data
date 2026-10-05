---
name: cm-design-system
description: |
  Ultimate Design System Intelligence. Manage, extract, replicate, and improve UI design systems. 
  Extracts design tokens visually from existing sites (Harvester v5), manages multi-page tokens, and utilizes MCP servers like Google Stitch and Pencil.dev to generate complete, consistent design systems (Shadcn UI, Halo, Lunaris, Nitro).
  Use when the user asks to "extract design from a URL", "create a Shadcn design system", "analyze design tokens", "build a design system for", or "copy the UI style of".
---

# Goal
Establish a robust, stable, and consistent UI Design System by either extracting tokens from an existing source (Harvester mode) or scaffolding a fresh system based on premium Kits (Shadcn, Halo, Lunaris, Nitro). Output a strictly formatted `DESIGN.md` artifact ready for UI generation.

# Instructions
0. **Load Design Taste** (if `.cm/design-taste.json` exists): Before proposing tokens, call `topTaste(cwd, 'color')`, `topTaste(cwd, 'font')`, `topTaste(cwd, 'layout')` from `src/utils/design-taste.ts`. Bias selections toward `approved` entries; avoid `rejected`. Decay is 5 %/week so stale taste fades — trust live weights. After the user accepts or rejects a palette, call `recordTaste(cwd, { dimension, value, verdict })` so future runs improve.
1. **Clarify Intent**: Determine if the user wants to *extract* an existing design from a URL/Image or *create* a new system from a specific UI Kit.
2. **Harvester Extraction (If applicable)**: 
   - Analyze the target visual source.
   - Extract semantic colors (Primary, Secondary, Success, Warning, Danger), neutral ramps (50-900), typography scales, spacing tokens, and border radii.
3. **Pre-built UI Kits (Default Mode)**:
   - If the user wants a beautiful design quickly, DO NOT try to generate tokens manually.
   - Instead, copy one of the pre-built design systems from `skills/cm-design-system/resources/` into the project's `.stitch/DESIGN.md` or continue directly in `cm-design-system`:
     - `shadcn-default.md` (Use this as the absolute DEFAULT if no style is specified)
     - `halo-modern.md` (Premium dark mode, glowing accents)
     - `lunaris-advanced.md` (Tech-focused, monospaced fonts)
     - `nitro-enterprise.md` (High-contrast, data-dense enterprise)
4. **Pencil.dev & Google Stitch MCP**:
   - **Stitch path:** Use `DESIGN.md` with `<!-- STITCH_TOKENS_START -->` JSON block to feed design tokens into Google Stitch's AI generator via `cm-design-system`.
   - **Pencil path:** Use the Pencil MCP tools to create and manage `.pen` design files directly:

   **Pencil.dev Workflow:**
   ```
   1. open_document()         → Create/open a .pen file
   2. get_guidelines("web-app") → Load design rules for target platform
   3. get_style_guide_tags()  → Browse available style tags
   4. get_style_guide(tags)   → Get color palette, typography, spacing
   5. set_variables()         → Apply design tokens as .pen variables
   6. batch_get(reusable:true)→ Read existing design system components
   7. batch_design()          → Insert/update components and screens
   8. get_screenshot()        → Verify visual output
   ```

   **Mapping DESIGN.md tokens to .pen variables:**
   ```javascript
   mcp_pencil_set_variables({
     filePath: "design-system.pen",
     variables: {
       "primary": { "type": "color", "value": "#3B82F6" },
       "secondary": { "type": "color", "value": "#10B981" },
       "surface": { "type": "color", "value": "#FFFFFF" },
       "text-primary": { "type": "color", "value": "#0F172A" },
       "border-radius": { "type": "number", "value": 8 },
       "spacing-sm": { "type": "number", "value": 8 },
       "spacing-md": { "type": "number", "value": 16 },
       "spacing-lg": { "type": "number", "value": 32 }
     }
   })
   ```

   - For UI component rendering against these tokens, continue through `cm-design-system`.
   - **IMPORTANT:** Never use `view_file` or `grep_search` on `.pen` files. Always use `mcp_pencil_batch_get`.
5. **Export Custom `DESIGN.md` (Extraction Mode)**:
   - If extracting from a site visually, create the `DESIGN.md` document.
   - You MUST construct the exact JSON token block wrapped in `<!-- STITCH_TOKENS_START -->` and `<!-- STITCH_TOKENS_END -->`.

# Examples

## Example 1: Extract design from a URL
**Input:** "Can you extract the design system from stripe.com to use in our project?"
**Action:**
1. Extract semantic colors: Primary (Blurple), surface colors, typography (Inter), rounded corners.
2. Build the `DESIGN.md` including the Stitch STITCH_TOKENS JSON block with these tokens.
3. Tell the user: "Extraction complete. I've saved the tokens in `DESIGN.md`. Would you like me to continue the `cm-design-system` flow to generate components?"

## Example 2: Scaffold a new robust design system
**Input:** "Create a modern dark-mode design system using Halo UI kit."
**Action:**
1. Generate a premium deep-dark color palette.
2. Structure the tokens using Halo's spacing and glassmorphic shadow values.
3. Output `DESIGN.md` with STITCH_TOKENS.
4. Provide standard Tailwind config parameters matching the system.

## Example 3: Create a design system in Pencil.dev
**Input:** "Create a design system for our SaaS dashboard directly in Pencil.dev."
**Action:**
1. Open or create a `.pen` file: `mcp_pencil_open_document({ filePathOrTemplate: "new" })`.
2. Load design guidelines: `mcp_pencil_get_guidelines({ topic: "design-system" })`.
3. Browse and select a style guide: `mcp_pencil_get_style_guide_tags()` → `mcp_pencil_get_style_guide({ tags: ["saas", "dashboard", "modern", "website", "clean"] })`.
4. Apply design tokens via `mcp_pencil_set_variables()` using the style guide's recommendations.
5. Create reusable components (buttons, cards, inputs) via `mcp_pencil_batch_design()`.
6. Verify with `mcp_pencil_get_screenshot()`.
7. Tell the user: "Design system created in `design-system.pen`. Would you like me to build screens using these components?"

# Constraints
- 🚫 **DO NOT** generate or build React/Vue UI components outside the `cm-design-system` flow.
- 🚫 **DO NOT** skip the `<!-- STITCH_TOKENS_START -->` wrapper in `DESIGN.md`. It is critical for Stitch MCP parsing.
- 🚫 **DO NOT** guess accessibility constraints — ensure text-on-background contrast aligns with WCAG AA (handled via `cm-ux-master` heuristics).
- 🚫 **DO NOT** use `view_file` or `grep_search` on `.pen` files. Always use Pencil MCP tools (`batch_get`, `batch_design`, etc.).
- ✅ **ALWAYS** define a complete neutral scale (50-900) even if the source site only uses a few grays.
