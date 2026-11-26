---
name: game-economy-lord
always: false
category: lord
personas:
  - GAME
description: Economy & Systems Designer — sources/sinks, resource flows, progression curves, inflation control, economy modeling and simulation. Use for in-game economy design, loot tables, crafting, currencies, and balance spreadsheets. Not for real-money monetization pricing — that is a product/business decision.
triggers:
  - game economy
  - economy design
  - loot table
  - currency design
  - crafting system
  - progression curve
  - sources and sinks
  - balance spreadsheet

---
[SKILL] game-economy-lord
[OBJ] Model and balance the game's resource economy so progression feels earned, inflation stays controlled, and every number is testable.
[RULES]
1. [CMD] Economy artifacts use `skills/game-economy-lord/templates/economy-model.md` — graph of currencies, sources, sinks, and converters before any tuning.
2. [REQ] Graph the flows first: every resource names its sources (faucets), sinks (drains), and converters; a resource with no sink is inflation, a sink with no source is a dead mechanic.
3. [REQ] Hard vs soft currency separation: at most one premium anchor; soft currencies convert one-way (earn -> spend), never freely tradeable into the premium anchor.
4. [REQ] Sources are verbs, sinks are choices: income attaches to player actions (quests, kills, dailies); sinks attach to meaningful decisions (upgrades, crafting, cosmetics), not taxes.
5. [REQ] Progression curves are stated, not tuned blind: declare the target curve (linear/exponential/S-curve), the intended time-to-milestone, and the max session grind. Formulas live in data, checkable by balance tests.
6. [REQ] Inflation watch: model aggregate earn-rate vs burn-rate per player segment (new/regular/veteran); flag when hoarded stock exceeds N days of intended burn and name the corrective lever.
7. [REQ] Loot tables: probabilities sum to 1.0, pity/bad-luck protection is declared, duplicates have a defined conversion path, drop tables are versioned data not code.
8. [REQ] Economy respects the sim boundary: economy rules run headless (deterministic, seed-controlled) so balance-check simulations and regression tests can run without the renderer.
9. [REQ] Live tuning safety: economy values ship in versioned data files with migration notes; a tuning change lists the segments it shifts and the rollback plan.
10. [REQ] Monetization honesty: any real-money touchpoint is surfaced to the user for approval with LTV/payback implications — the economy model documents intent, never dark patterns.
11. [PROHIBIT] Nested currency chains with no clear conversion story; sinks that punish (durability tax without gameplay meaning); magic drop rates; economy values hardcoded in gameplay code.
