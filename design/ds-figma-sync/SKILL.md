---
name: ds-figma-sync
description: |
  DS Figma Sync — verifies 1:1 parity between Swift code tokens/components and Figma DS file, finds mismatches, and fixes them. Covers: color values, spacing values, radius values, text styles, effect styles, component sets, variant counts, iOS code syntax, variable scopes. Use this skill ALWAYS when syncing code↔Figma, after adding new tokens or components, or for periodic DS health checks. Trigger: "figma sync", "sync ds", "figma parity", "проверь фигму", "синхронизируй", "code figma match", "ds health check", "токены совпадают?", "компоненты в фигме".
---

# DS Figma Sync

You verify and fix 1:1 parity between the Hexbound Swift design system and the Figma DS file.

**Figma DS file:** `uDjXIz7CdJxcEOI5jCBcjY`
**Figma Screens file:** `PalemJ36B97ZdC0cd8jzv4`

Verify these file keys with the user or current Figma context before making changes; they are project defaults, not proof that the active file is still current.

## Prerequisites

1. Load `figma-use` skill BEFORE any `use_figma` calls
2. Read Swift source files for ground truth values
3. All operations on Figma DS file only — NEVER modify Screens file in this skill

## Phase 1: Token Value Parity

### 1a. Color Tokens

Extract ALL `static let` color tokens from `DarkFantasyTheme.swift`, convert to hex, then compare with Figma Primitives collection:

```js
// In use_figma — get all Primitives with hex values
const collections = await figma.variables.getLocalVariableCollectionsAsync();
const primCol = collections.find(c => c.name === 'Primitives');
const modeId = primCol.modes[0].modeId;
const results = [];
for (const varId of primCol.variableIds) {
  const v = await figma.variables.getVariableByIdAsync(varId);
  const val = v.valuesByMode[modeId];
  if (typeof val === 'object' && 'r' in val) {
    const hex = '#' + [val.r, val.g, val.b].map(c => Math.round(c * 255).toString(16).padStart(2, '0')).join('').toUpperCase();
    results.push({ name: v.name, hex, codeSyntax: v.codeSyntax?.iOS });
  }
}
return results;
```

**For each Swift token:**
- ✅ Figma has matching variable with same hex → PASS
- ❌ Figma hex differs → FIX Figma value
- ❌ Figma variable missing → CREATE in Primitives + alias in Color collection
- ❌ Swift token missing from Figma → FLAG for review (maybe deprecated)

### 1b. Spacing Tokens

Compare `LayoutConstants.swift` spacing/radius values with Figma Spacing collection:

**Swift tokens to check:**
- `space2XS`(2), `spaceXS`(4), `spaceSM`(8), `spaceMS`(12), `spaceMD`(16), `spaceLG`(24), `spaceXL`(32), `space2XL`(48)
- `radiusXS`(3), `radiusSM`(6), `radiusMD`(8), `radiusLG`(12), `radiusXL`(16), `radius2XL`(22)

### 1c. iOS Code Syntax

Every Figma variable MUST have correct `codeSyntax.iOS`:
- Colors: `DarkFantasyTheme.{camelCaseName}` (e.g. `DarkFantasyTheme.bgPrimary`)
- Spacing: `LayoutConstants.{camelCaseName}` (e.g. `LayoutConstants.spaceMD`)
- Radius: `LayoutConstants.{camelCaseName}` (e.g. `LayoutConstants.radiusLG`)

**Format is camelCase, NOT snake_case.** If any variable has wrong format → FIX.

## Phase 2: Text Style Parity

Compare Figma text styles with Swift font tokens:

| Swift Token | Font | Size | Figma Style Expected |
|---|---|---|---|
| `.cinematicTitle` | Oswald | 40 | `Heading/Cinematic Title` |
| `.title` | Oswald | 28 | `Heading/Title` |
| `.section` | Oswald | 22 | `Heading/Section` |
| `.cardTitle` | Oswald | 18 | `Heading/Card Title` |
| `.buttonLabel` | Oswald | 18 | `Heading/Button Label` |
| `.body` | Inter | 16 | `Body/Body` |
| `.uiLabel` | Inter | 14 | `Body/UI Label` |
| `.caption` | Inter | 12 | `Body/Caption` |
| `.badge` | Inter Bold | 11 | `Body/Badge` |

Use `get_metadata` to verify all 9 text styles exist with correct font/size/weight.

## Phase 3: Effect Style Parity

Verify 4 effect styles exist:
- `Shadow/Card` — bgAbyss 0.4 radius 6 y:3
- `Shadow/Modal` — bgAbyss 0.8 radius 32 y:8
- `Shadow/Gold Glow` — goldGlow 0.4 radius 10 y:4
- `Shadow/Danger Glow` — danger 0.25 radius 8 y:4

## Phase 4: Component Set Parity

Cross-reference Swift components with Figma component pages:

### Expected mapping (from CLAUDE.md):

| Figma Page | Figma Component Sets | Swift Source |
|---|---|---|
| Buttons | Button, Compact Button, Combat Button, Special Button, Navigation Button, Wager Button | ButtonStyles.swift |
| Cards | Card (9 variants) | CardStyles.swift |
| Dividers | Divider (3 variants) | CardStyles.swift + OrnamentalStyles.swift |
| Tab Switcher | Tab Switcher (2 variants) | TabSwitcher.swift |
| Progress Bars | Progress Bar (15 variants) | HPBarView, XPBarView, StaminaBarView |
| Badges & Pills | 11 sets | WidgetPill, CardLevelBadge, StatPointsBadge, etc. |
| Currency Display | Currency Display (4 variants) | CurrencyDisplay.swift |
| ... | ... | ... |

**For each Swift component in `Views/Components/`:**
- ✅ Has matching Figma component set → PASS
- ❌ No Figma component → FLAG (needs Figma creation)
- ❌ Figma variant count differs from Swift states → FLAG

**For each Figma component set:**
- ✅ Has matching Swift source → PASS
- ❌ No Swift source → FLAG (orphaned Figma component or inline code)

## Phase 5: Variable Binding Audit

Sample 5 Figma component sets and verify their internal nodes use variable bindings (not raw values):

```js
// Check a component set for unbound fills
const node = await figma.getNodeByIdAsync('COMPONENT_SET_ID');
const violations = [];
function check(n) {
  if (n.type === 'TEXT' && !n.textStyleId) violations.push(`${n.name}: no text style`);
  if (n.fills?.length && !n.boundVariables?.fills) {
    // Check if it's a sub-layer of ornamental component (legitimate)
    if (n.parent?.type !== 'COMPONENT') violations.push(`${n.name}: unbound fill`);
  }
  if (n.children) n.children.forEach(check);
}
check(node);
return violations;
```

## Output Format

```
## DS Figma Sync Report — [date]

### Token Parity
- Colors: [X]/[Y] match ✅ | [Z] mismatches ❌
- Spacing: [X]/[Y] match ✅
- Radius: [X]/[Y] match ✅
- iOS Code Syntax: [X]/[Y] correct ✅

### Text Styles: [X]/9 match ✅
### Effect Styles: [X]/4 match ✅

### Component Parity
- Swift → Figma: [X] matched, [Y] missing in Figma
- Figma → Swift: [X] matched, [Y] orphaned in Figma
- Variant count mismatches: [list]

### Variable Bindings: [X] components sampled, [Y] violations

### Actions Taken
[list of fixes applied]

### Remaining Issues
[list of issues that need manual intervention]
```

## Fixing Mismatches

**Priority order:**
1. **Token values** — fix Figma to match Swift (Swift = source of truth)
2. **iOS code syntax** — fix in Figma
3. **Missing variables** — create in Figma Primitives + Color collections
4. **Missing components** — flag for `ds-extract-component` skill
5. **Variable bindings** — fix in Figma component internals

**Swift is ALWAYS the source of truth.** When values differ, Figma gets updated to match Swift, never the other way around.
