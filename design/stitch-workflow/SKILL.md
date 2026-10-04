---
name: stitch-workflow
description: Generate, edit, or vary UI screens with the Stitch MCP server, after gathering Linear + GitHub context. Use when a request is about designing/mocking up/generating a new screen, or a `stitch-design` rule trigger fires.
---

# Stitch Workflow

This skill covers the raw MCP call sequence against whichever `stitch`
server is configured in `.mcp.json` (currently `@_davideast/stitch-mcp` —
see `.claude/rules/stitch-design.md`). Tool names below are the underlying
API's names; the actual callable name is prefixed by the MCP connector
(confirm with `ToolSearch("select:mcp__stitch")` before first use — don't
assume the prefix).

If the `stitch-skills` plugin
(https://github.com/google-labs-code/stitch-skills) is installed locally
(a global, per-developer install — see `.claude/rules/stitch-design.md`),
its `stitch::*` skills (`stitch::generate-design`, `stitch::code-to-design`,
`stitch::react-components`, ...) cover the same ground with more
task-specific prompts/validation. Prefer this skill's flow when you want
the intake-driven, SBSI-specific prompt template below; reach for a
`stitch::*` skill when its more specialized workflow (e.g. converting
existing frontend code to a Stitch design, or Stitch screens to React
components) fits the task better.

## 0. Intake first

Before writing any prompt, complete the `design-request-intake` skill in
full — Linear context, GitHub/codebase context, and platform confirmation
(mapped here to Stitch's `deviceType`: `MOBILE`/`DESKTOP`/`TABLET`).
Skipping this produces a generic Stitch prompt with none of the
product/design context that made the request worth tracking in the first
place, and risks generating for the wrong platform.

## 1. Build the prompt

### New screen template

```
[Overall purpose and user intent of the page]

PLATFORM: [Mobile/Desktop/Tablet], [confirmed during intake]

PAGE STRUCTURE:
1. Header: [navigation and branding]
2. Primary Content Area: [detailed component breakdown — be specific:
   name components, not vague adjectives]
3. Secondary/Supporting Content: [sidebars, related content, etc.]
4. Footer/Actions: [links, primary/secondary CTAs]
```

Ground each section in what you learned during intake — actual product
terminology from the Linear issue, actual component names already used
elsewhere in the target app, not generic placeholders.

### Edit template

Be specific about location, change, and (for edits only — not new-screen
generation) exact values:

```
Change the [element] in the [section] to [new value/behavior].
Add a [new element] next to [existing element] with [content/behavior].
```

## 2. MCP call sequence

1. `list_projects` — find the project for the target app. If none
   exists, `create_project` (name it after the app, e.g. "SBSI Research
   Hub").
2. **Design system** — `list_design_systems` for that project. If SBSI's
   design system asset doesn't exist yet for this project, create it once:
   - `create_design_system` with (per `.claude/design-system/README.md`):
     `customColor: "#ad0a0c"` (SBSI brand primary — resolve live via Figma
     if connected instead of hardcoding, see `.claude/rules/figma-design.md`),
     `colorMode: "LIGHT"` or `"DARK"` matching the mode confirmed during
     intake (Stitch's theme is single-mode; for a screen that needs both,
     create two assets — e.g. "SBSI — Light" / "SBSI — Dark" — and pick
     the matching one per generation), and a `designMd` block listing the
     key semantic roles this project actually needs (Text/BG/Stroke for
     the relevant mode, plus `Text.Price.*` if the screen shows trading
     prices) resolved to hex from `.claude/design-system/tokens-SBSI-design-system-v1.json`.
   - Immediately call `update_design_system` after creation (the tool's
     own instructions require this to apply + display it).
   - Reuse the existing asset on later generations for the same
     project/mode — don't recreate it every time.
3. `generate_screen_from_text` with the enhanced prompt + the `deviceType`
   confirmed during intake, using the target project. For edits, call
   `edit_screens` against the existing screen instead.
4. Read the response's `outputComponents` — it carries a text
   description, suggestions, and HTML/screenshot URLs, plus the screen
   instance id/sourceScreen needed for step 5.
5. `apply_design_system` with the SBSI asset's id and the generated
   screen instance, so the output is forced onto SBSI's palette rather
   than whatever Stitch guessed from the prompt alone.
6. Download the HTML and screenshot into
   `.stitch/designs/<app>/<screen-slug>/` (create the directory if
   needed; gitignored, so nothing here needs cleanup before committing
   elsewhere).
7. Present the description + suggestions + screenshot back to the user.

## 3. Iterating

- **Single revision**: `edit_screens` with a targeted prompt (see Edit
  template above). No need to re-ask platform — it's fixed to the screen
  being edited.
- **Variants**: call `generate_screen_from_text` (or `edit_screens`)
  multiple times with explicit, named deltas ("dark mode", "high-density
  layout", "warm color variant") — never "give me some options" run blind
  N times with no stated axis of variation. Save each under a sibling
  slug in `.stitch/designs/<app>/`.

## Other available tools (use as needed, not part of the default flow)

- `extract_design_context` — pull font/color/layout "design DNA" from an
  existing screen, useful before generating a new screen that should
  match it.
- `fetch_screen_code` / `fetch_screen_image` — re-download an existing
  screen's HTML/screenshot without regenerating it.
- `list_screens` / `get_screen` / `get_project` — inspect existing state
  before deciding whether to create new vs. edit existing.
