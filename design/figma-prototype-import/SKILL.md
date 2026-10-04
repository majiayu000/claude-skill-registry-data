---
name: figma-prototype-import
description: Prototype Design Plugin workflow. Generate design-context notes, preview images, editable frontend review pages with direct edit requests and comments, structured JSON, optional frontend web pages, and a local Figma Desktop plugin that imports editable native Figma prototype nodes. Use when the user asks to turn text requirements, reference screenshots, existing-system screenshots, generated page images, SVG/PNG previews, admin pages, dashboards, app screens, or prototypes into editable Figma designs or web pages; when they mention prototype design plugin, one-click Figma import, local Figma plugin import, JSON-to-Figma, preserving editability across projects, matching an existing style, keeping a fixed navigation/sidebar/header, or reviewing and modifying prototype changes in a webpage before Figma import.
---

# Prototype Design Plugin

Use this skill to standardize the verified workflow:

`text requirements / reference screenshots -> design context -> preview images + editable frontend review page -> structured JSON -> local Figma plugin and/or frontend web page -> editable native Figma nodes`

Images are previews only. For editable prototypes, generate JSON and use the plugin to create Figma-native `FRAME`, `TEXT`, `RECTANGLE`, `LINE`, and other nodes.

## Start Here

1. Copy the template from `assets/figma-prototype-template` into the current project, usually as `figma-prototype/`.
2. Capture design context in `design-context.json` when the user provides screenshots, URLs, existing-system references, or style constraints.
3. Replace `prototype.json` with the project-specific page model.
4. Update `generate-preview-assets.js` so preview SVG/PNG/HTML and `previews/review.html` match the requested pages.
5. Update `build-plugin.js` so the JSON schema maps to Figma-native nodes.
6. Run preview and plugin build commands.
7. Let the user review `previews/review.html` and provide direct edit requests plus comments before final Figma import when iteration is expected.
8. Apply review JSON back into `design-context.json`, `prototype.json`, previews, generated web page code, and plugin output.
9. Register or import the local Figma plugin in Figma Desktop.
10. Run the localized Figma menu item `one-click generate prototype` or `import custom JSON` to append generated frames to the current Figma file.

Read `references/standard-workflow.md` when you need the full SOP, troubleshooting details, or registration caveats.

To initialize a project quickly, run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "$env:USERPROFILE\.codex\skills\figma-prototype-import\scripts\init-figma-prototype.ps1" -Destination ".\figma-prototype"
```

## Required Project Shape

Create or maintain this directory:

```text
figma-prototype/
  design-context.json
  prototype.json
  previews/
    index.html
    review.html
    *.svg
    *.png
  figma-json-native-plugin/
    manifest.json
    code.js
    ui.html
  build-plugin.js
  generate-preview-assets.js
  register-plugin.ps1
  README.md
```

## Core Rules

- Use `design-context.json` to preserve source references, style constraints, fixed navigation/header/sidebar rules, typography, color tokens, spacing, and component conventions.
- When the user provides screenshots from an existing system, inspect them as design references and extract reusable rules before generating new pages.
- Preserve fixed shell elements from reference screenshots, such as left navigation, top bar, tab structure, table density, filters, and button placement, unless the user asks to change them.
- Treat `prototype.json` as the source of truth for editable Figma output.
- Treat PNG/SVG/HTML and the frontend review page as visual preview and human review artifacts.
- The review page may collect direct edit requests and comments, but it does not automatically write local files when opened as a plain `file://` page. Use copied/downloaded review JSON as the input for the next generation pass.
- Do not use flat PNG/JPG import as the final path when the user wants editable Figma content.
- Use local Figma Plugin API for final import unless official Figma MCP is explicitly available and not quota-limited.
- Preserve previous imports by appending new frames to the right of existing canvas content. Do not delete or overwrite old frames unless the user explicitly asks.
- Keep generated top-level frames clearly named by page title.
- Return or document the plugin manifest path for user import.

## Design Context And Reference Screenshots

When the user provides screenshots or says to match an existing system:

1. Create or update `design-context.json`.
2. Record each reference file path and what should be copied from it.
3. Extract practical rules:
   - frame sizes and breakpoints
   - font family, type scale, weights, and line heights
   - color tokens and semantic usage
   - grid, spacing, border radius, shadows, and density
   - shell constraints such as fixed sidebar, header, tabs, breadcrumbs, and action areas
   - reusable component patterns such as tables, filters, cards, forms, charts, buttons, status tags, and empty states
4. Mark hard constraints explicitly, for example `preserve left navigation exactly` or `new content area only`.
5. Use the extracted rules in both previews and JSON-to-Figma mapping.

If an Open Design skill is available and installed, it can be used as an additional design-system source. If it is unavailable, use the installed Product Design skills and local `frontend-design` guidance as the practical design standard.

## Frontend Review Page

Generate a review page before Figma import when the user expects to iterate or wants to modify the prototype in a browser first.

Required behavior:

- Create `previews/review.html` next to `previews/index.html`.
- Show every generated screen preview.
- Include direct edit fields and comment fields per screen.
- Include global direct edit fields and global comment fields.
- Allow copying or downloading the review changes as JSON.
- Store changes in browser `localStorage` so refreshing the file does not lose feedback.
- Keep the review page non-authoritative: review JSON guides the next iteration, while `prototype.json` remains the Figma source of truth.

Use review JSON to update `design-context.json`, `prototype.json`, previews, generated web pages, and plugin output before asking the user to import into Figma.

## JSON Model Guidance

Use a project-specific JSON model with:

- `meta`: name, version, target Figma URL when known.
- `theme`: font family, typography, spacing, radius, and color tokens.
- `pages`: page id, title, frame size, navigation state, and page-specific sections.

Prefer semantic fields such as `stats`, `table`, `forms`, `toggles`, `charts`, `cards`, `sections`, and `interactions`.

The plugin should translate semantic JSON into native nodes, not into a single SVG or image.

## Plugin Requirements

The plugin manifest should expose two commands:

```json
"menu": [
  { "name": "<localized one-click generate prototype>", "command": "create-demo" },
  { "name": "<localized import custom JSON>", "command": "import-json" }
]
```

Implement behavior:

- The one-click command creates frames from embedded JSON without showing UI.
- The custom JSON command shows `ui.html`, prefills current JSON, then creates frames from edited JSON.

Important implementation details:

- Do not access `figma.ui` in the no-UI `create-demo` branch.
- Call `figma.showUI(__html__)` only in the custom JSON branch.
- Load fonts before creating or editing text: `await figma.loadFontAsync(...)`.
- Convert hex colors to Figma RGB 0-1 values.
- Append generated frames to a clear area to the right of existing top-level nodes.
- Use `figma.currentPage.selection = created` and `figma.viewport.scrollAndZoomIntoView(created)` after generation.
- Use `figma.closePlugin("...")` for success and failure messages.

## Commands

From the project root:

```powershell
node .\figma-prototype\generate-preview-assets.js
node .\figma-prototype\build-plugin.js
node --check .\figma-prototype\figma-json-native-plugin\code.js
Get-Content -Raw -Encoding UTF8 .\figma-prototype\figma-json-native-plugin\manifest.json | ConvertFrom-Json > $null
```

If using the bundled registration helper:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\figma-prototype\register-plugin.ps1
```

Register only while Figma Desktop is closed.

For review before import, open:

```text
figma-prototype\previews\review.html
```

## User-Facing Figma Steps

If the plugin is not already listed:

```text
Figma Desktop -> Plugins -> Development -> Import plugin from manifest...
```

Select:

```text
figma-prototype\figma-json-native-plugin\manifest.json
```

Then run:

```text
Plugins -> Development -> <Prototype Design Plugin> -> <one-click generate prototype>
```

For custom data:

```text
Plugins -> Development -> <Prototype Design Plugin> -> <import custom JSON>
```

## Non-Destructive Import Rule

Every import must preserve earlier generated content unless the user asks to clean or replace.

Implement this by computing the right edge of all existing top-level nodes and placing the first new frame after that edge, with a spacing gap such as 80 or 120 px. The bundled template already follows this pattern.

Do not select all and delete. Do not reuse fixed `x = 0` if there are existing frames.

## Validation

After import, success requires:

- Figma canvas shows the generated pages.
- Each page is a separate top-level frame.
- Layers panel contains child `TEXT`, `RECTANGLE`, `LINE`, etc.
- Text can be selected and edited.
- The result is not a single image.
- Existing imported frames remain on the canvas.

If a red Figma plugin error appears, ask for the console screenshot or error text, then fix the plugin code and rebuild.

## Known Pitfalls

- Figma Starter plan can limit official MCP calls; local plugin path avoids MCP quota.
- Figma Desktop can overwrite `settings.json` while running; close Figma before scripted registration.
- Write `settings.json` as UTF-8 without BOM if using scripted registration.
- Plugins with `ui.html` need manifest, code, and UI file entries in local registration.
- Windows desktop automation may be unavailable; when it is, hand off the final Figma menu click to the user.
