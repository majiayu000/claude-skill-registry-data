---
name: roblox-economy-balancing
description: Balance Roblox economies and progression math. Use for currency sources and sinks, pricing, reward curves, upgrade costs, inflation control, event economies, progression pacing, premium offers, and profitability without pay-to-win pressure.
---

# Roblox Economy Balancing

## Goal

Create an economy that rewards play, supports monetization, and lasts long enough for retention.

## Economy Map

Define:

- Sources: core loop rewards, quests, streaks, events, social rewards, purchases.
- Sinks: upgrades, crafting, cosmetics, rerolls, prestige, entry fees, repairs.
- Multipliers: boosts, VIP, game passes, events, group/friend bonuses.
- Gates: zones, levels, equipment, quests, timers.

## Balance Rules

- Reward every loop, but keep meaningful upgrades paced.
- Make early upgrades fast and satisfying.
- Avoid runaway compounding that destroys long-term goals.
- Add enough sinks before adding large sources.
- Keep premium boosts convenient, not mandatory.
- Preserve social fairness and competitive integrity.

## Curves

Use simple tables first:

- Early: quick wins and teaching.
- Mid: visible planning and choice.
- Late: prestige, collections, rarity, social flex.

Watch for the 2-3 hour content wall and add meaningful unlocks before it.

## Output

Return:

- Source/sink table.
- Upgrade or reward curve.
- Inflation risks.
- Monetization fairness notes.
- Playtest metrics to collect.

## Next

Protect the tuned economy from exploits with `roblox-security-economy`, and instrument sources and sinks with `roblox-analytics-instrumentation` to watch for inflation live.

