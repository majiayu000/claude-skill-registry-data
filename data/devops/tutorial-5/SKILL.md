---
name: tutorial-5
description: Manage D&D 5e character progression with XP tracking, automatic leveling, HP increases, proficiency bonus progression, and spell slot advancement. This skill should be used when conducting combat encounters with character advancement, awarding experience points after victories, or managing character level-ups in the training arena.
---

# D&D Character Progression System

## Overview

Orchestrate D&D 5th Edition character advancement through experience points and leveling. Handle XP awards after combat victories, automatic level-ups when XP thresholds are reached, HP increases, proficiency bonus progression, and spell slot advancement. Progression follows 5e rules for XP thresholds (PHB p.15) and supports levels 1-20.

## Available Scripts

Access seven Python scripts in the `scripts/` directory:

1. **roll_dice.py** - Dice rolling (from Tutorial 1)
2. **character.py** - Character management with XP tracking (extended from Tutorial 4)
3. **bestiary.py** - Monster database management
4. **equipment.py** - Equipment and AC calculation
5. **spells.py** - Spell database management
6. **combat.py** - Combat mechanics with XP awards (extended from Tutorial 4)
7. **progression.py** - **NEW**: Leveling logic, XP awards, threshold triggers

All scripts are located at: `~/.claude/skills/tutorial-5/scripts/`

## Character Progression System

Tutorial 5 introduces experience points and automatic leveling, teaching **threshold triggers** (automatic level-ups), **progressive complexity** (features unlock gradually), and **calculated growth** (stat increases follow formulas).

### Core Mechanics

**Experience Points (XP):**
- Awarded after combat victories based on monster CR
- Accumulates over time (never resets)
- Tracked persistently in character database

**Automatic Leveling:**
- When XP >= threshold for next level → automatic level-up
- Can level up multiple times from a single large XP award
- Grants HP, proficiency bonus increases, spell slot upgrades

**XP Awards by CR:**
- CR 0: 10 XP (Rat)
- CR 1/4: 50 XP (Goblin, Skeleton)
- CR 1/2: 100 XP (Orc)
- CR 1: 200 XP (Dire Wolf)
- CR 2+: Scales up (450, 700, 1100, 1800 XP)

### Level-Up Benefits

Each level grants specific benefits:

1. **Hit Points**: Gain average hit die + CON modifier
   - Wizard (d6): +4 + CON per level
   - Fighter (d10): +6 + CON per level

2. **Proficiency Bonus**: Increases at levels 5, 9, 13, 17
   - Levels 1-4: +2
   - Levels 5-8: +3
   - Levels 9-12: +4

3. **Spell Slots** (casters only): Gain additional slots and access to higher-level spells
   - Level 1: 2 × 1st-level
   - Level 2: 3 × 1st-level
   - Level 3: 4 × 1st-level, 2 × 2nd-level
   - Level 4: 4 × 1st-level, 3 × 2nd-level
   - Level 5: 4 × 1st-level, 3 × 2nd-level, 2 × 3rd-level

For complete progression rules and XP tables, see `references/progression-rules.md`

## Combat Workflow with XP

Follow this workflow when conducting training arena combat with character progression:

### Step 1: Seed Databases (First Time Only)

On first use, seed the databases:

```bash
python3 ~/.claude/skills/tutorial-5/scripts/bestiary.py seed
python3 ~/.claude/skills/tutorial-5/scripts/spells.py seed
```

### Step 2: Check Character Equipment

Before combat, verify character has equipment:

```bash
python3 ~/.claude/skills/tutorial-5/scripts/equipment.py show CHARACTER_NAME
```

If no equipment found, equip starting gear:

```bash
python3 ~/.claude/skills/tutorial-5/scripts/equipment.py equip CHARACTER_NAME CLASS_NAME
```

### Step 3: Start Combat

Initialize the combat encounter:

```bash
python3 ~/.claude/skills/tutorial-5/scripts/combat.py start CHARACTER_NAME MAX_CR
```

**MAX_CR calculation**: Use `character_level / 4` as guideline.

This outputs JSON containing character stats (including current XP and level), monster stats (including CR), and initiative.

Parse JSON and display combat start state narratively. See Tutorial 4's `references/narrative-guide.md` for radio drama narrative style.

### Step 4: Combat Loop

Execute turns in initiative order until end condition met.

**Character Turn:**
- Attack with weapon: `combat.py character-attack ...`
- Cast spell: `combat.py character-cast ...`
- Flee or surrender

**Monster Turn:**
- Monster attacks: `combat.py monster-attack ...`

**End Conditions:**
- Monster HP ≤ 0: Victory
- Character HP ≤ 0: Defeat
- Character fled: Escaped
- Character surrendered: Defeat

See Tutorial 4 for detailed combat mechanics.

### Step 5: End Combat and Award XP

When combat ends, call end combat with monster CR for XP award:

```bash
python3 ~/.claude/skills/tutorial-5/scripts/combat.py end CHARACTER_NAME OUTCOME --monster-cr CR_VALUE
```

**OUTCOME**: `victory`, `defeat`, or `fled`
**--monster-cr**: Monster's CR (e.g., 0.25 for Goblin, 0.5 for Orc)

**On victory:**
- Character healed to full HP
- XP awarded based on monster CR
- Automatic level-up if XP threshold reached
- Spell slots restored

**Example:**
```bash
python3 scripts/combat.py end Bob victory --monster-cr 0.25

# ✓ Victory! Bob has been fully healed.
# ✓ Awarded 50 XP to Bob
#   Total XP: 250 → 300
#
# 🎉 LEVEL UP! Bob is now level 2!
#   Levels gained: 1
#   HP increased: 11 → 20 (+9)
#   Proficiency bonus: +2
#   XP to next level: 600
```

**On defeat or fled:**
- No XP awarded
- Fled grants healing, defeat does not

## Progression Commands Reference

### Award XP Manually

Manually award XP for quest rewards or special achievements:

```bash
python3 ~/.claude/skills/tutorial-5/scripts/progression.py award CHARACTER_NAME XP_AMOUNT
```

**Example:**
```bash
python3 scripts/progression.py award Bob 150
# ✓ Awarded 150 XP to Bob
#   Total XP: 0 → 150
#   XP to level 2: 150 more needed
```

If the XP award crosses a level threshold, automatic level-up occurs with full benefits display.

### View XP Requirements

Display XP thresholds for all levels:

```bash
python3 ~/.claude/skills/tutorial-5/scripts/progression.py xp-table
```

Shows:
- Total XP required for each level (1-20)
- XP needed from previous level
- D&D 5e standard progression

### View CR XP Awards

Display XP awarded for each Challenge Rating:

```bash
python3 ~/.claude/skills/tutorial-5/scripts/progression.py cr-xp
```

Shows XP earned for defeating monsters of each CR.

### View Character Stats

Display character info including current XP and progress to next level:

```bash
python3 ~/.claude/skills/tutorial-5/scripts/character.py show CHARACTER_NAME
```

Output includes:
```
Bob (Fighter, Level 2)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
XP: 350/900 (need 550 more)

STR: 16 (+3)
DEX: 12 (+1)
...
HP: 20/20
Proficiency: +2
```

## Narrative Style

Continue using the **radio drama** narrative style from Tutorial 4 for combat. See Tutorial 4's `references/narrative-guide.md` for detailed guidance.

**Level-Up Narrative:**
When characters level up, narrate it dramatically:

```
🎉 LEVEL UP! 🎉

Bob's victories in the arena have forged him into a stronger warrior!
The training master nods approvingly as Bob demonstrates his newfound prowess.

He feels power surge through his body:
  • Muscles strengthen, endurance increases (+9 HP)
  • Technique refines, strikes land more accurately (+2 proficiency)
  • Ready to face greater challenges!

Bob stands tall, no longer a novice but a proven combatant. The arena
awaits his next battle.
```

Match the narrative tone to the magnitude of the level-up (level 2 vs. level 5 major power spike).

## XP Thresholds (Quick Reference)

| Level | Total XP  | From Prev | Goblin Fights (CR 1/4, 50 XP) |
|-------|-----------|-----------|-------------------------------|
| 1     | 0         | —         | Starting level                |
| 2     | 300       | +300      | 6 fights                      |
| 3     | 900       | +600      | 12 more fights                |
| 4     | 2,700     | +1,800    | 36 more fights                |
| 5     | 6,500     | +3,800    | 76 more fights                |

Progression slows dramatically at higher levels. Consider fighting higher CR monsters for faster advancement.

## Important Notes

- **Database location**: `~/.claude/data/dnd-dm.db`
- **XP accumulates**: Never resets, even after level-up
- **Multiple level-ups**: Single large XP award can grant multiple levels
- **Full heal on level-up**: Character restored to new max HP
- **Spell slots refresh**: All spell slots restored when leveling
- **No XP for defeat/fled**: Only victories grant XP
- **Character persistence**: XP and level tracked across sessions

## Error Handling

Handle these common scenarios:

- **Character not found**: Suggest using `character.py list`
- **No equipment**: Auto-equip starting gear
- **Bestiary/spells empty**: Run seed commands
- **Invalid CR**: Check monster CR from `start` command JSON output
- **Max level (20)**: No more XP needed, celebrate achievement!

## Reference Documentation

For detailed information on specific topics, see:

- **`references/progression-rules.md`** - Complete XP tables, level-up benefits, progression strategy, threshold triggers, and calculated growth formulas
- **Tutorial 4's `references/narrative-guide.md`** - Radio drama combat narrative (still applicable)
- **Tutorial 4's `references/spell-mechanics.md`** - Spellcasting system details
- **Tutorial 4's `references/dnd-5e-rules.md`** - D&D 5e combat rules

Load these references as needed when conducting combat encounters with character progression.

## Skill Concepts Taught

Tutorial 5 demonstrates three key skill-building concepts:

### 1. Threshold Triggers

Automatic events fire when a value crosses a threshold. When XP >= threshold → level-up happens automatically without manual intervention.

**Real-world applications:**
- Alert systems (temperature > 100°F → trigger alarm)
- Subscription tiers (usage exceeds limit → upgrade tier)
- Achievement systems (score threshold → unlock badge)

### 2. Progressive Complexity

Features unlock gradually as the system advances. Early levels come quickly with basic improvements, later levels take longer and grant more significant upgrades.

**Real-world applications:**
- SaaS product tiers (features unlock with higher plans)
- Learning systems (advanced features after basic mastery)
- Game progression (abilities unlock over time)

### 3. Calculated Growth

Growth follows deterministic formulas, not arbitrary values. Every stat increase is predictable based on class, level, and ability scores.

**Real-world applications:**
- Pricing calculators (base + usage × rate)
- Performance metrics (response time based on load formula)
- Financial modeling (compound interest calculations)
