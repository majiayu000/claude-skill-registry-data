---
name: d20-monsters
description: This skill should be used when the GM needs to create NPCs or monsters, generate stat blocks, determine enemy stats, design creatures, or generate adversaries for d20-style RPG encounters. Provides SRD 5.2 stat block format and NPC templates.
version: 1.0.0
---

# Monster and NPC Creation Skill

Create monsters, NPCs, and adversaries using the SRD 5.2 stat block format. This skill provides the standard format, reference tables, and templates for generating balanced creatures.

## When to Use This Skill

This skill applies when:
- Creating a new monster or NPC for an encounter
- Converting a narrative concept into game statistics
- Generating stat blocks for adversaries
- Balancing creatures for specific Challenge Ratings
- Looking up stat block format requirements

## Stat Block Format Overview

Every creature stat block follows this structure:

1. **Name and General Details**: Name, size, type, tags, alignment
2. **Combat Highlights**: AC, HP (with hit dice), Speed, Initiative
3. **Ability Scores**: Six abilities with scores, modifiers, and saves
4. **Additional Details**: Skills, resistances, immunities, gear, senses, languages, CR
5. **Traits**: Passive or conditional special abilities
6. **Actions**: What the creature does on its turn
7. **Bonus Actions**: Quick actions (optional)
8. **Reactions**: Triggered responses (optional)
9. **Legendary Actions**: For powerful creatures (optional)

Load the full format specification from `references/stat-blocks.md` when detailed guidance is needed.

## Quick Reference Tables

### Challenge Rating, XP, and Proficiency Bonus

| CR | XP | PB | CR | XP | PB |
|----|----|----|----|----|-----|
| 0 | 10 | +2 | 6 | 2,300 | +3 |
| 1/8 | 25 | +2 | 7 | 2,900 | +3 |
| 1/4 | 50 | +2 | 8 | 3,900 | +3 |
| 1/2 | 100 | +2 | 9 | 5,000 | +4 |
| 1 | 200 | +2 | 10 | 5,900 | +4 |
| 2 | 450 | +2 | 11 | 7,200 | +4 |
| 3 | 700 | +2 | 12 | 8,400 | +4 |
| 4 | 1,100 | +2 | 13 | 10,000 | +5 |
| 5 | 1,800 | +3 | 14+ | See stat-blocks.md | +5 to +9 |

### Hit Dice by Size

| Size | Hit Die | Avg HP/Die |
|------|---------|------------|
| Tiny | d4 | 2.5 |
| Small | d6 | 3.5 |
| Medium | d8 | 4.5 |
| Large | d10 | 5.5 |
| Huge | d12 | 6.5 |
| Gargantuan | d20 | 10.5 |

### Creature Types

Aberration, Beast, Celestial, Construct, Dragon, Elemental, Fey, Fiend, Giant, Humanoid, Monstrosity, Ooze, Plant, Undead

## Creating a Monster: Step by Step

### Step 1: Define the Concept

Determine the creature's narrative role:
- What does it look like?
- How does it fight (brute, skirmisher, caster, support)?
- What makes it interesting or unique?

### Step 2: Choose CR and Calculate Base Statistics

Target CR determines the creature's power level. Use these benchmarks:

| CR | HP Range | AC | Attack Bonus | Damage/Round | Save DC |
|----|----------|-----|--------------|--------------|---------|
| 1/4 | 10-20 | 12-13 | +3 to +4 | 4-5 | 10-11 |
| 1 | 25-45 | 13-14 | +4 to +5 | 9-14 | 12-13 |
| 5 | 80-110 | 15-16 | +6 to +8 | 35-45 | 14-15 |
| 10 | 180-220 | 17-18 | +9 to +10 | 65-75 | 17-18 |

### Step 3: Assign Ability Scores

Distribute scores based on creature role:

**Brute** (high STR/CON): 16, 14, 14, 10, 10, 8
**Skirmisher** (high DEX): 10, 16, 14, 10, 12, 8
**Caster** (high mental): 8, 14, 14, 16, 12, 10
**Balanced**: 12, 12, 12, 10, 10, 10

Calculate modifiers: **(Score - 10) / 2** rounded down.

### Step 4: Determine AC and HP

**Armor Class:**
- Base AC = 10 + DEX modifier
- Add armor bonus (light +1, medium +3-5, heavy +6-8)
- Add shield (+2)
- Natural armor replaces base calculation

**Hit Points:**
- Choose number of Hit Dice based on desired HP
- HP = (Hit Dice x average per die) + (Hit Dice x CON modifier)

### Step 5: Design Actions

Every creature needs at least one attack. Calculate:

**Attack Bonus** = Ability modifier + Proficiency Bonus
**Damage** = Dice + Ability modifier

For melee: usually STR-based
For ranged: usually DEX-based
For finesse weapons: attacker chooses STR or DEX

### Step 6: Add Special Abilities

Add traits, bonus actions, or reactions that reinforce the creature concept. Common options:

- **Pack Tactics**: Advantage when ally is adjacent
- **Nimble Escape**: Disengage or Hide as bonus action
- **Magic Resistance**: Advantage on saves vs spells
- **Multiattack**: Multiple attacks per turn
- **Spellcasting**: Access to spells

### Step 7: Validate CR

Compare your creature's statistics to the CR benchmarks. Adjust if the offensive or defensive capabilities don't match the target CR.

## Using the Templates

### NPC Template

Load `references/npc-template.md` for a complete template with inline comments explaining each field. Copy the template and fill in values for your creature.

### Example Stat Block

Load `references/npc-example.md` for a complete Goblin Warrior stat block with detailed breakdown of how each value was calculated.

## Rolling Dice for HP and Damage

Use the corvran dice-roller skill for randomized values:

```bash
# Roll HP for a creature with 3d8 + 6
bash "${CLAUDE_PLUGIN_ROOT}/../corvran/skills/dice-roller/scripts/roll.sh" "3d8+6"

# Roll damage for a longsword attack (1d8 + 3)
bash "${CLAUDE_PLUGIN_ROOT}/../corvran/skills/dice-roller/scripts/roll.sh" "1d8+3"

# Roll 2d6 for greatsword damage
bash "${CLAUDE_PLUGIN_ROOT}/../corvran/skills/dice-roller/scripts/roll.sh" "2d6+4"
```

The dice roller outputs JSON with the total and individual rolls for narration.

If the dice-roller skill is unavailable, describe the required roll and ask the player to provide the result.

## Common Stat Block Patterns

### Simple Melee Combatant (CR 1/4)

```
AC: 13 (leather armor)
HP: 11 (2d8 + 2)
Speed: 30 ft.
STR 14 (+2), DEX 12 (+1), CON 12 (+1)
Attack: +4 to hit, 1d8 + 2 damage
```

### Ranged Attacker (CR 1/2)

```
AC: 14 (leather armor)
HP: 16 (3d8 + 3)
Speed: 30 ft.
STR 10 (+0), DEX 16 (+3), CON 12 (+1)
Attack: +5 to hit, range 80/320 ft., 1d8 + 3 damage
```

### Tough Brute (CR 2)

```
AC: 12 (natural armor)
HP: 45 (6d10 + 12)
Speed: 30 ft.
STR 18 (+4), DEX 8 (-1), CON 15 (+2)
Multiattack: Two slam attacks
Attack: +6 to hit, 2d6 + 4 damage
```

### Spellcaster (CR 3)

```
AC: 12 (15 with mage armor)
HP: 27 (6d8)
Speed: 30 ft.
INT 16 (+3), WIS 12 (+1), CON 10 (+0)
Spellcasting: INT-based, DC 13, +5 to hit
Spells: mage armor, magic missile, fireball (3rd level)
```

## Recording NPCs

After creating a stat block, add it to the adventure's `characters.md` file for reference during play. Include:
- Full stat block
- Location where the NPC can be found
- Role in the story
- Disposition toward the player

## License

This work includes material from the System Reference Document 5.2.1 ("SRD 5.2.1") by Wizards of the Coast LLC. The SRD 5.2.1 is licensed under CC-BY-4.0.
