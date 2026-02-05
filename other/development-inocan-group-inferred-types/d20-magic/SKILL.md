---
name: d20-magic
description: This skill should be used when the GM needs to handle spellcasting situations, including resolving spell effects, managing spell slots, calculating spell save DCs, handling concentration, resolving spell attacks, determining spellcasting abilities, handling cantrips, or processing ritual casting. Provides spellcasting rules, formulas, and references for running magical gameplay.
version: 1.0.0
---

# Spellcasting Skill

Provides guidance for handling spellcasting in d20 system adventures. Use this skill when players cast spells, manage spell resources, or when you need to resolve magical effects.

## Core Formulas

These formulas are essential for all spellcasting. The spellcasting ability depends on class: Intelligence (Wizard), Wisdom (Cleric, Druid, Ranger), or Charisma (Bard, Paladin, Sorcerer, Warlock).

### Spell Save DC

When a spell forces a target to make a saving throw:

```
Spell Save DC = 8 + Proficiency Bonus + Spellcasting Ability Modifier
```

**Example**: A level 5 Wizard with Intelligence 18 (+4 modifier) has proficiency bonus +3.
- Spell Save DC = 8 + 3 + 4 = **15**

### Spell Attack Modifier

When a spell requires an attack roll against a target:

```
Spell Attack Modifier = Proficiency Bonus + Spellcasting Ability Modifier
```

**Example**: Same level 5 Wizard with Intelligence 18.
- Spell Attack Modifier = 3 + 4 = **+7**

To make a spell attack, use the dice-roller skill:

```bash
bash "${CLAUDE_PLUGIN_ROOT}/skills/dice-roller/scripts/roll.sh" "1d20+7"
```

Compare the result against the target's Armor Class (AC).

## Spell Slots

Spell slots represent a caster's magical energy. Each level 1+ spell requires expending a slot of that level or higher.

### Key Rules

1. **Expending Slots**: Casting a level 1+ spell uses one slot of the spell's level or higher
2. **Recovery**: All expended slots return after a Long Rest
3. **Upcasting**: Spells cast with higher-level slots often deal more damage or have enhanced effects
4. **One Spell per Turn**: You can only expend one spell slot per turn (cantrips don't use slots)

### Slot Availability

See `references/spellcasting.md` for complete spell slot tables by class and level.

**Full Casters** (Bard, Cleric, Druid, Sorcerer, Wizard): Access spell levels 1-9, gain slots at every level.

**Half Casters** (Paladin, Ranger): Access spell levels 1-5, gain first slot at level 1 (Ranger) or level 2 (Paladin), progress more slowly.

**Warlocks**: Use Pact Magic with fewer slots that recharge on Short Rest. See references for details.

## Cantrips

Cantrips are level 0 spells that don't consume spell slots.

- **At-Will Casting**: Can be cast unlimited times
- **Damage Scaling**: Damage cantrips increase at levels 5, 11, and 17
- **No Upcasting**: Cantrips cannot be cast at higher levels

**Cantrip Damage Scaling Example** (Fire Bolt):
| Character Level | Damage |
|-----------------|--------|
| 1-4             | 1d10   |
| 5-10            | 2d10   |
| 11-16           | 3d10   |
| 17+             | 4d10   |

## Concentration

Many powerful spells require concentration to maintain their effects.

### Concentration Rules

1. **One at a Time**: You can only concentrate on one spell at a time
2. **Duration**: The spell description specifies maximum concentration time
3. **Voluntary End**: You can end concentration at any time (no action required)

### Breaking Concentration

Concentration ends immediately if:

- **New Concentration Spell**: You cast another spell requiring concentration
- **Damage Taken**: You must make a Constitution saving throw to maintain concentration
- **Incapacitated**: You gain the Incapacitated condition
- **Death**: You die

### Concentration Saving Throws

When you take damage while concentrating:

```
Constitution Save DC = Higher of: 10 OR (Damage Taken / 2)
```

Maximum DC is 30 (from 60+ damage).

**Example**: A Wizard concentrating on Haste takes 18 damage.
- DC = max(10, 18/2) = max(10, 9) = **DC 10**

Roll the concentration save:

```bash
bash "${CLAUDE_PLUGIN_ROOT}/skills/dice-roller/scripts/roll.sh" "1d20+2"
```

(Assuming Constitution save modifier of +2)

If the save fails, the spell ends immediately.

## Spell Attack Procedure

When a spell requires an attack roll:

1. **Calculate modifier**: Proficiency Bonus + Spellcasting Ability Modifier
2. **Roll attack**: Use dice-roller with `1d20+[modifier]`
3. **Compare to AC**: Meet or exceed target's AC to hit
4. **Roll damage**: If hit, roll damage dice specified by the spell

**Example**: Casting Chromatic Orb (ranged spell attack, 3d8 damage)

```bash
# Attack roll with +7 modifier
bash "${CLAUDE_PLUGIN_ROOT}/skills/dice-roller/scripts/roll.sh" "1d20+7"
# If result >= target AC, roll damage
bash "${CLAUDE_PLUGIN_ROOT}/skills/dice-roller/scripts/roll.sh" "3d8"
```

## Saving Throw Spells

When a spell requires the target to make a saving throw:

1. **Announce the DC**: Use caster's Spell Save DC
2. **Identify ability**: The spell specifies which ability (Dex, Con, Wis, etc.)
3. **Target rolls**: Roll 1d20 + target's saving throw modifier
4. **Resolve effect**: Spell description states what happens on success/failure

**Example**: Fireball (Dex save, DC 15)
- Target has Dexterity save +3
- Roll: 1d20+3 = 14 (fails, takes full 8d6 fire damage)
- If rolled 15+: Success, takes half damage

## Ritual Casting

Spells with the Ritual tag can be cast without expending a slot.

### Ritual Rules

- **Extended Time**: Takes 10 minutes longer than normal casting time
- **No Slot Used**: Doesn't expend a spell slot
- **Must Be Prepared**: Most classes require the spell to be prepared
- **No Upcasting**: Ritual casting uses the spell's base level only

Classes with ritual casting: Bard, Cleric, Druid, Wizard (from spellbook without preparation).

## Spellcasting Components

Spells require specific components to cast:

| Component | Requirement |
|-----------|-------------|
| **V** (Verbal) | Must speak incantations; cannot cast if silenced |
| **S** (Somatic) | Must have free hand for gestures |
| **M** (Material) | Must have specified material or spellcasting focus |

**Focus Substitution**: A spellcasting focus (arcane focus, holy symbol, druidic focus) can replace material components that don't have a gold cost and aren't consumed.

## Quick Reference

| Situation | Formula |
|-----------|---------|
| Spell Save DC | 8 + Proficiency + Ability Mod |
| Spell Attack | 1d20 + Proficiency + Ability Mod |
| Concentration DC (damage) | Max(10, Damage/2), cap 30 |

## References

For detailed spell slot tables and class-specific spellcasting features, see:
- `references/spellcasting.md` - Complete spell slot progression tables
- `references/srd/07_Spells.md` - Full spell descriptions
- `references/srd/03_Classes/` - Class-specific spellcasting rules
