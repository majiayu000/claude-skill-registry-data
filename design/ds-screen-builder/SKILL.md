---
name: ds-screen-builder
description: |
  DS Screen Builder — builds app screens in Figma Screens file using ONLY DS components, tokens, and styles. Reads Swift view code, maps UI to DS components, assembles frame-by-frame in Figma with correct auto-layout, variable bindings, and component instances. Use this skill for building ANY screen in Figma from Swift code. Trigger: "build screen", "собери экран", "screen builder", "экран в фигме", "figma screen", "добавь экран", "new screen figma", "собери все экраны".
---

# DS Screen Builder

> **MANDATORY PREREQUISITE:** Read `docs/07_ui_ux/FIGMA_SCREEN_RULES.md` BEFORE any screen creation.
> That document contains the complete rules, variable IDs, style keys, and audit script.
> **This skill SUPPLEMENTS those rules — it does NOT replace them.**

You build Hexbound app screens in the **Figma Screens file** using ONLY components and tokens from the **Figma DS file**.

**Screens file:** `PalemJ36B97ZdC0cd8jzv4`
**DS file:** `uDjXIz7CdJxcEOI5jCBcjY`
**DS library key:** `lk-1e3d5b13e106c557d2ec56c3ac95231374bc21a6136997e732d7a804ec4d86c11297eee6bd376c1bc936574dd6ba4ddea2380be439e8701a5408d7daaff18fb4`

Verify these keys against the current Figma context before writing; do not build into a stale Screens or DS file.

## HARD RULES (violate any = delete and rebuild)

1. **ZERO hardcoded colors** — every fill/stroke/text color bound to Color collection variable
2. **ZERO unstyled text** — every TEXT node has `textStyleId` from published library
3. **ZERO fake components** — buttons, cards, badges, dividers MUST be DS instances
4. **ZERO default placeholder text** — every instance text overridden to match Swift code
5. **ZERO raw spacing** — all gap/padding/radius bound to Spacing collection variables
6. **Post-creation audit MUST PASS** before proceeding to next screen

## Prerequisites

1. Load `figma-use` skill BEFORE any `use_figma` calls
2. Read `docs/07_ui_ux/FIGMA_SCREEN_RULES.md` for variable IDs and style keys
3. Read the Swift view source for the screen you're building
4. All operations on **Screens file only** — NEVER create components here

## Phase 1: Read Swift Code and Build Truth Table (CRITICAL)

Before writing a SINGLE line of Figma code:

1. **Read the full Swift source file** — every line, every modifier
2. **Extract the truth table:**

```
| Swift Code                                    | Figma Equivalent                           |
|-----------------------------------------------|--------------------------------------------|
| Text("TUTORIAL")                              | Text characters = "TUTORIAL"               |
| .font(DarkFantasyTheme.title)                 | textStyleId → Heading/Title (key: ce24...) |
| .foregroundStyle(DarkFantasyTheme.textPrimary) | fill bound to color/text/primary           |
| .panelCard()                                  | Card / Panel instance from DS              |
| Button("Continue").buttonStyle(.primary)       | Button / Primary Default instance from DS  |
| .padding(.horizontal, LayoutConstants.spaceMD) | paddingLeft/Right bound to spacing/md      |
```

3. **List ALL DS components needed** — search in DS file for their variant keys

**DO NOT PROCEED until truth table is complete.**

## Phase 2: Discover and Cache DS Component Keys

```javascript
// In DS file (uDjXIz7CdJxcEOI5jCBcjY) — get variant keys
const page = figma.root.children.find(p => p.name === 'Buttons');
await figma.setCurrentPageAsync(page);
const compSet = page.findOne(n => n.type === 'COMPONENT_SET' && n.name === 'Button');
const keys = {};
for (const v of compSet.children) {
  keys[v.name] = v.key;
}
return JSON.stringify(keys, null, 2);
```

**Cache ALL needed keys before switching to Screens file.**

## Phase 3: Build Screen Using MANDATORY Helpers

Every screen script MUST use the helper functions from `FIGMA_SCREEN_RULES.md` Rule 8.

**Copy the entire helper block** into every `use_figma` call that creates a screen. This includes:
- `TEXT_STYLE_KEYS` dictionary
- `EFFECT_STYLE_KEYS` dictionary
- `getTextStyle()` / `getEffectStyle()` functions
- `makeText()` function — creates text with style + color binding
- `getColorVar()` / `bindFill()` functions
- `bindSpacing()` function
- `makeScreenFrame()` function
- `importComponent()` / `addToParent()` functions

### Screen frame template:

```javascript
// Create screen
const screen = await makeScreenFrame('Tutorial');

// Import DS components
const ornTitle = await importComponent('ORNAMENTAL_TITLE_VARIANT_KEY');
addToParent(screen, ornTitle);
// Override text inside instance:
const titleText = ornTitle.findOne(n => n.type === 'TEXT');
if (titleText) {
  await figma.loadFontAsync(titleText.fontName);
  titleText.characters = 'TUTORIAL'; // From Swift: OrnamentalTitle("Tutorial")
}

// Custom text (not a component)
const label = await makeText('1/3 STEPS COMPLETE', 'caption', 'color/text/tertiary');
screen.appendChild(label);

// Card section
const card = await importComponent('CARD_PANEL_VARIANT_KEY');
addToParent(screen, card);

// Button
const btn = await importComponent('BUTTON_PRIMARY_DEFAULT_KEY');
addToParent(screen, btn);
// Override button text:
const btnText = btn.findOne(n => n.type === 'TEXT');
if (btnText) {
  await figma.loadFontAsync(btnText.fontName);
  btnText.characters = 'BEGIN QUEST';
}
```

## Phase 4: Override ALL Instance Text

**DEFAULT TEXT IS NEVER ACCEPTABLE.**

After placing every instance, find and override its text nodes:

```javascript
async function overrideText(instance, defaultSubstring, newText) {
  const textNodes = instance.findAll(n => n.type === 'TEXT');
  for (const t of textNodes) {
    if (t.characters.toUpperCase().includes(defaultSubstring.toUpperCase())) {
      await figma.loadFontAsync(t.fontName);
      t.characters = newText;
    }
  }
}

// Examples:
await overrideText(ornTitle, 'ARENA OF CHAMPIONS', 'TUTORIAL');
await overrideText(button, 'BUTTON LABEL', 'BEGIN QUEST');
await overrideText(statPill, 'ATK', 'DMG DEALT');
await overrideText(statPill, '1,240', '3,847');
```

## Phase 5: MANDATORY Post-Creation Audit

**Run this IMMEDIATELY after creating each screen. MUST PASS.**

```javascript
async function auditScreen(screenId) {
  const node = await figma.getNodeByIdAsync(screenId);
  const failures = [];
  let totalText = 0, styledText = 0;
  let totalFills = 0, boundFills = 0;
  let instanceCount = 0;

  function walk(n) {
    if (n.type === 'INSTANCE') { instanceCount++; return; }
    if (n.type === 'TEXT') {
      totalText++;
      if (n.textStyleId && n.textStyleId !== '') styledText++;
      else failures.push(`UNSTYLED TEXT: "${n.characters.substring(0,30)}" (${n.id})`);

      // Check for default placeholder text
      const defaults = ['ARENA OF CHAMPIONS', 'BUTTON LABEL', '1,240', 'ATK'];
      for (const d of defaults) {
        if (n.characters.includes(d)) {
          failures.push(`DEFAULT TEXT: "${n.characters.substring(0,30)}" (${n.id})`);
        }
      }
    }
    if (n.fills && Array.isArray(n.fills) && n.fills.length > 0 && n.fills.some(f => f.visible !== false)) {
      totalFills++;
      if (n.boundVariables?.fills?.length > 0) boundFills++;
      else {
        const f = n.fills[0];
        const hex = f.color ? `#${Math.round(f.color.r*255).toString(16).padStart(2,'0')}${Math.round(f.color.g*255).toString(16).padStart(2,'0')}${Math.round(f.color.b*255).toString(16).padStart(2,'0')}` : 'gradient';
        failures.push(`HARDCODED FILL: ${n.type}:"${n.name}" → ${hex} (${n.id})`);
      }
    }
    if ('children' in n) n.children.forEach(walk);
  }
  walk(node);

  const textPct = totalText > 0 ? Math.round(styledText/totalText*100) : 100;
  const fillPct = totalFills > 0 ? Math.round(boundFills/totalFills*100) : 100;
  const pass = failures.length === 0;

  return { screen: node.name, textScore: `${textPct}%`, fillScore: `${fillPct}%`, instances: instanceCount, pass, failures: failures.slice(0, 15) };
}

const result = await auditScreen('SCREEN_ID');
if (!result.pass) return 'AUDIT FAILED:\\n' + result.failures.join('\\n');
return 'AUDIT PASSED: Text ' + result.textScore + ', Fills ' + result.fillScore;
```

### Acceptance Criteria:

| Metric | Required |
|---|---|
| Text styled % | **100%** |
| Fill bound % | **100%** (screen root allowed as exception) |
| Default text remaining | **0** |
| Instances as % of children | **≥ 50%** |

**If audit fails → FIX ALL FAILURES before proceeding to next screen.**

## Phase 6: Visual Verification

After audit passes:

1. `get_screenshot` of the screen
2. Compare visually against Swift code / iOS simulator
3. Verify: all text readable, all states visually distinct, layout correct
4. If anything looks wrong → investigate and fix → re-audit

## Handling Missing Components

If a screen element has no matching DS component:

1. **STOP building the screen**
2. Note the missing component
3. Use `ds-extract-component` skill to create it in DS first
4. Publish the library
5. Then return and continue building the screen

**NEVER create components in the Screens file. NEVER fake a component with frames.**

## Quick Reference: Style Keys

### Text Styles (importStyleByKeyAsync):

| Token | Key |
|---|---|
| cinematicTitle (40) | `9c11a0c58dae12b273c8a237e9b0b98450eaebf1` |
| title (28) | `ce245f83ac721aeb90db5258e80bedcfaa4e8cae` |
| section (22) | `460e0abe0ddacaefa8b6f698fb61f27a04af7759` |
| cardTitle (18) | `24f763b8b7ec47532b5c5f77d77375124f082210` |
| buttonLabel (18) | `197938eeaef9704d5ddf2e6efe8c6986d62b6b7f` |
| buttonLabelCompact (16) | `e5461cffd767dc18fc4ea03d3d5fcf7bff1f289c` |
| body (16) | `fef6dd502465059c68ca8041a45afbee2ed690f1` |
| uiLabel (14) | `b147294861bbd172aee02c25d4dd88c13c3a6b80` |
| caption (12) | `1d94244a59a22997f3f590d3ad9209b702a7a71d` |
| badge (11 bold) | `71f8c0a0806a1197ef63e77a0a591a5bfeac5a95` |

### Effect Styles:

| Style | Key |
|---|---|
| Shadow/Card | `492a984d82c5f4febf620e4ff807e01a21521209` |
| Shadow/Modal | `1452cba48fb12135a3e248ea91e548c38c64133e` |
| Shadow/Gold Glow | `765a5605d7606710559e71a6a24e473e70461c1c` |
| Shadow/Danger Glow | `35769d68a9327b01327c68baca2442868f16b19b` |

### Common Color Variables (use with bindFill/getColorVar):

| Swift Token | Variable Name |
|---|---|
| bgPrimary | `color/bg/primary` |
| bgSecondary | `color/bg/secondary` |
| bgElevated | `color/bg/elevated` |
| textPrimary | `color/text/primary` |
| textSecondary | `color/text/secondary` |
| textDisabled | `color/text/disabled` |
| gold | `color/gold/default` |
| textGold | `color/text/gold` |
| textOnGold | `color/text/on-gold` |
| danger | `color/feedback/danger` |
| success | `color/feedback/success` |
| borderSubtle | `color/border/subtle` |
| borderGold | `color/border/gold` |
| bgModal | `color/bg/modal` |

### Spacing Variables (use with bindSpacing):

| Swift Token | Variable Name |
|---|---|
| space2XS (2) | `spacing/2xs` |
| spaceXS (4) | `spacing/xs` |
| spaceSM (8) | `spacing/sm` |
| spaceMS (12) | `spacing/ms` |
| spaceMD (16) | `spacing/md` |
| spaceLG (24) | `spacing/lg` |
| spaceXL (32) | `spacing/xl` |
| space2XL (48) | `spacing/2xl` |
