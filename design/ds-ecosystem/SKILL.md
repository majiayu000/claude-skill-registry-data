---
name: ds-ecosystem
description: |
  DS Ecosystem Master Plan — полный пайплайн создания Figma экосистемы Hexbound. 10 этапов: UI-аудит → Foundations → Tokens → Components → Screens → Consistency → File Structure → Naming → Prototype → QA. Используй этот скилл как MASTER ORCHESTRATOR для любой задачи по построению полной Figma экосистемы. Trigger: "полная экосистема", "ds ecosystem", "все экраны в фигме", "собери всё", "figma full build", "10 этапов", "master plan", "полная дизайн-система".
---

# DS Ecosystem — Master Plan

Ты строишь полную Figma-экосистему Hexbound: все экраны, все токены, все компоненты, все состояния. Результат: любой экран собирается только из DS, full 1:1 parity с кодом.

## Текущее состояние (исторический снимок на 2026-04-03)

Перед выполнением обнови этот снимок из текущего Swift-кода, `docs/07_ui_ux/SCREEN_INVENTORY.md`, Figma metadata и wiki `[[screens]]`. Не считай числа ниже актуальными без повторной проверки.

### УЖЕ ГОТОВО (DS файл: `uDjXIz7CdJxcEOI5jCBcjY`)
- ✅ 359 design tokens (188 Primitives + 158 Semantic + 14 Spacing)
- ✅ 9 Text Styles (Oswald + Inter)
- ✅ 4 Effect Styles (Card, Modal, Gold Glow, Danger Glow)
- ✅ 45 component sets, 230 variants, 164 instances, 21 pages
- ✅ iOS Code Syntax на всех переменных
- ✅ Variable scopes настроены (FILL, TEXT_FILL, STROKE_FILL, GAP, CORNER_RADIUS)

### НУЖНО СДЕЛАТЬ (Screens файл: `PalemJ36B97ZdC0cd8jzv4`)
- ❌ Только 6 экранов из 48 (Hub, Arena, Hero Detail, Fortune Wheel, Shell Game, Quest Banner)
- ❌ 42+ экранов отсутствуют
- ❌ Нет прототипа (flow connections)
- ❌ Нет QA/Coverage проверки
- ❌ Некоторые inline-паттерны не извлечены в компоненты

## Два файла — строгое разделение

- **DS:** `uDjXIz7CdJxcEOI5jCBcjY` — ТОЛЬКО токены, стили, компоненты. НИКАКИХ экранов.
- **Screens:** `PalemJ36B97ZdC0cd8jzv4` — ТОЛЬКО экраны из DS компонентов. НИКАКИХ компонентов.
- **DS library key:** `lk-1e3d5b13e106c557d2ec56c3ac95231374bc21a6136997e732d7a804ec4d86c11297eee6bd376c1bc936574dd6ba4ddea2380be439e8701a5408d7daaff18fb4`

## 10 Этапов

### ЭТАП 1: UI-АУДИТ (используй `ds-code-audit` скилл)

Зафиксируй полный инвентарь из Swift кода:

**Исторический список экранов по категориям:**

| Категория | Экраны |
|---|---|
| Auth (8) | Welcome, Login, Register, EmailConfirmation, CharacterCreation (4 шага), CharacterSelection, LoreIntro, UpgradeGuest |
| Hub (6) | Hub/CityMap, CityBuilding, HubEditor(dev), CityMapEffects, StanceSelector, TutorialOverlay |
| Character (3) | CharacterProfile, HeroDetail, AppearanceEditor |
| Combat (4) | CombatView, CombatDetail, CombatResult(BattleResultCard), LootDetailView |
| Arena (5) | ArenaView, ArenaCarousel, ArenaComparison, OpponentProfile, RankUpCeremony |
| Inventory (2) | InventoryView (Equipment+Consumables tabs), ItemDetailSheet |
| Shop (3) | ShopView (3 tabs), CurrencyPurchase, PremiumPurchase |
| Dungeon (5) | DungeonSelectView, DungeonInfoSheet, DungeonRoomView, DungeonVictory, DungeonDefeat, LootPreview |
| BattlePass (3) | BattlePassView, BPRewardNodes, SeasonSummaryModal |
| Progression (3) | DailyQuestsDetail, DailyLoginPopup, AchievementsView |
| Leaderboard (2) | LeaderboardView, LeaderboardPlayerDetail |
| Social (3) | InboxView, InboxDetail, GuildHallDetail |
| Minigames (5) | GoldMineDetail, ShellGameDetail, DungeonRushDetail, FortuneWheelDetail, TavernHub |
| Settings (1) | SettingsView |
| Utility (2) | SessionExpiredModal, LevelUpModal |

**Состояния для каждого экрана:**
- Default, Loading, Empty, Error, Success
- + экран-специфичные: Selected, Disabled, Modal overlay, Banner active

**User Flows:**
1. Onboarding: Welcome → Login/Register → Email → Character Creation → Lore → Hub
2. PvP: Hub → Arena → Select Opponent → Compare → Combat → Result → Loot
3. PvE: Hub → Dungeon Select → Info → Room Combat → Victory/Defeat → Loot
4. Equipment: Hub → Inventory → Item Detail → Equip/Sell
5. Shopping: Hub → Shop → Select Item → Purchase → Confirm
6. Progression: Hub → Daily Quests/Achievements/BattlePass → Claim Rewards
7. Social: Hub → Leaderboard/Inbox/Guild → Interact
8. Minigames: Hub → Tavern → Game → Play → Reward

### ЭТАП 2: FOUNDATIONS (уже в DS файле)

Проверь наличие foundation pages:
- ✅ Foundations / Colors
- ✅ Foundations / Typography
- ✅ Foundations / Spacing & Radius
- ❓ Foundations / Motion (нужно добавить если нет)
- ❓ Foundations / Elevation (нужно добавить если нет)
- ❓ Foundations / Touch Targets (нужно добавить если нет)

### ЭТАП 3: DESIGN TOKENS (уже готовы)

359 переменных — проверь через `ds-figma-sync` скилл.

### ЭТАП 4: КОМПОНЕНТЫ

**Существующие (45 component sets):**
Buttons(6), Cards(1), Dividers(1), TabSwitcher(1), ProgressBars(1), Badges&Pills(11), CurrencyDisplay(1), EmptyErrorStates(1), Loading(1), Navigation(1), OrnamentalTitle(1), ItemCard(1), Skeleton(1), Input(1), Hero&Character(2), Arena&PvP(4), Dungeon&Progression(4), Social&Messaging(2), Toast&Banners(4), Modals&Sheets(1)

**Нужно извлечь (из ds-code-audit):**
1. StatComparisonDeltaBadge (▲+12 / ▼-5) — 5 мест в коде
2. RarityBorderedFrame — 4+ мест
3. ClassTagPill — 2 места (уже есть в Figma, нет в Swift)
4. RarityLabel (Capsule) — 3 места
5. RewardPill — 2 варианта

**Порядок:** Сначала извлеки в Swift (`ds-extract-component`), потом создай в Figma DS.

### ЭТАП 5: СБОРКА ЭКРАНОВ (используй `ds-screen-builder` скилл)

**Структура Screens файла:**

| Page | Экраны |
|---|---|
| Auth | Welcome, Login, Register, EmailConfirm, CharacterCreation, CharacterSelect, LoreIntro, UpgradeGuest |
| Hub | Hub/CityMap, CityBuilding, StanceSelector |
| Character | CharacterProfile, HeroDetail, AppearanceEditor |
| Combat | CombatView, CombatDetail, CombatResult, LootDetail |
| Arena | ArenaView, ArenaCarousel, ArenaComparison, OpponentProfile, RankUpCeremony |
| Inventory | InventoryView, ItemDetailSheet |
| Shop | ShopView, CurrencyPurchase, PremiumPurchase |
| Dungeon | DungeonSelect, DungeonInfo, DungeonRoom, Victory, Defeat, LootPreview |
| BattlePass | BattlePassView, RewardNodes, SeasonSummary |
| Progression | DailyQuests, DailyLogin, Achievements |
| Social | Leaderboard, LeaderboardDetail, Inbox, InboxDetail, GuildHall |
| Minigames | GoldMine, ShellGame, DungeonRush, FortuneWheel, TavernHub |
| Settings | Settings |
| Modals & Overlays | LevelUp, SessionExpired, GuestGate, all sheets |

**Правило:** каждый экран собирается ТОЛЬКО из DS компонентов + DS переменных. Если элемент не в DS — сначала добавь в DS, потом используй.

### ЭТАП 6: CONSISTENCY CHECK

Для каждого экрана проверь:
- [ ] Все элементы — instances DS компонентов
- [ ] Все цвета — variable bindings из Color collection
- [ ] Все шрифты — linked text styles
- [ ] Все spacing — variable bindings из Spacing collection
- [ ] Все radius — variable bindings из Spacing collection
- [ ] Все shadows — effect styles
- [ ] Нет one-off элементов
- [ ] Нет inline styles

### ЭТАП 7: NAMING

Нейминг уже установлен в DS. Для экранов:
- Screens / Auth / Welcome — Default
- Screens / Auth / Welcome — Loading
- Screens / Hub / CityMap — Default
- Screens / Combat / Battle — Default
- Screens / Combat / Battle — Victory

### ЭТАП 8: PROTOTYPE (используй `ds-prototype` скилл)

Подключи flow connections между экранами. Ключевые flow:
1. Onboarding (8 экранов)
2. PvP combat (6 экранов)
3. Dungeon PvE (6 экранов)
4. Equipment (3 экрана)
5. Shopping (3 экрана)

### ЭТАП 9: QA COVERAGE (используй `ds-qa-coverage` скилл)

Финальная проверка:
- Все экраны из актуального screen inventory покрыты
- Все состояния покрыты (min 3: default, loading, empty/error)
- Все компоненты используются
- Нет orphaned компонентов
- Нет inline styles
- Нет visual drift

### ЭТАП 10: ОТЧЁТ

Выдай:
1. Полный список экранов из актуального inventory + состояний
2. Полный список токенов (359)
3. Полный список компонентов (45+)
4. Что было добавлено
5. Какие расхождения найдены и закрыты
6. Что осталось на следующий этап

## Порядок выполнения (sequential)

```
1. ds-code-audit → найти inline-паттерны
2. ds-extract-component → извлечь в Swift + Figma DS
3. ds-figma-sync → проверить паритет токенов
4. ds-screen-builder → собрать все экраны из актуального inventory
5. ds-prototype → подключить flow
6. ds-qa-coverage → финальная проверка
```

## Скиллы экосистемы

| Скилл | Что делает |
|---|---|
| `ds-ecosystem` | Master plan — этот файл |
| `ds-code-audit` | Аудит Swift кода на DS compliance + дубликаты |
| `ds-figma-sync` | Проверка паритета Code ↔ Figma |
| `ds-extract-component` | Извлечение inline → reusable component |
| `ds-screen-builder` | Сборка экранов в Figma из DS компонентов |
| `ds-prototype` | Прототипирование flow в Figma |
| `ds-qa-coverage` | Финальный QA coverage check |
