---
name: ds-prototype
description: |
  DS Prototype — creates clickable prototype flows in Figma by connecting screens with interactions and transitions. Builds navigation flows for onboarding, PvP, PvE, shopping, equipment, progression, social, and minigames. Use this skill AFTER all screens are built (ds-screen-builder). Trigger: "prototype", "прототип", "flow connections", "clickable flow", "navigation flow", "connect screens", "подключи переходы", "сделай кликабельным".
---

# DS Prototype

You create clickable prototypes in the **Figma Screens file** by connecting screens with interactions, transitions, and navigation flows.

**Screens file:** `PalemJ36B97ZdC0cd8jzv4`

Verify this file key against the current Figma context before writing prototype links.

## Prerequisites

1. Load `figma-use` skill BEFORE any `use_figma` calls
2. All target screens must already exist (built via `ds-screen-builder`)
3. Read screen inventory to know which screens are available

## Core Concepts

### Figma Prototype API

```js
// In use_figma — connect two frames with a prototype interaction
const sourceNode = await figma.getNodeByIdAsync('SOURCE_NODE_ID');
const targetFrame = await figma.getNodeByIdAsync('TARGET_FRAME_ID');

// Add reaction (click → navigate)
sourceNode.reactions = [
  {
    trigger: { type: 'ON_CLICK' },
    actions: [
      {
        type: 'NODE',
        destinationId: targetFrame.id,
        navigation: 'NAVIGATE',
        transition: {
          type: 'SLIDE_IN',
          direction: 'LEFT',
          duration: 0.3,
          easing: { type: 'EASE_IN_OUT' }
        }
      }
    ]
  }
];
```

### Transition Types by Context

| Navigation Context | Transition | Duration | Direction |
|---|---|---|---|
| Push to new screen | SLIDE_IN | 0.3s | LEFT |
| Go back | SLIDE_IN | 0.3s | RIGHT |
| Open modal/sheet | MOVE_IN | 0.3s | BOTTOM → TOP |
| Close modal/sheet | MOVE_OUT | 0.2s | TOP → BOTTOM |
| Tab switch | DISSOLVE | 0.15s | — |
| Overlay popup | DISSOLVE | 0.2s | — |
| Auth flow forward | SLIDE_IN | 0.3s | LEFT |
| Success → Hub | DISSOLVE | 0.4s | — |

## 8 Key User Flows

### Flow 1: Onboarding (8 screens)

```
Welcome → Login/Register → EmailConfirmation → CharacterCreation (4 steps) → LoreIntro → Hub
```

| From | Trigger Element | To | Transition |
|---|---|---|---|
| Welcome | "Login" button | Login | SLIDE_IN LEFT |
| Welcome | "Register" button | Register | SLIDE_IN LEFT |
| Login | "Login" submit | Hub | DISSOLVE 0.4s |
| Login | "Register" link | Register | SLIDE_IN LEFT |
| Register | "Register" submit | EmailConfirmation | SLIDE_IN LEFT |
| EmailConfirmation | "Continue" button | CharacterCreation Step 1 | SLIDE_IN LEFT |
| CharCreation 1 | "Next" | CharCreation 2 | SLIDE_IN LEFT |
| CharCreation 2 | "Next" | CharCreation 3 | SLIDE_IN LEFT |
| CharCreation 3 | "Next" | CharCreation 4 | SLIDE_IN LEFT |
| CharCreation 4 | "Create" | LoreIntro | DISSOLVE 0.4s |
| LoreIntro | "Enter Hexbound" | Hub | DISSOLVE 0.5s |

### Flow 2: PvP Combat (6 screens)

```
Hub → ArenaView → ArenaComparison → CombatView → CombatResult → LootDetail
```

| From | Trigger | To | Transition |
|---|---|---|---|
| Hub | Arena building | ArenaView | SLIDE_IN LEFT |
| ArenaView | Opponent card tap | ArenaComparison | MOVE_IN BOTTOM |
| ArenaComparison | "Fight" button | CombatView | DISSOLVE 0.3s |
| CombatView | Combat ends | CombatResult | DISSOLVE 0.4s |
| CombatResult | "View Loot" | LootDetail | MOVE_IN BOTTOM |
| CombatResult | "Continue" | Hub | DISSOLVE 0.3s |
| LootDetail | Close | CombatResult | MOVE_OUT BOTTOM |
| ArenaView | Back button | Hub | SLIDE_IN RIGHT |

### Flow 3: Dungeon PvE (6 screens)

```
Hub → DungeonSelect → DungeonInfo → DungeonRoom → Victory/Defeat → LootPreview
```

| From | Trigger | To | Transition |
|---|---|---|---|
| Hub | Dungeon building | DungeonSelect | SLIDE_IN LEFT |
| DungeonSelect | Dungeon card | DungeonInfo | MOVE_IN BOTTOM |
| DungeonInfo | "Enter" button | DungeonRoom | DISSOLVE 0.3s |
| DungeonRoom | Win | Victory | DISSOLVE 0.4s |
| DungeonRoom | Lose | Defeat | DISSOLVE 0.4s |
| Victory | "View Loot" | LootPreview | MOVE_IN BOTTOM |
| Victory | "Continue" | Hub | DISSOLVE 0.3s |
| Defeat | "Try Again" | DungeonInfo | SLIDE_IN LEFT |
| Defeat | "Retreat" | Hub | DISSOLVE 0.3s |

### Flow 4: Equipment (3 screens)

```
Hub → InventoryView → ItemDetailSheet
```

| From | Trigger | To | Transition |
|---|---|---|---|
| Hub | Character tap / Inventory building | InventoryView | SLIDE_IN LEFT |
| InventoryView | Item card tap | ItemDetailSheet | MOVE_IN BOTTOM |
| ItemDetailSheet | "Equip" / Close | InventoryView | MOVE_OUT BOTTOM |
| InventoryView | Back | Hub | SLIDE_IN RIGHT |

### Flow 5: Shopping (3 screens)

```
Hub → ShopView → ItemDetailSheet / CurrencyPurchase
```

| From | Trigger | To | Transition |
|---|---|---|---|
| Hub | Shop building | ShopView | SLIDE_IN LEFT |
| ShopView | Item tap | ItemDetailSheet | MOVE_IN BOTTOM |
| ShopView | "Buy Gold/Gems" | CurrencyPurchase | MOVE_IN BOTTOM |
| ItemDetailSheet | "Buy" confirm | ShopView | MOVE_OUT BOTTOM |
| ShopView | Back | Hub | SLIDE_IN RIGHT |

### Flow 6: Progression (3 screens)

```
Hub → DailyQuestsDetail / AchievementsView / BattlePassView
```

| From | Trigger | To | Transition |
|---|---|---|---|
| Hub | Quest banner tap | DailyQuestsDetail | SLIDE_IN LEFT |
| Hub | Battle Pass building | BattlePassView | SLIDE_IN LEFT |
| DailyQuestsDetail | "Achievements" tab | AchievementsView | DISSOLVE 0.15s |
| DailyQuestsDetail | Back | Hub | SLIDE_IN RIGHT |
| BattlePassView | Back | Hub | SLIDE_IN RIGHT |

### Flow 7: Social (3 screens)

```
Hub → LeaderboardView / InboxView / GuildHallDetail
```

| From | Trigger | To | Transition |
|---|---|---|---|
| Hub | Leaderboard building | LeaderboardView | SLIDE_IN LEFT |
| Hub | Inbox building | InboxView | SLIDE_IN LEFT |
| Hub | Guild building | GuildHallDetail | SLIDE_IN LEFT |
| LeaderboardView | Player row tap | LeaderboardPlayerDetail | MOVE_IN BOTTOM |
| InboxView | Message tap | InboxDetail | SLIDE_IN LEFT |

### Flow 8: Minigames (5 screens)

```
Hub → TavernHub → GoldMine / ShellGame / DungeonRush / FortuneWheel
```

| From | Trigger | To | Transition |
|---|---|---|---|
| Hub | Tavern building | TavernHub | SLIDE_IN LEFT |
| TavernHub | Game card | GoldMineDetail / ShellGameDetail / etc. | SLIDE_IN LEFT |
| Each game | Back | TavernHub | SLIDE_IN RIGHT |
| TavernHub | Back | Hub | SLIDE_IN RIGHT |

## Global Navigation (NavGrid)

The bottom NavGrid is present on most screens. Connect NavGrid buttons:

| NavGrid Button | Destination | Transition |
|---|---|---|
| Hub | Hub/CityMap | DISSOLVE 0.15s |
| Character | CharacterProfile | DISSOLVE 0.15s |
| Arena | ArenaView | DISSOLVE 0.15s |
| Shop | ShopView | DISSOLVE 0.15s |
| Settings | SettingsView | DISSOLVE 0.15s |

## Modal / Sheet Pattern

Modals and sheets appear as overlays:

```js
// Open as overlay (doesn't navigate away from current screen)
sourceNode.reactions = [
  {
    trigger: { type: 'ON_CLICK' },
    actions: [
      {
        type: 'NODE',
        destinationId: modalFrame.id,
        navigation: 'OVERLAY',
        transition: {
          type: 'MOVE_IN',
          direction: 'BOTTOM',
          duration: 0.3,
          easing: { type: 'EASE_OUT' }
        },
        preserveScrollPosition: true
      }
    ]
  }
];
```

Modals that use OVERLAY navigation:
- ItemDetailSheet
- DungeonInfo
- ArenaComparison
- CurrencyPurchase
- PremiumPurchase
- DailyLoginPopup
- LevelUpModal
- SessionExpiredModal
- GuestGateView

## Execution Order

1. **Start with Hub** — it's the central node connecting to everything
2. **Connect Flow 2 (PvP)** — highest-engagement flow
3. **Connect Flow 3 (PvE)** — second core loop
4. **Connect Flow 4+5 (Equipment + Shop)** — monetization flows
5. **Connect Flow 6 (Progression)** — retention flows
6. **Connect Flow 1 (Onboarding)** — first-time experience
7. **Connect Flow 7+8 (Social + Minigames)** — secondary engagement
8. **Connect Global NavGrid** — cross-flow navigation
9. **Connect Modals/Sheets** — overlay interactions

## Verification

After connecting all flows:

```js
// Count all prototype connections in the file
const allFrames = figma.root.findAll(n => n.type === 'FRAME' && n.reactions?.length > 0);
return allFrames.map(f => ({
  name: f.name,
  connections: f.reactions.length
}));
```

**Expected:** prototype coverage for the current screen inventory. Historical baseline was 80+ connections across 48 screens; refresh the target count when screen inventory changes.

Take screenshots of each flow's starting screen to visually verify the blue prototype arrows are visible.
