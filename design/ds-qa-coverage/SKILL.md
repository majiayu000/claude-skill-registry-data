---
name: ds-qa-coverage
description: |
  DS QA Coverage — final quality assurance pass for the complete Figma ecosystem. Verifies: all current screen-inventory entries present, all states covered, all components used correctly, zero inline styles, zero orphaned elements, full token binding coverage, prototype connections complete, naming conventions consistent. Use this skill as the LAST step after all screens are built and prototyped. Trigger: "qa coverage", "финальная проверка", "ds qa", "coverage check", "всё ли покрыто", "final check", "проверь покрытие", "quality check figma".
---

# DS QA Coverage

You run the **final quality assurance pass** on the complete Hexbound Figma ecosystem. This is the last step before declaring the DS ecosystem production-ready.

**DS file:** `uDjXIz7CdJxcEOI5jCBcjY`
**Screens file:** `PalemJ36B97ZdC0cd8jzv4`

Verify these keys against the current Figma context before auditing; stale file keys produce false coverage results.

## Prerequisites

1. Load `figma-use` skill BEFORE any `use_figma` calls
2. ALL screens should already be built (`ds-screen-builder`)
3. ALL prototype flows should be connected (`ds-prototype`)

## Check 1: Screen Coverage

Use the current source of truth before counting: `docs/07_ui_ux/SCREEN_INVENTORY.md`, the Swift view tree, and wiki `[[screens]]`. The checklist below is a historical baseline and must be refreshed when screens are added, renamed, or removed.

### 1a. Screen Count

```js
// In use_figma on Screens file — count all screen frames
const pages = figma.root.children;
const screens = [];
for (const page of pages) {
  const frames = page.children.filter(n =>
    n.type === 'FRAME' && n.name.includes('Screens /')
  );
  screens.push(...frames.map(f => ({
    page: page.name,
    name: f.name,
    width: f.width,
    height: f.height
  })));
}
return {
  total: screens.length,
  byPage: pages.map(p => ({
    name: p.name,
    count: screens.filter(s => s.page === p.name).length
  })),
  screens
};
```

**Expected:** every current primary screen from the inventory plus required state variants. Historical baseline: at least 53 primary entries were listed here.

### 1b. Screen Inventory Checklist

Every screen from the refreshed master list must be present. Historical baseline:

| # | Screen | Status |
|---|---|---|
| 1 | Welcome | ☐ |
| 2 | Login | ☐ |
| 3 | Register | ☐ |
| 4 | EmailConfirmation | ☐ |
| 5 | CharacterCreation (4 steps) | ☐ |
| 6 | CharacterSelection | ☐ |
| 7 | LoreIntro | ☐ |
| 8 | UpgradeGuest | ☐ |
| 9 | Hub/CityMap | ☐ |
| 10 | CityBuilding | ☐ |
| 11 | StanceSelector | ☐ |
| 12 | CharacterProfile | ☐ |
| 13 | HeroDetail | ☐ |
| 14 | AppearanceEditor | ☐ |
| 15 | CombatView | ☐ |
| 16 | CombatDetail | ☐ |
| 17 | CombatResult | ☐ |
| 18 | LootDetailView | ☐ |
| 19 | ArenaView | ☐ |
| 20 | ArenaCarousel | ☐ |
| 21 | ArenaComparison | ☐ |
| 22 | OpponentProfile | ☐ |
| 23 | RankUpCeremony | ☐ |
| 24 | InventoryView | ☐ |
| 25 | ItemDetailSheet | ☐ |
| 26 | ShopView | ☐ |
| 27 | CurrencyPurchase | ☐ |
| 28 | PremiumPurchase | ☐ |
| 29 | DungeonSelectView | ☐ |
| 30 | DungeonInfoSheet | ☐ |
| 31 | DungeonRoomView | ☐ |
| 32 | DungeonVictory | ☐ |
| 33 | DungeonDefeat | ☐ |
| 34 | LootPreview | ☐ |
| 35 | BattlePassView | ☐ |
| 36 | BPRewardNodes | ☐ |
| 37 | SeasonSummaryModal | ☐ |
| 38 | DailyQuestsDetail | ☐ |
| 39 | DailyLoginPopup | ☐ |
| 40 | AchievementsView | ☐ |
| 41 | LeaderboardView | ☐ |
| 42 | LeaderboardPlayerDetail | ☐ |
| 43 | InboxView | ☐ |
| 44 | InboxDetail | ☐ |
| 45 | GuildHallDetail | ☐ |
| 46 | GoldMineDetail | ☐ |
| 47 | ShellGameDetail | ☐ |
| 48 | DungeonRushDetail | ☐ |
| 49 | FortuneWheelDetail | ☐ |
| 50 | TavernHub | ☐ |
| 51 | SettingsView | ☐ |
| 52 | SessionExpiredModal | ☐ |
| 53 | LevelUpModal | ☐ |

## Check 2: State Coverage

Each screen must have minimum 3 states:

```js
// Count states per screen base name
const frames = figma.root.findAll(n =>
  n.type === 'FRAME' && n.name.includes('Screens /')
);
const screenStates = {};
for (const f of frames) {
  // Extract base name (before " — ")
  const base = f.name.split(' — ')[0].trim();
  if (!screenStates[base]) screenStates[base] = [];
  const state = f.name.split(' — ')[1]?.trim() || 'Default';
  screenStates[base].push(state);
}

const underCovered = Object.entries(screenStates)
  .filter(([_, states]) => states.length < 3)
  .map(([name, states]) => ({ name, states, count: states.length }));

return {
  totalScreenBases: Object.keys(screenStates).length,
  totalFrames: frames.length,
  underCovered,
  coverage: Object.entries(screenStates).map(([name, states]) => ({
    name,
    states,
    ok: states.length >= 3
  }))
};
```

**Required states per screen:**
- Default (mandatory for ALL)
- Loading (mandatory for screens with async data)
- Empty (for list/collection screens)
- Error (for screens with network calls)
- Success/Result (for action screens: purchase, combat, etc.)

## Check 3: Token Binding Coverage

### 3a. Unbound Fills

```js
// Find all nodes with fills that aren't bound to variables
const violations = [];
figma.root.findAll(n => {
  if (n.fills?.length > 0 && n.fills[0]?.type === 'SOLID') {
    if (!n.boundVariables?.fills?.length) {
      // Exceptions: component internal sub-layers, images
      if (n.parent?.type !== 'COMPONENT' && n.fills[0].type !== 'IMAGE') {
        violations.push({
          name: n.name,
          page: getPageName(n),
          parentFrame: getParentFrameName(n),
          fill: rgbToHex(n.fills[0].color)
        });
      }
    }
  }
});
return { count: violations.length, violations: violations.slice(0, 50) };
```

**Target:** 0 unbound fills (excluding images and component internals)

### 3b. Unlinked Text Styles

```js
// Find all text nodes without linked text styles
const unlinked = [];
figma.root.findAll(n => {
  if (n.type === 'TEXT' && !n.textStyleId) {
    unlinked.push({
      name: n.name,
      page: getPageName(n),
      text: n.characters?.substring(0, 30),
      fontSize: n.fontSize
    });
  }
});
return { count: unlinked.length, unlinked: unlinked.slice(0, 50) };
```

**Target:** 0 unlinked text nodes

### 3c. Unbound Spacing

```js
// Check auto-layout frames for unbound spacing
const unboundSpacing = [];
figma.root.findAll(n => {
  if (n.layoutMode && n.layoutMode !== 'NONE') {
    const issues = [];
    if (n.itemSpacing > 0 && !n.boundVariables?.itemSpacing) issues.push('gap');
    if (n.paddingTop > 0 && !n.boundVariables?.paddingTop) issues.push('paddingTop');
    if (n.paddingRight > 0 && !n.boundVariables?.paddingRight) issues.push('paddingRight');
    if (n.paddingBottom > 0 && !n.boundVariables?.paddingBottom) issues.push('paddingBottom');
    if (n.paddingLeft > 0 && !n.boundVariables?.paddingLeft) issues.push('paddingLeft');
    if (issues.length > 0) {
      unboundSpacing.push({ name: n.name, issues });
    }
  }
});
return { count: unboundSpacing.length, items: unboundSpacing.slice(0, 50) };
```

**Target:** 0 unbound spacing values

## Check 4: Component Usage

### 4a. No Fake Components

```js
// Find FRAME nodes that should be component instances
const suspicious = [];
figma.root.findAll(n => {
  if (n.type === 'FRAME') {
    // Check if it looks like a button but isn't an instance
    if (n.name.toLowerCase().includes('button') && n.parent?.type !== 'COMPONENT_SET') {
      suspicious.push({ name: n.name, type: 'fake button', page: getPageName(n) });
    }
    // Check if it looks like a divider
    if (n.type === 'RECTANGLE' && n.height === 1 && n.width > 100) {
      suspicious.push({ name: n.name, type: 'fake divider', page: getPageName(n) });
    }
  }
});
return suspicious;
```

### 4b. DS Component Usage Stats

```js
// Count instances from DS library
const instances = figma.root.findAll(n => n.type === 'INSTANCE');
const fromDS = instances.filter(i => i.mainComponent?.remote);
const local = instances.filter(i => !i.mainComponent?.remote);

const componentUsage = {};
for (const inst of fromDS) {
  const name = inst.mainComponent?.name || 'Unknown';
  componentUsage[name] = (componentUsage[name] || 0) + 1;
}

return {
  totalInstances: instances.length,
  fromDS: fromDS.length,
  localInstances: local.length,
  topComponents: Object.entries(componentUsage)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 20)
};
```

**Target:** 100% instances from DS library, 0 local component instances

## Check 5: Naming Conventions

```js
// Verify all top-level frames follow naming convention
const frames = [];
for (const page of figma.root.children) {
  for (const child of page.children) {
    if (child.type === 'FRAME') {
      const valid = /^Screens \/ .+ \/ .+ — .+$/.test(child.name);
      frames.push({ name: child.name, valid, page: page.name });
    }
  }
}
const invalid = frames.filter(f => !f.valid);
return { total: frames.length, valid: frames.length - invalid.length, invalid };
```

**Convention:** `Screens / {Category} / {ScreenName} — {State}`

## Check 6: Frame Dimensions

```js
// All screen frames should be 390×844
const wrongSize = [];
figma.root.findAll(n => {
  if (n.type === 'FRAME' && n.name.includes('Screens /')) {
    if (n.width !== 390 || n.height !== 844) {
      wrongSize.push({ name: n.name, width: n.width, height: n.height });
    }
  }
});
return wrongSize;
```

**Target:** ALL screens 390×844 (iPhone 15 Pro)

## Check 7: Prototype Connections

```js
// Count prototype connections
const withReactions = figma.root.findAll(n => n.reactions?.length > 0);
const connections = withReactions.map(n => ({
  name: n.name,
  reactions: n.reactions.length,
  targets: n.reactions.map(r => r.actions?.[0]?.destinationId).filter(Boolean)
}));

// Check orphaned screens (no incoming connections)
const allTargets = new Set(connections.flatMap(c => c.targets));
const screenFrames = figma.root.findAll(n =>
  n.type === 'FRAME' && n.name.includes('Screens /') && n.name.includes('— Default')
);
const orphaned = screenFrames.filter(f => !allTargets.has(f.id) && !f.name.includes('Welcome'));

return {
  totalConnections: connections.reduce((sum, c) => sum + c.reactions, 0),
  nodesWithConnections: connections.length,
  orphanedScreens: orphaned.map(f => f.name)
};
```

**Target:** ≥80 connections, 0 orphaned screens (except Welcome as entry point)

## Check 8: Effect Styles

```js
// Verify cards and modals have effect styles applied
const cardsWithoutShadow = [];
figma.root.findAll(n => {
  if (n.type === 'INSTANCE' && n.name.includes('Card')) {
    if (!n.effectStyleId && !n.effects?.length) {
      cardsWithoutShadow.push(n.name);
    }
  }
});
return cardsWithoutShadow;
```

## Output: QA Coverage Report

```markdown
## DS QA Coverage Report — [date]

### Screen Coverage
- Total screens: [X]/48 (states: [Y] total)
- Missing screens: [list]
- Under-covered (< 3 states): [list]

### Token Binding
- Unbound fills: [X] violations
- Unlinked text styles: [X] violations
- Unbound spacing: [X] violations

### Component Usage
- Total instances: [X]
- From DS library: [X]%
- Local/fake: [X] (should be 0)

### Naming: [X]/[Y] valid ([Z]%)
### Frame sizes: [X]/[Y] correct
### Prototype: [X] connections, [Y] orphaned screens
### Effect styles: [X] cards without shadows

### Overall Score: [X]% coverage

### 🟢 PASS / 🔴 FAIL (threshold: 95%)

### Actions Required
[Prioritized list of fixes needed]
```

## Scoring

| Metric | Weight | 100% = |
|---|---|---|
| Screen coverage | 25% | 100% of current screen inventory |
| State coverage | 15% | ≥3 states per screen |
| Token binding (fills) | 15% | 0 unbound |
| Token binding (text) | 10% | 0 unlinked |
| Token binding (spacing) | 10% | 0 unbound |
| Component usage | 10% | 100% from DS |
| Naming | 5% | 100% valid |
| Prototype | 5% | ≥80 connections |
| Frame dimensions | 5% | 100% correct |

**Pass threshold:** 95% overall score

## Fix Priority

If QA finds issues, fix in this order:

1. **Missing screens** → use `ds-screen-builder`
2. **Unbound tokens** → fix variable bindings in Figma
3. **Unlinked text styles** → link to correct Heading/* or Body/*
4. **Fake components** → replace with DS instances
5. **Missing states** → add Loading/Empty/Error states
6. **Naming violations** → rename to convention
7. **Missing prototype connections** → use `ds-prototype`
8. **Wrong frame sizes** → resize to 390×844

Re-run this QA check after each fix round until 95%+ is achieved.
