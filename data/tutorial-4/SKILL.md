---
name: tutorial-4
description: Manage D&D 5e combat encounters with turn-based mechanics, spellcasting, attack rolls, and HP tracking. This skill should be used when the user requests to start a combat encounter, fight a monster, cast spells, enter the training arena, or engage in battle with their D&D character. Supports both weapon attacks and spell casting with spell slot management.
---

# D&D Combat System with Magic

## Overview

Orchestrate D&D 5th Edition combat encounters in a training arena setting with full spellcasting support. Handle equipment assignment, spell selection, monster selection, initiative rolls, turn-based combat with weapon attacks OR spell casting, spell slot management, and post-combat healing. Combat follows 5e rules for attack resolution (d20 + bonus vs AC), spell attacks, saving throws, and supports multiple end conditions (victory, defeat, flee, surrender).

## Available Scripts

Access six Python scripts in the `scripts/` directory:

1. **roll_dice.py** - Dice rolling (from Tutorial 1)
2. **character.py** - Character management with spell slot tracking (extended from Tutorial 2)
3. **bestiary.py** - Monster database management
4. **equipment.py** - Equipment and AC calculation
5. **spells.py** - Spell database management (NEW in Tutorial 4)
6. **combat.py** - Combat mechanics, turn resolution, and spellcasting (extended)

All scripts are located at: `~/.claude/skills/tutorial-4/scripts/`

## Spellcasting System

Tutorial 4 adds a complete spellcasting system with spell slot management and three resolution mechanics:

### Spell Types

**Cantrips (Level 0)**: Cast unlimited times, no spell slots required
- Fire Bolt, Ray of Frost, Shocking Grasp, Sacred Flame, Eldritch Blast

**Leveled Spells (Level 1+)**: Consume spell slots when cast
- Magic Missile, Burning Hands, Thunderwave, Shield, Healing Word

### Spell Resolution Mechanics

**Spell Attacks** (like Fire Bolt):
- Caster rolls d20 + spell attack bonus vs target AC
- On hit: Roll damage dice

**Saving Throws** (like Burning Hands):
- Target rolls d20 + save modifier vs caster's spell save DC
- On failed save: Take full damage
- On successful save: Take half damage (or no damage, depending on spell)

**Auto-Hit** (like Magic Missile):
- No attack roll or save required
- Automatically deals damage

### Spell Slot Management

- **Full casters** (Wizard, Sorcerer, Cleric, Druid) at level 1: 2 spell slots
- **Non-casters** (Fighter, Rogue): No spell slots
- Casting a leveled spell consumes one slot
- Long rest restores all spell slots

### Spellcasting Stats

Each spellcasting class uses a different ability:
- **Wizard**: Intelligence
- **Sorcerer/Warlock**: Charisma
- **Cleric/Druid**: Wisdom

**Formulas:**
- Spell attack bonus = Proficiency + Spellcasting Ability Modifier
- Spell save DC = 8 + Proficiency + Spellcasting Ability Modifier

For complete spell mechanics documentation, see `references/spell-mechanics.md`

## Combat Workflow

Follow this workflow when conducting a training arena combat encounter:

### Step 1: Seed Databases (First Time Only)

On first use, seed the bestiary and spell databases:

```bash
python3 ~/.claude/skills/tutorial-4/scripts/bestiary.py seed
python3 ~/.claude/skills/tutorial-4/scripts/spells.py seed
```

This adds:
- Monsters: Goblin, Skeleton (CR 1/4), Orc (CR 0.5), Zombie (CR 1/4), Rat (CR 0)
- Spells: 5 cantrips + 5 level-1 spells from `assets/data/spells_core.json`

### Step 2: Check Character Equipment

Before combat, verify the character has equipment:

```bash
python3 ~/.claude/skills/tutorial-4/scripts/equipment.py show CHARACTER_NAME
```

If no equipment found, equip starting gear based on their class:

```bash
python3 ~/.claude/skills/tutorial-4/scripts/equipment.py equip CHARACTER_NAME CLASS_NAME
```

Starting equipment by class:
- **Fighter**: Chain mail (AC 16), longsword (1d8+STR), shield (+2 AC) → Total AC 18
- **Wizard**: No armor (AC 10+DEX), quarterstaff (1d6+STR)
- **Rogue**: Leather armor (AC 11+DEX), shortsword (1d6+DEX)
- **Cleric**: Chain mail (AC 16), mace (1d6+STR), shield (+2 AC) → Total AC 18

### Step 3: Start Combat

Initialize the combat encounter:

```bash
python3 ~/.claude/skills/tutorial-4/scripts/combat.py start CHARACTER_NAME MAX_CR
```

**MAX_CR calculation**: Use `character_level / 4` as a guideline. Level 1 character = CR 0.25.

This command outputs JSON containing:
- Character stats (HP, AC, weapon, DEX modifier, spell slots if caster)
- Selected monster stats (HP, AC, attack, abilities)
- Initiative rolls for both combatants
- Who goes first ("character" or "monster")

Parse this JSON and display the combat start state to the user in narrative form.

For narrative guidance on setting the scene, see `references/narrative-guide.md`

### Step 4: Combat Loop

Execute turns in initiative order. Continue until an end condition is met.

#### Character's Turn

Ask the user what they want to do:
- **Attack** with weapon
- **Cast Spell** (cantrip or leveled spell if caster and has slots)
- **Flee** (attempt to escape)
- **Surrender** (end combat as defeat)

**To execute a weapon attack:**

```bash
python3 ~/.claude/skills/tutorial-4/scripts/combat.py character-attack CHARACTER_NAME MONSTER_NAME MONSTER_AC MONSTER_HP
```

The command outputs JSON with:
- Attack roll (natural d20, bonus, total)
- Whether it hit
- Whether it was a critical hit (natural 20)
- Damage dealt (if hit)
- Monster's HP before and after

Parse and narrate the results with dramatic descriptions.

**To cast a spell:**

First, check if character has spell slots available (for leveled spells). Cantrips don't require slots.

```bash
python3 ~/.claude/skills/tutorial-4/scripts/combat.py character-cast CHARACTER_NAME "SPELL_NAME" MONSTER_NAME MONSTER_AC MONSTER_HP 'MONSTER_STATS_JSON'
```

MONSTER_STATS_JSON must include the monster's abilities for saving throws. Get this from the start combat JSON.

The command outputs JSON with:
- Spell resolution (attack roll, saving throw, or auto-hit)
- Damage dealt
- Monster's HP before and after
- Spell slots remaining (if leveled spell)

**After casting a leveled spell**, the character's spell slots are automatically updated in the database.

For detailed spell casting narrative examples, see `references/narrative-guide.md`

#### Monster's Turn

The monster always attacks (simple AI). Execute the monster's attack:

```bash
python3 ~/.claude/skills/tutorial-4/scripts/combat.py monster-attack MONSTER_NAME MONSTER_ATTACK_BONUS MONSTER_DAMAGE CHARACTER_NAME CHARACTER_AC
```

The command outputs JSON with:
- Attack roll results
- Damage dealt (if hit)
- Character's HP before and after

The character's HP is automatically updated in the database.

Parse and narrate the monster's attack dramatically.

#### Check End Conditions

After each turn, check if combat should end:

1. **Monster HP ≤ 0**: Victory
2. **Character HP ≤ 0**: Defeat
3. **Character fled**: Escaped
4. **Character surrendered**: Defeat

If no end condition met, continue to next turn in initiative order.

### Step 5: End Combat

When combat ends, call the end combat command:

```bash
python3 ~/.claude/skills/tutorial-4/scripts/combat.py end CHARACTER_NAME OUTCOME
```

OUTCOME must be one of: `victory`, `defeat`, `fled`

**On victory or fled**: Character is automatically healed to full HP and spell slots refreshed.

**On defeat**: Character HP remains at 0 (or current value). No death saves in this tutorial - just narrative defeat.

Narrate the outcome with appropriate drama and closure.

## Core Commands Reference

### Equipment Management

**Show equipment:**
```bash
python3 ~/.claude/skills/tutorial-4/scripts/equipment.py show CHARACTER_NAME
```

**Calculate AC:**
```bash
python3 ~/.claude/skills/tutorial-4/scripts/equipment.py ac CHARACTER_NAME
```

**Get weapon stats:**
```bash
python3 ~/.claude/skills/tutorial-4/scripts/equipment.py weapon CHARACTER_NAME
```

Returns JSON with weapon name, damage dice, attack bonus, and ability modifier.

### Spell Management

**List all spells:**
```bash
python3 ~/.claude/skills/tutorial-4/scripts/spells.py list
```

**List spells by level:**
```bash
python3 ~/.claude/skills/tutorial-4/scripts/spells.py list --level 1
```

**List spells by class:**
```bash
python3 ~/.claude/skills/tutorial-4/scripts/spells.py list --class wizard
```

**Show spell details:**
```bash
python3 ~/.claude/skills/tutorial-4/scripts/spells.py show "Fire Bolt"
```

**Get spell data as JSON:**
```bash
python3 ~/.claude/skills/tutorial-4/scripts/spells.py get "Fire Bolt"
```

### Character Management

**Take long rest:**
```bash
python3 ~/.claude/skills/tutorial-4/scripts/character.py long-rest CHARACTER_NAME
```

Restores character to full HP and refreshes all spell slots.

**Show character:**
```bash
python3 ~/.claude/skills/tutorial-4/scripts/character.py show CHARACTER_NAME
```

Displays character stats including spell slots (if caster).

### Bestiary Management

**List all monsters:**
```bash
python3 ~/.claude/skills/tutorial-4/scripts/bestiary.py list
```

**List monsters by max CR:**
```bash
python3 ~/.claude/skills/tutorial-4/scripts/bestiary.py list --max-cr 0.5
```

**Show monster details:**
```bash
python3 ~/.claude/skills/tutorial-4/scripts/bestiary.py show MONSTER_NAME
```

**Add new monster:**
```bash
python3 ~/.claude/skills/tutorial-4/scripts/bestiary.py add NAME CR 'JSON_STAT_BLOCK'
```

JSON stat block format:
```json
{
    "ac": 15,
    "hp_dice": "2d6",
    "hp_avg": 7,
    "abilities": {
        "str": 8, "dex": 14, "con": 10,
        "int": 10, "wis": 8, "cha": 8
    },
    "attack": {
        "name": "Weapon Name",
        "bonus": 4,
        "damage_dice": "1d6+2",
        "damage_type": "slashing"
    }
}
```

## Narrative Style - Radio Drama

Present combat as a **radio drama** - create vivid scenes with words so the listener can see, hear, and feel the action.

### Key Principles

1. **Set atmosphere** - Describe the training arena, torchlight, tension
2. **Give monsters personality** - Based on stats and type (cunning Goblin, relentless Skeleton, shambling Zombie)
3. **Describe attacks dramatically** - Not just "hit" or "miss", but WHY and HOW
4. **Vary language** - Use rich vocabulary to avoid repetition (swing, slash, thrust, cleave, dodge, weave, parry)
5. **Match narrative to HP** - Fresh and confident at full HP, desperate and wounded at low HP
6. **Always show dice rolls** - Transparency builds trust (format: `🎲 Roll: 15 + 4 = 19 vs AC 15`)
7. **Player agency** - Make the character feel heroic and skilled

For complete narrative guidance with extensive examples, see `references/narrative-guide.md`

## Important Notes

- Database location: `~/.claude/data/dnd-dm.db`
- Monster HP is rolled fresh each combat (using hp_dice)
- Character HP is tracked persistently and updated in database
- Character automatically heals to full after victory or fleeing
- All combat scripts output JSON for easy parsing
- Initiative ties default to character going first (or use DEX as tiebreaker)

## Error Handling

Handle these common errors gracefully:

- **Character not found**: Suggest using `character.py list` to see available characters
- **No equipment**: Automatically equip starting gear for character's class
- **Bestiary empty**: Run `bestiary.py seed` to add initial monsters
- **Spells database empty**: Run `spells.py seed` to add initial spells
- **No monsters at CR**: Suggest lowering max_cr or adding monsters with `bestiary.py add`
- **No spell slots**: Suggest taking a long rest or using cantrips instead

## Reference Documentation

For detailed information on specific topics, see:

- **`references/narrative-guide.md`** - Complete radio drama narrative guide with extensive examples for combat openings, attacks, spellcasting, and endings
- **`references/spell-mechanics.md`** - Detailed spellcasting system documentation including spell types, resolution mechanics, spell slots, and class-specific spellcasting
- **`references/dnd-5e-rules.md`** - D&D 5th Edition combat rules reference including initiative, attack rolls, damage, AC calculation, proficiency bonuses, and ability scores

Load these references as needed when conducting combat encounters.
