---
name: dnd-simple-combat
description: Manage D&D 5e combat encounters with turn-based mechanics, attack rolls, and HP tracking. This skill should be used when the user requests to start a combat encounter, fight a monster, enter the training arena, or engage in battle with their D&D character.
---

# D&D Simple Combat System

## Overview

Orchestrate D&D 5th Edition combat encounters in a training arena setting. Handle equipment assignment, monster selection, initiative rolls, turn-based combat with attack and damage rolls, and post-combat healing. Combat follows 5e rules for attack resolution (d20 + bonus vs AC) and supports multiple end conditions (victory, defeat, flee, surrender).

## Available Scripts

Access five Python scripts in the `scripts/` directory:

1. **roll_dice.py** - Dice rolling (copied from Tutorial 1)
2. **character.py** - Character management (copied from Tutorial 2)
3. **bestiary.py** - Monster database management
4. **equipment.py** - Equipment and AC calculation
5. **combat.py** - Combat mechanics and turn resolution

## Combat Workflow

Follow this workflow when conducting a training arena combat encounter:

### Step 1: Seed Bestiary (First Time Only)

On first use, seed the bestiary database with initial monsters:

```bash
python3 ~/.claude/skills/dnd-simple-combat/scripts/bestiary.py seed
```

This adds Goblin and Skeleton (CR 1/4) to the bestiary.

### Step 2: Check Character Equipment

Before combat, verify the character has equipment:

```bash
python3 ~/.claude/skills/dnd-simple-combat/scripts/equipment.py show CHARACTER_NAME
```

If no equipment found, equip starting gear based on their class:

```bash
python3 ~/.claude/skills/dnd-simple-combat/scripts/equipment.py equip CHARACTER_NAME CLASS_NAME
```

Starting equipment by class:
- **Fighter**: Chain mail (AC 16), longsword (1d8+STR), shield (+2 AC)
- **Wizard**: No armor (AC 10+DEX), quarterstaff (1d6+STR)
- **Rogue**: Leather armor (AC 11+DEX), shortsword (1d6+DEX)
- **Cleric**: Chain mail (AC 16), mace (1d6+STR), shield (+2 AC)

### Step 3: Start Combat

Initialize the combat encounter:

```bash
python3 ~/.claude/skills/dnd-simple-combat/scripts/combat.py start CHARACTER_NAME MAX_CR
```

**MAX_CR calculation**: Use `character_level / 4` as a guideline. Level 1 character = CR 0.25.

This command outputs JSON containing:
- Character stats (HP, AC, weapon, DEX modifier)
- Selected monster stats (HP, AC, attack, abilities)
- Initiative rolls for both combatants
- Who goes first ("character" or "monster")

Parse this JSON and display the combat start state to the user in narrative form:
```
You enter the training arena and face a Goblin!

Initiative:
  - You rolled 14 (total: 16)
  - Goblin rolled 11 (total: 13)

You go first!

Combat State:
  - CHARACTER_NAME: 11/11 HP, AC 18
  - Goblin: 7/7 HP, AC 15
```

### Step 4: Combat Loop

Execute turns in initiative order. Continue until an end condition is met.

#### Character's Turn

Ask the user what they want to do:
- **Attack**: Proceed with attack roll
- **Flee**: Attempt to escape (DEX check or auto-succeed, designer's choice)
- **Surrender**: End combat as defeat

**To execute an attack:**

```bash
python3 ~/.claude/skills/dnd-simple-combat/scripts/combat.py character-attack CHARACTER_NAME MONSTER_NAME MONSTER_AC MONSTER_HP
```

The command outputs JSON with:
- Attack roll (natural d20)
- Attack bonus and total
- Whether it hit
- Whether it was a critical hit
- Damage dealt (if hit)
- Monster's HP before and after

Parse and narrate the results:
```
You swing your longsword at the Goblin!
  Attack roll: 15 + 4 = 19 vs AC 15
  Hit! Damage: 6 slashing

The Goblin now has 1/7 HP remaining.
```

On critical hit (natural 20), emphasize it in the narrative:
```
CRITICAL HIT! You roll damage twice!
  Damage: 12 slashing
```

#### Monster's Turn

The monster always attacks (simple AI). Execute the monster's attack:

```bash
python3 ~/.claude/skills/dnd-simple-combat/scripts/combat.py monster-attack MONSTER_NAME MONSTER_ATTACK_BONUS MONSTER_DAMAGE CHARACTER_NAME CHARACTER_AC
```

The command outputs JSON with:
- Attack roll results
- Damage dealt (if hit)
- Character's HP before and after

The character's HP is automatically updated in the database.

Parse and narrate:
```
The Goblin slashes at you with its scimitar!
  Attack roll: 12 + 4 = 16 vs AC 18
  Miss!
```

Or if it hits:
```
The Goblin slashes at you with its scimitar!
  Attack roll: 16 + 4 = 20 vs AC 18
  Hit! Damage: 5 slashing

You now have 6/11 HP remaining.
```

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
python3 ~/.claude/skills/dnd-simple-combat/scripts/combat.py end CHARACTER_NAME OUTCOME
```

OUTCOME must be one of: `victory`, `defeat`, `fled`

**On victory or fled**: Character is automatically healed to full HP.

**On defeat**: Character HP remains at 0 (or current value). No death saves in this tutorial - just narrative defeat.

Narrate the outcome:
```
Victory! The Goblin falls to the ground, defeated.
You have been fully healed and are ready for your next challenge.

Final HP: 11/11
```

## Equipment Management Commands

### Show Equipment
```bash
python3 ~/.claude/skills/dnd-simple-combat/scripts/equipment.py show CHARACTER_NAME
```

### Calculate AC
```bash
python3 ~/.claude/skills/dnd-simple-combat/scripts/equipment.py ac CHARACTER_NAME
```

Outputs just the AC number.

### Get Weapon Stats
```bash
python3 ~/.claude/skills/dnd-simple-combat/scripts/equipment.py weapon CHARACTER_NAME
```

Outputs JSON with weapon name, damage dice, attack bonus, and ability modifier.

## Bestiary Management Commands

### List All Monsters
```bash
python3 ~/.claude/skills/dnd-simple-combat/scripts/bestiary.py list
```

### List Monsters by Max CR
```bash
python3 ~/.claude/skills/dnd-simple-combat/scripts/bestiary.py list --max-cr 0.5
```

### Show Monster Details
```bash
python3 ~/.claude/skills/dnd-simple-combat/scripts/bestiary.py show MONSTER_NAME
```

### Add New Monster
```bash
python3 ~/.claude/skills/dnd-simple-combat/scripts/bestiary.py add NAME CR 'JSON_STAT_BLOCK'
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

## Combat Rules Reference (5e)

### Initiative
- Roll d20 + DEX modifier
- Higher total goes first
- On tie, higher DEX goes first (or re-roll)

### Attack Rolls
- Roll d20 + proficiency bonus + ability modifier
- Compare to target's AC
- Meet or exceed AC = hit
- Natural 20 = automatic critical hit (roll damage dice twice)
- Natural 1 = automatic miss

### Damage Rolls
- Roll weapon damage dice + ability modifier
- On critical hit, roll damage dice twice, then add modifier once
- Subtract damage from target's current HP

### Proficiency Bonus by Level
- Levels 1-4: +2
- Levels 5-8: +3
- Levels 9-12: +4
- Levels 13-16: +5
- Levels 17-20: +6

### AC Calculation
- **Unarmored**: 10 + DEX modifier
- **Light armor** (e.g., leather): Base AC + full DEX modifier
- **Heavy armor** (e.g., chain mail): Base AC only (no DEX)
- **Shield**: +2 AC bonus (stacks with armor)

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
- **No monsters at CR**: Suggest lowering max_cr or adding monsters with `bestiary.py add`

## Radio Drama Narrative Style

Present combat as a **radio drama** - paint vivid pictures with words so the listener can see, hear, and feel the action. Act as a Dungeon Master bringing the scene to life.

### Combat Opening (Step 3 - Start Combat)

Create atmosphere using the combat data:

**Set the Scene:**
- Describe the training arena environment (torchlight, weapon racks, sand underfoot)
- Build anticipation as the character enters
- Reveal the monster dramatically based on its type and CR

**Monster Introduction:**
- Use the monster's stats to inform description (high DEX = quick/agile, high STR = hulking/powerful)
- Describe appearance, movement, demeanor
- Create personality (Goblin = cunning/nasty, Skeleton = relentless/hollow, Zombie = shambling/groaning, Orc = fierce/aggressive)

**Initiative Drama:**
- Describe the tense moment before combat begins
- Use initiative rolls to narrate who strikes first and WHY (high roll = lightning reflexes, low roll = caught off guard)
- Build tension: "Who will strike first?"

**Example Opening:**
```
⚔️  TRAINING ARENA ⚔️

The heavy wooden doors creak open, and Bob steps into the torch-lit arena.
Sand crunches beneath his boots. The air smells of sweat and steel.

From the shadows across the arena, a hunched figure emerges—a Goblin!
Its yellow eyes gleam with malicious intelligence as it draws a wicked
curved scimitar. The creature cackles, crouching low,ready to pounce.

The tension is palpable. Both warriors eye each other, muscles coiled...

Initiative:
- Bob rolled 15 + 1 (DEX) = 16
- Goblin rolled 20 + 2 (DEX) = 22

The Goblin EXPLODES into motion with startling speed! Bob barely has time
to raise his shield before the creature is upon him!

Combat State:
- Bob: 11/11 HP, AC 18 - Armored and ready
- Goblin: 11/11 HP, AC 15 - Fast and dangerous
```

### During Combat (Step 4 - Combat Loop)

**Attack Declarations:**
Describe the action BEFORE showing the dice roll:
- Character positioning and movement
- Weapon grip, stance, facial expression
- Intent (desperate, calculated, furious)
- Environmental details (dust kicked up, torchlight glinting on steel)

**Attack Results - HITS:**
- Describe the impact viscerally (blade biting flesh, crunch of bone, spray of blood)
- Monster/character reactions (howl of pain, grimace, stagger)
- Use damage amount to inform severity (1-3 dmg = glancing, 4-7 = solid hit, 8+ = devastating)
- Show HP changes dramatically ("The Goblin's knees buckle!" for low HP)

**Attack Results - MISSES:**
- Never say just "miss" - describe WHY
  - Armor deflection: "The blade skitters off chain mail"
  - Dodge: "The Goblin twists aside at the last instant"
  - Parry: "Metal rings against metal as weapons clash"
  - Near-miss: "The sword whistles past, missing by inches"
- Build tension with close calls

**Critical Hits:**
- MAXIMUM DRAMA
- Slow down time, describe the perfect opening
- Epic impact description
- Use dramatic formatting (⚡💥🔥)

**HP Status Narration:**
- **75-100% HP**: Fresh, confident, strong
- **50-74% HP**: Bloodied, breathing hard, determined
- **25-49% HP**: Wounded, desperate, fighting for survival
- **1-24% HP**: Barely standing, eyes wild, on death's door
- **0 HP**: Describe the fall, the final moment

**Vary Your Language:**
Avoid repetition. Use synonyms and varied sentence structure:
- Attack verbs: swing, slash, thrust, strike, lunge, cleave, drive, plunge
- Movement: dodge, weave, duck, sidestep, roll, leap, pivot
- Sounds: clang, ring, thud, crack, whistle, crunch, scrape
- Sensory: flash of steel, spray of blood, cloud of dust, bitter tang of fear

### Victory/Defeat (Step 5 - End Combat)

**Victory:**
- Describe the killing blow in detail
- Monster's final moment (collapse, dissolve, shatter based on type)
- Character's reaction (relief, triumph, exhaustion)
- Transition to healing with a moment of peace

**Defeat:**
- Describe the character overwhelmed
- Respectful narration of loss
- Focus on the lesson learned

**Example Victory:**
```
Bob sees his opening—the Goblin overextends on a wild slash. He pivots,
bringing his longsword down in a brutal overhead chop!

🎲 Attack roll: 19 + 5 = 24 vs AC 15
💥 DEVASTATING HIT!

The blade cleaves through the Goblin's collarbone with a sickening CRUNCH.
The creature's eyes go wide, its scimitar clattering to the sand. It
crumples, twitching once, then still.

Silence falls over the arena. Bob lowers his sword, chest heaving. Victory.

🏆 The battle is won! Golden light washes over Bob as his wounds close.
He stands ready for whatever comes next.

Final Status: Bob 11/11 HP - Victorious and renewed!
```

### Important Guidelines

1. **Always show dice rolls** - Transparency builds trust
2. **Status updates after every action** - Clear HP tracking
3. **Pacing** - Short sentences for action, longer for atmosphere
4. **Emotion** - Characters should feel fear, determination, relief
5. **Consistency** - Match narrative tone to monster type (Goblin = scrappy, Skeleton = eerie, Zombie = relentless, Orc = brutal)
6. **Player agency** - Make the player character feel heroic, skilled, and in control of their choices
