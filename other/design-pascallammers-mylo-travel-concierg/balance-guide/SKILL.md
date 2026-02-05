---
name: balance-guide
description: Guide for balancing new Heart Rush content including talents, races, bloodmarks, and progression. Use when creating or modifying game mechanics to ensure they fit the existing power curve.
allowed-tools: Read, Grep, Glob
---

# Heart Rush Balance Guide

This skill provides guidelines for balancing new content for the Heart Rush TTRPG.

## General Philosophy

Heart Rush is "fail-forward" and gritty.
- **Power is Earned**: Characters start weak and become legendary.
- **Resource Management**: Abilities often cost resources (Actions, Rush Points, Daily Uses).
- **Niche Protection**: Talents should enable specific playstyles without invalidating others.

## Ability Definitions (Core Knowledge)

All content (Talents, Racial Abilities, Bloodmarks) relies on these standard definitions.

### Ability Structure
**Ability Name**  
_Ability tags (Frequency, Timing, Prerequisites)._  
Rules text describing the effect.

### Frequency Tags (Cost/Limit)
The first tag determines power budget.

| Tag | Frequency / Cost | Balance Philosophy |
| :--- | :--- | :--- |
| **Passive** | Always active. | **Low Impact/Consistent.** No cost. Avoid stacking flat bonuses. Good for niche perks or unlocking actions. |
| **Minor** | Encounter resource (Rush Points). | **Tactical/Spammable.** Costs 1 RP (1st use), 2 RP (2nd), etc. Resets after fight. Good for damage boosts, conditions, mobility. |
| **Major** | Daily (Long Rest). | **High Impact.** "Ultimate" moves defining a session. Good for boss fights. |
| **Weekly** | Once per 7 days. | **Narrative Power.** Long-term buffs, economic influence. |
| **Monthly** | Once per 30 days. | **Plot Device.** Resurrection, weather alteration, legendary crafting. |

### Timing Tags
Timing affects utility in combat.

| Tag | Timing | Balance Philosophy |
| :--- | :--- | :--- |
| **(None)** | Action Phase Only. | **Standard.** Cannot interrupt or be used during Engagements. Requires planning. |
| **Instant** | Anytime / Interrupt. | **Reactive/Powerful.** Used anytime (interrupting actions, after rolls, during Engagements). Premium utility; usually paired with a cost. Resolution is "Last-in, First-out". |

### Writing Rules Text
Ensure text covers:
1. **Trigger/Action Cost** (Action, Sidestep, Free?)
2. **Range & Target** (Self, 30ft, Allies?)
3. **Effect** (Specific mechanics, e.g., "Gain A2")
4. **Duration** (Instant, End of round, 1 min)
5. **Conditions** (Saving throws?)

## Specific Content Guides

For detailed costs and progression rules, refer to:

- **Talents**: `TALENT_BALANCE.md` - XP Costs, Combat/Noncombat/Elemental specifics.
- **Races**: `RACE_BALANCE.md` - Vitals, aspects, and racial abilities.
- **Bloodmarks**: `BLOODMARK_BALANCE.md` - Progression and ability types.
- **Progression**: `PROGRESSION_BALANCE.md` - XP economy and Heart Die milestones.