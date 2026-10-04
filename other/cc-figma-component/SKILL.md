---
name: cc-figma-component
description: "Generate a Figma component set from a component contract. Use when the user wants to build or update a Figma component from a contract definition — e.g. 'build the Button Figma component', 'generate Figma component from contract', 'sync the Accordion to Figma', 'create component variants in Figma'. PREREQUISITE: the cc-figma-tokens skill must have been run first — Primitive and Semantic variable collections must exist in the target Figma file. Requires the figma-use and figma-generate-library skills."
---

# cc-figma-component — Component Contracts Component Skill

Generate Figma component sets from component contracts. This skill reads a contract, derives component-scoped (Tier 3) tokens, and builds a fully variable-bound component set in Figma.

**Prerequisites — load these skills first:**
- `figma-use` — Plugin API syntax rules (mandatory before every `use_figma` call)
- `figma-generate-library` — Design system workflow and component creation patterns
- `cc-figma-tokens` must have been run — `Primitives` and `Semantic` collections must exist in the target Figma file

**Always pass `skillNames: "cc-figma-component"` when calling `use_figma` as part of this skill.**

---

## Global Rules

### Frame sizing defaults to HUG

**Every frame created by this skill must have both sizing properties set to `'HUG'` immediately after creation — no exceptions.**

```js
node.layoutSizingHorizontal = 'HUG';
node.layoutSizingVertical   = 'HUG';
```

This applies to: the base component frame, every variant duplicate, the Generation Notes frame, and any other frame created during the run. Never rely on Figma's default — it sets new frames to `FIXED` at 100px, which produces portrait-aspect components regardless of padding values. Only deviate from HUG when a slot child's `figma.sizing` is explicitly set to `"fixed"` in the contract. In that case use the contract's `figma.width` and `figma.height` values directly:
   ```js
   if (child.figma?.sizing === 'fixed') {
     node.layoutSizingHorizontal = 'FIXED';
     node.layoutSizingVertical   = 'FIXED';
     node.resize(child.figma.width, child.figma.height);
   }
   ```
   This is the only legitimate exception to the HUG default.

---

## 1. Configuration

Before anything else, read `.component-contracts` from the project root. Never output `FIGMA_ACCESS_TOKEN` in any response.

```
FIGMA_ACCESS_TOKEN=...       # never output this value
FIGMA_FILE_KEY=...           # use for all use_figma calls
TOKENS_DIR=...               # root directory of token files
CONTRACTS_DIR=...            # root directory of contract files
CC_FIGMA_WORKDIR=.claude/tmp/cc-figma-component/<run-id>
```

If `.component-contracts` is missing, stop before any Figma write and ask the user for the Figma file key plus token/contract directories, or create a safe `.component-contracts.example` in a separate setup step. Do not assume a template exists in this repo.

---

## 2. Contract Structure

A component contract is a JSON file at `{CONTRACTS_DIR}/{id}.contract.json`. Read it fully before planning anything.

Key sections used by this skill:

**`tokens`** — defines the component's Tier 3 token bindings, organized by category:
```json
{
  "tokens": {
    "color": {
      "background.primary": "brand.500",
      "text.primary": "neutral.0",
      "border.secondary": "brand.500"
    },
    "spacing": {
      "padding.x.sm": "space.sm",
      "padding.y.sm": "space.xs"
    },
    "typography": {
      "label.size": "textSize.sm",
      "label.weight": "weight.semibold"
    },
    "border": {
      "radius": "radius.md",
      "width": "border.width.sm"
    },
    "motion": {
      "transition": "duration.fast"
    }
  }
}
```

**`props`** — defines the component's variant axes (e.g. `variant`, `size`, `state`)

**`a11y`** — accessibility requirements (ARIA roles, keyboard behavior)

**`platforms`** — target platforms (web, ios, android)

---

## 3. Tier 3 Token Derivation

Component-scoped (Tier 3) tokens are derived from the contract's `tokens` section — they are NOT stored as a separate file. Derive them at runtime using these rules:

### Naming convention

```
--ds-{componentId}-{role}-{qualifier}
```

Where:
- `componentId` — the contract's `id` field (e.g. `button`, `accordion`)
- `role` — the Figma-aligned role name (see role translation table below)
- `qualifier` — derived from the Semantic alias name in the contract value

### Role translation table

| Contract category + key prefix | CSS/Figma role |
|-------------------------------|----------------|
| `color.background.*` | `fill` |
| `color.text.*` | `text` |
| `color.border.*` | `border` |
| `color.focus.*` | `focus` |
| `spacing.*` | `spacing` |
| `typography.*` | `typography` |
| `border.radius` | `border` (as `border-radius`) |
| `border.width` | `border` (as `border-width`) |
| `motion.*` | `transition` |

### Qualifier derivation

The qualifier comes from the Semantic alias value in the contract, with the scale suffix dropped:

```
"background.primary": "brand.500"   →  qualifier = "brand"   →  --ds-button-fill-brand
"background.primary.hover": "brand.600"  →  qualifier = "brand-hover"
"text.primary": "neutral.0"         →  qualifier = "neutral-0"
```

State suffixes (`hover`, `active`, `focus`, `disabled`) are appended after the qualifier:
```
--ds-button-fill-brand-hover
--ds-button-fill-brand-active
```

### Semantic variable lookup

Each Tier 3 token must bind to the corresponding Semantic variable in Figma. Look up the variable by name:

```
contract value "brand.500"  →  Semantic variable named "brand/500"
contract value "space.sm"   →  Semantic variable named "space/sm"
contract value "radius.md"  →  Semantic variable named "radius/md"
```

If a Semantic variable is not found, stop and report the missing variable to the user before proceeding.

---

## 4. Component Set Architecture

Each value of the primary variant prop (e.g. `variant`) becomes a **separate component set**, not a single combined set. Secondary axes (`Size`, `State`) become variant properties within each set.

### Naming convention

```
{ComponentName}/{VariantValue}   →   Button/Primary, Accordion/Multiple
```

- Component name: title case (`Button`, `Accordion`)
- Variant value: title case (`Primary`, `Secondary`)
- Separator: `/`

### Variant axes within each component set

All axes except the primary variant become properties within the component set:

```
Button/Primary:
  Size=Small,  State=Default
  Size=Small,  State=Hover
  Size=Small,  State=Focus
  Size=Small,  State=Active
  Size=Small,  State=Disabled
  Size=Small,  State=Loading
  Size=Medium, State=Default
  ... (18 total variants per set)
```

### Property naming

- Property names: title case, match contract prop names (`Size`, `State`)
- Property values: title case (`Small`, `Medium`, `Large`, `Default`, `Hover`, `Focus`, `Active`, `Disabled`, `Loading`)

### Standard state values

**Always read states from the contract's `states` array** — do not use a hardcoded list. Title-case each value for Figma property values (e.g. `"default"` → `"Default"`). Different components have different state sets — Button has 6 including Loading, Accordion has 5 with no Loading.

---

## 5. Execution Modes

**Default (fast):** Run all phases sequentially without stopping. Present the Phase 0 plan and await approval, then execute Phases 1–7 without interruption. This is the default for all runs.

**Debug mode:** Stop after each phase and await explicit approval before proceeding. Use when diagnosing issues or validating intermediate output. Activate by including "debug mode" in your prompt. Scripts are preserved in debug mode only — clean them up manually when done.

> **Scripts location:** All generated working files MUST be written to a per-run temp directory under `.claude/tmp/cc-figma-component/<run-id>/` — never to the repo root and never to the tracked project `scripts/` directory. Root-level dotfiles (`.mcp-args-phase3.json`, `.phase2-code-raw.js`, etc.) are not cleaned up automatically and will accumulate in the repo.

> **Note:** `.claude/tmp/` is ignored by the repo. Treat generated files there as build cache, not source artifacts.

---

## 6. Workflow

### Phase 0 — Discovery (read-only)

1. Read `.component-contracts` configuration
2. Read the contract file from `CONTRACTS_DIR`
3. Inspect the Figma file — check for existing Semantic/Primitive collections and any existing component with this name
4. Verify that Semantic and Primitive collections exist — if not, stop and tell the user to run `cc-figma-tokens` first
5. Derive the full Tier 3 token list from the contract's `tokens` section
6. Look up every Semantic variable — confirm all exist before proceeding
7. Build the full variant matrix from the contract's `props` section
8. Present a complete plan to the user:
   - Component name and variant count
   - Full Tier 3 token list with Semantic aliases
   - Any missing Semantic variables
9. In debug mode: **Await explicit user approval before proceeding**

### Phase 1 — Page setup

1. Create a dedicated page for the component: `{ComponentName}` (e.g. `Button`, `Accordion`)
2. Switch to that page with `await figma.setCurrentPageAsync(page)`
3. Return the page ID

### Phase 2 — Base component

Build one base component (the Default state of the primary variant) first:

1. Create a Frame with auto-layout, horizontal direction
2. **Immediately after creation, set sizing to HUG using these exact two lines — both are required, one is not enough:**
   ```js
   frame.layoutSizingHorizontal = 'HUG';
   frame.layoutSizingVertical   = 'HUG';
   ```
   Figma defaults new frames to `FIXED` at 100px. Omitting the vertical line produces a portrait-aspect button regardless of padding values. Do this before adding any children or bindings.
3. Apply all structural properties (padding, gap, radius) bound to Semantic variables
4. Add child nodes by reading the contract's `composition.slots` section. Use `childOrder` to determine render order — do not assume a fixed order:
   - Read `composition.slots.{slotName}.childOrder` — this array defines the order children are added to the frame
   - For each child in `childOrder`, read its `figma` hints:
     - `figma.textProp` — create a text node, wire to that component property name
     - `figma.booleanProp` — create an icon placeholder frame, set `visible: false`, wire to that BOOLEAN prop name
     - `figma.position: "trailing"` — this child goes last regardless of other children
     - `figma.rotateOnExpand` — note in Generation Notes that rotation is not variable-bindable
     - `figma.visibleWhen` — note in Generation Notes that visibility is state-driven
   - If no `composition.slots` is defined, fall back to: icon placeholder (hidden), then label text node
   - Icon placeholder frames are always fixed size (20×20 for md), no fill, `visible: false` by default
5. Bind all visual properties to Semantic variables — NO hardcoded values
6. **Run a post-creation sizing check immediately after all children are added.** This corrects any frame the minifier may have dropped HUG assignments for:
   ```js
   // Walk every frame in the component subtree and enforce HUG
   function enforceHug(node) {
     if (node.type === 'FRAME' || node.type === 'COMPONENT') {
       if (node.layoutSizingVertical === 'FIXED') {
         node.layoutSizingHorizontal = 'HUG';
         node.layoutSizingVertical   = 'HUG';
       }
     }
     if ('children' in node) node.children.forEach(enforceHug);
   }
   enforceHug(baseComponent);
   ```
7. Apply `setExplicitVariableModeForCollection` on all nodes recursively
8. Validate: `get_screenshot` — confirm button is wider than tall before proceeding
9. In debug mode: **Await user checkpoint**

### Phase 3 — Variant matrix

For each value of the primary variant prop, create a separate component set:

1. Duplicate the base component for every `Size × State` combination
2. **On every duplicate, reset sizing to HUG using these exact two lines before applying any token overrides:**
   ```js
   duplicate.layoutSizingHorizontal = 'HUG';
   duplicate.layoutSizingVertical   = 'HUG';
   ```
   Duplication may preserve the original's sizing mode but this must be re-set explicitly on every copy without exception.
3. Apply variant-specific token overrides per state (e.g. hover changes fill color)
4. Name each component: `Size=Small, State=Default` etc. (title case, Property=Value)
5. **Before calling `combineAsVariants`**, run a HUG enforcement pass over all variant frames. This is a safety net — catch any frame the agent missed:
   ```js
   variants.forEach(v => {
     v.layoutSizingHorizontal = 'HUG';
     v.layoutSizingVertical   = 'HUG';
   });
   ```
   Any variant still at 100px height after this pass indicates a binding issue, not a sizing issue.
6. Call `combineAsVariants` to create the component set
7. Rename the component set to `{ComponentName}/{VariantValue}` (e.g. `Button/Primary`)
8. **Immediately after `combineAsVariants`**: manually grid-layout the variants and resize to actual bounds:
   ```js
   const COLS = 6; // one column per state
   const GAP = 40;
   const PADDING = 40; // padding inside component set on all sides

   variants.forEach((v, i) => {
     v.x = PADDING + (i % COLS) * (v.width + GAP);
     v.y = PADDING + Math.floor(i / COLS) * (v.height + GAP);
   });

   // Resize to actual content bounds — never guess, always calculate
   const maxRight = Math.max(...variants.map(v => v.x + v.width));
   const maxBottom = Math.max(...variants.map(v => v.y + v.height));
   componentSet.resize(maxRight + PADDING, maxBottom + PADDING);
   ```
9. Repeat for each variant value (Primary, Secondary, Ghost, Destructive)
10. Validate: `get_screenshot` — confirm buttons are wider than tall at all sizes
11. In debug mode: **Await user checkpoint**

### Phase 4 — Variable binding pass

For every variant node:
1. Bind fill properties to the correct Semantic color variable
2. Bind stroke properties to the correct Semantic color variable
3. Bind padding/gap to the correct Semantic spacing variable
4. Bind corner radius to the correct Semantic radius variable
5. Call `setExplicitVariableModeForCollection` on every node and all children recursively after binding
6. Validate: `get_screenshot` — confirm colors resolve correctly (no ghosted/unresolved variables)

### Phase 5 — Component properties

1. Define component properties matching the contract's `props` section:
   - **TEXT** `label` — linked to the Label text node's `characters` on ALL variants including Loading. Never substitute a hardcoded string like "Saving" — the label text is always driven by the `label` prop value.
   - **BOOLEAN** `iconStart` — linked to the Icon placeholder's `visible` property via `componentPropertyReferences`. Default `false` (hidden). This is the correct way to toggle icon slot visibility.
   - **BOOLEAN** `iconOnly` — defined on the component set. Not linked to layout automatically (see Known Constraints).
   - **BOOLEAN** `fullWidth` — defined on the component set. Not linked to layout automatically (see Known Constraints).
2. Do NOT add `disabled` or `loading` as BOOLEAN props — these are handled exclusively as variant states
3. Do NOT add `INSTANCE_SWAP` for icons unless a real icon component exists in the file
4. Validate: confirm property panel matches contract props

### Phase 6 — Canvas annotations

Before final validation, create a `⚠️ Generation Notes` frame on the component page documenting everything the agent assumed, flagged, or couldn't resolve. This makes the output self-documenting for anyone opening the file.

The frame should be placed below all component sets, clearly separated. Use a light yellow fill (`#FFFBEB`), auto-layout vertical direction, and set sizing explicitly:
```js
notesFrame.layoutSizingHorizontal = 'HUG';
notesFrame.layoutSizingVertical   = 'HUG';
```
This ensures the frame expands to contain all note text rather than clipping at a fixed height. Add a title text node followed by individual note entries.

**Always include a note for each of the following if applicable:**

| Condition | Note to write |
|-----------|---------------|
| `focus/default` same color as a variant fill | "Focus ring color conflict: `focus/default` may be invisible on [variant] fill. Define a `focus/onBrand` Semantic token and re-run." |
| Loading state has no spinner component | "State=Loading: No spinner component found. Label text preserved. Add a spinner instance and wire to `iconStart`, or create a dedicated loading indicator." |
| Any token bound to Primitives instead of Semantic | "Token gap: [token name] has no Semantic alias. Bound to Primitive directly. Add a Semantic alias to align with the token architecture." |
| `fullWidth` or `iconOnly` not wired to layout | "`fullWidth` / `iconOnly` are defined as component properties but do not drive layout automatically. See known constraints." |
| `iconEnd` prop present in contract | "`iconEnd` is not modeled in Figma — no trailing icon slot created. Add a second icon placeholder frame and wire to an `iconEnd` BOOLEAN if needed." |
| Any contract prop not modeled in Figma | "[prop name] from contract not modeled in Figma: [reason]." |
| Any assumption made during generation | Document it explicitly. |

If there are no notes, create the frame anyway with the text "No issues — all tokens resolved, all props wired."

---

### Phase 7 — Final validation

1. `get_metadata` — confirm structure: variant count, property definitions, hierarchy
2. `get_screenshot` — visual check: buttons are wider than tall at all sizes, no clipped text, no overlapping elements, correct spacing, no cropped variants
3. Return structured summary:
```json
{
  "component": "Button",
  "componentSets": [
    { "name": "Button/Primary", "variantCount": 18, "id": "..." },
    { "name": "Button/Secondary", "variantCount": 18, "id": "..." },
    { "name": "Button/Ghost", "variantCount": 18, "id": "..." },
    { "name": "Button/Destructive", "variantCount": 18, "id": "..." }
  ],
  "propertiesDefined": ["Size", "State", "label", "iconStart", "iconOnly", "fullWidth"],
  "annotations": ["list of notes written to canvas"],
  "tier3Tokens": [...],
  "pageId": "..."
}
```

4. **Cleanup** — always run this at the end of every run, successful or not. The only exception is debug mode.

   **The scripts are disposable.** Do not suggest keeping, reusing, or regenerating them. Do not instruct the user to run terser or rewrite invoke files. Every run generates a fresh set from scratch. Treat them as build cache, not source artifacts.

   Delete only the current run temp directory and any accidental working files written to the repo root:
   ```bash
   npx rimraf "$CC_FIGMA_WORKDIR"
   rm -f .mcp-*.json .mcp-*.txt .*-phase*.js .*-phase*.json .*-args*.json .*-code*.js .*-code*.json .tmp-*.js
   ```
   In debug mode, leave all files in place for inspection.

---

## 7. Variable Binding Rules

- Components bind **exclusively to Semantic variables** — never directly to Primitives
- Every visual property with a corresponding token MUST be variable-bound — no hardcoded values
- `setExplicitVariableModeForCollection` MUST be called on every node AND all children recursively after any variable binding operation
- `setBoundVariable` on text nodes requires the font to be loaded first: `await figma.loadFontAsync({family, style})`
- `cornerRadius` does NOT support `setBoundVariable` directly — use individual corners: `topLeftRadius`, `topRightRadius`, `bottomLeftRadius`, `bottomRightRadius`
- **Always use `setSharedPluginData` / `getSharedPluginData` — never `setPluginData` / `getPluginData`**. The non-shared version uses a debug UUID as the plugin identifier that changes on each tool execution, making stored data permanently unretrievable and causing file bloat. Always use the `component_contracts` namespace:
  ```js
  // CORRECT
  node.setSharedPluginData('component_contracts', 'dsb_key', 'component/button/base');
  node.getSharedPluginData('component_contracts', 'dsb_key');

  // WRONG — UUID changes per execution, data becomes orphaned
  node.setPluginData('dsb_key', 'component/button/base');
  ```

---

## 8. Known Constraints

- **Frame sizing defaults to FIXED at 100px** — Figma sets new frames to `FIXED` sizing at 100px height. You must set both lines explicitly on every frame, every variant duplicate, and the Generation Notes frame:
  ```js
  node.layoutSizingHorizontal = 'HUG';
  node.layoutSizingVertical   = 'HUG';
  ```
  Setting only horizontal and omitting vertical is the most common cause of portrait-aspect buttons. There is no shorthand — both lines are always required.

- **Letter-spacing** — cannot be bound to a variable (em units incompatible with Figma FLOAT). Set as a fixed pixel value derived from the token's raw value.

- **combineAsVariants** does not auto-layout — variants stack at (0,0). Always manually grid-layout immediately after. Always resize the component set to actual content bounds using `Math.max` over all variant positions + sizes + padding. Never guess the resize dimensions.

- **`layoutSizingHorizontal/Vertical = 'FILL'`** must be set AFTER `parent.appendChild(child)` — setting before throws.

- **Ghost mode** — always call `setExplicitVariableModeForCollection` after every binding operation, on the node AND all children recursively. Skipping this causes variables to appear unresolved.

- **Variant count cap** — if Size × State > 30 variants per component set, raise this with the user before creating. Consider splitting into sub-components.

- **Focus ring color conflict** — the skill does NOT make judgment calls about focus ring color. Read the contract's `color.focus.*` tokens and use whatever Semantic variable is defined there for ALL variants. If `focus/default` is the same color as a variant's fill, flag this in the Generation Notes frame and suggest the user define a `focus/onBrand` Semantic token. Do not substitute `neutral/0` or any other color on the skill's own initiative.

- **`fullWidth` and `iconOnly` cannot drive layout automatically** — the Figma Plugin API's `componentPropertyReferences` only supports `visible`, `characters`, and `mainComponent`. It does not support linking a boolean to `layoutSizingHorizontal` or toggling between icon-only and full layouts. These props are defined for spec/Code Connect purposes. Document this limitation for consumers — layout changes require manual variant creation or a follow-up plugin.

- **Figma plugin sandbox — `atob` is undefined** — the plugin runtime has no native base64 decoding. Do not use `atob` or `btoa` in plugin scripts. If a script exceeds the 20k character limit and must be chunked, use a base64 polyfill or split the logic into multiple sequential `use_figma` calls instead.

- **Rotation values are always in degrees, never radians** — the Figma Plugin API's `node.rotation` property accepts degrees. Always pass degree values directly from the contract (e.g. `-90`). Never convert to radians (`-Math.PI/2`). Passing radians produces values like `-1.57°` in Figma's UI which looks wrong even though the visual result is correct. The contract's `expandedRotation` and `defaultRotation` fields are always in degrees.

- **Figma plugin sandbox — `eval` is blocked** — avoid dynamic code execution by default. If the script length forces a chunked runner and there is no smaller-step alternative, `new Function(code)()` may be used only with code generated by this skill in the current run temp directory. Never pass user-provided text, network content, arbitrary repo files, or Figma node text into `new Function`.

- **Icon slot visibility** — the icon placeholder frame must be hidden by default (`visible: false`) and wired to a BOOLEAN component property (`iconStart`) via `componentPropertyReferences` with type `visible`. Never leave the icon slot always-visible — it will appear as an empty box on every variant that doesn't use an icon.
