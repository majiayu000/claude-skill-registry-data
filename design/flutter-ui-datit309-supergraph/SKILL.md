---
name: flutter-ui
description: Build Flutter UI from Figma MCP or image input. Scans src for design tokens (colors, sizes, text styles), existing components, and naming conventions before writing a single line of code. Never hard-codes values.
---

# /supergraph:flutter-ui

Build pixel-faithful Flutter UI grounded in the project's own design system.

Announce: "🎨 /supergraph:flutter-ui — scanning project design system..."

## Input modes

- **Figma MCP** — user provides a Figma URL or node ID
- **Image** — user provides a screenshot or design image

Figma URL: extract `fileKey` (after `/design/`) and `nodeId` (`node-id` param, replace `-` with `:`).

---

## Step 1 — Scan project design system

### 1a. Locate token files (prefer ripgrep, fallback to codebase-memory)

```bash
# Prefer ripgrep — 10-20x faster than find|xargs grep; single pass covers all token types
rg --type dart --type yaml -l "Color|Colors\.|TextStyle|fontSize|FontWeight|EdgeInsets|Radius|ThemeData|colorScheme" | grep -iE "color|theme|token|palette|constant|style|text|typo|font|dimen|size|spacing|radius" | head -20
# Fallback if rg not available: codebase-memory search_graph(project=CBM_PROJECT, query="Color TextStyle EdgeInsets") or serena get_symbols_overview
find . \( -name "theme" -o -name "themes" \) -type d | head -10
```

### 1b. Extract token registry

Read identified files and extract:
- **Colors**: `grep -n "static.*Color\|Color(" <token_file> | head -40` → constant name → hex/Color value
- **Text styles**: `grep -n "TextStyle\|fontSize\|FontWeight" <style_file> | head -40` → style name → fontSize + weight + color
- **Spacing/sizing**: `grep -n "static.*double\|const.*= [0-9]" <dimen_file> | head -40` → constant name → value
- **Theme**: `grep -n "ThemeData\|colorScheme\|MaterialApp" <theme_file> | head -20` → determine access pattern (direct class vs `Theme.of(context)`)

### 1c. Find existing reusable widgets

```bash
find . -path "*/widgets/*.dart" -o -path "*/components/*.dart" -o -path "*/common/*.dart" | head -30
```
For each: `grep -n "class \|const \|required \|this\." <widget_file> | head -20` — list as `WidgetName(params) → path`.

### 1d. Detect state management

```bash
grep -rn "import.*bloc\|import.*riverpod\|import.*provider\|import.*getx\|import.*mobx\|import.*signals" lib/ pubspec.yaml | head -10
```

### 1e. Detect naming & import convention

```bash
find . \( -path "*/lib/screens/*.dart" -o -path "*/lib/pages/*.dart" -o -path "*/lib/features/*.dart" \) | head -1
grep -n "import.*lib/" <reference_file> | head -10
```

---

## Step 2 — Extract design from Figma or image

**Figma:** `mcp__Figma__get_figma_data(fileKey=<key>, nodeId=<nodeId>)` → extract layout, colors, text, corners, spacing, variants/states, icons.

**Image:** Analyze visually — sections, layout direction, colors → match to nearest token.

Both: map every color/size/font to the token registry. **If no match → STOP, ask user before proceeding.**

Variants/interactive states (Figma): if node has variants (Normal/Hover/Disabled/Active) → map to boolean/enum param on the widget (`isDisabled`, `isActive`). Do NOT generate separate widgets per variant — one widget with conditional styling.

Download custom assets if needed: `mcp__Figma__download_figma_images(...)`. Verify directory declared in `pubspec.yaml` under `flutter.assets:`.

---

## Step 3 — Build token mapping table

| Design value | Token to use | Source |
|---|---|---|
| `#6C63FF` primary bg | `AppColors.primary` | registry |
| `24px bold` heading | `AppTextStyles.heading1` | registry |

**After building full table: any unmapped row → STOP, resolve with user before Step 4.**

---

## Step 4 — Plan widget tree

Decompose into widget tree before coding. Rules:
- Reuse existing widgets (Step 1c) wherever shape/behavior matches
- Extract sections > 40 lines into private `_WidgetName` classes in same file
- No widget method extraction (`Widget _buildXxx()`) — use classes

---

## Step 5 — Generate code

**Token usage (CRITICAL):** Never hard-code colors, font sizes, spacing, or radius:
```dart
// ✅ color: AppColors.primary  fontSize: AppTextStyles.body.fontSize  padding: EdgeInsets.all(AppSizes.paddingM)
// ❌ color: Color(0xFF6C63FF)  fontSize: 14  padding: EdgeInsets.all(16)
```

**Structure:** One file per screen. File name/location matches Step 1e convention. `const` constructors where possible. No `print()`, no `TODO`.

**Assets:** Material icons → `Icon(Icons.xxx)`. Custom PNG/SVG → `flutter_gen` generated class (check existing screens for naming). Asset name format: `snake_case`, prefix `ic_`/`img_`/`bg_`, include state suffix. Verify `pubspec.yaml` declares the asset directory.

**If `flutter_gen` not in `pubspec.yaml`:** propose setup before writing any asset reference:
```yaml
dev_dependencies:
  build_runner:
  flutter_gen_runner:
flutter: { assets: [assets/images/, assets/icons/] }
```
Run `flutter pub get && dart run build_runner build`. Never fall back to `Image.asset(string)` or `SvgPicture.asset(string)`.

**Responsive:** Only add `LayoutBuilder` if design shows multiple form factors. **State:** Use pattern from Step 1d only. `const` constructors for stateless leaf widgets only — omit where widget depends on runtime/reactive state.

---

## Step 6 — Self-verify before handing off

```bash
grep -n "Color(0x\|Color\.from\|Colors\.\|Widget _build\|print(\|TODO" <generated_file>
grep -nE "EdgeInsets\.(all|symmetric|only)\([^A-Z]|fontSize:\s*[0-9]|SizedBox\((height|width):\s*[0-9]" <generated_file>
```

Fix all hits (exception: `Colors.transparent` is allowed). Unfixable → note and ask user.

---

## Output format

1. Token mapping table (Step 3)
2. Widget tree plan (Step 4 summary)
3. Generated code — full file(s), ready to paste
4. Assets to download (if any)

---

## Hard rules

- NEVER hard-code color, font size, spacing, or radius
- NEVER introduce new design token without user approval
- NEVER use different state management from what src uses
- NEVER extract widget sections as methods — use private classes
- ALWAYS scan src before reading Figma/image
- If registry empty → stop and ask where design tokens are declared
