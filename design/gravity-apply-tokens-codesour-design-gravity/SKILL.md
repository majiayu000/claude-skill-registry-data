---
name: gravity-apply-tokens
description: Apply all design system tokens (components, typography, colors, spacing) when transposing a Gravity design to Figma. Must be followed every time a Gravity screen is built or updated in Figma.
---

# Gravity — Apply Design System Tokens on Transposition

**Load this skill every time you build or update a Gravity screen in Figma.**
Never hard-code hex values, pixel sizes, or font properties — always bind library tokens.

Also load the `figma:figma-use` skill (use the Skill tool) before any `use_figma` call.

---

## File Keys

| File | Key |
|------|-----|
| Design System (Ant Design for Gravity) | `uR6CBOh0Y7dUQvH30SyD0P` |
| SSO screens | `AfqsPa76Xixhkq7Bx7VdsA` |

---

## Required Checklist — Every Transposition

Run these steps in order. Do not skip any.

### 1. Discover before building

Before placing a single node:
- Call `get_metadata` on the target page to understand what already exists.
- Call `get_screenshot` if visuals help verify current state.
- Never hard-code values from memory — always verify keys are still valid.

### 2. Import components from the library

Every UI element must be an instance from `uR6CBOh0Y7dUQvH30SyD0P`. Never draw primitives.

```js
// Always import by key, never recreate locally
const componentSet = await figma.importComponentSetByKeyAsync('COMPONENT_KEY');
const variant = componentSet.children.find(c => c.name.includes('Type=Primary'))
  || componentSet.defaultVariant;
const instance = variant.createInstance();
```

See CLAUDE.md for the full React → Figma component key map.

### 3. Apply typography text styles

Never set `fontSize`, `fontName`, or `fontWeight` directly on text nodes.
Always import the text style from the library and apply via `textStyleId`.

```js
// Discover styles on the Typography page of the DS file
const style = await figma.importStyleByKeyAsync('TEXT_STYLE_KEY');
textNode.textStyleId = style.id;
```

**Typography text style keys** (from DS file `uR6CBOh0Y7dUQvH30SyD0P`, page `Typography`):

| Style | Usage | Key |
|-------|-------|-----|
| Heading / H1 | Page titles | *(discover via search_design_system or inspect DS file)* |
| Heading / H2 | Section titles | *(discover)* |
| Heading / H3 | Card titles | *(discover)* |
| Body / Regular | Body text | *(discover)* |
| Body / SM | Secondary text | *(discover)* |
| Label / MD | Form labels | *(discover)* |

> **How to discover**: Run `search_design_system` with terms `heading`, `body`, `label`, `caption` and `includeStyles: true`. Or inspect an existing Gravity screen's `textStyleId` values.

### 4. Bind color variables

Never use hex fills directly. Always bind to library color variables.

```js
// Import variable then bind to fill
const colorVar = await figma.variables.importVariableByKeyAsync('COLOR_VAR_KEY');
const paint = figma.variables.setBoundVariableForPaint(
  { type: 'SOLID', color: { r: 0, g: 0, b: 0 } },
  'color',
  colorVar
);
node.fills = [paint];
```

**Color variable keys** (from DS collection `1. Color`):

| Token | Value | Usage |
|-------|-------|-------|
| Primary / `colorPrimary` | `#3E00FB` | Brand blue, CTAs |
| Secondary / `colorError` | `#FF4A1C` | Alerts, danger |
| `colorBgLayout` | `#F5F5F5` | Page background |
| `colorBgContainer` | `#FFFFFF` | Card background |
| `colorTextBase` | `rgba(0,0,0,0.88)` | Primary text |
| `colorTextSecondary` | `rgba(0,0,0,0.45)` | Secondary/placeholder text |

> **How to discover**: Run `search_design_system` with terms `color`, `background`, `text`, `primary`, `error` and `includeVariables: true`. Or inspect bound variables on an existing screen node.

### 5. Bind spacing variables

Never set `paddingTop`, `paddingBottom`, `paddingLeft`, `paddingRight`, or `itemSpacing` as raw numbers.
Always use `setBoundVariable`.

```js
const spacingVar = await figma.variables.importVariableByKeyAsync('SPACING_KEY');
node.setBoundVariable('paddingTop', spacingVar);
node.setBoundVariable('paddingBottom', spacingVar);
node.setBoundVariable('paddingLeft', spacingVar);
node.setBoundVariable('paddingRight', spacingVar);
node.setBoundVariable('itemSpacing', spacingVar);
```

**Spacing variable keys** (from DS collection `2. Dimensions`):

| Token | Value | Key |
|-------|-------|-----|
| `paddingXXS` / `sizeXXS` | 4px  | `1451c35b2cc8041d3ecd2975de517a9d533e426c` |
| `paddingXS`  | 8px  | `ff058f97c20808f7e932f1cdcb70153b4aec6fe9` |
| `paddingSM`  | 12px | `f1a4df654d0df4aafef1d32570bbc9b5a883c588` |
| `padding`    | 16px | `cea786bc0257366124ab4bac48eb65b18cbfa84e` |
| `paddingMD`  | 20px | `3b89ab44e6a9bbe5d28a59220075dd1b0996851d` |
| `paddingLG`  | 24px | `331209660c6df3f2a8c16e73e4cd62f01c5e7463` |
| `paddingXL`  | 32px | `bd4a10993d4e661fe90a61522ddb569946c916c9` |
| `sizeXXL`    | 48px | `ba87c63d9f87989675083558082f8227e3679a95` |

### 6. Validate after each section

After building or modifying each section:
1. `get_screenshot` on the section node — not only the full frame.
2. Confirm no placeholder text remains.
3. Confirm fills, spacing, and typography are visually correct.
4. Confirm each node's component is linked to the library (not a detached local copy).

### 7. Final full-screen screenshot

After all sections are complete, take a `get_screenshot` of the full wrapper frame and verify against the HTML prototype.

---

## Import boilerplate (copy-paste for each script)

```js
// ── Spacing tokens ──────────────────────────────────────────────────────────
const SPACING_KEYS = {
  xxs: '1451c35b2cc8041d3ecd2975de517a9d533e426c', // 4px
  xs:  'ff058f97c20808f7e932f1cdcb70153b4aec6fe9', // 8px
  sm:  'f1a4df654d0df4aafef1d32570bbc9b5a883c588', // 12px
  md_padding: 'cea786bc0257366124ab4bac48eb65b18cbfa84e', // 16px
  md:  '3b89ab44e6a9bbe5d28a59220075dd1b0996851d', // 20px
  lg:  '331209660c6df3f2a8c16e73e4cd62f01c5e7463', // 24px
  xl:  'bd4a10993d4e661fe90a61522ddb569946c916c9', // 32px
  xxl: 'ba87c63d9f87989675083558082f8227e3679a95', // 48px
};
const sv = {};
for (const [k, key] of Object.entries(SPACING_KEYS)) {
  sv[k] = await figma.variables.importVariableByKeyAsync(key);
}
const bsv = (node, prop, variable) => { if (variable) node.setBoundVariable(prop, variable); };

// ── Color tokens ─────────────────────────────────────────────────────────────
// Discover at runtime via search_design_system or inspect existing screens.
// Import with: await figma.variables.importVariableByKeyAsync(colorVarKey)
// Bind with:   node.fills = [figma.variables.setBoundVariableForPaint(basePaint, 'color', colorVar)]

// ── Text styles ───────────────────────────────────────────────────────────────
// Discover at runtime via search_design_system (includeStyles: true) or inspect existing screens.
// Import with: await figma.importStyleByKeyAsync(styleKey)
// Apply with:  textNode.textStyleId = style.id
```

---

## Common mistakes to avoid

| Wrong | Correct |
|-------|---------|
| `node.paddingTop = 24` | `bsv(node, 'paddingTop', sv.lg)` |
| `node.itemSpacing = 8` | `bsv(node, 'itemSpacing', sv.xs)` |
| `node.fills = [{ type:'SOLID', color:{r:0.243,...} }]` | Import color var, use `setBoundVariableForPaint` |
| `textNode.fontSize = 16` | Import text style, set `textNode.textStyleId` |
| `figma.createText()` with manual font | Import style from DS |
| `figma.createRectangle()` for a button | `importComponentSetByKeyAsync` + `createInstance()` |
| Set `layoutSizingHorizontal='FILL'` before `appendChild` | Append first, then set FILL |
| `counterAxisSizingMode = 'HUG'` | `counterAxisSizingMode = 'AUTO'` |
| `color: { r, g, b, a }` in fills | `opacity` property on the fill object, color has only `{r,g,b}` |
