---
name: figma-to-compose
description: Generate Android Jetpack Compose UI from Figma using Figma Desktop MCP (get_metadata, get_variable_defs, create_design_system_rules, get_design_context, get_screenshot). Automatically detect icon/vector nodes in Figma, obtain SVG/path data when available, and convert icons to Android VectorDrawable XML using Android MCP Toolkit (convert-svg-to-android-drawable). Use when the user shares a Figma link/node-id and asks to implement UI in Compose from Figma.
---

# Figma → Jetpack Compose (MCP) + Auto Icon → VectorDrawable XML

## Tools available

### Figma Desktop MCP
- get_design_context
- get_screenshot
- get_variable_defs
- get_metadata
- create_design_system_rules
- get_figjam

### Android MCP Toolkit
- convert-svg-to-android-drawable
- read-adb-logcat
- get-pid-by-package
- get-current-activity
- fetch-crash-stacktrace
- check-anr-state
- clear-logcat-buffer
- estimate-text-length-difference

---

## What this Skill does
1) Reads Figma frame/component via MCP and generates matching Jetpack Compose code (Material3 default).
2) Extracts tokens (colors/typography/spacing/radius) from Figma variables when present.
3) **Automatically** detects icon/vector nodes from the Figma node tree and:
   - tries to obtain SVG/path data via MCP,
   - then **automatically converts** to Android VectorDrawable XML via `convert-svg-to-android-drawable`,
   - falls back to requesting a batch SVG export only if SVG content is not obtainable.

---

## Inputs (ask only if missing)
- Figma link OR node-id (preferred: exact frame/component link)
- Which frame/component if multiple exist
- Defaults (unless user specifies otherwise):
  - Jetpack Compose + Material3
  - Output: screen + components + theme tokens (Color/Type/Dimens)
  - Previews: at least 1–2 @Preview

---

## Main workflow: Figma → Compose

### Step 1 — Resolve target
- Use `get_metadata` to confirm the exact frame/component node-id(s).
- If link includes multiple frames, select based on name or ask user which one.

### Step 2 — Pull tokens & design system rules
- Use `get_variable_defs` to extract:
  - colors (including opacity)
  - typography (font family, weight, size, line height, letter spacing)
  - spacing/radius if variables exist
- Use `create_design_system_rules` to generate mapping rules:
  - variables → MaterialTheme.colorScheme / typography
  - spacing scale → Dimens
  - component conventions (buttons/textfields/cards) if present

### Step 3 — Generate UI structure
- Use `get_design_context` for selected node(s) to obtain layout/component context.
- Translate to idiomatic Compose:
  - Vertical auto layout → Column
  - Horizontal auto layout → Row
  - Overlap/absolute → Box (use align/offset only when necessary)
  - Gap → Arrangement.spacedBy(x.dp)
  - Padding → Modifier.padding(...)
  - Fill → fillMaxWidth()/fillMaxSize()
  - Radius → RoundedCornerShape(r.dp)
  - Stroke → Modifier.border(...)
  - Shadow → Modifier.shadow(...) (note: blur may be approximate)
  - Text styles → MaterialTheme.typography or custom TextStyle tokens
- Detect repeated patterns and extract reusable composables.

### Step 4 — Auto icon pipeline (MANDATORY, automatic)
Run this automatically while processing the selected screen/component. Do not wait for the user to request it.

#### 4.1 Detect icon/vector candidates
- Use `get_metadata` to traverse the node tree under the target frame/component.
- Mark nodes as icon candidates if any of:
  - Node type is VECTOR or BOOLEAN_OPERATION
  - Name matches typical icon naming: `icon*`, `ic_*`, `*Icon`, `*Glyph`
  - Small, square-ish dimensions (approx 12–48dp equivalent) and uses strokes/fills typical of icons
  - Component instances that represent icons (by name/metadata)

#### 4.2 Obtain SVG/path data (best-effort)
For each icon node-id:
- Call `get_design_context` for that icon node-id and attempt to extract SVG/path data from the returned context.
- Optionally call `get_screenshot` for preview/verification.

#### 4.3 Convert to VectorDrawable XML (automatic)
If SVG/path data is available:
- Call `convert-svg-to-android-drawable`
- Output file: `res/drawable/ic_<normalized_name>.xml`

#### 4.4 Fallback when SVG is not obtainable from MCP output
If SVG content cannot be extracted from MCP context:
- Produce a section **Assets Needed (SVG export)** containing, for each missing icon:
  - normalized icon name
  - node-id
  - a small preview screenshot (use `get_screenshot`)
- Ask the user once (batch) to export those nodes as SVG from Figma and paste/upload SVGs.
- Upon receiving SVGs, immediately run `convert-svg-to-android-drawable` and output XML files.

### Step 5 — Visual validation (recommended)
- Use `get_screenshot` for the main screen/frame.
- Validate major layout/spacing/typography. Call out mismatch risks:
  - blur/shadow not 1:1
  - missing fonts/assets
  - images needing export (PNG/WebP)

### Step 6 — Output deliverables
Generate:
- `ui/screen/<ScreenName>Screen.kt`
  - screen composable + state surface + previews
- `ui/screen/<ScreenName>Components.kt`
  - reusable components
- `ui/theme/Color.kt`
- `ui/theme/Type.kt`
- `ui/theme/Dimens.kt` (when spacing/radius repeated)
- `res/drawable/ic_<name>.xml` for every detected icon converted

Always include:
- **Generated VectorDrawables** list (file names)
- **Mapping Notes**:
  - token mapping summary
  - assumptions/approximations
  - assets required and where to place them

---

## Naming conventions
### Icon names
- Normalize to lowercase snake: spaces/dashes → underscore
- Strip common prefixes: `icon_`, `ic_` (but keep semantic name)
- Examples:
  - `ic_home_filled` → `ic_home_filled.xml`
  - `Icon/Search` → `ic_search.xml`
  - `home-24` → `ic_home_24.xml`

---

## Optional debugging helpers (only when user asks)
If user reports crash/ANR after integrating:
- For crash: `fetch-crash-stacktrace` + `read-adb-logcat`
- For ANR: `check-anr-state`
- For noisy logs: `clear-logcat-buffer`
Return: root cause + actionable fixes + minimal patches.

---

## Examples that should trigger this Skill
- "Implement màn hình này theo Figma bằng Jetpack Compose: <figma link>"
- "Build component set này (Button variants) theo Figma"
- "Làm UI theo Figma và tự generate VectorDrawable cho icons"
