---
name: tutorial-6
description: Manage D&D 5e party-based encounters with multiple heroes vs multiple monsters. Teaches collection management, priority queues (initiative), and state synchronization through interactive JSON-driven combat. Players control characters, AI controls monsters.
---

# D&D Party Encounter System

## Overview

Orchestrate full D&D 5th Edition party combat encounters where 3-5 player characters face off against 2-5+ monsters. Handle initiative-based turn order (priority queue), manage multiple combatant states simultaneously (collection management), and keep all entity states synchronized. This tutorial teaches three critical skill-building concepts through tactical party combat.

## Available Scripts

Access seven Python scripts in the `scripts/` directory:

1. **roll_dice.py** - Dice rolling (from Tutorial 1)
2. **character.py** - Character management with party_id field (extended from Tutorial 5)
3. **party.py** - **NEW**: Party creation and roster management
4. **bestiary.py** - Monster database (from Tutorial 5)
5. **equipment.py** - Equipment and AC (from Tutorial 3)
6. **spells.py** - Spell database (from Tutorial 4)
7. **encounter.py** - **NEW**: Interactive party combat with JSON-driven state

All scripts are located at: `~/.claude/skills/tutorial-6/scripts/`

## Tutorial 6 Core Concepts

Tutorial 6 introduces party-based combat and teaches three key skill-building concepts:

###  1. Collection Management
Managing multiple related entities with synchronized state. Track 5-10 combatants simultaneously, each with their own HP, AC, position, and status.

**Real-world applications:**
- Multi-user systems (chat rooms, collaborative editing)
- Inventory management (tracking stock across warehouses)
- Fleet management (vehicle tracking, delivery routes)
- Task queues (multiple workers processing jobs)

### 2. Priority Queues
Ordered processing based on dynamic priorities, not arrival time. Initiative system: roll 1d20 + DEX at combat start, act in order from highest to lowest.

**Real-world applications:**
- Task scheduling (CPU schedulers, job priorities)
- Emergency response (triage systems, priority 1-5)
- Customer support (premium customers served first)
- Network routing (QoS classes for packets)

### 3. State Synchronization
Keeping multiple interdependent states consistent across operations. When one combatant is defeated, update HP, defeated status, initiative order, and check victory conditions—all synchronized.

**Real-world applications:**
- Distributed systems (database replication, node synchronization)
- Transaction management (all-or-nothing updates)
- UI state management (React/Vue component state)
- Multiplayer games (player positions, game state broadcast)

For detailed explanations and code examples, see:
- `references/collection-management.md`
- `references/priority-queues.md`
- `references/state-synchronization.md`

## Party Combat Workflow

Follow this workflow for interactive party encounters:

### Step 1: Create Party (One-Time Setup)

Create a party and add characters:

```bash
# Create party
python3 ~/.claude/skills/tutorial-6/scripts/party.py create heroes "The Heroes" --description "Brave adventurers"

# Add members
python3 ~/.claude/skills/tutorial-6/scripts/party.py add heroes Aria
python3 ~/.claude/skills/tutorial-6/scripts/party.py add heroes Theron
python3 ~/.claude/skills/tutorial-6/scripts/party.py add heroes Bob

# View party
python3 ~/.claude/skills/tutorial-6/scripts/party.py show heroes
```

**Alternative:** Characters can be created with party assignment:
```bash
python3 scripts/character.py create "Aria" wizard --str 8 --dex 14 --con 12 --int 16 --wis 13 --cha 10 --party heroes
```

### Step 2: Seed Databases (First Time Only)

```bash
python3 ~/.claude/skills/tutorial-6/scripts/bestiary.py seed
python3 ~/.claude/skills/tutorial-6/scripts/spells.py seed
```

### Step 3: Export Party to JSON

```bash
python3 ~/.claude/skills/tutorial-6/scripts/party.py export heroes > heroes.json
```

**Output (heroes.json):**
```json
{
  "heroes": [
    {
      "name": "Aria",
      "class": "wizard",
      "level": 1,
      "hp_max": 8,
      "hp_current": 8,
      "ac": 12,
      "abilities": {"str": 8, "dex": 14, "con": 12, "int": 16, "wis": 13, "cha": 10}
    },
    ...
  ]
}
```

### Step 4: Build Encounter (Export Foes to JSON)

```bash
# Export 3 goblins (auto-numbered: Goblin-1, Goblin-2, Goblin-3)
python3 ~/.claude/skills/tutorial-6/scripts/bestiary.py export Goblin Goblin Goblin > foes.json

# Or use pre-made encounter JSON files
cp ~/.claude/skills/tutorial-6/examples/foes-goblin-ambush.json foes.json
```

**Alternative:** Manually create foes.json with custom monsters.

### Step 5: Start Encounter

```bash
python3 ~/.claude/skills/tutorial-6/scripts/encounter.py start heroes.json foes.json
```

**Output:**
```
============================================================
ENCOUNTER STARTED!
============================================================

Initiative Order:
   1. [18] 👤 Theron              (d20: 17, DEX: +1)
   2. [16] 👹 Goblin-1             (d20: 14, DEX: +2)
   3. [14] 👤 Aria                 (d20: 12, DEX: +2)
   4. [12] 👹 Goblin-2             (d20: 10, DEX: +2)
   5. [ 9] 👤 Bob                  (d20: 9, DEX: +0)
   6. [ 8] 👹 Goblin-3             (d20: 6, DEX: +2)

============================================================

Round 1
Turn: Theron (Hero)
HP: 13/13

Available actions:
  encounter.py attack Theron TARGET
  encounter.py show

Targets:
  • Goblin-1 (HP: 7/7, AC: 15)
  • Goblin-2 (HP: 7/7, AC: 15)
  • Goblin-3 (HP: 7/7, AC: 15)
```

### Step 6: Combat Loop (Interactive Turns)

**Hero Turn (Player Controls):**
```bash
# Player decides action
python3 ~/.claude/skills/tutorial-6/scripts/encounter.py attack Theron Goblin-1 longsword
```

**Output:**
```
Theron attacks Goblin-1 with longsword!
  Attack roll: 1d20+5 = 19
  HIT! Damage: 1d8+3 = 9
  Goblin-1: 7 → 0 HP
  💀 Goblin-1 has been DEFEATED!

Goblin-2 attacks Theron!
  Attack roll: 1d20+4 = 12
  MISS! (AC 16)

Goblin-3 attacks Theron!
  Attack roll: 1d20+4 = 18
  HIT! Damage: 1d6+2 = 5
  Theron: 13 → 8 HP

Round 1
Turn: Aria (Hero)
HP: 8/8

Available actions:
  encounter.py attack Aria TARGET
  encounter.py cast Aria SPELL TARGET
  encounter.py show

Targets:
  • Goblin-2 (HP: 7/7, AC: 15)
  • Goblin-3 (HP: 7/7, AC: 15)
```

**Spellcasting:**
```bash
python3 ~/.claude/skills/tutorial-6/scripts/encounter.py cast Aria "Fire Bolt" Goblin-2
```

**Monster Turns (AI-Controlled):**
Monsters act automatically, targeting the hero with lowest HP. No user input required—encounter.py handles monster turns and advances to next player turn.

### Step 7: View State Anytime

```bash
python3 ~/.claude/skills/tutorial-6/scripts/encounter.py show
```

**Output:**
```
============================================================
ENCOUNTER STATE - Round 2
============================================================

Heroes:
  • Aria                HP: 5/8
  • Theron              HP: 8/13
  • Bob                 HP: 10/10

Foes:
  • Goblin-1            💀 DEFEATED
  • Goblin-2            HP: 0/7, AC: 15
  • Goblin-3            HP: 4/7, AC: 15

============================================================
Current turn: Bob (Hero)
============================================================
```

### Step 8: Combat Ends Automatically

When all foes or all heroes are defeated, encounter.py ends combat and outputs results:

**Output (Victory):**
```
============================================================
ENCOUNTER ENDED: VICTORY!
============================================================

📊 Combat Summary:
  Rounds: 3
  Total XP: 150
  XP per hero: 50

📄 Results saved to: encounter-results.json

💡 Update characters with:
  progression.py award Aria 50
  progression.py award Theron 50
  progression.py award Bob 50
```

### Step 9: Apply XP Awards

```bash
# Update each character
python3 ~/.claude/skills/tutorial-6/scripts/progression.py award Aria 50
python3 ~/.claude/skills/tutorial-6/scripts/progression.py award Theron 50
python3 ~/.claude/skills/tutorial-6/scripts/progression.py award Bob 50
```

Characters may level up if XP threshold reached (see Tutorial 5 for leveling mechanics).

## State Files

encounter.py creates two files during combat:

**encounter-state.json** - Active combat state (turn-by-turn)
```json
{
  "round": 2,
  "turn_index": 3,
  "combatants": [
    {"name": "Theron", "type": "hero", "hp_current": 8, "hp_max": 13, ...},
    {"name": "Goblin-1", "type": "foe", "hp_current": 0, "is_defeated": true, ...},
    ...
  ],
  "combat_log": [...]
}
```

**encounter-results.json** - Final results (created when combat ends)
```json
{
  "outcome": "victory",
  "rounds": 3,
  "heroes": [
    {"name": "Aria", "hp_final": 5, "hp_max": 8, "xp_earned": 50},
    ...
  ],
  "foes": [...],
  "total_xp": 150,
  "xp_per_hero": 50
}
```

## Commands Reference

### Party Management (party.py)

```bash
# Create party
party.py create PARTY_ID NAME [--description DESC]

# Add member
party.py add PARTY_ID CHARACTER_NAME [--force]

# Remove member
party.py remove CHARACTER_NAME

# Show party
party.py show PARTY_ID

# List all parties
party.py list

# Export to JSON
party.py export PARTY_ID > heroes.json

# Delete party
party.py delete PARTY_ID
```

### Bestiary Management (bestiary.py)

```bash
# Export monsters to JSON
bestiary.py export MONSTER [MONSTER ...] > foes.json

# Example: 3 goblins and 1 orc
bestiary.py export Goblin Goblin Goblin Orc > foes.json
# Output: Goblin-1, Goblin-2, Goblin-3, Orc

# Other commands from Tutorial 5
bestiary.py seed
bestiary.py list [--max-cr CR]
bestiary.py show MONSTER_NAME
```

### Encounter Combat (encounter.py)

```bash
# Start encounter
encounter.py start HEROES_FILE FOES_FILE

# Character attack
encounter.py attack CHARACTER TARGET [WEAPON]

# Character cast spell
encounter.py cast CHARACTER SPELL TARGET

# Show current state
encounter.py show
```

## Narrative Style

Use the **radio drama** narrative style for combat descriptions. See `references/narrative-guide.md` for detailed guidance on creating vivid, cinematic combat narration.

**Example narration:**
```
The goblins spring from the shadows! Theron draws his longsword as the creatures shriek
and charge. Aria's hands crackle with arcane energy while Bob raises his holy symbol.

[Initiative rolled]

Theron strikes first! His blade flashes in the dim light, cleaving through Goblin-1's
leather armor. The creature collapses with a final wheeze.

The remaining goblins counterattack! One's scimitar clangs off Theron's shield, but the
other finds a gap in his armor. Blood flows from a shallow cut across his shoulder.

"Burn!" shouts Aria, launching a bolt of flame at Goblin-2...
```

## Example JSON Files

Tutorial 6 includes ready-to-use encounter files in `examples/`:

- **heroes-level1.json** - Level 1 starting party (Aria, Theron, Bob)
- **foes-goblin-ambush.json** - 3 Goblins (CR 1/4 each, easy)
- **foes-orc-warband.json** - 2 Orcs (CR 1/2 each, medium)

Use these for quick testing or as templates for custom encounters.

## Troubleshooting

### "No active encounter found"

You need to start an encounter first:
```bash
encounter.py start heroes.json foes.json
```

### "Not CHARACTER's turn"

Check turn order with `encounter.py show`. Only the current character can act.

### "Target not found"

Verify target name exactly matches (case-sensitive). Use `encounter.py show` to see combatant names.

### "Monster already defeated"

Cannot target defeated foes. Choose a different target.

## Important Notes

- **Database location**: `~/.claude/data/dnd-dm.db`
- **State persistence**: encounter-state.json tracks active combat
- **Monster AI**: Automatically targets hero with lowest HP
- **Physical attacks only**: Monster spellcasting saved for later tutorial
- **XP split evenly**: All heroes get equal share, including defeated ones
- **Defeated heroes**: Can still earn XP if party wins

## Reference Documentation

For detailed information on specific topics, see:

- **`references/collection-management.md`** - Managing multiple entities, iteration patterns, filtering, bulk updates
- **`references/priority-queues.md`** - Initiative system, dynamic priorities, turn order, real-world applications
- **`references/state-synchronization.md`** - Keeping state consistent, atomic operations, cascading updates
- **`references/narrative-guide.md`** - Radio drama combat narrative style for party encounters

Load these references as needed when conducting party combat encounters.

## Error Handling

Handle these common scenarios:

- **No party members**: Suggest creating party and adding characters
- **No monsters in bestiary**: Run seed command
- **JSON parse errors**: Validate heroes.json and foes.json format
- **Encounter already active**: Finish or delete encounter-state.json
- **Character not found**: Check character.py list

## Extension Ideas

Once you've completed this tutorial, try extending it:

1. **AOE Spells** - Fireball hits multiple targets, apply damage to all
2. **Healing Spells** - Cure Wounds during combat (not just end)
3. **Conditions** - Stunned, prone, poisoned affecting combat
4. **Monster Spellcasting** - Add spellcasting monsters with AI spell selection
5. **Terrain/Cover** - Modify AC based on cover, difficult terrain slows movement
6. **Death Saving Throws** - Defeated heroes make death saves instead of instant death
7. **Encounter Templates** - Pre-built encounters from encounter_tables.json

## What's Next?

**Tutorial 7: Advanced Combat Mechanics** will teach:
- **Reactions** - Opportunity attacks, Shield spell, Counterspell
- **Legendary Actions** - Boss monsters with extra actions
- **Monster Spellcasting** - AI decides when to cast vs attack
- **Conditions and Status Effects** - Stunned, paralyzed, poisoned
- **Environmental Hazards** - Traps, lava, collapsing ceilings

You'll build complex boss encounters with mechanics that challenge even experienced players.
