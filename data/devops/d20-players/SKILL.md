---
name: d20-players
description: This skill should be used when the GM needs to help players create characters, roll for stats, assign ability scores, handle leveling up, increase hit points, choose classes, pick proficiencies, or manage player character creation, advancement, or character sheet management. Provides templates and rules for SRD 5.2 character creation and leveling.
version: 1.0.0
---

# Character Creation and Advancement Skill

Guide players through creating and advancing d20 system characters following SRD 5.2 rules.

## File Structure

Character files follow the corvran directory structure with D20-specific content:

```
players/
  {character-slug}/
    sheet.md   # Use sheet-template.md format (stats, abilities, equipment, current HP, conditions)
    story.md   # Use story-template.md format (objectives, story arcs, recent events)
```

The `sheet.md` contains character data including current game state (HP, conditions, spell slots). The `story.md` tracks narrative elements like objectives and story arcs.

## Character Creation Overview

Follow these five steps to create a new character:

1. **Choose a Class** - Determines primary abilities, hit die, proficiencies, and features
2. **Determine Origin** - Select background (grants feat, skills, tool) and species (grants traits, size, speed)
3. **Determine Ability Scores** - Generate six scores and assign to abilities
4. **Choose Alignment** - Select moral and ethical outlook
5. **Fill in Details** - Calculate derived stats and record equipment

## Generating Ability Scores

Offer three methods to generate the six ability scores.

### Standard Array
Use these six scores, assigning each to one ability: **15, 14, 13, 12, 10, 8**

### Random Generation
For each of the six abilities, roll 4d6 and sum the highest three dice:

```bash
bash "${CLAUDE_PLUGIN_ROOT}/../corvran/skills/dice-roller/scripts/roll.sh" "4d6"
```

Parse the JSON output, discard the lowest roll, and sum the remaining three. Repeat six times.

### Point Buy
Start with 27 points. Each ability starts at 8 (free). Costs to increase:

| Score | Total Cost | Score | Total Cost |
|-------|------------|-------|------------|
| 8     | 0          | 12    | 4          |
| 9     | 1          | 13    | 5          |
| 10    | 2          | 14    | 7          |
| 11    | 3          | 15    | 9          |

## Calculating Derived Statistics

After assigning ability scores, calculate these values:

### Ability Modifier
```
Modifier = (Score - 10) / 2, rounded down
```

| Score   | Modifier | Score   | Modifier |
|---------|----------|---------|----------|
| 8-9     | -1       | 14-15   | +2       |
| 10-11   | +0       | 16-17   | +3       |
| 12-13   | +1       | 18-19   | +4       |

### Proficiency Bonus by Level

| Level | Bonus | Level | Bonus |
|-------|-------|-------|-------|
| 1-4   | +2    | 13-16 | +5    |
| 5-8   | +3    | 17-20 | +6    |
| 9-12  | +4    |       |       |

### Hit Points at Level 1

| Class                                        | HP at Level 1        |
|----------------------------------------------|----------------------|
| Barbarian                                    | 12 + CON modifier    |
| Fighter, Paladin, Ranger                     | 10 + CON modifier    |
| Bard, Cleric, Druid, Monk, Rogue, Warlock    | 8 + CON modifier     |
| Sorcerer, Wizard                             | 6 + CON modifier     |

### Armor Class (AC)

Without armor: **10 + DEX modifier**

With armor, use the armor's AC formula from the equipment tables.

### Initiative
**Initiative = DEX modifier**

### Saving Throws
Each class grants proficiency in two saving throws. For proficient saves:
```
Save Bonus = Ability Modifier + Proficiency Bonus
```

### Skills
For proficient skills:
```
Skill Bonus = Ability Modifier + Proficiency Bonus
```

### Passive Perception
```
Passive Perception = 10 + Wisdom (Perception) modifier
```

## Recording the Character

Write character data to `players/{character-slug}/sheet.md` using the D20 template:

```
references/sheet-template.md
```

For a completed example, see:
```
references/sheet-example.md
```

### D20 Sheet Sections

The sheet.md file must include:

1. **Character Identity** - Name, class, level, species, background, alignment
2. **Ability Scores** - All six scores with modifiers
3. **Combat Stats** - AC, HP (current/max), Hit Dice, Initiative, Speed
4. **Proficiencies** - Saving throws, skills, weapons, armor, tools, languages
5. **Features & Traits** - Class features, species traits, background feat
6. **Equipment** - Weapons with attack/damage, armor, gear, currency
7. **Spellcasting** (if applicable) - Ability, DC, attack bonus, slots, spells known

## Level Advancement

When a character gains enough XP to level up:

### Experience Thresholds

| Level | XP Required | Level | XP Required |
|-------|-------------|-------|-------------|
| 2     | 300         | 11    | 85,000      |
| 3     | 900         | 12    | 100,000     |
| 4     | 2,700       | 13    | 120,000     |
| 5     | 6,500       | 14    | 140,000     |
| 6     | 14,000      | 15    | 165,000     |
| 7     | 23,000      | 16    | 195,000     |
| 8     | 34,000      | 17    | 225,000     |
| 9     | 48,000      | 18    | 265,000     |
| 10    | 64,000      | 19    | 305,000     |
|       |             | 20    | 355,000     |

### Level Up Steps

1. **Increase Hit Points** - Roll Hit Die + CON modifier (or use fixed value):

Roll HP:
```bash
bash "${CLAUDE_PLUGIN_ROOT}/../corvran/skills/dice-roller/scripts/roll.sh" "1d10"
```

Fixed HP values per level:
| Class                                        | HP per Level         |
|----------------------------------------------|----------------------|
| Barbarian                                    | 7 + CON modifier     |
| Fighter, Paladin, Ranger                     | 6 + CON modifier     |
| Bard, Cleric, Druid, Monk, Rogue, Warlock    | 5 + CON modifier     |
| Sorcerer, Wizard                             | 4 + CON modifier     |

2. **Gain Hit Die** - Add one Hit Die to your pool
3. **Check Proficiency Bonus** - Increases at levels 5, 9, 13, 17
4. **Record New Features** - Add class features for the new level
5. **Choose Subclass** (Level 3) - Record subclass features
6. **Ability Score Improvement** (Levels 4, 8, 12, 16, 19) - Increase one score by 2 or two scores by 1, or choose a feat

## Multiclassing

To take a level in a new class:

1. **Check Prerequisites** - Must have 13+ in primary abilities of both current and new class
2. **Gain Limited Proficiencies** - Only some proficiencies from the new class
3. **Calculate Spellcasting** - Combine levels per multiclass spellcaster rules

## Rolling During Character Creation

Use the dice-roller skill for all randomization:

**Ability Score (4d6 drop lowest)**:
```bash
bash "${CLAUDE_PLUGIN_ROOT}/../corvran/skills/dice-roller/scripts/roll.sh" "4d6"
```

**Starting Gold (if not using equipment packs)**:
```bash
bash "${CLAUDE_PLUGIN_ROOT}/../corvran/skills/dice-roller/scripts/roll.sh" "5d4"
```

**Trinket Roll**:
```bash
bash "${CLAUDE_PLUGIN_ROOT}/../corvran/skills/dice-roller/scripts/roll.sh" "1d100"
```

## Fallback Without Dice Roller

If the corvran dice-roller is unavailable, describe the required roll and ask the player for the result:

> "Roll 4d6 and tell me the results. We'll drop the lowest die and sum the rest for your ability score."

## References

Detailed rules in this skill's `references/` directory:

- `character-creation.md` - Complete SRD 5.2 character creation rules
- `sheet-template.md` - Blank character sheet template
- `story-template.md` - Character story template (objectives, arcs, events)
- `sheet-example.md` - Completed Level 3 Fighter example
